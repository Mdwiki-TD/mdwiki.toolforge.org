cd /data/project/mdwiki/
rm -rf mdwiki.toolforge.org-main
rm MdCoreNew.zip
# Download the md-core repository from GitHub.
wget https://github.com/MrIbrahem/mdwiki.toolforge.org/archive/refs/heads/main.zip -O MdCoreNew.zip
# Unzip the downloaded zip file
unzip MdCoreNew.zip
# Find all files in the unzipped 'md-core-main' directory that are not Python files (*.py)
# Delete those files using the '-exec' option with the 'rm' command
# find mdwiki.toolforge.org-main -type f ! -name "*.py" -exec rm {} \;
# Copy all the remaining files and directories from the 'mdwiki.toolforge.org-main' directory

# Into a new directory called 'md_core/' in the current working directory
cp -rf -v mdwiki.toolforge.org-main/md_core/* md_core/
# Remove the `mdwiki.toolforge.org-main` directory.
rm -rf mdwiki.toolforge.org-main
