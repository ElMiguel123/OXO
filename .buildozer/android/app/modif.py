class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

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

        # Bouton pour définir la difficulté
        self.difficulty_levels = ["Facile", "Moyenne", "Difficile", "Impossible"]
        self.current_difficulty_index = 0
        self.difficulty_button = Button(text=f"Difficulté : {self.difficulty_levels[self.current_difficulty_index]}",
                                         size_hint=(1, 0.2), background_color=(1, 0.5, 0, 1), color=(1, 1, 1, 1))
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

        # Taille de la matrice par défaut : 3x3
        self.matrix_size = 3

    def change_difficulty(self, instance):
        # Alterner entre les niveaux de difficulté
        self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulty_levels)
        self.difficulty_button.text = f"Difficulté : {self.difficulty_levels[self.current_difficulty_index]}"
        print(f"Difficulté définie sur : {self.difficulty_levels[self.current_difficulty_index]}")

    def start_game_vs_cpu(self, instance):
        # Passer la difficulté choisie au jeu CPU
        self.manager.current = 'game_vs_cpu'
        game_screen = self.manager.get_screen('game_vs_cpu')
        game_screen.set_difficulty(self.difficulty_levels[self.current_difficulty_index])

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.difficulty = "Facile"  # Niveau de difficulté par défaut

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        print(f"Niveau de difficulté réglé sur : {difficulty}")

    def ai_move(self):
        if self.difficulty == "Facile":
            self.ai_move_easy()
        elif self.difficulty == "Moyenne":
            self.ai_move_medium()
        elif self.difficulty == "Difficile":
            self.ai_move_hard()
        elif self.difficulty == "Impossible":
            self.ai_move_impossible()

    def ai_move_easy(self):
        # IA facile : mouvement aléatoire
        available_moves = [(row, col) for row in range(len(self.buttons)) for col in range(len(self.buttons)) if self.buttons[row][col].text == ""]
        if available_moves:
            row, col = random.choice(available_moves)
            self.buttons[row][col].text = "O"

    def ai_move_medium(self):
        # IA moyenne : blocage basique ou mouvement aléatoire
        if not self.block_player():
            self.ai_move_easy()

    def ai_move_hard(self):
        # IA difficile : blocage et tentative de victoire
        if not self.try_to_win():
            if not self.block_player():
                self.ai_move_easy()

    def ai_move_impossible(self):
        # IA impossible : stratégie optimale (placeholder)
        print("IA impossible non implémentée. Par défaut, IA difficile.")
        self.ai_move_hard()

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

    def try_to_win(self):
        # Tenter de gagner (simple implémentation)
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons)):
                if self.buttons[row][col].text == "":
                    self.buttons[row][col].text = "O"
                    if self.check_winner():
                        return True
                    self.buttons[row][col].text = ""
        return False
