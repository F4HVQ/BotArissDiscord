# Ariss Contact Discord Bot

## Name

Ariss Contact Discord Bot


## Description

Bot permettant l'envoi automatique de notifications vers un salon Discord, quand un évènnement ARISS est prévu dans les prochains jours.


## Compilation et installation de Python

Utilisez Python par défault ou téléchargez puis compilez en un par vous même.
Pour ce faire suivez les instructions depuis le site officiel [Python.org](https://www.python.org/downloads/)

```
cd ~
mkdir ./bots_discord/

sudo apt install libffi-dev build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev libmpdec-dev libreadline-dev

wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tar.xz
tar -xvf ./Python-3.8.20.tar.xz 
cd ./Python-3.8.20

./configure 
make
make test
sudo make install
```

Suivre les instructions indiquées dans le fichier README.rst


## Python par défaut

Spécifier Python 3.8.20 (dernièrement installé), comme étant le Python par défault.

```
cd ~
cd bots_discord
sudo update-alternatives --help
which python
python3.8 --version
which python3.8
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 2
sudo update-alternatives --config python 
python --version
```


### Sources

Récupération des sources

```  
cd ~/bots_discord
git clone git@github.com:F4HVQ/BotArissDiscord.git 01_bot_ariss
cd ./01_bot_ariss/
```

Création de l'environnement et installation des modules nécessaires

```
python -m venv .venv_bot_ariss
source ./.venv/bin/activate
pip install -r requirements.txt
```


### Configuration

Editez le fichier ~/bots_discord/01_bot_ariss/env.yaml,
pour spécifier les paramètres à votre convenance.


### Usage

Execution manuelle
```
[~]$ cd ~/bots_discord/01_bot_ariss/
[01_bot_ariss]$ source ./.env_bot_ariss/bin/activate
[01_bot_ariss]$ cd ./src
[src]$ python ./ariss_main.py --help
```

Execution automatique
```
[?]$ crontab -e
```

Ajouter la ligne d'instruction suivante
```
# Tout les jours
0 0 * * * cd /home/pi/bots_discord/01_bot_ariss && source .env_bot_ariss/bin/activate && python ./ariss_main.py -n 2

# Tout les 3 mois
0 0 * */2 * cd /home/pi/bots_discord/01_bot_ariss && source .env_bot_ariss/bin/activate && python ./ariss_main.py -n 2 --test
```

