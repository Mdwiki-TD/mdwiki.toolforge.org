'''

from priorviews.bots import sections_text #make_text(section, links)

python3 core8/pwb.py priorviews/sections_text

'''
from priorviews.bots import helps  # views_url(title, lang, view)
from priorviews.lists import views
import sys
from pathlib import Path

# ---
Dir = Path(__file__).parent
# ---
text_v = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">
{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! #
! style="position: sticky;top: 0;left: 0;" | Title
! Views
!'''
# ---
# ---
# views.views_by_mdtitle_langs
# views.count_views_by_mdtitle
# views.count_views_by_lang
# views.views_by_lang
# ---
section_langs_views = {}
all_section_views = 0


def make_lang_text(mdtitle, langlinks, langs_keys_sorted, section):
    if section not in section_langs_views:
        section_langs_views[section] = {}
    """
    Returns a formatted string containing view counts for all available languages.
    """
    lang_text = ''
    u = 0

    if 'test1' in sys.argv:
        print('mdtitle:')
        print(mdtitle)
        print('langlinks:')
        print(langlinks)

    # Loop through all available languages in the sorted order
    for l in langs_keys_sorted:
        u += 1
        if l not in section_langs_views[section]:
            section_langs_views[section][l] = 0
        view = ''

        # Get the title of the current language, or an empty string if not found
        title = langlinks.get(l, '')
        if title != '':
            # Get the view count for the current language and title, or 0 if not found
            view = views.views_by_lang.get(l, {}).get(title.lower(), 0)
            section_langs_views[section][l] += view
            # ---
            view = helps.views_url(title, l, view)
            # ---
            '''
            params = {
                'project': f"{l}.wikipedia.org",
                'platform': 'all-access',
                'agent': 'all-agents',
                'start': "2015-07-01",
                'redirects': '0',
                'pages': title
            }
            d_end   = datetime.datetime.utcnow() - timedelta(days = 1)
            d_end   = d_end.strftime('%Y-%m-%d')
            params['end'] = d_end
            params = urlencode(params)
            url_views = f"https://pageviews.wmcloud.org/?{params}"

            view = f'[{url_views} {view:,}]'
            '''
            # ---
            if 'test1' in sys.argv:
                view = f'[[:w:{l}:{title}|a]] {view}'
        # Create a formatted string with the view count for the current language and title
        tt = f' || {view}'

        # If this is the first language being processed, do not prepend the formatted string with ' || '
        if u == 1:
            tt = f'{view}'

        # Append the formatted string to the overall formatted string
        lang_text += tt

    # Return the overall formatted string containing view counts for all available languages
    return lang_text


def make_text(section, links):
    """
    Generate formatted text from given section and links.
    """
    global all_section_views, section_langs_views
    section_langs_views[section] = {}
    # Create an empty list to store language keys.
    langs_keys = []

    # Loop through the dictionary of links and add the keys to langs_keys.
    for mdtitle, langs in links.items():
        langs_keys.extend(langs.keys())

    # Strip whitespace from keys in langs_keys and remove any empty strings.
    langs_keys = [x.strip() for x in langs_keys if x.strip() != '']

    # Remove duplicates from langs_keys and sort the list.
    langs_keys = sorted(set(langs_keys))

    text = text_v

    # Add the language keys to text separated by '!!'.
    # text += " " + " !! ".join(langs_keys)
    def format_x(x):
        if len(x) < 4:
            return x
        # ---
        x2 = x.replace('-', '')
        x2 = x2[:3]
        # ---
        return "{{abbr|" + f"{x2}|{x}" + "}}"

    def fo_n(x):
        return f'{x:,}'

    langs_keys_text = " !! ".join([format_x(x) for x in langs_keys])
    text += f" {langs_keys_text}"

    n = 0

    if 'test' in sys.argv:
        print(langs_keys)

    section_views = 0

    # Loop through the dictionary of links.
    for mdtitle, langlinks in links.items():
        n += 1

        # Call make_lang_text to create the language text for this row.
        lang_text = make_lang_text(mdtitle, langlinks, langs_keys, section)

        mdtitle_views = views.count_views_by_mdtitle.get(mdtitle, 0)

        section_views += mdtitle_views
        # Create the table row with the language text and the row number.
        l_text = '\n|-\n'
        l_text += f'! {n}\n'
        l_text += f'! style="position: sticky;left: 0;" | [[{mdtitle}]]\n'
        l_text += f'! {mdtitle_views:,}\n'
        l_text += f'| {lang_text}'

        # Add the row to the text variable.
        text += l_text

    all_section_views += section_views
    # total views by language
    text += '\n|-\n'
    text += f'! !! style="position: sticky;left: 0;colspan:2;" | Total views !! {section_views:,} \n'
    text += '! ' + " !! ".join([str(fo_n(section_langs_views[section].get(l, 0))) for l in langs_keys])
    # text += '! ' + " !! ".join([ str(views.count_views_by_lang.get(l, 0)) for l in langs_keys ])

    # Add the closing table tag and div tag to the text variable.
    text += '\n|}\n</div>'

    # Create the final formatted text with the section header, number of links, and the table.
    faf = f'* views: {section_views:,}\n'
    faf += f'=={section} ({len(links)})==\n{text}'

    # Return the final formatted text.
    return faf


# ---
if __name__ == '__main__':
    lngs = [
        "af",
        "ar",
        "ast",
        "ay",
        "az",
        "be",
        "be-tarask",
        "bg",
        "bn",
        "bs",
        "ca",
        "ckb",
        "cs",
        "cy",
        "da",
        "de",
        "el",
        "eo",
        "es",
        "et",
        "eu",
        "fa",
        "fi",
        "fr",
        "gcr",
        "gl",
        "ha",
        "he",
        "hi",
        "hr",
        "hu",
        "hy",
        "id",
        "is",
        "it",
        "ja",
        "jv",
        "ka",
        "kk",
        "kn",
        "ko",
        "ky",
        "la",
        "lt",
        "lv",
        "mk",
        "ml",
        "mr",
        "ms",
        "my",
        "ne",
        "nl",
        "nn",
        "no",
        "or",
        "pa",
        "pl",
        "pt",
        "qu",
        "ro",
        "ru",
        "sah",
        "sh",
        "si",
        "sk",
        "sl",
        "sq",
        "sr",
        "sv",
        "sw",
        "ta",
        "te",
        "tg",
        "tl",
        "tr",
        "tt",
        "uk",
        "uz",
        "vi",
        "wa",
        "wuu",
        "za",
        "zh",
        "zh-min-nan",
        "zh-yue",
    ]
    lala = {
        # "Tooth decay":{ x : x for x in lngs},
        "Angular cheilitis": {},
        "Pit latrine": {
            'ar': 'مرحاض ذو حفرة',
            'bn': 'খাটা পায়খানা',
            'ca': 'Latrina de fossa',
            'ee': 'Do nugododeƒe',
            'es': 'Letrina de hoyo',
            'fa': 'توالت گودالی',
            'ha': 'Shaddar gargajiya',
            'hi': 'खुड्डी शौचालय',
            'ig': 'Ụlọ mposi',
            'it': 'Latrina a fossa',
            'ln': 'Latrine ya libulu',
            'nso': 'Boithomelo bja mokoti',
            'or': 'ବରପାଲି ପାଇଖାନା',
            'pl': 'Latryna',
            'ru': 'Ямный туалет',
            'sw': 'Choo cha shimo',
            'ta': 'குழி கழிவறை',
            'tr': 'Köy tuvaleti',
            'ur': 'گڑھے والا بیت الخلا',
            'wo': 'Duus',
            'xh': 'Ithoyilethi yomngxuma',
            'yo': 'Ṣalanga oniho',
            'zh': '旱廁',
            'zu': 'Ithoyilethe lomgodi',
        },
        "Bad breath": {},
        "Leukoplakia": {},
        "Periodontal disease": {},
        "Tonsil stones": {},
    }
    u = make_text('Dentistry', lala)
    print(u.replace("height:580px;", ""))
# ---
