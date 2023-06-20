'''

python3 uuu.py owner nodirs path:core only:py
python3 uuu.py owner nodirs path:public_html only:php

python3 uuu.py owner nodirs path:public_html

python3 uuu.py fixpy nodirs path:new/master_18-11-22
python3 uuu.py fixpy nodirs path:master

python3 uuu.py a owner nodirs only:php

python3 core/uuu.py onlypy a owner

'''
import sys
sys.dont_write_bytecode = True
import os
#------------------
paths_to_add = [
    '/data/project/mdwiki/md_core/'
    ]
#------------------
for u_path in paths_to_add:
    if os.path.exists(u_path):
        sys.path.append(os.path.abspath(u_path))
    else:
        print(f"u_path:{u_path} not exists")
#------------------
print(__file__)
print(__file__)
#------------------
import diffe
import time
import re
import shutil
import stat
from pathlib import Path
'''
stat.S_IRWXU : Read, write, and execute by owner
stat.S_IRWXG : Read, write, and execute by group
stat.S_IRWXO : Read, write, and execute by others.
stat.S_IROTH : Read by others
stat.S_IWOTH : Write by others
stat.S_IXOTH : Execute by others
'''
#---
# list of all compression extensions
false_ex = [
    '.bz2', '.gz', '.xz', '.lzma', '.lz', '.zst', '.br', '.7z', '.rar', '.zip', '.tar', '.tar.gz', 
    '.tar.bz2', '.tar.xz', '.tar.lzma', '.tar.lz', '.tar.zst', '.tar.7z', '.tar.rar', '.tar.zip', '.tgz'
    ]
#---
q_path = ""
only = ""
for arg in sys.argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg == 'only':
        only = value.strip()
    #---
    if arg == "path":
        q_path = value.strip()
#---
ASK_all = { 1 : True}
#---
g_path = os.getcwd()
#---
if q_path == "":
    path = '/data/project/himo/core1'
    #---
    if 'yemen' in sys.argv: path = "i:\\core\\core-yemen"
    #---
    if 'local' in sys.argv: path = "i:\\core\\master"
    #---
    if "a" in sys.argv: path = g_path
else:
    path = q_path
#---
diffe.output( f" <<lightblue>> work on path : {path}\n"  * 3)
#---
tools = [ "himo", "sanaa", "suha", "yemen", "lyan", "mdwiki" ]
uow = "/%s"
mytool = 'tools.himo'
#---
print(f'g_path: {g_path}')
#---
for tool in tools:
    if g_path.find( uow % tool ) != -1 :
        mytool = 'tools.%s' % tool 
        break
#---
diffe.output( f"<<lightgreen>> mytool : {mytool}\n"  * 3)
diffe.output( "use 'fixpy' or 'unlink' or 'change' or 'owner' in command line\n" * 2 )
#---
def write(oldtext,text,filepath):
    #---
    if oldtext == text:
        path2 = filepath.split('/')[-1]
        diffe.output( 'No change in %s' % path2 )
        return ''
    #---
    diffe.showDiff(oldtext,text)
    #---
    diffe.output(filepath.replace('/','\\'))
    #---
    ask = 'y'
    if ASK_all[1] :
        diffe.output( '<<lightgreen>> Save?' )
        ask = input("(y/n)")
        if ask == 'a' :
            ASK_all[1] = False
    #---
    if ask == 'y' or ask == '' or ask == 'a':
        # write without errors
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
                diffe.output("replaced")
                #---
                diffe.output('file: %s done.' % filepath)
                #---
                #time.sleep(1)
                return ''
        except Exception as e:
            diffe.output( '<<lightred>> Error: %s' % e )
            #time.sleep(1)
            return text
    else:
        diffe.output("not replaced")
#---
def fix_py(filepath):
    text = open(filepath, 'r', encoding='utf-8').read()
    #---
    oldtext = text
    #---
    # jjson
    if text.lower().find('jjson') != -1 :
        text = re.sub(r'import json as JJson' , '' , text , flags=re.IGNORECASE )
        if text.lower().find('jjson') == -1 : 
            write(oldtext,text,filepath)
            oldtext = text
    #---
    # from pywikibot import pagegenerators
    if text.lower().find('from pywikibot import pagegenerators') != -1 :
        text = re.sub(r'\n#*\s*from pywikibot import pagegenerators\n' , '\n' , text , flags=re.IGNORECASE )
        #---
        text = re.sub(r'#\s*([\w\d\-_])+\s*\=\s*pagegenerators\..*?\n' , '\n' , text , flags=re.IGNORECASE )
        #---
        if text.lower().find('pagegenerators') == -1 :   
            write(oldtext,text,filepath)
            oldtext = text
    #---
    # from\s*pywikibot\.bot\s*import\s*\(\s*SingleSiteBot\s*,\s*ExistingPageBot\s*,\s*NoRedirectPageBot\s*,\s*AutomaticTWSummaryBot\s*\)
    # from pywikibot.bot import (SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
    #---
    text = re.sub(r'from\s*pywikibot\.bot\s*import\s*\(\s*SingleSiteBot\s*,\s*ExistingPageBot\s*,\s*NoRedirectPageBot\s*,\s*AutomaticTWSummaryBot\s*\)' , '\n' , text , flags=re.IGNORECASE )
    #---
    test = re.sub(r'(SingleSiteBot|ExistingPageBot|NoRedirectPageBot|AutomaticTWSummaryBot)' , '\n', text, flags=re.IGNORECASE )
    #---
    if test == text : 
        write(oldtext,text,filepath)
        oldtext = text
    #---

    #---
    # from pywikibot.tools import issue_deprecation_warning
    if text.lower().find('issue_deprecation_warning') != -1 :
        text = re.sub(r'\n#*\s*from pywikibot\.tools\s*import\s*issue_deprecation_warning\s*\n' , '\n' , text , flags=re.IGNORECASE )
        #---
        if text.lower().find('pagegenerators') == -1 :   
            write(oldtext,text,filepath)
            oldtext = text
    #---
    # from __future__ import absolute_import, unicode_literals
    if text.lower().find('absolute_import') != -1 or text.lower().find('unicode_literals') != -1 :
        text = re.sub(r'\n#*\s*from\s+__future__\s+import\s+absolute_import\s*\,\s*unicode_literals\s*\n' , '\n' , text , flags=re.IGNORECASE )
        #---
        if text.lower().find('unicode_literals') == -1 and text.lower().find('unicode_literals') == -1 : 
            write(oldtext,text,filepath)
    #---

#---
def fix_py2(filepath):
    oldtext = open(filepath, 'r', encoding='utf-8').read()
    #---
    text = oldtext
    #---
    # faf = [\w\d\'\"]+
    # faf = .*?
    #---
    # if text.find('page_putWithAsk') != -1 or text.find('page_put') != -1 :
    if 'uuxx' in sys.argv:
        text = re.sub(
            r'\#\s*(arAPI2*)\.(page_putWithAsk|page_put)\(.*?\)', 
            '',
            text, 
            flags=re.IGNORECASE
        )
        #---
        if text != oldtext:
            diffe.output("file:" + filepath)
            write(oldtext, text, filepath)
            oldtext = text
        #---
        return ''
    #---
    # if text.find('page_putWithAsk') != -1 or text.find('page_put') != -1 :
    text = re.sub(
        r'(arAPI2*)\.(page_putWithAsk|page_put)\(\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*(.*?)\s*,\s*(.*?)\s*\)', 
        '\g<1>.page_put(oldtext=\g<3>, newtext=\g<4>, summary=\g<5>, title=\g<6>, \g<8>)',
        text, 
        flags=re.IGNORECASE
    )
    #---
    text = re.sub(
        r'(arAPI2*)\.(page_putWithAsk|page_put)\(\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*(.*?)\s*\)', 
        '\g<1>.page_put(oldtext=\g<3>, newtext=\g<4>, summary=\g<5>, title=\g<6>)',
        text, 
        flags=re.IGNORECASE
    )
    #---
    text = re.sub(
        r'(arAPI2*)\.(page_putWithAsk|page_put)\(\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*\)', 
        '\g<1>.page_put(oldtext="", newtext=\g<3>, summary=\g<4>, title=\g<5>)',
        text, 
        flags=re.IGNORECASE
    )
    #---
    text = re.sub(
        r'(arAPI2*)\.(page_putWithAsk|page_put)\(\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*([^,\=]+?)\s*,\s*(.*?)\s*\)', 
        '\g<1>.page_put(oldtext="", newtext=\g<3>, summary=\g<4>, title=\g<5>, \g<6>)',
        text, 
        flags=re.IGNORECASE
    )
    #---
    if text != oldtext:
        diffe.output("file:" + filepath)
        text = text.replace(', time_sleep = "", family="", minor="")', ')')
        write(oldtext, text, filepath)
#---
def fix_py3(filepath):
    #---
    text = open(filepath, 'r', encoding='utf-8').read()
    #---
    print('fix_py3')
    #---
    oldtext = text
    #---
    '''
        pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
        pywikibot.output(f'<<lightred>> {__file__} Exception:' + str(e) )
        pywikibot.output( 'CRITICAL:' )
    '''
    #---
    # jjson
    if 'CRITICAL' in sys.argv and text.find('CRITICAL') != -1 :
        #---
        text = re.sub(r"pywikibot\.output\(\s*(f'\s*<<\w+>>|f'\s*)(\s*\{__file__\}\s*Exception:\s*'\s*\+\s*str\(\w+\))\s*\)", 
            "warn(\g<1>\g<2>, UserWarning)", text , flags=re.IGNORECASE )
        #---
        if text.find('UserWarning') != -1 :
            if text.find('from warnings import warn') == -1 :
                text = text.replace( "import pywikibot", "from warnings import warn\nimport pywikibot", 1)
                if text.find('from warnings import warn') == -1 :
                    text = "from warnings import warn\n" + text

            write(oldtext,text,filepath)
            oldtext = text
    #---
    # pywikibot.showDiff
    if 'diff' in sys.argv:
        if text.find('pywikibot.showDiff') != -1 :
            #---
            text = text.replace( "pywikibot.showDiff(", "printe.showDiff(")
            #---
            if text.find('printe.') != -1 :
                if text.find('from API import printe') == -1 :
                    text = text.replace( "import pywikibot", "from API import printe\nimport pywikibot", 1)
                    if text.find('from API import printe') == -1 :
                        text = "from API import printe\n" + text
                #---
                write(oldtext,text,filepath)
                oldtext = text
    #---
    if text.find('warn(') != -1:
        text = text.replace( "warn(f'<<lightred>> Exception: ConnectionError', UserWarning)", "warn('Exception: ConnectionError', UserWarning)")
        text = text.replace( "warn(f'<<lightred>> Exception:'", "warn('Exception:'")
        #---
        if text != oldtext:
            write(oldtext,text,filepath)
            oldtext = text
    #---
    # warn(f'<<lightred>> Exception: ConnectionError', UserWarning)
#---
if "fixpy" in sys.argv:
    for (root,dirs,files) in os.walk(path, topdown=True):
        if root.find('__pycache__') > -1: continue
        if root.find('.git') > -1: continue
        if root.find('/.') > -1: continue
        #---
        for f in files:
            # filepath = root + '/' + f
            filepath = os.path.join(root, f)
            #---
            if f == "uuu.py": continue
            #---
            filepath2 = filepath.replace('\\','/')
            #---
            if filepath2.find('wikidataintegrator') != -1 : continue
            if filepath2.find('/venv/') != -1 : continue
            if filepath2.find('/old/') != -1 : continue
            if filepath2.find('/scripts/') != -1 : continue
            if filepath2.find('/pywikibot/') != -1 : continue
            if filepath2.find('/pkg_resources/') != -1 : continue
            if filepath2.find('/setuptools/') != -1 : continue
            if filepath2.find('/tests/') != -1 : continue
            #---
            if filepath.endswith('.py'):
                diffe.output("file:" + filepath)
                #fix_py(filepath)
                fix_py2(filepath)
                fix_py3(filepath)
#---
if "unlink" in sys.argv:
    for (root,dirs,files) in os.walk(path, topdown=True):
        if root.find('__pycache__') > -1: continue
        if root.find("/.git/") != -1 : continue 
        if root.find("/.") != -1 : continue 
        #---
        # delete symbolic links
        for d in dirs:
            # dirpath = root + '/' + d
            dirpath = os.path.join(root, d)
            if dirpath.find('__pycache__') > -1: continue
            if os.path.islink(dirpath):
                diffe.output("unlink: " + dirpath)
                # ask
                ask = 'y'
                if ASK_all[1] :
                    diffe.output( '<<lightgreen>> Unlink?' )
                    ask = input("(y/n)")
                    if ask == 'a' :
                        ASK_all[1] = False
                #---
                if ask == 'y' or ask == '' or ask == 'a':
                    # unlink without errors
                    try:
                        os.unlink(dirpath)
                        diffe.output("unlinked")
                        #---
                        diffe.output('dir: %s done.' % dirpath)
                        #---
                    except Exception as e:
                        diffe.output( '<<lightred>> Error: %s' % e )
                        #time.sleep(1)
#---
change_per_error = []
#---
if "change" in sys.argv:
    #---
    def set_chmod(path):
        #---
        if path.find("/.git/") != -1 : return 
        if path.find("/.") != -1 : return 
        diffe.output("chmod: " + path)
        #---
        # get the dir permissions
        mode = os.stat(path)
        #diffe.output(f"mode : {mode}")
        #---
        uif = stat.S_IRWXU | stat.S_IRWXG
        #---
        if path.find('/public_html/') != -1 :
            uif = stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH
        diffe.output(f"uif : {uif}")
        #---
        if str(oct(uif)).endswith("770") and str(oct(mode.st_mode)).endswith("770"):
            diffe.output("already ok")
            return
        #---
        diffe.output("<<yellow>> mode.st_mode: %s" % mode.st_mode)
        diffe.output("<<yellow>> oct(mode.st_mode): %s" % oct(mode.st_mode)) 
        diffe.output("<<yellow>> oct(uif): %s" % oct(uif)) 
        #---
        # ask
        ask = 'y' 
        if ASK_all[1] :
            diffe.output( '<<lightgreen>> Chmod?' )
            ask = input("(y/n)")
            if ask == 'a' : ASK_all[1] = False
        #---
        if ask == 'y' or ask == '' or ask == 'a':
            # chmod without errors
            try:
                # os.chmod(path, 0o777)
                os.chmod(path, uif )
                diffe.output("<<lightgreen>> chmoded to : %s" % str(uif) )
                diffe.output('path: %s done.' % path)
                #---
            except Exception as e:
                change_per_error.append(path)
                diffe.output( '<<lightred>> Error: %s' % e )
                #time.sleep(1)
    #---
    if not "nodirs" in sys.argv:
        # set all files and dirs permissions to 770 with shutil
        for (root,dirs,files) in os.walk(path, topdown=True):
            #---
            if root.find('__pycache__') > -1: continue
            if root.find('.git') > -1: continue
            if root.find('/.') > -1: continue
            #---
            for d in dirs:
                # dirpath = root + '/' + d
                dirpath = os.path.join(root, d)
                if dirpath.find('__pycache__') > -1: continue
                if os.path.islink(dirpath): continue
                set_chmod(dirpath)
    #---
    ASK_all[1] = True
    #---
    if not "nofiles" in sys.argv:
        for (root,dirs,files) in os.walk(path, topdown=True):
            #---
            if root.find('__pycache__') > -1: continue
            if root.find('.git') > -1: continue
            if root.find('/.') > -1: continue
            #---
            for f in files:
                #filepath = root + '/' + f
                filepath = os.path.join(root, f)
                if f.endswith('.pyc'): continue
                #---
                #---
                # if any(ext in filepath for ext in false_ex): continue
                if filepath.endswith(tuple(false_ex)): continue
                #---
                if os.path.islink(filepath): continue
                #---
                if "nopy" in sys.argv and f.endswith('.py'): continue
                if "onlypy" in sys.argv and not f.endswith('.py'): continue
                if only != "" and not f.endswith('.%s' % only ): continue
                #---
                if not filepath.startswith(path): 
                    diffe.output( '<<lightred>> filepath not in main path: %s' % filepath )
                    continue
                #---
                if f.startswith(".") : continue
                #---
                set_chmod(filepath)
            #---
    #---
    for path in change_per_error:
        diffe.output("<<lightred>> %s set_chmod Error." % path)
#---
can_set_owner = { 1 : True, "not done" : True }
change_owner_error = []
#---
if "owner" in sys.argv:
    #---
    ASK_all["owner"] = True
    #---
    def recreated(path2):
        # get the file content
        if path2.find("/.git/") != -1 : return 
        if path2.find('__pycache__') > -1: return
        if path2.find("/.") != -1 : return 
        diffe.output("<<lightgreen>> ===========================.")
        #---
        # get file size
        size = os.path.getsize(path2)
        diffe.output("<<lightgreen>> size: %s" % size)
        # return pass if size > 70 mg
        maxsize = 70*1024*1024
        if size > maxsize : return
        #---
        try:
            text = open(path2, 'r').read()
            #---
            # change the file name
            newpath = path2 + '.old'
            os.rename(path2, newpath)
            #---
            # recreate the file
            open(path2, 'w').write(text)
            #---
            diffe.output("<<lightgreen>> %s recreated." % path2)
            #---
            if path2.find('/public_html/') == -1 :
                os.chmod(path2, stat.S_IRWXU | stat.S_IRWXG )
                diffe.output("<<lightgreen>> chmoded to : stat.S_IRWXU | stat.S_IRWXG")
            else:
                os.chmod(path2, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH )
                diffe.output("<<lightgreen>> chmoded to : stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH")
            #---
            # remove old file
            os.remove(newpath)
            diffe.output("<<lightgreen>> oldfile removed.")
            diffe.output("<<lightgreen>> ===========================.")
        except Exception as e:
            diffe.output( '<<lightred>> recreated Error: %s' % e )
            #time.sleep(1)
    #---
    def set_owner(path2):
        #---
        if path2.find("/.git/") != -1 : return
        if path2.find('__pycache__') != -1: return
        if path2.find("/.") != -1 : return
        #---
        diffe.output("set_owner: " + path2)
        # get the file owner
        uid = os.stat(path2).st_uid
        #diffe.output(f"uid : {uid}")
        #---
        if can_set_owner["not done"] :
            can_set_owner["not done"] = False
            try:
                pathe = Path(path2)
                owner = pathe.owner()
                group = pathe.group()
            except Exception as e:
                diffe.output( '<<lightred>> Error: %s' % e )
                can_set_owner[1] = False
                return False
        #---
        pathe = Path(path2)
        owner = pathe.owner()
        group = pathe.group()
        #---
        if owner != mytool or group != mytool:
            print("----------------------------------------------------")
            print(f"path2: {path2} \n owned by {owner}:{group}")
            #diffe.output(" change owners to %s" mytool)
            #---
            ask = 'y'
            if ASK_all["owner"]:
                diffe.output( '<<lightgreen>> Change owners to %s?' % mytool )
                ask = input("(y/n)")
                if ask == 'a' :
                    ASK_all["owner"] = False
            #---
            if ask == 'y' or ask == '' or ask == 'a':
                # change owner without errors
                erroe = False
                try:
                    # os.chown(path2, uid, group)
                    shutil.chown(path2, mytool, mytool)
                    diffe.output("changed")
                    diffe.output('dir: %s done.' % path2)
                    #---
                except Exception as e:
                    change_owner_error.append(path2)
                    diffe.output( '<<lightred>> Error: %s' % e )
                    erroe = True
                #---
                if erroe and os.path.isfile(path2):
                    recreated(path2)
    #---
    if not "nodirs" in sys.argv and not "onlypy" in sys.argv:
        # set all files and dirs permissions to 770 with shutil
        for (root,dirs,files) in os.walk(path, topdown=True):
            #---
            if root.find('__pycache__') > -1: continue
            if root.find('.git') > -1: continue
            if root.find('/.') > -1: continue
            #---
            if not can_set_owner[1]: break
            #---
            for d in dirs:
                # dirpath = root + '/' + d
                dirpath = os.path.join(root, d)
                if os.path.islink(dirpath): continue
                set_owner(dirpath)
                if not can_set_owner[1]: break
    #---
    ASK_all["owner"] = True
    #---
    if not "nofiles" in sys.argv:
        for (root,dirs,files) in os.walk(path, topdown=True):
            #---
            if root.find('__pycache__') > -1: continue
            if root.find('.git') > -1: continue
            if root.find('/.') > -1: continue
            #---
            if not can_set_owner[1]: break
            #---
            for f in files:
                # filepath = root + '/' + f
                filepath = os.path.join(root, f)
                #---
                if f.endswith('.pyc'): continue
                #---
                # if any(ext in filepath for ext in false_ex): continue
                if filepath.endswith(tuple(false_ex)): continue
                #---
                if os.path.islink(filepath): continue
                #---
                if "nopy" in sys.argv and f.endswith('.py'): continue
                if "onlypy" in sys.argv and not f.endswith('.py'): continue
                if only != "" and not f.endswith('.%s' % only ): continue
                #---
                if f.startswith(".") : continue
                #---
                if not filepath.startswith(path): 
                    diffe.output( '<<lightred>> filepath not in main path: %s' % filepath )
                    continue
                #---
                set_owner(filepath)
                if not can_set_owner[1]: break
    #---
    for path in change_owner_error:
        diffe.output("<<lightred>> %s set_owner Error." % path)
#---
#---