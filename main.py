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

# Enregistrement d'une police personnalisée pour un style rétro
LabelBase.register(name="8bit", fn_regular="8bit.ttf")

# Définition de l'écran du menu principal
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        # Définir une couleur de fond pour le menu principal
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Couleur de fond gris foncé
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Création d'un layout vertical pour organiser les éléments du menu
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Taille de police dynamique pour le titre du jeu
        self.title_font_size = min(Window.width, Window.height) * 0.1

        # Titre du jeu
        title = Label(text='[b]OXO[/b]', markup=True, font_size=self.title_font_size, halign='center', color=(1, 1, 0, 1))
        layout.add_widget(title)

        # Création des boutons de menu avec leurs actions respectives
        buttons = [
            ("vs CPU 3x3", self.start_game_vs_cpu),  # Lancer un jeu contre l'ordinateur
            ("Two players", self.start_two_player_game),  # Lancer un jeu à deux joueurs
            ("Match", self.placeholder),  # Fonctionnalité de match, inactive pour l'instant
            ("Instructions", self.show_instructions),  # Afficher les instructions du jeu
            ("Donation si vous voulez", self.placeholder),  # Option pour les dons
            ("Quitter", self.quit_app)  # Quitter l'application
        ]
        for text, action in buttons:
            button = Button(text=text, size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
            button.bind(on_release=action)
            layout.add_widget(button)

        # Création d'un message défilant en bas de l'écran
        self.marquee_text = Label(
            text=("(c) ByteRoots Studio - 2024 - release 0.1 - ce jeu est gratuit et ne contient pas de pub - "
                  "Des améliorations suivront au fur et à mesure de mon propre apprentissage - belle journée à vous tous ..."),
            font_size='14sp', font_name="8bit", halign='left', size_hint_y=None, height='30sp', color=(0, 1, 0, 1)
        )
        marquee_container = BoxLayout(size_hint_y=None, height='30sp')
        with marquee_container.canvas.before:
            Color(0, 0, 0, 1)  # Fond noir pour le message
            self.marquee_bg = Rectangle(size=marquee_container.size, pos=marquee_container.pos)
        marquee_container.bind(size=self.update_rect, pos=self.update_rect)
        
        marquee_container.add_widget(self.marquee_text)
        layout.add_widget(marquee_container)

        self.add_widget(layout)
        self.start_marquee_animation()

    def update_rect(self, *args):
        # Ajuster la taille et la position du rectangle de fond
        self.rect.size = self.size
        self.rect.pos = self.pos

    def start_game_vs_cpu(self, instance):
        # Passer à l'écran de jeu contre l'ordinateur
        self.manager.current = 'game_vs_cpu'

    def start_two_player_game(self, instance):
        # Passer à l'écran de jeu pour deux joueurs
        self.manager.current = 'two_player_game'

    def placeholder(self, instance):
        pass  # Fonctionnalité non active pour le moment

    def show_instructions(self, instance):
        # Passer à l'écran des instructions
        self.manager.current = 'instructions'

    def quit_app(self, instance):
        # Quitter l'application
        App.get_running_app().stop()

    def start_marquee_animation(self):
        # Lancer l'animation pour le message défilant
        self.marquee_text.x = self.width
        total_width = self.marquee_text.texture_size[0] + self.width
        duration = total_width / 100

        animation = Animation(x=-self.marquee_text.texture_size[0], duration=duration, transition='linear')
        animation.bind(on_complete=lambda *args: self.reset_marquee_position())
        animation.start(self.marquee_text)

    def reset_marquee_position(self):
        # Réinitialiser la position du message pour un défilement continu
        self.marquee_text.x = self.width
        self.start_marquee_animation()

# Définition de l'écran des instructions
class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)

        # Création d'un layout vertical pour organiser les éléments
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Calculer une taille de police dynamique pour les instructions
        self.instruction_font_size = min(Window.width, Window.height) * 0.04

        # Label contenant les instructions du jeu
        instructions_label = Label(text="Instructions du jeu :\n\n"
                                         "Le jeu se joue à deux joueurs. Chaque joueur choisit un symbole (X ou O).\n"
                                         "Le but est d'aligner trois symboles sur une ligne, une colonne ou une diagonale.\n"
                                         "Cliquez sur une case vide pour faire votre mouvement.\n"
                                         "Le premier joueur à aligner trois symboles gagne.\n"
                                         "En cas d'égalité, la partie se termine sans gagnant.\n\n"
                                         "Amusez-vous bien !",
                                     font_size=self.instruction_font_size, halign='center', valign='middle', text_size=(Window.width * 0.9, None),
                                     color=(1, 1, 1, 1))
        layout.add_widget(instructions_label)

        # Bouton pour retourner au menu principal
        back_button = Button(text="Retour", size_hint=(1, 0.1), on_release=self.return_to_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def return_to_menu(self, *args):
        # Retourner au menu principal
        self.manager.current = 'menu'

# Définition de l'application principale
class MyOXO(App):
    def build(self):
        # Mise en plein écran pour Android
        if platform.system() == 'Android':
            Window.fullscreen = 'auto'
            Clock.schedule_once(self.force_fullscreen_refresh, 0.1)

        # Création du ScreenManager pour gérer les différents écrans
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))  # Écran du menu principal
        sm.add_widget(InstructionsScreen(name='instructions'))  # Écran des instructions
        return sm

    def force_fullscreen_refresh(self, *args):
        # Rafraîchir la taille de la fenêtre pour s'assurer qu'elle est bien en plein écran
        Window.size = (Window.width, Window.height)
        for screen in self.root.screens:
            screen.size = Window.size
            screen.pos = (0, 0)

if __name__ == '__main__':
    MyOXO().run()
