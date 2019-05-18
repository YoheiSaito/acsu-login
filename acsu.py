#!/usr/bin/python3

import sys, os
import requests
import hashlib

from getpass import getpass
from subprocess import Popen,  check_call

conf_file = "acsu-conf"
pass_file = ".acsupw"
unique_opt =  "zsafhuisehflisehlzdizufhnleuwhlefuihnzluhesfluihenlsuiehzuliweh"

def remove_lf(line_str):
    return line_str.rstrip('\r').rstrip('\n')

def get_conf():
    uid, key = "", ""
    with open(conf_file, "r") as f:
        uid = f.readline()
        key = f.readline()
    return remove_lf(uid), remove_lf(key)

def login_invoke():
    if (not os.path.exists(conf_file)):
        sys.stderr.writelines("execute 'acsu init' first\n")
        return 
    _, k = get_conf()
    python_name = 'python'
    if (os.name == 'posix'):
        python_name = 'python3'
    os.system("openssl enc -d -aes-256-cbc -in " + pass_file + " -k " + k + "| "+ \
            python_name + " " + sys.argv[0] + " " + unique_opt)


def login(u, p):
    dat = { 'uid' : u, 'pwd' : p }
    resp = 1
    try:
        resp = requests.post('https://login.shinshu-u.ac.jp/cgi-bin/Login.cgi', data=dat)
    except:
        sys.stderr.writelines("faild to login\n")
        return
    else:
        print("connect")
    finally:
        if (resp == 0):
            print("success!!")


def init():
    if (not reset()):
        sys.stderr.writelines( "faild to init login info\n")
        return
    uid = input("User name: ")
    pwd = getpass("password: ")
    passwd_tmp_file = "." + hashlib.md5(pwd.encode()).hexdigest()
    
    with open(conf_file, 'w') as f:
        f.write(uid+'\n')

    os.system("openssl rand -base64 6 >> " + conf_file)
    u, k = get_conf()
    if(uid != u):
        sys.stderr.writelines("Faild to store user name\n")
    
    with open(passwd_tmp_file, 'w') as f:
        f.write(pwd)

    check_call(["openssl", "aes-256-cbc","-e", "-in", passwd_tmp_file,\
            "-out", pass_file, "-pass", "pass:"+k] )

    if(os.path.exists(passwd_tmp_file)):
        os.remove(passwd_tmp_file)
    else:
        sys.stderr.writelines("error\n")

def reset():
    ans = input("Password and username will be reset\n continue? [Y/n] ")

    if(ans == 'Y' or ans == 'y'):
        if(os.path.exists(pass_file)):
            os.remove(pass_file)
        if(os.path.exists(conf_file)):
            os.remove(conf_file)
        return True
    return False

def error():
    print(sys.argv[0])
    print(" 使用方法")
    print("    " + sys.argv[0] + "  init \t... 初期設定")
    print("    " + sys.argv[0] + "  login\t... ログイン")
    print("    " + sys.argv[0] + "  reset\t... 設定リセット")

def main():
    if (len(sys.argv) == 1):
        login_invoke()
    elif (sys.argv[1] == "login"):
        login(input("User Name: "), getpass("password: "))
    elif (sys.argv[1] == unique_opt):
        u, _ = get_conf()
        login( u, input(""))
    elif  (sys.argv[1] == "init"):
        init()
    elif  (sys.argv[1] == "reset"):
        reset()
    else:
        error()
main()
