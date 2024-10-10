import tkinter as tk
import tkinter.filedialog as filedialog
import whisper
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
import torch
import os

def convertir(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def drop_inside_list_box(event):
    files = listb.tk.splitlist(event.data)
    for filename in files:
        listb.insert(tk.END, filename)

def select_file():
    file_path = filedialog.askopenfilename()
    listb.insert(tk.END, file_path)

def clear_file():
    selected_index = listb.curselection()
    listb.delete(selected_index)

def clear_all_file():
    listb.delete(0, tk.END)

def transcribe_all_files():
    if listb.size() > 0:
        progress_window = tk.Toplevel(window)
        progress_window.title("Transcription en cours")
        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()

        x_pos = (screen_width / 2) - (200 / 2)
        y_pos = (screen_height / 2) - (50 / 2)

        progress_window.geometry("400x50+%d+%d" % (x_pos, y_pos))
        progressbar = ttk.Progressbar(progress_window, orient="horizontal", length=400, mode="indeterminate")
        progressbar.pack()
        progressbar.start()
        progress_window.update()

        def transcribe_all():
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model = whisper.load_model("turbo").to(device)

            for index in range(listb.size()):
                selected_item = listb.get(index)
                result = model.transcribe(selected_item)

                base_name = os.path.basename(selected_item)
                file_name, file_extension = os.path.splitext(base_name)
                save_path = os.path.join(os.path.dirname(selected_item), f"{file_name}_transcription.txt")

                with open(save_path, "w", encoding="utf-8") as file:
                    for segment in result["segments"]:
                        start_time = convertir(segment["start"])
                        end_time = convertir(segment["end"])
                        file.write(f"{start_time} - {end_time}: {segment['text']}\n")

            progressbar.stop()
            progress_window.destroy()

            fin = tk.Toplevel(window)
            fin.title("Fin de la transcription")
            fin.geometry("300x100")
            fin_label = tk.Label(fin, text="La transcription est terminée")
            fin_label.pack(pady=20)
            bouton_quitter = tk.Button(fin, text="Quitter", command=fin.destroy)
            bouton_quitter.pack()

        thread = threading.Thread(target=transcribe_all)
        thread.start()
    else:
        text.delete(1.0, tk.END)
        text.insert(tk.END, "Ajoutez des fichiers avant de lancer la transcription")

window = TkinterDnD.Tk()

window.geometry('1000x800')
window.config(bg='Navy')
window.wm_title("Retranscripteur")

label = tk.Label(window, text="Bienvenue\n\n1) Ajoutez vos fichiers audio ici en les glissant ici ou en cliquant sur 'ajouter fichier' ( mp3, mp4, avi, wav )\n2) Selectionnez les fichiers que vous souhaitez transcrire et cliquez sur 'transcrire'\n3)Le texte sera copié dans le copier/coller, dans la fenêtre située ci-dessous et à l'emplacement du fichier audio/video\n", justify=tk.LEFT)
label.config(bg='White')
label.pack(side=tk.TOP)

listb = tk.Listbox(window, selectmode=tk.SINGLE, width=100, height=10)
listb.pack()
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box)

button = tk.Button(text='Ajouter fichier', command=select_file)
button.pack()

button = tk.Button(text='Effacer', command=clear_file)
button.pack()

button = tk.Button(text='Tout effacer', command=clear_all_file)
button.pack()

button = tk.Button(text='Transcrire tous les fichiers', command=transcribe_all_files)
button.pack()

text = tk.Text(wrap=tk.WORD, width=100, height=30)
text.pack()

window.mainloop()
