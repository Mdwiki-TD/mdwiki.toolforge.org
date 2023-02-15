#!/usr/bin/python

"""

python3 pwb.py py/backup

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
#---
import pywikibot
#from pywikibot import textlib
#---
import re
import string
import datetime 
#import dateutil.parser
import time
from datetime import datetime, date
dayh = datetime.now().strftime("%Y-%b-%d")
import sys
#---
import urllib
#---
sys_argv = sys.argv or []
#---
import os
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
Malk={}
#---
leader_file = project + '/public_html/Translation_Dashboard/Tables/leader.json'
backup_file = project + '/public_html/Translation_Dashboard/Tables/backup/leader_' + str(dayh) + '.json'
#---
Malk[1]={leader_file:backup_file}
#---
text = ''
#---
with codecs.open(leader_file, "r", encoding="utf-8-sig") as mama:
    text = mama.read()
mama.close()
#---
if text != '' : 
    List_by_user = json.loads( text )
    #---
    # الكتابة إلى الملف
    with open( backup_file , 'w' ) as outfile:
        json.dump( List_by_user , outfile )
    outfile.close()
    #---
    pywikibot.output(" List_by_user:'%s', lenth:%d." % (backup_file , len(List_by_user)) )
#---
csv_file = project + '/public_html/Translation_Dashboard/Tables/leader.csv'
backupcsv_file = project + '/public_html/Translation_Dashboard/Tables/backup/leader_' + str(dayh) + '.csv'
#---
text2 = ''
#---
with codecs.open(csv_file, "r", encoding="utf-8-sig") as mamae:
    text2 = mamae.read()
mamae.close()
#---
if text2 != '' : 
    # الكتابة إلى الملف
    #---
    with codecs.open( backupcsv_file , 'w' , encoding="utf-8") as fff: 
        fff.write( text2 )
    fff.close()
    #---
    pywikibot.output(" csv_file:'%s'." % csv_file )
    pywikibot.output(" backupcsv_file:'%s'." % backupcsv_file )
#---







#---
