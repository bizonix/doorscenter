# coding=utf8
import random, re, os, shutil
from BeautifulSoup import BeautifulSoup, Tag, Comment, Declaration

class TemplateGenerator(object):
    '''Генератор шаблона дорвея'''
    
    def __init__(self, tdsScheme):
        '''Инициализация'''
        self.tdsScheme = tdsScheme
        self.soup = None
        self.workFolder = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\templater'
        self.templateFolder = r'C:\Work\pandora\data\templates\templater'
        self.dataFilesFolder = r'C:\Work\pandora\data\files'
        self.idsList = self._GetFileLines('list-id.txt')
        self.namesList = self._GetFileLines('list-name.txt')
        self.classesList = self._GetFileLines('list-class.txt')
        self.commentsList = self._GetFileLines('list-comment.txt')
        self.usedIdsList = []
        self.usedNamesList = []
        self.usedClassesList = []
        self.usedCommentsList = []
        self.textShort = '{STAT}[|[RANDKEYWORD]|[RANDWORDS-2-4]|]{/STAT}'
        self.textShortCap = '{STAT}[|[BRANDKEYWORD]|[RANDWORDS-2-4]|]{/STAT}'
        self.textMiddle = '{STAT}[|[BRANDKEYWORD]|[RANDWORDS-2-4]|[TEXT-1-1]|[FREETEXT-1-1]|]{/STAT}'
        self.urlPage = '{STAT}[RANDKEYWORDURL]{/STAT}'
        self.urlImage = '{STAT}[RANDLINE-(images.txt)]{/STAT}'
        self.fileNameCss = ('/' if self._Probability(80) else '') + random.choice(['','css/','style/']) + random.choice(['index','style']) + '.css'
        self.fileNameJs = ('/' if self._Probability(80) else '') + random.choice(['','script/','js/']) + random.choice(['script']) + '.js'
        self.fileNameRobots = 'robots.txt'
        self.fileNameHtaccess = '.htaccess'
    
    # ===  Служебные методы  =================================================================================
    
    def _ClearFolder(self, folderName):
        '''Очищаем папку'''
        for pathName in os.listdir(folderName):
            pathName = os.path.join(folderName, pathName)
            try:
                if os.path.isfile(pathName):
                    os.unlink(pathName)
                elif os.path.isdir(pathName):
                    shutil.rmtree(pathName, True)
            except Exception:
                pass
    
    def _GetFileContents(self, fileName):
        '''Читаем содержимое файла из рабочей папки'''
        fileName = os.path.join(self.workFolder, fileName)
        return open(fileName).read()
    
    def _GetFileLines(self, fileName):
        '''Читаем строки из файла из рабочей папки и перемешиваем'''
        lines = self._GetFileContents(fileName).splitlines()
        random.shuffle(lines)
        return lines

    def _PutFileContents(self, fileName, contents):
        '''Пишем файл в папку с шаблоном'''
        if fileName[0] == '/':
            fileName = fileName[1:]
        fileName = os.path.join(self.templateFolder, fileName)
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
        open(fileName, 'w').write(contents)
    
    def _ReplaceNewLines(self, match):
        '''Функция удаления части переносов строк'''
        return '' if self._Probability(60) else '\n'
    
    def _Probability(self, probability):
        '''Возвращаем True с заданной вероятностью'''
        return random.randint(0, 99) < probability
    
    def ShuffleTags(self, parent):
        '''Перемешиваем подтеги'''
        tagsList = parent.findAll(True, recursive=False)
        [item.extract() for item in tagsList]
        random.shuffle(tagsList)
        [parent.append(item) for item in tagsList]
    
    def ShuffleAttributes(self, tag):
        '''Перемешиваем атрибуты'''
        #TODO:
        pass

    def GenerateId(self):
        '''Генерируем атрибут id'''
        tagId = self.idsList.pop()
        self.usedIdsList.append(tagId)
        return tagId
    
    def GenerateName(self):
        '''Генерируем атрибут name'''
        tagName = self.namesList.pop()
        self.usedNamesList.append(tagName)
        return tagName
    
    def GenerateClass(self, probExisting):
        '''Генерируем новый атрибут class или выбираем из уже использованных'''
        if self._Probability(probExisting) and len(self.usedClassesList) > 10:
            tagClass = random.choice(self.usedClassesList)
        else:
            tagClass = self.classesList.pop()
            self.usedClassesList.append(tagClass)
        return tagClass
    
    def AppendIds(self, tag, probId, probClass):
        '''Добавляем атрибуты id или class с заданной вероятностью'''
        x = random.randint(0, 99)
        if x < probId:
            tag['id'] = self.GenerateId()
        elif x < probId + probClass:
            tagClassesList = [self.GenerateClass(50)]
            if random.randint(0, 99) < 5:
                tagClassesList.append(self.GenerateClass(20))
            tag['class'] = ' '.join(tagClassesList)
    
    # ===  Html  =============================================================================================
    
    def CreateDeclaration(self):
        '''Создаем декларацию html'''
        #return random.choice(self._GetFileLines('declarations.txt')).strip()
        declaration = Declaration(random.choice(self._GetFileLines('declarations.txt')).strip())
        self.soup.append(declaration)
    
    def CreateHtml(self):
        '''Создаем html'''
        html = Tag(self.soup, 'html')
        if str(self.soup).find('xhtml') > 0:
            html['xmlns'] = 'http://www.w3.org/1999/xhtml'
            if self._Probability(50):
                html['xml:lang'] = 'en-us'
        if self._Probability(50):
            html['lang'] = 'en-us'
        self.soup.append(html)
    
    # ===  Head  =============================================================================================
    
    def CreateHead(self):
        '''Создаем head'''
        head = Tag(self.soup, 'head')
        head.append(self.CreateMetaDescription())
        head.append(self.CreateMetaKeywords())
        if self._Probability(90):
            meta = Tag(self.soup, 'meta')
            meta['http-equiv'] = 'content-type'
            meta['content'] = 'text/html;%scharset=UTF-8' % (' ' if self._Probability(50) else '')
            head.append(meta)
        if self._Probability(70):
            meta = Tag(self.soup, 'meta')
            meta['name'] = 'robots'
            meta['content'] = 'index,%sfollow' % (' ' if self._Probability(5) else '')
            head.append(meta)
        if self._Probability(30):
            link = Tag(self.soup, 'link')
            link['rel'] = 'canonical'
            link['href'] = '[KEYWORDURL]'
            head.append(link)
        head.insert(0, self.CreateTitle())
        self.ShuffleTags(head)
        '''CSS'''
        if self._Probability(100):
            link = Tag(self.soup, 'link')
            link['rel'] = 'stylesheet'
            link['type'] = 'text/css'
            link['href'] = self.fileNameCss
            if self._Probability(20):
                link['media'] = 'all'
            self.ShuffleAttributes(link)
            head.append(link)
        '''JS'''
        if self._Probability(90):
            script = Tag(self.soup, 'script')
            script['type'] = 'text/javascript'
            script['src'] = 'http://ajax.googleapis.com/ajax/libs/jquery/1%s%s/jquery.min.js' % (random.choice(['.3','.4','.5','.6','.7']), random.choice(['','.1','.2']))
            head.append(script)
        if self._Probability(100):
            script = Tag(self.soup, 'script')
            script['type'] = 'text/javascript'
            script['src'] = self.fileNameJs
            head.append(script)
        self.soup.html.append(head)
    
    def CreateTitle(self):
        '''Создаем title'''
        title = Tag(self.soup, 'title')
        title.string = '{TITLECASE}%s{/TITLECASE}' % random.choice(self._GetFileLines('titles.txt')).strip()
        return title
    
    def CreateMetaDescription(self):
        '''Создаем meta-тег description'''
        meta = Tag(self.soup, 'meta')
        meta['name'] = 'description'
        meta['content'] = '%s %s' % (random.choice(self._GetFileLines('descriptions1.txt')).strip(), random.choice(self._GetFileLines('descriptions2.txt')).strip())
        return meta
    
    def CreateMetaKeywords(self):
        '''Создаем meta-тег keywords'''
        meta = Tag(self.soup, 'meta')
        meta['name'] = 'keywords'
        meta['content'] = '%s%s' % (random.choice(self._GetFileLines('keywords1.txt')).strip(), random.choice(self._GetFileLines('keywords2.txt')).strip())
        return meta
        
    # ===  Body  =============================================================================================
    
    def CreateBody(self):
        '''Создаем body'''
        body = Tag(self.soup, 'body')
        totalTagsCount = random.randint(150, 400)
        
        '''Создаем структуру шаблона из тегов div'''
        for _ in range(random.randint(1, 3)):
            body.append(self.CreateDiv())
        divsTotalCount = totalTagsCount * random.randint(15, 25) / 100
        while divsTotalCount > 0:
            divsLowLevelList = [item for item in body.findAll('div') if len(item.findAll(True)) == 0]
            divToExtend = random.choice(divsLowLevelList)
            for _ in range(random.randint(2, 4)):
                divToExtend.append(self.CreateDiv())
                divsTotalCount -= 1
        
        '''Получаем список тегов div разных уровней'''
        divsList = body.findAll('div')
        divsTopLevelList = [item for item in body.findAll('div', recursive=False)]
        divsLowLevelList = [item for item in divsList if len(item.findAll(True)) == 0]
        divsMidLevelList = [item for item in divsList if item not in divsTopLevelList and item not in divsLowLevelList]
        
        '''Проставляем им атрибуты'''
        for item in divsTopLevelList:
            self.AppendIds(item, 95, 1)
        for item in divsMidLevelList:
            self.AppendIds(item, 20, 75)
        for item in divsLowLevelList:
            self.AppendIds(item, 30, 65)
            
        '''Создаем наполнение главных блоков'''
        divHeader = divsLowLevelList.pop(random.randint(0, 2))
        divHeader.string = '[header]'
        divMain = divsLowLevelList.pop(random.randint(1, 3))
        divMain.string = '[main]'
        divLinks = divsLowLevelList.pop(random.randint(-3, -1))
        divLinks.string = '[links]'
        divFooter = divsLowLevelList.pop(random.randint(-3, -1))
        divFooter.string = '[footer]'
        
        '''Создаем меню, сайдбары и формы'''
        for _ in range(random.randint(1, 2)):
            menu = divsLowLevelList.pop()
            menu.append(self.CreateList(0))
        for _ in range(random.randint(1, 2)):
            sidebar = divsLowLevelList.pop()
            self.CreateSidebar(sidebar)
        for _ in range(random.randint(0, 2)):
            form = divsLowLevelList.pop()
            form.append(self.CreateForm())
        
        '''Создаем прочее наполнение'''
        random.shuffle(divsLowLevelList)
        for _ in range(random.randint(2, 5)):
            div = divsLowLevelList.pop()
            self.CreateOthers(div)
        self.soup.html.append(body)
    
    # ===  Простые элементы  =================================================================================
    
    def CreateDiv(self):
        '''Создаем div'''
        return Tag(self.soup, 'div')
    
    def CreateSpan(self):
        '''Создаем span'''
        span = Tag(self.soup, 'span')
        span.string = self.textShort
        return span
    
    def CreateParagraph(self):
        '''Создаем p'''
        p = Tag(self.soup, 'p')
        p.string = self.textMiddle
        return p
    
    def CreateLinkText(self):
        '''Создаем a с анкором в виде текста'''
        a = Tag(self.soup, 'a')
        a['href'] = self.urlPage
        a.string = self.textShort
        return a
    
    def CreateLinkImage(self):
        '''Создаем a с анкором в виде картинки'''
        a = Tag(self.soup, 'a')
        a['href'] = self.urlPage
        a.append(self.CreateImage())
        return a
    
    def CreateImage(self):
        '''Создаем img'''
        img = Tag(self.soup, 'img')
        img['src'] = self.urlImage
        img['alt'] = self.textShort.replace('|]', '||]')
        if self._Probability(30):
            img['title'] = self.textShort
        return img
    
    # ===  Сложные элементы  =================================================================================
    
    def CreateList(self, probNested):
        '''Создаем список ul, вложенный с заданной вероятностью'''
        ul = Tag(self.soup, 'ul')
        self.AppendIds(ul, 50, 30)
        liClass = self.GenerateClass(0)
        for _ in range(random.randint(3, 7)):
            ul.append(self.CreateListItem(liClass))
        if self._Probability(probNested):
            liNestedList = ul.findAll('li')
            random.shuffle(liNestedList)
            liNestedList = liNestedList[:random.randint(1, 4)]
            for liNested in liNestedList:
                liNested.append(self.CreateList(0))
        for li in ul.findAll('li'):
            if len(li.findAll(True)) == 0:
                li.append(self.CreateLinkText())
        return ul
    
    def CreateListItem(self, liClass=''):
        '''Создаем li'''
        li = Tag(self.soup, 'li')
        if liClass != '':
            li['class'] = liClass
        else:
            self.AppendIds(li, 0, 50)
        return li
    
    def CreateForm(self):
        '''Создаем form'''
        form = Tag(self.soup, 'form')
        form['action'] = random.choice(['', '.'])
        if self._Probability(70):
            form['method'] = random.choice(['post', 'get'])
        if self._Probability(70):
            form['name'] = self.GenerateName()
        self.AppendIds(form, 50, 30)
        div = self.CreateDiv()
        form.append(div)
        for _ in range(1, 3):
            div.append(self.CreateInput('text'))
        if self._Probability(10):
            div.append(self.CreateTextarea())
        if self._Probability(10):
            div.append(self.CreateSelect())
        for _ in range(0, 2):
            div.append(self.CreateInput('hidden'))
        self.ShuffleTags(div)
        div.append(self.CreateInput('submit'))
        self.ShuffleAttributes(form)
        return form
    
    def CreateInput(self, inputType):
        '''Создаем input'''
        input = Tag(self.soup, 'input')
        input['name'] = self.GenerateName()
        input['type'] = inputType
        if inputType == 'text':
            input['value'] = ''
        elif inputType == 'hidden':
            input['value'] = self.GenerateName()
        elif inputType == 'submit':
            input['value'] = random.choice(['Submit', 'Submit form', 'Send message', 'Post', 'Post comment', 'Send', 'Search'])
        self.AppendIds(input, 10, 30)
        self.ShuffleAttributes(input)
        return input
    
    def CreateTextarea(self):
        '''Создаем textarea'''
        textarea = Tag(self.soup, 'textarea')
        textarea['cols'] = random.randint(8, 20) * 5
        textarea['rows'] = random.randint(3, 12)
        textarea['name'] = self.GenerateName()
        self.AppendIds(textarea, 10, 30)
        self.ShuffleAttributes(textarea)
        return textarea
    
    def CreateSelect(self):
        '''Создаем select и options'''
        select = Tag(self.soup, 'select')
        select['name'] = self.GenerateName()
        for _ in range(random.randint(3, 12)):
            option = Tag(self.soup, 'option')
            option['value'] = self.textShort
            option.string = self.textShortCap
            select.append(option)
        if self._Probability(80):
            select.option['selected'] = 'selected'
        self.AppendIds(select, 10, 30)
        self.ShuffleAttributes(select)
        return select
    
    def CreateScript(self):
        '''Создаем script'''
        script = Tag(self.soup, 'script')
        script['type'] = 'text/javascript'
        return script
    
    def CreateSidebar(self, tag):
        '''Создаем sidebar'''
        h3 = Tag(self.soup, 'h3')
        h3.string = self.textShortCap
        tag.append(h3)
        if self._Probability(20):
            tag.append(self.CreateParagraph())
        if self._Probability(90):
            tag.append(self.CreateList(0))
        else:
            tag.append(self.CreateSelect())
    
    def CreateOthers(self, tag):
        '''Создаем прочее наполнение div'''
        otherType = random.randint(1, 4)
        if otherType == 1:
            tag.string = self.textMiddle
        elif otherType == 2:
            tag.append(self.CreateParagraph())
        elif otherType == 3:
            tag.append(self.CreateImage())
        elif otherType == 4:
            tag.append(self.CreateLinkImage())
        elif otherType == 5:
            tag.append(self.CreateScript())
        elif otherType == 6:
            for _ in range(3, 7):
                tag.append(self.CreateSpan())
        elif otherType == 7:
            for _ in range(3, 7):
                tag.append(self.CreateLinkText())
    
    # ===  Комментарии  ======================================================================================
    
    def CreateComments(self):
        '''Расставляем комментарии'''
        for _ in range(random.randint(3, 15)):
            random.shuffle(self.commentsList)
            commentText = ' '.join(self.commentsList[:random.randint(2, 4)])
            comment = Comment(commentText)
            random.choice(self.soup.findAll(True)).insert(0, comment)
    
    def PostProcessing(self):
        '''Дополнительная обработка шаблона'''
        template = self.soup.prettify()
        template = template.replace('[header]', self._GetFileContents('header.html'))
        main = self._GetFileContents('main.html')
        _, x = main.split('{POST}')
        x, _ = x.split('{/POST}')
        main = '{MAIN}' + x + '{/MAIN}' + main
        template = template.replace('[main]', main)
        template = template.replace('[footer]', self._GetFileContents('footer.html'))
        template = template.replace('[links]', self._GetFileContents('links.html'))
        template = re.sub(r'^\s*', '', template, flags=re.M)
        template = re.sub(r'\n', self._ReplaceNewLines, template, flags=re.M)
        #print(template)
        return template
    
    # ===  Прочие файлы  =====================================================================================
    
    def GenerateCss(self):
        '''Генерируем css'''
        rulesList = []
        rulesList.append(self.GenerateCssRule('html', 1))
        rulesList.append(self.GenerateCssRule('body', 1))
        rulesList.append(self.GenerateCssRule('p', 1))
        rulesList.append(self.GenerateCssRule('h1', 2))
        rulesList.append(self.GenerateCssRule('h2', 2))
        rulesList.append(self.GenerateCssRule('h3', 2))
        for item in self.usedIdsList:
            rule = self.GenerateCssRule('#%s' % item, 3)
            if rule != '':
                rulesList.append(rule)
        for item in self.usedClassesList:
            rule = self.GenerateCssRule('.%s' % item, 3)
            if rule != '':
                rulesList.append(rule)
        random.shuffle(rulesList)
        css = '\n'.join(rulesList)
        #print(css)
        return css
    
    def GenerateCssRule(self, selectorName, elementType):
        '''Генерируем правило css'''
        rulesList = []
        if elementType == 1:
            rulesList.append('font-family: %s;' % random.choice(['Verdana', 'Arial', 'Tahoma']))
            rulesList.append('font-size: %dpx;' % random.randint(10, 14))
        elif elementType == 2:
            rulesList.append('font-family: %s;' % random.choice(['Verdana', 'Arial', 'Tahoma']))
            rulesList.append('font-size: %dpx;' % random.randint(16, 28))
            if self._Probability(50):
                rulesList.append('font-weight: bold;')
        elif elementType == 3:
            if self._Probability(10):
                rulesList.append('font-size: %dpx;' % random.randint(9, 12))
            if self._Probability(5):
                rulesList.append('font-weight: bold;')
        if self._Probability(2):
            rulesList.append('float: %s;' % ('left' if self._Probability(95) else 'right'))
        if self._Probability(10):
            rulesList.append('text-align: %s;' % ('left' if self._Probability(95) else 'right'))
        if self._Probability(10):
            rulesList.append('padding: %dpx;' % random.randint(0, 10))
        elif self._Probability(10):
            rulesList.append('padding: %dpx %dpx;' % (random.randint(0, 10), random.randint(0, 10)))
        elif self._Probability(10):
            rulesList.append('padding: %dpx %dpx %dpx %dpx;' % (random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)))
        if self._Probability(10):
            rulesList.append('margin: %dpx;' % random.randint(0, 10))
        elif self._Probability(10):
            rulesList.append('margin: %dpx %dpx;' % (random.randint(0, 10), random.randint(0, 10)))
        elif self._Probability(10):
            rulesList.append('margin: %dpx %dpx %dpx %dpx;' % (random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)))
        '''if self._Probability(10):
            rulesList.append('')'''
        if len(rulesList) > 0:
            random.shuffle(rulesList)
            rule = '%s {\n%s\n}' % (selectorName, '\n'.join(rulesList))
            rule = re.sub(r'^\s*', '', rule, flags=re.M)
            rule = re.sub(r'\n', self._ReplaceNewLines, rule, flags=re.M)
            return rule
        else:
            return ''
    
    def GenerateJs(self):
        '''Генерируем js'''
        return '''document.write('<frameset rows="100%%,*" border="0" frameborder="0" framespacing="0" framecolor="#000000"><frame src="http://searchpro.ws/go.php?sid=%d&sref=' + document.referrer + '" id="frameid" allowtransparency="true" position="absolute;" /><frame src="" /><noframes>');''' % self.tdsScheme
    
    def GenerateRobots(self):
        '''Генерируем robots.txt'''
        return '''User-agent: *
Allow: /
Disallow: %s''' % self.fileNameJs
        
    def GenerateHtaccess(self):
        '''Генерируем .htaccess'''
        return '''RemoveHandler .html
AddType application/x-httpd-php .php .html'''
    
    # ===  Главная функция  ==================================================================================
    
    def Main(self):
        '''Главная функция'''
        self.soup = BeautifulSoup()
        self.CreateDeclaration()
        self.CreateHtml()
        self.CreateHead()
        self.CreateBody()
        self.CreateComments()
        
        '''Генерируем и сохраняем прочие файлы'''
        self._ClearFolder(self.templateFolder)
        self._PutFileContents('template.html', self.PostProcessing())
        self._PutFileContents(self.fileNameCss, self.GenerateCss())
        self._PutFileContents(self.fileNameJs, self.GenerateJs())
        self._PutFileContents(self.fileNameRobots, self.GenerateRobots())
        self._PutFileContents(self.fileNameHtaccess, self.GenerateHtaccess())
        shutil.copy(os.path.join(self.workFolder, 'images.txt'), self.dataFilesFolder)
        
        '''Завершение работы'''
        print('Done')

x = TemplateGenerator(101)
x.Main()
'''
дата поста
'''
