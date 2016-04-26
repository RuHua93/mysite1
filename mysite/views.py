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