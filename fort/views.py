from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from . import models
from django.db.models import Q
from .server import WSSHBridge
from .server import add_log
# from .v_scan import Scan

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名和密码正确
            userprofile = models.UserProfile.objects.get(user=user)
            if userprofile.enabled:
                auth_login(request, user)
                return redirect('/index/')
            else:
                # enabled=False
                message = '该用户已经被禁用，请联系管理员！'
                return render(request, 'fort/login.html', locals())
        else:
            # 登录失败
            message = '登录失败，用户名或者密码错误！'
            return render(request, 'fort/login.html', locals())
    return render(request, 'fort/login.html', locals())

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def index(request):
    # request.user
    remote_user_bind_hosts = models.RemoteUserBindHost.objects.filter(
        Q(enabled=True),
        Q(userprofile__user=request.user)|Q(group__userprofile__user = request.user)).distinct()
    return render(request,'fort/index.html',locals())


@login_required(login_url='/login/')
def connect(request,user_bind_host_id):
    # 如果当前请求不是websocket请求，则退出
    if not request.environ.get('wsgi.websocket'):
        return HttpResponse('错误，非websocket请求！')
    try:
        remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
            Q(enabled=True),
            Q(id=user_bind_host_id),
            Q(userprofile__user=request.user) | Q(group__userprofile__user=request.user)).distinct()[0]
    except Exception as e :
        message = '无效的账户或者无权访问！\n' + str(e)
        add_log(request.user,message,log_type='2')
        return HttpResponse('请求主机发生错误!')

    message = '来自{remote}的请求 尝试连接 -> {username} @ {hostname} <{ip} : {port}>'.format(
        remote = request.META.get('REMOTE_ADDR'),
        username = remote_user_bind_host.remote_user.remote_user_name,
        hostname = remote_user_bind_host.host.host_name,
        ip = remote_user_bind_host.host.ip,
        port = remote_user_bind_host.host.port
    )
    print(message)
    add_log(request.user, message, log_type='0')

    bridge = WSSHBridge(request.environ.get('wsgi.websocket'),request.user)
    try:
        bridge.open(
            host_ip=remote_user_bind_host.host.ip,
            port=remote_user_bind_host.host.port,
            username=remote_user_bind_host.remote_user.remote_user_name,
            password=remote_user_bind_host.remote_user.password
        )
    except Exception as e:
        message = '尝试连接{0}的过程中发送错误： \n {1}'.format(
            remote_user_bind_host.remote_user.remote_user_name,e)
        print(message)
        add_log(request.user,message,log_type='2')
        return HttpResponse('错误！无法建立SSH连接！')

    bridge.shell()

    request.environ.get('wsgi.websocket').close()
    print('用户断开连接......')
    return HttpResponse('200,ok')

@login_required(login_url='/login/')
def get_log(request):
    if request.user.is_superuser:
        logs = models.AccessLog.objects.all()
        return render(request,'fort/log.html',locals())
    else:
        add_log(request.user, '非超级用户尝试访问日志系统',log_type='4')
        return redirect('/index/')

@login_required(login_url='/login/')
def virus_scan(request):
    # request.host
    remote_user_bind_hosts = models.RemoteUserBindHost.objects.filter(
        Q(enabled=True),
        Q(userprofile__user=request.user)|Q(group__userprofile__user = request.user)).distinct()
    return render(request,'fort/virus_scan.html',locals())


