import flet as ft
import asyncio
import base64
import sys
import os
import importlib.util
from pantalla import progreso as prog
from pantalla.responsive import is_mobile, stack_or_row, content_padding, mobile_bottom_nav


def _cargar_db():
    """Busca db.py subiendo carpetas desde este archivo hasta encontrarlo,
    sin depender de si está 1, 2 o 3 niveles arriba."""
    directorio = os.path.dirname(os.path.abspath(__file__))
    buscados = []
    for _ in range(6):
        candidato = os.path.join(directorio, "db.py")
        buscados.append(candidato)
        if os.path.isfile(candidato):
            spec = importlib.util.spec_from_file_location("db", candidato)
            modulo = importlib.util.module_from_spec(spec)
            sys.modules["db"] = modulo
            spec.loader.exec_module(modulo)
            return modulo
        nuevo_directorio = os.path.dirname(directorio)
        if nuevo_directorio == directorio:  # llegamos a la raíz del disco
            break
        directorio = nuevo_directorio
    raise ModuleNotFoundError(
        "No pude encontrar db.py. Busqué en estas rutas:\n" + "\n".join(buscados)
    )


db = _cargar_db()  # ← usamos las funciones reales de db.py (Mongo)

# ── Colores ──
PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
BG        = "#FDFAF3"
GRAY_TEXT = "#777777"
DARK      = "#1A1A1A"
NAV_BG    = "#FFFFFF"
PURPLE    = "#7B61FF"
PURPLE_BG = "#C9B8F0"
AMBER     = "#F5A623"
GREEN     = "#2ECC71"
BLUE      = "#1E88E5"
ERROR     = "#E53935"

CENTER = ft.Alignment(0, 0)


# ══════════════════════════════════════════════════════════════════════════════
#  LOGO
# ══════════════════════════════════════════════════════════════════════════════
def logo_icon():
    """Real DixLearn logo (with emoji fallback if the image fails to load)."""
    return ft.Container(
        width=64, height=64, border_radius=18, bgcolor="#F0E8FF", alignment=CENTER,
        content=ft.Image(
            src="imagenes/logo.png", width=52, height=52, fit="contain",
            error_content=ft.Text("📚", size=24),
        ),
    )


def nav_item_widget(icon, label, active, on_click=None):
    bg    = "#FFF3C4" if active else "transparent"
    color = DARK      if active else GRAY_TEXT
    w     = ft.FontWeight.W_700 if active else ft.FontWeight.W_500
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=color, size=21),
                ft.Text(label, color=color, size=14, weight=w),
            ],
            spacing=13,
        ),
        bgcolor=bg, border_radius=12,
        padding=ft.Padding(left=14, right=14, top=11, bottom=11),
        ink=True, on_click=on_click,
    )


def avatar_widget(iniciales, foto_b64=None, size=56, bg=PURPLE_BG, text_size=20):
    """Muestra la foto real (si existe) o las iniciales como respaldo."""
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(src=foto_b64, width=size, height=size,
                              fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor=bg, alignment=CENTER,
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_700),
    )


def sidebar_widget(usuario, foto_b64=None, on_inicio=None, on_lecciones=None, on_pruebas=None,
                   on_estadisticas=None, on_logros=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,         "Home",        False, on_inicio),
        (ft.Icons.MENU_BOOK_ROUNDED,    "Lessons",     False, on_lecciones),
        (ft.Icons.ASSIGNMENT_ROUNDED,   "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,    "Statistics",  False, on_estadisticas),
        (ft.Icons.EMOJI_EVENTS_ROUNDED, "Achievements",        False, on_logros),
        (ft.Icons.SETTINGS_ROUNDED,     "Settings", True,  None),
    ]
    return ft.Container(
        width=205, bgcolor=NAV_BG,
        shadow=ft.BoxShadow(blur_radius=16, color="#18000000", offset=ft.Offset(2, 0)),
        content=ft.Column(
            spacing=0, expand=True,
            controls=[
                ft.Container(height=20),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
                    controls=[
                        logo_icon(),
                        ft.Text("DixLearn", size=16, weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text("Makes you learn", size=11, color=GRAY_TEXT),
                    ],
                ),
                ft.Container(height=20),
                ft.Column(
                    expand=True, spacing=2,
                    controls=[nav_item_widget(i, l, a, cb) for i, l, a, cb in nav_items],
                ),
                ft.Divider(color="#EEEEEE", height=1),
                ft.Container(
                    padding=ft.Padding(left=12, right=12, top=10, bottom=20),
                    content=ft.Row(
                        controls=[
                            avatar_widget(iniciales, foto_b64, size=38, text_size=13),
                            ft.Column(
                                controls=[
                                    ft.Text(usuario, size=13, weight=ft.FontWeight.W_700, color=DARK),
                                    ft.Text("Student", size=11, color=GRAY_TEXT),
                                ],
                                spacing=0, expand=True,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=18),
                        ],
                        spacing=10,
                    ),
                ),
            ],
        ),
    )


def topbar_widget(usuario, foto_b64=None, puntos=0, mobile=False):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"

    titulo = ft.Column(
        spacing=2,
        controls=[
            ft.Text("Settings", size=22,
                    weight=ft.FontWeight.W_800, color=DARK),
            ft.Text("Customize your experience on DixLearn.",
                    size=13, color=GRAY_TEXT),
        ],
    )

    puntos_badge = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                ft.Text(f"{puntos} points", size=14,
                        weight=ft.FontWeight.W_700, color=DARK),
            ],
            spacing=6,
        ),
        bgcolor=WHITE, border_radius=24,
        border=ft.Border.all(1, "#EEEEEE"),
        padding=ft.Padding(left=16, right=16, top=8, bottom=8),
        shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                            offset=ft.Offset(0, 2)),
    )

    avatar = avatar_widget(iniciales, foto_b64, size=44, text_size=15)

    if mobile:
        # Stacked layout on mobile so the avatar never gets pushed
        # off the edge of the screen and cropped.
        return ft.Container(
            bgcolor=WHITE,
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[titulo, avatar],
                    ),
                    puntos_badge,
                ],
            ),
        )

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=14, bottom=14),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                titulo,
                ft.Row(spacing=12, controls=[puntos_badge, avatar]),
            ],
        ),
    )


def seccion_card(title, controls_list):
    return ft.Container(
        bgcolor=WHITE, border_radius=16,
        padding=ft.Padding(left=24, right=24, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.W_800, color=DARK),
                ft.Divider(color="#EEEEEE", height=1),
                *controls_list,
            ],
        ),
    )


def fila_dropdown(icon, label, opciones, valor_inicial, color=GRAY_TEXT):
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(op) for op in opciones],
        value=valor_inicial,
        text_size=12,
        height=40,
        width=160,
        border_radius=8,
        bgcolor="#F5F5F5",
    )
    return ft.Container(
        padding=ft.Padding(left=8, right=8, top=10, bottom=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Icon(icon, color=color, size=20),
                        ft.Text(label, size=13, color=DARK, weight=ft.FontWeight.W_600),
                    ],
                ),
                dropdown,
            ],
        ),
    )


def fila_expansible(icon, label, contenido_texto, color=GRAY_TEXT):
    expandible = ft.Container(
        visible=False,
        padding=ft.Padding(left=40, right=16, top=8, bottom=8),
        content=ft.Text(contenido_texto, size=12, color=GRAY_TEXT),
    )

    def toggle_expansible(e):
        expandible.visible = not expandible.visible
        e.page.update()

    return ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                ink=True, border_radius=10, on_click=toggle_expansible,
                padding=ft.Padding(left=8, right=8, top=10, bottom=10),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.Icon(icon, color=color, size=20),
                                ft.Text(label, size=13, color=DARK, weight=ft.FontWeight.W_600),
                            ],
                        ),
                        ft.Icon(ft.Icons.EXPAND_MORE, color=GRAY_TEXT, size=20),
                    ],
                ),
            ),
            expandible,
        ]
    )


def build_configuracion(page: ft.Page, usuario: str, on_inicio=None, on_lecciones=None,
                         on_pruebas=None, on_estadisticas=None, on_logros=None, on_logout=None,
                         on_perfil_actualizado=None):
    """
    on_perfil_actualizado(nuevo_usuario: str, nueva_foto_b64: str | None):
        Llamado después de guardar cambios de perfil que afectan al nombre y/o
        la foto, para que la pantalla que llama (tu router / main.py) pueda
        actualizar el 'usuario' que tiene guardado en su estado y reconstruir
        las demás pantallas (sidebar, topbar, perfil...) con el valor nuevo.
    """

    # Estado local mutable (para poder cambiarlo dentro de las funciones anidadas)
    estado = {
        "usuario": usuario,
        "foto_pendiente": None,   # base64 nuevo (aún no guardado)
    }

    usuario_doc = db.obtener_usuario(usuario) or {}
    estado["foto_pendiente"] = usuario_doc.get("foto")  # foto actual, si existe
    puntos_actuales = prog.obtener_progreso(usuario).get("puntos", 0)

    def iniciales_de(nombre):
        return "".join([p[0].upper() for p in nombre.split()[:2]]) if nombre else "U"

    # ── Referencias a sidebar/topbar para poder refrescarlos sin recargar toda la página ──
    sidebar_ctrl = sidebar_widget(estado["usuario"], estado["foto_pendiente"],
                                   on_inicio=on_inicio, on_lecciones=on_lecciones,
                                   on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                                   on_logros=on_logros)
    mobile_actual = is_mobile(page)
    sidebar_ctrl.visible = not mobile_actual
    topbar_ctrl = topbar_widget(estado["usuario"], estado["foto_pendiente"], puntos=puntos_actuales, mobile=mobile_actual)

    def refrescar_sidebar_topbar():
        nuevo_sidebar = sidebar_widget(estado["usuario"], estado["foto_pendiente"],
                                        on_inicio=on_inicio, on_lecciones=on_lecciones,
                                        on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                                        on_logros=on_logros)
        nuevo_sidebar.visible = sidebar_ctrl.visible
        nuevo_topbar = topbar_widget(estado["usuario"], estado["foto_pendiente"],
                                    puntos=prog.obtener_progreso(estado["usuario"]).get("puntos", 0),
                                    mobile=is_mobile(page))
        sidebar_ctrl.content = nuevo_sidebar.content
        topbar_ctrl.content = nuevo_topbar.content

    def notificar(mensaje, color=DARK):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=WHITE),
            bgcolor=color, duration=2800, behavior=ft.SnackBarBehavior.FLOATING,
        )
        page.snack_bar.open = True
        page.update()

    # ── 1. PERFIL EDITABLE ──
    nombre_ctrl = ft.TextField(
        label="Full name", value=usuario, text_size=13, dense=True, height=50, border_radius=10
    )
    email_ctrl = ft.TextField(
        label="Email", value=usuario_doc.get("correo", ""), text_size=13, dense=True,
        height=50, border_radius=10,
    )

    # ── Selector de foto de perfil ──
    avatar_preview = avatar_widget(iniciales_de(usuario), estado["foto_pendiente"], size=56, text_size=20)

    avatar_container = ft.Container(
        width=56, height=56, border_radius=28,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=avatar_preview.content,
    )

    # ── FilePicker como "Service" (arquitectura nueva de Flet): se registra en
    # page.services (o page.overlay como respaldo en versiones más viejas) y
    # pick_files() se usa con await, devolviendo el resultado directo. ──
    file_picker = ft.FilePicker()
    if hasattr(page, "services"):
        page.services.append(file_picker)
    else:
        page.overlay.append(file_picker)

    async def elegir_foto(e):
        resultado = await file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"],
            with_data=True,   # trae los bytes directo, necesario en modo web/navegador
        )
        if not resultado:
            return
        # Según la versión de Flet, pick_files() devuelve directamente la lista
        # de archivos, o un objeto con un atributo .files. Soportamos ambos.
        archivos = resultado.files if hasattr(resultado, "files") else resultado
        if not archivos:
            return
        archivo = archivos[0]
        try:
            # Preferimos los bytes que ya vienen en el objeto (with_data=True);
            # si no están, caemos a leer del path local (modo escritorio).
            datos = getattr(archivo, "bytes", None)
            if not datos and getattr(archivo, "path", None):
                with open(archivo.path, "rb") as f:
                    datos = f.read()
            if not datos:
                notificar("Could not read the selected image ❌", ERROR)
                return
            # límite de seguridad ~4MB para no pasarnos del límite de documento de Mongo
            if len(datos) > 4 * 1024 * 1024:
                notificar("Image is too large (max 4MB) ❌", ERROR)
                return
            b64 = base64.b64encode(datos).decode("utf-8")
            estado["foto_pendiente"] = b64
            nuevo_avatar = avatar_widget(iniciales_de(nombre_ctrl.value or usuario), b64, size=56, text_size=20)
            avatar_container.content = nuevo_avatar.content
            page.update()
            notificar("Photo loaded — click 'Save changes' to keep it ✅", GREEN)
        except Exception as ex:
            notificar(f"Could not load image: {ex}", ERROR)

    btn_cambiar_foto = ft.Container(
        ink=True, border_radius=8,
        padding=ft.Padding(left=14, right=14, top=8, bottom=8),
        bgcolor="#F5F5F5",
        content=ft.Row(spacing=6, controls=[
            ft.Icon(ft.Icons.PHOTO_CAMERA_ROUNDED, color=PURPLE, size=16),
            ft.Text("Change photo", size=12, color=DARK, weight=ft.FontWeight.W_600),
        ]),
        on_click=elegir_foto,
    )

    btn_guardar = ft.Container(
        height=42, border_radius=10, bgcolor=PRIMARY,
        alignment=CENTER, ink=True,
        content=ft.Text("Save changes", size=14, color=WHITE, weight=ft.FontWeight.W_700),
    )

    async def guardar_perfil(e):
        nuevo_nombre = (nombre_ctrl.value or "").strip()
        nuevo_correo = (email_ctrl.value or "").strip()

        if not nuevo_nombre:
            notificar("Name cannot be empty ❌", ERROR)
            return
        if nuevo_correo and not db.correo_valido(nuevo_correo):
            notificar("That email doesn't look valid ❌", ERROR)
            return

        usuario_actual = estado["usuario"]

        # 1) Renombrar si cambió el nombre (nombre = identificador único en Mongo)
        if nuevo_nombre != usuario_actual:
            ok, msg = db.renombrar_usuario(usuario_actual, nuevo_nombre)
            if not ok:
                notificar(msg, ERROR)
                return
            usuario_actual = nuevo_nombre
            estado["usuario"] = nuevo_nombre

        # 2) Actualizar correo y/o foto si cambiaron
        cambios = {}
        if nuevo_correo and nuevo_correo != usuario_doc.get("correo", ""):
            cambios["correo"] = nuevo_correo
        if estado["foto_pendiente"] != usuario_doc.get("foto"):
            cambios["foto"] = estado["foto_pendiente"]

        if cambios:
            ok, msg = db.actualizar_usuario(usuario_actual, cambios)
            if not ok:
                notificar(msg, ERROR)
                return

        # actualizamos la "foto original" en memoria para futuras comparaciones
        usuario_doc["correo"] = nuevo_correo
        usuario_doc["foto"] = estado["foto_pendiente"]
        usuario_doc["nombre"] = usuario_actual

        # feedback visual del botón
        btn_guardar.bgcolor = GREEN
        btn_guardar.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=WHITE, size=20),
                ft.Text("Saved!", size=14, color=WHITE, weight=ft.FontWeight.W_700)
            ],
            alignment=ft.MainAxisAlignment.CENTER, spacing=8,
        )
        refrescar_sidebar_topbar()
        page.update()

        notificar("Profile updated successfully! ✅", DARK)

        if on_perfil_actualizado:
            on_perfil_actualizado(usuario_actual, estado["foto_pendiente"])

        await asyncio.sleep(2)
        btn_guardar.bgcolor = PRIMARY
        btn_guardar.content = ft.Text("Save changes", size=14, color=WHITE, weight=ft.FontWeight.W_700)
        page.update()

    btn_guardar.on_click = guardar_perfil

    perfil_card = ft.Container(
        bgcolor=WHITE, border_radius=16,
        padding=ft.Padding(left=24, right=24, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Text("Profile", size=14, weight=ft.FontWeight.W_800, color=DARK),
                ft.Divider(color="#EEEEEE", height=1),
                ft.Row(
                    spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        avatar_container,
                        ft.Column(spacing=6, expand=True, controls=[
                            ft.Text("Edit your personal information", size=12, color=GRAY_TEXT),
                            btn_cambiar_foto,
                        ]),
                    ],
                ),
                nombre_ctrl,
                email_ctrl,
                btn_guardar,
            ],
        ),
    )

    # ── 2. PREFERENCIAS CON DROPDOWNS ──
    preferencias_card = seccion_card("Learning preferences", [
        fila_dropdown(ft.Icons.TUNE_ROUNDED, "Difficulty level",
                      ["Beginner", "Intermediate", "Advanced"], "Intermediate", PURPLE),
        fila_dropdown(ft.Icons.STYLE_ROUNDED, "Learning style",
                      ["Visual", "Auditory", "Kinesthetic"], "Visual", BLUE),
        fila_dropdown(ft.Icons.FLAG_ROUNDED, "Study goal",
                      ["Improve reading", "Increase speed", "Comprehension"], "Improve reading", GREEN),
    ])

    # ── 3. NOTIFICACIONES ──
    notificaciones_card = seccion_card("Notifications", [
        ft.Container(
            padding=ft.Padding(left=8, right=8, top=6, bottom=6),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Icon(ft.Icons.ALARM_ROUNDED, color=AMBER, size=20),
                        ft.Text("Session reminders", size=13, color=DARK, weight=ft.FontWeight.W_600),
                    ]),
                    ft.Switch(value=True, active_color=PRIMARY),
                ],
            ),
        ),
        ft.Container(
            padding=ft.Padding(left=8, right=8, top=6, bottom=6),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Icon(ft.Icons.ASSESSMENT_ROUNDED, color=PURPLE, size=20),
                        ft.Text("Test results", size=13, color=DARK, weight=ft.FontWeight.W_600),
                    ]),
                    ft.Switch(value=True, active_color=PRIMARY),
                ],
            ),
        ),
    ])

    # ── 4. SEGURIDAD Y CONTRASEÑA ──
    pass_actual = ft.TextField(label="Current password", password=True, can_reveal_password=True, text_size=13, dense=True, height=50, border_radius=10)
    pass_nueva = ft.TextField(label="New password", password=True, can_reveal_password=True, text_size=13, dense=True, height=50, border_radius=10)
    pass_confirmar = ft.TextField(label="Confirm new password", password=True, can_reveal_password=True, text_size=13, dense=True, height=50, border_radius=10)

    async def actualizar_password(e):
        usuario_actual = estado["usuario"]
        doc = db.obtener_usuario(usuario_actual)

        if doc is None:
            notificar("Could not find your user account ❌", ERROR)
            return

        if not db.verificar_password(pass_actual.value or "", doc.get("contrasena", "")):
            notificar("Current password is incorrect ❌", ERROR)
            return

        if not pass_nueva.value or len(pass_nueva.value) < 6:
            notificar("New password must be at least 6 characters ❌", ERROR)
            return

        if pass_nueva.value != pass_confirmar.value:
            notificar("The passwords don't match ❌", ERROR)
            return

        ok, msg = db.actualizar_usuario(usuario_actual, {"contrasena": db.hash_password(pass_nueva.value)})
        if not ok:
            notificar(msg, ERROR)
            return

        notificar("Password updated successfully ✅", GREEN)
        pass_actual.value = ""
        pass_nueva.value = ""
        pass_confirmar.value = ""
        page.update()

    btn_password = ft.Container(
        height=42, border_radius=10, bgcolor=DARK,
        alignment=CENTER, ink=True, on_click=actualizar_password,
        content=ft.Text("Update password", size=14, color=WHITE, weight=ft.FontWeight.W_700),
    )

    seguridad_card = seccion_card("Security", [
        ft.Text("Change password", size=13, weight=ft.FontWeight.W_700, color=DARK),
        pass_actual,
        pass_nueva,
        pass_confirmar,
        btn_password,
    ])

    # ── 5. AYUDA Y SOPORTE (EXPANSIBLE) ──
    ayuda_card = seccion_card("Help and support", [
        fila_expansible(ft.Icons.HELP_OUTLINE_ROUNDED, "How do I use DixLearn?",
                        "1. Go to Lessons to get started.\n2. Complete the tests to measure your progress.\n3. Check your stats weekly.", BLUE),
        fila_expansible(ft.Icons.QUIZ_ROUNDED, "Frequently asked questions",
                        "Q: Is it free? A: Yes, all basic features are.\nQ: Can I change my level? A: Yes, in Preferences.", PURPLE),
        ft.Container(
            ink=True, border_radius=10,
            padding=ft.Padding(left=8, right=8, top=10, bottom=10),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(ft.Icons.SUPPORT_AGENT_ROUNDED, color=GREEN, size=20),
                    ft.Text("Contact support by email", size=13, color=DARK, weight=ft.FontWeight.W_600),
                ],
            ),
            on_click=lambda e: page.launch_url("mailto:soporte@dixlearn.com"),
        ),
    ])

    # ── 6. CUENTA ──
    cuenta_card = seccion_card("Account", [
        ft.Container(
            ink=True, border_radius=10, on_click=on_logout,
            padding=ft.Padding(left=8, right=8, top=10, bottom=10),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=PRIMARY, size=20),
                    ft.Text("log out", size=13, color=PRIMARY, weight=ft.FontWeight.W_700),
                ],
            ),
        ),
        ft.Container(
            ink=True, border_radius=10,
            padding=ft.Padding(left=8, right=8, top=10, bottom=10),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, color=ERROR, size=20),
                    ft.Text("Delete account", size=13, color=ERROR, weight=ft.FontWeight.W_700),
                ],
            ),
        ),
    ])

    # ── Layout 2 columnas (se apilan en celular) ──
    mobile = is_mobile(page)
    col_izq = ft.Column(
        spacing=16, expand=True,
        controls=[perfil_card, preferencias_card, seguridad_card],
    )
    col_der = ft.Column(
        spacing=16, expand=True,
        controls=[notificaciones_card, ayuda_card, cuenta_card],
    )

    main_content = ft.Container(
        expand=True, bgcolor=BG,
        content=ft.Column(
            expand=True, spacing=0,
            controls=[
                topbar_ctrl,
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        padding=content_padding(page),
                        spacing=20,
                        controls=[
                            stack_or_row(mobile, spacing=16, controls=[col_izq, col_der]),
                        ],
                    ),
                ),
            ],
        ),
    )

    sidebar_ctrl.visible = not mobile

    body = ft.Row(
        expand=True, spacing=0,
        controls=[
            sidebar_ctrl,
            main_content,
        ],
    )
    if mobile:
        return ft.Column(expand=True, spacing=0, controls=[
            body,
            mobile_bottom_nav("configuracion", on_inicio=on_inicio, on_lecciones=on_lecciones,
                               on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                               on_logros=on_logros),
        ])
    return body
