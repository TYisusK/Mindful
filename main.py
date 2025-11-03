# main.py
import flet as ft
from dotenv import load_dotenv
from pages.splash_view import SplashView
from pages.welcome_page import WelcomeView
from pages.register_page import RegisterView
from pages.login_page import LoginView
from pages.home_page import HomeView
from pages.diagnostic_page import DiagnosticView
from pages.notes_page import NotesView
from pages.note_editor_page import NoteEditorView
from pages.recommendations_page import RecommendationsView
from pages.tellme_page import TellMeView
from pages.stats_page import StatsView

load_dotenv()

def main(page: ft.Page):
    page.title = "Mindful"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_min_width = 360
    page.window_min_height = 640
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    def route_change(_):
        page.views.clear()
        r = page.route or "/splash"

        if r == "/splash":
            page.views.append(SplashView(page))
        elif r == "/":
            page.views.append(WelcomeView(page))
        elif r == "/register":
            page.views.append(RegisterView(page))
        elif r == "/login":
            page.views.append(LoginView(page))
        elif r == "/home":
            page.views.append(HomeView(page))
        elif r == "/diagnostic":
            page.views.append(DiagnosticView(page))
        elif r.startswith("/notes"):
            page.views.append(NotesView(page))
        elif r.startswith("/note_new") or r.startswith("/note_edit"):
            page.views.append(NoteEditorView(page))
        elif r.startswith("/recommendations"):
            page.views.append(RecommendationsView(page))
        elif r.startswith("/tellme"):
            page.views.append(TellMeView(page))
        elif r.startswith("/stats"):
            page.views.append(StatsView(page))
        else:
            page.views.append(WelcomeView(page))
        page.update()

    def view_pop(_):
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # Arranca en splash para evitar parpadeos
    page.go("/splash")

if __name__ == "__main__":
    # Asegúrate de que "assets" es el folder con logo.png
    ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)
