# Projet présenté pour les certifications RS3497 “Développer une base de données”
# RS3508 “Exploiter une base de données” : Ou Je Vais 


## | Installation

1. Télécharger puis installer PostgreSQL selon votre OS (Windows, Linux ou MacOS)
en allant à l'adresse https://www.postgresql.org/download/

2. Créer un dossier `.env` et y insérer en y replaçant les {} :

	URI_POSTGRES = postgresql://{nom utilisateur}:{ mot de passe}@localhost:5432/{base de données}

	CLE_SECRETE = {votre clé secrete}

	CLE_OPENWEATHER_1 = "{y inserer votre clé / token OpenweatherMap}"
	CLE_OPENWEATHER_2 = {si vous en disposezy inserer votre 2ème clé / token OpenweatherMap}


3. Installer python en allant sur https://www.python.org/downloads/

4. Installer python env : `sudo apt install python3.8-venv`

5. Exécuter dans un terminal à la racine du dossier de l'application:
`python3 -m venv (nom_de_l_environnement_virtuel)`
Cela créera un environnement virtuel s'appellant `nom_de_l_environnement_virtuel`

6. Lancer l'environnement virtuel :
`source (nom_de_l_environnement_virtuel)/bin/activate`
nb: pour quitter l'environnement : executer `deactivate`

7. Exécuter `pip install -r requierements.txt` pour installer les bibliothèque nécessaires

8. Mettre à jour `pip` si l'on vous le propose

9. Creer le dossier de migration :  `flask db init`

10. Créer votre 1ere migration:  `flask db migrate -m "{votre texte} "`

11. Enregistrer là :  `flask db upgrade`
Ou supprimer là :  `flask db downgrade`

12. Creer la base de données : `flash shell` puis `db.create_all()`

13. Peupler les tables en important la fonction `populate_all_tables` depuis
le dossier racine : `from app.models import populate_all_tables`
Puis `populate_all_tables()` , après quelques minutes toutes les tables seront créees

14. Enfin lancer l'application avec `flask run` depuis la racine du dossier

## | Grandes étapes d'hebergement sur serveur Ubuntu (NGINX + gunicorn)
# ----(source DigitalOcean : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04-fr )

1. Créer un point d'entrée WSGI:
A la racine du dossier `nano ~/{nom projet}/wsgi.py`
puis vérifier que le fichier contient bien
`if __name__ == "__main__":`
`    app = create_app()`
`    app.run()`

2. Créer fichier d'unité:
`sudo nano /etc/systemd/system/{nom du projet}.service`

3. Activer le projet pour qu'il demarre au boot :
`sudo systemctl start {nom projet}`
puis
`sudo systemctl enable {nom projet}`

4. Confrigurer NGINX et relier le dossier du projet à un nom de dommaine:
- `sudo nano /etc/nginx/sites-available/{nom projet}`
- `sudo ln -s /etc/nginx/sites-available/{nom projet} /etc/nginx/sites-enabled`

5. Tester la syntaxe : `sudo nginx -t`

6. Relacer NGINX : `sudo systemctl restart nginx` 

## | Description

En se basant sur les bases de données de l'OCDE et celle
du service en ligne de prévisions météorologiques, OpenWeatherMap, cette
application vous dresse un classement, en fonction des critères que vous
choisissez, des pays où vous devriez aller pour être satisfait.e.s...

Pour l'instant elle vous propose de choisir vos préferences selon 5 critères :

- Le nombre d'habitants : Elevé ou Faible
- L'esperance de vie : Elevée ou Faible
- Le taux de chômage : Elevé ou Faible
- La temperature : Elevée ou Faible
- La météo : Temps clair ou Pluie

Pour l'instant vous ne pourrez pas selectionner plus d'un critère à la fois. 
Il faudra laisser les autres selecteurs sur "Ignorer" lorsque vous
selectionnerez un critère.

Pour cela, cliquez sur l'onglet "J'y vais!", choisissez vos préferences et
cliquez sur soumettre.

L'application vous affichera alors les 10 premiers pays, classés selon
votre choix.

Vous aurez alors : 

- accès aux données de ces premiers pays

[ ET ]

- un graphique montrant l'evolution de la population du 1er pays
 entre 2000 et 2018

- un graphique présentation l'evolution du taux de chômage du premier
pays entre 2000 et 2018

- un graphique présentant le taux de chômage du 1er pays entre 2000 et 2018

- un graphique de corrélation croisant les temperarures, esperances de vie, 
population et taux de chômage du premier pays.
Plus la couleur sera claire et plus il existerait une corrélation entre les
2 facteurs.
(Dans la prochaine version du projet nous affineront les resultats trouvés
pour essayer d'en determiner la raison, quand 2 critères sont réellement
 corrélées).




