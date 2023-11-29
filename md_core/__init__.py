# -*- coding: utf-8 -*-
"""The initialization file for the Pywikibot framework."""
#
# (C) Pywikibot team, 2008-2017
#
# Distributed under the terms of the MIT license.
#
# find      :   \s*\n(\s*#\s*[-]+\s*)+\n*^def
# find      :   \s*\n(#\s*[-]+\s*)+\n*def
# replace   :   \n\n\ndef


# find      :   \s*\n(\s*#\s*[-]+\s*)+\n*^(\s*def )
# replace   :   \n\n\n$2
