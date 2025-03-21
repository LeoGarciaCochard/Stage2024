import mne

input_fname = './sub-08_task-work_run-01_eeg.edf'

# Lecture du fichier EDF
raw = mne.io.read_raw_edf(input_fname, preload=True, verbose=True)

# Conversion des annotations en événements
events, event_id = mne.events_from_annotations(raw)

# Affichage du signal brut (vous verrez les annotations en surbrillance)
raw.plot()

# Affichage des événements détectés
mne.viz.plot_events(events, event_id=event_id)

# Possibilité de superposer ces événements dans la fenêtre Raw :
raw.plot(events=events, event_id=event_id)

