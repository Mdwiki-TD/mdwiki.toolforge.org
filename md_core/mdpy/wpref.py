#!/usr/bin/python

"""

تجميع المراجع في الصفحات

python3 core8/pwb.py mdpy/wpref -lang:es ask savetofile
python3 core8/pwb.py mdpy/wpref -lang:or ask -page:ପାଟେଲୋଫିମୋରାଲ_ଯନ୍ତ୍ରଣା_ସିଣ୍ଡ୍ରୋମ
python3 core8/pwb.py mdpy/wpref -lang:or ask -page:ପୋଷ୍ଟିରିଅର_ୟୁରେଥ୍ରାଲ_ଭଲଭ ask
python3 core8/pwb.py mdpy/wpref -lang:or -page:user:Mr._Ibrahem/sandbox ask

python3 core8/pwb.py mdpy/wpref -lang:ro ask

python3 core8/pwb.py mdpy/wpref ask

"""
#
# (C) Ibrahem Qasim, 2023
#
#
#---
from wprefs.bot import *
#---
if __name__ == '__main__':
    if 'tests' in sys.argv:
        tests()
    else:
        maine()
#---