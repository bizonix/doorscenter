# coding=utf8
import os, sys, argparse, threading, Queue, time
import pinterest, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class LauncherSingle(object):
    '''Запускаем бота - одна команда'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.bot = pinterest.PinterestBot(printPrefix)
        self.loggedIn = False
    
    def Parse(self, command):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012')
        parser.add_argument('--email', required=True, help='user\'s email')
        parser.add_argument('--password', required=True, help='user\'s password')
        parser.add_argument('--action', required=True, choices=['follow-users', 'unfollow-users', 'follow-boards', 'like-pins', 'repost-pins', 'comment-pins', 'add-pins-amazon', 'report'], help='action to execute')
        parser.add_argument('--countmin', required=True, type=int, help='minimal actions count')
        parser.add_argument('--countmax', required=True, type=int, help='maximum actions count')
        parser.add_argument('--keywords', required=True, help='comma-separated keywords for scraping; use "popular" for liking, reposting and commenting popular pins')
        parser.add_argument('--boards', default='', help='comma-separated board names or keywords for repinning and posting')
        parser.add_argument('--department', default='All', help='amazon department for searching for goods')
        parser.add_argument('--proxy', default='', help='proxy host[:port]')
        parser.add_argument('--proxypwd', default='', help='proxy username:password')
        
        args = parser.parse_args(command.split(' '))
        self.userEmail = args.email
        self.userPassword = args.password
        self.action = args.action
        self.actionsCountMin = args.countmin
        self.actionsCountMax = args.countmax
        self.keywordsList = args.keywords.split(',')
        self.boardsList = args.boards.split(',')
        self.amazonDepartment = args.department
        self.proxyHost = args.proxy
        self.proxyPassword = args.proxypwd
    
    def Execute(self, command):
        '''Выполняем команду'''
        if command != 'parsed':
            self.Parse(command)
        try:
            '''Логинимся'''
            if self.bot.userData['email'] != self.userEmail:
                self.loggedIn = False
            if not self.loggedIn:
                if self.bot.Login(self.userEmail, self.userPassword, self.proxyHost, self.proxyPassword):
                    self.loggedIn = True
                else:
                    raise Exception('Cannot log in with user "%s"' % self.userEmail)
            
            '''Выполняем команду'''
            if self.action == 'follow-users':
                self.bot.FollowUsers(self.keywordsList, self.actionsCountMin, self.actionsCountMax)
            elif self.action == 'unfollow-users':
                self.bot.UnfollowUsers(self.actionsCountMin, self.actionsCountMax)
            elif self.action == 'follow-boards':
                self.bot.FollowBoards(self.keywordsList, self.actionsCountMin, self.actionsCountMax)
            elif self.action == 'like-pins':
                self.bot.LikePins(self.keywordsList, self.actionsCountMin, self.actionsCountMax)
            elif self.action == 'repost-pins':
                self.bot.RepostPins(self.keywordsList, self.actionsCountMin, self.actionsCountMax, self.boardsList)
            elif self.action == 'comment-pins':
                self.bot.CommentPins(self.keywordsList, self.actionsCountMin, self.actionsCountMax)
            elif self.action == 'add-pins-amazon':
                self.bot.AddPinsAmazon(self.keywordsList, self.actionsCountMin, self.actionsCountMax, self.boardsList, self.amazonDepartment)
            elif self.action == 'report':
                self.bot.Report()
            else:
                raise Exception('Unknown action')
        except Exception as error:
            self.bot._Print('### Error: %s' % error)


class LauncherSingleThreaded(threading.Thread):
    '''Запускаем бота - одна команда в потоке'''
    
    def __init__(self, batch, threadNumber):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.batch = batch
        self.threadNumber = threadNumber
        self.printPrefix = ' ' * ((self.threadNumber - 1) * 4) + 'Thread #%d - ' % self.threadNumber
        self.launcher = LauncherSingle(self.printPrefix)
    
    def run(self):
        '''Главный метод'''
        common.PrintThreaded(self.printPrefix + 'Thread started')
        while not self.batch.commandsQueue.empty():
            command = self.batch.commandsQueue.get()
            self.launcher.Parse(command)
            if self.batch.CommandAllowed(self.launcher.userEmail, self.launcher.proxyHost):
                self.launcher.Execute('parsed')
            else:
                self.batch.commandsQueue.put(command)
            self.batch.commandsQueue.task_done()
        common.PrintThreaded(self.printPrefix + 'Thread finished')


class LauncherBatch(object):
    '''Запускаем бота - команды по списку'''
    
    def __init__(self):
        '''Инициализация'''
        self.commandsQueue = None
    
    def Parse(self, command):
        '''Парсим команду'''
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012')
        parser.add_argument('--batchfile', required=True, help='commands file name for batch mode')
        parser.add_argument('--threads', type=int, default=5, help='threads count')
        
        args = parser.parse_args(command.split(' '))
        self.batchFileName = args.batchfile
        self.threadsCount = args.threads
        
        self.commandsList = []
        if os.path.exists(self.batchFileName):
            self.commandsList = open(self.batchFileName).read().splitlines()
            self.commandsList = [item.strip() for item in self.commandsList if item.strip() != '']
            #self.threadsCount = min(self.threadsCount, len(self.commandsList))
        else:
            common.PrintThreaded('### Error: File "%s" not found' % self.batchFileName)
    
    def Execute(self, command):
        '''Выполняем команды'''
        if command != 'parsed':
            self.Parse(command)
        if len(self.commandsList) == 0:
            return
        common.PrintThreaded('=== Executing commands from "%s" ...' % self.batchFileName)
        self.commandsQueue = Queue.Queue()
        for command in self.commandsList:
            self.commandsQueue.put(command)
        for n in range(self.threadsCount):
            LauncherSingleThreaded(self, n + 1).start()
        self.commandsQueue.join()
        common.PrintThreaded('=== Done commands from "%s".' % self.batchFileName)
    
    def CommandAllowed(self, userEmail, proxyHost):
        '''Проверяем, выполняются ли команды с этим юзером или прокси'''
        pass
        return True


def Dispatcher(command=None):
    '''Точка входа'''
    if not command:
        command = ' '.join(sys.argv[1:])
    if command.find('--batchfile') < 0:
        launcher = LauncherSingle()
    else:
        launcher = LauncherBatch()
    launcher.Execute(command)


if __name__ == '__main__':
    command = '--email=alex@altstone.com --password=kernel32 --action=follow-users --countmin=3 --countmax=5 --keywords=shoes,gucci'
    command = '--email=alex@altstone.com --password=kernel32 --action=follow-boards --countmin=3 --countmax=5 --keywords=shoes,gucci'
    command = '--email=alex@altstone.com --password=kernel32 --action=report --countmin=1 --countmax=1 --keywords='
    command = '--batchfile=commands.txt'
    Dispatcher(command)
