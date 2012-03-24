import operator

blackListKeys = '''
,a,an,the,
this,these,that,those,some,any,
what,which,who,whom,whose,how,
i,me,myself,mine,my,
we,us,ourselves,ourself,ours,our,
you,yourself,yourselves,yours,your,
he,him,himself,hisself,his,
she,her,herself,hers,her,
it,itself,its,
they,them,themself,themselves,theirs,their,
am,is,are,being,was,were,been,have,has,having,had,do,does,doing,did,done,
shall,will,must,can,may,
here,there,only,such,few,much,many,lot,more,all,none,no,even,already,yet,also,
and,or,not,
aboard,about,above,across,after,against,along,alongside,among,amongst,around,
as,aside,at,before,behind,below,beneath,beside,besides,between,beyond,but,by,
despite,down,during,except,excluding,following,for,from,given,in,including,
inside,into,like,near,next,of,off,on,onto,out,outside,over,past,per,plus,
regarding,round,sans,since,than,through,thru,till,to,toward,towards,under,
underneath,unlike,until,up,upon,versus,via,with,within,without
'''
blackListKeys = blackListKeys.replace('\n', '').split(',')

def IsBlackKey(key):
  return key in blackListKeys

def MakeSingle(key):
  if key[-3:] == 'oes':
    key = key[:-2]
  elif key[-3:] == 'ies':
    key = key[:-3] + 'y'
  elif key[-3:] == 'ses':
    key = key[:-2]
  elif key[-3:] == 'xes':
    key = key[:-2]
  elif key[-1:] == 's':
    key = key[:-1]
  return key

for keyLength in range(1,5):
  keys = {}
  for line in open('stats.csv'):
    lineKeys = [MakeSingle(item) for item in line.strip().split(' ')]
    for n in range(len(lineKeys) - keyLength + 1):
      key = ' '.join(lineKeys[n:n + keyLength])
      if key not in keys:
        keys[key] = 0
      keys[key] += 1
  items = sorted(keys.iteritems(), key=operator.itemgetter(1))
  items.reverse()
  for n in range(40):
    print('%d: %s - %d' % (n + 1, items[n][0], items[n][1]))
  print('\n---\n')
