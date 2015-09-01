#!/usr/bin/env python
#coding=utf8
"""NTP Scanner and 'monlist' checker

INSTALLATION: (debian)--
    sudo apt-get install python-pip python-argparse ntp;
    sudo pip install ntplib iptools;


Usage:
    python ntp-scanner.py [ARGS]
    -f, --file          : specify input file
    -t, --target        : specify specific host or subnet(cidr)
    --help              : print help
"""

from ntplib import *
from time import ctime,sleep
import os
import argparse
import iptools
import sys

class c:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

ERROR = "[" + c.FAIL + " !! " +c.ENDC + "] "
OK = "[" + c.OKGREEN + " OK " + c.ENDC + "] "

arg = argparse.ArgumentParser()
arg.add_argument("-t", "--target", help="Scan NTP for a given host")
arg.add_argument("-f", "--file", help="Input file")
args = arg.parse_args()
addr = args.target
scan_file = args.file

def check_ntp(addr):
    try:
	n = NTPClient()
	ans = n.request(addr, version=3)
	print OK + "NTP is enabled on {}".format(addr)
	print "\t" + ctime(ans.tx_time)
	test_monlist = os.system("ntpdc -c monlist {}".format(addr))
        if test_monlist is None:
            print ERROR+"Unable to query monlist on {}\n".format(addr)
        else:
            print OK+"monlist query successful on {}\n".format(addr)
    except KeyboardInterrupt:
	print "Exiting on user interrupt.."
        sys.exit()
    except Exception, e:
	print ERROR + "Error Connecting to {} \n  {}\n".format(addr,str(e))

if __name__ == '__main__':
    if not "/" in args.target:
        print addr
        check_ntp(addr)
    elif "/" in args.target:
        range = iptools.IpRange(addr)
        for ip in range:
            print ip
            check_ntp(ip)
    elif args.file:
        with open(scan_file, 'r') as f:
            for line in f:
                check_ntp(line)
    else:
        print "You must supply a host to scan"
        sys.exit(2)
