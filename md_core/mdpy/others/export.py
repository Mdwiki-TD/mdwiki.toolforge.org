#!/usr/bin/python3
"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
from API import himoBOT3
import codecs
from mdpy import printe

# ---

import sys

# ---

# ---
import requests

Session = requests.Session()
# ---
La_si = {1: 2500000}
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(':')
    # ---
    if arg == "-lasi" or arg == "lasi" and value.isdigit():
        printe.output('<<lightyellow>> change La_si[1] from "%d" to %s' % (La_si[1], value))
        # ---
        La_si[1] = int(value)
        # ---
    # ---
# start of himoBOT3.py file
himoBOT3.log('https://' + 'en.wikipedia.org/w/api.php')
# ---
# himoBOT3.get_Export_xml( title )


def export_en_history(title):
    paramse = {
        'pages': title,
        'title': 'Special:Export',
    }
    # ---
    # if title == 'Pubic lice' : paramse['pages'] =
    # ---
    if 'teest' in sys.argv:
        xmldata = codecs.open('mdwiki/xml/w.xml', "r", encoding="utf-8").read()
    else:
        # ---
        # gg = Session.post( url= "https://" + 'en.wikipedia.org/w/index.php?' , data = paramse )
        # xmldata = gg.text
        # ---
        xmldata = himoBOT3.get_Export_xml(title)
        # ---
    # ---
    printe.output(f'<<lightyellow>> len of history == {len(xmldata)} ')
    # ---
    last = '''
    </page>
</mediawiki>'''
    first = xmldata.split('<revision>')[0]
    # if 'teest' in sys.argv:
    # printe.output( 'first' )
    # printe.output( first )
    # printe.output( 'first' )
    # ---
    # 16282189
    # ---
    texts = {}
    # ---
    revisione = xmldata.replace(first, '').split('</page>')[0].split('</revision>')
    revisions = [x + '</revision>' for x in revisione if x.strip().startswith('<revision>')]
    if 'teest' in sys.argv:
        printe.output(revisions)
    # ---
    printe.output(f"<<lightyellow>> > title:\"{title}\" has {len(xmldata.split('<revision>'))} revisions")
    # ---
    # ---
    title2 = title.replace(':', '-').replace('/', '-')
    num = 1
    Lasa = [1, 2, 3, 4, 5]
    FILE_PATHS = []
    done = False
    # ---
    numbdone = []
    # ---

    # ---
    if len(xmldata) > La_si[1] and 'nosplit' not in sys.argv:
        # while done == False :
        for rev in revisions:
            # ---
            if num not in texts:
                texts[num] = ''
            # ---
            texts[num] += rev
            # ---
            if len(texts[num]) > La_si[1]:
                # ---
                path = 'mdwiki/xml/%s-%d.xml' % (title2, num)
                # tf = tempfile.NamedTemporaryFile()
                # path = tf.name
                # ---
                # oodfo.write( first + texts[num] + last )
                # ---
                with codecs.open(path, "w", encoding="utf-8") as oodfo:
                    oodfo.write(first + texts[num] + last)
                oodfo.close()
                # ---
                FILE_PATHS.append(path)
                # ---
                numbdone.append(num)
                num += 1
            # ---
        # ---
        if num not in numbdone and num in texts and texts[num] != '':
            # ---
            path2 = 'mdwiki/xml/%s-%d.xml' % (title2, num)
            # ---
            with codecs.open(path2, "w", encoding="utf-8") as oodfo:
                oodfo.write(first + texts[num] + last)
            oodfo.close()
            # ---
            FILE_PATHS.append(path2)
            # ---
        # ---
        printe.output(f' split revisions to {len(FILE_PATHS)} files..')
        printe.output(FILE_PATHS)
        return FILE_PATHS
        # ---
    else:
        FILE_PATH = f'mdwiki/xml/{title2}.xml'
        with codecs.open(FILE_PATH, "w", encoding="utf-8") as ooo:
            ooo.write(xmldata)
        ooo.close()
        # ---
        printe.output(' revisions in one file.')
        # ---
        return FILE_PATH


def export(title):
    paramse = {
        # 'pages' : title ,
        # 'title' : 'Special:Export' ,
        'pagelink-depth': '0',
        'followRedirects': True,
        'timeout': 500,
    }
    # ---
    # if title == 'Pubic lice' : paramse['pages'] =
    # ---
    urll = "https://" + 'en.wikipedia.org/w/index.php?title=Special:Export/' + title.replace(' ', '_')
    # urll = "https://" + 'en.wikipedia.org/wiki/Special:Export/' + title.replace(' ','_')
    # ---
    gg = Session.post(url=urll, data=paramse)
    xmldata = gg.text
    # ---
    printe.output(f'<<lightyellow>> len of history == {len(xmldata)} ')
    # ---
    revisions = xmldata.split('</revision>')
    # ---
    printe.output(f"<<lightyellow>> > title:\"{title}\" has {len(xmldata.split('<revision>'))} revisions")
    # ---
    title2 = title.replace(':', '-').replace('/', '-')
    # ---
    FILE_PATH = f'mdwiki/xml/{title2}.xml'
    with codecs.open(FILE_PATH, "w", encoding="utf-8") as ooo:
        ooo.write(xmldata)
    ooo.close()
    # ---
    # printe.output( ' revisions in one file.' )
    # ---
    return FILE_PATH


# ---
if __name__ == "__main__":
    if 'teest' in sys.argv:
        export_en_history('fafa')
    elif len(sys.argv) > 1:
        export(sys.argv[1])
        # export_en_history( sys.argv[1] )
# ---
