# coding=utf8

def ModifyIniSettings(oldSettingsList, newSettingsDict):
    '''В списке настроек типа ini-файла меняет параметры по словарю'''
    newSettingsList = []
    for line in oldSettingsList:
        line = line.strip()
        if line.find('=') >= 0:
            key, _, value = line.partition('=')
            if key in newSettingsDict:
                value = newSettingsDict[key]
            line = key + '=' + value
        newSettingsList.append(line)
    return newSettingsList

def ModifyIniFile(path, settingsDict):
    '''В ini-файле меняет настройки по словарю'''
    with open(path, 'r') as fd:
        lines = fd.readlines()
    with open(path, 'w') as fd:
        fd.write('\n'.join(ModifyIniSettings(lines, settingsDict)))
