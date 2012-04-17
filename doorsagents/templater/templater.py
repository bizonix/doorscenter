# coding=utf8
import random, re, os
from BeautifulSoup import BeautifulSoup, Tag

class TemplateGenerator(object):
    '''Генератор шаблона дорвея'''
    
    def __init__(self):
        '''Инициализация'''
        self.soup = None
        self.workFolder = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\templater'
        self.templateFolder = r'C:\Work\pandora\data\templates\templater'
        self.idsList = self._GetFileLines('list-id.txt')
        self.namesList = self._GetFileLines('list-name.txt')
        self.classesList = self._GetFileLines('list-class.txt')
        self.usedIdsList = []
        self.usedNamesList = []
        self.usedClassesList = []
        self.textShort = '{STAT}[|[RANDKEYWORD]|[RANDWORDS-2-4]|]{/STAT}'
        self.textShortCap = '{STAT}[|[BRANDKEYWORD]|[RANDWORDS-2-4]|]{/STAT}'
        self.textMiddle = '{STAT}[|[BRANDKEYWORD]|[RANDWORDS-2-4]|[TEXT-1-1]|[FREETEXT-1-1]|]{/STAT}'
        self.urlPage = '{STAT}[RANDKEYWORDURL]{/STAT}'
        self.urlImage = '{STAT}[RANDLINE-(images.txt)]{/STAT}'
    
    # ===  Служебные методы  =================================================================================
    
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
    
    def CreateDeclaration(self):
        '''Создаем декларацию html'''
        return random.choice(self._GetFileLines('declarations.txt')).strip()
    
    # ===  Html  =============================================================================================
    
    def CreateHtml(self):
        '''Создаем html'''
        html = Tag(self.soup, 'html')
        if str(self.soup).find('xhtml') > 0:
            html['xmlns'] = 'http://www.w3.org/1999/xhtml'
            if self._Probability(50):
                html['xml:lang'] = 'en-us'
        if self._Probability(50):
            html['lang'] = 'en-us'
        return html
    
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
        self.fileNameCss = ''
        if self._Probability(100):
            link = Tag(self.soup, 'link')
            link['rel'] = 'stylesheet'
            link['type'] = 'text/css'
            self.fileNameCss = ('/' if self._Probability(80) else '') + random.choice(['','css/','style/']) + random.choice(['index','style']) + '.css'
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
        self.fileNameJs = ''
        if self._Probability(100):
            script = Tag(self.soup, 'script')
            script['type'] = 'text/javascript'
            self.fileNameJs = ('/' if self._Probability(80) else '') + random.choice(['','js/']) + random.choice(['script']) + '.js'
            script['src'] = self.fileNameJs
            head.append(script)
        return head
    
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
        return body
    
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
    
    # ===  Прочие файлы  =====================================================================================
    
    def GenerateCss(self):
        '''Генерируем css'''
        return ''
    
    def GenerateJs(self):
        '''Генерируем js'''
        return ''
    
    def GenerateRobots(self):
        '''Генерируем robots.txt'''
        return ''
    
    # ===  Главная функция  ==================================================================================
    
    def Main(self):
        '''Главная функция'''
        self.soup = BeautifulSoup(self.CreateDeclaration())
        self.soup.append(self.CreateHtml())
        self.soup.html.append(self.CreateHead())
        self.soup.html.append(self.CreateBody())
        
        '''Сохраняем шаблон'''
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
        self._PutFileContents('template.html', template)
        print(template)
        
        '''Генерируем и сохраняем прочие файлы'''
        self._PutFileContents(self.fileNameCss, self.GenerateCss())
        self._PutFileContents(self.fileNameJs, self.GenerateJs())
        self._PutFileContents('robots.txt', self.GenerateRobots())
        

x = TemplateGenerator()
x.Main()
'''
генератор css, в нем все использованные классы и id, а также основные теги типа p, h1 и пр.
в формы добавить текст
комментарии
robots.txt
дата поста
'''
