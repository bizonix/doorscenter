# coding=utf8
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from doorsadmin.models import Agent, EventLog, GetObjectByTaskType
import pickle, datetime, base64

@transaction.commit_manually
def get(request, agentId):
    '''Получить задание из очереди'''
    agent = get_object_or_404(Agent, pk=agentId)
    try:
        '''Пишем дату пинга'''
        agent.dateLastPing = datetime.datetime.now()
        agent.ipAddress = request.META['REMOTE_ADDR']
        agent.stateSimple = 'ok'
        agent.save()
        transaction.commit()
        '''Ищем задание'''
        if agent.active:
            for queue in agent.GetQueues(): 
                '''Очередь возвращает порцию заданий для агента'''
                tasksList = queue.GetTasksList(agent)
                if len(tasksList) > 0:
                    tasksDataList = []
                    for task in tasksList:
                        '''Обновляем задание'''
                        task.agent = agent
                        task.stateManaged = 'inproc'
                        task.save()
                        '''Формируем текст задания для агента'''
                        taskData = task.GetTaskDetails()
                        taskData['id'] = task.pk
                        taskData['type'] = task.__class__.__name__
                        taskData['state'] = task.stateManaged
                        taskData['error'] = task.lastError
                        agent.AppendParams(taskData)
                        '''Добавляем текст задания в список заданий'''
                        tasksDataList.append(taskData)
                    '''Обновляем агента'''
                    tasksType = tasksDataList[0]['type']
                    tasksIdsList = [str(item['id']) for item in tasksDataList]
                    agent.currentTask = '%s #%s' % (tasksType, ','.join(tasksIdsList))
                    agent.save()
                    transaction.commit()
                    '''Формируем ответ'''
                    return HttpResponse(base64.b64encode(pickle.dumps(tasksDataList)))
    except Exception as error:
        EventLog('error', 'Cannot handle "get" request', None, error)
    transaction.rollback()
    '''Формируем ответ'''
    return HttpResponse(base64.b64encode(pickle.dumps(None)))

@transaction.commit_manually
def update(request, agentId):
    '''Обновить состояние задания'''
    agent = get_object_or_404(Agent, pk=agentId)
    try:
        '''Пишем дату пинга'''
        agent.dateLastPing = datetime.datetime.now()
        agent.ipAddress = request.META['REMOTE_ADDR']
        agent.stateSimple = 'ok'
        agent.save()
        transaction.commit()
        '''Обновляем задания'''
        tasksDataList = pickle.loads(base64.b64decode(request.POST['data']))
        for taskData in tasksDataList:
            task = GetObjectByTaskType(taskData['type']).objects.get(pk=taskData['id'])
            try:
                task.SetTaskDetails(taskData)
            except Exception as errorHandle:
                taskData['state'] = 'error'
                taskData['error'] += '. The task handling error:' + str(errorHandle)
            task.stateManaged = taskData['state']
            task.lastError = taskData['error']
            task.runTime = taskData['runTime']
            task.save()
            if task.stateManaged == 'error':
                EventLog(task.stateManaged, task.lastError, task)
        '''Обновляем агента'''
        agent.currentTask = 'idle'
        agent.save()
        '''Дергаем событие'''
        try:
            agent.OnUpdate()
        except Exception as error:
            EventLog('error', 'Error in "OnUpdate" event', agent, error)
        transaction.commit()
        '''Формируем ответ'''
        return HttpResponse('ok')
    except Exception as error:
        EventLog('error', 'Cannot handle "update" request', agent, error)
    transaction.rollback()
    '''Формируем ответ'''
    return HttpResponse('error')
