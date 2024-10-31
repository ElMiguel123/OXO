from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import random

class myOxo(App): 
    def build(self):
        Window.size = (300, 400)  # Ajuste la taille de la fenêtre pour le PC
        self.mode = None  # Mode de jeu choisi (1 joueur ou 2 joueurs)
        
        # Affichage du menu principal
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.build_menu())
        return self.root

    def build_menu(self):
        # Page de menu principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Titre
        title_label = Label(text="OXO", font_size=48, size_hint=(1, 0.4))
        layout.add_widget(title_label)
        
        # Bouton pour 1 joueur (contre ordinateur)
        btn_1_player = Button(text="1 Joueur (contre Ordinateur)", font_size=24)
        btn_1_player.bind(on_press=self.start_single_player)
        layout.add_widget(btn_1_player)
        
        # Bouton pour 2 joueurs (humain contre humain)
        btn_2_players = Button(text="2 Joueurs (Humain contre Humain)", font_size=24)
        btn_2_players.bind(on_press=self.start_two_players)
        layout.add_widget(btn_2_players)
        
        # Bouton pour quitter
        btn_quit = Button(text="Quitter", font_size=24)
        btn_quit.bind(on_press=self.stop)
        layout.add_widget(btn_quit)
        
        # Ligne de crédit
        credit_label = Label(text="(c) Wolfiz UniKorn Software - Release 0.1 - 2024", font_size=16, size_hint=(1, 0.2))
        layout.add_widget(credit_label)
        
        return layout

    def start_single_player(self, instance):
        self.mode = "single"
        self.build_game()

    def start_two_players(self, instance):
        self.mode = "two"
        self.build_game()

    def build_game(self):
        # Construction de la grille de jeu
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        
        # Affichage de la grille de jeu
        self.layout = GridLayout(cols=3, rows=4, row_force_default=True, row_default_height=100)
        
        # Ajout des boutons de la grille
        for i in range(3):
            for j in range(3):
                button = Button(font_size=50)
                button.bind(on_press=lambda btn, x=i, y=j: self.on_button_press(btn, x, y))
                self.layout.add_widget(button)
        
        # Ajout du label de statut
        self.status_label = Label(text="Tour du joueur : X", font_size=24, size_hint_y=None, height=50)
        self.layout.add_widget(self.status_label)
        
        # Remplace la vue actuelle par le jeu
        self.root.clear_widgets()
        self.root.add_widget(self.layout)

    def on_button_press(self, button, x, y):
        if self.board[x][y] == "":
            if self.mode == "single" and self.turn == "X":
                # Mode contre l'ordinateur
                self.board[x][y] = "X"
                button.text = "X"
                if self.check_winner("X"):
                    self.show_end_menu("Vous avez gagné !")
                else:
                    self.turn = "O"
                    self.status_label.text = "Tour de l'ordinateur"
                    self.computer_move()
            elif self.mode == "two":
                # Mode 2 joueurs (tour par tour)
                self.board[x][y] = self.turn
                button.text = self.turn
                if self.check_winner(self.turn):
                    self.show_end_menu(f"Le joueur {self.turn} a gagné !")
                else:
                    self.turn = "O" if self.turn == "X" else "X"
                    self.status_label.text = f"Tour du joueur : {self.turn}"

    def computer_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.board[x][y] = "O"
            button = self.layout.children[(2 - x) * 3 + (2 - y)]
            button.text = "O"
            if self.check_winner("O"):
                self.show_end_menu("L'ordinateur a gagné !")
            else:
                self.turn = "X"
                self.status_label.text = "Tour du joueur : X"

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def show_end_menu(self, message):
        # Affichage du menu de fin de partie
        end_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Message de victoire
        end_message = Label(text=message, font_size=24)
        end_layout.add_widget(end_message)
        
        # Bouton Rejouer
        btn_replay = Button(text="Rejouer", font_size=24)
        btn_replay.bind(on_press=lambda x: self.build_game())
        end_layout.add_widget(btn_replay)
        
        # Bouton Retour au menu
        btn_main_menu = Button(text="Retour au menu", font_size=24)
        btn_main_menu.bind(on_press=lambda x: self.root.clear_widgets() or self.root.add_widget(self.build_menu()))
        end_layout.add_widget(btn_main_menu)
        
        # Remplace la vue actuelle par le menu de fin
        self.root.clear_widgets()
        self.root.add_widget(end_layout)

if __name__ == '__main__':
    myOxo().run()
