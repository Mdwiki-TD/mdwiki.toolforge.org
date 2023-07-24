#!/usr/bin/python

"""

python ./nash/mdpy/getall2.py

"""
import os
import time
import re
import sys
import chardet
#---
def printe(color, text):
	color_table = {
		'red': "\033[91m%s\033[00m",
		'green': "\033[92m%s\033[00m",
		'yellow': "\033[93m%s\033[00m",
		'blue': "\033[94m%s\033[00m",
		'purple': "\033[95m%s\033[00m",
		'cyan': "\033[96m%s\033[00m",
		'white': "\033[97m%s\033[00m",
		'black': "\033[98m%s\033[00m",
		'grey': "\033[99m%s\033[00m",
		'lightred': "\033[101m%s\033[00m",
		'lightgreen': "\033[102m%s\033[00m",
		'lightyellow': "\033[103m%s\033[00m",
		'lightblue': "\033[104m%s\033[00m",
		'lightpurple': "\033[105m%s\033[00m",
		'lightcyan': "\033[106m%s\033[00m",
		'lightwhite': "\033[107m%s\033[00m",
		'lightblack': "\033[108m%s\033[00m",
		'lightgrey': "\033[109m%s\033[00m",
		'bold': "\033[1m%s\033[00m",
		'underline': "\033[4m%s\033[00m",
		'invert': "\033[7m%s\033[00m",
		'blink': "\033[5m%s\033[00m",
        'aqua': "\033[106m%s\033[00m",
        'lightaqua': "\033[107m%s\033[00m",
        'lightgray': "\033[107m%s\033[00m",
        'gray': "\033[100m%s\033[00m",		
	}
	#---
	if color in color_table:
		print(color_table[color] % text)
	else:
		print(text)
#---

def get_text(file_path):
	#---
	# find out what encoding the file is
	#---
	#---
	# find out what encoding the file is
	#---
	enc = ''
	#---
	with open(file_path, 'rb') as f:
		raw = f.read()
		enc = chardet.detect(raw)['encoding']
		f.close()
	#---
	if enc and enc.startswith("ISO-8859"):	enc = "windows-1256"
	#---
	text = ''
	#---
	try:
		text = open(file_path, encoding=enc).read()
	except UnicodeDecodeError:
		printe("red", "UnicodeDecodeError: %s" % file_path.replace("/", "\\"))
		try:
			enc = "utf-8"
			text = open(file_path, encoding=enc).read()
		except Exception as e:
			printe("red", "Exception: %s" % file_path.replace("/", "\\"))
			print(e)
		#print(we)
	except UnicodeError:
		printe("red", "UnicodeError: %s" % file_path.replace("/", "\\"))
	except Exception as e:
		printe("red", "Exception: %s" % file_path.replace("/", "\\"))
		print(e)
	#---
	#if text == '' :return sad
	#---
	return text, enc
#---
#---
shared_paths = {}
#---
drivepath = "I:\\mdwiki\\mdpy"
#---
for pyfile in os.listdir(drivepath):
    #---
    printe("blue", pyfile)
    #---
    pyfilepath = drivepath + '/' + pyfile
    #---
    if os.path.isfile(pyfilepath) and pyfile.endswith('.py'):
        #printe( "red" , "%s found in: %s" % (pyfile,floder) )
        #---
        text, enc = get_text(pyfilepath)
        #---
        # match all defs
        rec = re.compile(r'def\s+([^\(\)]+)\s*\(.*?\)\s*\:')
        for def_ in rec.finditer( text ):
            #---
            Def = def_.group()
            name = def_.group(1)
            printe( "green" , f"{Def} found in: {pyfile}" )
            printe( "green" , f"name:{name} " )
            #---
            #shared_paths
            if not name in shared_paths:shared_paths[name] = 0
            shared_paths[name] += 1
        #---
#---
printe( "yellow" , f"lenth of shared_paths: {len(shared_paths)}" )
#---

sort = sorted(shared_paths.items(), key=lambda x: x[1], reverse=True)
#---
for key, value in sort:
    if value > 1:
        printe( "yellow" , "%s: %d" % (key,value) )
#---
