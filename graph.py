from copy import deepcopy

class Task():  # représentation d'une tâche dans le graphe
    def __init__(self, name, out_link=0):
        self.name = name
        self.duration = {name: 0}  # dictionnaire stockant les prédecesseurs de notre tâche et la durée du prédecesseur
        self.dependencies = []  # liste qui stocke les prédecesseurs
        self.children = []  # liste qui stocke les sucesseurs
        self.out_link = int(out_link)  # durée de la tâche (indiquée dans le fichier d'entrée)
        self.rank = 0  # rang de la tâche (pour l'ordonnancement)
        self.early_date = (0, None)  # (date au plus tôt de la tâche, predecesseur) (servira pour après)
        self.late_date = (0, None)  # (date au plus tard de la tâche, predecesseur) (servira pour après)
        self.total_float = self.early_date[0] - self.late_date[0] 

    def set_dependencies(self,
                         dependencie):  # méthode qui permet d'ajouter les prédécesseurs dans la liste dependencies
        self.dependencies.append(dependencie)

    def set_children(self,child):  # méthode qui permet d'ajouter les successeurs dans la liste children
        self.children.append(child)


class Graph:
    def __init__(self, lines):
        self.lines = lines
        self.graph = []  # liste d'objets "Task", représentant les tâches du graphe
        self.create_graph()

    # assigne les valeurs des liens entre les tâches en fonction des dépendances
    def set_link_value(self, task):
        if not task.dependencies:  # si aucune dépendance, la durée depuis α vers notre tâche est 0
            task.duration['0'] = 0
        else:
            for dependencie in task.dependencies:  # parcours les tâches dont dépend notre tâche actuelle (les prédecesseurs)
                task.duration[
                    dependencie.name] = dependencie.out_link  # associe dans notre dictionnaire la durée de la tâche prédécesseur

    def create_graph(self):
        entry_node = Task('0', 0)  # Sommet α
        self.graph.append(entry_node)  # ajoute le sommet 0 (α)

        # Création des tâches
        for line in self.lines:  # parcous les lignes du fichier txt
            line_read = line.split()  # découpe la ligne en morceaux (indice 0 = nom, indice 1 = durée etc)
            if any(task.name == line_read[0] for task in self.graph):
                continue  # évite d'ajouter deux fois la même tâche
            task_obj = Task(line_read[0], line_read[1])  # création de la tâche avec nom (indice 0) + durée (indice 1)
            self.graph.append(task_obj)
            if len(line_read) == 2:  # si ya que deux chiffres dans la ligne alors pas de prédecesseurs donc α (0) sera notre prédecesseur
                task_obj.set_dependencies(entry_node)

        # Ajout des dépendances
        for line in self.lines:
            line_read = line.split()
            current_task = next(task for task in self.graph if task.name == line_read[0])  # Parcourt les tâches
            task_read = [int(element) for element in
                         line_read[2:]]  # Récupère les prédécesseurs de notre tâche actuelle

            # Associe chaque tâche prédécesseur à la tâche actuelle
            for i in task_read:  # Parcourt chaque tâche prédécesseur
                for task in self.graph:  # Parcourt toutes les tâches du graphe
                    if task.name == str(i):  # Cherche la tâche correspondant au prédécesseur
                        current_task.set_dependencies(task)  # Ajoute la dépendance
                        break
            self.set_link_value(current_task)  # Met à jour les durées des liens entre les tâches

        # Ajout du sommet final ω
        exit_nodes = [node for node in self.graph if not any(node in task.dependencies for task in self.graph)]
        exit_task = Task(str(len(self.graph)), 0)  # Sommet ω (N+1) comme on part de 0 on a pas besoin de faire +1
        for node in exit_nodes:
            exit_task.set_dependencies(node)
            exit_task.duration[node.name] = node.out_link
        self.graph.append(exit_task)

    def print_graph(self, output_file = None):  # choix 1 dans le menu
        for task in self.graph:
            for dependencie in task.dependencies:
                print(dependencie.name, '->', task.name, "=", task.duration[
                    dependencie.name], file=output_file)  # affiche les relations entre tâches sous la forme prédecesseurs -> tâche actuelle = durée prédécesseur

    def print_matrix(self, output_file=None):  # choix 2 dans le menu
        if (output_file==None):
            print("\nMatrice des valeurs du graphe :")

        #Calcul de la largeur max des colonnes
        max_length = max(len(str(task.name)) for task in self.graph)

        #Affichage de l'en-tête
        header_format = "{:>" + str(max_length) + "}"
        print(header_format.format(""), end=" ", file=output_file)
        for task in self.graph:
            print(header_format.format(task.name), end=" ", file=output_file)
        print(file=output_file)

        #Affichage de la matrice
        for task in self.graph:
            print(header_format.format(task.name), end=" ", file=output_file)
            for target in self.graph:
                if task in target.dependencies:
                    print(header_format.format(target.duration[task.name]), end=" ", file=output_file)
                else:
                    print(header_format.format("-"),
                          end=" ", file=output_file)  # - au lieu de 0 pour par confondre avec la durée du sommet alpha
            print(file=output_file)

    def verify_cycle(self, display=True, output_file=None):
        graph_copy = self.graph.copy()

        while True:
            entry_nodes = [node for node in graph_copy if not node.dependencies]

            if not entry_nodes:
                if graph_copy:
                    if display:
                        print("\n-> Le graphe contient un cycle ❌\n")
                    if output_file:
                        print("\n-> Le graphe contient un cycle ❌\n", file=output_file)
                    return False
                if display:
                    print("\n-> Il n’y a pas de circuit ✅\n")
                if output_file:
                    print("\n-> Il n’y a pas de circuit ✅\n", file=output_file)
                return True

            if display:
                print("Points d’entrée :", " ".join(node.name for node in entry_nodes))
            if output_file:
                print("Points d’entrée :", " ".join(node.name for node in entry_nodes), file=output_file)

            for node in entry_nodes:
                graph_copy.remove(node)
                for task in graph_copy:
                    if node in task.dependencies:
                        task.dependencies.remove(node)

            remaining_nodes = " ".join(node.name for node in graph_copy) if graph_copy else "Aucun"
            if display:
                print("Suppression des points d’entrée")
                print(f"Sommets restant : {remaining_nodes}\n")
            if output_file:
                print("Suppression des points d’entrée", file=output_file)
                print(f"Sommets restant : {remaining_nodes}\n", file=output_file)


    def check_negative_val(self, display=True, output_file=None):
        if display:
            print("Vérification des arcs à valeurs négatives :")
        if output_file:
            print("Vérification des arcs à valeurs négatives :", file=output_file)

        for task in self.graph:
            for dependencie in task.dependencies:
                val = task.duration[dependencie.name]
                if display:
                    print(f"  - Tâche {dependencie.name} -> {task.name} = {val}")
                if output_file:
                    print(f"  - Tâche {dependencie.name} -> {task.name} = {val}", file=output_file)

                if val < 0:
                    if display:
                        print(f"--> Valeur négative détectée ❌ : {dependencie.name} -> {task.name} = {val}\n")
                    if output_file:
                        print(f"--> Valeur négative détectée ❌ : {dependencie.name} -> {task.name} = {val}\n", file=output_file)
                    return False

        if display:
            print("--> Aucun arc à valeur négative détecté ✅\n")
        if output_file:
            print("--> Aucun arc à valeur négative détecté ✅\n", file=output_file)
        return True


    def set_rank(self, output_file=None):
        def copy(self):
            return Graph(self.lines)

        g_copy = copy(self)  # copie du graphe

        rank = 0
        tasks_without_predecessors = []
        for task in g_copy.graph:
            if not task.dependencies:
                tasks_without_predecessors.append(task)

        if output_file:
            print("Début du calcul des rangs avec tri topologique :", file=output_file)

        while tasks_without_predecessors:
            next_tasks = []

            if output_file:
                print(f"\nTâches sans prédécesseurs (rang {rank}) :", " ".join(t.name for t in tasks_without_predecessors), file=output_file)

            for task in tasks_without_predecessors:
                task.rank = rank
                for successor in g_copy.graph:
                    if task in successor.dependencies:
                        successor.dependencies.remove(task)
                        if not successor.dependencies:
                            next_tasks.append(successor)

            tasks_without_predecessors = next_tasks
            rank += 1

        # Appliquer les rangs calculés à ton graphe principal
        for task_copy in g_copy.graph:
            for task in self.graph:
                if task.name == task_copy.name:
                    task.rank = task_copy.rank


    def print_rank(self, output_file=None):
        self.set_rank()  # a faire : faire en sorte de n'appeler qu'une fois set_rank pour tt le pgm
        print("\nListe des tâches avec leur rang :", file=output_file)
        tasks_sorted = list(self.graph)  # Copie la liste
        tasks_sorted.sort(key=lambda task: task.rank)  # Trier par rang

        for task in tasks_sorted:
            print(f"Tâche {task.name} → Rang : {task.rank}", file=output_file)

    def order_by_rank(self):
        for i in range(len(self.graph) - 1):
            for j in range(i, len(self.graph)):
                if (self.graph[i].rank > self.graph[j].rank):
                    temp = self.graph[i]
                    self.graph[i] = self.graph[j]
                    self.graph[j] = temp

    def calculate_early_start(self, output_file=None):
        self.set_rank()  # On peut garder l'appel pour s'assurer que les rangs sont là
        self.order_by_rank()  # Tri des tâches par rang

        if output_file:
            print("Début du calcul des dates au plus tôt (ES)", file=output_file)

        for task in self.graph:
            dependencies_dates = []

            if output_file:
                print(f"\nTâche {task.name} (rang {task.rank}) :", file=output_file)

            for dependencie in task.dependencies:
                val = dependencie.early_date[0] + task.duration[dependencie.name]
                dependencies_dates.append((val, dependencie))
                if output_file:
                    print(f"  - depuis tâche {dependencie.name} : ES = {dependencie.early_date[0]} + durée = {task.duration[dependencie.name]} → {val}", file=output_file)

            # Sélection du max
            maxi = (0, None)
            for i in range(len(dependencies_dates)):
                if maxi[1] is None or dependencies_dates[i][0] > maxi[0]:
                    maxi = dependencies_dates[i]

            task.early_date = maxi

            if output_file:
                origin = maxi[1].name if maxi[1] else "None"
                print(f"  => Date au plus tôt retenue : {maxi[0]} (origine : {origin})", file=output_file)


    def display_early_start(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tot(origine)':<20}", file=output_file)
        print("-" * 45, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.early_date[0]) + '(' + str(task.early_date[1].name if task.early_date[1] != None else None) + ')':<20}", file=output_file)

    def calculate_late_start(self, output_file=None):
        self.set_rank()
        self.order_by_rank()

        if self.graph[-1].early_date == (0, None):
            self.calculate_early_start(output_file=output_file)

        # Création des liens enfants (successeurs)
        for task in self.graph:
            task.children = []
            for child in self.graph:
                if task in child.dependencies:
                    task.set_children(child)

        # Initialisation
        last_task = self.graph[-1]
        last_task.late_date = (last_task.early_date[0], None)

        if output_file:
            print(f"\nInitialisation : tâche finale {last_task.name} → LS = {last_task.late_date[0]}", file=output_file)

        for task in self.graph[:-1]:
            task.late_date = (float('inf'), None)

        if output_file:
            print("\nDébut du calcul des dates au plus tard (LS)", file=output_file)

        # Parcours en ordre inverse
        for task in reversed(self.graph):
            if output_file:
                print(f"\nTâche {task.name} (rang {task.rank}) :", file=output_file)

            for child in task.children:
                if task.name not in child.duration:
                    continue  # sécurité

                ls_child = child.late_date[0]
                arc_duration = child.duration[task.name]
                candidate_ls = ls_child - arc_duration

                if output_file:
                    print(f"  - via successeur {child.name} : LS = {ls_child} - durée = {arc_duration} → {candidate_ls}", file=output_file)

                if candidate_ls < task.late_date[0]:
                    task.late_date = (candidate_ls, child)
                    if output_file:
                        print(f"  => Nouvelle date au plus tard retenue : {candidate_ls} (via {child.name})", file=output_file)


    def display_late_start(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tard(origine)':<20}", file=output_file)
        print("-" * 45, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.late_date[0]) + '(' + str(task.late_date[1].name if task.late_date[1] != None else None) + ')':<20}", file=output_file)

    def compute_total_float(self, output_file=None):
        self.calculate_late_start()

        if output_file:
            print("\nCalcul des marges totales (Total Float - TF) :", file=output_file)

        for task in self.graph:
            es = task.early_date[0]
            ls = task.late_date[0]
            tf = ls - es
            task.total_float = tf

            if output_file:
                print(f"  - Tâche {task.name} : LS = {ls}, ES = {es} → TF = {tf}", file=output_file)


    def display_total_float(self, output_file=None):

        print("\nMargesTotales (TF) des tâches :\n", file=output_file)
        print(f"{'Tâche':<10}{'ES':<10}{'LS':<10}{'TF'}", file=output_file)
        print("-" * 35, file=output_file)

        for task in self.graph:
            print(f"{task.name:<10}{task.late_date[0]:<10}{task.early_date[0]:<10}{task.total_float}", file=output_file)

    def display_critical_path(self, output_file=None):
        self.compute_total_float()  # s'assure que les marges sont bien calculées

        # on vérifie si toutes les tâches ont une marge totale de 0 (on en aura besoin après)
        all_zero_margin = all(task.total_float == 0 for task in self.graph)

        # durée totale du projet = date au plus tôt de la tâche finale
        project_duration = self.graph[-1].early_date[0]

        # liste qui stocke les chemins critiques trouvés
        all_critical_paths = []

        # parcours en profondeur récursif
        def dfs(task, path, total_duration):
            if task.total_float != 0:
                return  # tâche non critique, on ne continue pas

            path.append(task)

            # si on atteint le sommet final (ω)
            if task.name == str(len(self.graph) - 1):
                if total_duration == project_duration:
                    all_critical_paths.append(list(path))
            else:
                for child in task.children:
                    if task.name in child.duration:
                        dfs(child, path, total_duration + child.duration[task.name])

            path.pop()

        # trouver le point d’entrée (pour nous c'est la tâche 0)
        start_tasks = [task for task in self.graph if task.name == '0']
        if not start_tasks:
            print("Pas de tâche de départ trouvée.", file=output_file)
            return

        # lancer la DFS depuis le sommet 0
        dfs(start_tasks[0], [], 0)

        # affichage des chemins critiques
        if not all_critical_paths:
            print("Aucun chemin critique trouvé.", file=output_file)
        else:
            for i, path in enumerate(all_critical_paths):
                print(f"Chemin critique {i + 1} :", " -> ".join(task.name for task in path), file=output_file)




    def display_scheduling(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tot(origine)':<20}{'Date au plus tard(origine)':<20}{'Marges Totales':<15}", file=output_file)
        print("-" * 55, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.early_date[0]) + '(' + str(task.early_date[1].name if task.early_date[1] != None else None) + ')':<20}{str(
                task.late_date[0]) + '(' + str(task.late_date[1].name if task.late_date[1] != None else None) + ')':<20}{task.total_float:<15}", file=output_file)

    def save_results(self, graph_number):
        output_path = f"results/result_graph_{graph_number}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"===== Analyse du graphe table {graph_number} =====\n\n")

            f.write("=== 1. Affichage des relations entre tâches ===\n")
            f.write("\n")
            self.print_graph(f)
            f.write("\n")

            f.write("=== 2. Matrice des valeurs du graphe ===\n")
            f.write("\n")
            self.print_matrix(f)
            f.write("\n")

            f.write("=== 3. Vérification du graphe ===\n")
            graph_copy = deepcopy(self)
            cycle = graph_copy.verify_cycle(display=False, output_file=f)
            negative = self.check_negative_val(display=False, output_file=f)


            if not cycle or not negative:
                f.write("Ce graphe n’est pas un graphe d’ordonnancement.\n")
                return
            f.write("Ce graphe est un graphe d’ordonnancement.\n\n")

            f.write("=== 4. Rangs des tâches ===\n")
            self.set_rank(output_file=f)
            self.print_rank(f)
            f.write("\n")
            f.write("\n")

            f.write("=== 5. Dates au plus tôt (Early Start - ES) ===\n")
            f.write("\n")
            self.calculate_early_start(output_file=f)
            f.write("\n")
            f.write("===Résultat des dates au plus tôt (Early Start - ES) ===\n")
            f.write("\n")
            self.display_early_start(f)
            f.write("\n")
            f.write("\n")

            f.write("=== 6. Dates au plus tard (Late Start - LS) ===\n")
            self.calculate_late_start(output_file=f)
            f.write("\n")
            f.write("===Résultat des dates au plus tard (Late Start - LS) ===\n")
            f.write("\n")
            self.display_late_start(f)
            f.write("\n")
            f.write("\n")

            f.write("=== 7. Marges totales (Total Float - TF) ===\n")
            self.compute_total_float(output_file=f)
            self.display_total_float(f)
            f.write("\n")
            f.write("\n")

            f.write("=== 8. Chemins critiques ===\n")
            f.write("\n")
            self.display_critical_path(f)
            f.write("\n")
            f.write("\n")

            f.write("=== 9. Résumé de l’ordonnancement ===\n")
            f.write("\n")
            self.display_scheduling(f)
            f.write("\n")

