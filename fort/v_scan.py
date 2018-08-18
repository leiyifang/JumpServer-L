#-*- coding:utf-8 -*-
# -*- coding: utf-8 -*-

import time
import pyclamd
from threading import Thread
import subprocess


class Scan(Thread):
    def __init__(self, IP, scan_type, file):
        Thread.__init__(self)
        self.IP = IP
        self.scan_type = scan_type
        self.file = file
        self.connstr = ""
        self.scanresult = ""

    def run(self):
        try:
            cd = pyclamd.ClamdNetworkSocket(self.IP, 3310)
            if cd.ping():
                self.connstr = self.IP + " connection [OK]"
                cd.reload()
                if self.scan_type == "contscan_file":
                    self.scanresult = "{0}\n".format(cd.contscan_file(self.file))
                elif self.scan_type == "multiscan_file":
                    self.scanresult = "{0}\n".format(cd.multiscan_file(self.file))
                elif self.scan_type == "scan_file":
                    self.scanresult = "{0}\n".format(cd.scan_file(self.file))
                time.sleep(1)
            else:
                self.constr = self.IP + " ping error,exit"
                return
        except Exception as  e:
            self.connstr = self.IP + " " + str(e)


ip_list = subprocess.Popen(
    'mysql -hxx.xx.xx -uxx -pxxx -e "use xxx; select ip from jasset_asset;" | egrep -v "ip|x.x.x.x|x.x.x.x|x.x.x.x"',
    shell=True, stdout=subprocess.PIPE)

IPs = ip_list.stdout.read()
IPs = bytes.decode(IPs.split("\n"))
scan_type = "multiscan_file"
# scanfile="/data/code/pancool_laravel"
scanfiles = ["/data/code/pancool_laravel", "/data/code/qixin-lawyer/file", "/data/code/weichi"]
i = 1

threadnum = 20
scanlist = []

for ip in IPs:

    for scanfile in scanfiles:
        currp = Scan(ip, scan_type, scanfile)
        scanlist.append(currp)

        if i % threadnum == 0 or i == len(IPs):
            for task in scanlist:
                task.start()

            for task in scanlist:
                task.join()
                print
                task.connstr
                print
                task.scanresult
            scanlist = []
        i += 1
