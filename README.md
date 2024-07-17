# Interface graphique pour l'utilisateur participant à l'étude sur les potentiels d'erreur en milieu écologique

### Refactor en cours,  je suis en train d'améliorer le code pour le rendre plus lisible et réutilisable.


## Information

Pour l'implémentation sur la machine finale, modifier les chemins absolus dans le code `main.py` 
Ainsi que dans les boîtes OpenVibe.

(Pas pour le pilote).

## Prérequis :

- Poetry

### Si non installé :
  
#### Sous MacOs :
    
- **Installer pipx**
```shell
brew install pipx
```
```shell
pipx ensurepath
```
```sh
sudo pipx ensurepath --global # optional to allow pipx actions in global scope. See "Global installation" section below.
```
- **Installer poetry**  

```shell
pipx install poetry
```

## Installation :


1. **Cloner le dépôt / Extraire le .zip** 


2. **Se placer dans le répertoire** :

    ```
    cd path/to/Stage2024
    ```

3. **Installer les dépendances dans un environnement virtuel** :

    ```sh
    poetry install
    ```

4. **Activer l'environnement virtuel** :

    ```sh
    poetry shell
    ```

5. **Lancer l'interface** :

    ```sh
    poetry run python main.py
    ```
### Sans Poetry :

### Sous Linux

Si Tkinter n'est pas installé :

```sh
sudo apt install python3-tk
```

### Puis / Sinon :

Se placer dans le répertoire :

```
cd path/to/Stage2024
```
Installer les dépendances :

```sh
pip install -r requirements.txt
```

Lancer l'interface :

```sh
python3 main.py
```

## Outils

- Python 3.11
- LUA
- OpenVibe
- Git
- Poetry
