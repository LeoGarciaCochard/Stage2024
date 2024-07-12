# Interface Graphique pour l'utilisateur participant à l'étude sur les potentiels d'erreur en milieu écologique



## Information 

Modifier les path abs dans le code ./Interface_Graphique/Interface.py
Seulement lors de l'utilisation d'openVibe (Inutile pour le pilote sans EEG)

## Installation  :

Utilisation de python3.9

bash : 
>cd path/to/Interface_Graphique

> pip install -r requirements.txt

> Interface1.py


## Outils 

- Python
- LUA 
- OpenVibe
- Git

## EXE

> pyinstaller --onefile --hidden-import=tkinter --hidden-import=customtkinter --hidden-import=screeninfo Interface1.py
