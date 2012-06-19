# coding=utf8
import os, time, shlex, threading, Queue
import stumbleupon, botschedule, common

class SocialBotCommand(object):
    '''Команда для бота'''
    
    '''Формат команды (cmd-line-like):
    1. Команда задается в виде строки.
    2. Части команды разделяются пробелами.
    3. Если одна из частей содержит пробелы, вся часть заключается в "двойные кавычки"
    4. Первая часть команды - имя публичного метода бота, остальные части - аргументы метода.'''
    
    def __init__(self, bot, command):
        '''Инициализация'''
        self.bot = bot
        self.command = command
    
    def Execute(self):
        '''Парсим и выполняем команду'''
        try:
            argumentsList = shlex.split(self.command)
            methodName = argumentsList.pop(0)
            if methodName.startswith('_'):
                raise Exception('Cannot execute a private method')
            if not hasattr(self.bot, methodName):
                raise Exception('Unknown bot method "%s"' % methodName)
            getattr(self.bot, methodName)(*argumentsList)
        except Exception as error:
            common.ThreadSafePrint('### Error: %s' % error)


class SocialBotThread(threading.Thread):
    '''Ботом заданного класса выполняем набор команд в отдельном потоке'''
    
    def __init__(self, botClass, commandsQueue):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True  # cм. комментарий в common
        self.bot = botClass()
        self.commandsQueue = commandsQueue
    
    def run(self):
        '''Главный метод'''
        self.bot._Print('Thread started')
        while not self.commandsQueue.empty():
            command = self.commandsQueue.get()
            SocialBotCommand(self.bot, command).Execute()
            self.commandsQueue.task_done()
        self.bot._Print('Thread finished')


class SocialBotLauncherWaitingThread(threading.Thread):
    '''Ожидаем завершения обработки очереди команд и выводим заданный текст'''
    
    def __init__(self, metaQueue, commandsQueue, text=None):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True  # cм. комментарий в common
        self.metaQueue = metaQueue
        self.commandsQueue = commandsQueue
        self.text = text
    
    def run(self):
        '''Главный метод'''
        self.commandsQueue.join()
        if self.text:
            common.ThreadSafePrint(self.text)
        self.metaQueue.task_done()


class SocialBotLauncher(object):
    '''Запускаем ботов в несколько потоков'''
    
    '''Варианты запуска:
    1. "One command - one bot". Используется при ручном запуске. Является подвидом "Many commands - many bots", когда в список команд помещается одна команда и запускается один поток.
    2. "One command - many bots". Т.н. "mass mode", когда одну и ту же команду надо выполнить несколькими аккаунтами. Напрямую не используется; для этого генерятся расписания, которые затем выполняются.
    3. "Many commands - one bot". Список команд отдается одному боту. Используется при выполнении расписаний. Является подвидом "Many commands - many bots", когда запускается только один поток.
    4. "Many commands - many bots". Список команд отдается нескольким ботам (запускаются в разных потоках). Используется при выполнении списка команд из файла (batch mode).
    
    Замечания:
    1. Каждый бот всегда запускается в отдельном потоке (SocialBotThread).
    2. Число запускаемых потоков не превышает число команд в списке.
    3. После запуска потоков происходит выход из метода запуска.
    4. Ожидание завершения выполнения списка команд происходит также в отдельном потоке (SocialBotLauncherWaitingThread).
    5. Подождать окончания выполнения всех списков команд можно с помощью метода Join.
    '''
    
    def __init__(self, botClass):
        '''Инициализация'''
        self.botClass = botClass
        self.metaQueue = Queue.Queue()
    
    def Launch(self, commandsList, threadsCount, textStart=None, textFinish=None):
        '''Запускаем команды в несколько потоков (возможно, в дополнение к уже существующим) и выходим'''
        commandsList = [item.strip() for item in commandsList if item.strip() != '']
        threadsCount = min(threadsCount, len(commandsList))
        threadsCount = max(threadsCount, 0)
        if threadsCount == 0:
            return
        
        self.metaQueue.put('')
        self.metaQueue.get()
        if textStart:
            common.ThreadSafePrint(textStart)
        commandsQueue = Queue.Queue()
        for command in commandsList:
            commandsQueue.put(command)
        for _ in range(threadsCount):
            SocialBotThread(self, self.botClass, commandsQueue).start()
        SocialBotLauncherWaitingThread(self.metaQueue, commandsQueue, textFinish).start()
    
    def Join(self):
        '''Ожидаем окончания выполнения всех списков команд'''
        self.metaQueue.join()


class SocialBotLauncherSchedule(object):
    '''Запускаем ботов по расписанию. Достаточно запустить бота один раз, ставить на крон не надо.'''
    
    def __init__(self, botClass):
        '''Инициализация'''
        self.botClass = botClass
    
    def Execute(self):
        '''Выполняем расписания'''
        launcher = SocialBotLauncher(self.botClass)
        scheduler = botschedule.SocialBotScheduleIterator()
        while True:  # в любом случае необходимо дать завершиться потокам-демонам, cм. комментарий в common
            fileName = scheduler.Next()
            if fileName:
                commandsList = open(fileName).read().splitlines()
                textStart = '=== Schedule "%s" started' % os.path.basename(fileName)
                textFinish = '=== Schedule "%s" finished' % os.path.basename(fileName)
                launcher.Launch(commandsList, 1, textStart, textFinish)
            else:
                common.ThreadSafePrint('=== Waiting for a schedule ...')
                time.sleep(60)


if (__name__ == '__main__') and common.DevelopmentMode():
    pass
