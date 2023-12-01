#!/usr/bin/python3
"""
Usage:
# ---
from nccommons import mosab_api
# newpages = mosab_api.Get_All_pages(start="", namespace="0", limit="max", apfilterredir="", limit_all="")
# new = mosab_api.create_Page(text=, title)
# exists = mosab_api.Find_pages_exists_or_not(titles)
# upload = mosab_api.upload_by_url(file_name, text, url, comment='')
# ---
"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
import sys
import time
import urllib
import urllib.parse
import os
import pywikibot
import configparser
import requests

# ---
project = "/data/project/mdwiki/"
# ---
if not os.path.isdir(project):
    project = "I:/mdwiki"
# ---
config = configparser.ConfigParser()
config.read(project + "/confs/nccommons_user.ini")
# ---
username = config["MOSSAB"]["username"].strip()
password = config["MOSSAB"]["password"].strip()
# ---
pywikibot.output(f"username: {username}")
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
Save_all = {1: False}
upload_all = {1: False}
# ---
r1_params = {"format": "json", "action": "query", "meta": "tokens", "type": "login"}
r2_params = {"format": "json", "action": "login", "lgname": username, "lgpassword": password}
# ---
SS = {}
SS["ss"] = requests.Session()
SS["login_not_done"] = True


def py_input(s):
    pywikibot.output(s)
    sa = input()
    # ---
    return sa


def Log_to_wiki(family="nccommons", lang="www"):
    # ---
    user = r2_params["lgname"]
    # ---
    pywikibot.output(f"nccommons.py: log to {lang}.{family}.org user:{user}")
    # ---
    SS["family"] = family
    SS["lang"] = lang
    SS["url"] = "https://" + f"{lang}.{family}.org/w/api.php"
    SS["ss"] = requests.Session()
    # ---
    r11 = SS["ss"].get(SS["url"], params=r1_params)
    r11.raise_for_status()
    # ---
    r2_params["lgtoken"] = r11.json()["query"]["tokens"]["logintoken"]
    r22 = SS["ss"].post(SS["url"], data=r2_params)
    # ---
    if r22.json()["login"]["result"] != "Success":
        pywikibot.output(f"nccommons.py: login failed, reason: {r22.json()['login']['reason']}")
        # sys.exit(1)
        SS["login_not_done"] = True
        return False
    else:
        pywikibot.output("com.py login Success")
    # ---
    SS["r33"] = SS["ss"].get(SS["url"], params={"format": "json", "action": "query", "meta": "tokens"})
    # ---
    SS["r3_token"] = SS["r33"].json()["query"]["tokens"]["csrftoken"]
    SS["login_not_done"] = False


def post_s(params, addtoken=False):
    # ---
    params['format'] = 'json'
    params['utf8'] = 1
    # ---
    if SS["login_not_done"]:
        Log_to_wiki()
    # ---
    if addtoken:
        params['token'] = SS["r3_token"]
    # ---
    jj = {}
    # ---
    url = SS["url"] + '?' + urllib.parse.urlencode(params)
    # ---
    if 'printurl' in sys.argv:
        pywikibot.output(url.replace('&format=json', ''))
    # ---
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
    except Exception as e:
        pywikibot.output(f"nccommons.py: {e}")
        SS["login_not_done"] = True
        return {}
    # ---
    try:
        jj = r4.json()
    except BaseException:
        text = r4.text
        # ---
        if text.find('<!DOCTYPE html>') != -1:
            text = "<!DOCTYPE html>"
        # ---
        pywikibot.output("error r4.json()")
        pywikibot.output(f"r4.text: {text}")
        SS["login_not_done"] = True
    # ---
    return jj


def Get_All_pages(start, namespace="0", limit="max", apfilterredir='', limit_all=0):
    # ---
    pywikibot.output(f'Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}')
    # ---
    numb = 0
    # ---
    params = {
        "action": "query",
        "list": "allpages",
        # "apfrom": start,
        "apnamespace": namespace,
        "aplimit": limit,
        "apfilterredir": "nonredirects",
    }
    # ---
    if apfilterredir in ['redirects', 'all', 'nonredirects']:
        params['apfilterredir'] = apfilterredir
    # ---
    if start != '':
        params['apfrom'] = start
    # ---
    apcontinue = 'x'
    # ---
    Main_table = []
    # ---
    while apcontinue != '':
        # ---
        numb += 1
        # ---
        pywikibot.output(f'Get_All_pages {numb}, apcontinue:{apcontinue}..')
        # ---
        if apcontinue != 'x':
            params['apcontinue'] = apcontinue
        # ---
        json1 = post_s(params)
        # ---
        if not json1 or json1 == {}:
            break
        # ---
        apcontinue = json1.get("continue", {}).get("apcontinue", '')
        # ---
        newp = json1.get("query", {}).get("allpages", [])
        pywikibot.output(f"<<lightpurple>> --- Get_All_pages : find {len(newp)} pages.")
        # ---
        for x in newp:
            if x["title"] not in Main_table:
                Main_table.append(x["title"])
        # ---
        pywikibot.output(f"len of Main_table {len(Main_table)}.")
        # ---
        if limit_all > 0 and len(Main_table) > limit_all:
            apcontinue = ''
            pywikibot.output("<<lightgreen>> limit_all > len(Main_table) ")
            break
        # ---
    # ---
    if numb > 0 and apcontinue == '':
        pywikibot.output("<<lightgreen>> apcontinue == '' ")
    # ---
    pywikibot.output(f"mdwiki_api.py Get_All_pages : find {len(Main_table)} pages.")
    # ---
    return Main_table


def upload_by_url(file_name, text, url, comment=''):
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    params = {'action': 'upload', 'format': 'json', 'filename': file_name, 'url': url, 'comment': comment, 'text': text}
    # ---
    if not upload_all[1] and "ask" in sys.argv:
        if 'nodiff' not in sys.argv:
            pywikibot.output(text)
        sa = py_input(f"<<lightyellow>> nccommons.py: upload file:'{file_name}' ? ([y]es, [N]o):user:{r2_params['lgname']}")
        # ---
        if sa.strip() not in yes_answer:
            pywikibot.output("<<lightred>> wrong answer")
            return False
        # ---
        if sa.strip() == "a":
            pywikibot.output("---------------------------------------------")
            pywikibot.output("nccommons.py upload_by_url save all without asking.")
            pywikibot.output("---------------------------------------------")
            upload_all[1] = True
        # ---
    # ---
    result = post_s(params, addtoken=True)
    # ---
    # {'upload': {'result': 'Success', 'filename': 'Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'imageinfo': {'timestamp': '2023-11-29T20:12:26Z', 'user': 'Mr. Ibrahem', 'userid': 13, 'size': 52289, 'width': 506, 'height': 379, 'parsedcomment': '', 'comment': '', 'html': '', 'canonicaltitle': 'File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg', 'url': 'https://nccommons.org/media/f/fd/Pediculosis_Palpebrarum_%28Dermatology_Atlas_1%29.jpg', 'descriptionurl': 'https://nccommons.org/wiki/File:Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'sha1': '1df195d80a496c6aadcefbc6d7b8adf13caddafc', 'metadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}, {'name': 'MEDIAWIKI_EXIF_VERSION', 'value': 2}], 'commonmetadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}], 'extmetadata': {'DateTime': {'value': '2023-11-29T20:12:26Z', 'source': 'mediawiki-metadata', 'hidden': ''}, 'ObjectName': {'value': 'Pediculosis Palpebrarum (Dermatology Atlas 1)', 'source': 'mediawiki-metadata', 'hidden': ''}}, 'mime': 'image/jpeg', 'mediatype': 'BITMAP', 'bitdepth': 8}}}

    # ---
    upload_result = result.get("upload", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", '')
    # ---
    if success:
        pywikibot.output(f"<<lightgreen>> ** true ..  {SS['family']} : [[File:{file_name}]] ")
        return True
    elif error != {}:
        pywikibot.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        pywikibot.output(error)
    else:
        pywikibot.output(result)
        return False
    # ---
    return False


def create_Page(text, title, summary="create page"):
    pywikibot.output(f" create Page {title}:")
    time_sleep = 0
    # ---
    params = {"action": "edit", "title": title, "text": text, "summary": summary, "notminor": 1, "createonly": 1}
    # ---
    if not Save_all[1] and ("ask" in sys.argv and "save" not in sys.argv):
        if 'nodiff' not in sys.argv:
            pywikibot.output(text)
        sa = py_input(f"<<lightyellow>> nccommons.py: create:\"{title}\" page ? ([y]es, [N]o):user:{r2_params['lgname']}")
        # ---
        if sa.strip() not in yes_answer:
            pywikibot.output("<<lightred>> wrong answer")
            return False
        # ---
        if sa.strip() == "a":
            pywikibot.output("---------------------------------------------")
            pywikibot.output("nccommons.py create_Page save all without asking.")
            pywikibot.output("---------------------------------------------")
            Save_all[1] = True
        # ---
    # ---
    result = post_s(params, addtoken=True)
    # ---
    upload_result = result.get("edit", {})
    # ---
    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", '')
    # ---
    if success:
        pywikibot.output(f"** true ..  {SS['family']} : [[{title}]] ")
        pywikibot.output("Done True... time.sleep(%d) " % time_sleep)
        time.sleep(time_sleep)
        return True
    elif error != {}:
        pywikibot.output(f"<<lightred>> error when create_Page, error_code:{error_code}")
        pywikibot.output(error)
    else:
        pywikibot.output(result)
        return False
    # ---
    # pywikibot.output("end of create_Page def return False title:(%s)" % title)
    # ---
    return False


def Find_pages_exists_or_not(liste):
    # ---
    normalized = {}
    table = {}
    # ---
    done = 0
    # ---
    missing = 0
    exists = 0
    # ---
    for i in range(0, len(liste), 50):
        titles = liste[i : i + 50]
        # ---
        done += len(titles)
        # ---
        pywikibot.output(f"Find_pages_exists_or_not : {done}/{len(liste)}")
        # ---
        params = {
            "action": "query",
            "titles": "|".join(titles),
            # "redirects": 0,
            # "normalize": 1,
        }
        # ---
        json1 = post_s(params)
        # ---
        if not json1 or json1 == {}:
            pywikibot.output("<<lightred>> error when Find_pages_exists_or_not")
            return table
        # ---
        query = json1.get("query", {})
        normalz = query.get("normalized", {})
        # ---
        for red in normalz:
            normalized[red["to"]] = red["from"]
        # ---
        query_pages = query.get("pages", {})
        # ---
        for _, kk in query_pages.items():
            tit = kk.get("title", "")
            if tit != "":
                tit = normalized.get(tit, tit)
                # ---
                table[tit] = True
                # ---
                if "missing" in kk:
                    table[tit] = False
                    missing += 1
                else:
                    exists += 1
    # ---
    pywikibot.output(f"Find_pages_exists_or_not : missing:{missing}, exists: {exists}")
    # ---
    return table


if __name__ == '__main__':
    Get_All_pages('')
