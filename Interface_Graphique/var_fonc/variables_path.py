import os


def resource_path(relative_path):
    """ On crée un path absolut depuis le relatif """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    return os.path.join(base_path, relative_path)

# Paths to images
img_btn = resource_path("../Sources/btn.png")
img_btn_hover = resource_path("../Sources/btn_f.png")
img_aide = resource_path("../Sources/aide.png")
img_aide_hover = resource_path("../Sources/aide_f.png")