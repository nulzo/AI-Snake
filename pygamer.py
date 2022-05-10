from StartWindow import *
from main_menu import *

startup = Game()

while startup.running:
    startup.current_menu.display_menu()
    startup.game_loop()
