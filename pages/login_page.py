import flet as ft
from dataclasses import asdict
from services.firebase_service import FirebaseService
from models.user_model import User
from theme import BG, INK, MUTED, rounded_card, primary_button, ghost_button

class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login", bgcolor=BG, padding=20)

        self.fb = FirebaseService()

        self.email = ft.TextField(
            label="Correo electrónico",
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=16,
        )
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=16,
        )

        title = ft.Text("Iniciar sesión", size=22, weight=ft.FontWeight.W_700, color=INK)
        hint = ft.Text("Nos alegra verte de nuevo", size=12, color=MUTED)

        form = ft.Column(
            [
                title,
                hint,
                ft.Container(height=20),
                self.email,
                self.password,
                ft.Row(
                    [primary_button("Entrar", self.on_login)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                ghost_button("¿No tienes cuenta? Regístrate", lambda e: e.page.go("/register")),
            ],
            spacing=12,
            tight=True,
        )

        self.controls = [
            ft.Container(
                content=rounded_card(form, 20),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]

    def _toast(self, page: ft.Page, msg: str, error: bool = False):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#E5484D" if error else "#2ECC71")
        page.snack_bar.open = True
        page.update()

    def on_login(self, e: ft.ControlEvent):
        page = e.page
        email = (self.email.value or "").strip()
        password = self.password.value or ""

        if not email or not password:
            self._toast(page, "Ingresa correo y contraseña.", error=True)
            return

        try:
            id_token, uid = self.fb.sign_in(email, password)
            profile = self.fb.get_user_profile(uid) or {}
            user = User(uid=uid, email=email, username=profile.get("username"), id_token=id_token)
            user_dict = asdict(user)

            # Guarda en sesión y también en client_storage (persistencia)
            page.session.set("user", user_dict)
            page.client_storage.set("user", user_dict)

            self._toast(page, f"Bienvenido, {user.username or user.email} 👋")
            page.go("/home")
        except Exception as ex:
            self._toast(page, f"Error: {ex}", error=True)
