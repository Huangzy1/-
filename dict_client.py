#!/usr/bin/python3
#coding=utf-8

from socket import *
import sys
import getpass

#创建网络连接
def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    s=socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    #连接成功之后
    while True:
            print("+---------------------------+")
            print("|       电子词典v1.0        |")
            print("| 1)  注册            　　  |")
            print("| 2)  登录               　 |")  
            print("| 3)  退出                  |")
            print("+---------------------------+")
            try:
                cmd=int(input('请输入选项：'))
            except:
                print('请输入正确的选项！')
                continue

            if cmd not in [1,2,3]:
                print('请输入正确的选项！')
                sys.stdin.flush(0)  #清除标准输入
                continue
            elif cmd==1:
                r=do_register(s)
                if r==0:
                    print('注册成功')
                elif r==1:
                    print('用户存在')
                else:
                    print('注册失败')
            elif cmd==2:
                name=do_login(s)
                if name:
                    print('登录成功')
                    login(s,name)
                else:
                    print('登录失败')
            elif cmd==3:
                s.send(b'E')
                sys.exit('谢谢使用')

#注册操作
def do_register(s):
    while True:
        name=input('User:')
        password=getpass.getpass()
        password1=getpass.getpass('Again:')

        if (' ' in name)or(' ' in password):
            print('用户名和密码不能有非法字符！')
        if password != password1:
            print('两次密码不一致')
            continue

        msg='R {} {}'.format(name,password)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data=s.recv(128).decode()
        if data=='ok':
            return 0
        elif data=='EXISTS':
            return 1
        else:
            return 2

#登录操作
def do_login(s):
    name=input('User:')
    password=getpass.getpass()
    msg='L {} {}'.format(name,password)
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=='ok':
        return name
    else:
        return

#二级登录界面
def login(s,name):
     while True:
        print("+---------------------------+")
        print("| 1)  查单词            　  |")
        print("| 2)  查看历史记录       　 |")  
        print("| 3)  退出                  |")
        print("+---------------------------+")
        try:
                cmd=int(input('请输入选项：'))
        except:
                print('请输入正确的选项！')
                continue

        if cmd not in [1,2,3]:
                print('请输入正确的选项！')
                sys.stdin.flush(0)  #清除标准输入
                continue
        elif cmd==1:
            do_query(s,name)
        elif cmd==2:
            do_hist(s,name)
        elif cmd==3:
            return

def do_query(s,name):
    while True:
        word=input('请输入查询的单词:')
        if word=='##':
            break
        msg='Q {} {}'.format(name,word)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='ok':
            data=s.recv(2048).decode()
            print(data)
        else:
            print('没有查到该单词')

def do_hist(s,name):
    name=input('请输入要查询的姓名:')
    msg='H {}'.format(name)
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=='ok':
        while True:
            data=s.recv(1024).decode()
            if data=='##':
                break
            print(data)
    else:
        print('没有历史记录')

if __name__ == '__main__':
    main()