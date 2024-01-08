cd /data/project/mdwiki/
rm -rf mdwikix

# Download the md-core repository from GitHub.
git clone --recurse-submodules https://github.com/MrIbrahem/mdwiki-python-files.git mdwikix

# Into a new directory called 'md_core/' in the current working directory
# cp -rf -v mdwikix/pybot/md_core/* md_core/
# cp -rf -v mdwikix/pybot/TDpynew/* TDpynew/
# cp -rf -v mdwikix/pybot/newupdater/* newupdater/

cp -rf -v mdwikix/* pybot/

chmod -R 6770 pybot

# Remove the `mdwikix` directory.
rm -rf mdwikix
