#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import sys
import datetime
import logging

# get account and passowrd by 1st, 2nd line, ex:
# admin
# UGE1NXdvcmQ=  ## =  base64(Pa55word), avoid shoulder surfing
# rename sample.auth.txt to auth.txt
def getAuth():
    with open("./config/auth.config") as auth:
        authtext = auth.readlines()
        authtext =[x.strip('\n') for x in authtext]
    return authtext


def mail_content(feed, keywords, content):
    print("Construct mail content")
    # Complete below information please.
    auth = getAuth()
    username = auth[0]
    password = base64.b64decode(auth[1]).decode('ascii')
    fromaddr = username + '@gmail.com'
    part = "*******\n\n"

    # The actual mail send
    #server = smtplib.SMTP('mail.ecpay.com.tw', 587)
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Get Mail List
    toaddrs = ''
    for line in open("./config/mail_list.lst"):
        li = line.strip()
        if not li.startswith("#"):
            toaddrs += li + ","
    toaddrs = toaddrs[:-1]  # remove last comma

    # Setting Mail Address and Subject
    #print("mail content:"+str(content))
    vul_count = extract_content_count(feed, content)
    dnsZoneTransferSuccess = False
    dnsZoneTransferResult, dnsZoneTransferCount = doZoneTransfer()
    if dnsZoneTransferResult != "":
        dnsZoneTransferSuccess = True
    mailSubject = "Subject: (" + str(vul_count) + " - " + dnsZoneTransferCount + ") Security Keywords Alert " + datetime.date.today().strftime("%Y-%m-%d")
    logging.debug("mail Subject: " + mailSubject)
    #mailSubject = "Subject: test"
    msg = "\r\n".join([
        "From: " + fromaddr,
        "To: null",
        mailSubject ,
        "",
        "Keywords: " + keywords.replace('|', ' | ').lower() + "\n\n" 
    ])
    mail_body = extract_content(feed, content)
    if not mail_body.strip():
        msg += "Keyword alert no news is good news!\n\n\n\n"
    else:
        msg += mail_body
    msg += part
    logging.debug("msg add feed done.")
    msg += domain()
    logging.debug("msg add domain done.")
    if dnsZoneTransferSuccess:
        msg += part
        msg += dnsZoneTransferResult
    logging.debug("msg add zone transfer done.")
    msg = msg.encode('ascii', 'replace')
    logging.debug("mail full message:" + str(msg))

    server.starttls() # why we not use tls?
    try:
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs.split(','), msg)
        logging.info("mail_content() - toaddrs:" + toaddrs + ", mail_msg:" + str(msg) )
        server.quit()
    except:
        logging.error("mail_content() - mail send error")
        logging.critical("Unexpected error", sys.exc_info()[0])
    logging.debug("mail to " + toaddrs)


def extract_content(feed, content):
    mail_contents = ""
    logging.debug("start extract feed content")
    for key in content.keys():
        if len(content[key]) != 0:
            mail_contents += "Site: " + key + " 嚗� \r\n"
            # ���誑content['site_feed']憛𧼮��, 隞亙�𠰴ế�𪃾�糓銝齿糓蝛箇�
            for v in content[key]:
                mail_contents += str(v) + " \n\n"
            mail_contents += "\n\n\n"
    return mail_contents


def extract_content_count(feed, content):
    vul_count = 0
    logging.debug("start extract feed content count")
    for key in content.keys():
        if len(content[key]) != 0:
            vul_count += len(content[key])
    return vul_count


def domain():
    dns_main_content = ''
    dns_unsort = whois_query.whois_query()
    notify_days = 7
    #print(dns)
    dns = OrderedDict(sorted(dns_unsort.items(), key=itemgetter(1)))
    #dns = OrderedDict(sorted(dns_unsort.items()))
    for d in dns:
        if d in dns:
            if dns[d] != '':
                expire_date = dns[d]
                expire_days = datetime.datetime.strptime(dns[d], '%Y-%m-%d') - datetime.datetime.now()
                dns_main_content += ("%s - Expires: %s - Days: %s \n\n" % (d, str(expire_date), str(expire_days.days)))
                if int(expire_days.days) < notify_days:
                    dns_main_content += ("Expires Day %s < %s !!\n\n" % (str(expire_days.days), str(notify_days)))
            else:
                dns_main_content += ("{domain} process expires date fail \n\n".format(domain=d))
        else:
            dns_main_content += ("{domain} process expires date fail \n\n".format(domain=d))
    logging.info("dns_main_content: {dns_main_content}.".format(dns_main_content=dns_main_content))
    return dns_main_content

def doZoneTransfer():
    #zoneTransfer.logSetting()
    dnList = zoneTransfer.loadList()
    dnsZTFresult, dnsZTFCount = zoneTransfer.passiveZoneTransfer(dnList)
    return dnsZTFresult, str(dnsZTFCount)