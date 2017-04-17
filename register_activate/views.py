import smtplib
import random
import string
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django_countries import countries
from register_activate.models import Congratulations
from register_activate.models import User_info, Type, Letters, Register_vk
from . import forms
import vk
from django.contrib.auth.hashers import make_password
from http.client import HTTPConnection
import json
from urllib.request import urlopen


def main(request):
    '''
    session = vk.Session()
    api = vk.API(session)
    api.messages.send(user_id=37757609, message='Кто то зашел на сайт!!!',
                      access_token='e52dd7a0e52dd7a0e59d132ab1e5746d32ee52de52dd7a0bd8b0ef06f3215fc5819ea43')
    '''
    return render(request, 'main.html')


def contacts(request):
    auth_id_id= id
    user = Register_vk.objects.filter(auth_id_id=auth_id_id)
    session = vk.Session()
    api = vk.API(session)
    fields = api.friends.get(user_id=user[0].nickname, fields='first_name,last_name,domain,bdate,online,photo_50')
    return render(request, 'register_vk.html', {'user': user, 'fields': fields})


def register_vk(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    nickname = request.GET.get('id')
    user = Register_vk.objects.filter(nickname=nickname)
    if user:
        print('нашли юзера', user[0].id, user[0].auth_id_id)
        global id
        id = user[0].auth_id_id
        Register_vk(id=user[0].id,data_visit=datetime.today()).save(update_fields=['data_visit'])
        user = authenticate(username=nickname, password=nickname)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('register_activate:mainpage')
            else:
                print('Не активен')
                return render(request, 'ErrorPage.html')
        else:
            print('Не тот пароль или юзер')
            return render(request, 'ErrorPage.html', {'errormessage': 'Invalid login'})
    else:
        user2 = User.objects.filter(username=nickname)
        User(first_name=first_name,
             last_name=last_name,
             username=nickname,
             password=make_password(nickname, make_salt())).save()
        Register_vk(first_name=first_name,
                    last_name=last_name,
                    nickname=nickname,
                    data_visit=datetime.today(),
                    auth_id_id=user2[0].id).save()
        user = authenticate(username=nickname, password=nickname)
        if user is not None:
            if user.is_active:
                login(request, user)
        print('сохранили нового')
        return render(request, 'register_vk.html')


def register_ok(request):
    code = request.GET.get('code')
    if code:
        client_id = settings.OK_APP_ID
        client_secret = settings.OK_API_SECRET
        con = HTTPConnection('api.ok.ru')
        url = "/oauth/token.do?code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri=http://127.0.0.1:8000/register_activate/register_ok/?&grant_type=authorization_code".format(
            client_id=client_id, client_secret=client_secret, code=code)
        con.request('POST', url)
        result = con.getresponse()
        res = json.loads(result.read().decode('cp1251'))
        print(res)
        access_token = res['access_token']
        refresh_token = res['refresh_token']
        expires_in = res['expires_in']

        application_key = 'CBACIQHLEBABABABA'
        url = "/fb.do?method=friends.get&access_token={access_token}".format(application_key=application_key,
                                                                             access_token=access_token)
        con.request('POST', url)
        result = con.getresponse()
        res = json.loads(result.read().decode('cp1251'))
        print(res)

        print(type(res), access_token)
        con.close()
        return render(request, 'register_ok.html', {'code': code})


def register_f(request):
    return render(request, 'register_f.html')


@login_required(login_url='/register_activate/signin/')
def congratulations(request):
    if request.method == 'POST':
        data = request.POST['data']
        type_name = Type.objects.filter(data=data)
        return render(request, 'congratulations.html', {'data': data,
                                                        'type_name': type_name})
    if request.method == 'GET':
        type_name_id = request.GET.get('type_name_id', None)
        if type_name_id:
            type_name = Type.objects.filter(name=type_name_id)
            congratulations_text = Congratulations.objects.filter(type_id=type_name[0].id, status=2)
            return render(request, 'congratulations.html', {'type_name_id': type_name_id,
                                                            'data': type_name[0].data,
                                                            'congratulations_text': congratulations_text})
        else:
            return render(request, 'congratulations.html', {'type_name_id': type_name_id})


@login_required(login_url='/register_activate/signin/')
def congratulations_new(request):
    list = Type.objects.all()
    if request.method == 'POST':
        form = {'text': request.POST['text'],
                'name': request.POST['name'],
                'category_cmc': request.POST['category_cmc']}
        list_name = Type.objects.filter(name=form['name'])
        data_created = datetime.today()
        Congratulations(id=None,
                        text=form['text'],
                        status=1,
                        data_created=data_created,
                        category_cmc=form['category_cmc'],
                        type_id_id=int(list_name[0].id),
                        user_id_id=1).save()
    return render(request, 'congratulations_new.html', {'list': list})


@login_required(login_url='/register_activate/signin/')
def setting_id(request):
    list = User_info.objects.all()
    list_countries = {}
    for code, name in countries:
        list_countries[name] = code
    if request.method == 'POST':
        form = {}
        for i in ['middlename',
                  'name',
                  'surname',
                  'city',
                  'phone',
                  'birthday',
                  'time_zone',
                  'time_congratulations']:
            form[i] = request.POST[i]
        form['gender'] = request.POST.get('gender', False)
        form['country'] = request.POST.get('country', False)
        form['country'] = (list_countries[form['country']] if form['country'] else None)
        id = request.user.id
        User_info(id,
                  middlename=form['middlename'],
                  name=form['name'],
                  surname=form['surname'],
                  country=form['country'],
                  city=form['city'],
                  phone=(form['phone'] if form['phone'] else None),
                  birthday=(form['birthday'] if form['birthday'] else None),
                  gender=(form['gender'] if form['gender'] else None),
                  time_zone=form['time_zone'],
                  time_congratulations=form['time_congratulations']).save()
    if list:
        return render_to_response('setting_id.html', {'list': list[0], 'list_countries': list_countries},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('setting_id.html', {'list_countries': list_countries},
                                  context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            user = authenticate(username=username, password=password)
            print(user)
            user.is_active = False
            user.save()
            id = user.id
            email = user.email
            send_email(email, id)
            return render(request, 'thankyou.html')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = forms.SignupForm()
        return render(request, 'register.html', {'form': form})


def activate(request):
    id = int(request.GET.get('id'))
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return render(request, 'activation.html')


def log_in(request):
    if request.method == 'POST':
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            if email:
                user = authenticate(username=email, password=password)
            else:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('register_activate:mainpage')
                else:
                    return render(request, 'ErrorPage.html')
            else:
                return render(request, 'ErrorPage.html', {'errormessage': 'Invalid login'})
        else:
            return render(request, 'log_in.html', {'form': form})
    else:
        form = forms.SigninForm()
        return render(request, 'log_in.html', {'form': form})


@login_required(login_url='/register_activate/signin/')
def mainpage(request):
    if request.method == 'GET':
        message = _("Вы успешно вошли в систему")
        return render(request, 'mainpage.html', {'user': request.user, 'message': message})
    elif request.method == 'POST':
        if request.POST.get("logout"):
            return redirect('register_activate:logout')
        else:
            return redirect('register_activate:thankyou')


def log_out(request):
    logout(request)
    return render(request, 'log_out.html')


def letter(request):
    letter_id = request.GET.get('letter_id', None)
    data_current = datetime.today()
    if request.method == 'POST':
        email = request.POST['email']
        text = request.POST['text']
        date_send = request.POST['date_send']
        '''
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
        letter_id = "Ваше письмо отправлено!!!"
'''
        Letters(user_letters_id=1,
                text_letters=text,
                date_create=datetime.today(),
                email_create=email,
                date_send=date_send,
                email_send=email,
                status=2).save()

        return render(request, 'letter.html', {'letter_id': letter_id,
                                               'data_current': data_current})

    return render(request, 'letter.html', {'letter_id': letter_id,
                                           'data_current': data_current})


def send_email(toaddr, id):
    fromaddr = settings.EMAIL_HOST
    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    text = 'Пройдите по этой ссылке :\nhttp://127.0.0.1:8000/register_activate/activation/?id=%s' \
           % id
    subject = "Спасибо за регистрацию"
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    mail_coding = 'windows-1251'
    part1 = MIMEText(text.encode('cp1251'), 'plain', mail_coding)
    msg.set_charset(mail_coding)
    msg.attach(part1)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, [toaddr], msg.as_string())
    server.quit()


def make_salt():
    letters = string.ascii_letters
    result = random.sample(letters, 5)
    return ''.join(result)
