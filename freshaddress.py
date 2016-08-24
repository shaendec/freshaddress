#!/usr/bin/env hpython

import argparse, requests, json
import util

KEY = "<key>"
API_URL = "https://listvet.freshaddress.com/api?apikey=" + KEY

def postList(emailList):
    emailFile = {"file": open(emailList, "rb")}
    r = requests.post(API_URL, files=emailFile)
    resp = r.json()
    if resp["status"] != "ok":
        util.fatal("%s" % resp["message"])
    else:
        results = {}
        report = '''
File:                  {filename}
Count:                 {count}
Purchased/harvested:   {p_flag}
Deliverability:        {d_flag}
Forced signups:        {f_flag}
Spamtrap/blacklist:    {s_flag}
Overall:               {o_flag}
'''
        for k,v in resp.iteritems():
            if isinstance(v, dict):
                results[k] = ",".join(["{key}: {message}".format(key=x, message=y) for x,y in v.iteritems()])
            else:
                results[k] = v
        print report.format(**results)

parser = argparse.ArgumentParser(description="Validate an email list")
parser.add_argument("emailList", help="Email list")

args = parser.parse_args()
postList(args.emailList)
