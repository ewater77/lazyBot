#! python3
# -*- coding: utf-8 -*-

# File Description: Log Setting
# Author: Walter (mcitocwalter@gmail.com, walter.chen@ecpay.com.tw, https://www.walter.com.tw)
# Date: 2020/02/21
# Version: 1.0
# Environment: Python 3.6.8
# Usage: import and logSetting.logInit()
import os
import sys
import logging
import time
import datetime

def logInit(loglevel=logging.DEBUG, logPath="", logFileMainName=""):
    # Change dir to current python path
    cur_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cur_path)
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    logging.basicConfig(filename="./log/dnsZoneTransfer_" + today +".log", 
                    level=loglevel, 
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Log Init done")

def main():
    logInit()

if __name__ == "__main__":
	main()