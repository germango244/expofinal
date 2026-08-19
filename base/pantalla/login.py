import flet as ft
from pantalla.db import (
    usuarios_col, hash_password, verificar_password,
    obtener_usuario, registrar_usuario, correo_valido,
)

# ── Colores ──
PRIMARY    = "#D94F2B"
PRIMARY_L  = "#F7A98B"
WHITE      = "#FFFFFF"
BG         = "#FDFAF3"
GRAY_TEXT  = "#777777"
GRAY_LIGHT = "#F5F5F5"
BORDER     = "#E0E0E0"
DARK       = "#1A1A1A"
SUCCESS    = "#2E7D32"
ERROR      = "#E53935"
PURPLE     = "#A084E8"
PURPLE_L   = "#EDE7FF"
CENTER     = ft.Alignment(0, 0)


# ── Widget helpers ────────────────────────────────────────────────────────────
def _field(hint, ref, icon=None, password=False, eye_ref=None, on_toggle=None):
    prefix = ft.Icon(icon, color=GRAY_TEXT, size=18) if icon else None
    suffix = None
    if password and eye_ref is not None:
        suffix = ft.IconButton(ref=eye_ref, icon=ft.Icons.VISIBILITY_OUTLINED,
                               icon_color=GRAY_TEXT, icon_size=18, on_click=on_toggle)
    return ft.TextField(
        ref=ref, hint_text=hint,
        password=password, can_reveal_password=False,
        border=ft.InputBorder.OUTLINE,
        border_color=BORDER, focused_border_color=PURPLE,
        border_radius=10, bgcolor=WHITE,
        height=50, text_size=14,
        content_padding=ft.Padding(left=14, right=14, top=0, bottom=0),
        prefix_icon=icon,
        suffix=suffix,
    )

def _primary_btn(label, on_click):
    return ft.Container(
        ink=True, border_radius=12, on_click=on_click,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
            colors=[PURPLE, "#C084E8"],
        ),
        padding=ft.Padding(left=0, right=0, top=14, bottom=14),
        content=ft.Text(label, color=WHITE, size=15,
                        weight=ft.FontWeight.W_700,
                        text_align=ft.TextAlign.CENTER),
        alignment=CENTER,
        shadow=ft.BoxShadow(blur_radius=12, color="#44A084E8", offset=ft.Offset(0, 4)),
    )

def _social_btn(icon_src, label):
    return ft.Container(
        border_radius=10, border=ft.Border.all(1, BORDER),
        bgcolor=WHITE, ink=True,
        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
        content=ft.Row(spacing=10,
                       alignment=ft.MainAxisAlignment.CENTER,
                       controls=[
                           ft.Image(src=icon_src, width=20, height=20,
                                    error_content=ft.Icon(ft.Icons.LANGUAGE, size=18, color=GRAY_TEXT)),
                           ft.Text(label, size=13, color=DARK,
                                   weight=ft.FontWeight.W_600),
                       ]),
    )

def _divider_or(text="or continue with"):
    return ft.Row(spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                  controls=[
                      ft.Container(expand=True, height=1, bgcolor=BORDER),
                      ft.Text(text, size=12, color=GRAY_TEXT),
                      ft.Container(expand=True, height=1, bgcolor=BORDER),
                  ])

# ── Panel izquierdo ────────────────────────────────────────────────────────────
def _left_panel_login():
    """Left panel of the login screen."""
    return ft.Container(
        expand=True, bgcolor="#FDFAF3",
        border_radius=ft.BorderRadius(20, 0, 0, 20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack(expand=True, controls=[
            # Manchas decorativas
            ft.Container(width=180, height=180, border_radius=90,
                         bgcolor="#FFE0D0", left=-60, top=-40),
            ft.Container(width=120, height=120, border_radius=60,
                         bgcolor="#E8F8F0", right=-30, bottom=60),
            ft.Container(width=80, height=80, border_radius=40,
                         bgcolor="#EDE7FF", left=20, bottom=30),
            ft.Container(
                expand=True,
                padding=ft.Padding(left=40, right=40, top=40, bottom=40),
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        # Logo
                        ft.Row(spacing=8, controls=[
                            ft.Container(width=36, height=36, border_radius=10,
                                         bgcolor="#F0E8FF", alignment=CENTER,
                                         content=ft.Image(src="imagenes/logo.png", width=26, height=26, fit="contain", error_content=ft.Text("📚", size=18))),
                            ft.Row(spacing=0, controls=[
                                ft.Text("Dix", size=22, weight=ft.FontWeight.W_900, color=DARK),
                                ft.Text("Learn", size=22, weight=ft.FontWeight.W_900, color=PRIMARY),
                            ]),
                        ]),
                        ft.Container(expand=True),
                        # Abeja / ilustración
                        ft.Container(
                            alignment=CENTER,
                            content=ft.Image(src="imagenes/abeja.png", width=200, height=200, fit="contain", error_content=ft.Text("🐝", size=140)),
                        ),
                        ft.Container(height=16),
                        ft.Text("DixLearn", size=22, weight=ft.FontWeight.W_900,
                                color=DARK, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=4),
                        ft.Text("Learn differently, learn brilliantly.",
                                size=13, color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                        ft.Container(expand=True),
                    ],
                ),
            ),
        ]),
    )


def _left_panel_register():
    """Left panel of the sign-up screen."""
    return ft.Container(
        expand=True, bgcolor="#FDFAF3",
        border_radius=ft.BorderRadius(20, 0, 0, 20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack(expand=True, controls=[
            ft.Container(width=200, height=200, border_radius=100,
                         bgcolor="#FFE0D0", left=-70, top=-50),
            ft.Container(width=100, height=100, border_radius=50,
                         bgcolor="#EDE7FF", right=-20, top=100),
            ft.Container(width=80, height=80, border_radius=40,
                         bgcolor="#E8F8F0", left=30, bottom=40),
            ft.Container(
                expand=True,
                padding=ft.Padding(left=40, right=40, top=40, bottom=40),
                content=ft.Column(
                    expand=True, spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(spacing=8, controls=[
                            ft.Container(width=36, height=36, border_radius=10,
                                         bgcolor="#F0E8FF", alignment=CENTER,
                                         content=ft.Image(src="imagenes/logo.png", width=26, height=26, fit="contain", error_content=ft.Text("📚", size=18))),
                            ft.Row(spacing=0, controls=[
                                ft.Text("Dix", size=22, weight=ft.FontWeight.W_900, color=DARK),
                                ft.Text("Learn", size=22, weight=ft.FontWeight.W_900, color=PRIMARY),
                            ]),
                        ]),
                        ft.Container(expand=True),
                        ft.Image(src="imagenes/abeja.png", width=120, height=120, fit="contain", error_content=ft.Text("🐝", size=100)),
                        ft.Container(height=12),
                        ft.Text("Welcome to DixLearn!", size=20,
                                weight=ft.FontWeight.W_800, color=DARK,
                                text_align=ft.TextAlign.CENTER),
                        ft.Container(height=6),
                        ft.Text("Create your account and start learning\nin a fun and effective way.",
                                size=13, color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                        ft.Container(expand=True),
                        # Mini feature cards
                        ft.Row(spacing=8, alignment=ft.MainAxisAlignment.CENTER, controls=[
                            ft.Container(
                                bgcolor=WHITE, border_radius=12,
                                padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                                shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                                                    offset=ft.Offset(0, 2)),
                                content=ft.Column(spacing=4,
                                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                  controls=[
                                    ft.Text("📖", size=22),
                                    ft.Text("Learn at your\nown pace", size=9,
                                            color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                                ]),
                            ),
                            ft.Container(
                                bgcolor=WHITE, border_radius=12,
                                padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                                shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                                                    offset=ft.Offset(0, 2)),
                                content=ft.Column(spacing=4,
                                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                  controls=[
                                    ft.Text("🔔", size=22),
                                    ft.Text("Adapted\ncontent", size=9,
                                            color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                                ]),
                            ),
                        ]),
                        ft.Container(height=16),
                    ],
                ),
            ),
        ]),
    )


# ── BUILD LOGIN SCREEN ────────────────────────────────────────────────────────
def build_login_screen(page: ft.Page, on_login_success, on_register_success=None):

    # ── Refs login ──
    ref_correo  = ft.Ref[ft.TextField]()
    ref_pwd     = ft.Ref[ft.TextField]()
    ref_eye     = ft.Ref[ft.IconButton]()
    # ── Refs registro ──
    ref_nombre  = ft.Ref[ft.TextField]()
    ref_apellido= ft.Ref[ft.TextField]()
    ref_r_correo= ft.Ref[ft.TextField]()
    ref_r_pwd   = ft.Ref[ft.TextField]()
    ref_r_eye   = ft.Ref[ft.IconButton]()
    ref_r_cpwd  = ft.Ref[ft.TextField]()
    ref_r_ceye  = ft.Ref[ft.IconButton]()

    panel_ref   = ft.Ref()   # panel derecho (formulario)
    left_ref    =ft.Ref()   # panel izquierdo

    def snack(msg, color=ERROR):
        s = ft.SnackBar(content=ft.Text(msg, color=WHITE), bgcolor=color, open=True)
        page.overlay.append(s)
        page.update()

    # ── Toggle passwords ──
    def toggle_pwd(e):
        tf = ref_pwd.current; tf.password = not tf.password
        ref_eye.current.icon = ft.Icons.VISIBILITY_OFF_OUTLINED if not tf.password else ft.Icons.VISIBILITY_OUTLINED
        page.update()

    def toggle_r_pwd(e):
        tf = ref_r_pwd.current; tf.password = not tf.password
        ref_r_eye.current.icon = ft.Icons.VISIBILITY_OFF_OUTLINED if not tf.password else ft.Icons.VISIBILITY_OUTLINED
        page.update()

    def toggle_r_cpwd(e):
        tf = ref_r_cpwd.current; tf.password = not tf.password
        ref_r_ceye.current.icon = ft.Icons.VISIBILITY_OFF_OUTLINED if not tf.password else ft.Icons.VISIBILITY_OUTLINED
        page.update()

    # ── Acciones ──
    def hacer_login(e):
        correo = (ref_correo.current.value or "").strip()
        pwd    = ref_pwd.current.value or ""
        if not correo or not pwd:
            snack("Fill in all fields.")
            return
        if usuarios_col is None:
            snack("No connection to the database.")
            return
        # buscar por nombre o correo
        doc = usuarios_col.find_one({"$or": [{"nombre": correo}, {"correo": correo.lower()}]})
        if not doc:
            snack("User not found.")
            return
        if not verificar_password(pwd, doc["contrasena"]):
            snack("Incorrect password.")
            return
        on_login_success(doc["nombre"])

    def hacer_registro(e):
        nombre  = (ref_nombre.current.value or "").strip()
        apell   = (ref_apellido.current.value or "").strip()
        correo  = (ref_r_correo.current.value or "").strip().lower()
        pwd     = ref_r_pwd.current.value or ""
        cpwd    = ref_r_cpwd.current.value or ""

        if not nombre or not apell or not correo or not pwd or not cpwd:
            snack("Fill in all fields.")
            return
        if not correo_valido(correo):
            snack("Enter a valid email.")
            return
        if len(pwd) < 4:
            snack("The password must be at least 4 characters long.")
            return
        if pwd != cpwd:
            snack("The passwords don't match.")
            return

        ok, msg = registrar_usuario(nombre, apell, pwd, correo)
        if not ok:
            snack(msg)
            return

        if on_register_success:
            on_register_success(nombre)
        else:
            snack(f"Registration successful! Welcome, {nombre}.", SUCCESS)
            show_login()

    # ── Cambio de pantalla ──
    def show_login(e=None):
        left_ref.current.content  = _left_panel_login()
        panel_ref.current.content = _login_form()
        page.update()

    def show_register(e=None):
        left_ref.current.content  = _left_panel_register()
        panel_ref.current.content = _register_form()
        page.update()

    # ── Formulario LOGIN ──
    def _login_form():
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                # Header
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(),
                        ft.Row(spacing=10, controls=[
                            ft.Text("Already have an account?", size=12, color=GRAY_TEXT),
                            ft.Container(
                                ink=True, border_radius=20,
                                border=ft.Border.all(1.5, PRIMARY),
                                padding=ft.Padding(left=16, right=16, top=7, bottom=7),
                                on_click=show_login,
                                content=ft.Text("Log in", size=12,
                                                color=PRIMARY, weight=ft.FontWeight.W_700),
                            ),
                        ]),
                    ],
                ),
                ft.Container(height=32),
                ft.Text("Log in", size=26, weight=ft.FontWeight.W_800, color=DARK,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.Text("Welcome back. We're glad to see you",
                        size=13, color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                ft.Container(height=28),
                # Username
                ft.Text("Username", size=12, color=DARK,
                        weight=ft.FontWeight.W_600),
                ft.Container(height=6),
                _field("Enter your username", ref_correo,
                       icon=ft.Icons.PERSON_OUTLINED),
                ft.Container(height=16),
                # Password
                ft.Text("Password", size=12, color=DARK, weight=ft.FontWeight.W_600),
                ft.Container(height=6),
                _field("Enter your password", ref_pwd, icon=ft.Icons.LOCK_OUTLINED,
                       password=True, eye_ref=ref_eye, on_toggle=toggle_pwd),
                ft.Container(height=6),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Text("Forgot your password?", size=11,
                                color=PURPLE, weight=ft.FontWeight.W_600),
                    ],
                ),
                ft.Container(height=24),
                _primary_btn("Log in", hacer_login),
                ft.Container(height=16),
                _divider_or(),
                ft.Container(height=12),
                ft.Row(
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            ink=True, on_click=show_register,
                            content=ft.Text("Sign up", size=12, color=PRIMARY,
                                            weight=ft.FontWeight.W_700),
                        ),
                    ],
                ),
                ft.Container(height=12),
                _social_btn("imagenes/google.png", "Continue with Google"),
                ft.Container(height=8),
                _social_btn("imagenes/apple.png", "Continue with Apple"),
                ft.Container(height=24),
            ],
        )

    # ── Formulario REGISTRO ──
    def _register_form():
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(),
                        ft.Row(spacing=10, controls=[
                            ft.Text("Already have an account?", size=12, color=GRAY_TEXT),
                            ft.Container(
                                ink=True, border_radius=20,
                                border=ft.Border.all(1.5, PRIMARY),
                                padding=ft.Padding(left=16, right=16, top=7, bottom=7),
                                on_click=show_login,
                                content=ft.Text("Log in", size=12,
                                                color=PRIMARY, weight=ft.FontWeight.W_700),
                            ),
                        ]),
                    ],
                ),
                ft.Container(height=20),
                ft.Text("Create account", size=24, weight=ft.FontWeight.W_800, color=DARK),
                ft.Container(height=4),
                ft.Text("Join DixLearn and start your learning journey.",
                        size=12, color=GRAY_TEXT),
                ft.Container(height=20),
                # First name + Last name en fila
                ft.Row(spacing=12, controls=[
                    ft.Column(expand=True, spacing=5, controls=[
                        ft.Text("First name", size=12, color=DARK, weight=ft.FontWeight.W_600),
                        _field("Enter your first name", ref_nombre,
                               icon=ft.Icons.PERSON_OUTLINED),
                    ]),
                    ft.Column(expand=True, spacing=5, controls=[
                        ft.Text("Last name", size=12, color=DARK, weight=ft.FontWeight.W_600),
                        _field("Enter your last name", ref_apellido,
                               icon=ft.Icons.PERSON_OUTLINED),
                    ]),
                ]),
                ft.Container(height=12),
                ft.Text("Email", size=12, color=DARK, weight=ft.FontWeight.W_600),
                ft.Container(height=5),
                _field("Enter your email", ref_r_correo,
                       icon=ft.Icons.EMAIL_OUTLINED),
                ft.Container(height=12),
                ft.Text("Password", size=12, color=DARK, weight=ft.FontWeight.W_600),
                ft.Container(height=5),
                _field("Create a password", ref_r_pwd, icon=ft.Icons.LOCK_OUTLINED,
                       password=True, eye_ref=ref_r_eye, on_toggle=toggle_r_pwd),
                ft.Container(height=5),
                ft.Text("At least 4 characters, with uppercase, lowercase, and numbers.",
                        size=10, color=GRAY_TEXT),
                ft.Container(height=12),
                ft.Text("Confirm password", size=12, color=DARK, weight=ft.FontWeight.W_600),
                ft.Container(height=5),
                _field("Confirm your password", ref_r_cpwd, icon=ft.Icons.LOCK_OUTLINED,
                       password=True, eye_ref=ref_r_ceye, on_toggle=toggle_r_cpwd),
                ft.Container(height=14),
                ft.Row(spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Checkbox(value=False, active_color=PURPLE),
                    ft.Row(spacing=4, controls=[
                        ft.Text("I agree to the", size=11, color=GRAY_TEXT),
                        ft.Text("Terms and Conditions", size=11, color=PURPLE,
                                weight=ft.FontWeight.W_600),
                        ft.Text("and the", size=11, color=GRAY_TEXT),
                        ft.Text("Privacy Policy", size=11, color=PURPLE,
                                weight=ft.FontWeight.W_600),
                    ]),
                ]),
                ft.Container(height=18),
                _primary_btn("Create account", hacer_registro),
                ft.Container(height=12),
                _divider_or(),
                ft.Container(height=8),
                ft.Row(spacing=6, alignment=ft.MainAxisAlignment.CENTER, controls=[
                    ft.Container(
                        ink=True, on_click=show_login,
                        content=ft.Text("Sign up", size=12, color=PRIMARY,
                                        weight=ft.FontWeight.W_700),
                    ),
                ]),
                ft.Container(height=16),
            ],
        )

    # ── Layout principal ───────────────────────────────────────────────────────
    left_container = ft.Container(
        ref=left_ref,
        expand=True,
        content=_left_panel_login(),
    )

    # Modo exclusivo para teléfono: siempre se usa el layout angosto,
    # sin el panel izquierdo, sin importar el ancho de la ventana.
    is_mobile = True
    right_panel = ft.Container(
        ref=panel_ref,
        width=None if is_mobile else 460,
        expand=is_mobile,
        bgcolor=WHITE,
        border_radius=20 if is_mobile else ft.BorderRadius(0, 20, 20, 0),
        padding=ft.Padding(left=20 if is_mobile else 40, right=20 if is_mobile else 40, top=24, bottom=24),
        content=_login_form(),
    )

    card = ft.Container(
        width=None,
        height=None,
        expand=is_mobile,
        border_radius=20,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(blur_radius=40, color="#28000000", offset=ft.Offset(0, 12)),
        content=ft.Row(spacing=0, expand=True, controls=[
            ft.Container(left_container, visible=not is_mobile, expand=True),
            right_panel,
        ]),
    )

    return ft.Container(
        key="login",
        expand=True,
        image=ft.DecorationImage(src="imagenes/fondo.png", fit="cover"),
        content=ft.Stack(expand=True, controls=[
            ft.Container(expand=True, bgcolor="#33F5F0E8",
                         content=ft.Stack(expand=True, controls=[
                             ft.Container(expand=True,
                                          blur=ft.Blur(sigma_x=10, sigma_y=10)),
                         ])),
            ft.Row(expand=True, alignment=ft.MainAxisAlignment.CENTER,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER,
                   controls=[card]),
        ]),
    )