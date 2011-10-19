# coding=utf8
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from doorsadmin.models import Agent, EventLog, ObjectLog, GetObjectByTaskType
import pickle, datetime, base64

@transaction.commit_manually
def get(request, agentId):
    '''Получить задание из очереди'''
    agent = get_object_or_404(Agent, pk=agentId)
    try:
        '''Пишем дату пинга'''
        agent.dateLastPing = datetime.datetime.now()
        agent.stateSimple = 'ok'
        agent.save()
        transaction.commit()
        '''Ищем задание'''
        if agent.active:
            for queue in agent.GetQueues(): 
                tasksList = queue.GetTasksList()
                if tasksList:
                    task = tasksList[0]
                    '''Обновляем задание'''
                    task.agent = agent
                    task.stateManaged = 'inproc'
                    task.save()
                    ObjectLog(task, 'Change state to "%s".' % task.stateManaged)
                    '''Формируем текст задания для агента'''
                    data = task.GetTaskDetails()
                    data['id'] = task.pk
                    data['type'] = task.__class__.__name__
                    data['state'] = task.stateManaged
                    data['error'] = task.lastError
                    '''Обновляем агента'''
                    agent.currentTask = '%s #%s' % (data['type'], data['id'])
                    agent.save()
                    ObjectLog(agent, agent.currentTask)
                    transaction.commit()
                    '''Формируем ответ'''
                    return HttpResponse(base64.b64encode(pickle.dumps(data)))
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
        agent.stateSimple = 'ok'
        agent.save()
        transaction.commit()
        '''Обновляем задание'''
        data = pickle.loads(base64.b64decode(request.POST['data']))
        task = GetObjectByTaskType(data['type']).objects.get(pk=data['id'])
        try:
            task.SetTaskDetails(data)
        except Exception as errorHandle:
            data['state'] = 'error'
            data['error'] += '. Handle error:' + str(errorHandle)
        task.stateManaged = data['state']
        task.lastError = data['error']
        task.runTime = data['runTime']
        task.save()
        if task.stateManaged == 'error':
            EventLog(task.stateManaged, task.lastError, task)
        ObjectLog(task, 'Change state to "%s".' % task.stateManaged)
        '''Обновляем агента'''
        agent.currentTask = 'idle'
        agent.save()
        ObjectLog(agent, agent.currentTask)
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

@transaction.commit_manually
def ping(request, agentId):
    '''Обновить состояние задания'''
    agent = get_object_or_404(Agent, pk=agentId)
    try:
        '''Пишем дату пинга'''
        agent.dateLastPing = datetime.datetime.now()
        agent.stateSimple = 'ok'
        agent.save()
        transaction.commit()
        '''Формируем ответ'''
        return HttpResponse('ok')
    except Exception as error:
        EventLog('error', 'Cannot handle "ping" request', None, error)
    transaction.rollback()
    '''Формируем ответ'''
    return HttpResponse('error')
