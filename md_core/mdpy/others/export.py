#!/usr/bin/python

"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
from mdpy import printe
import pywikibot
#---
import re
import string
import sys
#---

#---
import requests
Session = requests.Session()
#---
La_si = { 1 : 2500000 }
#---
for arg in sys.argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg == "-lasi" or arg == "lasi" and value.isdigit():
        printe.output( '<<lightyellow>> change La_si[1] from "%d" to %s' % (La_si[1],value) )
        #---
        La_si[1] = int(value)
        #---
    #---
# start of himoBOT3.py file
from API import himoBOT3 
himoBOT3.log('https://' + 'en.wikipedia.org/w/api.php')
#---
# himoBOT3.get_Export_xml( title )
#---
import tempfile
#---
def export_en_history( title ) :
    paramse = { 
        'pages' : title , 
        'title' : 'Special:Export' , 
        }
    #---
    #if title == 'Pubic lice' : paramse['pages'] = 
    #---
    if 'teest' in sys.argv:
        xmldata = codecs.open( 'mdwiki/xml/w.xml'  , "r", encoding="utf-8").read()
    else:
        #---
        #gg = Session.post( url= "https://" + 'en.wikipedia.org/w/index.php?' , data = paramse )
        #xmldata = gg.text
        #---
        xmldata = himoBOT3.get_Export_xml( title )
        #---
    #---
    printe.output( '<<lightyellow>> len of history == %d ' % len(xmldata) )
    #---
    last = '''
    </page>
</mediawiki>'''
    first = xmldata.split('<revision>')[0]
    #if 'teest' in sys.argv: 
        #printe.output( 'first' )
        #printe.output( first )
        #printe.output( 'first' )
    #---
    # 16282189
    #---
    texts = {}
    #---
    revisione = xmldata.replace(first,'').split('</page>')[0].split('</revision>')
    revisions = [ x + '</revision>' for x in revisione if x.strip().startswith('<revision>') ]
    if 'teest' in sys.argv: 
        printe.output( revisions )
    #---
    printe.output( '<<lightyellow>> > title:"%s" has %d revisions' % ( title , len(xmldata.split('<revision>')) ) )
    #---
    #---
    title2 = title.replace(':','-').replace('/','-')
    num = 1
    Lasa  = [1,2,3,4,5] 
    FILE_PATHS = []
    done = False
    #---
    numbdone = []
    #---

    #---
    if len(xmldata) > La_si[1] and not 'nosplit' in sys.argv : 
        #while done == False :
        for rev in revisions :
            #---
            if not num in texts : texts[num] = ''
            #---
            texts[num] += rev
            #---
            if len(texts[num]) > La_si[1] : 
                #---
                path = 'mdwiki/xml/%s-%d.xml' % ( title2 , num )
                #tf = tempfile.NamedTemporaryFile()
                #path = tf.name
                #---
                #oodfo.write( first + texts[num] + last )
                #---
                with codecs.open( path , "w", encoding="utf-8") as oodfo:
                    oodfo.write( first + texts[num] + last )
                oodfo.close()
                #---
                FILE_PATHS.append( path )           
                #---
                numbdone.append(num)
                num += 1
            #---
        #---
        if not num in numbdone and num in texts and texts[num] != '' :
            #---
            path2 = 'mdwiki/xml/%s-%d.xml' % ( title2 , num )
            #---
            with codecs.open( path2 , "w", encoding="utf-8") as oodfo:
                oodfo.write( first + texts[num] + last )
            oodfo.close()
            #---
            FILE_PATHS.append( path2 )           
            #---
        #---
        printe.output( ' split revisions to %d files..' % len(FILE_PATHS) )
        printe.output( FILE_PATHS )
        return FILE_PATHS
        #---
    else:
        FILE_PATH = 'mdwiki/xml/%s.xml' % title2
        with codecs.open( FILE_PATH , "w", encoding="utf-8") as ooo:
            ooo.write( xmldata )
        ooo.close()
        #---
        printe.output( ' revisions in one file.' )
        #---
        return FILE_PATH
#---
def export( title ) :
    paramse = { 
        #'pages' : title , 
        #'title' : 'Special:Export' , 
        'pagelink-depth' : '0' ,
        'followRedirects' : True,
        'timeout' : 500,
        }
    #---
    #if title == 'Pubic lice' : paramse['pages'] = 
    #---
    urll = "https://" + 'en.wikipedia.org/w/index.php?title=Special:Export/' + title.replace(' ','_')
    #urll = "https://" + 'en.wikipedia.org/wiki/Special:Export/' + title.replace(' ','_')
    #---
    gg = Session.post( url = urll , data = paramse )
    xmldata = gg.text
    #---
    printe.output( '<<lightyellow>> len of history == %d ' % len(xmldata) )
    #---
    revisions = xmldata.split('</revision>')
    #---
    printe.output( '<<lightyellow>> > title:"%s" has %d revisions' % ( title , len(xmldata.split('<revision>')) ) )
    #---
    title2 = title.replace(':','-').replace('/','-')
    #---
    FILE_PATH = 'mdwiki/xml/%s.xml' % title2
    with codecs.open( FILE_PATH , "w", encoding="utf-8") as ooo:
        ooo.write( xmldata )
    ooo.close()
    #---
    #printe.output( ' revisions in one file.' )
    #---
    return FILE_PATH
#---
if __name__ == "__main__":
    if 'teest' in sys.argv:
        export_en_history( 'fafa' )
    elif len(sys.argv) > 1 : 
        export( sys.argv[1] )
        #export_en_history( sys.argv[1] )
#---