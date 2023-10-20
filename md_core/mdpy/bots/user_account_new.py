'''
# ---
from mdpy.bots import user_account_new
# ---
username = user_account_new.bot_username     #user_account_new.my_username
password = user_account_new.bot_password     #user_account_new.my_password      #user_account_new.mdwiki_pass
lgname_enwiki   = user_account_new.lgname_enwiki
lgpass_enwiki   = user_account_new.lgpass_enwiki
# ---
'''
import os
import configparser

# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
config = configparser.ConfigParser()
config.read(project + '/confs/user.ini')

username = config['DEFAULT']['botusername']
password = config['DEFAULT']['botpassword']

bot_username = config['DEFAULT']['botusername']
bot_password = config['DEFAULT']['botpassword']

my_username = config['DEFAULT']['my_username']
my_password = config['DEFAULT']['my_password']

mdwiki_pass = config['DEFAULT']['mdwiki_pass']

lgname_enwiki = config['DEFAULT']['lgname_enwiki']
lgpass_enwiki = config['DEFAULT']['lgpass_enwiki']

qs_token = config['DEFAULT']['qs_token']
