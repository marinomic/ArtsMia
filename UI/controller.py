import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {nNodes}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero archi: {nEdges}"))
        self._view.update_page()

    def handleCompConnessa(self, e):
        idOggetto = self._view._txtIdOggetto.value
        try:
            intId = int(idOggetto)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Il valore inserito non è un intero. Inserire un id valido."))
            self._view.update_page()
            return
        if self._model.checkExistence(intId):
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} esiste nel grafo."))
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} NON esiste nel grafo."))

        sizeConnessa = self._model.getCompConnessa(intId)
        self._view._txt_result.controls.append(
                ft.Text(f"La componente connessa che contiene {intId} ha dimensione: {sizeConnessa}")
        )
        # Fill DD with the possible lengths between 2 and the size of the connected component
        # Metodo 1), ciclo classico
        # for i in range(2, sizeConnessa + 1):
        #     self._view._ddLunghezza.add_option(i, str(i))

        # Metodo 2), crea una lista di oggetti myoption che si possono aggiungere al dropdown
        myOptsNum = list(range(2, sizeConnessa + 1))
        myOptsStrDD = list(map(lambda x: ft.dropdown.Option(x), myOptsNum))
        self._view._ddLunghezza.options = myOptsStrDD

        # Oppure
        # for i in range(2, sizeConnessa + 1):
        #     self._view._ddLunghezza.options.append(ft.dropdown.Option(i))
        self._view._ddLunghezza.disabled = False
        self._view._btnCercaOggetti.disabled = False
        self._view.update_page()

    def handleCercaOggetti(self, e):
        """
        Al termine della ricerca, il programma dovrà stampare il cammino, indicando gli oggetti incontrati (ordinati per object_name)
        e il peso totale del cammino trovato.
        """
        pesoMax, percorso = self._model.getBestPath(int(self._view._ddLunghezza.value),
                                                    self._model.getObjFromId(int(self._view._txtIdOggetto.value)))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Cammino trovato con peso massimo {pesoMax}:"))
        for obj in percorso:
            self._view._txt_result.controls.append(ft.Text(f"{obj}"))
        self._view.update_page()
