# coding=utf8
import os, glob, random, datetime, ConfigParser
import pinterest, common
from pinterest import PinterestBoard, PlannedCommonBoard, PlannedProfitBoard  # workaround for unserialization

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

SCHEDULE_NEW_FOLDER = 'schedule'
SCHEDULE_DONE_FOLDER = 'schedule/done'

if not os.path.exists(SCHEDULE_NEW_FOLDER):
    os.makedirs(SCHEDULE_NEW_FOLDER)
if not os.path.exists(SCHEDULE_DONE_FOLDER):
    os.makedirs(SCHEDULE_DONE_FOLDER)

class Schedule(object):
    '''Расписание'''

    def __init__(self):
        '''Инициализация'''
        self.timeStampFormat = '%Y-%m-%d %H-%M'
        self.timeStampLength = 16
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.hoursCorrection = int(config.get('Schedule', 'HoursCorrection'))
        self.commonFollowUsersPopular = int(config.get('Schedule', 'CommonFollowUsersPopular'))
        self.commonFollowUsersByCategory = int(config.get('Schedule', 'CommonFollowUsersByCategory'))
        self.commonFollowUsersByKeywords = int(config.get('Schedule', 'CommonFollowUsersByKeywords'))
        self.commonFollowBoardsPopular = int(config.get('Schedule', 'CommonFollowBoardsPopular'))
        self.commonFollowBoardsByCategory = int(config.get('Schedule', 'CommonFollowBoardsByCategory'))
        self.commonFollowBoardsByKeywords = int(config.get('Schedule', 'CommonFollowBoardsByKeywords'))
        self.commonLikePinsPopular = int(config.get('Schedule', 'CommonLikePinsPopular'))
        self.commonLikePinsByCategory = int(config.get('Schedule', 'CommonLikePinsByCategory'))
        self.commonLikePinsByKeywords = int(config.get('Schedule', 'CommonLikePinsByKeywords'))
        self.commonRepostPinsPopular = int(config.get('Schedule', 'CommonRepostPinsPopular'))
        self.commonRepostPinsByCategory = int(config.get('Schedule', 'CommonRepostPinsByCategory'))
        self.commonRepostPinsByKeywords = int(config.get('Schedule', 'CommonRepostPinsByKeywords'))
        self.commonCommentPinsPopular = int(config.get('Schedule', 'CommonCommentPinsPopular'))
        self.commonCommentPinsByCategory = int(config.get('Schedule', 'CommonCommentPinsByCategory'))
        self.commonCommentPinsByKeywords = int(config.get('Schedule', 'CommonCommentPinsByKeywords'))
        self.commonUnfollowUsers = int(config.get('Schedule', 'CommonUnfollowUsers'))
        self.profitFollowUsersByKeywords = int(config.get('Schedule', 'ProfitFollowUsersByKeywords'))
        self.profitFollowBoardsByKeywords = int(config.get('Schedule', 'ProfitFollowBoardsByKeywords'))
        self.profitLikePinsByKeywords = int(config.get('Schedule', 'ProfitLikePinsByKeywords'))
        self.profitRepostPinsByKeywords = int(config.get('Schedule', 'ProfitRepostPinsByKeywords'))
        self.profitCommentPinsByKeywords = int(config.get('Schedule', 'ProfitCommentPinsByKeywords'))
        self.profitPostFromAmazon = int(config.get('Schedule', 'ProfitPostFromAmazon'))
    
    def _GetScheduleFilesList(self):
        '''Возвращаем список файлов с расписаниями'''
        return sorted(glob.glob(os.path.join(SCHEDULE_NEW_FOLDER, '201*.txt')))
    
    def _FileNameToDateTime(self, fileName):
        '''Имя файла -> дата и время его выполнения'''
        timeStamp = os.path.basename(fileName)[:self.timeStampLength]
        return datetime.datetime.strptime(timeStamp, self.timeStampFormat)
    
    def _DateTimeCorrect(self, dateTime):
        '''Корректировка часового пояса'''
        return dateTime + datetime.timedelta(0, self.hoursCorrection * 60 * 60)


class ScheduleGenerator(Schedule):
    '''Создание расписания работы ботов'''
    
    def _GetUserLoginsList(self):
        '''Получаем список логинов юзеров для генерации расписания'''
        user = pinterest.PinterestUser()
        return user.usersDict.keys()
    
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
                timeStamp = (datetime.datetime.today() + datetime.timedelta(dayOffset)).strftime('%Y-%m-%d') + ' %02d-%02d' % (random.randint(7, 22), random.randint(0, 59))
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
        for line in open('boards.txt'):
            if line.strip() != '':
                category, _, boards = line.strip().partition(':')
                commonBoardsDict[category] = boards.split(',')
        commonBoardsList = []
        for category in random.sample(commonBoardsDict.keys(), random.randint(10, 20)):
            boardName = random.choice(commonBoardsDict[category])
            board = pinterest.PlannedCommonBoard(boardName, category, ['', ''])  # два пустых кея для примера
            commonBoardsList.append(board)
        return commonBoardsList
    
    def _Save(self, userLogin, timeStamp, commandsList):
        '''Сохраняем расписание'''
        fileName = os.path.join(SCHEDULE_NEW_FOLDER, '%s %s.txt' % (timeStamp, userLogin))
        open(fileName, 'w').write('\n'.join(commandsList))
        #print(timeStamp + '\n' + '\n'.join(commandsList))
    
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
                                    #(self.commonFollowUsersPopular, '--user=%s --action=follow-users --count=%d --category=popular' % (userLogin, random.randint(1, 5))),  # TODO: реализовать
                                    #(self.commonFollowBoardsPopular, '--user=%s --action=follow-boards --count=%d --category=popular' % (userLogin, random.randint(1, 2))),  # TODO: реализовать
                                    (self.commonLikePinsPopular, '--user=%s --action=like-pins --count=%d --category=popular' % (userLogin, random.randint(1, 5))),
                                    #(self.commonRepostPinsPopular, '--user=%s --action=repost-pins --count=%d --category=popular --boards="%s:%s"' % (userLogin, random.randint(1, 5), board.name, board.category)),  # TODO: выбор доски
                                    (self.commonCommentPinsPopular, '--user=%s --action=comment-pins --count=%d --category=popular' % (userLogin, random.randint(1, 2))),
                                    
                                    (self.commonFollowUsersByCategory, '--user=%s --action=follow-users --count=%d --category=%s' % (userLogin, random.randint(1, 5), board.category)),
                                    (self.commonFollowBoardsByCategory, '--user=%s --action=follow-boards --count=%d --category=%s' % (userLogin, random.randint(1, 2), board.category)),
                                    (self.commonLikePinsByCategory, '--user=%s --action=like-pins --count=%d --category=%s' % (userLogin, random.randint(1, 5), random.choice(pinterest.boardCategoriesList))),
                                    (self.commonRepostPinsByCategory, '--user=%s --action=repost-pins --count=%d --category=%s --boards="%s:%s"' % (userLogin, random.randint(1, 5), board.category, board.name, board.category)),
                                    (self.commonCommentPinsByCategory, '--user=%s --action=comment-pins --count=%d --category=%s' % (userLogin, random.randint(1, 2), random.choice(pinterest.boardCategoriesList))),
                                    
                                    (self.commonUnfollowUsers, '--user=%s --action=unfollow-users --count=%d' % (userLogin, random.randint(1, 2))),
                        ]
                        if keywords != '':
                            itemsList.extend([
                                    (self.commonFollowUsersByKeywords, '--user=%s --action=follow-users --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    (self.commonFollowBoardsByKeywords, '--user=%s --action=follow-boards --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                                    (self.commonLikePinsByKeywords, '--user=%s --action=like-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    (self.commonRepostPinsByKeywords, '--user=%s --action=repost-pins --count=%d --keywords="%s" --boards="%s:%s"' % (userLogin, random.randint(1, 2), keywords, board.name, board.category)),
                                    (self.commonCommentPinsByKeywords, '--user=%s --action=comment-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                            ])
                        '''Доски для продвижения товаров'''
                        if len(user.plannedProfitBoardsList) > 0:
                            board = random.choice(user.plannedProfitBoardsList)
                            keywords = board.GetKeywords()
                            itemsList.extend([
                                    (self.profitFollowUsersByKeywords, '--user=%s --action=follow-users --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    (self.profitFollowBoardsByKeywords, '--user=%s --action=follow-boards --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                                    (self.profitLikePinsByKeywords, '--user=%s --action=like-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 5), keywords)),
                                    (self.profitCommentPinsByKeywords, '--user=%s --action=comment-pins --count=%d --keywords="%s"' % (userLogin, random.randint(1, 2), keywords)),
                            ])
                            if 'pinterest' in board.sourcesList:
                                itemsList.extend([
                                    (self.profitRepostPinsByKeywords, '--user=%s --action=repost-pins --count=%d --keywords="%s" --boards="%s:%s"' % (userLogin, random.randint(1, 2), keywords, board.name, board.category)),
                                ])
                            if 'amazon' in board.sourcesList:
                                itemsList.extend([
                                    (self.profitPostFromAmazon, '--user=%s --action=post-amazon --count=%d --keywords="%s" --boards="%s:%s" --department=%s' % (userLogin, random.randint(1, 3), keywords, board.name, board.category, board.department)),
                                ])
                        commandsList.append(self._SelectItem(itemsList))
                    self._Save(userLogin, timeStamp, commandsList)
        self.Clear(datetime.datetime.now())
    
    def Clear(self, dateTime):
        '''Удаляем расписания по заданную дату/время'''
        dateTime = self._DateTimeCorrect(dateTime)
        for fileName in self._GetScheduleFilesList():
            if dateTime >= self._FileNameToDateTime(fileName):
                os.unlink(fileName)
    
    def ClearAll(self):
        '''Удаляем все расписания'''
        for fileName in self._GetScheduleFilesList():
            os.unlink(fileName)


class ScheduleIterator(Schedule):
    '''Обход расписания работы ботов'''
    
    def Next(self):
        '''Находим следующее расписание, которое пора выполнить. Возвращаем список команд и имя файла с расписанием'''
        dateTimeNow = self._DateTimeCorrect(datetime.datetime.now())
        for fileName in self._GetScheduleFilesList():
            if dateTimeNow >= self._FileNameToDateTime(fileName):
                newFileName = fileName.replace(SCHEDULE_NEW_FOLDER, SCHEDULE_DONE_FOLDER)
                os.rename(fileName, newFileName)
                return newFileName
    
    def Empty(self):
        '''Есть ли еще расписания'''
        return len(self._GetScheduleFilesList()) == 0


if (__name__ == '__main__') and common.DevelopmentMode():
    schedule = ScheduleGenerator()
    #schedule.ClearAll()
    #schedule.Generate(1000, 2)
