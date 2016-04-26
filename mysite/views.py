#coding=utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

import sys

# 默认编码改成utf8,不然会报错
reload(sys)
sys.setdefaultencoding("utf-8")

def welcome(req):
    return render_to_response('welcome.html')

def login(req):
    return render_to_response('login.html')

def register(req):
    return render_to_response('register.html')

def show(req):
    return render_to_response('show.html')

def doreg(req):
    # do reg
    return render_to_response('regok.html')
    # str =  "<div class=\"alert alert-error alert-dismissable\">" \
    #        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" onclick" \
    #        "=\"cancel()\">&times;</button><strong>注册成功</strong></div>"
    # return render_to_response('login.html', {'str':str}, context_instance=RequestContext(req))