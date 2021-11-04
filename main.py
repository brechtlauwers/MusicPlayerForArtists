import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from tinytag import TinyTag
import os

# global variable to store music data
music = []


# Music Player application
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        global music

        # Variable to check if music is playing or/and loaded
        self.PLAYING = False
        self.LOADED = False

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # https://github.com/rdbende/Azure-ttk-theme
        # Set the theme
        self.root.tk.call('source', os.path.join(dir_path, 'Azure-ttk-theme-2.0/azure.tcl'))
        self.root.tk.call('set_theme', 'dark')
        self.root.update()
        self.root.title('Brecht music player')
        self.root.minsize(root.winfo_width(), root.winfo_height())
        self.root.geometry('1200x1000')

        # Tkinter grid configuration
        for i in range(0, 3):
            self.root.grid_rowconfigure(index=i, weight=1)
            self.root.grid_columnconfigure(index=i, weight=1)

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        files = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label='Media', menu=files)
        files.add_command(label='open')

        # load icons for buttons
        root.play_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/play.png'))
        root.pause_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/pause.png'))
        root.next_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/next.png'))
        root.previous_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/previous.png'))
        root.repeat_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/repeat.png'))
        root.shuffle_button_img = tk.PhotoImage(file=os.path.join(dir_path, 'icons/shuffle.png'))

        # create play button
        self.play_button = tk.Button(self.root, borderwidth=0, image=root.play_button_img,
                                     highlightthickness=0, activebackground="#333333")
        self.play_button['command'] = lambda: self.toggle_playpause()
        self.play_button.grid(row=2, column=1)

        # create playlist to browse music
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.grid(row=0, column=1)

        self.playlist = ttk.Treeview(self.middle_frame,
                                     selectmode="browse",
                                     columns=(1, 2, 3, 4),
                                     show='headings',
                                     height=10
                                     )

        self.playlist.pack(side='bottom')
        self.playlist.heading(1, text='Title')
        self.playlist.heading(2, text='Artist')
        self.playlist.heading(3, text='Duration')

        self.playlist.column(2, stretch=0)
        self.playlist.column(3, stretch=0)
        self.playlist.column(4, stretch=0, minwidth=0, width=0)

        # Create button to browse and add music to the playlist
        self.add_music = tk.Button(self.middle_frame, text='add music', command=lambda: self.file_browser())
        self.add_music.pack(side='top')

        # Create active music info frame
        self.leftbottom_frame = tk.Frame(self.root)
        self.leftbottom_frame.grid(row=2, column=0)

        self.musictitle = tk.Label(self.leftbottom_frame, text="")
        self.musictitle.pack(fill='both')

        self.musicartist = tk.Label(self.leftbottom_frame, text="")
        self.musicartist.pack(fill='both')

    # Select and add tracks to the music list
    def file_browser(self):
        global music
        filename_path = tk.filedialog.askdirectory()
        music = os.listdir(filename_path)

        for item in music:
            if not item.endswith(('.m4a', '.flac', '.mp3', '.wav')):
                music.remove(item)

        self.fill_playlist(filename_path)

    # Displays music list in the playlist
    def fill_playlist(self, filename_path):
        global music
        index = 0
        for item in music:
            if '-' in item:
                artist, title = item.split('-')
            else:
                title = item
                artist = ''

            title = title.replace('.m4a', '')
            title = title.replace('.flac', '')
            title = title.replace('.mp3', '')
            title = title.replace('.wav', '')

            metadata = TinyTag.get(filename_path + '/' + item)
            duration_m, duration_s = divmod(metadata.duration, 60)

            self.playlist.insert(parent='', index=index, iid=index, text='',
                                 values=(title, artist,
                                         f"{int(duration_m):02d}:{int(duration_s):02d}",
                                         filename_path + '/' + item
                                         )
                                 )
            index += 1

        self.playlist["displaycolumns"] = (1, 2, 3)
        self.playlist.bind("<Double-1>", self.play_music)

    # Play track when double clicked in the playlist
    def play_music(self, event):
        item = self.playlist.selection()[0]
        current_song = self.playlist.item(item, 'values')[3]
        mixer.music.load(current_song)
        mixer.music.play()
        self.play_button['image'] = self.root.pause_button_img
        self.musictitle['text'] = self.playlist.item(item, 'values')[0]
        self.musicartist['text'] = self.playlist.item(item, 'values')[1]
        self.LOADED = True
        self.PLAYING = True

    # Stop and unload current track
    def stop_music(self):
        mixer.music.unload()
        mixer.music.stop()
        self.LOADED = False
        self.PLAYING = False

    # Pause playing track
    def pause_music(self):
        mixer.music.pause()
        self.play_button['image'] = self.root.play_button_img
        self.PLAYING = False

    # Unpause loaded track
    def unpause_music(self):
        mixer.music.unpause()
        self.play_button['image'] = self.root.pause_button_img
        self.PLAYING = True

    # Play or pause music when play/pause button is clicked
    def toggle_playpause(self):
        if self.LOADED:
            if self.PLAYING:
                self.pause_music()
            else:
                self.unpause_music()


# main function
def main():
    root = tk.Tk()
    mixer.init()
    musicplayer = MusicPlayer(root)

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
