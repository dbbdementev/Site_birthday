# coding=utf-8
from celery.task import periodic_task
from datetime import timedelta, datetime
from celery import Celery


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Celery('tasks', backend='amqp', broker='amqp://')


@periodic_task(run_every=timedelta(seconds=5))
def test():
    from register_activate.models import Letters
    list = Letters.objects.filter(status=1)
    for list1 in list:
        data_current = datetime.today()
        data_letter = list1.date_send
        print(data_current, data_letter)
        if data_current > data_letter:
            print('Отправлено')
            fromaddr = 'dbbdementev@gmail.com'
            username = "dbbdementev@gmail.com"
            password = "19dbb68121"
            email = list1.email_create
            text = list1.text_letters
            subject = "Поздравляем!!!"
            msg = MIMEMultipart('alternative')
            msg['From'] = fromaddr
            msg['To'] = email
            msg['Subject'] = subject
            mail_coding = 'windows-1251'
            part1 = MIMEText(text.encode('cp1251'), 'plain', mail_coding)
            msg.set_charset(mail_coding)
            msg.attach(part1)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, [email], msg.as_string())
            server.quit()
            id = list1.id
            Letters(id,
                    user_letters=list1.user_letters,
                    text_letters=list1.text_letters,
                    date_create=list1.date_create,
                    email_create=list1.email_create,
                    date_send=list1.date_send,
                    email_send=list1.email_send,
                    status=2).save()
        else:
            print('еще не пришло время ')
