import os
import wave
import time
import threading
import customtkinter as ctk
import pyaudio

from Interface_Graphique.var_fonc.variables_info import dic_informations_incident, directory_paths, dic_informations
from Interface_Graphique.tools.buttons import ButtonImage

import Interface_Graphique.var_fonc.variables_path as paths
from Interface_Graphique.tools.frames import Frame
from Interface_Graphique.var_fonc.recolte_donnes import stimulation

class VoiceRecorder:
    def __init__(self, root, row, column):

        self.cadre = Frame(master=root, px=10, py=0, fg_color="#2b2b2b", row=row, column=column)

        self.button = ButtonImage(master=self.cadre.frame, width=150, height=150, text="", path=paths.img_btn_micro,
                                  path_hover=paths.img_btn_micro, py=0,
                                  function=self.click_handler, tooltip=True,
                                  text_tooltip="Enregistrer un incident oralement")
        self.button.afficher()

        # Recording time

        self.label = ctk.CTkLabel(self.cadre.frame, text="00:00:00")

        self.recording = False


    def click_handler(self, event):
        if self.recording:
            self.recording = False
            self.cadre.frame.configure(fg_color="#2b2b2b")
            self.label.pack_forget()
        else:
            self.recording = True
            self.cadre.frame.configure(fg_color="red")
            threading.Thread(target=self.record).start()
            self.label.pack(padx=10, pady=0)

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        frames = []

        stimulation(5)

        start_time = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            self.label.configure(text=time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))

        stream.stop_stream()
        stream.close()
        audio.terminate()

        record_path =  f"{directory_paths['path_audio']}/sub-{str(dic_informations['n_anonymat'])}_task-work_run-01_id-{str(dic_informations_incident['ID'])}_audio.wav"

        # Save the recording
        wave_file = wave.open(record_path, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

    def fixer(self):
        self.cadre.fixer()
