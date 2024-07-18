# Interface graphique pour l'utilisateur participant à l'étude sur les potentiels d'erreur en milieu écologique

### Refactor en cours,  je suis en train d'améliorer le code pour le rendre plus lisible et réutilisable.


## Information

Pour déploiement sur la machine finale, modifier les chemins absolus dans le code `main.py` 
Ainsi que dans les boîtes OpenVibe.

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

- **Python3.11.9**

    - **Installer Python3.11**
        - **Installer brew (si non installé)**

        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

        - **Installer python3.11**

        ```shell
        brew install python@3.11
        ```

- **Poetry**

    - **(Si non installé) :**
    
        - **Installer brew (si non installé)**

        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

        - **Installer pipx (si non installé)**

        ```shell
        brew install pipx
        ```
            
        - **Installer poetry (si non installé)**

        ```shell
        pipx install poetry
        pipx ensurepath
        ```
- **Tkinter**

    - **(Si non installé) :**
    
        - **Installer brew (si non installé)**

        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

        - **Installer Tkinter**

        ```shell
        brew install python-tk
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


