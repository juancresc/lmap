https://www.r-bloggers.com/how-to-install-r-on-linux-ubuntu-16-04-xenial-xerus/


virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo chmod o+w  /usr/local/lib/R/site-library

python lmap.py -i Prueba2.csv -o out.csv