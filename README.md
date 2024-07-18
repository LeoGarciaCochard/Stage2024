# Interface graphique pour l'utilisateur participant à l'étude sur les potentiels d'erreur en milieu écologique

### Refactor en cours,  je suis en train d'améliorer le code pour le rendre plus lisible et réutilisable.


## Information

Pour l'implémentation sur la machine finale, modifier les chemins absolus dans le code `main.py` 
Ainsi que dans les boîtes OpenVibe.

(Pas pour le pilote).

## Prérequis :

- Python3.11.9

    - **Installer Python3.11 sous linux**
    ```shell
    sudo apt install python-3.11
    ```

    - **Installer Python3.11 sous MacOs**
        - **Installer brew (si non installé)**

        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
        ```shell
        brew install python@3.11
        ```

- Poetry

    - Sous linux (Si non installé) :


        - **Installer pipx**
        ```shell
        sudo apt update
        sudo apt install pipx
        pipx ensurepath
        sudo pipx ensurepath --global
        ```
        - **Installer poetry**
        ```shell
        pipx install poetry
        pipx ensurepath
        ```


    - **Sous MacOs (Si non installé) :**
    
        - **Installer brew (si non installé)**

        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

        - **Installer pipx (si non installé)**

        ```shell
        brew install pipx
        ```
        ```shell
        pipx ensurepath
        ```
        ```sh
        sudo pipx ensurepath --global # optional to allow pipx actions in global scope. See "Global installation" section below.
        ```
                - **Installer poetry (si non installé)**

        ```shell
        pipx install poetry
        ```

## Installation :


1. **Verifier l'installation de poetry** :

    ```
    poetry --version
    ```

S'il vient d'être installé mais n'est pas recconu, vous pouvez relancer le terminal 


2. **Cloner le dépôt / Extraire le .zip et se placer dans le répertoire** 

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

    
## Sans Poetry :

### Sous Linux

- Si Tkinter n'est pas installé :

```sh
sudo apt install python3-tk
```

### Puis / Sinon :

- Se placer dans le répertoire :

```sh
cd path/to/Stage2024
```
- Installer les dépendances :

```sh
pip install -r requirements.txt
```

- Lancer l'interface :

```sh
python3 main.py
```

## Outils

- Python 3.11
- LUA
- OpenVibe
- Git
- Poetry
