import math
import random
import os
import sys
import json
import subprocess
import ctypes
from PySide6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QScrollArea, QStackedWidget, QGraphicsOpacityEffect, QInputDialog, QLineEdit, QDialog, QFileDialog
from PySide6.QtGui import QClipboard, QIcon, QMovie
from pymobiledevice3.lockdown import create_using_usbmux, NoDeviceConnectedError
from typing import Optional

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

ICON_PATH = resource_path('CatICON.ico')
ART_UNLOCK_TOKEN = 'catchecker_art_unlocked_v1'

ARTS = {
    'Cat Checker': '''
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠙⢻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⣠⣄⠀⢻⣿⣿⣿⣿⣿⡿⠀⣠⣄⠀⠀⠀⢻⣿⣿⣏⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⠀⠀⠀⠀⠰⣿⣿⠀⢸⣿⣿⣿⣿⣿⡇⠀⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠙⠃⠀⣼⣿⣿⣿⣿⣿⣇⠀⠙⠛⠁⠀⠀⣼⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣷⣤⣄⣀⣠⣤⣾⣿⣿⣿⣿⣽⣿⣿⣦⣄⣀⣀⣤⣾⣿⣿⣿⣿⠃⠀⠀⢀⣀⠀⠀
        ⠰⡶⠶⠶⠶⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠉⠉⠙⠛⠋⠀
        ⠀⠀⢀⣀⣠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠷⠶⠶⠶⢤⣤⣀⠀
        ⠀⠛⠋⠉⠁⠀⣀⣴⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣤⣀⡀⠀⠀⠀⠀⠘⠃
        ⠀⠀⢀⣤⡶⠟⠉⠁⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠉⠙⠳⠶⣄⡀⠀⠀
        ⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',
    'Anime Tyanka': '''
        ⣄⡀⠀⠀⠀⠀⠀⠀⣠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣻⣿⣶⣤⣀⢈⣀⣲⣷⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣾⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢠⣾⣛⢿⠿⢿⣿⣿⣿⣛⣹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⣸⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠜⣿⡟⠸⣿⣿⣿⢙⣿⣿⣿⣿⣿⣿⣿⣿⠑⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⣿⣗⠰⠘⡹⡏⣀⡟⣿⣿⣿⣿⣿⣿⣿⢆⠀⠀⠀⠀⡀⢀⣀⠀⠀⠀⠀⠀
        ⠀⠘⣿⣽⠀⠀⠁⠁⠘⠽⢻⣿⡏⣹⣿⡿⣿⠁⠉⢀⣤⣾⣾⣿⣿⠗⠋⠁⠀⠀
        ⠀⠸⡸⣦⠀⠀⠀⠀⠀⣸⣿⣧⣿⣿⡗⠃⠀⣐⣾⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠙⣷⣶⣲⣷⣄⡾⣽⣟⣛⣛⣛⡓⠶⣟⣿⣿⡿⣵⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣿⣿⣿⣿⣫⣿⣽⣿⣶⣶⣶⣿⡞⠘⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢹⢿⢏⣻⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⠈⠻⣿⣿⣿⣧⢨⠀⠀⠀⠀
        ⠀⠀⠀⢂⣼⡾⡿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣾⣆⠀⠀⠀
        ⠀⠀⢀⠍⣿⣻⣦⣿⣿⣿⣿⣿⣿⣿⣿⣇⢂⠀⠀⠀⠀⠙⣿⣿⣿⣇⡄⠀
        ⠀⠀⠀⢠⣧⣸⣿⣿⡿⡿⠿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠀
        ⠀⠀⠀⣸⣿⣿⣿⣟⣿⣾⣷⡻⣍⢽⣿⣿⡄⢀⡀⢀⡀⠀⠀⣿⣿⣿⣿⠀
        ⠀⠀⠀⣿⣿⣿⡟⢋⣻⠿⣿⣿⣿⣷⣿⣿⣷⡄⠖⢀⠀⠈⠀⠻⣿⡟⠃⠀
        ⠀⠀⢸⣿⣿⣿⢁⣾⣿⣿⡾⡜⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⢠⡄⠀⠀
        ⠀⢀⣿⣿⣿⣿⢸⣿⣿⣿⣿⣵⡿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣀⣼⡗⠀⠀
        ⠀⣸⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠆⠀
        ⠠⠻⠿⣿⣭⣽⣿⣿⣿⣿⣿⣿⣷⣦⣽⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⠁⠀⠀
        ⠀⠘⣤⣀⣃⣀⢸⣿⣿⣿⣿⣿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣠⣴⠇⠀⠀
        ⠀⠸⠉⠹⠇⠀⠈⣻⣿⣿⣿⠀⠀⠀⠀⠀⠫⢿⣿⣿⣿⣿⣿⠿⠏⠀⠀⠀
        ⠀⠀⠀⠀⠠⠀⣧⣿⣿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⡶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣿⣋⡒⢤⣄⣀⣠⡄
    ''',
    'Femboy': '''
    ⣿⡟⢸⣿⣿⣿⣄⠹⣷⠰⣤⣌⡙⢿⠏⣠⣿⣿⣿⣿⡇⣸
    ⣿⡇⣾⣿⣿⣿⣿⡧⠈⣀⣹⣿⣿⣦⣰⣿⣿⣿⣿⣿⡇⣿
    ⣿⡇⢿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿
    ⣿⣇⢸⣿⡿⠿⠿⠿⠿⣿⣿⣿⣿⠿⠟⠛⠛⢻⣿⣿⢁⣿
    ⡿⠿⠄⠻⡖⢰⡆⠀⠀⢸⣿⣿⡇⠀⠀⢸⡆⢹⠋⠁⠚⣿
    ⣷⡀⠲⣶⡇⢺⣷⡀⢀⡾⠿⣿⣷⣀⣀⣾⠇⣸⡿⠋⣰⣿
    ⣿⣿⢁⣦⣀⣡⣿⣿⡿⠿⠛⠻⠟⢻⣿⣥⣀⣽⣷⡌⢻⣿
    ⣿⣿⣬⣭⣌⡙⠛⠿⣷⣶⣾⣿⣿⣿⠛⢛⣀⣬⣥⣤⣼⣿
    ⣿⣿⣿⣿⣿⣿⣄⠒⢶⣾⣿⣿⣿⣿⣧⡈⢿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡏⠐⢻⣿⣿⣿⣿⣿⣿⣧⠘⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿
    ''',
    'Creeper (Vlad)': '''
    ⠄⠄⠄⠄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀
    ⠄⠄⠄⠄⡍⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣭
    ⠄⠄⠄⠄⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
    ⠄⠄⠄⠄⡇⠄⢸⣿⣿⡇⠄⠄⠄⢸⣿⣿⣿⡇⠄⣿
    ⠄⠄⠄⠄⡇⠄⢸⣿⣿⡇⠄⠄⠄⢸⣿⣿⣿⡇⠄⣿
    ⠄⠄⠄⠄⡇⠄⠄⠄⣀⣀⣸⣿⣿⣀⣀⡀⠄⠄⠄⣿
    ⠄⠄⠄⠄⡇⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⣿
    ⠄⠄⠄⠄⡇⠄⠄⠄⣿⡿⠿⠿⠿⠿⣿⡇⠄⠄⠄⣿
    ⠄⠄⠄⠄⠇⠤⠤⠤⠭⠥⠤⠤⠤⠤⠭⠥⠤⠤⠤⠿
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸
    ⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⢸⡀
    ⠄⠄⠄⠄⠄⣸⢀⠄⠄⠄⠄⠄⠄⠄⠄⢸⠄⠄⠄⠸⢈⡡⠒
    ⠄⠄⠠⠔⠈⠁⠈⠙⠲⠦⣄⣀⠄⠄⠄⢸⠄⠄⣀⣴⠋⠄⢸
    ⠄⡍⠓⠦⣄⡀⠄⣠⠴⠃⠄⠈⠙⠓⠆⢘⡤⠚⠁⣿⠄⠄⢸
    ⠄⡇⠄⠄⠄⠈⡙⠲⢤⣀⡀⠄⠄⣠⠖⢫⡀⠄⠄⣿⠄⠄⠘
    ⠄⠇⠄⠄⠄⠄⡇⠄⠄⠄⠉⠓⠈⠁⠄⢸⣿⣷⣦⣬⢀⣴⠎
    ⠄⣶⣤⣀⠄⠄⡇⠄⠄⠄⠄⢸⠄⠄⠄⢘⡛⠿⣿⣿⠟⠁
    ⠄⠻⣿⣿⣿⣶⣅⡀⠄⠄⠄⢸⠄⠄⠄⢸⡇
    ⠄⠄⠈⠙⠻⢿⣿⣿⣷⣦⣄⡘⠄⠄⢀⡼⠃
    ⠄⠄⠄⠄⠄⠄⠉⠛⠿⣿⣿⣿⢀⡴⠋
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠻⠈
    ''',
    'Onda Andar': '''
        ⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠉⠁⠄⠄⠄⠄⠈⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠻⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⣿⣿⣿
        ⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿
        ⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿
        ⣿⣿⣿⣿⣇⠄⠄⠄⢀⣀⣀⣀⠄⠄⠄⠄⠄⢀⣀⣀⣀⡀⠄⠄⢠⣿⣿⣿
        ⣿⣿⣿⣿⣿⡄⠄⣼⣿⣿⣿⣿⣷⠄⠄⠄⢀⣿⣿⣿⣿⣿⠄⠄⣼⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠄⠹⣿⣿⣿⣿⠏⣰⣿⣷⡀⢿⣿⣿⣿⡿⠄⢸⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠄⠄⠉⠛⠛⠁⢠⣿⣿⣿⣷⠄⠙⠛⠋⠄⠄⢸⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣄⣀⡀⠄⠄⠄⠈⠛⠋⠙⠋⠄⠄⠄⠄⣀⣀⣸⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⡄⠄⢀⡀⣀⠄⠄⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣧⣿⣿⣟⣿⢸⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⡏⠿⢿⡿⣿⠛⠏⢿⠁⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠄⠈⠁⠄⠄⠄⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⡇⠄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⢻⣿⣿⣿⣿
        ⣿⣿⣿⣿⠁⠄⠄⠄⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠃⠄⠄⠸⣿⣿
        ⣿⣿⣿⣿⣧⣤⣶⣶⣶⣦⣄⠈⠙⠿⣿⣿⣿⡿⠟⠋⢁⣀⣀⣀⠄⢠⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⠄⠉⠁⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢉⣠⣴⣶⣶⣤⣌⡙⠻⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⡿⠟⢋⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣈⠙⠻⢿⣿⣿
        ⠟⠛⠛⠛⠋⣁⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠄⣷

        ⣿⣿⣿⣿⠄⣿⠄⠄⣿⠄⣿⣿⣿⠄⠄⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⠄⠄⣿⠄⠄⣿⠄⣿⣿⣿⠄⠄⠄⣿⣿⠄⠄⣿⣿⣿⠄
        ⣿⠄⠄⣿⠄⣿⣿⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⠄⠄⠄⠄⠄⣿⠄⠄⣿⠄⣿⣿⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿
        ⣿⠄⠄⣿⠄⣿⠄⣿⣿⠄⣿⠄⠄⣿⠄⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⠄⣿⠄⣿⣿⠄⣿⠄⠄⣿⠄⣿⣿⣿⣿⠄⣿⣿⣿⠄
        ⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⠄⠄⠄⠄⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⠄⣿⠄
        ⣿⣿⣿⣿⠄⣿⠄⠄⣿⠄⣿⣿⣿⠄⠄⣿⠄⠄⣿⠄⠄⠄⠄⠄⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿⠄⣿⣿⣿⠄⠄⣿⠄⠄⣿⠄⣿⠄⠄⣿
    ''',
    'Hello Kitty': '''
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⡀
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣠⣶⣿⣿⣿⣿⣦⡀
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣴⣿⣿⣿⣿⣿⣿⣿⣷
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣤⣤⣤⣄⡀
    ⠄⠄⠄⠄⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦
    ⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
    ⠄⠄⠄⢠⠔⠒⠴⡿⠟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠄⠄⠄⠸⡀⠄⡤⠤⡀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠄⠄⠄⣰⠁⠄⠳⠔⠁⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠄⠄⣴⣿⣦⣤⣶⣷⣦⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆
    ⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇
    ⢀⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
    ⢸⣿⣿⣿⣿⣿⠋⣡⣤⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠙⠿⣿⣿⣿⣿⣿⣿⡇
    ⠄⣿⣿⣿⣿⠁⠄⣿⣿⡇⠄⠄⠄⠄⣀⠄⠄⠄⠄⠄⣾⣿⡆⠘⣿⣿⣿⣿⣿⠃
    ⠄⠘⣿⣿⣿⠄⠄⠉⠋⠄⠄⠄⠄⠸⣍⡵⠄⠄⠄⠄⠻⡿⠇⠄⢸⣿⣿⣿⠏
    ⠄⠄⠈⠻⣿⣦⡀⠄⠄⠄⠄⠄⠄⠄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⣼⣿⡿⠋
    ⠄⠄⠄⠄⠄⠉⢻⣶⡶⠴⢲⣄⣀⣀⣁⠄⠄⠄⠄⣀⣀⣀⣤⠾⠟⠋
    ⠄⠄⠄⠄⠄⢶⣿⣿⠄⠄⠄⢹⣿⠋⠉⠙⣿⣿⣿⣿⣿⣿⣿⡆
    ⠄⠄⠄⠄⠄⠄⣼⠋⠄⠄⣴⣿⠏⠄⠄⠄⠹⣿⣿⣿⠿⢛⠉⢳⣀
    ⠄⠄⠄⠄⠄⠄⢻⣀⣀⡴⠃⠄⠄⠄⠄⠄⠄⠉⠉⠄⠄⢸⡄⠄⠈⢳
    ⠄⠄⠄⠄⠄⠄⠄⠈⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⡧⣄⣠⠞
    ⠄⠄⠄⠄⠄⠄⠄⠄⢹⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣾
    ⠄⠄⠄⠄⠄⠄⠄⠄⢸⠃⠄⢀⣤⣀⠄⣴⡄⣠⣤⡄⠄⠸⡇
    ⠄⠄⠄⠄⠄⠄⠄⠄⣼⠄⠄⠄⠄⠄⠈⣷⠋⠄⠄⠄⠄⠄⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⠙⢦⣀⣀⣀⣀⣠⠟⢤⣀⣀⣀⣀⡴⠃
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠉⠉⠉⠄⠄⠄⠈⠉⠉
    '''
}

CAT_BLINK = '''
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠙⢻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠃⠀⠀      ⢻⣿⣿⣿⣿⣿⡿⠀       ⢻⣿⣿⣏⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⠀⠀⠀⠀⠰⣿⣿⠀⢸⣿⣿⣿⣿⣿⡇⠀⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠙⠃⠀⣼⣿⣿⣿⣿⣿⣇⠀⠙⠛⠁⠀⠀⣼⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣷⣤⣄⣀⣠⣤⣾⣿⣿⣿⣿⣽⣿⣿⣦⣄⣀⣀⣤⣾⣿⣿⣿⣿⠃⠀⠀⢀⣀⠀⠀
        ⠰⡶⠶⠶⠶⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠉⠉⠙⠛⠋⠀
        ⠀⠀⢀⣀⣠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠷⠶⠶⠶⢤⣤⣀⠀
        ⠀⠛⠋⠉⠁⠀⣀⣴⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣤⣀⡀⠀⠀⠀⠀⠘⠃
        ⠀⠀⢀⣤⡶⠟⠉⠁⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠉⠙⠳⠶⣄⡀⠀⠀
        ⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

class DeviceInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(800, 580)
        self.current_theme = 'dark'
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(self.get_theme_style('dark'))
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(55)
        self.title_bar.setStyleSheet(self.get_title_bar_style('dark'))
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(20, 0, 15, 0)
        self.btn_back = QPushButton('<')
        self.btn_back.setFixedSize(32, 32)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setStyleSheet(self.get_button_back_style('dark'))
        self.btn_back.clicked.connect(self.on_back_clicked)
        self.btn_back.setVisible(False)
        title_layout.addWidget(self.btn_back)
        title_layout.addSpacing(5)
        self.btn_settings = QPushButton('⚙')
        self.btn_settings.setFixedSize(32, 32)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setStyleSheet(self.get_button_settings_style('dark'))
        self.btn_settings.clicked.connect(self.toggle_page)
        title_layout.addWidget(self.btn_settings)
        self.title_label = QLabel('CatChecker iPhone')
        self.title_label.setStyleSheet(self.get_title_style('dark'))
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        self.btn_minimize = QPushButton('─')
        self.btn_minimize.setFixedSize(32, 32)
        self.btn_minimize.setCursor(Qt.PointingHandCursor)
        self.btn_minimize.setStyleSheet(self.get_button_window_style('dark'))
        self.btn_minimize.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.btn_minimize)
        self.btn_close = QPushButton('✕')
        self.btn_close.setFixedSize(32, 32)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setStyleSheet(self.get_button_close_style('dark'))
        self.btn_close.clicked.connect(self.close)
        title_layout.addWidget(self.btn_close)
        self.title_bar.setLayout(title_layout)
        main_layout.addWidget(self.title_bar)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet('background-color: transparent;')
        self.page_info = QWidget()
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(10)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(self.get_scroll_area_style('dark'))
        self.scroll_area.setMinimumHeight(350)
        self.info_container = QWidget()
        self.info_container.setStyleSheet('background-color: transparent;')
        info_text_layout = QVBoxLayout()
        info_text_layout.setContentsMargins(20, 20, 20, 20)
        info_text_layout.setSpacing(2)
        self.label_info = QLabel('Ожидания запроса')
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setWordWrap(True)
        self.label_info.setStyleSheet(self.get_label_info_style('dark'))
        info_text_layout.addWidget(self.label_info)
        info_text_layout.addStretch(3)
        info_text_layout.addStretch(1)
        self.info_container.setLayout(info_text_layout)
        self.scroll_area.setWidget(self.info_container)
        info_cat_layout = QHBoxLayout()
        info_cat_layout.setSpacing(10)
        self.cat_container = QWidget()
        self.cat_container.setVisible(True)
        self.cat_container.setStyleSheet(self.get_cat_container_style('dark'))
        self.cat_container.setMinimumWidth(200)
        cat_layout = QVBoxLayout()
        cat_layout.setContentsMargins(5, 5, 5, 5)
        self.cat_label = QLabel()
        self.cat_label.setAlignment(Qt.AlignCenter)
        self.cat_label.setStyleSheet('background-color: transparent;')
        self.cat_label.setText(ARTS['Cat Checker'].replace('⣠⣄', '⣿⣿'))
        self.cat_label.setStyleSheet(self.get_cat_label_style('dark', 'Cat Checker'))
        cat_layout.addWidget(self.cat_label)
        self.cat_container.setLayout(cat_layout)
        info_cat_layout.addWidget(self.scroll_area, 1)
        info_cat_layout.addWidget(self.cat_container, 1)
        info_layout.addLayout(info_cat_layout)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.btn_get_info = QPushButton('Получить информацию')
        self.btn_get_info.setFixedHeight(40)
        self.btn_get_info.setCursor(Qt.PointingHandCursor)
        self.btn_get_info.setStyleSheet(self.get_main_button_style('dark'))
        self.btn_get_info.clicked.connect(self.get_full_device_info)
        button_layout.addWidget(self.btn_get_info)
        self.btn_copy_device_data = QPushButton('Скопировать данные устройства')
        self.btn_copy_device_data.setFixedHeight(40)
        self.btn_copy_device_data.setCursor(Qt.PointingHandCursor)
        self.btn_copy_device_data.setVisible(False)
        self.btn_copy_device_data.setStyleSheet(self.get_copy_button_style('dark'))
        self.btn_copy_device_data.clicked.connect(self.copy_all_device_data)
        button_layout.addWidget(self.btn_copy_device_data)
        info_layout.addLayout(button_layout)
        self.page_info.setLayout(info_layout)
        self.stacked_widget.addWidget(self.page_info)
        self.current_art = 'Cat Checker'
        self.current_gif_path = None
        self.current_movie = None
        self._loading_state = False
        appdata_dir = os.path.join(os.environ['LOCALAPPDATA'], 'CatChecker')
        os.makedirs(appdata_dir, exist_ok=True)
        self.art_unlocked_file = os.path.join(appdata_dir, '.art_unlocked')
        self.settings_file = os.path.join(appdata_dir, 'settings.json')
        if os.path.exists(self.art_unlocked_file):
            try:
                with open(self.art_unlocked_file, 'r') as f:
                    self.art_unlocked = f.read().strip() == ART_UNLOCK_TOKEN
            except Exception:
                self.art_unlocked = False
        else:
            self.art_unlocked = False
        self.page_settings = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_title = QLabel('Настройки')
        settings_title.setStyleSheet(self.get_settings_title_style('dark'))
        settings_layout.addWidget(settings_title)
        self.theme_toggle_btn = QPushButton('Переключить на светлую тему')
        self.theme_toggle_btn.setFixedHeight(40)
        self.theme_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.theme_toggle_btn.setStyleSheet(self.get_theme_toggle_style('dark'))
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        settings_layout.addWidget(self.theme_toggle_btn)
        self.art_toggle_btn = QPushButton('▶ Сменить арт на табе')
        self.art_toggle_btn.setFixedHeight(40)
        self.art_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.art_toggle_btn.setStyleSheet(self.get_theme_toggle_style('dark'))
        self.art_toggle_btn.clicked.connect(self.toggle_art_section)
        settings_layout.addWidget(self.art_toggle_btn)
        self.art_container = QWidget()
        self.art_container.setVisible(False)
        art_layout = QVBoxLayout()
        art_layout.setContentsMargins(10, 5, 10, 5)
        art_layout.setSpacing(5)
        self.art_buttons = {}
        for art_name in ARTS:
            btn = QPushButton(art_name)
            btn.setFixedHeight(32)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self.get_art_option_style('dark', art_name == self.current_art))
            btn.clicked.connect(lambda checked, name=art_name: self.select_art(name))
            art_layout.addWidget(btn)
            self.art_buttons[art_name] = btn
        self.art_container.setLayout(art_layout)
        settings_layout.addWidget(self.art_container)
        self.animate_btn = QPushButton('▶ Оживить арт на табе (Beta)')
        self.animate_btn.setFixedHeight(40)
        self.animate_btn.setCursor(Qt.PointingHandCursor)
        self.animate_btn.setStyleSheet(self.get_theme_toggle_style('dark'))
        self.animate_btn.clicked.connect(self.toggle_animation)
        settings_layout.addWidget(self.animate_btn)
        self.animation_on = False
        self.btn_live_cat = QPushButton('Cat Checker (live)')
        self.btn_live_cat.setFixedHeight(32)
        self.btn_live_cat.setCursor(Qt.PointingHandCursor)
        self.btn_live_cat.setStyleSheet(self.get_art_option_style('dark', False))
        self.btn_live_cat.clicked.connect(self.toggle_live_cat)
        self.btn_live_cat.setVisible(False)
        settings_layout.addWidget(self.btn_live_cat)
        self.gif_btn = QPushButton('▶ Разместить свой GIF на табе')
        self.gif_btn.setFixedHeight(40)
        self.gif_btn.setCursor(Qt.PointingHandCursor)
        self.gif_btn.setStyleSheet(self.get_theme_toggle_style('dark'))
        self.gif_btn.clicked.connect(self.select_gif)
        settings_layout.addWidget(self.gif_btn)
        self.anim_is_blinking = False
        settings_layout.addStretch()
        self.page_settings.setLayout(settings_layout)
        self.stacked_widget.addWidget(self.page_settings)
        main_layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(main_layout)
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse_buttons)
        self.pulse_value = 0
        self.pulse_timer.start(30)
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.typewriter_tick)
        self.typewriter_buffer = ''
        self.typewriter_index = 0
        self.drag_position = None
        self.title_bar.mousePressEvent = self.mousePressEvent
        self.title_bar.mouseMoveEvent = self.mouseMoveEvent
        self.current_info = None
        self.is_fetching = False
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.update_dots)
        self.dot_count = 0
        self.base_text = 'Ожидания запроса'
        self.dot_timer.start(500)
        self.previous_page = self.page_info
        self.device_check_timer = QTimer()
        self.device_check_timer.timeout.connect(self.check_for_device)
        self.device_check_timer.start(2000)
        for btn in self.findChildren(QPushButton):
            btn.setFocusPolicy(Qt.NoFocus)
        self._load_state()

    def pulse_buttons(self):
        self.pulse_value = (self.pulse_value + 1) % 100
        brightness = 200 + int(55 * math.sin(self.pulse_value * math.pi / 50))
        r, g, b = (brightness, brightness, brightness)
        self.btn_get_info.setStyleSheet(f'''
            QPushButton {{
                background-color: rgb({r}, {g}, {b});
                color: #000000;
                border: 2px solid rgb({min(255, r + 50)}, {min(255, g + 50)}, {min(255, b + 50)});
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #e6e6e6;
            }}
            QPushButton:pressed {{
                background-color: #cccccc;
            }}
        ''')

    def typewriter_start(self, text):
        self.typewriter_buffer = text
        self.typewriter_index = 0
        self.label_info.setText('')
        self.typewriter_timer.start(5)

    def typewriter_tick(self):
        if self.typewriter_index < len(self.typewriter_buffer):
            chunk_size = random.randint(3, 6)
            end = min(self.typewriter_index + chunk_size, len(self.typewriter_buffer))
            self.label_info.setText(self.typewriter_buffer[:end])
            self.typewriter_index = end
        else:
            self.typewriter_timer.stop()

    def typewriter_finish(self):
        if self.typewriter_timer.isActive():
            self.typewriter_timer.stop()
            if self.typewriter_buffer:
                self.label_info.setText(self.typewriter_buffer)
                self.typewriter_index = len(self.typewriter_buffer)

    def switch_page(self, target_page, show_back=True):
        if self.stacked_widget.currentWidget() == target_page:
            return
        else:
            self.stacked_widget.setCurrentWidget(target_page)
            self.btn_back.setVisible(show_back and target_page != self.page_info)

    def toggle_page(self):
        if self.stacked_widget.currentWidget() == self.page_info:
            self.typewriter_finish()
            self.previous_page = self.stacked_widget.currentWidget()
            self.switch_page(self.page_settings, True)

    def on_back_clicked(self):
        if self.stacked_widget.currentWidget() == self.page_settings:
            self.typewriter_finish()
            show_back = self.previous_page != self.page_info or self.current_info is not None
            self.switch_page(self.previous_page, show_back)
        else:
            self.reset_to_waiting()

    def toggle_art_section(self):
        if not self.art_unlocked:
            if self.show_password_dialog():
                self.art_unlocked = True
                with open(self.art_unlocked_file, 'w') as f:
                    f.write(ART_UNLOCK_TOKEN)
                self.art_toggle_btn.setText('▶ Сменить арт на табе')
                self.art_toggle_btn.setStyleSheet(self.get_theme_toggle_style(self.current_theme))
            else:
                return None
        expanded = self.art_container.isVisible()
        self.art_container.setVisible(not expanded)
        self.art_toggle_btn.setText(f"{('▼' if not expanded else '▶')} Сменить арт на табе")

    def show_password_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowFlag(Qt.FramelessWindowHint, True)
        if self.current_theme == 'dark':
            dialog.setStyleSheet('''
                QDialog { background-color: #1a1a1a; color: #ffffff; }
                QLabel { color: #ffffff; font-size: 13px; }
                QLineEdit { background-color: #2a2a2a; color: #ffffff; border: 1px solid #3a3a3a; padding: 5px; font-size: 13px; }
                QPushButton { background-color: #000000; color: #ffffff; border: none; padding: 6px 20px; font-size: 13px; font-weight: bold; }
                QPushButton:hover { background-color: #333333; }
            ''')
        else:
            dialog.setStyleSheet('''
                QDialog { background-color: #f5f5f5; color: #000000; }
                QLabel { color: #000000; font-size: 13px; }
                QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #cccccc; padding: 5px; font-size: 13px; }
                QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #cccccc; padding: 6px 20px; font-size: 13px; font-weight: bold; }
                QPushButton:hover { background-color: #f0f0f0; }
            ''')
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 10, 20, 15)
        title_bg = '#000000' if self.current_theme == 'dark' else '#ffffff'
        title_color = '#ffffff' if self.current_theme == 'dark' else '#000000'
        title_bar = QLabel('Функция недоступна')
        title_bar.setAlignment(Qt.AlignCenter)
        title_bar.setStyleSheet(f'background-color: {title_bg}; color: {title_color}; font-size: 14px; font-weight: bold; padding: 6px;')
        layout.addWidget(title_bar)
        label = QLabel('Введите пароль:')
        layout.addWidget(label)
        input_field = QLineEdit()
        input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(input_field)
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton('OK')
        btn_cancel = QPushButton('Отмена')
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)
        input_field.returnPressed.connect(dialog.accept)
        dialog.setFixedSize(320, 170)
        result = dialog.exec()
        if result == QDialog.Accepted and input_field.text() == 'CatChecker_ArtTab':
            return True
        else:
            return False

    def select_art(self, name):
        self._stop_gif()
        self.current_art = name
        if self.animation_on:
            self.animation_on = False
            self.anim_is_blinking = False
            self.btn_live_cat.setVisible(False)
            self.animate_btn.setText('▶ Оживить арт на табе (Beta)')
            self.btn_live_cat.setStyleSheet(self.get_art_option_style(self.current_theme, False))
        art_text = ARTS[name].replace('⣠⣄', '⣿⣿') if name == 'Cat Checker' else ARTS[name]
        self.cat_label.setText(art_text)
        self.cat_label.setStyleSheet(self.get_cat_label_style(self.current_theme, name))
        self.art_toggle_btn.setText('▶ Сменить арт на табе')
        self.art_container.setVisible(False)
        theme = self.current_theme
        for art_name, btn in self.art_buttons.items():
            btn.setStyleSheet(self.get_art_option_style(theme, art_name == name))
        self.btn_back.setVisible(self.stacked_widget.currentWidget() == self.page_settings)
        if not self._loading_state:
            self._save_state()

    def toggle_animation(self):
        if not self.art_unlocked:
            if self.show_password_dialog():
                self.art_unlocked = True
                with open(self.art_unlocked_file, 'w') as f:
                    f.write(ART_UNLOCK_TOKEN)
                self.art_toggle_btn.setText('▶ Сменить арт на табе')
                self.art_toggle_btn.setStyleSheet(self.get_theme_toggle_style(self.current_theme))
            else:
                return None
        visible = self.btn_live_cat.isVisible()
        self.btn_live_cat.setVisible(not visible)
        self.animate_btn.setText(f"{('▼' if not visible else '▶')} Оживить арт на табе (Beta)")

    def _save_state(self):
        data = {'theme': self.current_theme, 'mode': 'art', 'art_name': 'Cat Checker', 'gif_path': None}
        if self.animation_on and self.current_art == 'Cat Checker':
            data['mode'] = 'live'
            data['art_name'] = 'Cat Checker'
        else:
            if self.current_art is None and hasattr(self, 'current_movie') and self.current_movie:
                data['mode'] = 'gif'
                data['gif_path'] = self.current_gif_path if hasattr(self, 'current_gif_path') and self.current_gif_path else ''
            else:
                data['mode'] = 'art'
                data['art_name'] = self.current_art if self.current_art else 'Cat Checker'
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass

    def _load_state(self):
        if not os.path.exists(self.settings_file):
            return
        else:
            self._loading_state = True
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                theme = data.get('theme', 'dark')
                if theme != self.current_theme:
                    self.toggle_theme()
                mode = data.get('mode', 'art')
                if mode == 'gif':
                    gif_path = data.get('gif_path', '')
                    if gif_path and os.path.exists(gif_path):
                            self._apply_gif_direct(gif_path)
                else:
                    if mode == 'live':
                        self.select_art('Cat Checker')
                        self.animation_on = True
                        self.btn_live_cat.setStyleSheet(self.get_art_option_style(self.current_theme, True))
                        self._blink_close()
                    else:
                        art_name = data.get('art_name', 'Cat Checker')
                        if art_name in ARTS:
                            self.select_art(art_name)
            except Exception:
                pass
            finally:
                self._loading_state = False

    def _apply_gif_direct(self, gif_path):
        self._stop_gif()
        self.current_art = None
        self.current_gif_path = gif_path
        movie = QMovie(gif_path)
        movie.setCacheMode(QMovie.CacheAll)
        frame = movie.currentPixmap()
        if not frame.isNull():
            movie.setScaledSize(frame.size().scaled(300, 300, Qt.KeepAspectRatio))
        self.cat_label.setMovie(movie)
        self.cat_label.setStyleSheet('background-color: transparent;')
        movie.start()
        self.current_movie = movie

    def _stop_gif(self):
        if hasattr(self, 'current_movie') and self.current_movie:
                self.current_movie.stop()
                self.cat_label.setMovie(None)
                self.current_movie.deleteLater()
                self.current_movie = None
        self.cat_label.setScaledContents(False)

    def select_gif(self):
        if not self.art_unlocked:
            if self.show_password_dialog():
                self.art_unlocked = True
                with open(self.art_unlocked_file, 'w') as f:
                    f.write(ART_UNLOCK_TOKEN)
                self.art_toggle_btn.setText('▶ Сменить арт на табе')
                self.art_toggle_btn.setStyleSheet(self.get_theme_toggle_style(self.current_theme))
            else:
                return None
        if self.animation_on:
            self.animation_on = False
            self.anim_is_blinking = False
            self.btn_live_cat.setVisible(False)
            self.animate_btn.setText('▶ Оживить арт на табе (Beta)')
            self.btn_live_cat.setStyleSheet(self.get_art_option_style(self.current_theme, False))
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите GIF-файл', os.path.join(os.path.expanduser('~'), 'Downloads'), 'GIF (*.gif)')
        if not file_path:
            return
        else:
            self._apply_gif_direct(file_path)
            self.btn_back.setVisible(self.stacked_widget.currentWidget() == self.page_settings)
            if not self._loading_state:
                self._save_state()

    def toggle_live_cat(self):
        if self.animation_on:
            if self.anim_is_blinking:
                self.cat_label.setText(ARTS['Cat Checker'].replace('⣠⣄', '⣿⣿'))
                self.anim_is_blinking = False
            self.animation_on = False
            self.btn_live_cat.setStyleSheet(self.get_art_option_style(self.current_theme, False))
        else:
            self._stop_gif()
            if self.current_art != 'Cat Checker':
                self.current_art = 'Cat Checker'
                self.cat_label.setText(ARTS['Cat Checker'].replace('⣠⣄', '⣿⣿'))
                self.cat_label.setStyleSheet(self.get_cat_label_style(self.current_theme, 'Cat Checker'))
                self.art_toggle_btn.setText('▶ Сменить арт на табе')
                self.art_container.setVisible(False)
                theme = self.current_theme
                for art_name, btn in self.art_buttons.items():
                    btn.setStyleSheet(self.get_art_option_style(theme, art_name == 'Cat Checker'))
            self.animation_on = True
            self.btn_live_cat.setStyleSheet(self.get_art_option_style(self.current_theme, True))
            self._blink_close()
        self.btn_live_cat.setVisible(False)
        self.animate_btn.setText('▶ Оживить арт на табе (Beta)')
        self.btn_back.setVisible(self.stacked_widget.currentWidget() == self.page_settings)
        if not self._loading_state:
            self._save_state()

    def _blink_close(self):
        if not self.animation_on or self.current_art != 'Cat Checker':
            return None
        else:
            self.anim_is_blinking = True
            few = ARTS['Cat Checker'].replace('⣠⣄', '⣀⣀')
            self.cat_label.setText(few)
            QTimer.singleShot(100, self._blink_close_full)

    def _blink_close_full(self):
        if not self.animation_on:
            return
        else:
            self.cat_label.setText(CAT_BLINK)
            QTimer.singleShot(100, self._blink_open)

    def _blink_open(self):
        if not self.animation_on:
            return
        else:
            few = ARTS['Cat Checker'].replace('⣠⣄', '⣀⣀')
            self.cat_label.setText(few)
            QTimer.singleShot(100, self._blink_open_full)

    def _blink_open_full(self):
        if not self.animation_on:
            return
        else:
            self.cat_label.setText(ARTS['Cat Checker'].replace('⣠⣄', '⣿⣿'))
            self.anim_is_blinking = False
            QTimer.singleShot(3000, self._blink_close)

    def get_art_option_style(self, theme, selected):
        if selected:
            bg = '#ffffff'
            hover = '#e6e6e6'
            color = '#000000'
            hover_color = '#000000'
        else:
            bg = '#1a1a1a' if theme == 'dark' else '#e0e0e0'
            hover = '#2a2a2a' if theme == 'dark' else '#d0d0d0'
            color = '#ffffff' if theme == 'dark' else '#000000'
            hover_color = '#ffffff' if theme == 'dark' else '#000000'
        return f'''
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: 1px solid #3a3a3a;
                font-size: 13px;
                text-align: left;
                padding-left: 15px;
            }}
            QPushButton:hover {{
                background-color: {hover};
                color: {hover_color};
            }}
        '''

    def reset_to_waiting(self):
        self.typewriter_finish()
        self.dot_count = 0
        self.dot_timer.start(500)
        self.base_text = 'Ожидания запроса'
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setText('Ожидания запроса')
        self.current_info = None
        self.btn_copy_device_data.setVisible(False)
        self.btn_back.setVisible(False)

    def toggle_theme(self):
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_toggle_btn.setText('Переключить на тёмную тему')
        else:
            self.current_theme = 'dark'
            self.theme_toggle_btn.setText('Переключить на светлую тему')
        self.apply_theme(self.current_theme)
        if not self._loading_state:
            self._save_state()

    def apply_theme(self, theme):
        self.central_widget.setStyleSheet(self.get_theme_style(theme))
        self.title_bar.setStyleSheet(self.get_title_bar_style(theme))
        self.title_label.setStyleSheet(self.get_title_style(theme))
        self.btn_settings.setStyleSheet(self.get_button_settings_style(theme))
        self.btn_back.setStyleSheet(self.get_button_back_style(theme))
        self.btn_minimize.setStyleSheet(self.get_button_window_style(theme))
        self.btn_close.setStyleSheet(self.get_button_close_style(theme))
        self.scroll_area.setStyleSheet(self.get_scroll_area_style(theme))
        self.label_info.setStyleSheet(self.get_label_info_style(theme))
        self.cat_container.setStyleSheet(self.get_cat_container_style(theme))
        self.cat_label.setStyleSheet(self.get_cat_label_style(theme, self.current_art))
        self.btn_get_info.setStyleSheet(self.get_main_button_style(theme))
        self.btn_copy_device_data.setStyleSheet(self.get_copy_button_style(theme))
        self.theme_toggle_btn.setStyleSheet(self.get_theme_toggle_style(theme))
        self.art_toggle_btn.setStyleSheet(self.get_theme_toggle_style(theme))
        self.animate_btn.setStyleSheet(self.get_theme_toggle_style(theme))
        self.gif_btn.setStyleSheet(self.get_theme_toggle_style(theme))
        self.btn_live_cat.setStyleSheet(self.get_art_option_style(theme, self.animation_on))
        for art_name, btn in self.art_buttons.items():
            btn.setStyleSheet(self.get_art_option_style(theme, art_name == self.current_art))
        settings_title = self.page_settings.findChild(QLabel)
        if settings_title:
            settings_title.setStyleSheet(self.get_settings_title_style(theme))

    def get_theme_style(self, theme):
        if theme == 'dark':
            return 'QWidget { background-color: #0a0a0a; border: 1px solid #1a1a1a; }'
        else:
            return 'QWidget { background-color: #f0f0f0; border: 1px solid #cccccc; }'

    def get_title_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        return f'color: {color}; font-size: 17px; font-weight: bold; background-color: transparent; border: none;'

    def get_title_bar_style(self, theme):
        bg = '#000000' if theme == 'dark' else '#ffffff'
        return f'background-color: {bg}; border: none;'

    def get_button_settings_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        hover = '#555555' if theme == 'dark' else '#333333'
        return f'''
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: none;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {hover};
            }}
        '''

    def get_button_back_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        return f'''
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: none;
                font-size: 18px;
                font-weight: bold;
            }}
        '''

    def get_button_window_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        hover_bg = '#333333' if theme == 'dark' else '#cccccc'
        return f'''
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: none;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                color: {color};
            }}
        '''

    def get_button_close_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        return f'''
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #cc0000;
                color: #ffffff;
            }}
        '''

    def get_scroll_area_style(self, theme):
        if theme == 'dark':
            return '''
                QScrollArea {
                    background-color: #0d0d0d;
                    border: 2px solid #2a2a2a;
                }
                QScrollBar:vertical {
                    background-color: #0d0d0d;
                    width: 10px;
                    margin: 2px;
                }
                QScrollBar::handle:vertical {
                    background-color: #2a2a2a;
                    min-height: 30px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #3a3a3a;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            '''
        else:
            return '''
                QScrollArea {
                    background-color: #f5f5f5;
                    border: 2px solid #cccccc;
                }
                QScrollBar:vertical {
                    background-color: #f5f5f5;
                    width: 10px;
                    margin: 2px;
                }
                QScrollBar::handle:vertical {
                    background-color: #cccccc;
                    min-height: 30px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #bbbbbb;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            '''

    def get_label_info_style(self, theme):
        color = '#aaaaaa' if theme == 'dark' else '#333333'
        return f'''
            color: {color};
            font-size: 13px;
            background-color: transparent;
            font-family: 'Segoe UI', 'Consolas', monospace;
            line-height: 1.8;
            padding: 5px;
            border: none;
        '''

    def get_cat_container_style(self, theme):
        bg = '#0d0d0d' if theme == 'dark' else '#f5f5f5'
        border = '#1a1a1a' if theme == 'dark' else '#cccccc'
        return f'background-color: {bg}; border: 1px solid {border};'

    def get_cat_label_style(self, theme, art_name=None):
        color = '#ffffff' if theme == 'dark' else '#000000'
        size = '17px' if art_name == 'Femboy' else '14px' if art_name == 'Creeper (Vlad)' else '13px' if art_name == 'Anime Tyanka' else '10px'
        return f'''
            color: {color};
            font-size: {size};
            font-family: 'Consolas', monospace;
            background-color: transparent;
            line-height: 1.0;
        '''

    def get_main_button_style(self, theme):
        if theme == 'dark':
            return '''
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: none;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                QPushButton:pressed {
                    background-color: #cccccc;
                }
            '''
        else:
            return '''
                QPushButton {
                    background-color: #333333;
                    color: #ffffff;
                    border: none;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #222222;
                }
            '''

    def get_copy_button_style(self, theme):
        if theme == 'dark':
            return '''
                QPushButton {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: none;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QPushButton:pressed {
                    background-color: #1a1a1a;
                }
            '''
        else:
            return '''
                QPushButton {
                    background-color: #d0d0d0;
                    color: #000000;
                    border: none;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0c0c0;
                }
                QPushButton:pressed {
                    background-color: #b0b0b0;
                }
            '''

    def get_theme_toggle_style(self, theme):
        if theme == 'dark':
            return '''
                QPushButton {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: 1px solid #444444;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            '''
        else:
            return '''
                QPushButton {
                    background-color: #d0d0d0;
                    color: #000000;
                    border: 1px solid #aaaaaa;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0c0c0;
                }
            '''

    def get_settings_title_style(self, theme):
        color = '#ffffff' if theme == 'dark' else '#000000'
        return f'color: {color}; font-size: 20px; font-weight: bold;'

    def update_dots(self):
        dots = '.' * (self.dot_count % 4)
        self.label_info.setText(f'{self.base_text}{dots}')
        self.dot_count += 1

    def check_for_device(self):
        if self.is_fetching:
            return
        if self.stacked_widget.currentWidget() != self.page_info:
            return
            
        try:
            lockdown = create_using_usbmux()
            lockdown.close()
            if self.current_info is None:
                self.is_fetching = True
                try:
                    self.get_full_device_info()
                finally:
                    self.is_fetching = False
        except NoDeviceConnectedError:
            if self.current_info is not None:
                self.reset_to_waiting()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
                self.move(event.globalPosition().toPoint() - self.drag_position)
                event.accept()

    def copy_all_device_data(self):
        if self.current_info is None:
            self.label_info.setText(self.label_info.text() + '\n\n⚠️ Сначала получите информацию об устройстве!')
            return
        else:
            try:
                copy_text = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                copy_text += '            ИНФОРМАЦИЯ ОБ УСТРОЙСТВЕ          \n'
                copy_text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                copy_text += f"  Имя: {self.current_info['DeviceName']}\n"
                copy_text += f"  Модель: {self.current_info['ProductType']}\n"
                copy_text += f"  iOS: {self.current_info['ProductVersion']} (Build: {self.current_info['BuildVersion']})\n"
                copy_text += f"  Серийный номер: {self.current_info['SerialNumber']}\n"
                copy_text += f"  IMEI: {self.current_info['InternationalMobileEquipmentIdentity']}\n"
                copy_text += f"  Активация: {self.current_info['ActivationState']}\n"
                copy_text += f"  Номер телефона: {self.current_info['PhoneNumber']}\n"
                copy_text += '\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\n'
                copy_text += f"  Номер модели: {self.current_info['ModelNumber']}\n"
                copy_text += f"  Архитектура: {self.current_info['CPUArchitecture']}\n"
                copy_text += f"  Класс: {self.current_info['DeviceClass']}\n"
                copy_text += f"  Регион: {self.current_info['RegionInfo']}\n"
                copy_text += f"  Язык: {self.current_info['UserLanguage']}\n"
                copy_text += f"  Часовой пояс: {self.current_info['TimeZone']}\n"
                copy_text += f"  ICCID: {self.current_info['IntegratedCircuitCardIdentity']}\n"
                copy_text += f"  UDID: {self.current_info['UniqueDeviceID']}\n"
                if self.current_info['TotalDataCapacity'] != 'Unknown':
                    try:
                        capacity_gb = int(self.current_info['TotalDataCapacity']) / 1073741824
                        available_gb = int(self.current_info['TotalDataAvailable']) / 1073741824
                        copy_text += f'\n  💾 Хранилище:     {capacity_gb:.1f} GB (Доступно: {available_gb:.1f} GB)\n'
                    except:
                        pass
                copy_text += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                clipboard = QApplication.clipboard()
                clipboard.setText(copy_text)
                current_text = self.label_info.text()
                self.label_info.setText(current_text + '\n\n✅ Все данные скопированы в буфер обмена!')
                QTimer.singleShot(2000, lambda: self.label_info.setText(current_text))
            except Exception as e:
                self.label_info.setText(self.label_info.text() + f'\n\n❌ Ошибка копирования: {str(e)}')

    def get_phone_number_via_idevice(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            result = subprocess.run(['ideviceinfo', '-k', 'PhoneNumber'], capture_output=True, text=True, timeout=3, startupinfo=startupinfo)
            output = result.stdout.strip()
            if output and output != '':
                return output
            else:
                result = subprocess.run(['ideviceinfo', '-k', 'PhoneNumber', '-d', 'com.apple.commcenter'], capture_output=True, text=True, timeout=3, startupinfo=startupinfo)
                output = result.stdout.strip()
                if output and output != '':
                    return output
                else:
                    possible_keys = [('PhoneNumber', None), ('PhoneNumber', 'com.apple.commcenter'), ('MSISDN', None), ('SubscriberNumber', None)]
                    for key, domain in possible_keys:
                        cmd = ['ideviceinfo', '-k', key]
                        if domain:
                            cmd.extend(['-d', domain])
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3, startupinfo=startupinfo)
                        output = result.stdout.strip()
                        if output and output != '' and not output.startswith('Could not'):
                            return output
        except Exception:
            return None
        return None

    def get_full_device_info(self) -> Optional[dict]:
        try:
            self.typewriter_finish()
            self.dot_timer.stop()
            self.cat_container.setVisible(True)
            self.btn_copy_device_data.setVisible(True)
            lockdown = create_using_usbmux()
            values = lockdown.all_values
            phone_number = 'Неизвестно'
            number = self.get_phone_number_via_idevice()
            if number is not None and number != '':
                phone_number = number
            else:
                try:
                    if 'PhoneNumber' in values:
                        phone_number = values['PhoneNumber']
                    else:
                        if 'MSISDN' in values:
                            phone_number = values['MSISDN']
                        else:
                            try:
                                phone_number = lockdown.get_value('com.apple.commcenter', 'PhoneNumber')
                                if not phone_number:
                                    phone_number = lockdown.get_value('com.apple.phone', 'PhoneNumber')
                            except:
                                pass
                except:
                    pass
            info = {'DeviceName': values.get('DeviceName', 'Unknown'), 'ProductType': values.get('ProductType', 'Unknown'), 'ProductVersion': values.get('ProductVersion', 'Unknown'), 'BuildVersion': values.get('BuildVersion', 'Unknown'), 'SerialNumber': values.get('SerialNumber', 'Unknown'), 'UniqueDeviceID': values.get('UniqueDeviceID', 'Unknown'), 'ActivationState': values.get('ActivationState', 'Unknown'), 'TotalDataCapacity': values.get('TotalDataCapacity', 'Unknown'), 'TotalDataAvailable': values.get('TotalDataAvailable', 'Unknown'), 'RegionInfo': values.get('RegionInfo', 'Unknown'), 'UserLanguage': values.get('UserLanguage', 'Unknown'), 'DeviceClass': values.get('DeviceClass', 'Unknown'), 'PhoneNumber': phone_number}
            lockdown.close()
            self.current_info = info
            info_text = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            info_text += '            ИНФОРМАЦИЯ ОБ УСТРОЙСТВЕ          \n'
            info_text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
            info_text += f"  Имя: {info['DeviceName']}\n"
            info_text += f"  Модель: {info['ProductType']}\n"
            info_text += f"  iOS: {info['ProductVersion']} (Build: {info['BuildVersion']})\n"
            info_text += f"  Серийный номер: {info['SerialNumber']}\n"
            info_text += f"  IMEI: {info['InternationalMobileEquipmentIdentity']}\n"
            info_text += f"  Активация: {info['ActivationState']}\n"
            info_text += f"  Номер телефона: {info['PhoneNumber']}\n"
            info_text += '\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\n'
            info_text += f"  Номер модели: {info['ModelNumber']}\n"
            info_text += f"  Архитектура: {info['CPUArchitecture']}\n"
            info_text += f"  Класс: {info['DeviceClass']}\n"
            info_text += f"  Регион: {info['RegionInfo']}\n"
            info_text += f"  Язык: {info['UserLanguage']}\n"
            info_text += f"  Часовой пояс: {info['TimeZone']}\n"
            info_text += f"  ICCID: {info['IntegratedCircuitCardIdentity']}\n"
            info_text += f"  UDID: {info['UniqueDeviceID']}\n"
            if info['TotalDataCapacity'] != 'Unknown':
                try:
                    capacity_gb = int(info['TotalDataCapacity']) / 1073741824
                    available_gb = int(info['TotalDataAvailable']) / 1073741824
                    info_text += f'\n  💾 Хранилище:     {capacity_gb:.1f} GB (Доступно: {available_gb:.1f} GB)\n'
                except:
                    pass
            info_text += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            self.label_info.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.scroll_area.verticalScrollBar().setValue(0)
            self.typewriter_start(info_text)
            return info
        except NoDeviceConnectedError:
            self.dot_timer.start(500)
            error_msg = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            error_msg += 'УСТРОЙСТВО НЕ ПОДКЛЮЧЕНО!\n'
            error_msg += 'Подключите iPhone/iPad через USB\n'
            error_msg += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            self.label_info.setAlignment(Qt.AlignCenter)
            self.current_info = None
            self.btn_copy_device_data.setVisible(False)
            self.typewriter_start(error_msg)
            QTimer.singleShot(7000, self.reset_to_waiting)
            return None
        except Exception as e:
            self.dot_timer.start(500)
            error_msg = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            error_msg += f'ОШИБКА: {str(e)[:40]}\n'
            error_msg += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            self.label_info.setAlignment(Qt.AlignCenter)
            self.current_info = None
            self.btn_copy_device_data.setVisible(False)
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_PATH))
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('catchecker.iphone.1')
    except Exception:
        pass
    window = DeviceInfoApp()
    window.show()
    sys.exit(app.exec())