import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._graph_creato = False


    def fillDDChromosomes(self):
        chr = self._model.getChromosomes()

        for c in chr:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(c))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(c))

        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()

        if self._view.dd_min_ch.value is None or self._view.dd_max_ch.value is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Attenzione! Inserisci scegli prima il cromosome mancante", color="red"))
            self._view.update_page()
            return

        try:
            c1 = int(self._view.dd_min_ch.value)
            c2 = int(self._view.dd_max_ch.value)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Attenzione! Inserisci scegli un range valido", color="red"))
            self._view.update_page()
            return

        if c1 > c2:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Attenzione! Range non valido.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(c1, c2)

        Nnodes, Nedges = self._model.getGraphDetails()

        if Nnodes == 0:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(
                    f"Nessun grafo trovato",
                    color="red"))
            self._view.update_page()
            return

        self._graph_creato = True

        self._view.txt_result1.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo contiene {Nnodes} nodi e {Nedges} archi"))

        top5 = self._model.getTop5()

        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 nodi col maggior numero di archi uscenti sono:"))

        for t in top5:
            self._view.txt_result1.controls.append(
                ft.Text(f"{t[0]} ---- num. archi uscenti: {t[1]} ---- peso tot: {t[2]}"))

        self._view.update_page()



    def handle_dettagli(self, e):
        pass


    def handle_path(self, e):
        if self._graph_creato == False:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(
                ft.Text("Non ho trovato un grafo su cui calcolare il cammino", color="red"))
            self._view.update_page()
            return

        path, valore = self._model.cerca_cammino()

        if len(path) == 0:  # non ho trovato un cammino
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Non ho trovato un cammino", color="red"))
            self._view.update_page()
            return

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(
            ft.Text("Ecco il cammino più lungo trovato:", color="green"))

        self._view.txt_result2.controls.append(
            ft.Text(f"Il cammino è lungo {len(path)} e pesa {valore}. Questa è la sequenza di nodi:", color="green"))

        for gene in path:
            self._view.txt_result2.controls.append(
                ft.Text(f"{gene.GeneID}"))

        self._view.update_page()