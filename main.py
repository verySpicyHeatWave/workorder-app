#pylint: skip-file

from appfiles.forms.mainwindow import MainWindow
import customtkinter as ctk             #type: ignore

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

main = MainWindow()
main.mainloop()