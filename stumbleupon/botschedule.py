# coding=utf8
import os, glob, random, datetime, ConfigParser
import botuser, common

SCHEDULE_NEW_FOLDER = 'schedule'
SCHEDULE_DONE_FOLDER = 'schedule/done'

if not os.path.exists(SCHEDULE_NEW_FOLDER):
    os.makedirs(SCHEDULE_NEW_FOLDER)
if not os.path.exists(SCHEDULE_DONE_FOLDER):
    os.makedirs(SCHEDULE_DONE_FOLDER)

class SocialBotSchedule(object):
    '''Расписание работы бота'''

    def __init__(self):
        '''Инициализация'''
        self.timeStampFormat = '%Y-%m-%d %H-%M'
        self.timeStampLength = 16
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.hoursCorrection = int(config.get('Schedule', 'HoursCorrection'))
    
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


class SocialBotScheduleGenerator(SocialBotSchedule):
    '''Создание расписания работы ботов'''
    
    def __init__(self):
        '''Инициализация'''
        super(SocialBotScheduleGenerator, self).__init__()
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.workingHourStart = int(config.get('Schedule', 'WorkingHourStart'))
        self.workingHourFinish = int(config.get('Schedule', 'WorkingHourFinish'))
        
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
    
    @classmethod
    def _DayOffsetToDateString(self, dayOffset):
        '''Прибавляем с текущей дате заданное число дней и возвращаем полученную дату в виде строки'''
        return (datetime.datetime.today() + datetime.timedelta(dayOffset)).strftime('%Y-%m-%d')
    
    def _ReadTimeStamps(self, userLogin, dayOffset):
        '''Читаем временные точки уже существующих расписаний'''
        dateString = self._DayOffsetToDateString(dayOffset)
        fileNamesList = glob.glob(os.path.join(SCHEDULE_NEW_FOLDER, '%s*%s.txt' % (dateString, userLogin)))
        if fileNamesList == None:
            return []
        return [os.path.basename(fileName)[:self.timeStampLength] for fileName in sorted(fileNamesList)]
    
    def _SaveSchedule(self, userLogin, timeStamp, commandsList):
        '''Сохраняем расписание'''
        fileName = os.path.join(SCHEDULE_NEW_FOLDER, '%s %s.txt' % (timeStamp, userLogin))
        open(fileName, 'a').write('\n'.join(commandsList) + '\n')
    
    def _GenerateTimeStamps(self, userLogin, dayOffset, count=-1, minInterval=45):
        '''Генерим заданное число точек времени с заданным минимальным интервалом в минутах'''
        if count == -1:
            count = random.randint(3, 7)
        '''Читаем существующие точки и если их достаточно, возвращем их'''
        timeStampsExistingList = self._ReadTimeStamps(userLogin, dayOffset)
        if len(timeStampsExistingList) >= count:
            return timeStampsExistingList
        '''Иначе генерим недостающие точки'''
        dateString = self._DayOffsetToDateString(dayOffset)
        while True:
            timeStampsList = timeStampsExistingList[:]
            while len(timeStampsList) < count:
                hour = random.randint(self.workingHourStart, self.workingHourFinish - 1)
                minute = random.randint(0, 59)
                timeStamp = dateString + ' %02d-%02d' % (hour, minute)
                timeStampsList.append(timeStamp)
            timeStampsList.sort()
            '''Проверяем на соблюдение заданного минимального интервала между точками'''
            valid = True
            dateTimePrevious = datetime.datetime.now() - datetime.timedelta(1)
            for timeStamp in timeStampsList:
                dateTimeCurrent = datetime.datetime.strptime(timeStamp, self.timeStampFormat)
                if (dateTimeCurrent - dateTimePrevious).seconds < minInterval * 60:
                    valid = False
                    break
                dateTimePrevious = dateTimeCurrent
            '''Если интервалы подходят, то возвращаем список'''
            if valid:
                return timeStampsList
    
    def _GenerateCommandsList(self, userLogin, timeStamp):
        '''Генерируем список команд для юзера. Абстрактный метод.'''
        raise NotImplementedError()
    
    def Generate(self, usersCount=1, daysCount=1):
        '''Генерируем расписание для заданного числа юзеров на заданное число дней'''
        userLoginsList = botuser.usersList.GetLoginsList()
        for userLogin in random.sample(userLoginsList, usersCount):
            for dayOffset in range(daysCount):
                for timeStamp in self._GenerateTimeStamps(userLogin, dayOffset):
                    commandsList = self._GenerateCommandsList(userLogin, timeStamp)
                    self._SaveSchedule(userLogin, timeStamp, commandsList)
        self.ClearByDateTime(datetime.datetime.now())  # очищаем расписание по текущее время
    
    def PlanMassAction(self, command, usersCount, dayOffset=1):
        '''Генерируем расписание для массового действия'''
        
        '''Замечания: 
        1. По умолчанию генерим действия на следующий день, чтобы в случае генерации в середине текущего дня боты не стали выполнять действия один за другим.
        2. Не очищаем расписание по текущее время, чтобы в случае генерации действия на текущий день не уменьшить количество действий.
        3. Каждый юзер выполняет действие один раз.'''
        
        userLoginsList = botuser.usersList.GetLoginsList()
        for userLogin in random.sample(userLoginsList, usersCount):
            timeStamp = self._GenerateTimeStamps(userLogin, dayOffset, 1)[0]
            self._SaveSchedule(userLogin, timeStamp, [command])
    
    def ClearByDateTime(self, dateTime):
        '''Удаляем расписания по заданную дату/время'''
        dateTime = self._DateTimeCorrect(dateTime)
        for fileName in self._GetScheduleFilesList():
            if dateTime >= self._FileNameToDateTime(fileName):
                os.unlink(fileName)
    
    def ClearAll(self):
        '''Удаляем все расписания'''
        for fileName in self._GetScheduleFilesList():
            os.unlink(fileName)


class SocialBotScheduleIterator(SocialBotSchedule):
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
    schedule = SocialBotScheduleGenerator()
    #schedule.ClearAll()
    schedule.PlanMassAction('xxx-command', 4)
