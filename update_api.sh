cd /data/project/mdwiki/

rm -rf newapi_x

# Download the wd-core repository from GitHub.
git clone https://github.com/MrIbrahem/newapi.git newapi_x

cp -rf newapi_x/* pybot/md_core/newapi -v

chmod -R 6770 pybot/md_core/newapi

rm -rf newapi_x

