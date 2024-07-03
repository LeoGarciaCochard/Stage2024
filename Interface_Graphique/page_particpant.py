from screeninfo import get_monitors

# Obtenir les informations sur le moniteur
monitor = get_monitors()[0]

# Stocker la largeur et la hauteur de l'écran dans des variables
screen_width = monitor.width
screen_height = monitor.height

# Afficher la résolution de l'écran
print(f"La résolution de l'écran est de {screen_width} x {screen_height} pixels.")
