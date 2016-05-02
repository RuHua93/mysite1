#coding=utf-8
from _threading_local import local

import datetime
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

def getShow(pn):
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    conn.row_factory = sqlite3.Row
    csr.execute("select count(*) from sqlDemo")
    cnt = int(csr.fetchall()[0][0])
    offset = int(pn) * 10 - 10
    csr.execute("select * from sqlDemo order by time desc, ctime desc limit 10 offset ?", (offset,))
    items = csr.fetchall()
    return items, cnt

def getMyOrder(uid, pn):
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    conn.row_factory = sqlite3.Row
    csr.execute("select count(*) from od where uid=?", (uid,))
    cnt = int(csr.fetchall()[0][0])
    offset = int(pn) * 10 - 10
    csr.execute("select * from sqlDemo, od where sqlDemo.did=od.did and od.uid=? order by time desc, ctime desc limit 10 offset ?;", (uid, offset,))
    items = csr.fetchall()
    return items, cnt

def getOrder(uid):
    odr = []
    conn = sqlite3.connect("/tmpdb/newdb.db")
    conn.row_factory = sqlite3.Row
    csr = conn.cursor()
    csr.execute("select * from od where uid=?", (uid,))
    items = csr.fetchall()
    for item in items:
        odr.append(item["did"])
    return odr

def getOneItem(did):
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    conn.row_factory = sqlite3.Row
    csr.execute("select * from sqlDemo where did=?", (did,))
    items = csr.fetchall()
    ret = None
    for item in items:
        ret = item
    return ret

def getTopHigh():
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    conn.row_factory = sqlite3.Row
    num = 5
    csr.execute("select * from sqlDemo order by rnum desc limit ?", (num,))
    top_items = csr.fetchall()
    csr.execute("select * from sqlDemo order by rate desc limit ?", (num,))
    high_items = csr.fetchall()
    return top_items, high_items

def getCmt(uid, did):
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    conn.row_factory = sqlite3.Row
    csr.execute("select user.uname, comment.* from user, comment where user.uid=comment.uid and did=?", (did,))
    cnt = 0
    cmts = csr.fetchall()
    for cmt in cmts:
        cnt += 1
    csr.execute("select * from comment where did=?", (did,))
    dcmted = "no"
    dcmt = csr.fetchall()
    if dcmt:
        dcmted = "yes"
    csr.execute("select * from comment where did=? and uid=?", (did,uid))
    mcmt = csr.fetchall()
    cmted = "no"
    if mcmt:
        cmted = "yes"

    return cnt, cmts, cmted, dcmted

# 计算需要展示的页码范围
def getRange(pn, pcnt):
    if pcnt <= 10:
        return 1, pcnt
    left = pn-4
    right = pn+5
    if pn - 4 < 1:
        left = 1
        right = 10
    elif pn + 5 > pcnt:
        left = pcnt - 9
        right = pcnt
    return left, right

def welcome(req):
    return render_to_response('welcome.html')

def login(req):
    return render_to_response('login.html',{},context_instance=RequestContext(req))

def register(req):
    return render_to_response('register.html',{},context_instance=RequestContext(req))

def cmt(req):
    username=req.COOKIES.get("username")
    uid=req.GET["uid"]
    did=req.GET["did"]
    top_items, high_items = getTopHigh()
    citem = getOneItem(did)
    ccnt, cmts, cmted, dcmted = getCmt(uid, did)
    dic = {"citem":citem, "username":username, "h_items":high_items, "t_items":top_items,
           "dcmted":dcmted, "uid":uid, "did":did, "ccnt":ccnt, "cmts":cmts, "cmted":cmted}

    return render_to_response('cmt.html',dic,context_instance=RequestContext(req))

def show(req):
    username=req.COOKIES.get("username")
    uid = req.COOKIES.get("uid")
    pn = req.GET["pn"]
    pn = int(pn)
    items, cnt = getShow(pn)
    odr = getOrder(uid)
    # print odr
    top_items, high_items = getTopHigh()
    # 向上取整
    pcnt = (cnt + 10) / 10
    left, right = getRange(pn, pcnt)
    lim = []
    for i in range(left, right+1):
        lim.append(i)
    dic = {"pn":int(pn), "uid":uid, "items":items, "username":username, "pcnt":int(pcnt), "odr":odr,
           "h_items":high_items, "t_items":top_items, "ppre":int(pn)-1, "pnxt":int(pn)+1, "lim":lim}
    return render_to_response('show.html',dic,context_instance=RequestContext(req))

def myorder(req):
    username=req.COOKIES.get("username")
    uid = req.COOKIES.get("uid")
    pn = req.GET["pn"]
    pn = int(pn)
    items, cnt = getMyOrder(uid, pn)
    odr = getOrder(uid)
    # print odr
    top_items, high_items = getTopHigh()
    # 向上取整
    pcnt = (cnt + 10) / 10
    left, right = getRange(pn, pcnt)
    lim = []
    for i in range(left, right+1):
        lim.append(i)
    dic = {"pn":int(pn), "uid":uid, "items":items, "username":username, "pcnt":int(pcnt), "odr":odr,
           "h_items":high_items, "t_items":top_items, "ppre":int(pn)-1, "pnxt":int(pn)+1, "lim":lim}
    return render_to_response('myorder.html',dic,context_instance=RequestContext(req))


def doreg(req):
    # do reg
    username = req.POST.get('uname')
    email = req.POST.get('uemail')
    password = req.POST.get('upwd')
    conn = sqlite3.connect("/tmpdb/newdb.db")
    csr = conn.cursor()
    csr.execute("select * from user where uname=?", (username,))
    recs = csr.fetchall()
    if recs:
        return render_to_response('register.html', {"regstat":"fail", "str":"用户名已存在"},context_instance=RequestContext(req))
    csr.execute("select * from user where email=?", (email,))
    recs = csr.fetchall()
    if recs:
        return render_to_response('register.html', {"regstat":"fail", "str":"该邮箱已注册"},context_instance=RequestContext(req))
    conn.execute("insert into user(uname, pwd, email) values(?, ?, ?);", (username, password, email,))
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
        conn = sqlite3.connect("/tmpdb/newdb.db")
        conn.row_factory = sqlite3.Row
        csr = conn.cursor()
        print username
        csr.execute("select uid, pwd, uname from user where uname=?", (username,))
        recs = csr.fetchall()
        if recs:
            print 1
            for rec in recs:
                if rec["pwd"] == password:
                    print rec["uid"]
                    response = HttpResponseRedirect('show?pn=1')
                    response.set_cookie('username', rec["uname"], 3600)
                    response.set_cookie('uid', rec["uid"], 3600)
                    return response
        return render_to_response("login.html", {"logstat":"fail", "str":"用户名或密码不正确"},context_instance=RequestContext(req))
    # render_to_response("test.html",{},context_instance=RequestContext(req))
    return render_to_response('show.html',{},context_instance=RequestContext(req))

def logout(req):
    # 清除cookie并返回登录页
    response = render_to_response("login.html",{},context_instance=RequestContext(req))
    response.delete_cookie('username')

    return response

# 处理订阅ajax请求,更新数据库
def order(req):
    uid=req.GET["uid"]
    did=req.GET["did"]
    conn = sqlite3.connect("/tmpdb/newdb.db")
    conn.execute("insert into od(uid, did) values(?, ?);", (uid, did,))
    conn.commit()
    print "done"

    return

# 处理退订ajax请求,更新数据库
def unorder(req):
    uid=req.GET["uid"]
    did=req.GET["did"]
    conn = sqlite3.connect("/tmpdb/newdb.db")
    conn.execute("delete from od where uid=? and did=?;", (uid, did,))
    conn.commit()

    return

def docmt(req):
    uid = req.GET["uid"]
    did = req.GET["did"]
    rate = float(req.POST.get("result"))
    txt = req.POST.get("cmtarea")
    conn = sqlite3.connect("/tmpdb/newdb.db")
    conn.row_factory = sqlite3.Row
    csr = conn.cursor()
    mydate = datetime.datetime.now().strftime("%Y-%m-%d %X")

    conn.execute("insert into comment(uid, did, cmt, rate, date) values(?,?,?,?,?)",
                 (uid, did, txt, rate, mydate))
    conn.commit()
    csr.execute("select * from sqlDemo where did=?", (did,))
    recs = csr.fetchall()
    ditem = None
    for rec in recs:
        ditem = rec
    old_rnum = float(ditem["rnum"])
    old_rate = float(ditem["rate"])
    new_rnum = round(old_rnum + 1.0, 2)
    new_rate = round((old_rate * old_rnum + rate) / new_rnum, 2)
    conn.execute("update sqlDemo set rnum=?, rate=? where did=?", (new_rnum, new_rate, did))
    conn.commit()
    response = HttpResponseRedirect('cmt?uid='+str(uid)+'&did='+str(did))
    return response

def test(req):
    return render_to_response('/static/test.txt')

