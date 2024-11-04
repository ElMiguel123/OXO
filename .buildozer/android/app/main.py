from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import platform
import random

# Register a custom font
LabelBase.register(name="8bit", fn_regular="8bit.ttf")

# Define the Main Menu screen
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Dynamic font size based on screen size
        self.title_font_size = min(Window.width, Window.height) * 0.1

        # Title of the game
        title = Label(text='[b]OXO[/b]', markup=True, font_size=self.title_font_size, halign='center', color=(1, 1, 0, 1))
        layout.add_widget(title)

        # Define menu buttons with actions
        buttons = [
            ("vs CPU 3x3", self.start_game_vs_cpu),
            ("Two players", self.start_two_player_game),
            ("Match", self.placeholder),
            ("Instructions", self.show_instructions),
            ("Donation si vous voulez", self.placeholder),
            ("Quitter", self.quit_app)
        ]
        for text, action in buttons:
            button = Button(text=text, size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
            button.bind(on_release=action)
            layout.add_widget(button)

        # Scrolling message
        self.marquee_text = Label(
            text=("(c) ByteRoots Studio - 2024 - release 0.1 - ce jeu est gratuit et ne contient pas de pub - "
                  "Des améliorations suivront au fur et à mesure de mon propre apprentissage - belle journée à vous tous ..."),
            font_size='14sp', font_name="8bit", halign='left', size_hint_y=None, height='30sp', color=(0, 1, 0, 1)
        )
        marquee_container = BoxLayout(size_hint_y=None, height='30sp')
        with marquee_container.canvas.before:
            Color(0, 0, 0, 1)
            self.marquee_bg = Rectangle(size=marquee_container.size, pos=marquee_container.pos)
        marquee_container.bind(size=self.update_rect, pos=self.update_rect)
        
        marquee_container.add_widget(self.marquee_text)
        layout.add_widget(marquee_container)

        self.add_widget(layout)
        self.start_marquee_animation()

    def update_rect(self, *args):
        # Update background rectangle size and position
        self.rect.size = self.size
        self.rect.pos = self.pos

    def start_game_vs_cpu(self, instance):
        # Switch to the game screen for CPU vs Player
        self.manager.current = 'game_vs_cpu'

    def start_two_player_game(self, instance):
        # Switch to the game screen for Player vs Player
        self.manager.current = 'two_player_game'

    def placeholder(self, instance):
        pass

    def show_instructions(self, instance):
        # Switch to the instructions screen
        self.manager.current = 'instructions'

    def quit_app(self, instance):
        App.get_running_app().stop()

    def start_marquee_animation(self):
        # Start the animation for the scrolling message
        self.marquee_text.x = self.width
        total_width = self.marquee_text.texture_size[0] + self.width
        duration = total_width / 100

        animation = Animation(x=-self.marquee_text.texture_size[0], duration=duration, transition='linear')
        animation.bind(on_complete=lambda *args: self.reset_marquee_position())
        animation.start(self.marquee_text)

    def reset_marquee_position(self):
        self.marquee_text.x = self.width
        self.start_marquee_animation()

# Define the Game screen for player vs CPU
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout = layout

        # Dynamic font size for buttons and labels
        self.font_size = min(Window.width, Window.height) * 0.15
        self.status_font_size = min(Window.width, Window.height) * 0.05

        # Create a grid layout for the Tic-Tac-Toe board
        self.grid = GridLayout(cols=3, spacing=5)

        self.buttons = [[Button(font_size=self.font_size, background_color=(0.3, 0.9, 0.3, 1), color=(0, 0, 0, 1))
                         for _ in range(3)] for _ in range(3)]
        
        for row in self.buttons:
            for button in row:
                button.bind(on_release=self.make_move)
                self.grid.add_widget(button)

        layout.add_widget(self.grid)

        # Status label for turns and game results
        self.status_label = Label(text='Your turn', font_size=self.status_font_size, halign='center', color=(1, 0.5, 0, 1))
        layout.add_widget(self.status_label)

        # Control buttons for restarting and returning to menu
        control_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.restart_button = Button(text="Recommencer", on_release=self.reset_game, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.menu_button = Button(text="Retour au menu", on_release=self.return_to_menu, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        control_layout.add_widget(self.restart_button)
        control_layout.add_widget(self.menu_button)
        layout.add_widget(control_layout)

        self.add_widget(layout)
        self.reset_game()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def make_move(self, button):
        if button.text == '' and not self.check_winner():
            button.text = 'X'
            button.color = (0, 0, 1, 1)
            self.status_label.text = "AI's turn"
            if not self.check_winner():
                self.ai_move()
                if not self.check_winner():
                    self.status_label.text = "Your turn"

    def ai_move(self):
        for row in self.buttons:
            for button in row:
                if button.text == '':
                    button.text = 'O'
                    button.color = (0, 1, 0, 1)
                    return

    def check_winner(self):
        lines = self.buttons + [[self.buttons[r][c] for r in range(3)] for c in range(3)] + \
                [[self.buttons[i][i] for i in range(3)], [self.buttons[i][2 - i] for i in range(3)]]

        for line in lines:
            if line[0].text != '' and all(button.text == line[0].text for button in line):
                self.status_label.text = f"{line[0].text} a gagné !"
                return True

        if all(button.text != '' for row in self.buttons for button in row):
            self.status_label.text = "Égalité !"
            return True

        return False

    def reset_game(self, *args):
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.color = (0, 0, 0, 1)
        self.status_label.text = 'Your turn'
        self.current_player = random.choice(['X', 'O'])
        self.status_label.text = f"{self.current_player}'s turn"

    def return_to_menu(self, *args):
        self.manager.current = 'menu'
        self.reset_game()

# Define the game screen for two players
class TwoPlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super(TwoPlayerGameScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Dynamic font sizes for game elements
        self.font_size = min(Window.width, Window.height) * 0.15
        self.status_font_size = min(Window.width, Window.height) * 0.05

        # Create a grid layout for the Tic-Tac-Toe board
        self.grid = GridLayout(cols=3, spacing=5)

        self.buttons = [[Button(font_size=self.font_size, background_color=(0.3, 0.9, 0.3, 1), color=(0, 0, 0, 1))
                         for _ in range(3)] for _ in range(3)]
        
        for row in self.buttons:
            for button in row:
                button.bind(on_release=self.make_move)
                self.grid.add_widget(button)

        layout.add_widget(self.grid)

        # Status label for turns and results
        self.status_label = Label(text='Joueur 1 (X) à jouer', font_size=self.status_font_size, halign='center', color=(1, 0.5, 0, 1))
        layout.add_widget(self.status_label)

        # Control buttons
        control_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.restart_button = Button(text="Recommencer", on_release=self.reset_game, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.menu_button = Button(text="Retour au menu", on_release=self.return_to_menu, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        control_layout.add_widget(self.restart_button)
        control_layout.add_widget(self.menu_button)
        layout.add_widget(control_layout)

        self.add_widget(layout)
        self.reset_game()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def make_move(self, button):
        if button.text == '' and not self.check_winner():
            current_player = 'X' if self.status_label.text.endswith("1 (X) à jouer") else 'O'
            button.text = current_player
            button.color = (0, 0, 1, 1) if current_player == 'X' else (0, 1, 0, 1)
            if not self.check_winner():
                next_player = '2 (O)' if current_player == 'X' else '1 (X)'
                self.status_label.text = f'Joueur {next_player} à jouer'

    def check_winner(self):
        lines = self.buttons + [[self.buttons[r][c] for r in range(3)] for c in range(3)] + \
                [[self.buttons[i][i] for i in range(3)], [self.buttons[i][2 - i] for i in range(3)]]

        for line in lines:
            if line[0].text != '' and all(button.text == line[0].text for button in line):
                self.status_label.text = f"Joueur {line[0].text} a gagné !"
                return True

        if all(button.text != '' for row in self.buttons for button in row):
            self.status_label.text = "Égalité !"
            return True

        return False

    def reset_game(self, *args):
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.color = (0, 0, 0, 1)
        self.status_label.text = 'Joueur 1 (X) à jouer'

    def return_to_menu(self, *args):
        self.manager.current = 'menu'
        self.reset_game()

# Define the instructions screen
class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Dynamic font size for instructions
        self.instruction_font_size = min(Window.width, Window.height) * 0.04

        instructions_label = Label(text="Instructions du jeu :\n\n"
                                         "Le jeu se joue à deux joueurs. Chaque joueur choisit un symbole (X ou O).\n"
                                         "Le but est d'aligner trois symboles sur une ligne, une colonne ou une diagonale.\n"
                                         "Cliquez sur une case vide pour faire votre mouvement.\n"
                                         "Le premier joueur à aligner trois symboles gagne.\n"
                                         "En cas d'égalité, la partie se termine sans gagnant.\n\n"
                                         "Amusez-vous bien !",
                                     font_size=self.instruction_font_size, halign='center', color=(1, 1, 1, 1))
        layout.add_widget(instructions_label)

        back_button = Button(text="Retour", size_hint=(1, 0.1), on_release=self.return_to_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def return_to_menu(self, *args):
        self.manager.current = 'menu'

class MyOXO(App):
    def build(self):
        if platform.system() == 'Android':
            Window.fullscreen = 'auto'
            Clock.schedule_once(self.force_fullscreen_refresh, 0.1)

        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game_vs_cpu'))
        sm.add_widget(TwoPlayerGameScreen(name='two_player_game'))
        sm.add_widget(InstructionsScreen(name='instructions'))
        return sm

    def force_fullscreen_refresh(self, *args):
        Window.size = (Window.width, Window.height)
        for screen in self.root.screens:
            screen.size = Window.size
            screen.pos = (0, 0)

if __name__ == '__main__':
    MyOXO().run()
