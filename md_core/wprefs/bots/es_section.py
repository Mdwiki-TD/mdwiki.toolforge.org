"""
"""
import re

# ---
from wprefs.helps import print_s
from wprefs.api import get_revisions
from wprefs.bots.es_months import es_months_tab

# ---
n = 0
m_keys = {}
for k, v in es_months_tab.items():
    n += 1
    m_keys[n] = v


def make_date(timestamp):
    # ---
    timestamp = timestamp.split('T')[0]
    # ---
    # 2022-01-24
    maa2 = r'^(?P<y>\d{4})-(?P<m>\d+)-(?P<d>\d+)$'
    # ---
    sas = re.search(maa2, timestamp.strip())
    # ---
    if not sas:
        return timestamp
    d = sas.group('d')
    y = sas.group('y')
    # ---
    m = sas.group('m')
    if m.startswith('0'):
        m = m[1:]
    # ---
    m_ky = int(m)
    m_ky = m_keys.get(m_ky, '').strip()
    # ---
    if m_ky == '':
        return timestamp
    # ---
    return f"{d} de {m_ky} de {y}"


def add_section(text, title):
    # ---
    # if text has section "==Enlaces externos==" return text
    # ---
    if re.search(r'\{\{\s*Traducido ref\s*\|', text, flags=re.I):
        return text
    # ---
    # else add section "==Enlaces externos=="
    # ---
    revisions = get_revisions(title, lang='es')
    # ---
    timestamp = ''  # 2023-02-28T14:01:49Z
    comment = ''  # Creado al traducir la página «[[:en:Special:Redirect/revision/1138582883|User:Mr. Ibrahem/Herpes labialis]]
    # ---
    for r in revisions:
        # user = r.get('user', '')
        # if user == '':  continue
        # ---
        timestamp = r.get('timestamp', '')
        # ---
        comment = r.get('comment', '')
        if comment.lower().find("|user:mr. ibrahem/") != -1:
            break
    # ---
    print_s(f'timestamp = {timestamp}')
    print_s(f'comment = {comment}')
    # ---
    oldid = re.search(r'revision/(\d+)\|', comment)
    if oldid:
        oldid = oldid.group(1)
    else:
        oldid = ''
    # ---
    _title = re.search(r'\|(User:Mr. Ibrahem/[^\]\[]+)\]\]', comment)
    if _title:
        _title = _title.group(1)
    else:
        _title = ''
    # ---
    section = '\n==Enlaces externos==\n{{'
    # {{Traducido ref|en|User:Mr. Ibrahem/Herpes labialis|oldid=1138582883|trad=|fecha=10 Febrero 2023}}
    # ---
    date = make_date(timestamp)
    # ---
    section += f'Traducido ref|en|{_title}|oldid={oldid}|trad=|fecha={date}'
    # ---
    section += '}}'
    # ---
    if _title == '' or date == '':
        return text
    # ---
    gag = re.search(r'(==\s*Enlaces\s*externos\s*==)', text)
    if gag:
        ss = gag.group(1)
        text = text.replace(ss, section)
    else:
        text += section
    # ---
    return text


# ---
if __name__ == '__main__':
    d = '2022-01-24'
    print_s(make_date(d))
