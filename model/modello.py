import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._allGenes = []
        self._idMapGenes = {}

        self.best_path = []
        self.best_score = 0.0


    def getChromosomes(self):
            return DAO.getAllChromosomes()


    def buildGraph(self, min, max):
        self._graph.clear()

        self._allGenes = DAO.getAllNodes(min, max)
        for g in self._allGenes:
            self._idMapGenes[(g.GeneID, g.Function)] = g

        self._graph.add_nodes_from(self._allGenes)

        self._archi = DAO.getAllEdges(min, max, self._idMapGenes)

        for tupla in self._archi:
            gene1 = tupla[0]
            gene2 = tupla[1]

            if gene1.Chromosome < gene2.Chromosome:
                self._graph.add_edge(gene1, gene2, weight=tupla[2])

            if gene1.Chromosome > gene2.Chromosome:
                self._graph.add_edge(gene2, gene1, weight=tupla[2])

            if gene1.Chromosome == gene2.Chromosome:
                self._graph.add_edge(gene1, gene2, weight=tupla[2])
                self._graph.add_edge(gene2, gene1, weight=tupla[2])


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getTop5(self):
        lista = []

        for u in self._graph.nodes:
            # Chiediamo a networkx di calcolare la somma dei pesi
            peso_uscenti = self._graph.out_degree(u, weight='weight')
            # peso_entranti = self._graph.in_degree(u, weight='weight')
            num = len(self._graph.out_edges(u))
            lista.append((u, num, peso_uscenti))

        lista_ordinata = sorted(lista, key=lambda x: x[1], reverse=True)[:5]

        return lista_ordinata





    # PUNTO 2

    def cerca_cammino(self):
        self.best_path = []
        self.best_score = 0.0

        for nodo in self._graph.nodes:
            nodo_partenza = nodo
            parziale = [nodo_partenza]
            self._ricorsione_path(parziale)

        return self.best_path, self.best_score

    def _ricorsione_path(self, parziale):
        # 1. VALUTAZIONE SOLUZIONE E AGGIORNAMENTO BEST

        # 1.a --> massimizzare la lunghezza
        if len(parziale) > len(self.best_path):
            self.best_path = copy.deepcopy(parziale)  # FONDAMENTALE:  una COPIA !
            score = 0
            for i in range(len(parziale) - 1):
                u = parziale[i]
                v = parziale[i + 1]
                score += self._graph[u][v]['weight']
            self.best_score = score

        if len(parziale) == len(self.best_path):

            # 1.b --> minimizzare il peso
            peso_corrente = 0
            for i in range(len(parziale) - 1):
                u = parziale[i]
                v = parziale[i + 1]
                peso_corrente += self._graph[u][v]['weight']

            if peso_corrente < self.best_score:
                self.best_score = peso_corrente
                self.best_path = list(parziale)

        # 2. ESTRAZIONE ULTIMO NODO E RICERCA VICINI

        ultimo_nodo = parziale[-1]

        for vicino in self._graph.successors(
                ultimo_nodo):  # self._graph.successors se DiGraph() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if vicino not in parziale:  # Evita di ripassare sugli stessi nodi (niente cicli)

                # 3. FILTRO DI VALIDITÀ DELLA TRACCIA (DA ADATTARE ALL'ESAME!)
                is_valid = True

                # VARIANTE 1A: Vincolo sull'arco (es. peso crescente)
                if len(parziale) == 1:
                    is_valid = True  # Il primo arco va sempre bene
                else:
                    penultimo_nodo = parziale[-2]
                    peso_vecchio = self._graph[penultimo_nodo][ultimo_nodo]['weight']
                    peso_nuovo = self._graph[ultimo_nodo][vicino]['weight']

                    # LO BLOCCO SOLO SE DECRESCE STRETTAMENTE!
                    if peso_nuovo < peso_vecchio:
                        is_valid = False

                # VARIANTE 1B: Vincolo sul nodo
                if vicino.Essential == ultimo_nodo.Essential:
                    is_valid = False

                # 4. BACKTRACKING
                if is_valid:
                    parziale.append(vicino)
                    self._ricorsione_path(parziale)
                    parziale.pop()  # Torno indietro








