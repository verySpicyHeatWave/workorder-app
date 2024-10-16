from lib.forms.main_form import MainWindow
main: MainWindow = MainWindow()
main.mainloop()


#BCOBB: Refactor every method, field, and variable to use an_underscoring_naming_convention rather than camelCaseWhichIThinkIsWorse
#BCOBB: Now I'm in charge of scheduling. This app now needs to manage completion and due dates. Changes that need to be made to support this include:
#   Tracking all of the systems and their routine tasks and the time between their required execution
#   Generating new TWOIS requests for routine tasks based on the date of completion of prior events
#   Add log comments at the end of the form in the "Close Work Order" section