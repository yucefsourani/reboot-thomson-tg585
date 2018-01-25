#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  reboot_thomson_tg585.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>

import telnetlib
from time import sleep
from os import system


host               = "192.168.1.254"
port               = 23 #default telnet port
user               = b"Administrator\r\n"
password           = b"\r\n" #blank password
user_readuntil     = b"Username : "
password_readuntil = b"Password : "


def telnet_parser(host,port,user,password,user_readuntil,password_readuntil):
    """connect and return telnetlib.Telnet Object """
    try:
        telnet_co = telnetlib.Telnet(host,port)
        telnet_co.read_until(user_readuntil)
        telnet_co.write(user)
        telnet_co.read_until(password_readuntil)
        telnet_co.write(password)
    except Exception as e:
        print(e)
        return False

    return telnet_co

def main():
    telnetparser = telnet_parser(host,port,user,password,user_readuntil,password_readuntil)
    if telnetparser:
        telnetparser.write(b"xdsl\r\n")
        telnetparser.write(b"info\r\n")

        info     = telnetparser.read_until(b"\0",1).decode("utf-8")
        speed    = info.split("\t\t")[-1].split("\r")[0].strip().split("/")
        download = speed[0]
        upload   = speed[1]
        
        telnetparser.write(b"..\r\n")
        telnetparser.write(b"ip\r\n")
        telnetparser.write(b"iflist\r\n")
        info     = telnetparser.read_until(b"\0",1).decode("utf-8").split("\n")
        
        while True:
            system("clear")
            print ("*********************************")
            print ("* youssef.m.sourani@gmail.com   *")
            print ("* https://arfedora.blogspot.com *")
            print ("* Thomson Gateway TG585 v7      *")
            print ("*********************************\n")
            print(info[3])
            print(info[4])
            print(info[5])
            print(info[6])
            print ("\nDownload Speed : {} kbps".format(download))
            print ("Upload   Speed : {}  kbps\n\n".format(upload))
            print("R To Reboot Modem || F To Refresh || Q To Quit :\n")
            answer = input("- ").strip()
            if answer == "q" or answer == "Q":
                break
            elif answer == "f" or answer == "F":
                telnetparser.close()
                return main()
            elif answer == "r" or answer == "R":
                telnetparser.write(b"..\r\n")
                telnetparser.write(b"system\r\n")
                telnetparser.write(b"reboot\r\n")
                break
        
        telnetparser.close()
        print("\nbye..")
    else:
        print("Connect {}:{} Fail.".format(host,port))
   
main()
