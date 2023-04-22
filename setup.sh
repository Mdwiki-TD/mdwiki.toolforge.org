
wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz
tar xzf Python-3.10.8.tgz
cd Python-3.10.8
./configure --enable-optimizations --prefix=$HOME
make altinstall prefix=~/local
cd ../
rm .bash_profile

echo 'export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/data/project/mdwiki/local/bin' >>~/.bash_profile

./local/bin/python3.10 -V
./local/bin/python3.10 -V
./local/bin/python3.10 -m pip install --upgrade pip
./local/bin/python3.10 -m pip install -r core/requirements.txt
./local/bin/python3.10 -m pip install -r requirements.in
./local/bin/python3.10 -m pip install wikitextparser
./local/bin/python3.10 -m pip install pipreqs
./local/bin/python3.10 -m pip install requests
./local/bin/python3.10 -m pip install python-dateutil
./local/bin/python3.10 -m pip install --upgrade regex==2022.10.31
rm -r -f Python-3.10.8
