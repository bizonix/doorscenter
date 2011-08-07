# coding=utf8
import os, sys, urllib, pickle, subprocess, datetime, base64
try:  # импорт требуется только на Windows
    from win32com.client import GetObject
except ImportError:
    pass

'''Для реализации агента требуется создать модуль с классом, унаследованным от 
BaseAgent, и переопределить в нем методы _ActionOn() и _ActionOff(). 

В первом методе надо устанавливать параметры контролируемого приложения и 
запускать его. В втором методе надо получать данные работы приложения. Данные 
для работы необходимо получать из/записывать в словарь self.currentTask. В 
целях уменьшения трафика и ускорения работы, из ответа можно удалять большие 
входные данные. 

В конце модуля должны быть следующие строки:

if __name__ == '__main__':
    agent = YourAgent('http://127.0.0.1:8000/doorsadmin', 1)

, где надо указать URL ЦА и номер агента в ЦА.

Передача параметров в/из агента:
Список входных/выходных параметров см. в методах агента GetTaskDetails и 
SetTaskDetails. Все строки должны передаваться в кодировке win-1251. Списки 
строк должны передаваться в виде list of strings, в конце строк не должно быть 
переводов строки. Ссылки передаются в формате html.

Настройка: 
1. Поставить на cron выполение скрипта "python26.exe youragent.py cron".
2. По завершении работы контролируемое приложение должно вызыват скрипт 
"python26.exe youragent.py done".    
'''

class BaseAgent(object):
    '''Базовый класс агентов'''
    
    def __init__(self, adminUrl, agentId):
        '''Конструктор'''
        self.agentId = agentId
        self.adminUrl = adminUrl
        self.actionUrl = r'%s/agents/%d/' % (self.adminUrl, self.agentId)
        
        self.currentTask = None
        self.currentTaskFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'CurrentTask'
        self.maintenanceFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'Maintenance'
        self._LoadCurrentTaskData()
        self._ProcessCommandLine()
    
    def _ProcessCommandLine(self):
        '''Обработка командной строки'''
        if len(sys.argv) > 1:
            if sys.argv[1] == 'cron':
                self._Cron()
            elif sys.argv[1] == 'done':
                self._Done()            
    
    def _IsMaintenanceMode(self):
        '''Режим поддержки'''
        return os.path.isfile(self.maintenanceFileName)
    
    def _IsHeavyLoad(self):
        '''...'''
        return False
        '''Есть ли в процессах тяжелые задачи'''
        try:
            heavyProcessesList = ['AGGRESSDoorgen.exe', 'xpymep.exe']
            processesList = GetObject('winmgmts:').InstancesOf('Win32_Process')
            processesNames = [process.Properties_('Name').Value.lower() for process in processesList]
            for processName in heavyProcessesList:
                if processName.lower() in processesNames:
                    return True
        except Exception:
            pass
        return False
        
    def _GetNextTask(self):
        '''Получить задание из очереди ЦА'''
        try:
            fd = urllib.urlopen(self.actionUrl + 'get')
            self.currentTask = pickle.loads(base64.b64decode(fd.read()))
            fd.close()
        except Exception as error:
            self.currentTask = None
            print('Error in _GetNextTask: %s' % error)
        self._SaveCurrentTaskData()
    
    def _ReportTaskState(self):
        '''Сообщить в ЦА о завершении текущего задания.
        state: done, error'''
        result = False
        try:
            data = urllib.urlencode({'data': base64.b64encode(pickle.dumps(self.currentTask))})
            fd = urllib.urlopen(self.actionUrl + 'update', data)
            reply = fd.read()
            fd.close()
            result = (reply == 'ok')
            print('Send data reply: %s' % reply)
        except Exception as error:
            print('Error in _ReportTaskState: %s' % error)
        return result
    
    def _ReportPing(self):
        '''Сделать пинг в случае, если не можем начать выполнение задания
        из-за загрузки сервера'''
        try:
            urllib.urlopen(self.actionUrl + 'ping').close()
        except Exception as error:
            print('Error in _ReportPing: %s' % error)
    
    def _LoadCurrentTaskData(self):
        '''Получить данные о текущем задании из локального хранилища'''
        self.currentTask = None
        try:
            if os.path.isfile(self.currentTaskFileName):
                with open(self.currentTaskFileName, 'r') as fd:
                    self.currentTask = pickle.load(fd)
        except Exception as error:
            print('Error in _LoadCurrentTaskData: %s' % error)
    
    def _SaveCurrentTaskData(self):
        '''Записать данные о текущем задании в локальное хранилище'''
        result = False
        try:
            with open(self.currentTaskFileName, 'w') as fd:
                pickle.dump(self.currentTask, fd)
            result = True
        except Exception as error:
            print('Error in _SaveCurrentTaskData: %s' % error)
        return result
    
    def _GetCurrentTaskId(self):
        '''Идентификатор текущего задания'''
        taskId = None
        try:
            taskId = self.currentTask['id']
        except Exception as error:
            print('Error in _GetCurrentTaskId: %s' % error)
        return taskId
    
    def _SetCurrentTaskState(self, state, error):
        '''Состояние текущего задания'''
        try:
            self.currentTask['state'] = state
            self.currentTask['error'] = error
        except Exception as error:
            print('Error in _SetCurrentTaskState: %s' % error)
    
    def _HasTask(self):
        '''Есть ли выполняющееся задание?'''
        return self.currentTask != None
    
    def _Cron(self):
        '''Метод вызывается по cron'''
        dts = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if not self._IsMaintenanceMode():
            if not self._HasTask():
                if not self._IsHeavyLoad():
                    self._GetNextTask()
                    if self._HasTask():
                        print('%s - Starting task #%s' % (dts, self._GetCurrentTaskId()))
                        try:
                            self.currentTask['timeStart'] = datetime.datetime.now()
                            self._SaveCurrentTaskData()
                            self._ActionOn()
                        except Exception as error:
                            print('Error: %s' % error)
                            self._SetCurrentTaskState('error', str(error))
                            self._ReportTaskState()
                    else:
                        print('%s - No tasks found' % dts)
                else:
                    print('%s - Heavy load detected' % dts)
                    self._ReportPing()
            else:
                print('%s - Task #%s is currently running' % (dts, self._GetCurrentTaskId()))
        else:
            print('%s - Maintenance mode' % dts)

    def _Done(self):
        '''Текущее задание выполнено'''
        dts = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if self._HasTask():
            print('%s - Finishing task #%s' % (dts, self._GetCurrentTaskId()))
            try:
                self.currentTask['runTime'] = (datetime.datetime.now() - self.currentTask['timeStart']).seconds
                self._SaveCurrentTaskData()
                if self._ActionOff():
                    self._SetCurrentTaskState('done', '')
                else:
                    self._SetCurrentTaskState('error', '')
            except Exception as error:
                print('Error: %s' % error)
                self._SetCurrentTaskState('error', str(error))
            if self._ReportTaskState():
                self.currentTask = None
                self._SaveCurrentTaskData()
        else:
            print('%s - No task is currently running' % dts)
    
    def _RunApp(self, path):
        '''Запускаем приложение и не ждем завершения. 
        По завершении наше приложение должно вызвать этот же скрипт с 
        агрументом командной строки "done".'''
        print('Running %s...' % path)
        subprocess.Popen('start ' + path, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        
    def _ActionOn(self):
        '''Выполнение полученного задания. Абстрактный метод'''
        return True
    
    def _ActionOff(self):
        '''Выполнение полученного задания. Абстрактный метод'''
        return True
    
class SomeAgent(BaseAgent):
    '''Пример агента'''
    def _ActionOn(self):
        return True
    def _ActionOff(self):
        self.currentTask['keywordsList'] = []
        self.currentTask['stopwordsList'] = []
        self.currentTask['spamLinksList'] = []
        return True

if __name__ == '__main__':
    agent = SomeAgent('http://127.0.0.1:8000/doorsadmin', 1)
