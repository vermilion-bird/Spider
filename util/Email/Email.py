# !/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys
import os
import smtplib
from config import MAIL_PWD_163, MAIL_Name_163


class Email:
    def __init__(self):
       # self.mailto_list = mailto_list  # ["xxx@163.com"]  # 目标邮箱
        self.mail_host = "smtp.163.com"
        self.mail_user = MAIL_Name_163  # "xxx@163.com"
        self.mail_pass = MAIL_PWD_163  # 163邮箱smtp生成的密码
        pass

    def send_mail(self, to_list, sub, content, attach_path):
        me = "vole.store" + "<" + self.mail_user + ">"
        outer = MIMEMultipart()
        outer['Subject'] = sub
        outer['To'] = ','.join(to_list)
        outer['From'] = me
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        outer.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))
        # msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        # msg['Subject'] = sub
        # msg['From'] = me
        # msg['To'] = ",".join(to_list)
        attachments = [attach_path]
        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except Exception as e:
                print("发送邮件附件读取出错", str(e))
                #print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, composed)  # msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(str(e))
            return False


if __name__ == '__main__':
    mailto_list = ['zhucaidong@aliyun.com']
    em = Email()
    em.send_mail(mailto_list, 'submit', 'content', '../../taobao.csv')
