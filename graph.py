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

        # Calcul de la largeur max des colonnes
        max_length = max(len(str(task.name)) for task in self.graph)

        # Affichage de l'en-tête
        header_format = "{:>" + str(max_length) + "}"
        print(header_format.format(""), end=" ", file=output_file)
        for task in self.graph:
            print(header_format.format(task.name), end=" ", file=output_file)
        print(file=output_file)

        # Affichage de la matrice
        for task in self.graph:
            print(header_format.format(task.name), end=" ", file=output_file)
            for target in self.graph:
                if task in target.dependencies:
                    print(header_format.format(target.duration[task.name]), end=" ", file=output_file)
                else:
                    print(header_format.format("-"),
                          end=" ", file=output_file)  # - au lieu de 0 pour par confondre avec la durée du sommet alpha
            print(file=output_file)

    def verify_cycle(self, display=True):
        graph_copy = self.graph.copy()  # copie du graphe pour éviter de modifier l'original

        while True:
            entry_nodes = [node for node in graph_copy if
                           not node.dependencies]  # contient les points d'éntrées (sommets sans prédecesseurs)

            if not entry_nodes:  # Si plus aucun point d'entrée
                if graph_copy:  # S'il reste des sommets -> Cycle détecté
                    if (display):
                        print("\n-> Le graphe contient un cycle ❌\n")
                    return False
                if(display):
                    print("\n-> Il n’y a pas de circuit ✅\n")
                return True

            # Affichage des points d’entrée avant suppression
            if(display):
                print("Points d’entrée :", " ".join(node.name for node in entry_nodes))

            # Suppression des points d’entrée
            for node in entry_nodes:
                graph_copy.remove(node)  # supprimer les tâches sans prédécesseurs
                for task in graph_copy:
                    if node in task.dependencies:
                        task.dependencies.remove(node)  # supprimer les dépendances

            # affichage des sommets restants après suppression
            remaining_nodes = " ".join(node.name for node in
                                       graph_copy) if graph_copy else "Aucun"  # si graph_copy est vide on affiche "Aucun"
            if(display):
                print("Suppression des points d’entrée")
                print(f"Sommets restant : {remaining_nodes}\n")

    def check_negative_val(self, display=True):
        for task in self.graph:
            for dependencie in task.dependencies:
                if task.duration[dependencie.name] < 0:
                    if (display):
                        print(
                        f"--> Oui, le graphe contient une valeure négative : Tache {task.name} -> {dependencie.name} = {task.duration[dependencie.name]}\n")
                    return False
        if(display):
            print("--> Non, le graphe ne contient aucune valeure négative\n")
        return True

    def set_rank(self):
        def copy(self):
            g_copy = Graph(self.lines)
            return g_copy

        g_copy = copy(self)  # copie du graphe

        rank = 0
        tasks_without_predecessors = []
        for task in g_copy.graph:
            if not task.dependencies:  # Si la tâche n'a pas de prédécesseur
                tasks_without_predecessors.append(task)

        while tasks_without_predecessors:
            next_tasks = []  # Liste des tâches qui seront traitées au prochain rang

            for task in tasks_without_predecessors:
                task.rank = rank  # Assigner le rang actuel

                # Parcourir les tâches qui dépendent de la tâche actuelle
                for successor in g_copy.graph:
                    if task in successor.dependencies:
                        successor.dependencies.remove(task)  # Supprimer la dépendance traitée
                        if not successor.dependencies:  # Si plus de dépendance, la tâche suivante peut être traitée au prochain tour
                            next_tasks.append(successor)

            # Passer au rang suivant
            tasks_without_predecessors = next_tasks
            rank += 1

            # associer les rangs au taches :
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

    def calculate_early_start(self):
        self.set_rank()  # a faire : faire en sorte de n'appeler qu'une fois set_rank pour tt le pgm
        self.order_by_rank()  # Tri des tâches par rang

        for task in self.graph:
            dependencies_dates = []  # correspond a la ligne "dates par predecesseur"
            for dependencie in task.dependencies:
                dependencies_dates.append((dependencie.early_date[0] + task.duration[dependencie.name], dependencie))
            maxi = (0, None)
            for i in range(len(dependencies_dates)):
                if (maxi[1] == None):
                    maxi = dependencies_dates[i]
                if (maxi[0] < dependencies_dates[i][0]):
                    maxi = dependencies_dates[i]
            task.early_date = maxi

    def display_early_start(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tot(origine)':<20}", file=output_file)
        print("-" * 45, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.early_date[0]) + '(' + str(task.early_date[1].name if task.early_date[1] != None else None) + ')':<20}", file=output_file)

    def calculate_late_start(self):

        self.set_rank()
        # Tri des tâches selon leur rang
        self.order_by_rank()

        # Calcul des dates au plus tot si cela n'est pas deja fait
        if self.graph[len(self.graph) -1].early_date == (0, None):
            self.calculate_early_start()

        # Construire les relations de successeurs
        for task in self.graph:
            # Réinitialiser la liste des enfants pour toutes les tâches
            task.children = []
            for children in self.graph:
                if task in children.dependencies:
                    task.set_children(children)

        # Initialisation de la date au plus tard pour la tâche finale
        last_task = self.graph[-1]
        last_task.late_date = (last_task.early_date[0], None)  # Convention: date au plus tard = date au plus tôt

        # Initialisation des autres tâches avec une valeur infinie pour être sûr de prende la valeur calculées
        for task in self.graph[:-1]:  # Toutes les tâches sauf la dernière
            task.late_date = (float('inf'), None)

        # On parcourt les tâches en ordre inverse de rang
        for task in reversed(self.graph):
            # Pour chaque successeur (enfant) de la tâche
            for child in task.children:
                # Date au plus tard du successeur - durée de l'arc entre la tâche actuelle et le successeur
                late_date_via_child = child.late_date[0] - child.duration[task.name]

                # Si cette date est plus petite que la date actuelle, on la met à jour
                if late_date_via_child < task.late_date[0]:
                    task.late_date = (late_date_via_child, child)

    def display_late_start(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tard(origine)':<20}", file=output_file)
        print("-" * 45, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.late_date[0]) + '(' + str(task.late_date[1].name if task.late_date[1] != None else None) + ')':<20}", file=output_file)

    def compute_total_float(self):

        self.calculate_late_start()

        for task in self.graph:
            # recalcul de la marge totale (TF) : TF = LS - ES
            task.total_float = task.late_date[0] - task.early_date[0]

    def display_total_float(self, output_file=None):

        print("\nMargesTotales (TF) des tâches :\n", file=output_file)
        print(f"{'Tâche':<10}{'ES':<10}{'LS':<10}{'TF'}", file=output_file)
        print("-" * 35, file=output_file)

        for task in self.graph:
            print(f"{task.name:<10}{task.late_date[0]:<10}{task.early_date[0]:<10}{task.total_float}", file=output_file)

    def display_critical_path(self, output_file=None):

        critical_path = []

        # Vérifie si les marges sont calculées
        self.compute_total_float()

        # Identification des tâches critiques (marge Totales = 0)
        for task in self.graph:
            if task.total_float == 0:
                critical_path.append(task)

        # Tri des tâches critiques dans l'ordre chronologique (par date au plus tôt)
        critical_path = sorted(critical_path, key=lambda x: x.early_date[0])

        # Affichage du chemin critique
        print("Chemin critique : ", ' -> '.join(task.name for task in critical_path), file=output_file)

    def display_scheduling(self, output_file=None):
        print(f"{'Rang':<10}{'Taches':<10}{'Date au plus tot(origine)':<20}{'Date au plus tard(origine)':<20}{'Marges Totales':<15}", file=output_file)
        print("-" * 55, file=output_file)

        for task in self.graph:
            print(f"{task.rank:<10}{task.name:<10}{str(
                task.early_date[0]) + '(' + str(task.early_date[1].name if task.early_date[1] != None else None) + ')':<20}{str(
                task.late_date[0]) + '(' + str(task.late_date[1].name if task.late_date[1] != None else None) + ')':<20}{task.total_float:<15}", file=output_file)

    def save_results(self, graph_number):

        with open("results/result_graph_"+str(graph_number)+".txt", "w") as f:
            f.write("RESULTATS DU GRAPHE N°"+str(graph_number)+"")

            f.write("\n\nGRAPHE SOUS FORME DE LIGNE\n")
            self.print_graph(f)

            f.write("\n\nMATRICE DE VALEURS\n")
            self.print_matrix(f)

            f.write("\n\nORDONANCEMENT\n")
            graph_copy = deepcopy(self)
            cycle = graph_copy.verify_cycle(False)  # Vérifie l'absence de cycles
            negative = self.check_negative_val(False)  # Vérifie l'absence de valeurs négatives
            if cycle and negative:  # Vérifie que le graphe est bien un graphe d'ordonnancement
                print("✅ Le graphe ne contient aucun cycle et aucune valeur négative, donc c'est un graphe d'ordonnancement.\n", file=f)
            else:
                print("❌ Le graphe contient au un cycle, donc ce n'est pas un graphe d'ordonnancement.\n", file=f)
                return

            f.write("\n\nRANG - DATE AU PLUS TARD - DATE AU PLUS TOT - MARGES\n")
            self.compute_total_float() #appel des fonctions

            self.display_scheduling(f)

            f.write("\n\nCHEMIN CRITIQUE\n")
            self.display_critical_path(f)

        f.close()

