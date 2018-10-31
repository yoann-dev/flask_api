# Créer l'environnement virtuel
```
python3.6 -m venv venv_flask
source venv_flask/bin/activate
pip install -r venv_flask/requirements.txt
```

# Créer la base de données manuellement
```
source venv_flask/bin/activate
python
from BookModel import db
db.create_all()
from UserModel import db
db.create_all()
```

# Références

* http://apprendre-python.com/page-virtualenv-python-environnement-virtuel
* https://pip.pypa.io/en/stable/installing/