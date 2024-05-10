import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._artObjectList = DAO().getAllObjects()
        self._grafo.add_nodes_from(self._artObjectList)
        self._idMap = {obj.object_id: obj for obj in self._artObjectList}

    def buildGraph(self):
        self.addEdges()

    def addEdges(self):
        # self._grafo.edges.clear()
        # Soluzione 1: Ciclare sui nodi, conviene quando ho pochi nodi (in questo caso la tabella objects sul db conta 8500 righe)
        # for u in self._artObjectList:
        #     for v in self._artObjectList:
        #         edge_weight = DAO.getWeight(u, v)
        #         self._grafo.add_edge(u, v, weight=edge_weight)
        # Soluzione 2: una sola query
        allEdges = DAO.getAllConnessioni(self._idMap)
        for edge in allEdges:
            self._grafo.add_edge(edge.u, edge.v, weight=edge.weight)

    def getNumNodes(self):
        return self._grafo.number_of_nodes()

    def getNumEdges(self):
        return self._grafo.number_of_edges()

    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap

# Per calcolare la componente connessa conviene usare DFS e siccome ci interessano i numeri di vertici che la compongono
# come richiesto nella traccia, non conviene utilizzare dfs_edges perchè restituisce solo gli archi del grafo. Proviamo
# invece a utilizzare
# 1) dfs_successors che restituisce un dizionario con i successori di ogni nodo visitato.
# 2) dfs_predecessors che restituisce un dizionario con i predecessori di ogni nodo visitato.
# 3) dfs_tree che restituisce un albero di copertura del grafo.
# 4) node_connected_component che restituisce la componente connessa di un nodo.
# Siccome il grafo non è orientato, prendere i successori o i predecessori è indifferente. L'unica differenza è che
# dfs_successors restituisce un dizionario con come chiave un nodo e come valore una lista di tutti i suoi successori
# (vedi debug per capire meglio) mentre dfs_predecessors ha come valore per ogni chiave il singolo nodo predecessore,
# siccome il noto in chiave sarà stato raggiunto da un solo altro nodo.
# Facendo il testModel e debuggando len(successors.values) e len(predecessors.values) si nota quindi che il numero
# risultante è minore per i predecessori rispetto ai successori(perchè gli elementi values di successori sono liste di nodi).
    def getCompConnessa(self, idOggetto):
        # return nx.node_connected_component(self._grafo, self._idMap[idOggetto])
        #  Metodo 1) dfs_successors
        v0 = self._idMap[idOggetto]
        # Per separare i nodi memorizzati nelle liste e metterli separatamente tutti in'unica lista uso il metodo extend
        # che prende come argomento un iterabile e lo aggiunge alla lista.
        allSucc = []
        successors = nx.dfs_successors(self._grafo, v0)
        for v in successors.values():
            allSucc.extend(v)
        print(f"Metodo 1 (succ): {len(allSucc)}")

        # Metodo 2) dfs_predecessors
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"Metodo 2 (pred): {len(predecessors.values())}")

        # Metodo 3) dfs_tree
        tree = nx.dfs_tree(self._grafo, v0)  # restituisce un albero di copertura del grafo, contiene anche il nodo source, q
        # quindi risulterà avere un nodo in più rispetto ai precedenti metodi
        print(f"Metodo 3 (tree): {len(tree.nodes)}")

        # Metodo 4) node_connected_component
        compCon = nx.node_connected_component(self._grafo, v0)  # restituisce un set di nodi, anche questo contiene il nodo source
        print(f"Metodo 4 (node_connected_component): {len(compCon)}")

        return len(compCon)  # restituisco il numero di nodi della componente connessa, come richiesto nella traccia
