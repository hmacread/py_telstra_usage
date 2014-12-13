#!/usr/bin/python

import urllib2, httplib, ssl
import re

class QuotaInfo(object):

    def __init__(self, timeout=6):

        self.credit = None
        self.expires = None
        self.data = None
        self.URL = 'https://m.telstra.com/ppdata/viewBalanceAction.html?a=view'

        req = urllib2.Request(self.URL)
        html = ""
        try: 
            html = urllib2.urlopen(req, timeout=timeout)
            self.parse(html)
        except ssl.SSLError:
            raise Exception("SSL timeout talking to %s after %ss." % (self.URL, timeout))
        except IOError:
            raise Exception("Could not connect to %s" % self.URL) 

    def parse(self, html):
        for line in html:
            if "credit remaining" in line:
                self.credit = float(re.search(r'[0-9]+\.?[0-9]+', line).group(0))
            if "Credit expires on" in line:
                self.expires = re.search(r'[0-3][0-9] .* 20[0-9][0-9]', line).group(0)
            if re.search(r'[0-9]\.[0-9]*GB', line):
                self.data = float(re.search(r'[0-9]*\.[0-9]*', line).group(0))
        if not (self.credit or self.expires or self.data):
            raise Exception("No quota information found at %s" % self.URL)
                
    
    def ratio_remaining(self):

        #mapping of credit available to data allowance, will change as telstra updates plans
        PLANS = { 200 : 12,
                   100 : 10,
                   50 : 4,
                   30 : 2,
                   15 : 1,
                   }
                   
        if self.credit and int(self.credit) in PLANS:
            return (self.data / PLANS[int(self.credit)])
        else:
            return None
    
    def ratio_used(self):
        return 1 - self.ratio_remaining()
    
class colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

if __name__ == '__main__':

    ERR = "Unavailable"
    
    try:
        q = QuotaInfo()
        print "Data remaining: " + ((str(q.data) + " GB") if q.data else ERR)
        print "Recharge Credit: " + (("$" + str(q.credit)) if q.credit else ERR)
        print "Expiring on: " + (q.expires if q.expires else ERR)
        ratio = q.ratio_used()
        if ratio:
            if 0 < ratio < 0.4 :
                color = colors.GREEN
            elif 0.5 <= ratio < 0.7:
                color = colors.BLUE
            elif 0.7 <= ratio < 0.9:
                color = colors.WARNING
            else:
                color = colors.FAIL
        print "Percent used: " + color + (str(ratio * 100) if ratio else ERR) + "%" + colors.ENDC
    except Exception as e:
        print "Error: " + colors.RED + str(e) + colors.ENDC