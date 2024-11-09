# Ariss Contact Discord Bot

## Description

This bot is making announces in a Discord Channel when an ARISS contact is scheduled during the next **two weeks**. 

- It get the events from an ICS calendar from the network
- In this configuration, it filter only **European** passes


## Installation

### Python

Use default Python or install new one.


### Discord Webhook

TODO


### Sources

Récupération des sources
```
[?]$ cd ~
[~]$ git clone git@github.com:F4HVQ/BotArissDiscord.git
[~]$ cd BotArissDiscord
```

Création de l'environnement et installation des modules nécessaires
```
[BotArissDiscord]$ python -m venv .venv
[BotArissDiscord]$ source .venv/bin/activate

[BotArissDiscord]$ pip install -r requirements.txt
```


### Configuration

Copy the `.env.dist` file as `.env` file
```
cp .env.dist .env
```
Edit the `.env` file to specify
- You can change the **Location** to your area.
  It's the one from the "FM over Europe" string in the event. Put "." if you want the whole world.
- Set the **CalendarURL** to the URL containing the ICS calendar
  The URL of the ICS calendar (example: https://www.amsat-on.be/)


### Usage

Execution manuelle
```
[~]$ cd ./BotArissDiscord
[BotArissDiscord]$ source ../.venv/bin/activate
[BotArissDiscord]$ cd ./src
[src]$ python ./ariss_main.py --help
```

Execution automatique
```
[?]$ crontab -e
```

Ajouter la ligne d'instruction suivante
```
# Tout les jours
0 0 * * * cd <pat_to>/BotArissDiscord/src && ../.venv/bin/python3 ./ariss_main.py -n 2

# Tout les 3 mois
0 0 * */2 * cd <pat_to>/BotArissDiscord/src && ../.venv/bin/python3 ./ariss_main.py -t

```



