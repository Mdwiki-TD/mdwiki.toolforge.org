# from new_api.mdwiki_page import MainPage as md_MainPage
'''
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
#---
# if page.isRedirect() :  return
# target = page.get_redirect_target()
#---
text        = page.get_text()
ns          = page.namespace()
links       = page.page_links()
categories  = page.get_categories(with_hidden=False)
wiki_links  = page.get_wiki_links_from_text()
refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
words       = page.get_words()
templates   = page.get_templates()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
#---
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
purge       = page.purge()
'''
#---
from mdpy.bots import user_account_new
#---
User_tables = {"username": user_account_new.my_username, "password": user_account_new.mdwiki_pass}
#---
# xxxxxxxxxxx
#---

from new_api import super_page as su_page
from new_api import bot_api
from new_api import super_login as su_login
#---
su_login.User_tables["mdwiki"] = User_tables
#---
Login = su_login.Login
#---
bot_api.login_def = Login
su_page.login_def = Login
#---
NEW_API = bot_api.NEW_API
MainPage = su_page.MainPage
change_codes = su_page.change_codes

#---
# xxxxxxxxxxx
#---
def test():
    '''
    page      = MainPage(title, 'www', family='mdwiki')
    exists    = page.exists()
    text      = page.get_text()
    timestamp = page.get_timestamp()
    user      = page.get_user()
    links     = page.page_links()
    words     = page.get_words()
    purge     = page.purge()
    templates = page.get_templates()
    save_page = page.save(newtext='', summary='', nocreate=1, minor='')
    create    = page.Create(text='', summary='')
    '''
    #---
    page = MainPage("User:Mr. Ibrahem/sandbox", 'www', family='mdwiki')
    #---
    text = page.get_text()
    print(text)
    #---
    # ex = page.page_backlinks()
    # print(f'---------------------------')
    # print(f'page_backlinks:{ex}')
    #---
    # hidden_categories= page.get_hidden_categories()
    # print(f'---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    #---
    # red = page.page_links()
    # print(f'page_links:{red}')
    #---
    # save = page.save(newtext=text + "\n{}")
    api_new = NEW_API('www', family='mdwiki')
    # login   = api_new.Login_to_wiki()
    # pages   = api_new.Find_pages_exists_or_not(liste)
    pages = api_new.Get_Newpages(limit=5000)
#---
if __name__ == '__main__':
    # python3 core8/pwb.py new_api/page
    su_page.print_test[1] = True
    su_login.print_test[1] = True
    test()
#---