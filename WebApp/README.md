## Build Setup

``` bash
# install virtualenv
sudo pip install virtualenv
sudo apt-get install python-virtualenv

# create environment
virtualenv env

# activate environment
. env/bin/activate

# install flask
pip install Flask

# serve files at localhost:5000
export FLASK_APP=run.py
flask run
```