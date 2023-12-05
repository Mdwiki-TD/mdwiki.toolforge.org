cd /data/project/mdwiki/
rm -rf mdwiki.toolforge.org-main
rm MdCoreNew.zip

# Download the md-core repository from GitHub.
git clone --recurse-submodules https://github.com/MrIbrahem/mdwiki.toolforge.org.git mdwiki

# Into a new directory called 'md_core/' in the current working directory
cp -rf -v mdwiki/pybot/* pybot/

# Remove the `mdwiki.toolforge.org-main` directory.
rm -rf mdwiki
