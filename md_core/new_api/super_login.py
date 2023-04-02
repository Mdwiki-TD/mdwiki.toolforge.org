import sys
import os
import pywikibot
import urllib
import requests
import urllib.parse
from warnings import warn
from new_api import printe
#---
print_test = {1:False}
#---
Main_s = {1:requests.Session()}
#---
User_tables = { "username" : "", "password" : ""}
#---
ar_lag = { 1 : 3 }
#---
import inspect
def warn_err(err):
    err = str(err)
    nn = inspect.stack()[1][3]
    return f'\ndef {nn}(): {err}'
#---
class Login():
    def __init__(self, lang, family='wikipedia'):
        self.lang = lang
        self.username = User_tables['username']
        self.password = User_tables['password']
        #---
        self.Bot_or_himo = ''
        if User_tables['username'].find("bot") == -1:  self.Bot_or_himo = 1
        #---
        self.not_loged   = True
        self.family   = family
        self.endpoint = 'https://' + f'{self.lang}.{self.family}.org/w/api.php'
        self.r3_token = ''
        #---
    #---
    def Log_to_wiki(self):
        #---
        self.not_loged = False
        #---
        Main_s[1] = requests.Session()
        printe.output( "newapi/page.py: Log_to_wiki %s," % self.endpoint)
        #---
        r2_params = {
            'format': 'json',
            'action': 'login',
            'lgname': self.username,
            'lgpassword': self.password,
            'lgtoken' : ''
            }
        #---
        printe.output( "newapi/page.py: log to %s.%s.org user:%s" % (self.lang, self.family, self.username )  )
        #---
        r1_params = { 'format': 'json', 'action': 'query', 'meta': 'tokens', 'type': 'login'}
        #---
        try:
            r11 = Main_s[1].post(self.endpoint, data=r1_params)
            r11.raise_for_status()
            r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
        except Exception as e:
            # WARNING: /data/project/himo/core/newapi/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php
            #---
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(e)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return False
        #---
        r22 = {}
        #---
        if r2_params['lgtoken'] != '':
            try:
                uu  = Main_s[1].post(self.endpoint, data=r2_params)
                r22 = uu.json()
            except Exception as e:
                pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
                warn(warn_err('Exception:' + str(e)), UserWarning)
                pywikibot.output( 'CRITICAL:' )
                return False
        #---
        if r22.get('login', {}).get('result', '').lower() != 'success':
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(r22)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return False
        else:
            printe.output(f'<<green>> {__file__} login Success')
        #---
        try:
            # get edit token
            r33 = Main_s[1].post(self.endpoint, data={'format': 'json', 'action': 'query', 'meta': 'tokens' })
            r3_token = r33.json()['query']['tokens']['csrftoken']
            self.r3_token = r3_token
            Main_s['token'] = r3_token
            printe.output(f'<<green>> r3_token: {self.r3_token}')
        except Exception as e:
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(e)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            #---
            return False
    #---
    def post(self, params, Type='get', addtoken=False):
        #---
        params['format'] = 'json'
        params['utf8']   = 1
        params['bot']    = self.Bot_or_himo
        params["maxlag"] = ar_lag[1]
        #---
        if 'minor' in params and params['minor'] == '' : params['minor'] = self.Bot_or_himo
        #---
        if addtoken or params["action"] in ["edit", "create"]:
            if self.r3_token == '': self.r3_token = Main_s.get('token', '')
            if self.r3_token == '':
                warn(warn_err('self.r3_token == "" '), UserWarning)
                warn(warn_err('self.r3_token == "" '), UserWarning)
            params["token"] = self.r3_token
        #---
        if self.family == "wikipedia" and params.get("summary") and User_tables["username"].find("bot") == -1 :
            params["summary"] = ""
        #---
        if 'workibrahem' in sys.argv: params["summary"] = ""
        #---
        if params['action'] in ['query']:
            if "bot" in params: del params["bot"]
            if "summary" in params: del params["summary"]
        #---
        params["formatversion"] = params.get("formatversion") or "1"
        #---
        url = self.endpoint + '?' + urllib.parse.urlencode(params)
        if print_test[1] or 'printurl' in sys.argv:
            printe.output(url.replace('&format=json', ''))
        #---
        data = {}
        #---
        try:
            response = Main_s[1].post(self.endpoint, data=params)
        except Exception as e:
            printe.output(e)
            return {}
        #---
        try:
            data = response.json()
        except Exception as e:
            printe.output(e)
        #---
        error = data.get("error",{})
        #---
        if error != {}:
            # printe.output(data)
            #---
            Invalid = error.get("info",'')
            code = error.get("code",'')
            #---
            # printe.output(Invalid)
            #---
            if Invalid == "Invalid CSRF token." :
                pywikibot.output('<<lightred>> ** error "Invalid CSRF token.". ')
                #---
                self.Log_to_wiki()
                #---
                return self.post(params, Type=Type, addtoken=addtoken)
        #---
        if 'printdata' in sys.argv:
            # printe.output( json.dumps(data,ensure_ascii=False) )
            printe.output( data )
        #---
        return data
    #---
#---