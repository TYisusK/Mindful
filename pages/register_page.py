# pages/register_page.py
import flet as ft
from services.firebase_service import FirebaseService
from theme import BG, INK, MUTED, rounded_card, primary_button, ghost_button

class RegisterView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/register", bgcolor=BG, padding=20)
        self.page = page
        self.fb = FirebaseService()

        self.name = ft.TextField(label="Nombre", border_radius=16)
        self.email = ft.TextField(label="Correo electrónico", keyboard_type=ft.KeyboardType.EMAIL, border_radius=16)
        self.password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=16)

        self.hint = ft.Text("Crea tu cuenta para comenzar", size=12, color=MUTED)

        form = ft.Column(
            [
                ft.Text("Crear una cuenta", size=22, weight=ft.FontWeight.W_700, color=INK),
                self.hint,
                self.name, self.email, self.password,
                ft.Row(
                    [
                        primary_button("Crear cuenta", self.on_signup),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ghost_button("Volver", lambda _: self.page.go("/")),
            ],
            spacing=12, tight=True,
        )

        self.controls = [ft.Container(
            content=rounded_card(form, pad=20),
            alignment=ft.alignment.center, expand=True
        )]

    def on_signup(self, _):
        username = self.name.value.strip()
        email = self.email.value.strip()
        password = self.password.value

        if not username or not email or not password:
            self.page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."), bgcolor="#E5484D")
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            id_token, uid = self.fb.sign_up(email, password)
            self.fb.create_user_profile(uid, email, username)
            self.page.snack_bar = ft.SnackBar(ft.Text("Cuenta creada ✅"), bgcolor="#2ECC71")
            self.page.snack_bar.open = True
            self.page.update()
            self.page.go("/login")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#E5484D")
            self.page.snack_bar.open = True
            self.page.update()
