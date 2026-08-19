import flet as ft
import sys
import os
import importlib.util

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


db = _cargar_db()  # ← para leer la foto/correo reales del usuario

# ── Colores ──
PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
BG        = "#FDFAF3"
GRAY_TEXT = "#777777"
DARK      = "#1A1A1A"
NAV_BG    = "#FFFFFF"
AMBER     = "#F5A623"
GREEN     = "#2ECC71"
BLUE      = "#1E88E5"
PURPLE    = "#7B61FF"
PURPLE_BG = "#C9B8F0"

CENTER = ft.Alignment(0, 0)


# ── Avatar (foto real o iniciales) ──────────────────────────────────────────

def avatar_widget(iniciales, foto_b64=None, size=64, bg=PURPLE_BG, text_size=24):
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(blur_radius=12, color="#30C9B8F0", offset=ft.Offset(0, 4)),
            content=ft.Image(src=foto_b64, width=size, height=size, fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor=bg, alignment=CENTER,
        shadow=ft.BoxShadow(blur_radius=12, color="#30C9B8F0", offset=ft.Offset(0, 4)),
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_800),
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────

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
        content=ft.Row(controls=[
            ft.Icon(icon, color=color, size=21),
            ft.Text(label, color=color, size=14, weight=w),
        ], spacing=13),
        bgcolor=bg, border_radius=12,
        padding=ft.Padding(left=14, right=14, top=11, bottom=11),
        ink=True, on_click=on_click,
    )


def sidebar_widget(usuario: str, foto_b64=None, on_inicio=None, on_lecciones=None,
                   on_pruebas=None, on_estadisticas=None, on_logros=None,
                   on_configuracion=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,          "Home",        False, on_inicio),
        (ft.Icons.MENU_BOOK_ROUNDED,     "Lessons",     False, on_lecciones),
        (ft.Icons.ASSIGNMENT_ROUNDED,    "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,     "Statistics",  False, on_estadisticas),
        (ft.Icons.EMOJI_EVENTS_ROUNDED,  "Achievements",        False, on_logros),
        (ft.Icons.SETTINGS_ROUNDED,      "Settings", False, on_configuracion),
    ]
    return ft.Container(
        width=205, bgcolor=NAV_BG,
        shadow=ft.BoxShadow(blur_radius=16, color="#18000000", offset=ft.Offset(2, 0)),
        content=ft.Column(spacing=0, expand=True, controls=[
            ft.Container(height=20),
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
                logo_icon(),
                ft.Text("DixLearn", size=16, weight=ft.FontWeight.W_900, color=DARK),
                ft.Text("Makes you learn", size=11, color=GRAY_TEXT),
            ]),
            ft.Container(height=20),
            ft.Column(expand=True, spacing=2,
                      controls=[nav_item_widget(i, l, a, cb) for i, l, a, cb in nav_items]),
            ft.Divider(color="#EEEEEE", height=1),
            ft.Container(
                padding=ft.Padding(left=12, right=12, top=10, bottom=20),
                content=ft.Row(spacing=10, controls=[
                    avatar_widget(iniciales, foto_b64, size=38, text_size=13),
                    ft.Column(spacing=0, expand=True, controls=[
                        ft.Text(usuario, size=13, weight=ft.FontWeight.W_700, color=DARK),
                        ft.Text("Student", size=11, color=GRAY_TEXT),
                    ]),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=18),
                ]),
            ),
        ]),
    )


# ── Topbar ─────────────────────────────────────────────────────────────────────

def topbar_widget(usuario: str, foto_b64=None, puntos=0):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(spacing=2, controls=[
                    ft.Text("My profile", size=24, weight=ft.FontWeight.W_800, color=DARK),
                    ft.Text("Manage your personal information.", size=13, color=GRAY_TEXT),
                ]),
                ft.Row(spacing=12, controls=[
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                            ft.Text(f"{puntos} points", size=14,
                                    weight=ft.FontWeight.W_700, color=DARK),
                        ], spacing=6),
                        bgcolor=WHITE, border_radius=24,
                        border=ft.Border.all(1, "#EEEEEE"),
                        padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                        shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                                            offset=ft.Offset(0, 2)),
                    ),
                    avatar_widget(iniciales, foto_b64, size=44, text_size=15),
                ]),
            ],
        ),
    )


# ── Helpers ────────────────────────────────────────────────────────────────────

def card(content, expand=False, bgcolor=WHITE):
    return ft.Container(
        expand=expand,
        bgcolor=bgcolor,
        border_radius=16,
        border=ft.Border.all(1.5, "#EEEEEE"),
        padding=ft.Padding(left=22, right=22, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#0C000000", offset=ft.Offset(0, 3)),
        content=content,
    )


def divider():
    return ft.Divider(color="#F0F0F0", height=1)


def stat_row(label, value, value_color=DARK, bold=False):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(label, size=12, color=GRAY_TEXT),
            ft.Text(value, size=13,
                    weight=ft.FontWeight.W_800 if bold else ft.FontWeight.W_600,
                    color=value_color),
        ],
    )


def meta_bar(label, actual, total, color):
    pct = min(100, int((actual / total) * 100)) if total else 0
    return ft.Column(spacing=5, controls=[
        ft.Text(label, size=12, color=DARK, weight=ft.FontWeight.W_600),
        ft.Row(spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Container(
                expand=True, height=9, border_radius=5, bgcolor="#EEEEEE",
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Container(
                    width=f"{pct}%", height=9, border_radius=5, bgcolor=color,
                ),
            ),
            ft.Text(f"{actual}/{total}", size=11, color=GRAY_TEXT,
                    weight=ft.FontWeight.W_600),
        ]),
    ])


# ── Card hero (avatar + nombre) ────────────────────────────────────────────

def hero_card(usuario: str, correo: str = "", foto_b64: str = None, on_editar=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    correo_display = correo if correo else f"{usuario.lower().replace(' ', '.')}@gmail.com"

    return card(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                avatar_widget(iniciales, foto_b64, size=80, text_size=28),
                ft.Text(usuario, size=20, weight=ft.FontWeight.W_800, color=DARK),
                # Badge Student
                ft.Container(
                    bgcolor=PURPLE_BG,
                    border_radius=20,
                    padding=ft.Padding(left=18, right=18, top=6, bottom=6),
                    content=ft.Text("Student", size=12,
                                    weight=ft.FontWeight.W_700, color=PURPLE),
                ),
                ft.Container(height=2),
                ft.Text(correo_display, size=12, color=GRAY_TEXT),
                ft.Text("Member since: February 11, 2026",
                        size=11, color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.Container(
                    ink=True, border_radius=20,
                    bgcolor="#FEF0EC",
                    padding=ft.Padding(left=20, right=20, top=8, bottom=8),
                    content=ft.Text("Edit profile", size=12,
                                    weight=ft.FontWeight.W_700, color=PRIMARY),
                    on_click=on_editar,
                ),
            ],
        ),
        bgcolor="#F0EAFF",   # fondo morado suave como en la imagen
    )


# ── Activity summary ───────────────────────────────────────────────────────

def resumen_card():
    return card(
        ft.Column(spacing=0, controls=[
            ft.Text("Activity summary", size=14,
                    weight=ft.FontWeight.W_800, color=DARK),
            ft.Container(height=12),
            stat_row("Completed lessons", "24"),
            divider(),
            ft.Container(height=4),
            stat_row("Tests taken", "18"),
            divider(),
            ft.Container(height=4),
            stat_row("Average score", "85%", value_color=GREEN, bold=True),
            divider(),
            ft.Container(height=4),
            stat_row("Current streak", "12 days", value_color=AMBER, bold=True),
        ]),
        expand=True,
    )


# ── Personal information ───────────────────────────────────────────────────────

def info_row(label, value):
    return ft.Row(spacing=10, controls=[
        ft.Container(width=130,
                     content=ft.Text(label, size=12, color=GRAY_TEXT,
                                     weight=ft.FontWeight.W_600)),
        ft.Text(value, size=12, color=DARK, weight=ft.FontWeight.W_500, expand=True),
    ])


def info_personal_card(usuario: str):
    nombre = usuario
    return card(
        ft.Column(spacing=7, controls=[
            ft.Text("Personal information", size=14,
                    weight=ft.FontWeight.W_800, color=DARK),
            ft.Container(height=4),
            info_row("Full name",    nombre),
            info_row("Date of birth","November 19, 2009"),
            info_row("Country",               "Argentina"),
            info_row("Language",             "Spanish"),
            info_row("Role",                "Student"),
            info_row("Current level",       "Level 2 - Intermediate"),
        ]),
        expand=True,
    )


# ── Personal goals ───────────────────────────────────────────────────────────

def metas_card():
    return card(
        ft.Column(spacing=12, controls=[
            ft.Column(spacing=2, controls=[
                ft.Text("Personal goals", size=14,
                        weight=ft.FontWeight.W_800, color=DARK),
                ft.Text("Your goals help you keep growing.",
                        size=11, color=GRAY_TEXT),
            ]),
            meta_bar("Complete 30 lessons",          12, 30, BLUE),
            meta_bar("Get a 90% average on tests", 12, 30, PRIMARY),
            meta_bar("Keep a 30-day streak",       12, 30, AMBER),
        ]),
        expand=True,
    )


# ── Builder principal ──────────────────────────────────────────────────────────

def build_perfil(page: ft.Page, usuario: str, on_inicio=None,
                 on_lecciones=None, on_pruebas=None, on_estadisticas=None,
                 on_logros=None, on_configuracion=None):

    # ── Traemos los datos reales del usuario (correo y foto) desde Mongo ──
    usuario_doc = db.obtener_usuario(usuario) or {}
    correo = usuario_doc.get("correo", "")
    foto_b64 = usuario_doc.get("foto")
    puntos = prog.obtener_progreso(usuario).get("puntos", 0)

    mobile = is_mobile(page)

    main_content = ft.Container(
        expand=True, bgcolor=BG,
        content=ft.Column(expand=True, spacing=0, controls=[
            topbar_widget(usuario, foto_b64, puntos=puntos),
            ft.Container(
                expand=True,
                content=ft.ListView(
                    expand=True,
                    padding=content_padding(page, top=24),
                    spacing=16,
                    controls=[
                        # Fila 1: hero card (izq) + resumen actividad (der)
                        stack_or_row(mobile, spacing=16, controls=[
                            hero_card(usuario, correo, foto_b64, on_editar=on_configuracion),
                            resumen_card(),
                        ]),
                        # Fila 2: info personal (izq) + metas (der)
                        stack_or_row(mobile, spacing=16, controls=[
                            info_personal_card(usuario),
                            metas_card(),
                        ]),
                    ],
                ),
            ),
        ]),
    )

    sidebar = sidebar_widget(usuario, foto_b64, on_inicio=on_inicio, on_lecciones=on_lecciones,
                             on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                             on_logros=on_logros, on_configuracion=on_configuracion)
    sidebar.visible = not mobile

    body = ft.Row(
        expand=True, spacing=0,
        controls=[
            sidebar,
            main_content,
        ],
    )
    if mobile:
        return ft.Column(expand=True, spacing=0, controls=[
            body,
            mobile_bottom_nav("inicio", on_inicio=on_inicio, on_lecciones=on_lecciones,
                               on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                               on_logros=on_logros, on_configuracion=on_configuracion),
        ])
    return body
