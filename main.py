import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

# Initialize the Tkinter window
window = tk.Tk()
window.title("MP3 Player")
window.geometry("1980x1080")
window.configure(bg="#000000")  # Black main color/background

# Initialize the mixer
mixer.init()

# Global variables
current_song = ""
paused = False
song_index = 0


def play_song():
    global current_song, paused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        if len(song_queue) > 0:
            song = song_queue[song_index]
            current_song = song
            mixer.music.load(song)
            mixer.music.play()
            update_song_label()


def pause_song():
    global paused
    mixer.music.pause()
    paused = True


def stop_song():
    mixer.music.stop()


def add_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if file_path:
        song_queue.append(file_path)
        update_queue()


def add_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                song_queue.append(os.path.join(folder_path, file))
        update_queue()


def remove_all_songs():
    global current_song, song_index
    stop_song()
    song_queue.clear()
    current_song = ""
    song_index = 0
    update_queue()


def remove_song(index):
    global current_song, song_index
    if index == song_index and current_song != "":
        stop_song()
        current_song = ""
    song_queue.pop(index)
    update_queue()


def next_song():
    global song_index
    if song_index < len(song_queue) - 1:
        song_index += 1
        play_song()


def back_song():
    global song_index
    if song_index > 0:
        song_index -= 1
        play_song()


def update_queue():
    song_queue_listbox.delete(0, tk.END)
    for song in song_queue:
        song_queue_listbox.insert(tk.END, os.path.basename(song))


def update_state():
    if paused:
        state_label.config(text="State: Paused")
    elif current_song != "":
        state_label.config(text="State: Playing")
    else:
        state_label.config(text="State: Stopped")
    window.after(1000, update_state)


def update_song_label():
    song_label.config(text="" + os.path.basename(current_song))


def search_song(event):
    search_text = search_entry.get()
    song_queue_listbox.delete(0, tk.END)
    for song in song_queue:
        if search_text.lower() in os.path.basename(song).lower():
            song_queue_listbox.insert(tk.END, os.path.basename(song))


# Create the GUI components
now_playing_label = tk.Label(window, text="Now Playing:", bg="#000000", fg="#FFFFFF", font=("Arial", 24))
now_playing_label.pack(pady=20)

song_label = tk.Label(window, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 20))
song_label.pack(pady=10)

button_frame = tk.Frame(window, bg="#000000")
button_frame.pack(pady=10)

play_button = tk.Button(button_frame, text="Play", command=play_song, font=("Arial", 20))
play_button.pack(side=tk.LEFT, padx=10)

pause_button = tk.Button(button_frame, text="Pause", command=pause_song, font=("Arial", 20))
pause_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_song, font=("Arial", 20))
stop_button.pack(side=tk.LEFT, padx=10)

back_button = tk.Button(button_frame, text="Back", command=back_song, font=("Arial", 20))
back_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(button_frame, text="Next", command=next_song, font=("Arial", 20))
next_button.pack(side=tk.LEFT, padx=10)

add_file_button = tk.Button(window, text="Add File", command=add_file, font=("Arial", 20))
add_file_button.pack(pady=10)

add_folder_button = tk.Button(window, text="Add Folder", command=add_folder, font=("Arial", 20))
add_folder_button.pack(pady=10)

remove_all_button = tk.Button(window, text="Remove All Songs", command=remove_all_songs, font=("Arial", 20))
remove_all_button.pack(pady=10)

song_queue_listbox = tk.Listbox(window, bg="#000000", fg="#FFFFFF", selectbackground="#FFC0CB",
                               selectforeground="#000000", font=("Arial", 16), height=10)
song_queue_listbox.pack(pady=20)

song_queue_scrollbar = tk.Scrollbar(window, bg="#FFFFFF")
song_queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

song_queue_listbox.config(yscrollcommand=song_queue_scrollbar.set)
song_queue_scrollbar.config(command=song_queue_listbox.yview)

song_queue_listbox.bind("<Double-Button-1>", lambda event: play_song())
song_queue_listbox.bind("<Delete>", lambda event: remove_song(song_queue_listbox.curselection()[0]))

state_label = tk.Label(window, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 16))
state_label.pack(pady=10)

search_label = tk.Label(window, text="Search:", bg="#000000", fg="#FFFFFF", font=("Arial", 16))
search_label.pack(pady=10)

search_entry = tk.Entry(window, bg="#FFFFFF", fg="#000000", font=("Arial", 16))
search_entry.pack(pady=10)
search_entry.bind("<KeyRelease>", search_song)

# Initialize the song queue
song_queue = []

# Start updating the state label
update_state()

# Run the Tkinter event loop
window.mainloop()
