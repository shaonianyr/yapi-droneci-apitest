import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import  make_header
import time
        
def sendEmail(sendSubject, sendContent, pwd, fileList):

    # 发送邮箱服务器
    smtpserver = ''

    # 发送邮箱用户名密码
    user = ''
    password = ''

    # 发送和接收邮箱
    sender = ''
    receives = ['']

    # 发送邮件主题和内容
    subject = 'YApi-DroneCI - ' + sendSubject + '接口自动化测试报告'
    content = sendContent

    # 构建发送与接收信息
    msgRoot = MIMEMultipart()                            
    msgRoot.attach(MIMEText(content, 'html', 'utf-8'))
    msgRoot['subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = ','.join(receives)

    # 批量添加附件
    for i in range(len(fileList)):
        sendPath = pwd + fileList[i]
        sendFile = open(sendPath, 'rb').read()
        time.sleep(2)
        att = MIMEText(sendFile, 'base64', 'utf-8')
        att["Content-Type"]='application/octet-stream'
        # att['Content-Disposition'] = 'attachment;filename = "' + fileList[i] + '"'
        att['Content-Disposition'] = 'attachment;filename =  %s' % make_header([(fileList[i], 'UTF-8')]).encode('UTF-8')
        msgRoot.attach(att)
        print('Added ' + fileList[i])
        time.sleep(2)

    # SSL协议端口号要使用465
    smtp = smtplib.SMTP_SSL(smtpserver, 465)

    # HELO 向服务器标识用户身份
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user, password)

    print("Start send email...")

    smtp.sendmail(sender, receives, msgRoot.as_string())

    smtp.quit()

    print("Send End！")