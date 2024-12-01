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
from kivy.graphics import Color, Line, Rectangle
import platform
import random

# Enregistrement d'une police rétro pour le style du jeu
LabelBase.register(name="8bit", fn_regular="8bit.ttf")

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        
        self.difficulty_levels = ["Facile", "Moyenne", "Difficile", "Impossible"]
        self.current_difficulty_index = 0
        self.current_difficulty = self.difficulty_levels[self.current_difficulty_index]

        # Configuration de la couleur de fond du menu principal
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Taille de police dynamique pour le titre en fonction de la taille de l'écran
        self.title_font_size = min(Window.width, Window.height) * 0.1

        # Titre du jeu en gras
        title = Label(text='[b]OXO[/b]', markup=True, font_size=self.title_font_size, halign='center', color=(1, 1, 0, 1))
        layout.add_widget(title)

        # Bouton pour jouer contre le CPU
        self.vs_cpu_button = Button(text="vs CPU 3x3", size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
        self.vs_cpu_button.bind(on_release=self.start_game_vs_cpu)
        layout.add_widget(self.vs_cpu_button)

        # Bouton pour le mode deux joueurs
        two_players_button = Button(text="Two players", size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
        two_players_button.bind(on_release=self.start_two_player_game)
        layout.add_widget(two_players_button)

        # Bouton pour alterner entre 3x3 et 6x6 (Ordre et Chaos)
        self.ordre_chaos_button = Button(text="Ordre et Chaos : [b]3x3[/b]", markup=True, size_hint=(1, 0.2),
                                         background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
        self.ordre_chaos_button.bind(on_release=self.toggle_ordre_chaos)
        layout.add_widget(self.ordre_chaos_button)

        # Add a button for "Difficulté"
        self.difficulty_button = Button(
            text="Difficulté : [b]Facile[/b]",
            markup=True,
            size_hint=(1, 0.2),
            background_color=(1, 0.5, 0, 1)  # Orange color
        )
        self.difficulty_button.bind(on_release=self.change_difficulty)
        layout.add_widget(self.difficulty_button)


        # Bouton pour afficher les instructions
        instructions_button = Button(text="Instructions", size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.9, 1), color=(1, 1, 1, 1))
        instructions_button.bind(on_release=self.show_instructions)
        layout.add_widget(instructions_button)

        # Bouton pour quitter l'application
        quit_button = Button(text="Quitter", size_hint=(1, 0.2), background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        quit_button.bind(on_release=self.quit_app)
        layout.add_widget(quit_button)

        # Message défilant en bas de l'écran
        self.marquee_text = Label(
            text=("(c) ByteRoots Studio - 2024 - release 1.0 - cette application est gratuite et dépourvue de publicitée - "
                  "Des améliorations suivront au fur et à mesure de mon propre apprentissage :) - belle journée à vous tous ..."),
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

        # Taille de la matrice par défaut : 3x3
        self.matrix_size = 3

    def change_difficulty(self, instance):
        self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulty_levels)
        self.current_difficulty = self.difficulty_levels[self.current_difficulty_index]
        self.difficulty_button.text = f"Difficulté : [b]{self.current_difficulty}[/b]"
        
    def update_rect(self, *args):
        # Mettre à jour la taille et position du fond
        self.rect.size = self.size
        self.rect.pos = self.pos

    def start_game_vs_cpu(self, instance):
        # Passer à l'écran de jeu vs CPU avec la taille de matrice sélectionnée
        GameScreen.set_difficulty(self, self.difficulty_levels[self.current_difficulty_index])
        self.manager.current = 'game_vs_cpu'
        self.manager.get_screen('game_vs_cpu').set_grid_size(self.matrix_size)


    def start_two_player_game(self, instance):
        # Passer à l'écran de jeu pour deux joueurs avec la taille de matrice sélectionnée
        self.manager.current = 'two_player_game'
        self.manager.get_screen('two_player_game').set_grid_size(self.matrix_size)

    def toggle_ordre_chaos(self, instance):
        # Alterner entre une matrice 3x3 et 6x6 et mettre à jour les intitulés des boutons
        self.matrix_size = 6 if self.matrix_size == 3 else 3
        self.vs_cpu_button.text = f"vs CPU {self.matrix_size}x{self.matrix_size}"
        self.ordre_chaos_button.text = f"Ordre et Chaos : [b]{self.matrix_size}x{self.matrix_size}[/b]"

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

# Écran de jeu contre CPU
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.cpu_difficulty = "Facile"  # Default value
        print(f"Valeur initiale {self.cpu_difficulty}")

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout = layout

        self.status_font_size = min(Window.width, Window.height) * 0.05
        self.grid = GridLayout(cols=3, spacing=5)
        layout.add_widget(self.grid)

        self.status_label = Label(text='Your turn', font_size=self.status_font_size, halign='center', color=(1, 0.5, 0, 1))
        layout.add_widget(self.status_label)

        control_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.restart_button = Button(text="Recommencer", on_release=self.reset_game, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.menu_button = Button(text="Retour au menu", on_release=self.return_to_menu, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        control_layout.add_widget(self.restart_button)
        control_layout.add_widget(self.menu_button)
        layout.add_widget(control_layout)

        self.add_widget(layout)

    def set_difficulty(self,difficulty):
        self.cpu_difficulty = difficulty
        print(f"Niveau de difficulté réglé sur : {self.cpu_difficulty}")

    def cpu_move(self):
        
        #button.color = (0, 1, 0, 1)
        
        if self.cpu_difficulty == "Facile":
            return self.easy_move()
        elif self.cpu_difficulty == "Moyenne":
            return self.medium_move()
        elif self.cpu_difficulty == "Difficile":
            return self.hard_move()
        elif self.cpu_difficulty == "Impossible":
            return self.impossible_move()
        
    
    # Define the logic for different levels of CPU intelligence
    
    def ai_move(self):
        for row in self.buttons:
            for button in row:
                if button.text == '':
                    button.text = 'O'
                    button.color = (0, 1, 0, 1)
                    return
                
    def easy_move(self):
        # IA facile : mouvement aléatoire
        available_moves = [(row, col) for row in range(len(self.buttons)) for col in range(len(self.buttons)) if self.buttons[row][col].text == ""]
        if available_moves:
            row, col = random.choice(available_moves)
            self.buttons[row][col].color=(0,1,0,1)
            self.buttons[row][col].text = "O"


    def medium_move(self):
        """
        IA défensive : bloque les tentatives de victoire de l'utilisateur.
        """
        # Vérifie si l'utilisateur peut gagner, et bloque
        if self.block_user():
            return
        # Sinon, joue aléatoirement
        else:
            self.random_ai()

    def hard_move(self):
        """
        IA offensive : cherche à gagner en priorité.
        """
        # Si elle peut gagner, elle le fait
        if self.make_win():
            return
        # Sinon, bloque l'utilisateur
        if self.block_user():
            return
        # Sinon, joue aléatoirement
        else:
            self.random_ai()

    def impossible_move(self):
        """
        IA optimale : joue parfaitement en combinant attaque et défense.
        """
        # Si elle peut gagner, elle le fait
        if self.make_win():
            return
        # Sinon, bloque l'utilisateur
        if self.block_user():
            return
        # Si aucun danger ou opportunité, joue le centre (grille 3x3 uniquement)
        center = len(self.buttons) // 2
        if self.buttons[center][center].text == '':
            self.buttons[center][center].text = 'O'
            self.buttons[center][center].color = (0, 1, 0, 1)
            return
        # Sinon, joue aléatoirement
        else:
            self.random_ai()
        
    def make_win(self):
        """
        Vérifie si l'IA peut gagner et joue le coup gagnant.
        Retourne True si un coup gagnant a été effectué.
        """
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons)):
                if self.buttons[row][col].text == '':
                    self.buttons[row][col].text = 'O'
                    if self.check_winner_temp('O'):
                        self.buttons[row][col].color = (0, 1, 0, 1)
                        return True
                    self.buttons[row][col].text = ''
        return False

    def check_winner_temp(self, symbol):
        """
        Vérifie temporairement si une combinaison gagnante existe pour un symbole donné.
        Utile pour `block_user` et `make_win`.
        """
        win_condition = 3
        size = len(self.buttons)

        # Vérification des lignes et colonnes
        for row in range(size):
            for col in range(size - win_condition + 1):
                if all(self.buttons[row][col + i].text == symbol for i in range(win_condition)):
                    return True
                if all(self.buttons[col + i][row].text == symbol for i in range(win_condition)):
                    return True

        # Vérification des diagonales
        for row in range(size - win_condition + 1):
            for col in range(size - win_condition + 1):
                if all(self.buttons[row + i][col + i].text == symbol for i in range(win_condition)):
                    return True
                if all(self.buttons[row + i][col + win_condition - 1 - i].text == symbol for i in range(win_condition)):
                    return True

        return False
        
    def block_player(self):
        # Bloquer le joueur si nécessaire (simple implémentation)
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons)):
                if self.buttons[row][col].text == "":
                    self.buttons[row][col].text = "X"
                    if self.check_winner():
                        self.buttons[row][col].text = "O"
                        return True
                    self.buttons[row][col].text = ""
        return False
        
    def set_difficulty(self, difficulty):
        self.cpu_difficulty = difficulty
        print(f"{self.cpu_difficulty}")
        
    def set_grid_size(self, size):
        # Configurer la taille de la grille et des X/O
        self.grid.clear_widgets()
        self.grid.cols = size
        # Ajuster la taille de police des symboles
        self.font_size = min(Window.width, Window.height) * (0.08 if size == 6 else 0.15)

        self.buttons = [[Button(font_size=self.font_size, background_color=(0.3, 0.9, 0.3, 1), color=(0, 0, 0, 1))
                         for _ in range(size)] for _ in range(size)]
        
        for row in self.buttons:
            for button in row:
                button.bind(on_release=self.make_move)
                self.grid.add_widget(button)

        self.winning_line = None  # Réinitialiser la ligne gagnante

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def make_move(self, button):
        # Effectuer un coup si la case est vide et vérifier le gagnant
        if button.text == '' and not self.check_winner():
            button.text = 'X'
            button.color = (0, 0, 1, 1)
            self.status_label.text = "AI's turn"
            if not self.check_winner():
                #self.ai_move()
                self.cpu_move()
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
        win_condition = 3
        size = len(self.buttons)

        # Vérification des lignes, colonnes et diagonales
        for row in range(size):
            for col in range(size - win_condition + 1):
                if self.check_sequence([self.buttons[row][col + i] for i in range(win_condition)]):
                    self.draw_winning_line([(row, col + i) for i in range(win_condition)])
                    return True
                if self.check_sequence([self.buttons[col + i][row] for i in range(win_condition)]):
                    self.draw_winning_line([(col + i, row) for i in range(win_condition)])
                    return True

        for row in range(size - win_condition + 1):
            for col in range(size - win_condition + 1):
                if self.check_sequence([self.buttons[row + i][col + i] for i in range(win_condition)]):
                    self.draw_winning_line([(row + i, col + i) for i in range(win_condition)])
                    return True
                if self.check_sequence([self.buttons[row + i][col + win_condition - 1 - i] for i in range(win_condition)]):
                    self.draw_winning_line([(row + i, col + win_condition - 1 - i) for i in range(win_condition)])
                    return True

        if all(button.text != '' for row in self.buttons for button in row):
            self.status_label.text = "Égalité !"
            return True

        return False

    def check_sequence(self, buttons):
        # Vérifier si tous les boutons d'une séquence contiennent le même texte
        if buttons[0].text != '' and all(button.text == buttons[0].text for button in buttons):
            self.status_label.text = f"{buttons[0].text} a gagné !"
            return True
        return False

    def draw_winning_line(self, coordinates):
        # Tracer une ligne jaune sur la combinaison gagnante
        if self.winning_line:
            self.canvas.remove(self.winning_line)

        with self.canvas:
            Color(1, 1, 0, 1)  # Couleur jaune pour la ligne gagnante
            points = []
            for row, col in coordinates:
                button = self.buttons[row][col]
                x, y = button.center
                points.extend([x, y])
            self.winning_line = Line(points=points, width=2)

    def reset_game(self, *args):
        # Réinitialiser le plateau et enlever la ligne gagnante
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.color = (0, 0, 0, 1)
        self.status_label.text = 'Your turn'
        if self.winning_line:
            self.canvas.remove(self.winning_line)
            self.winning_line = None

    def return_to_menu(self, *args):
        self.manager.current = 'menu'
        self.reset_game()

class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.instruction_font_size = min(Window.width, Window.height) * 0.04

        instructions_label = Label(
            text="Instructions du jeu :\n\n"
                 "Le jeu se joue à deux joueurs. Chaque joueur choisit un symbole (X ou O).\n"
                 "Le but est d'aligner trois symboles sur une ligne, une colonne ou une diagonale.\n"
                 "Cliquez sur une case vide pour faire votre mouvement.\n"
                 "Le premier joueur à aligner trois symboles gagne.\n"
                 "En cas d'égalité, la partie se termine sans gagnant.\n\n"
                 "Amusez-vous bien !",
            font_size=self.instruction_font_size, halign='center', valign='middle', text_size=(Window.width * 0.9, None),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(instructions_label)

        back_button = Button(text="Retour", size_hint=(1, 0.1), on_release=self.return_to_menu)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def return_to_menu(self, *args):
        self.manager.current = 'menu'

class TwoPlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super(TwoPlayerGameScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.font_size = min(Window.width, Window.height) * 0.15
        self.status_font_size = min(Window.width, Window.height) * 0.05

        self.grid = GridLayout(cols=3, spacing=5)
        layout.add_widget(self.grid)

        self.status_label = Label(text='Joueur 1 (X) à jouer', font_size=self.status_font_size, halign='center', color=(1, 0.5, 0, 1))
        layout.add_widget(self.status_label)

        control_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.restart_button = Button(text="Recommencer", on_release=self.reset_game, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.menu_button = Button(text="Retour au menu", on_release=self.return_to_menu, background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        control_layout.add_widget(self.restart_button)
        control_layout.add_widget(self.menu_button)
        layout.add_widget(control_layout)

        self.add_widget(layout)
        self.set_grid_size(3)

    def set_grid_size(self, size):
        self.grid.clear_widgets()
        self.grid.cols = size
        self.font_size = min(Window.width, Window.height) * (0.08 if size == 6 else 0.15)

        self.buttons = [[Button(font_size=self.font_size, background_color=(0.3, 0.9, 0.3, 1), color=(0, 0, 0, 1))
                         for _ in range(size)] for _ in range(size)]
        
        for row in self.buttons:
            for button in row:
                button.bind(on_release=self.make_move)
                self.grid.add_widget(button)

        self.winning_line = None

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
        win_condition = 3
        size = len(self.buttons)

        for row in range(size):
            for col in range(size - win_condition + 1):
                if self.check_sequence([self.buttons[row][col + i] for i in range(win_condition)]):
                    self.draw_winning_line([(row, col + i) for i in range(win_condition)])
                    return True
                if self.check_sequence([self.buttons[col + i][row] for i in range(win_condition)]):
                    self.draw_winning_line([(col + i, row) for i in range(win_condition)])
                    return True

        for row in range(size - win_condition + 1):
            for col in range(size - win_condition + 1):
                if self.check_sequence([self.buttons[row + i][col + i] for i in range(win_condition)]):
                    self.draw_winning_line([(row + i, col + i) for i in range(win_condition)])
                    return True
                if self.check_sequence([self.buttons[row + i][col + win_condition - 1 - i] for i in range(win_condition)]):
                    self.draw_winning_line([(row + i, col + win_condition - 1 - i) for i in range(win_condition)])
                    return True

        if all(button.text != '' for row in self.buttons for button in row):
            self.status_label.text = "Égalité !"
            return True

        return False

    def check_sequence(self, buttons):
        if buttons[0].text != '' and all(button.text == buttons[0].text for button in buttons):
            self.status_label.text = f"{buttons[0].text} a gagné !"
            return True
        return False

    def draw_winning_line(self, coordinates):
        if self.winning_line:
            self.canvas.remove(self.winning_line)

        with self.canvas:
            Color(1, 1, 0, 1)
            points = []
            for row, col in coordinates:
                button = self.buttons[row][col]
                x, y = button.center
                points.extend([x, y])
            self.winning_line = Line(points=points, width=2)

    def reset_game(self, *args):
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.color = (0, 0, 0, 1)
        self.status_label.text = 'Joueur 1 (X) à jouer'
        if self.winning_line:
            self.canvas.remove(self.winning_line)
            self.winning_line = None

    def return_to_menu(self, *args):
        self.manager.current = 'menu'
        self.reset_game()

class MyOXO(App):
    def build(self):
        if platform.system() == 'Android':
            Window.fullscreen = 'auto'
            Clock.schedule_once(self.force_fullscreen_refresh, 0.1)
             
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game_vs_cpu'))
        sm.add_widget(InstructionsScreen(name='instructions'))
        sm.add_widget(TwoPlayerGameScreen(name='two_player_game'))     
        return sm

    def force_fullscreen_refresh(self, *args):
        Window.size = (Window.width, Window.height)
        for screen in self.root.screens:
            screen.size = Window.size
            screen.pos = (0, 0)

if __name__ == '__main__':
    MyOXO().run()
