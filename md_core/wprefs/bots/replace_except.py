import re
import sys
from contextlib import suppress

_regex_cache = {}

NESTED_TEMPLATE_REGEX = re.compile(
    r"""
{{\s*(?:msg:\s*)?
  (?P<name>[^{\|#0-9][^{\|#]*?)\s*
  (?:\|(?P<params> [^{]*?
          (({{{[^{}]+?}}}
            |{{[^{}]+?}}
            |{[^{}]*?}
          ) [^{]*?
        )*?
    )?
  )?
}}
|
(?P<unhandled_depth>{{\s*[^{\|#0-9][^{\|#]*?\s* [^{]* {{ .* }})
""",
    re.VERBOSE | re.DOTALL,
)

FILE_LINK_REGEX = r"""
    \[\[\s*
    (?:%s)  # namespace aliases
    \s*:
    (?=(?P<filename>
        [^]|]*
    ))(?P=filename)
    (
        \|
        (
            (
                (?=(?P<inner_link>
                    \[\[.*?\]\]
                ))(?P=inner_link)
            )?
            (?=(?P<other_chars>
                [^\[\]]*
            ))(?P=other_chars)
        |
            (?=(?P<not_wikilink>
                \[[^]]*\]
            ))(?P=not_wikilink)
        )*?
    )??
    \]\]
"""
PYTHON_VERSION = sys.version_info[:3]
if PYTHON_VERSION >= (3, 9):
    removeprefix = str.removeprefix  # type: ignore[attr-defined]
    removesuffix = str.removesuffix  # type: ignore[attr-defined]
else:

    def removeprefix(string: str, prefix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        if string.startswith(prefix):
            return string[len(prefix) :]
        return string

    def removesuffix(string: str, suffix: str) -> str:
        """Remove prefix from a string or return a copy otherwise.

        .. versionadded:: 5.4
        """
        if string.endswith(suffix):
            return string[: -len(suffix)]
        return string


def compileLinkR(withoutBracketed: bool = False, onlyBracketed: bool = False):
    """Return a regex that matches external links."""
    notAtEnd = r'\]\s\.:;,<>"\|\)'
    notInside = r'\]\s<>"'
    regex = r'(?P<url>http[s]?://[^{notInside}]*?[^{notAtEnd}]' r'(?=[{notAtEnd}]*\'\')|http[s]?://[^{notInside}]*' r'[^{notAtEnd}])'.format(notInside=notInside, notAtEnd=notAtEnd)

    if withoutBracketed:
        regex = r'(?<!\[)' + regex
    elif onlyBracketed:
        regex = r'\[' + regex
    linkR = re.compile(regex)
    return linkR


def ignore_case(string: str) -> str:
    """Return a case-insensitive pattern for the string.

    .. versionchanged:: 7.2
       `_ignore_case` becomes a public method
    """
    return ''.join(f'[{c}{s}]' if c != s else c for s, c in zip(string, string.swapcase()))


def _tag_pattern(tag_name: str) -> str:
    """Return a tag pattern for the given tag name."""
    return r'<{0}(?:>|\s+[^>]*(?<!/)>)' r'[\s\S]*?' r'</{0}\s*>'.format(ignore_case(tag_name))  # start tag  # contents  # end tag


def _create_default_regexes() -> None:
    """Fill (and possibly overwrite) _regex_cache with default regexes."""
    _regex_cache.update(
        {
            # categories
            'category': (r'\[\[ *(?:%s)\s*:.*?\]\]', lambda site: '|'.join(site.namespaces[14])),
            'comment': re.compile(r'<!--[\s\S]*?-->'),
            # files
            'file': (FILE_LINK_REGEX, lambda site: '|'.join(site.namespaces[6])),
            # section headers
            'header': re.compile(r'(?:(?<=\n)|\A)(?:<!--[\s\S]*?-->)*' r'=(?:[^\n]|<!--[\s\S]*?-->)+=' r' *(?:<!--[\s\S]*?--> *)*(?=\n|\Z)'),
            # external links
            'hyperlink': compileLinkR(),
            # also finds links to foreign sites with preleading ":"
            'interwiki': (r'\[\[:?(%s)\s?:[^\]]*\]\]\s*', lambda site: '|'.join(ignore_case(i) for i in site.validLanguageLinks() + list(site.family.obsolete.keys()))),
            # Module invocations (currently only Lua)
            'invoke': (r'\{\{\s*\#(?:%s):[\s\S]*?\}\}', lambda site: '|'.join(ignore_case(mw) for mw in site.getmagicwords('invoke'))),
            # this matches internal wikilinks, but also interwiki, categories, and
            # images.
            'link': re.compile(r'\[\[[^\]|]*(\|[^\]]*)?\]\]'),
            # pagelist tag (used in Proofread extension).
            'pagelist': re.compile(r'<{}[\s\S]*?/>'.format(ignore_case('pagelist'))),
            # Wikibase property inclusions
            'property': (r'\{\{\s*\#(?:%s):\s*[Pp]\d+.*?\}\}', lambda site: '|'.join(ignore_case(mw) for mw in site.getmagicwords('property'))),
            # lines that start with a colon or more will be indented
            'startcolon': re.compile(r'(?:(?<=\n)|\A):(.*?)(?=\n|\Z)'),
            # lines that start with a space are shown in a monospace font and
            # have whitespace preserved.
            'startspace': re.compile(r'(?:(?<=\n)|\A) (.*?)(?=\n|\Z)'),
            # tables often have whitespace that is used to improve wiki
            # source code readability.
            # TODO: handle nested tables.
            'table': re.compile(r'(?:(?<=\n)|\A){\|[\S\s]*?\n\|}|%s' % _tag_pattern('table')),
            'template': NESTED_TEMPLATE_REGEX,
        }
    )


def _tag_regex(tag_name: str):
    """Return a compiled tag regex for the given tag name."""
    return re.compile(_tag_pattern(tag_name))


def _get_regexes(keys, site):
    """Fetch compiled regexes."""
    if not _regex_cache:
        _create_default_regexes()

    result = []

    for exc in keys:
        if not isinstance(exc, str):
            # assume it's a regular expression
            result.append(exc)
            continue

        # assume the string is a reference to a standard regex above,
        # which may not yet have a site specific re compiled.
        if exc in _regex_cache:
            if isinstance(_regex_cache[exc], tuple):
                if not site and exc in ('interwiki', 'property', 'invoke', 'category', 'file'):
                    raise ValueError(f"Site cannot be None for the '{exc}' regex")

                if (exc, site) not in _regex_cache:
                    re_text, re_var = _regex_cache[exc]
                    _regex_cache[(exc, site)] = re.compile(re_text % re_var(site), re.VERBOSE)

                result.append(_regex_cache[(exc, site)])
            else:
                result.append(_regex_cache[exc])
        else:
            # nowiki, noinclude, includeonly, timeline, math and other
            # extensions
            _regex_cache[exc] = _tag_regex(exc)
            result.append(_regex_cache[exc])

        # handle aliases
        if exc == 'source':
            result.append(_tag_regex('syntaxhighlight'))
        elif exc == 'syntaxhighlight':
            result.append(_tag_regex('source'))
        elif exc == 'chem':
            result.append(_tag_regex('ce'))
        elif exc == 'math':
            result.append(_tag_regex('chem'))
            result.append(_tag_regex('ce'))

    return result


def replaceExcept(text: str, old, new, exceptions: list, caseInsensitive: bool = False, allowoverlap: bool = False, marker: str = '', site=None, count: int = 0) -> str:
    # if we got a string, compile it as a regular expression
    if isinstance(old, str):
        old = re.compile(old, flags=re.IGNORECASE if caseInsensitive else 0)

    # early termination if not relevant
    if not old.search(text):
        return text + marker

    dontTouchRegexes = _get_regexes(exceptions, site)

    index = 0
    replaced = 0
    markerpos = len(text)
    while not count or replaced < count:
        if index > len(text):
            break
        match = old.search(text, index)
        if not match:
            # nothing left to replace
            break

        # check which exception will occur next.
        nextExceptionMatch = None
        for dontTouchR in dontTouchRegexes:
            excMatch = dontTouchR.search(text, index)
            if excMatch and (nextExceptionMatch is None or excMatch.start() < nextExceptionMatch.start()):
                nextExceptionMatch = excMatch

        if nextExceptionMatch is not None and nextExceptionMatch.start() <= match.start():
            # an HTML comment or text in nowiki tags stands before the next
            # valid match. Skip.
            index = nextExceptionMatch.end()
        else:
            # We found a valid match. Replace it.
            if callable(new):
                # the parameter new can be a function which takes the match
                # as a parameter.
                replacement = new(match)
            else:
                # it is not a function, but a string.

                # it is a little hack to make \n work. It would be better
                # to fix it previously, but better than nothing.
                new = new.replace('\\n', '\n')

                # We cannot just insert the new string, as it may contain regex
                # group references such as \2 or \g<name>.
                # On the other hand, this approach does not work because it
                # can't handle lookahead or lookbehind (see bug T123185).
                # So we have to process the group references manually.
                replacement = ''

                group_regex = re.compile(r'\\(\d+)|\\g<(.+?)>')
                last = 0
                for group_match in group_regex.finditer(new):
                    group_id = group_match.group(1) or group_match.group(2)
                    with suppress(ValueError):
                        group_id = int(group_id)

                    try:
                        replacement += new[last : group_match.start()]
                        replacement += match.group(group_id) or ''
                    except IndexError:
                        raise IndexError(f'Invalid group reference: {group_id}\n Groups found: {match.groups()}')
                    last = group_match.end()
                replacement += new[last:]

            text = text[: match.start()] + replacement + text[match.end() :]

            # continue the search on the remaining text
            if allowoverlap:
                index = match.start() + 1
            else:
                index = match.start() + len(replacement)
            if not match.group():
                # When the regex allows to match nothing, shift by one char
                index += 1
            markerpos = match.start() + len(replacement)
            replaced += 1
    text = text[:markerpos] + marker + text[markerpos:]
    return text
