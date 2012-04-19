# coding=utf8
import os, sys, urllib, pickle, subprocess, datetime, base64

'''Для реализации агента требуется создать модуль с классом, унаследованным от BaseAgent, и переопределить в нем методы _ActionOn() и _ActionOff(). 

В первом методе надо устанавливать параметры контролируемого приложения и запускать его. В втором методе надо получать данные работы приложения. Данные 
для работы необходимо получать из/записывать в словарь self.currentTask. В целях уменьшения трафика и ускорения работы, из ответа можно удалять большие 
входные данные. В конце модуля должны быть следующие строки:

if __name__ == '__main__':
    agent = YourAgent('http://127.0.0.1:8000/doorsadmin')

, где надо указать URL ЦА. Номер агента в ЦА указывается в файле [AgentName]Number.

   Передача параметров в/из агента:

Список входных/выходных параметров см. в методах агента GetTaskDetails и SetTaskDetails. Все строки должны передаваться в кодировке win-1251. Списки 
строк должны передаваться в виде list of strings, в конце строк не должно быть переводов строки. Ссылки передаются в формате html.

   Настройка: 

1. Поставить на cron выполение скрипта "python26.exe youragent.py cron".
2. По завершении работы контролируемое приложение должно вызыват скрипт "python26.exe youragent.py done".    
'''

class BaseAgent(object):
    '''Базовый класс агентов'''
    
    def __init__(self, adminUrl):
        '''Конструктор'''
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # убираем буферизацию stdout

        self.agentNumberFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'Number'
        self.currentTaskFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'CurrentTask'
        self.tasksQueueInFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'TasksQueueIn'
        self.tasksQueueOutFileName = os.path.dirname(os.path.abspath(__file__)) + '/' + self.__class__.__name__ + 'TasksQueueOut'

        self.adminUrl = adminUrl
        self.agentId = int(open(self.agentNumberFileName).read().strip())
        self.actionUrl = r'%s/agents/%d/' % (self.adminUrl, self.agentId)
        
        self._LoadLocalData()
        self._ProcessCommandLine()
    
    def _ProcessCommandLine(self):
        '''Обработка командной строки'''
        if len(sys.argv) > 1:
            if sys.argv[1] == 'cron':
                self._Cron()
            elif sys.argv[1] == 'done':
                self._Done()            
    
    def _LoadLocalData(self):
        '''Получить текущие данные из локального хранилища'''
        self.currentTask = None
        self.tasksQueueIn = []
        self.tasksQueueOut = []
        try:
            if os.path.isfile(self.currentTaskFileName):
                with open(self.currentTaskFileName) as fd:
                    self.currentTask = pickle.load(fd)
            if os.path.isfile(self.tasksQueueInFileName):
                with open(self.tasksQueueInFileName) as fd:
                    self.tasksQueueIn = pickle.load(fd)
            if os.path.isfile(self.tasksQueueOutFileName):
                with open(self.tasksQueueOutFileName) as fd:
                    self.tasksQueueOut = pickle.load(fd)
        except Exception as error:
            print('Error in _LoadLocalData: %s' % error)
    
    def _SaveLocalData(self):
        '''Записать текущие данные в локальное хранилище'''
        result = False
        try:
            with open(self.currentTaskFileName, 'w') as fd:
                pickle.dump(self.currentTask, fd)
            with open(self.tasksQueueInFileName, 'w') as fd:
                pickle.dump(self.tasksQueueIn, fd)
            with open(self.tasksQueueOutFileName, 'w') as fd:
                pickle.dump(self.tasksQueueOut, fd)
            result = True
        except Exception as error:
            print('Error in _SaveLocalData: %s' % error)
        return result
    
    def _GetNextTask(self):
        '''Получить задание из локального списка, либо из очереди ЦА'''
        try:
            if not self._HasQueuedTasks():
                sys.stdout.write('- getting data ... ')
                fd = urllib.urlopen(self.actionUrl + 'get')
                self.tasksQueueIn = pickle.loads(base64.b64decode(fd.read()))
                self.tasksQueueOut = []
                fd.close()
                print('done')
            if self._HasQueuedTasks():
                self.currentTask = self.tasksQueueIn.pop(0)
        except Exception as error:
            self.currentTask = None
            print('Error in _GetNextTask: %s' % error)
        self._SaveLocalData()
    
    def _ReportTask(self):
        '''Записать информацию о завершении текущего задания в локальный список. По завершении очереди 
        сообщить в ЦА . state: done, error'''
        try:
            if self._HasTask():
                self.tasksQueueOut.append(self.currentTask)
            self.currentTask = None
            if not self._HasQueuedTasks():
                sys.stdout.write('- sending data ... ')
                data = urllib.urlencode({'data': base64.b64encode(pickle.dumps(self.tasksQueueOut))})
                fd = urllib.urlopen(self.actionUrl + 'update', data)
                reply = fd.read()
                fd.close()
                print(reply)
                if reply == 'ok':
                    self.tasksQueueOut = []
                else:
                    self.currentTask = {'reportError': True}
        except Exception as error:
            print('Error in _ReportTask: %s' % error)
            self.currentTask = {'reportError': True}
        self._SaveLocalData()
    
    def _GetCurrentTaskId(self):
        '''Получить идентификатор текущего задания'''
        try:
            return self.currentTask['id']
        except Exception:
            return None
    
    def _SetCurrentTaskState(self, state, error):
        '''Задать состояние текущего задания'''
        try:
            self.currentTask['state'] = state
            self.currentTask['error'] = error
        except Exception as error:
            print('Error in _SetCurrentTaskState: %s' % error)
    
    def _HasQueuedTasks(self):
        '''Есть ли задания в локальной очереди?'''
        try:
            return len(self.tasksQueueIn) > 0
        except Exception:
            return False
    
    def _HasTask(self):
        '''Есть ли выполняющееся задание?'''
        return (self.currentTask != None) and not self._HasReportError()
    
    def _HasReportError(self):
        '''Есть ли неудачно отправленный отчет?'''
        try:
            return 'reportError' in self.currentTask
        except Exception:
            return False
    
    def _Cron(self):
        '''Метод вызывается по cron'''
        dts = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if self._HasReportError():
            print('%s - Reporting again last tasks queue' % (dts))
            self._ReportTask()
        if not self._HasTask() and not self._HasReportError():
            self._GetNextTask()
            if self._HasTask():
                print('%s - Starting task #%s' % (dts, self._GetCurrentTaskId()))
                try:
                    self.currentTask['timeStart'] = datetime.datetime.now()
                    self.currentTask['runTime'] = 0
                    self._SaveLocalData()
                    self._ActionOn()
                except Exception as error:
                    print('Error: %s' % error)
                    self._SetCurrentTaskState('error', str(error))
                    self._ReportTask()
            else:
                print('%s - No tasks found' % dts)
        elif self._HasTask():
            print('%s - Task #%s is currently running' % (dts, self._GetCurrentTaskId()))

    def _Done(self):
        '''Текущее задание выполнено'''
        dts = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if self._HasTask():
            print('%s - Finishing task #%s' % (dts, self._GetCurrentTaskId()))
            try:
                self.currentTask['runTime'] = (datetime.datetime.now() - self.currentTask['timeStart']).seconds
                self._SaveLocalData()
                if self._ActionOff():
                    self._SetCurrentTaskState('done', '')
                else:
                    self._SetCurrentTaskState('error', '')
            except Exception as error:
                print('Error: %s' % error)
                self._SetCurrentTaskState('error', str(error))
            self._ReportTask()
        else:
            print('%s - No task is currently running' % dts)
    
    def _RunApp(self, path):
        '''Запускаем приложение и не ждем завершения. По завершении наше приложение должно вызвать этот же скрипт с 
        агрументом командной строки "done".'''
        subprocess.Popen(path, stdin=None, stdout=None, stderr=None)
        
    def _KillApp(self, imageName):
        '''Принудительное завершение работы приложения'''
        os.system('taskkill /im %s /f >nul 2>&1' % imageName)
        
    def _ActionOn(self):
        '''Выполнение полученного задания. Абстрактный метод'''
        return True
    
    def _ActionOff(self):
        '''Выполнение полученного задания. Абстрактный метод'''
        return True
