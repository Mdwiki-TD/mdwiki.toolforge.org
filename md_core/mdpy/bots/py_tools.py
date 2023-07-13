#!/usr/bin/python

"""

"""
#
# (C) Ibrahem Qasim, 2022
# 
# 
import re
import codecs
import unicodedata
import sys
import urllib
import traceback
import pywikibot
#---
'''
#---
from mdpy.bots import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.Decode_bytes(x)
# py_tools.quoteurl(fao)
#---
'''
#---
PYTHON_VERSION = sys.version_info[:3]
if PYTHON_VERSION >= (3, 9):
    removeprefix = str.removeprefix  # type: ignore[attr-defined]
    removesuffix = str.removesuffix  # type: ignore[attr-defined]
else:
    def removeprefix(string: str, prefix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        if string.startswith(prefix):
            return string[len(prefix):]
        return string

    def removesuffix(string: str, suffix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        if string.endswith(suffix):
            return string[:-len(suffix)]
        return string
#---
def quoteurl(fao):
    endash = False
    #---
    #url2 = urllib.parse.quote_plus(url)
    #---
    if fao.find("–") != -1 : 
        endash = True
        fao = fao.replace("–" , "ioioioioio")
    #---
    try:
        fao = urllib.parse.quote(fao)
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        pywikibot.output(traceback.format_exc())
        pywikibot.output( 'CRITICAL:' )
    #---
    if endash:
        fao = fao.replace("ioioioioio" , "%E2%80%93")
    #---
    return fao
#---
def Decode_bytes(x):
    if type(x) == bytes:    x = x.decode("utf-8")
    return x
#---
def split_lists_to_numbers( lise , maxnumber = 100, out =True ):
    List = {}
    DDone = []
    num = 1 
    #---
    if out:
        pywikibot.output(' split_lists_to_numbers:%d,maxnumber:%d' % (len(lise),maxnumber) )
    #---
    numbs2 = maxnumber - 1
    #---
    for cc in lise:
        #---
        if not num in List:
            List[num] = []
        #---
        if len(List[num]) < maxnumber :
            if not cc in DDone:
                List[num].append( cc )
                DDone.append( cc )
                #---
                if len(List[num]) > numbs2 :
                    num += 1
                #---
    #---
    return List
#---
def ec_de_code( tt , type ):
    fao = tt
    if type == 'encode' :
        #fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif type == 'decode' :
        fao = urllib.parse.unquote(tt)
    return fao
#---