import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Exercise on MIA Art database"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self.__theme_switch = None
        self._title = None
        self._btnAnalizzaOggetti = None
        self._btnCompConnessa = None
        self._txtIdOggetto = None
        self._txt_result = None

    def load_interface(self):
        # title
        self.__theme_switch = ft.Switch(label="Dark Theme", on_change=self.theme_changed)
        self._title = ft.Text("The MIA Collection database", color="orange", size=24)
        self._page.controls.append(self.__theme_switch)
        self._page.controls.append(self._title)

        # controls
        self._btnAnalizzaOggetti = ft.ElevatedButton(text="Analizza oggetti",
                                                     on_click=self._controller.handleAnalizzaOggetti,
                                                     bgcolor="orange",
                                                     color="black",
                                                     width=200)
        self._txtIdOggetto = ft.TextField(label="Id Oggetto", color="orange", border_color="orange")
        self._btnCompConnessa = ft.ElevatedButton(text="Cerca Connessa", on_click=self._controller.handleCompConnessa,
                                                  bgcolor="orange",
                                                  color="black",
                                                  width=200)

        self._page.controls.append(ft.Row([self._btnAnalizzaOggetti, self._txtIdOggetto, self._btnCompConnessa],
                                          alignment=ft.MainAxisAlignment.CENTER))

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def theme_changed(self, e):
        """Function that changes the color theme of the app, when the corresponding
        switch is triggered"""
        self._page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self._page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.__theme_switch.label = (
            "Light theme" if self._page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        self.update_page()

    def update_page(self):
        self._page.update()
