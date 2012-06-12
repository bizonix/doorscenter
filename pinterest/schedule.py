# coding=utf8
import os, sys, glob, random, datetime, ConfigParser
import pinterest, common

'''

    Стратегия работы

Каждому юзеру планируется набор из 10-20 досок общего назначения (plannedCommonBoardsList), на которые он будет 
репостить пины с пинтереста. Для каждой доски указывается имя, категория и кейворды, по которым репостить. 
Случайным образом планируется набор действий:

 - фолловить юзеров по выбранным категориям
 - анфолловить случайных юзеров
 - фолловить доски по выбранным категориям
 - лайкать пины из любых категорий
 - репостить пины из выбранных категорий на доски категорий
 - репостить пины по выбранным кейвордам на доски категорий
 - комментить любые пины

Также юзеру назначается набор досок для продвижения товаров (plannedProfitBoardsList). Для каждой доски указывается имя, 
категория, кейворды для парсинга пинтереста и/или амазона, раздел амазона и откуда постить (пинтерест и/или амазон).
Случайным образом планируется набор действий:

 - фолловить юзеров по выбранным кейвордам
 - фолловить доски по выбранным кейвордам
 - лайкать пины по выбранным кейвордам
 - репостить пины по выбранным кейвордам на соответствующие доски
 - комментить пины по выбранным кейвордам
 - постить товары с Амазона по выбранным кейвордам на соответствующие доски

'''

SCHEDULE_FOLDER = 'schedule'

class Schedule(object):
    '''Расписание работы ботов'''
    
    def __init__(self):
        '''Инициализация'''
        self.timeStampFormat = '%Y-%m-%d-%H-%M'
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.hoursCorrection = int(config.get('Schedule', 'HoursCorrection'))
    
    def _Save(self, timeStamp, commandsList):
        '''Сохраняем расписание'''
        if not os.path.exists(SCHEDULE_FOLDER):
            os.makedirs(SCHEDULE_FOLDER)
        fileName = os.path.join(SCHEDULE_FOLDER, timeStamp + '.txt')
        open(fileName, 'w').write('\n'.join(commandsList))
        print(timeStamp + '\n' + '\n'.join(commandsList))
    
    def _GetUserLoginsList(self):
        '''Получаем список логинов юзеров для генерации расписания'''
        user = pinterest.PinterestUser()
        return user.usersDict.keys()
    
    @classmethod
    def _SelectItem(self, itemsList):
        '''Делаем выбор из списка с заданными вероятностями: [(propapilityA, itemA), (propapilityB, itemB), ...]'''
        total = 0
        for item in itemsList:
            total += item[0]
        selected = random.randint(0, total - 1)
        for item in itemsList:
            selected -= item[0]
            if selected <= 0:
                return item[1]
    
    def _GenerateTimeStamps(self, count, dayOffset, minInterval):
        '''Генерим заданное число точек времени с заданным минимальным интервалом в минутах'''
        while True:
            timeStampsList = []
            for _ in range(count):
                timeStamp = (datetime.datetime.today() + datetime.timedelta(dayOffset)).strftime('%Y-%m-%d') + '-%02d-%02d' % (random.randint(7, 22), random.randint(0, 59))
                timeStampsList.append(timeStamp)
            timeStampsList = sorted(timeStampsList)
            
            correct = True
            dateTimePrevious = datetime.datetime.now() - datetime.timedelta(1)
            for timeStamp in timeStampsList:
                dateTimeCurrent = datetime.datetime.strptime(timeStamp, self.timeStampFormat)
                if (dateTimeCurrent - dateTimePrevious).seconds < minInterval * 60:
                    correct = False
                    break
                dateTimePrevious = dateTimeCurrent
            if correct:
                return timeStampsList
    
    def _GenerateCommonBoardsList(self):
        '''Генерируем список названий досок общего назначения с указанием категорий'''
        commonBoardsDict = {}
        for line in open('categories.txt'):
            if line.strip() != '':
                category, _, boards = line.strip().partition(':')
                commonBoardsDict[category] = boards.split(',')
        commonBoardsList = []
        for category in random.sample(commonBoardsDict.keys(), random.randint(10, 20)):
            boardName = random.choice(commonBoardsDict[category])
            board = pinterest.PlannedCommonBoard(boardName, category, [])
            commonBoardsList.append(board)
        return commonBoardsList
    
    def Generate(self, usersCount=1, daysCount=1):
        '''Генерируем расписание для заданного числа юзеров на заданное число дней'''
        userLoginsList = self._GetUserLoginsList()
        random.shuffle(userLoginsList)
        for userLogin in userLoginsList[:usersCount]:
            user = pinterest.PinterestUser()
            user.LoadData(userLogin)
            if len(user.plannedCommonBoardsList) == 0:  # если плановых досок нет, то генерируем их
                user.plannedCommonBoardsList = self._GenerateCommonBoardsList()
                user.SaveData()
            for dayOffset in range(daysCount):
                for timeStamp in self._GenerateTimeStamps(random.randint(3, 7), dayOffset, 45):
                    commandsList = []
                    for _ in range(random.randint(3, 15)):
                        '''Доски общего назначения'''
                        board = random.choice(user.plannedCommonBoardsList)
                        keywords = board.GetKeywords()
                        itemsList = [
                                    (100, '--user=%s --action=follow-users --count=%d --category=%s' % (userLogin, random.randint(1, 5), board.category)),
                                    (  5, '--user=%s --action=unfollow-users --count=%d' % (userLogin, random.randint(1, 2))),
                                    ( 20, '--user=%s --action=follow-boards --count=%d --category=%s' % (userLogin, random.randint(1, 2), board.category)),
                                    (100, '--user=%s --action=like-pins --count=%d --category=%s' % (userLogin, random.randint(1, 5), random.choice(pinterest.boardCategoriesList))),
                                    ( 30, '--user=%s --action=repost-pins --count=%d --category=%s --boards="%s:%s"' % (userLogin, random.randint(1, 5), board.category, board.name, board.category)),
                                    ( 10, '--user=%s --action=comment-pins --count=%d --category=%s' % (userLogin, random.randint(1, 2), random.choice(pinterest.boardCategoriesList))),
                        ]
                        if keywords != '':
                            itemsList.extend([
                                    ( 50, '--user=%s --action=follow-users --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    ( 10, '--user=%s --action=follow-boards --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                                    ( 50, '--user=%s --action=like-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    ( 10, '--user=%s --action=repost-pins --count=%d --keywords="%s" --boards="%s:%s"' % (userLogin, random.randint(1, 2), keywords, board.name, board.category)),
                                    (  5, '--user=%s --action=comment-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                            ])
                        '''Доски для продвижения товаров'''
                        if len(user.plannedProfitBoardsList) > 0:
                            board = random.choice(user.plannedProfitBoardsList)
                            keywords = board.GetKeywords()
                            itemsList.extend([
                                    (200, '--user=%s --action=follow-users --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    ( 50, '--user=%s --action=follow-boards --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                                    (200, '--user=%s --action=like-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    ( 10, '--user=%s --action=comment-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                            ])
                            if 'pinterest' in board.sourcesList:
                                itemsList.extend([
                                    ( 30, '--user=%s --action=repost-pins --count=%d --keywords="%s" --boards="%s:%s"' % (userLogin, random.randint(1, 2), keywords, board.name, board.category)),
                                ])
                            if 'amazon' in board.sourcesList:
                                itemsList.extend([
                                    ( 50, '--user=%s --action=post-amazon --count=%d --keywords="%s" --boards="%s:%s" --department=%s' % (userLogin, random.randint(1, 3), keywords, board.name, board.category, board.department)),
                                ])
                        commandsList.append(self._SelectItem(itemsList))
                    self._Save(timeStamp, commandsList)
    
    def FindNext(self):
        '''Находим следующее расписание, которое пора выполнить. Возвращаем файл с расписанием'''
        dateTimeNow = datetime.datetime.now() + datetime.timedelta(0, self.hoursCorrection * 60 * 60)  # текущее время с корректировкой часового пояса
        for fileName in glob.glob(os.path.join(SCHEDULE_FOLDER, '201*.txt')):
            fileName = os.path.basename(fileName)
            dateTimePlanned = datetime.datetime.strptime(fileName.replace('.txt', ''), self.timeStampFormat)
            if dateTimeNow >= dateTimePlanned:
                return fileName


if (__name__ == '__main__') and common.DevelopmentMode():
    schedule = Schedule()
    #print(schedule._GenerateCommonBoardsList())
    schedule.Generate()
