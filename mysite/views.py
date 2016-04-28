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
    username=req.COOKIES.get("username")
    conn = sqlite3.connect("/tmpdb/test.db")
    csr = conn.cursor()
    csr.execute("select count(*) from sqlDemo")
    cnt = csr.fetchall()[0][0]
    pcnt = (cnt + 10) / 10
    return render_to_response('show.html',{"username":username, "pcnt":pcnt},context_instance=RequestContext(req))

def doreg(req):
    # do reg
    username = req.POST.get('uname')
    email = req.POST.get('uemail')
    password = req.POST.get('upwd')
    conn = sqlite3.connect("/tmpdb/tb.db")
    csr = conn.cursor()
    csr.execute("select * from user where username=?", (username,))
    recs = csr.fetchall()
    if recs:
        return render_to_response('register.html', {"regstat":"fail", "str":"用户名已存在"},context_instance=RequestContext(req))
    csr.execute("select * from user where email=?", (email,))
    recs = csr.fetchall()
    if recs:
        return render_to_response('register.html', {"regstat":"fail", "str":"该邮箱已注册"},context_instance=RequestContext(req))
    conn.execute("insert into user(username, password, email) values(?, ?, ?);", (username, password, email,))
    print "done"
    conn.commit()
    return render_to_response('login.html',{"regstat":"ok"},context_instance=RequestContext(req))
    # str =  "<div class=\"alert alert-error alert-dismissable\">" \
    #        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" onclick" \
    #        "=\"cancel()\">&times;</button><strong>注册成功</strong></div>"
    # return render_to_response('login.html', {'str':str}, context_instance=RequestContext(req))

def regok(req):
    return render_to_response('login.html',{"regstat":"ok"},context_instance=RequestContext(req))

def dolog(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        conn = sqlite3.connect("/tmpdb/tb.db")
        conn.row_factory = sqlite3.Row
        csr = conn.cursor()
        print username
        csr.execute("select id, password, username from user where username=?", (username,))
        recs = csr.fetchall()
        if recs:
            print 1
            for rec in recs:
                if rec["password"] == password:
                    print rec["id"]
                    response = render_to_response('show.html', {"logstat":"ok", "uid":rec["id"], "username":rec["username"]})
                    response.set_cookie('uid', rec["id"], 3600)
                    response.set_cookie('username', rec["username"], 3600)
                    return response
        return render_to_response("login.html", {"logstat":"fail", "str":"用户名或密码不正确"},context_instance=RequestContext(req))
    # render_to_response("test.html",{},context_instance=RequestContext(req))
    return render_to_response('show.html',{},context_instance=RequestContext(req))