from tkinter import *
from PIL import Image, ImageTk
import subprocess
import sys
import pygame
from music_manager import music_manager

def root_destroy():
    music_manager.save_state()
    music_manager.stop()
    root.destroy()

def nextmusic():
    music_manager.next_track()

def prevmusic():
    music_manager.prev_track()

def start_game():
    music_manager.save_state()
    pygame.mixer.music.stop()
    root.destroy()
    subprocess.Popen([sys.executable, "game.py"])

root = Tk()
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", lambda: (root_destroy()))
root.geometry("400x400+350+200")
root.title("Menu")

# Запускаємо музику лише якщо вона не була збережена як вимкнена або призупинена
if not music_manager.is_playing and not music_manager.paused:
    music_manager.play()

img = Image.open("%3F%3F%3F%3F.webp")
img = img.resize((400, 400))
bg_img = ImageTk.PhotoImage(img)

bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ================= SETTINGS =================
def sett():
    root.withdraw()

    root1 = Toplevel(root)
    root1.resizable(False, False)
    root1.geometry("400x400+350+200")
    root1.title("Settings")

    Label(root1, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

    def C():
        root1.withdraw()

        root3 = Toplevel(root1)
        root3.resizable(False, False)
        root3.geometry("400x400+350+200")
        root3.title("Control Settings")

        Label(root3, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        def back2():
            root3.destroy()
            root1.deiconify()

        Label(root3, text="Control Settings",
              font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=20)

        Label(root3, text="W: Move Forward", font="arial 15",
              fg="white", bg="#832625").pack(pady=10)
        Label(root3, text="S: Move Backward", font="arial 15",
              fg="white", bg="#832625").pack(pady=10)
        Label(root3, text="A: Move Left", font="arial 15",
              fg="white", bg="#832625").pack(pady=10)
        Label(root3, text="D: Move Right", font="arial 15",
              fg="white", bg="#832625").pack(pady=10)

        Button(root3, text="Back", bg="#832625",
               font="arial 15", command=back2).pack(pady=20)

    def back1():
        root1.destroy()
        root.deiconify()

    def mus():
        root1.withdraw()

        root2 = Toplevel(root1)
        root2.resizable(False, False)
        root2.geometry("400x400+350+200")
        root2.title("Sound Settings")

        Label(root2, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        def back():
            root2.destroy()
            root1.deiconify()

        def toggle_music():
            if val.get() == "on":
                music_manager.play()
            else:
                music_manager.stop()

        def set_volume(value):
            music_manager.set_volume(int(value) / 100)

        Label(root2, text="Sound Settings",
              font="arial 20 bold", fg="white", bg="#0c1d37").place(relx=0.5, y=40, anchor="center")

        val = StringVar(value="on")

        Radiobutton(root2, text="On", variable=val, value="on",
                    bg="white", command=toggle_music)\
            .place(relx=0.45, rely=0.4, anchor="center")

        Radiobutton(root2, text="Off", variable=val, value="off",
                    bg="white", command=toggle_music)\
            .place(relx=0.55, rely=0.4, anchor="center")

        scale = Scale(root2, from_=0, to=100,
                      orient=HORIZONTAL, command=set_volume,bg="#0c1d37", fg="white")
        scale.set(25)
        scale.place(relx=0.5, rely=0.3, anchor="center")

        Button(root2, text="Previous", bg="#832625",
               command=prevmusic).place(relx=0.4, rely=0.6, anchor="center")

        Button(root2, text="Next", bg="#832625",
               command=nextmusic).place(relx=0.6, rely=0.6, anchor="center")

        Button(root2, text="Back", bg="#832625",
               command=back).place(relx=0.5, rely=0.75, anchor="center")
        
        k2 = 0

        def pause():
            global k2

            if k2 % 2 == 0:
                pygame.mixer.music.pause()
                music_manager.is_playing = False
                butt["text"] = "▶️"
            else:
                pygame.mixer.music.unpause()
                music_manager.is_playing = True
                butt["text"] = "⏸️"

            k2 += 1

        butt=Button(root2,text="⏸️",bg="#832625",command=pause)
        butt.place(relx=0.5, rely=0.5, anchor="center")

    Label(root1, text="Settings",
          font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=10)

    Button(root1, text="Controls", font="arial 15 bold",
           fg="white", bg="#0c1d37", command=C).pack(pady=10)

    Button(root1, text="Sound", font="arial 15 bold",
           fg="white", bg="#0c1d37", command=mus).pack(pady=10)

    Button(root1, text="Back", bg="#832625",
           font="arial 15 bold", command=back1).pack(pady=20)

Label(root, text="Menu",
      fg="white", bg="#0c1d37",
      font="arial 20 bold").pack(pady=20)

Button(root, text="Start Game",
       font="arial 15", fg="white",
       bg="#0c1d37", command=start_game).pack(pady=10)

def open_music_menu():
    root.withdraw()

    root2 = Toplevel(root)
    root2.resizable(False, False)
    root2.geometry("400x400+350+200")
    root2.title("Sound Settings")

    Label(root2, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

    def back():
        root2.destroy()
        root.deiconify()

    def toggle_music():
        if val.get() == "on":
            music_manager.play()
        else:
            music_manager.stop()

    def set_volume(value):
        music_manager.set_volume(int(value) / 100)

    Label(root2, text="Sound Settings",
          font="arial 20 bold", fg="white", bg="#0c1d37").place(relx=0.5, y=40, anchor="center")

    val = StringVar(value="on")

    Radiobutton(root2, text="On", variable=val, value="on",
                bg="white", command=toggle_music)\
        .place(relx=0.45, rely=0.4, anchor="center")

    Radiobutton(root2, text="Off", variable=val, value="off",
                bg="white", command=toggle_music)\
        .place(relx=0.55, rely=0.4, anchor="center")

    scale = Scale(root2, from_=0, to=100,
                  orient=HORIZONTAL, command=set_volume,bg="#0c1d37", fg="white")
    scale.set(25)
    scale.place(relx=0.5, rely=0.3, anchor="center")

    Button(root2, text="Previous", bg="#832625",
           command=prevmusic).place(relx=0.4, rely=0.6, anchor="center")

    Button(root2, text="Next", bg="#832625",
           command=nextmusic).place(relx=0.6, rely=0.6, anchor="center")

    Button(root2, text="Back", bg="#832625",
           command=back).place(relx=0.5, rely=0.75, anchor="center")
    
    k2 = 0

    def pause():
        global k2

        if k2 % 2 == 0:
            pygame.mixer.music.pause()
            music_manager.is_playing = False
            butt["text"] = "▶️"
        else:
            pygame.mixer.music.unpause()
            music_manager.is_playing = True
            butt["text"] = "⏸️"

        k2 += 1

    butt=Button(root2,text="⏸️",bg="#832625",command=pause)
    butt.place(relx=0.5, rely=0.5, anchor="center")

Button(root, text="Settings",
       font="arial 15", bg="#0c1d37",
       fg="white", command=sett).pack(pady=10)

Button(root, text="Exit",
       font="arial 15 bold", bg="#832625",
       fg="white", command=root_destroy).pack(pady=10)

root.mainloop()