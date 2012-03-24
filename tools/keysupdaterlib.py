# coding=utf8
'''Adult-list и black-list для парсинга кейвордов'''

adultWords = '''adult
amateur
anal
annilingus
anus
asian
ass
babe
babydoll
ball
bare
bbw
bdsm
beach
bear
bikini
bitch
bizarre
blonde
blowjob
bondage
boob
bottom
breast
brunette
bukkake
butt
cartoon
celeb
clitor
close up
clothes free
clothesfree
cock
condom
cross dress
cum shot
cumshot
cunninglus
cunt
dating
deviance
dick
dildo
discipline
disipline
dog style
doggy style
doggystyle
dogstyle
domination
ebony
ejaculation
enema
erection
erogenous
erotic
escort
ethnic
exhibitionist
face sitting
facesitting
fellatio
fem dom
femdom
fetish
fingered
fingering
fisting
flogging
frontage
fuck
galler
gay
genital
girl
gloryhole
hairy
handjob
hardcore
horny
hunk
interracial
intim
kinky
kiss
latin
lesbi
licking
lingerie
live cam
masochism
masochist
masturb
mature
milf
naked
naturalist
naturism
naturist
nude
nudism
nudist
nudity
oral
orgasm
orgy
peeing
penis
pennis
pervas
pervert
piss
porn
pregnant
prostit
punishment
pussy
redhead
sadism
sadist
sadomaso
sex
shaved
shemale
slapped
slave training
smoking
smothering
softcore
spank
strap on
strapon
strapped
stripping
suck
swing
teen
testicl
tgp
tits
topless
torture
transvest
twink
unclothed
undress
uniform
upskirt
vagin
vibrat
virgin
voyeur
vulva
wank
web cam
webcam
whipping
whore
xxx
young'''

blackWords = '''1 teen
1 year old
1 yo
1teen
1year old
1yo
10 teen
10 year
10 yo
10teen
10year old
10yo
11 year
12 year
13 teen
13 year
14 year
15 teen
15 year
16 teen
1o1ita
2 teen
2 year old
2 yo
2teen
2year old
3 year old
3 yo
3teen
3year old
4 teen
4 year old
4 yo
4teen
4year old
5 year old
5 yo
5teen
5year old
6 year
6 yo
6teen
6year old
7 teen
7 year
7 yo
7teen
7year old
8 year
8 yo
8teen
8year old
9 teen
9 year
9 yo
9teen
9year old
accomodati
adolescent
animal
antivir
banned
beast
burial
cambod
cambri
camcod
camero
child
consolidat
coprophag
dead
death
deceased
demise
desanguinat
disfigur
disney
download
driver
dying
eight year old
eight yo
electrocuted
electrocution
eleven year old
eleven yo
execution
exsanguinated
fifteen
five year old
five yo
forteen
four year old
four yo
fourteen
funeral
gmail
healthy bdsm
healthybdsm
hooker
horse
hussyfan
illegal
incest
juvenile
kachat
kid
kill
kindeer
kinder
kotoran
little boy
little girl
little teen
littleboy
littlegirl
lola
lolipop
lolit
lollit
looolit
microsoft
minor
murder
necrophil
newborn
nine year old
nine yo
nonconsensual
one year old
one yo
padophylia
paeder
paedophil
paidophilia
pdohilie
pdophile
pdophilie
peder
pediphile
pedo
perverted
pony
pre teen
pre-teen
preeteen
preteen
preten
pthc
puberty
rape
rapi
scam
schoolgirl
seven year old
seven yo
seventeen
shit
sitteen
six year old
six yo
sixteen
slaughtered
software
teen 11
teen 3
teen 5
teen 6
teen 8
teen boy
teen girl
teen1
teen2
teen3
teen4
teen5
teen6
teen7
teen8
teen9
teenboy
teengirl
ten year old
ten yo
thirteen
three year old
three yo
torture
transsex
transvest
twelve year old
twelve yo
two year old
two yo
under
update
windows
young boy
young girl
young teen
youngboy
younggirl
youngteen
youth
zoo
.com
.net
.info
.ru'''

def SimplifyWordsList(words):
    '''Сокращение списка кейвордов за счет вхождений.
    Также выводится список кейвордов, оканчивающихся на "s".'''
    wordsList = words.split('\n')
    wordsList = [item.strip().lower() for item in wordsList]
    wordsListLengthOld = len(wordsList)
    wordsListNew = []
    for item in wordsList:
        found = False
        if item.endswith('s'):
            print('s: %s' % item)
        for item2 in wordsList:
            if (item.find(item2) >= 0) and (item != item2) and (item != '') and (item2 != ''):
                found = True
                print('%s - %s' % (item, item2))
                break
        if not found:
            wordsListNew.append(item)
    wordsList = sorted(list(set(wordsListNew)))
    print('\n'.join(wordsList))
    print('---')
    print('List length: %d => %d.' % (wordsListLengthOld, len(wordsList)))

if __name__ == '__main__':
    SimplifyWordsList(adultWords)
