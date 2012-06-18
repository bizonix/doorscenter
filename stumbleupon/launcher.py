# coding=utf8
import os, sys, time, random, shlex, argparse, threading, Queue
import pinterest, amazon, schedule, common
from pinterest import PinterestBoard, PlannedCommonBoard, PlannedProfitBoard  # workaround for unserialization

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

WAIT_TIMEOUT = 60 * 60 * 24 * 7  # cм. комментарий в common

proxiesCondition = threading.Condition()
proxiesUsingSet = set()

screenSlotsCondition = threading.Condition()
screenSlotsList = range(20)  # также ограничение общего числа работающих потоков

class LauncherSingle(object):
    '''Запускаем бота - одна команда'''
    
    def __init__(self):
        '''Инициализация'''
        self.screenSlotAcquired = None
        self._AcquireScreenSlot()
        self.loggedIn = False
        self.proxyHostAcquired = None
        self.bot = pinterest.PinterestBot(self.screenSlotAcquired)
    
    def __del__(self):
        '''Деструктор, освобождаем прокси и слот'''
        try:
            self._ReleaseProxy()
        except Exception:
            pass
        try:
            self._ReleaseScreenSlot()
        except Exception:
            pass
    
    def _AcquireScreenSlot(self):
        '''Захватываем слот вывода на экран'''
        if self.screenSlotAcquired != None:
            return
        screenSlotsCondition.acquire()
        try:
            while len(screenSlotsList) == 0:
                screenSlotsCondition.wait(WAIT_TIMEOUT)
            self.screenSlotAcquired = screenSlotsList.pop(0)
        finally:
            screenSlotsCondition.release()
    
    def _ReleaseScreenSlot(self):
        '''Освобождаем захваченный слот'''
        if self.screenSlotAcquired == None:
            return
        screenSlotsCondition.acquire()
        try:
            screenSlotsList.append(self.screenSlotAcquired)
            screenSlotsList.sort()
            screenSlotsCondition.notifyAll()
        finally:
            screenSlotsCondition.release()
    
    def _AcquireProxy(self, proxyHost):
        '''Ждем освобожения требуемого прокси и захватываем его'''
        if proxyHost == self.proxyHostAcquired:
            return
        proxiesCondition.acquire()
        try:
            if proxyHost in proxiesUsingSet:
                self.bot._Print('Proxy "%s" is already used in another thread, waiting ...' % proxyHost)
            while proxyHost in proxiesUsingSet:
                proxiesCondition.wait(WAIT_TIMEOUT)
            proxiesUsingSet.add(proxyHost)
            self.proxyHostAcquired = proxyHost
        finally:
            proxiesCondition.release()
        self.bot._Print('Proxy "%s" acquired' % proxyHost)
    
    def _ReleaseProxy(self):
        '''Освобождаем захваченный прокси'''
        if self.proxyHostAcquired == None:
            return
        self.bot._Print('Proxy "%s" released' % self.proxyHostAcquired)
        proxiesCondition.acquire()
        try:
            proxiesUsingSet.remove(self.proxyHostAcquired)
            proxiesCondition.notifyAll()
        finally:
            proxiesCondition.release()
    
    def Execute(self, argumentsList):
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
        parser.epilog = 'Pinterest categories list: %s.\n\nAmazon departments list: %s.' % (', '.join(pinterest.boardCategoriesList), ', '.join(amazon.departmentsList))
        
        args = parser.parse_args(argumentsList)
        userLogin = args.user
        action = args.action
        actionsCount = args.count
        actionsCountMin = args.count_min
        actionsCountMax = args.count_max
        if (actionsCountMin != 1) or (actionsCountMax != 1):
            actionsCount = random.randint(actionsCountMin, actionsCountMax)
        keywordsList = args.keywords.split(',')
        category = args.category
        boardsList = args.boards.split(',')
        department = args.department
        
        try:
            '''Логинимся, а также операции с прокси. Блокируем и освобождаем прокси только при смене юзера, освобождаем также в деструкторе'''
            userProxy = self.bot.user.GetProxyHostByLogin(userLogin)
            if self.bot.user.login != userLogin:
                self._ReleaseProxy()
                self.loggedIn = False
            self._AcquireProxy(userProxy)
            if not self.loggedIn:
                if self.bot.Login(userLogin):
                    self.loggedIn = True
                else:
                    raise Exception('Cannot log in with user "%s"' % userLogin)
            
            '''Выполняем команду'''
            if action == 'follow-users':
                self.bot.FollowUsers(keywordsList, category, actionsCount)
            elif action == 'unfollow-users':
                self.bot.UnfollowUsers(actionsCount)
            elif action == 'follow-boards':
                self.bot.FollowBoards(keywordsList, category, actionsCount)
            elif action == 'like-pins':
                self.bot.LikePins(keywordsList, category, actionsCount)
            elif action == 'repost-pins':
                self.bot.RepostPins(keywordsList, category, actionsCount, boardsList)
            elif action == 'comment-pins':
                self.bot.CommentPins(keywordsList, category, actionsCount)
            elif action == 'post-amazon':
                self.bot.PostFromAmazon(keywordsList, actionsCount, boardsList, department)
            elif action == 'user-info':
                self.bot.ShowUserInfo()
            else:
                raise Exception('Unknown action')
        except Exception as error:
            self.bot._Print('### Error running a command: %s' % error)


class LauncherSingleThreaded(threading.Thread):
    '''Запускаем бота - одна команда в потоке'''
    
    def __init__(self, parent, commandsQueue):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True  # cм. комментарий в common
        self.parent = parent
        self.commandsQueue = commandsQueue
        self.launcher = LauncherSingle()
    
    def run(self):
        '''Главный метод'''
        self.launcher.bot._Print('Thread started')
        while not self.commandsQueue.empty():
            command = self.commandsQueue.get()
            argumentsList = shlex.split(command)
            self.launcher.Execute(argumentsList)
            self.commandsQueue.task_done()
        self.launcher.bot._Print('Thread finished')


class LauncherListThreadedWait(threading.Thread):
    '''Ожидаем завершения обработки очереди и выводим текст'''
    
    def __init__(self, queue, text):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True  # cм. комментарий в common
        self.queue = queue
        self.text = text
    
    def run(self):
        '''Главный метод'''
        self.queue.join()
        common.ThreadSafePrint(self.text)


class LauncherListThreaded(object):
    '''Запускаем список команд в несколько потоков'''
    
    def Launch(self, description, commandsList, threadsCount, wait):
        '''Запускаем команды в несколько потоков, в дополнение к уже существующим потокам'''
        if (len(commandsList) == 0) or (threadsCount <= 0):
            return
        textStart = '=== Running %s' % description
        textFinish = '=== Done %s' % description
        
        common.ThreadSafePrint(textStart)
        commandsQueue = Queue.Queue()
        for command in commandsList:
            commandsQueue.put(command)
        for _ in range(threadsCount):
            LauncherSingleThreaded(self, commandsQueue).start()
        if wait:
            commandsQueue.join()
            common.ThreadSafePrint(textFinish)
        else:
            LauncherListThreadedWait(commandsQueue, textFinish).start()


class LauncherTest(object):
    '''Запускаем тест'''
    
    def Execute(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--user', required=True, help='user\'s login or email')
        parser.add_argument('--keywords', required=True, help='keywords for testing')
        parser.add_argument('--category', required=True, help='category for testing')
        parser.add_argument('--boards', required=True, help='boards for testing')
        parser.add_argument('--department', required=True, help='amazon department for scraping items')
        parser.add_argument('--test-mode', required=True, action='store_true', help='test (or demo) mode, executes all available commands')
        
        args = parser.parse_args(argumentsList)
        userLogin = args.user
        keywords = args.keywords
        category = args.category
        boards = args.boards
        department = args.department
        
        commands =  '''
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
        commands = commands.replace('%LOGIN%', userLogin)
        commands = commands.replace('%KEYWORDS%', keywords)
        commands = commands.replace('%CATEGORY%', category)
        commands = commands.replace('%BOARDS%', boards)
        commands = commands.replace('%DEPARTMENT%', department)
        commandsList = common.CommandsListFromText(commands)
    
        '''Выполняем список команд'''
        launcher = LauncherListThreaded()
        launcher.Launch('test mode', commandsList, 1, True)


class LauncherBatch(object):
    '''Запускаем бота - команды по списку из файла'''
    
    def Execute(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--batch-file', required=True, help='commands file name for batch mode')
        parser.add_argument('--threads', type=int, default=5, help='threads count for batch mode, 5 threads by default')
        
        args = parser.parse_args(argumentsList)
        batchFileName = args.batch_file
        threadsCount = args.threads
        
        if not os.path.exists(batchFileName):
            common.ThreadSafePrint('### Error: File "%s" not found' % batchFileName)
            return
        commandsList = common.CommandsListFromText(open(batchFileName).read())
        threadsCount = min(threadsCount, len(commandsList))
    
        '''Выполняем список команд'''
        launcher = LauncherListThreaded()
        launcher.Launch('batch file "%s"' % batchFileName, commandsList, threadsCount, True)


class LauncherSchedule(object):
    '''Запускаем ботов по расписанию. в режиме выполнения расписания бота надо запустить один раз, а не ставить на крон'''
    
    def Execute(self, argumentsList):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--schedule-generate', default=False, action='store_true', help='generate new schedule')
        parser.add_argument('--schedule-execute', default=False, action='store_true', help='run scheduled tasks')
        parser.add_argument('--generate-users', default=1000000, type=int, help='users count for generating schedule, all by default')
        parser.add_argument('--generate-days', default=1, type=int, help='days count for generating schedule, 1 day by default')
        
        args = parser.parse_args(argumentsList)
        scheduleExecute = args.schedule_execute
        scheduleGenerate = args.schedule_generate
        generateUsers = args.generate_users
        generateDays = args.generate_days
    
        '''Выполняем команду'''
        if scheduleGenerate:
            scheduleObj = schedule.ScheduleGenerator()
            scheduleObj.Generate(generateUsers, generateDays)
        elif scheduleExecute:
            scheduleObj = schedule.ScheduleIterator()
            launcher = LauncherListThreaded()
            while True:  # в любом случае необходимо дать завершиться потокам-демонам, cм. комментарий в common
                fileName = scheduleObj.Next()
                if fileName:
                    commandsList = common.CommandsListFromText(open(fileName).read())
                    launcher.Launch('schedule "%s"' % os.path.basename(fileName), commandsList, 1, False)
                else:
                    common.ThreadSafePrint('=== Waiting for a schedule ...')
                    time.sleep(60)


def Dispatcher(command=None):
    '''Точка входа'''
    if command:
        argumentsList = shlex.split(command)
    else:
        argumentsList = sys.argv[1:]
        command = ' '.join(argumentsList)
    
    '''Запускаем нужный launcher'''
    if command.find('--batch') >= 0:
        launcher = LauncherBatch()
    elif command.find('--schedule') >= 0:
        launcher = LauncherSchedule()
    elif command.find('--test') >= 0:
        launcher = LauncherTest()
    else:
        launcher = LauncherSingle()
    launcher.Execute(argumentsList)
    
    '''Предотвращаем повторный запуск для упрощения разработки и отладки'''
    sys.exit()


if __name__ == '__main__':
    Dispatcher()
    if not common.DevelopmentMode():
        Dispatcher()
    command = '--user=searchxxx --keywords=shoes --category=design --boards="For the Home,My Home" --test-mode'
    Dispatcher(command)
