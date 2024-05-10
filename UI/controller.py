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
            self._view._txt_result.controls.append(ft.Text("Il valore inserito non è un intero. Inserire un id valido."))
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
        self._view.update_page()


