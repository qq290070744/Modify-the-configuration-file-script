#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json,os,sys
def cha(backend):#定义查询的函数
    li=[]
    falg=False
    with open('1.txt') as f:
        for i in f:
            if i.strip()=='backend %s'%backend:#如果找到了backend 123.xxx.com这一行则重新循环
                falg=True
                continue
            if falg and i.strip().startswith('backend'):#如果再次遇到backend开头的结束
                falg=False
                break

            if falg and i.strip():#添加查询后的内容到列表
                li.append(i.strip())

    return  li

def add(dic):#定义添加的函数
    backend_v=dic.get('backend')
    start_backend='backend %s'%backend_v
    record_v="server %s weight %s maxconn %s" %(dic['record']['server'],dic['record']['weight'],dic['record']['maxconn'],)
    chalist=cha(backend_v)#调用查询函数


    if chalist and backend_v:#如果backebd下有内容存在则在下面添加一条记录
        if record_v in chalist:#如果要添加的内容已存在，则不添加，提示重新输入
            print("添加的内容已存在，请重新输入")
            II()
            pass
        else:
            chalist.append(record_v)

            flag=False
            xie=False
            with open('1.txt') as f_r,open('2.txt','w') as f_w:#同时打开两个文件一个读，一个写
                for i in f_r:
                    if i.strip()==start_backend:
                        flag=True
                        f_w.write(i)
                        continue
                    if flag and i.strip().startswith('backend'):
                        flag=False
                    if flag:
                        if not xie:
                            for new_i in chalist:
                                f_w.write('%s%s\n'%(" "*8,new_i))
                            xie=True
                    else:
                        f_w.write(i)
            print("存在%s的记录，并了插入要添加的内容"%start_backend)
            os.rename("1.txt","1.txt.bak")
            os.rename("2.txt","1.txt")

    else:#如果以backend开头的不存在，则创建以backend开头的记录并在下面增加内容
        with open("1.txt") as f_r,open("2.txt",'w') as f_w:
            for i in f_r:
                f_w.write(i)
            f_w.write('\n%s\n'%start_backend)
            f_w.write('        %s\n'%record_v)
        print("不存在以%s的记录，系统自动创建了%s的记录并在下面插入了要增加了内容"%(start_backend,start_backend))
        os.rename("1.txt","1.txt.bak")#给文件改名
        os.rename("2.txt","1.txt")

def dele(dic):#定义删除函数
    backend_v=dic.get('backend')
    start_backend='backend %s'%backend_v
    record_v="server %s weight %s maxconn %s" %(dic['record']['server'],dic['record']['weight'],dic['record']['maxconn'],)
    chalist=cha(backend_v)
    if chalist:
        if record_v in chalist:#如果存在要删除内容则remove否则提示重新输入
            chalist.remove(record_v)
            flag=False
            xie=False
            with open('1.txt') as f_r,open('2.txt','w') as f_w:
                for i in f_r:
                    if i.strip()==start_backend:
                        flag=True
                        f_w.write(i)
                        continue
                    if flag and i.strip().startswith('backend'):
                        flag=False
                    if flag:
                        if not xie:
                            for new_i in chalist:
                                f_w.write('%s%s\n'%(" "*8,new_i))
                            xie=True
                    else:
                        f_w.write(i)
            print("已删除记录")
            os.rename("1.txt","1.txt.bak")
            os.rename("2.txt","1.txt")
        else:
            print("不存在你要删除的内容请重新输入")
            III()
    else:
        #如果backend下所有的记录都已经被删除，那么将当前 backend test.oldboy.org 也删除掉。

        with open("1.txt") as f_r,open("2.txt",'w') as f_w:
            for i in f_r:
                if i.strip()==start_backend:
                    continue
                f_w.write(i)
        print("%s下不存在记录，系统删除了%s"%(start_backend,start_backend,))

        os.rename("1.txt","1.txt.bak")
        os.rename("2.txt","1.txt")



enter=input("输入1查询，2增加，3删除：")
if enter=="1":
    def I():
        chanr=input("请输入要查询的内容格式如：’buy.oldboy.org‘:")
        print(cha(chanr))
    I()
elif enter=='2':
    def II():
        while True:
            try:
                print(''' {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}''')
                zeng = input('请输入要新加的记录(格式如上)：')
                z=json.loads(zeng)#把字符串转换成字典
            except json.decoder.JSONDecodeError:
                print("请输入正确的格式")
                continue
            else:
                break
        add(z)
    II()

elif enter=='3':
    def III():
        while True:
            try:
                shan = input('请输入要删除的记录：格式如： {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}:')
                s=json.loads(shan)
            except json.decoder.JSONDecodeError:
                print("请输入正确的格式")
                continue
            else:
                break
        dele(s)
    III()
