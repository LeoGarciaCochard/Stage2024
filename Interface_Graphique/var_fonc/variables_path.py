from Interface_Graphique.var_fonc.functions import resource_path

import pathlib as pl


fpaths = pl.Path(__file__).parent.parent.parent

SRC = fpaths / "Sources"

# Paths to images
# img_btn = resource_path("../Sources/btn.png")
# img_btn_hover = resource_path("../Sources/btn_f.png")
# img_aide = resource_path("../Sources/aide.png")
# img_aide_hover = resource_path("../Sources/aide_f.png")
#
# img_btn_micro = resource_path("../Sources/voice_rec.png")
# img_btn_micro_f = resource_path("../Sources/voice_rec_f.png")
#
# fichier_types_err = resource_path("../Sources/types_err.xlsx")

img_btn = SRC / "btn.png"
img_btn_hover = SRC / "btn_f.png"
img_aide = SRC / "aide.png"
img_aide_hover = SRC / "aide_f.png"
img_btn_micro = SRC / "voice_rec.png"
img_btn_micro_f = SRC / "voice_rec_f.png"

# Paths to files
fichier_types_err = SRC / "types_err.xlsx"

#TODO MODIFIER les path dans openVibe :
# placement : placementStimulation.xml
# - LUA
# - Generic Stream Reader
# - Generic Stream Writer
# - EDF File Writer
# - EDF File Writer Backup
#
# Ecriture : EcritureEEG.xml
# - Generic Stream Writer
# - Generic Stream Writer Backup



##################
# Paths to OpenVibe

ov = fpaths / "OpenVibe"
scenarios = ov / "Scenario"

openvibe_executable = r"C:\Program Files\openvibe-3.6.0-64bit\bin\openvibe-designer.exe"

# scenario_file_Ecriture = r"C:\Users\milio\PycharmProjects\Stage2024\OpenVibe\Scenario\EcritureEEG.xml"
# scenario_file_Stim = r"C:\Users\milio\PycharmProjects\Stage2024\OpenVibe\Scenario\placementStimulation.xml"

scenario_file_Ecriture = scenarios / "EcritureEEG.xml"
scenario_file_Stim = scenarios / "placementStimulation.xml"


# record_ov = r"C:/Users/milio/PycharmProjects/Stage2024/OpenVibe/enregistrement_en_cours/record.ov"
record_ov = ov / "enregistrement_en_cours" / "record.ov"

# path_recordStim_edf = r"C:/Users/milio/PycharmProjects/Stage2024/OpenVibe/enregistrements_avec_stim/recordStim.edf"
# path_recordStim_ov = r"C:/Users/milio/PycharmProjects/Stage2024/OpenVibe/enregistrements_avec_stim/recordStim.ov"

path_recordStim_ov = ov / "enregistrements_avec_stim" / "recordStim.ov"
path_recordStim_edf = ov / "enregistrements_avec_stim" / "recordStim.edf"



# TODO: revoir les path
# uv
#
# petry remove
#
# poetry add