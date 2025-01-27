# Interface graphique pour l'utilisateur participant à l'étude sur les potentiels d'erreur en milieu écologique

### Description

Dans le dossier `Interface_Graphique`, vous trouverez le fichier `interface1.py` qui est le premier fichier de 
l'interface graphique que je vous ai envoyé par mail, le code fonctionne mais n'est absolument pas modulable.
Les dossiers `pages`, `tools` et `var_fonc` sont des dossiers qui contiennent des les fichiers python qui sont utilisés 
dans le `main.py` pour l'interface en poo.

Le fichier `main.py` est le fichier principal de l'interface graphique en POO

Le dossier `Database` est l'emplacement de récolte des données de l'étude sous format BIDS.
Celui de `DATA` est l'ancien emplacement de récolte des données de l'étude lié au fichier `interface1.py`.

Le dossier `OpenVibe` contient les scénarios OpenVibe utilisées pour l'acquisition des données, les dossiers 
d'enregistrement depuis openvibe ainsi que le script LUA pour placer les stimulations.

## Information

Pour déploiement sur la machine finale, modifier les chemins absolus dans le code 
`Interface_Graphique/var_fonc/variables_paths.py` 
Ainsi que dans les boîtes OpenVibe.
Et dans le script LUA l.166

(Pas pour le pilote).


# Linux :

## Prérequis :

- Python3.11.9

    - **Installer Python3.11**
        ```shell
        sudo apt update
        sudo apt upgrade
        sudo apt install python3.11
        ```

- Poetry

    - **Sous linux (Si non installé)** :
        - **Installer pipx**

        ```shell
        sudo apt install pipx
        ```
        - **Installer poetry**
        ```shell
        pipx install poetry
        pipx ensurepath
        ```

- **Tkinter**
  - **(Si non installé) :**
    - **Installer Tkinter :**
    ```shell
    sudo apt update
    sudo apt install python3-tk
    ```

# MacOS :

## Prérequis :


- **Installer brew (si non installé)**

    ```shell
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```


- **Poetry**

    - **(Si non installé) :**
    
        - **Installer pipx (si non installé)**

        ```shell
        brew install pipx
        ```
            
        - **Installer poetry**

        ```shell
        pipx install poetry
        pipx ensurepath
        ```
  - **Pyenv :**
    ```shell
    brew install pyenv
    brew install openssl readline sqlite3 xz zlib
    
    env LDFLAGS="-L$(brew --prefix openssl@1.1)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix sqlite3)/lib -L$(brew --prefix xz)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix tcl-tk)/lib" \
    CPPFLAGS="-I$(brew --prefix openssl@1.1)/include -I$(brew --prefix readline)/include -I$(brew --prefix sqlite3)/include -I$(brew --prefix xz)/include -I$(brew --prefix zlib)/include -I$(brew --prefix tcl-tk)/include" \
    PKG_CONFIG_PATH="$(brew --prefix openssl@1.1)/lib/pkgconfig:$(brew --prefix readline)/lib/pkgconfig:$(brew --prefix sqlite3)/lib/pkgconfig:$(brew --prefix xz)/lib/pkgconfig:$(brew --prefix zlib)/lib/pkgconfig:$(brew --prefix tcl-tk)/lib/pkgconfig" \
    pyenv install 3.11
    ```


# Installation avec Poetry :

1. **Verifier l'installation de poetry** :

    ```shell
    poetry --version
    ```

S'il vient d'être installé mais n'est pas reconnu, vous pouvez relancer le terminal 


2. **Cloner le dépôt / Extraire le .zip et se placer dans le répertoire** 

    ```
    cd path/to/Stage2024
    ```

3. **Update le lock** :

    ```sh
    poetry lock
    ```

4. **Installer les dépendances dans un environnement virtuel** :

    ```sh
    poetry install
    ```

5. **Activer l'environnement virtuel** :

    ```sh
    poetry shell
    ```

6. **Lancer l'interface** :

    ```sh
    poetry run python main.py
    ```


