"""Yo!"""

import customtkinter as ctk #type: ignore

class ConfigurationFrame(ctk.CTkFrame):
    """Yo!"""
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame):
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.tabview: ctk.CTkTabview = ctk.CTkTabview(self)

        self.tabview.add('Tab1')
        self.tabview.tab('Tab1').grid_columnconfigure(0, weight=1)
        self.tabview.tab('Tab1').grid_rowconfigure(0, weight=1)

        self.tabview.add('Tab2')
        self.tabview.tab('Tab2').grid_columnconfigure(0, weight=1)
        self.tabview.tab('Tab2').grid_rowconfigure(0, weight=1)

        self.tabview.add('Tab3')
        self.tabview.tab('Tab3').grid_columnconfigure(0, weight=1)
        self.tabview.tab('Tab3').grid_rowconfigure(0, weight=1)

        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
