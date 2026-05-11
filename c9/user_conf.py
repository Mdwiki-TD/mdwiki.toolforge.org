
import sys
import os
from logger_config import setup_logging as _setup_logging  # type: ignore

from dotenv import load_dotenv
try:
    load_dotenv()
except Exception as e:
    print(e)

user_script_paths = [
    'I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/',
    'I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/pybot/md_core/',
    'I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/pybot/md_core_helps/',
    'I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/pybot/td_core/',
    'I:/MD_TOOLS/mdwiki.toolforge.org/PYTHON_REPOS/pybot/',
    'I:/TOOLFORGE_TOOLS/ncc/',
    'I:/TOOLFORGE_TOOLS/ncc/nccbot/ncc_core/',
    'I:/TOOLFORGE_TOOLS/ncc/nccbot/',
]

if os.getenv("APP_ENV") == "production":
    user_script_paths = [
        '/data/project/mdwiki',
        '/data/project/mdwiki/pybot/wd_api_new',
        '/data/project/mdwiki/pybot',
        '/data/project/mdwiki/pybot/new',
        '/data/project/mdwiki/pybot/td_core',
        '/data/project/mdwiki/pybot/md_core_helps',
        '/data/project/mdwiki/pybot/md_core',
        '/data/project/mdwiki/local/lib/python3.11/site-packages'
    ]

_ver = sys.version_info[:3]
_python_v = str(_ver[0]) + str(_ver[1]) + str(_ver[2])

_red_ = "\033[91m%s\033[00m"
_blue_ = "\033[94m%s\033[00m"

print(_blue_ % 'PYTHON VERSION' + ': ' + _red_ % _python_v)

for _u_path in user_script_paths.copy():
    if os.path.exists(_u_path):
        sys.path.append(os.path.abspath(_u_path))
    else:
        print(f"user-config.py, path not exists:{_red_ % _u_path}")

bots = [
    "__main__",
    "alabel",
    "API",
    "api_page",
    "api_sql",
    "arwiki",
    "asa",
    "asa1",
    "asapages",
    "auths",
    "bots_helps",
    "bots_mv_all",
    "c18",
    "c30",
    "catsm",
    "catsn",
    "cite",
    "remove_today",
    "copy_to",
    "cos",
    "cy",
    "d_30",
    "day19",
    "dbs",
    "dbs_not_yet",
    "des",
    "desc_dicts",
    "dump26",
    "dump27",
    "dump_files",
    "dump_lua",
    "fals",
    "fotball",
    "himo_api",
    "hrr4",
    "ill",
    "ill_add",
    "imgx",
    "info",
    "infobox",
    "jsons",
    "lex-examples",
    "likeapi",
    "ment",
    "mkn",
    "most",
    "mv_it",
    "mvafrica",
    "mw_api",
    "nav",
    "nep",
    "neq",
    "new_all",
    "newapi",
    "newtra",
    "npa",
    "people",
    "petscan",
    "portal",
    "portalpages",
    "pr",
    "prop",
    "prop_labs",
    "prope",
    "qlever_dumps",
    "refgroups",
    "refn",
    "results",
    "rice3",
    "rice4",
    "stub",
    "stub1",
    "stub_tables",
    "tempdata",
    "templatecount",
    "textfiles",
    "texts",
    "to_load",
    "tra",
    "typos",
    "wd",
    "wd_api",
    "wd_api_new",
    "wd_link",
    "wd_utils",
    "WDYe",
    "wikiapi",
    "src",
    "core1.src",
    "mwclient",
    "repo",
]

for _bot in bots:
    _setup_logging(name=_bot, level="INFO")
