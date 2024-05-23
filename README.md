# Data Warehouse Project

Les fichiers CSV `Weatherfact` et `location` contiennent la table des faits et la table des localisations respectivement. 

## Structure du Projet

### Dossier ETL
Ce dossier contient les fichiers Python utilisés pour les processus d'Extraction, Transformation et Chargement (ETL). Ces scripts permettent de transformer et de charger les données brutes dans des formats utilisables pour l'analyse.

### Dossier data
Ce dossier contient le dataset complet, y compris les fichiers CSV des données météorologiques pour l'Algérie, la Tunisie et le Maroc.

### Dossier Dashboard
Ce dossier contient les fichiers nécessaires pour exécuter le tableau de bord interactif. 
1. **assets** : Ce sous-dossier contient les éléments de l'interface utilisateur tels que les icônes et les fichiers CSS pour le style.
2. **App.py** : Ce fichier est le script principal de l'application Dash. En l'exécutant, une page web interactive est générée, permettant de visualiser et d'analyser les données météorologiques.

## Instructions d'Installation et d'Exécution

1. Cloner le dépôt :
    ```bash
    git clone <url_du_dépôt>
    ```
2. Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3. Exécuter l'application :
    ```bash
    python Dashboard/App.py
    ```

Une fois l'application lancée, ouvrez votre navigateur et accédez à l'URL affichée dans le terminal (par défaut, cela devrait être `http://127.0.0.1:8050/`) pour visualiser le tableau de bord interactif.

## Fonctionnalités de l'Application

- **Sélection de Station Météorologique** : Utilisez le menu déroulant pour sélectionner une station météorologique spécifique.
- **Plage de Dates** : Ajustez la plage de dates à l'aide du curseur pour filtrer les données affichées.
- **Visualisation Interactives** : Les graphiques affichent les précipitations, les températures moyennes, maximales et minimales pour la station et la période sélectionnées.

## Avantages des Entrepôts de Données

Les entrepôts de données jouent un rôle crucial dans ce projet en permettant de stocker de grandes quantités de données météorologiques de manière structurée et efficace. Ils facilitent la récupération et l'analyse des données, permettant des visualisations précises et fiables. Les entrepôts de données assurent également l'intégrité et la qualité des données, et offrent une évolutivité pour gérer des volumes de données croissants sans compromettre les performances de l'application.

En somme, cette application démontre comment l'intégration de technologies modernes comme Dash et Plotly avec des pratiques robustes de gestion des données peut fournir des outils puissants pour l'analyse et la visualisation des données météorologiques.
