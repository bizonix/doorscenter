'''python 3.1'''
import email, imaplib, zipfile, io, ftplib

done = False
'''Get mail'''
obj = imaplib.IMAP4_SSL('imap.gmail.com', 993)
obj.login('proxy@alexborisov.info'.encode(), 'kernel32'.encode())
obj.select()
typ, data = obj.search(None, 'ALL')
for num in reversed(data[0].split()):
    typ, data = obj.fetch(num, '(RFC822)')
    email_body = data[0][1]
    mail = email.message_from_string(email_body.decode())
    if mail.get_content_maintype() != 'multipart':
        continue
    '''Get the attachment'''
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        counter = 1
        if not filename:
            filename = 'part-%03d%s' % (counter, 'bin')
            counter += 1
        decoded = part.get_payload(decode=True)
        fileObj1 = io.BytesIO(decoded)
        '''Unzip the file'''
        attachment = zipfile.ZipFile(fileObj1)
        listAll = attachment.read('full_list_nopl/_full_list.txt').decode('utf-8').split('\n')
        '''Split to HTTP and Socks. HTTP ports: 27977, 3128, 80. Socks ports: 1080.'''
        listHttp = []
        listSocks = []
        for line in listAll:
            _, _, port = line.strip().partition(':')
            if port in ['80', '3128', '27977']:
                listHttp.append(line)
            elif port in ['1080']:
                listSocks.append(line)
            else:
                listHttp.append(line)
                listSocks.append(line)
        print('{0}, {1}, {2}'.format(len(listAll), len(listHttp), len(listSocks)))
        '''Upload to FTP'''
        ftp = ftplib.FTP("alexborisov.net")
        ftp.login("proxy@alexborisov.net", "kernel32")
        ftp.storbinary("STOR list-all.txt", io.BytesIO('\n'.join(listAll).encode('utf-8')))
        ftp.storbinary("STOR list-http.txt", io.BytesIO('\n'.join(listHttp).encode('utf-8')))
        ftp.storbinary("STOR list-socks.txt", io.BytesIO('\n'.join(listSocks).encode('utf-8')))
        done = True
    if done:
        break
obj.close()
obj.logout()
print(done)
