# coding=utf8
import os, sys, argparse
import pinterest

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class Launcher(object):
    '''Запускаем бота'''
    
    def __init__(self):
        '''Инициализация'''
        self.bot = pinterest.PinterestBot(True)
        self.loggedIn = False
    
    def Test(self):
        '''Тест бота'''
        pass
    
    def Execute(self, command=None):
        '''Выполняем команды'''
        if not command:
            batchMode = ' '.join(sys.argv).find('--batchfile') >= 0
        else:
            batchMode = command.find('--batchfile') >= 0
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012')
        parser.add_argument('--email', required=(not batchMode), help='user\'s email')
        parser.add_argument('--password', required=(not batchMode), help='user\'s password')
        parser.add_argument('--action', required=(not batchMode), choices=['report', 'follow-users', 'unfollow-users', 'follow-boards', 'like-pins', 'repost-pins', 'comment-pins', 'add-pins-amazon'], help='action to execute')
        parser.add_argument('--countmin', required=(not batchMode), type=int, help='minimal actions count')
        parser.add_argument('--countmax', required=(not batchMode), type=int, help='maximum actions count')
        parser.add_argument('--keywords', required=(not batchMode), help='comma-separated keywords for scraping; use "popular" for liking, reposting and commenting popular pins')
        parser.add_argument('--boards', help='comma-separated board names or keywords for repinning and posting')
        parser.add_argument('--department', default='All', help='amazon department for searching')
        parser.add_argument('--proxy', default='', help='proxy host[:port]')
        parser.add_argument('--proxypwd', default='', help='proxy username:password')
        parser.add_argument('--batchfile', default='', help='commands file name for batch mode')
        if not command:
            args = parser.parse_args()
        else:
            args = parser.parse_args(command.split(' '))
        
        if not batchMode:
            '''Одиночная команда'''
            userEmail = args.email
            userPassword = args.password
            action = args.action
            actionsCountMin = args.countmin
            actionsCountMax = args.countmax
            keywordsList = args.keywords.split(',')
            boardsList = args.boards.split(',')
            amazonDepartment = args.department
            proxyHost = args.proxy
            proxyPassword = args.proxypwd
            
            '''Логинимся'''
            if not self.loggedIn:
                self.bot.Login(userEmail, userPassword, proxyHost, proxyPassword)
                self.loggedIn = True
            
            '''Выполняем команду'''
            if action == 'report':
                self.bot.UserReport()
            elif action == 'follow-users':
                self.bot.FollowUsers(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'unfollow-users':
                self.bot.UnfollowUsers(actionsCountMin, actionsCountMax)
            elif action == 'follow-boards':
                self.bot.FollowBoards(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'like-pins':
                self.bot.LikePins(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'repost-pins':
                self.bot.RepostPins(keywordsList, actionsCountMin, actionsCountMax, boardsList)
            elif action == 'comment-pins':
                self.bot.CommentPins(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'add-pins-amazon':
                self.bot.AddPinsAmazon(keywordsList, actionsCountMin, actionsCountMax, boardsList, amazonDepartment)
        else:
            '''Читаем и выполняем команды из файла'''
            batchFileName = args.batchfile
            print('=== Executing commands from "%s" ...' % batchFileName)
            try:
                commandsList = open(batchFileName).read().splitlines()
                for command in commandsList:
                    if command.strip() != '':
                        try:
                            self.Execute(command)
                        except Exception as error:
                            print('### Error: %s' % error)
            except Exception as error:
                print('### Error: %s' % error)
            print('=== Done commands from "%s".' % batchFileName)


if __name__ == '__main__':
    argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-users --countmin=3 --countmax=5 --keywords=shoes,gucci'
    argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-boards --countmin=3 --countmax=5 --keywords=shoes,gucci'
    #launcher = Launcher(argsString)
    launcher = Launcher()
    launcher.Execute()
