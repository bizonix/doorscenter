import email, getpass, imaplib, os, zipfile, io, ftplib

done = False
obj = imaplib.IMAP4_SSL('imap.gmail.com',993)
obj.login('proxy@alexborisov.info'.encode(),'kernel32'.encode())
obj.select()
typ, data = obj.search(None, 'ALL')
for num in reversed(data[0].split()):
    typ, data = obj.fetch(num, '(RFC822)')
    email_body = data[0][1]
    mail = email.message_from_string(email_body.decode())
    if mail.get_content_maintype() != 'multipart':
        continue
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
        attachment = zipfile.ZipFile(fileObj1)
        fileObj2 = io.BytesIO(attachment.read('emaillists/full_list_nopl/_full-list.txt')) 
        ftp = ftplib.FTP("alexborisov.net")
        ftp.login("proxy@alexborisov.net", "kernel32")
        ftp.storbinary("STOR _full-list.txt", fileObj2)
        done = True
    if done:
        break
obj.close()
obj.logout()
print(done)
