#coding=utf-8
from _threading_local import local
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
import sqlite3

import sys

# 默认编码改成utf8,不然会报错
reload(sys)
sys.setdefaultencoding("utf-8")

def welcome(req):
    return render_to_response('welcome.html')

def login(req):
    # return render_to_response('login.html',{'csrf_token':'T83ow7BDm8RlRP8Hxj622rKExUqyHAm1'})
    return render_to_response('login.html',{},context_instance=RequestContext(req))

def register(req):
    return render_to_response('register.html',{},context_instance=RequestContext(req))

def show(req):
    return render_to_response('show.html')

def doreg(req):
    # do reg
    return render_to_response('login.html',{"regstat":"ok"},context_instance=RequestContext(req))
    # str =  "<div class=\"alert alert-error alert-dismissable\">" \
    #        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" onclick" \
    #        "=\"cancel()\">&times;</button><strong>注册成功</strong></div>"
    # return render_to_response('login.html', {'str':str}, context_instance=RequestContext(req))

def regok(req):
    return render_to_response('login.html',{"regstat":"ok"},context_instance=RequestContext(req))

def dolog(req):
    if req.method == 'POST':
        print 1
        return HttpResponseRedirect('show')

    print 2
    # render_to_response("test.html",{},context_instance=RequestContext(req))
    return render_to_response('show.html',{},context_instance=RequestContext(req))