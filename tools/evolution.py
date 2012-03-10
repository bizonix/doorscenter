# coding=utf8
import datetime

dateToday = datetime.date.today()
deltaWeek = datetime.timedelta(7)

class Doors(object):
    '''Пачка доров - доменов'''
    def __init__(self, type, dateStart, count):
        '''Инициализация'''
        self.type = type
        self.dateStart = dateStart
        self.count = count
        
        self.trafStat = []
        self.trafKoef = 1
        self.incomeKoef = 1
        if self.type == 'gay':
            self.trafStat = [53, 430, 1565, 4354, 8880, 14444, 13633, 14980, 14086, 13063, 11377, 10191, 9869, 8931, 8627, 7892, 7709, 7707]  # трафик в неделю на реальной сетке из 40 доменов
            self.trafKoef = 40  # размер реальной сетки
            self.incomeKoef = 1.5 * 7 / 7800  # реальный доход 
        elif self.type == 'dating':
            self.trafStat = [13, 139, 245, 337, 417, 525, 709, 884, 981, 1183, 1270, 1447, 917, 186, 184]
            self.trafKoef = 35
            self.incomeKoef = 4.0 * 7 / 1447
    
    def Traffic(self, date):
        '''Трафик в день на заданную дату'''
        delta = (date - self.dateStart).days / 7
        if delta <= 0:
            traf = 0
        elif delta <= len(self.trafStat):
            traf = self.trafStat[delta - 1]
        else:
            traf = max(0, self.trafStat[-1] + (self.trafStat[-1] - self.trafStat[-2]) * (delta - len(self.trafStat)))
        return float(traf) / self.trafKoef / 7 * self.count
        
    def Income(self, date):
        '''Доход в день на заданную дату'''
        return self.Traffic(date) * self.incomeKoef

class DoorsBriefcase(object):
    '''Портфель доров'''
    def __init__(self):
        self.doors = []
        
    def Add(self, type, dateStart, count):
        '''Добавляем пачку доров'''
        if count > 0:
            self.doors.append(Doors(type, dateStart, count))
        
    def Traffic(self, date, type):
        '''Трафик в день на заданную дату'''
        total = 0
        for door in self.doors:
            if door.type == type:
                total += door.Traffic(date)
        return total
        
    def Income(self, date, type):
        '''Доход в день на заданную дату'''
        total = 0
        for door in self.doors:
            if door.type == type:
                total += door.Income(date)
        return total

'''Текущий портфель доров'''
x = DoorsBriefcase()
x.Add('gay', datetime.date(2011, 5, 23), 40)
x.Add('dating', datetime.date(2011, 5, 28), 112)
x.Add('dating', datetime.date(2011, 6, 6), 35 * 9)
x.Add('gay', datetime.date(2011, 9, 5), 10)
x.Add('dating', datetime.date(2011, 9, 9), 34)

weekCostEat = 0  # на жизнь в неделю
weekCostServers = 0  # на сервера в неделю
domainsPerDay = 30  # сколько доменов покупаем в день
amountLimit = -2800  # кредитный лимит
amountTop = 3000  # сумма, достаточная для увольнения

targetPrinted1 = False
targetPrinted2 = False
targetPrinted3 = False

amount = 0  # сумма в кошельке
date = datetime.date(2011, 9, 25)
for week in range(25):
    '''Новая дата'''
    date += deltaWeek
    '''Покупаем домены'''
    weekCostDomains = 0
    x.Add('gay', date, domainsPerDay * 0.3 * 7)
    x.Add('dating', date, domainsPerDay * 0.7 * 7)
    weekCostDomains = domainsPerDay * 2.17 * 7  # на домены в неделю
    '''Получаем трафик'''
    incomeGay = x.Income(date, 'gay')
    incomeDating = x.Income(date, 'dating')
    incomeTotal = incomeGay + incomeDating
    '''Считаем деньги'''
    amount += -weekCostEat -weekCostServers -weekCostDomains + (incomeGay + incomeDating) * 7
    '''Текущее состояние дел'''
    print('%s - %.2f (%.2f / %.2f) - %d' % (date, incomeTotal, incomeGay, incomeDating, amount))
    '''Если исчерпали первоначальный бюджет на домены, перестаем их покупать'''
    if (amount < amountLimit) and not targetPrinted1:
        domainsPerDay = 0
        print('target 1')
        targetPrinted1 = True 
    '''Если текущая сумма больше нуля, снова покупаем домены'''
    if (amount > 0) and not targetPrinted2:
        domainsPerDay = 30#incomeTotal / 8
        print('target 2')
        targetPrinted2 = True
    '''Если текущая сумма больше заданной, увольняемся с работы и покупаем больше доменов'''
    if (amount > amountTop) and not targetPrinted3:
        weekCostEat = 350
        weekCostServers = 60
        domainsPerDay = 30#incomeTotal / 4
        print('target 3')
        targetPrinted3 = True
