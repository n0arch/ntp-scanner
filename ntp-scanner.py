#!/usr/bin/env python
#coding=utf8
##
## Checks NTP on a server and tests NTP output if NTP is enabled by: n0arch

from ntplib import *
from time import ctime
import sys, os, argparse

class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

arg = argparse.ArgumentParser()
arg.add_argument("host", help="Scan NTP for a given host")
args = arg.parse_args()
addr = args.host

def checkntp(addr):
    try:
	c = NTPClient()
	ans = c.request(addr, version=3)
	print "[" + colors.OKGREEN + " OK " + colors.ENDC + "] NTP is enabled on %s" % addr
	print "\t" + ctime(ans.tx_time)
	os.system("ntpdc -c monlist %s" % addr)
    except KeyboardInterrupt:
	print "Exiting on user interrupt.."
	sys.exit()
    except:
	print "[" + colors.FAIL + " !! " +colors.ENDC + "] Error Connecting to %s \n" % addr
	sys.exit()

if args.host:
    checkntp(addr)
else:
    print "You must supply a host to scan"
    sys.exit(2)
