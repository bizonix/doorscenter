# coding=utf8
import os, sys, time, random, shlex, argparse, threading, Queue
import pinterest, amazon, schedule, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class PinterestBoard(object):  # workaround for serialization
    pass

class PlannedCommonBoard(object):
    pass

class PlannedProfitBoard(object):
    pass


class LauncherSingle(object):
    '''Запускаем бота - одна команда'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.bot = pinterest.PinterestBot(printPrefix)
        self.loggedIn = False
    
    def Parse(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--user', required=True, help='login or email; you must specify logins (or emails), passwords and proxy (if needed) in "users.txt"')
        parser.add_argument('--action', required=True, choices=['follow-users', 'unfollow-users', 'follow-boards', 'like-pins', 'repost-pins', 'comment-pins', 'post-amazon', 'user-info'], help='action to execute')
        parser.add_argument('--count', default=1, type=int, help='actions count to execute, 1 action by default; you may specify minimum and maximum actions')
        parser.add_argument('--count-min', default=1, type=int, help='minimal actions count to execute, 1 action by default')
        parser.add_argument('--count-max', default=1, type=int, help='maximum actions count to execute, 1 action by default')
        parser.add_argument('--keywords', default='', help='comma-separated keywords for scraping people, boards and pins; see also "--category"')
        parser.add_argument('--category', default='', help='you may specify a category for scraping instead of keywords; use "popular" for scraping popular pins')
        parser.add_argument('--boards', default='', help='comma-separated board names for repinning and posting new pins; you may specify a category after the colon sign')
        parser.add_argument('--department', default='All', help='amazon department for scraping items')
        parser.add_argument('--batch-file', default='', help='commands file name for batch mode')  # аргумент нужен только для справки, реально используется только в LauncherBatch
        parser.add_argument('--threads', type=int, default=5, help='threads count for batch mode, 5 threads by default')  # аргумент нужен только для справки, реально используется только в LauncherBatch
        parser.add_argument('--test-mode', action='store_true', help='test (or demo) mode, executes all available commands')  # аргумент нужен только для справки, реально используется только в LauncherTest
        parser.epilog = 'Pinterest categories list: %s.\n\nAmazon departments list: %s.' % (', '.join(pinterest.boardCategoriesList), ', '.join(amazon.departmentsList))
        
        args = parser.parse_args(argumentsList)
        self.userLogin = args.user
        self.action = args.action
        self.actionsCount = args.count
        self.actionsCountMin = args.count_min
        self.actionsCountMax = args.count_max
        self.keywordsList = args.keywords.split(',')
        self.category = args.category
        self.boardsList = args.boards.split(',')
        self.amazonDepartment = args.department
    
    def Execute(self, argumentsList):
        '''Выполняем команду'''
        if argumentsList != []:
            self.Parse(argumentsList)
        try:
            '''Логинимся'''
            if self.bot.user.login != self.userLogin:
                self.loggedIn = False
            if not self.loggedIn:
                if self.bot.Login(self.userLogin):
                    self.loggedIn = True
                else:
                    raise Exception('Cannot log in with user "%s"' % self.userLogin)
            
            '''Выполняем команду'''
            if (self.actionsCountMin != 1) or (self.actionsCountMax != 1):
                self.actionsCount = random.randint(self.actionsCountMin, self.actionsCountMax)
            if self.action == 'follow-users':
                self.bot.FollowUsers(self.keywordsList, self.category, self.actionsCount)
            elif self.action == 'unfollow-users':
                self.bot.UnfollowUsers(self.actionsCount)
            elif self.action == 'follow-boards':
                self.bot.FollowBoards(self.keywordsList, self.category, self.actionsCount)
            elif self.action == 'like-pins':
                self.bot.LikePins(self.keywordsList, self.category, self.actionsCount)
            elif self.action == 'repost-pins':
                self.bot.RepostPins(self.keywordsList, self.category, self.actionsCount, self.boardsList)
            elif self.action == 'comment-pins':
                self.bot.CommentPins(self.keywordsList, self.category, self.actionsCount)
            elif self.action == 'post-amazon':
                self.bot.PostFromAmazon(self.keywordsList, self.actionsCount, self.boardsList, self.amazonDepartment)
            elif self.action == 'user-info':
                self.bot.ShowUserInfo()
            else:
                raise Exception('Unknown action')
        except Exception as error:
            self.bot._Print('### Error running a command: %s' % error)


class LauncherSingleThreaded(threading.Thread):
    '''Запускаем бота - одна команда в потоке'''
    
    def __init__(self, parent, commandsQueue, threadNumber):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.commandsQueue = commandsQueue
        self.threadNumber = threadNumber
        self.printPrefix = 'Thread #%d - ' % self.threadNumber + (' ' * ((self.threadNumber - 1) * 4))
        self.launcher = LauncherSingle(self.printPrefix)
        self._ClearLoginAndProxy()
    
    def _Print(self, text):
        '''Thread-safe print'''
        common.threadLock.acquire()
        print(self.printPrefix + text)
        common.threadLock.release()
    
    def _ClearLoginAndProxy(self):
        '''Очищаем юзера и прокси'''
        self.launcher.userLogin = ''
        self.launcher.proxyHost = ''
    
    def RunningUserOrProxy(self, userLogin, proxyHost):
        '''Проверяем, выполняется ли команда с этим юзером или прокси'''
        return (self.launcher.userLogin == userLogin) or (self.launcher.proxyHost == proxyHost)
    
    def run(self):
        '''Главный метод'''
        self._Print('Thread started')
        while not self.commandsQueue.empty():
            command = self.commandsQueue.get()
            argumentsList = shlex.split(command)
            self.launcher.Parse(argumentsList)
            while not self.parent.ExecutionAllowed(self, self.launcher.userLogin, self.launcher.proxyHost):
                self._Print('User "%s" or proxy "%s" is being used in another thread, waiting ...')
                time.sleep(60)
            self.launcher.Execute([])
            self._ClearLoginAndProxy()
            self.commandsQueue.task_done()
        self.parent.ThreadFinished(self)
        self._Print('Thread finished')


class LauncherThreaded(object):
    '''Запускаем команды в несколько потоков'''
    
    def __init__(self):
        '''Инициализация'''
        self.threadsList = []
        self.threadsNumbersList = []
    
    def _GetThreadNumber(self):
        '''Находим минимальный свободный номер для потока'''
        threadNumber = 1
        while threadNumber in self.threadsNumbersList:
            threadNumber += 1
        self.threadsNumbersList.append(threadNumber)
        return threadNumber
    
    def _ReleaseThreadNumber(self, threadNumber):
        '''Удаляем номер из списка занятых'''
        if threadNumber in self.threadsNumbersList:
            self.threadsNumbersList.remove(threadNumber)
    
    def Launch(self, commandsList, threadsCount):
        '''Запускаем команды в несколько потоков, в дополнение к уже существующим потокам.
        Возвращаем очередь команд.'''
        commandsQueue = Queue.Queue()
        for command in commandsList:
            commandsQueue.put(command)
        for _ in range(threadsCount):
            thread = LauncherSingleThreaded(self, commandsQueue, self._GetThreadNumber())
            self.threadsList.append(thread)
            thread.start()
        return commandsQueue
    
    def ExecutionAllowed(self, callingThread, userLogin, proxyHost):
        '''Проверяем, выполняются ли команды с этим юзером или прокси'''
        common.threadLock.acquire()
        result = True
        for thread in self.threadsList:
            if thread != callingThread:
                if thread.RunningUserOrProxy(userLogin, proxyHost):
                    result = False
                    break
        common.threadLock.release()
        return result
    
    def ThreadFinished(self, thread):
        '''Выполнение потока завершено'''
        common.threadLock.acquire()
        try:
            self._ReleaseThreadNumber(thread.threadNumber)
            if thread in self.threadsList:
                self.threadsList.remove(thread)
        except Exception as error:
            print('### Error: %s' % error)
        common.threadLock.release()


class LauncherBatch(object):
    '''Запускаем бота - команды по списку из файла'''
    
    def __init__(self):
        '''Инициализация'''
        self.commandsQueue = None
    
    def Parse(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--batch-file', required=True, help='commands file name for batch mode')
        parser.add_argument('--threads', type=int, default=5, help='threads count for batch mode, 5 threads by default')
        
        args = parser.parse_args(argumentsList)
        self.batchFileName = args.batch_file
        self.threadsCount = args.threads
        
        self.commandsList = []
        if os.path.exists(self.batchFileName):
            self.commandsList = common.CommandsListFromText(open(self.batchFileName).read())
            self.threadsCount = min(self.threadsCount, len(self.commandsList))
        else:
            print('### Error parsing batch file: File "%s" not found' % self.batchFileName)
    
    def Execute(self, argumentsList):
        '''Выполняем команды'''
        if argumentsList != []:
            self.Parse(argumentsList)
        if len(self.commandsList) == 0:
            return
        print('=== Executing commands from "%s"' % self.batchFileName)
        launcher = LauncherThreaded()
        commandsQueue = launcher.Launch(self.commandsList, self.threadsCount)
        commandsQueue.join()
        print('=== Done commands from "%s"' % self.batchFileName)


class LauncherSchedule(object):
    '''Запускаем ботов по расписанию'''

    def __init__(self):
        '''Инициализация'''
        pass
    
    def Parse(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--schedule-execute', default=False, action='store_true', help='run scheduled tasks')
        parser.add_argument('--schedule-generate', default=False, action='store_true', help='generate new schedule')
        parser.add_argument('--generate-users', default=1000000, type=int, help='users count for generating schedule, all by default')
        parser.add_argument('--generate-days', default=1, type=int, help='days count for generating schedule, 1 day by default')
        
        args = parser.parse_args(argumentsList)
        self.scheduleExecute = args.schedule_execute
        self.scheduleGenerate = args.schedule_generate
        self.generateUsers = args.generate_users
        self.generateDays = args.generate_days
    
    def Execute(self, argumentsList):
        '''Выполняем команду'''
        if argumentsList != []:
            self.Parse(argumentsList)
        scheduleObj = schedule.Schedule()
        if self.scheduleExecute:
            launcher = LauncherThreaded()
            while True:  # бесконечный цикл: в режиме выполнения расписания бота надо запустить один раз, а не ставить на крон
                fileName = scheduleObj.FindNext()
                if fileName:
                    launcher.Launch(common.CommandsListFromText(open(fileName).read()), 1)
                time.sleep(60)
        if self.scheduleGenerate:
            scheduleObj.Generate(self.generateUsers, self.generateDays)


class LauncherTest(object):
    '''Запускаем тест'''
    
    def __init__(self):
        '''Инициализация'''
        pass
    
    def Parse(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--user', required=True, help='user\'s login or email')
        parser.add_argument('--keywords', required=True, help='keywords for testing')
        parser.add_argument('--category', required=True, help='category for testing')
        parser.add_argument('--boards', required=True, help='boards for testing')
        parser.add_argument('--department', required=True, help='amazon department for scraping items')
        parser.add_argument('--test-mode', required=True, action='store_true', help='test (or demo) mode, executes all available commands')
        
        args = parser.parse_args(argumentsList)
        self.userLogin = args.user
        self.keywords = args.keywords
        self.category = args.category
        self.boards = args.boards
        self.department = args.department
        
        self.commands =  '''
            --user=%LOGIN% --action=follow-users --count=1 --category="%CATEGORY%"
            --user=%LOGIN% --action=follow-users --count=1 --keywords="%KEYWORDS%"
            --user=%LOGIN% --action=unfollow-users --count=1
            --user=%LOGIN% --action=follow-boards --count=1 --category=%CATEGORY%
            --user=%LOGIN% --action=follow-boards --count=1 --keywords="%KEYWORDS%"
            --user=%LOGIN% --action=like-pins --count=1 --category=%CATEGORY%
            --user=%LOGIN% --action=like-pins --count=1 --keywords="%KEYWORDS%"
            --user=%LOGIN% --action=repost-pins --count=1 --category=%CATEGORY% --boards="%BOARDS%"
            --user=%LOGIN% --action=repost-pins --count=1 --keywords="%KEYWORDS%" --boards="%BOARDS%"
            --user=%LOGIN% --action=comment-pins --count=1 --category=%CATEGORY%
            --user=%LOGIN% --action=comment-pins --count=1 --keywords="%KEYWORDS%"
            --user=%LOGIN% --action=post-amazon --count=1 --keywords="%KEYWORDS%" --boards="%BOARDS%" --department=%DEPARTMENT%
            --user=%LOGIN% --action=user-info
        '''
        self.commands = self.commands.replace('%LOGIN%', self.userLogin)
        self.commands = self.commands.replace('%KEYWORDS%', self.keywords)
        self.commands = self.commands.replace('%CATEGORY%', self.category)
        self.commands = self.commands.replace('%BOARDS%', self.boards)
        self.commands = self.commands.replace('%DEPARTMENT%', self.department)
        self.commandsList = common.CommandsListFromText(self.commands)
    
    def Execute(self, argumentsList):
        '''Выполняем команды'''
        if argumentsList != []:
            self.Parse(argumentsList)
        if len(self.commandsList) == 0:
            return
        print('=== Running test mode')
        launcher = LauncherThreaded()
        commandsQueue = launcher.Launch(self.commandsList, 1)
        commandsQueue.join()
        print('=== Done test mode')


def Dispatcher(command=None):
    '''Точка входа'''
    if command:
        argumentsList = shlex.split(command)
    else:
        argumentsList = sys.argv[1:]
        command = ' '.join(argumentsList)
    if command.find('--batch') >= 0:
        launcher = LauncherBatch()
    elif command.find('--schedule') >= 0:
        launcher = LauncherSchedule()
    elif command.find('--test') >= 0:
        launcher = LauncherTest()
    else:
        launcher = LauncherSingle()
    launcher.Execute(argumentsList)
    sys.exit()  # для упрощения разработки и отладки - предотвращаем повторный запуск


if __name__ == '__main__':
    Dispatcher()
    if not common.DevelopmentMode():
        Dispatcher()
    command = '--user=searchxxx --keywords=shoes --category=design --boards="For the Home,My Home" --test-mode'
    Dispatcher(command)
