import flet as ft
from pantalla import progreso as prog
from pantalla.db import obtener_usuario
from pantalla.responsive import is_mobile, stack_or_row, content_padding, mobile_bottom_nav

# ── Colores (igual que dashboard) ──
PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
BG        = "#FDFAF3"
GRAY_TEXT = "#777777"
DARK      = "#1A1A1A"
NAV_BG    = "#FFFFFF"
NAVY      = "#1A2C5B"
PURPLE    = "#7B61FF"
AMBER     = "#F5A623"
GREEN     = "#2ECC71"
BLUE      = "#1E88E5"
PINK      = "#FF6B9D"

CENTER = ft.Alignment(0, 0)


def avatar_widget(iniciales, foto_b64=None, size=38, text_size=13):
    """Muestra la foto real del usuario (si existe) o sus iniciales como respaldo."""
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(src=foto_b64, width=size, height=size, fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor="#C9B8F0", alignment=CENTER,
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_700),
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────

def logo_icon():
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


def sidebar_widget(usuario: str, foto_b64=None, on_inicio=None, on_lecciones=None, on_pruebas=None,
                   on_logros=None, on_configuracion=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,        "Home",        False, on_inicio),
        (ft.Icons.MENU_BOOK_ROUNDED,   "Lessons",     False, on_lecciones),
        (ft.Icons.ASSIGNMENT_ROUNDED,  "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,   "Statistics",  True,  None),
        (ft.Icons.EMOJI_EVENTS_ROUNDED,"Achievements",        False, on_logros),
        (ft.Icons.SETTINGS_ROUNDED,    "Settings", False, on_configuracion),
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

def topbar_widget(usuario: str, puntos: int = 0, foto_b64=None, mobile: bool = False):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"

    titulo = ft.Column(spacing=2, controls=[
        ft.Text("Statistics", size=22, weight=ft.FontWeight.W_800, color=DARK),
        ft.Text("Check your learning progress and performance.",
                size=13, color=GRAY_TEXT),
    ])

    puntos_badge = ft.Container(
        content=ft.Row(controls=[
            ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
            ft.Text(f"{puntos} points", size=14, weight=ft.FontWeight.W_700, color=DARK),
        ], spacing=6),
        bgcolor=WHITE, border_radius=24,
        border=ft.Border.all(1, "#EEEEEE"),
        padding=ft.Padding(left=16, right=16, top=8, bottom=8),
        shadow=ft.BoxShadow(blur_radius=6, color="#10000000", offset=ft.Offset(0, 2)),
    )

    avatar = avatar_widget(iniciales, foto_b64, size=44, text_size=15)

    if mobile:
        # Stacked layout on mobile so nothing gets pushed off-screen
        # and cropped (title/avatar on top, points badge below).
        return ft.Container(
            bgcolor=WHITE,
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
            content=ft.Column(spacing=12, controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[titulo, avatar],
                ),
                puntos_badge,
            ]),
        )

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=16, bottom=16),
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


# ── Card de resumen ─────────────────────────────────────────────────────────

def stat_card(title, subtitle, value_text, bg_color, border_color):
    return ft.Container(
        expand=True,
        bgcolor=bg_color,
        border_radius=16,
        border=ft.Border.all(2, border_color),
        padding=ft.Padding(left=20, right=20, top=18, bottom=18),
        shadow=ft.BoxShadow(blur_radius=8, color="#12000000", offset=ft.Offset(0, 3)),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Container(
                    width=46, height=46, border_radius=13,
                    bgcolor="#FFF3C4",
                    alignment=CENTER,
                    content=ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=28),
                ),
                ft.Column(spacing=3, expand=True, controls=[
                    ft.Text(title, size=14, weight=ft.FontWeight.W_800, color=DARK),
                    ft.Text(subtitle, size=11, color=GRAY_TEXT),
                ]),
                ft.Container(
                    bgcolor=border_color,
                    border_radius=20,
                    padding=ft.Padding(left=14, right=14, top=6, bottom=6),
                    content=ft.Text(value_text, size=13, weight=ft.FontWeight.W_800, color=WHITE),
                ),
            ],
        ),
    )


# ── Banner ─────────────────────────────────────────────────────────────────────

def banner_lecciones(completadas: int, total: int, mobile=False):
    return ft.Container(
        bgcolor=AMBER,
        border_radius=16,
        padding=ft.Padding(left=18 if mobile else 28, right=18 if mobile else 28, top=22, bottom=22),
        shadow=ft.BoxShadow(blur_radius=10, color="#22F5A623", offset=ft.Offset(0, 4)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            wrap=True,
            controls=[
                ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color=WHITE, size=32),
                ft.Text(
                    f"You've completed {completadas} of {total} lessons!",
                    size=16 if mobile else 20, weight=ft.FontWeight.W_800, color=WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )


# ── Skills ────────────────────────────────────────────────────────────────

def skill_bar(label: str, pct: int, color: str):
    return ft.Column(spacing=5, controls=[
        ft.Text(label, size=12, color=GRAY_TEXT, weight=ft.FontWeight.W_600),
        ft.Row(spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.ProgressBar(
                expand=True,
                value=pct / 100,
                height=10,
                border_radius=ft.BorderRadius(5, 5, 5, 5),
                bgcolor="#EEEEEE",
                color=color,
            ),
            ft.Text(f"{pct}%", size=12, color=color, weight=ft.FontWeight.W_800),
        ]),
    ])


def habilidades_card():
    return ft.Container(
        expand=True,
        bgcolor=WHITE,
        border_radius=16,
        padding=ft.Padding(left=22, right=22, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 3)),
        content=ft.Column(spacing=14, controls=[
            ft.Text("Skills", size=15, weight=ft.FontWeight.W_800, color=DARK),
            skill_bar("Letter recognition", 75, AMBER),
            skill_bar("Reading fluency",           75, PINK),
            skill_bar("Reading comprehension",        75, PRIMARY),
        ]),
    )


# ── Weekly Activity ──────────────────────────────────────────────────────────

def bar_col(label: str, minutes: int, max_min: int, color: str):
    max_height = 90
    bar_h = max(6, int((minutes / max_min) * max_height)) if max_min > 0 else 6
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Text(f"{minutes} Min", size=10, color=GRAY_TEXT, weight=ft.FontWeight.W_600),
            ft.Container(
                width=38, height=max_height,
                alignment=ft.Alignment(0, 1),
                content=ft.Container(
                    width=38, height=bar_h,
                    border_radius=ft.BorderRadius(top_left=6, top_right=6,
                                                  bottom_left=0, bottom_right=0),
                    bgcolor=color,
                ),
            ),
            ft.Text(label, size=11, color=GRAY_TEXT, weight=ft.FontWeight.W_600),
        ],
    )


def actividad_card():
    semanas = [
        ("Week 1", 50, AMBER),
        ("Week 2", 45, AMBER),
        ("Week 3", 35, AMBER),
    ]
    max_min = max(m for _, m, _ in semanas)
    return ft.Container(
        expand=True,
        bgcolor=WHITE,
        border_radius=16,
        padding=ft.Padding(left=22, right=22, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 3)),
        content=ft.Column(spacing=14, controls=[
            ft.Text("Weekly Activity", size=15, weight=ft.FontWeight.W_800, color=DARK),
            ft.Container(
                bgcolor=BG,
                border_radius=12,
                padding=ft.Padding(left=16, right=16, top=16, bottom=16),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=[bar_col(l, m, max_min, c) for l, m, c in semanas],
                ),
            ),
        ]),
    )


# ── Builder principal ──────────────────────────────────────────────────────────

def build_estadisticas(page: ft.Page, usuario: str, on_inicio=None,
                       on_lecciones=None, on_pruebas=None,
                       on_logros=None, on_configuracion=None):
    progreso_usuario = prog.obtener_progreso(usuario)
    total_lecciones = prog.total_lecciones()
    completadas = prog.contar_completadas(progreso_usuario)
    porcentaje = prog.porcentaje_general(progreso_usuario)
    puntos = progreso_usuario.get("puntos", 0)

    usuario_doc = obtener_usuario(usuario) or {}
    foto_b64 = usuario_doc.get("foto")

    mobile = is_mobile(page)

    main_content = ft.Container(
        expand=True,
        bgcolor=BG,
        content=ft.Column(expand=True, spacing=0, controls=[
            topbar_widget(usuario, puntos=puntos, foto_b64=foto_b64, mobile=mobile),
            ft.Container(
                expand=True,
                content=ft.ListView(
                    expand=True,
                    padding=content_padding(page),
                    spacing=20,
                    controls=[
                        stack_or_row(mobile, spacing=16, controls=[
                            stat_card(
                                "Overall progress",
                                f"You've completed {completadas} of {total_lecciones} lessons.",
                                f"{porcentaje}%",
                                "#FFFDE7",
                                AMBER,
                            ),
                            stat_card(
                                "Total points",
                                "Points earned from completed lessons.",
                                f"{puntos}",
                                "#FFF8E7",
                                AMBER,
                            ),
                        ]),
                        banner_lecciones(completadas, total_lecciones, mobile),
                        stack_or_row(mobile, spacing=16, controls=[
                            habilidades_card(),
                            actividad_card(),
                        ]),
                    ],
                ),
            ),
        ]),
    )

    sidebar = sidebar_widget(usuario, foto_b64, on_inicio=on_inicio,
                             on_lecciones=on_lecciones, on_pruebas=on_pruebas,
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
            mobile_bottom_nav("estadisticas", on_inicio=on_inicio, on_lecciones=on_lecciones,
                               on_pruebas=on_pruebas, on_logros=on_logros,
                               on_configuracion=on_configuracion),
        ])
    return body