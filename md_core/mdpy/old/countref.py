#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد الكلمات

python3 pwb.py /data/project/mdwiki/TDpy/countref less100

python3 pwb.py TDpy/countref newpages

"""
#
# (C) Ibrahem Qasim, 2021
#
#
import json
import urllib
import codecs
import re
import os
import string
import time
import sys
#------
sys_argv = sys.argv or []
#------
#======
print_pywikibot = { 1 : False }
try:
	import pywikibot
	print_pywikibot[1] = True
except:
	print_pywikibot[1] = False
#======
#------
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#------
if not os.path.isdir(project): project = '/mdwiki'
#------
#======
#------
import mdapi
# mdapi.submitAPI( params )
#------
all_ref = {}
#------
file_all = project + '/public_html/Translation_Dashboard/Tables/all_refcount.json'
#------
with codecs.open(file_all, "r", encoding="utf-8") as hhg:
	all_ref = json.load(hhg)
hhg.close()
#------
lead_ref = {}
file_lead = project + '/public_html/Translation_Dashboard/Tables/lead_refcount.json'
with codecs.open(file_lead, "r", encoding="utf-8") as haha:
	lead_ref = json.load(haha)
haha.close()
#======
lead_ref = { x : lead_ref[x] for x in lead_ref if lead_ref[x] > 0 }
all_ref = { x : all_ref[x] for x in all_ref if all_ref[x] > 0 }
#======
# list for titles in both all_ref and lead_ref
list_fu = list( set(all_ref.keys()) & set(lead_ref.keys()) )
# remove duplicates from list
list_fu = list(set(list_fu))
list_ma = [ x for x in list_fu if (x in all_ref and x in lead_ref) ]
#======
def count_ref_from_text( text, get_short = False ):
	#------
	short_ref = re.compile( r'<ref\s*name\s*\=\s*(?P<name>[^>]*)\s*\/\s*>', re.IGNORECASE | re.DOTALL)
	#------
	ref_list = []
	#------
	# count = 0
	#------
	if get_short:
		for m in short_ref.finditer(text):
			name = m.group('name')
			if name.strip() != '' : 
				if not name.strip() in ref_list : ref_list.append(name.strip())
	#------	  
	# refreg = re.compile(r'(<ref[^>]*>[^<>]+</ref>|<ref[^>]*\/\s*>)')
	refreg = re.compile( r'(?i)<ref(?P<name>[^>/]*)>(?P<content>.*?)</ref>', re.IGNORECASE | re.DOTALL)
	#------	  
	for m in refreg.finditer(text):
		# content = m.group('content')
		# if content.strip() != '' : if not content.strip() in ref_list : ref_list.append(content.strip())
		#------
		name	= m.group('name')
		content = m.group('content')
		#------
		if name.strip() != '' :
			if not name.strip() in ref_list : ref_list.append(name.strip())
		elif content.strip() != '' :
			if not content.strip() in ref_list : ref_list.append(content.strip())
			# count += 1
	#------	  
	count = len(ref_list)
	#------	  
	return count
#======
import ref
# ref.fix_ref( first, alltext )
#======
def count_refs( title ):
	#------
	text = mdapi.GetPageText(title)
	#------
	text2 = ref.fix_ref( text, text )
	#------
	all_c = count_ref_from_text( text2 )
	all_ref[title] = all_c
	#------
	leadtext = text2.split('==')[0]
	lead_c = count_ref_from_text( leadtext, get_short = True )
	#------
	lead_ref[title] = lead_c
	#------
	pywikibot.output('<<lightgreen>> all:%d \t lead:%d' % ( all_c, lead_c ) )
#====== 
def logaa(file,table):
	with open( file, 'w') as outfile:
		json.dump( table, outfile, sort_keys = True, indent=4)
	outfile.close()
	#------
	pywikibot.output('<<lightgreen>> %d lines to %s' % ( len(table), file ) )
#======
vaild_links = { 1 : [] }
#======
import catdepth2
if not 'test1' in sys_argv:
	tabe = catdepth2.subcatquery2( 'RTT', depth = '1', ns = '0' )
	vaild_links[1] = tabe['list']
#======
if 'newpages' in sys_argv:
	newlist = [ x for x in vaild_links[1] if ( not x in list_ma )]
	vaild_links[1] = newlist
#======
def mmain():
	#======
	numb = 0
	#======
	limit = 10000
	if 'limit100' in sys.argv : limit = 100
	#======
	# python pwb.py mdwiki/public_html/Translation_Dashboard/countref test1 local -title:Testosterone_\(medication\)
	# python3 pwb.py /data/project/mdwiki/TDpy/countref test1 -title:Testosterone_\(medication\)
	#======
	for arg in sys.argv:
		arg, sep, value = arg.partition(':')
		#------
		if arg == "-title" : vaild_links[1].append( value.replace('_',' ') )
		#------
	#======
	for x in vaild_links[1]:
		#------
		numb += 1
		#------
		if numb >= limit :	break
		#------
		pywikibot.output(' p %d from %d: for %s:' % (numb, len(vaild_links[1]), x) )
		#------
		count_refs(x)
		#------
		if numb == 10 or str(numb).endswith('00'):
			logaa(file_lead,lead_ref)
			logaa(file_all,all_ref)
		#------
	#======
	logaa(file_lead,lead_ref)
	logaa(file_all,all_ref)
#======
if __name__ == '__main__':
	mmain()
#======
