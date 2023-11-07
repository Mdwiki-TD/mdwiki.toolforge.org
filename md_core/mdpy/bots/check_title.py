"""
from mdpy.bots.check_title import valid_title #valid_title(title)
"""
def valid_title(title):
    # ---
    title = title.lower().strip()
    # ---
    if title.find('(disambiguation)') != -1:
        return False
    # ---
    # if title.startswith('category:') or title.startswith('file:') or title.startswith('template:') or title.startswith('user:'):
    if any(title.startswith(prefix) for prefix in ['category:', 'file:', 'template:', 'user:']):
        return False
    # ---
    return True