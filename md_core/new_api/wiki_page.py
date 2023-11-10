# ---
from new_api import super_login
from new_api import bot_api
from new_api import super_page
from mdpy.bots import user_account_new

# ---
User_tables = {
    "username": user_account_new.my_username,
    "password": user_account_new.my_password
}
# ---
# xxxxxxxxxxx
# ---

# ---
super_login.User_tables["wikipedia"] = User_tables
# ---
Login = super_login.Login
# ---
bot_api.login_def = Login
super_page.login_def = Login
# ---
NEW_API = bot_api.NEW_API
MainPage = super_page.MainPage
change_codes = super_page.change_codes

# ---
# xxxxxxxxxxx
# ---


def test():
    '''
    page      = MainPage(title, 'ar', family='wikipedia')
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
    # ---
    page = MainPage("تصنيف:اليمن", 'ar', family='wikipedia')
    # ---
    text = page.get_text()
    print(text)
    # ---
    page2 = MainPage("Yemen", 'en', family='wikipedia')
    # ---
    # ---
    ex = page.page_backlinks()
    print('---------------------------')
    print(f'page_backlinks:{ex}')

    # ---
    # hidden_categories= page.get_hidden_categories()
    # print(f'---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    # ---
    # red = page.page_links()
    # print(f'page_links:{red}')
    # ---
    # save = page.save(newtext='')
    # api_new = NEW_API('en', family='wikipedia')
    # login   = api_new.Login_to_wiki()
    # pages   = api_new.Find_pages_exists_or_not(liste)
    # pages   = api_new.Get_Newpages()


# ---
if __name__ == '__main__':
    # python3 core8/pwb.py new_api/wiki_page
    super_page.print_test[1] = True
    super_login.print_test[1] = True
    test()
# ---
