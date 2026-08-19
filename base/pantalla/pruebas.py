import flet as ft
from pantalla import progreso as prog
from pantalla.db import obtener_usuario
from pantalla.responsive import is_mobile, stack_or_row, content_padding, mobile_bottom_nav
 
# ── Colores ──

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

ORANGE    = "#FF7043"
 
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
 
 
# ──────────────────────────────────────────────────

#  Componentes reutilizados del dashboard

# ──────────────────────────────────────────────────
 
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
 
 
def sidebar_widget(usuario: str, foto_b64=None, on_inicio=None, on_lecciones=None, on_estadisticas=None, on_logros=None, on_configuracion=None):

    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"

    nav_items = [

        (ft.Icons.HOME_ROUNDED,         "Home",        False, on_inicio),

        (ft.Icons.MENU_BOOK_ROUNDED,    "Lessons",     False, on_lecciones),

        (ft.Icons.ASSIGNMENT_ROUNDED,   "Tests",       True,  None),

        (ft.Icons.BAR_CHART_ROUNDED,    "Statistics",  False, on_estadisticas),

        (ft.Icons.EMOJI_EVENTS_ROUNDED, "Achievements",        False, on_logros),

        (ft.Icons.SETTINGS_ROUNDED,     "Settings", False, on_configuracion),

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

                        ft.Text("DixLearn",      size=16, weight=ft.FontWeight.W_900, color=DARK),

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

                                    ft.Text(usuario,    size=13, weight=ft.FontWeight.W_700, color=DARK),

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
 
 
def topbar_widget(usuario: str, on_lecciones=None, on_estadisticas=None, foto_b64=None, puntos=0):

    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
 
    def nav_btn(icon, label, active=False, on_click=None):

        bg    = AMBER   if active else "transparent"

        color = DARK    if active else GRAY_TEXT

        return ft.Container(

            content=ft.Row(

                controls=[ft.Icon(icon, color=color if not active else DARK, size=18),

                           ft.Text(label, color=DARK, size=14, weight=ft.FontWeight.W_700)],

                spacing=8,

            ),

            bgcolor=bg, border_radius=24, ink=True, on_click=on_click,

            padding=ft.Padding(left=18, right=18, top=10, bottom=10),

        )
 
    return ft.Container(

        bgcolor=WHITE,

        padding=ft.Padding(left=32, right=32, top=14, bottom=14),

        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),

        content=ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                # Logo pequeño (ahora solo DixLearn, sin botones)

                ft.Row(

                    spacing=10,

                    controls=[

                        ft.Container(

                            width=44, height=44, border_radius=12, bgcolor="#F0E8FF", alignment=CENTER,

                            content=ft.Text("📚", size=20),

                        ),

                        ft.Column(

                            spacing=1,

                            controls=[

                                ft.Text("DixLearn", size=15, weight=ft.FontWeight.W_900, color=DARK),

                                ft.Text("Learn differently, learn brilliantly.",

                                        size=10, color=GRAY_TEXT),

                            ],

                        ),

                    ],

                ),

                # ✅ ELIMINADOS: Los botones de Lessons y Statistics

                # ft.Row(...),  <-- ¡Eliminado!

                # Puntos + avatar

                ft.Row(

                    spacing=12,

                    controls=[

                        ft.Container(

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

                        ),

                        avatar_widget(iniciales, foto_b64, size=44, text_size=15),

                    ],

                ),

            ],

        ),

    )
 
 
# ──────────────────────────────────────────────────

#  Componentes propios de Tests

# ──────────────────────────────────────────────────
 
def info_card(icon, icon_bg, title, subtitle, extra=None):

    return ft.Container(

        expand=True, bgcolor=WHITE, border_radius=16,

        padding=ft.Padding(left=20, right=20, top=16, bottom=16),

        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),

        content=ft.Column(

            spacing=10,

            controls=[

                ft.Text(title, size=12, color=GRAY_TEXT, weight=ft.FontWeight.W_600),

                ft.Row(

                    spacing=14,

                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Container(

                            width=44, height=44, border_radius=12,

                            bgcolor=icon_bg, alignment=CENTER,

                            content=ft.Icon(icon, color=WHITE, size=22),

                        ),

                        ft.Column(

                            spacing=2,

                            controls=[

                                ft.Text(subtitle, size=14,

                                        weight=ft.FontWeight.W_700, color=DARK),

                                extra if extra else ft.Container(),

                            ],

                        ),

                    ],

                ),

            ],

        ),

    )
 
 
def circular_score(pct: int, color: str):

    return ft.Stack(

        width=52, height=52,

        controls=[

            ft.ProgressRing(
                width=52, height=52, stroke_width=5,
                value=pct / 100,
                color=color,
                bgcolor="#EEEEEE",
            ),

            ft.Container(

                alignment=CENTER, width=52, height=52,

                content=ft.Text(f"{pct}%", size=11,

                                weight=ft.FontWeight.W_800, color=color),

            ),

        ],

    )
 
 
def result_row(tipo: str, fecha: str, puntaje: int, total: int, color: str,

               icon: ft.Icons, icon_bg: str, mobile: bool = False):

    pct = round(puntaje / total * 100)

    icon_box = ft.Container(

        width=42, height=42, border_radius=12,

        bgcolor=icon_bg, alignment=CENTER,

        content=ft.Icon(icon, color=WHITE, size=20),

    )

    tipo_fecha = ft.Column(

        expand=True, spacing=2,

        controls=[

            ft.Text(tipo,  size=13, weight=ft.FontWeight.W_700, color=DARK,
                     no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),

            ft.Text(fecha, size=11, color=GRAY_TEXT,
                     no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),

        ],

    )

    completado_badge = ft.Container(

        content=ft.Text("Completed", size=11, color=GREEN,

                        weight=ft.FontWeight.W_700, no_wrap=True),

        bgcolor="#E8F8F0", border_radius=20,

        padding=ft.Padding(left=10, right=10, top=5, bottom=5),

    )

    score_col = ft.Column(

        spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END,

        controls=[

            ft.Text("Score", size=10, color=GRAY_TEXT, no_wrap=True),

            ft.Text(f"{puntaje} / {total}", size=13,

                    weight=ft.FontWeight.W_800, color=DARK, no_wrap=True),

        ],

    )

    if mobile:
        # Compact two-line layout on narrow screens so nothing gets
        # squeezed into a single-letter-per-line column.
        return ft.Container(

            bgcolor=WHITE, border_radius=12,

            padding=ft.Padding(left=14, right=14, top=12, bottom=12),

            border=ft.Border.all(1, "#F0F0F0"),

            content=ft.Column(

                spacing=10,

                controls=[

                    ft.Row(

                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                        spacing=12,

                        controls=[icon_box, tipo_fecha, completado_badge],

                    ),

                    ft.Row(

                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            score_col,

                            ft.Row(spacing=6, controls=[

                                circular_score(pct, color),

                                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=20),

                            ]),

                        ],

                    ),

                ],

            ),

        )

    return ft.Container(

        bgcolor=WHITE, border_radius=12,

        padding=ft.Padding(left=16, right=16, top=14, bottom=14),

        border=ft.Border.all(1, "#F0F0F0"),

        content=ft.Row(

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                icon_box,

                ft.Container(width=12),

                tipo_fecha,

                completado_badge,

                ft.Container(width=16),

                score_col,

                ft.Container(width=12),

                circular_score(pct, color),

                ft.Container(width=6),

                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=20),

            ],

        ),

    )
 
 
def proxima_prueba_card(on_ver_detalles=None):

    """Left card with details of the upcoming test."""

    tema = lambda t: ft.Row(

        spacing=8,

        controls=[

            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=GREEN, size=17),

            ft.Text(t, size=13, color=DARK),

        ],

    )

    return ft.Container(

        expand=True, bgcolor=WHITE, border_radius=16,

        padding=ft.Padding(left=24, right=24, top=22, bottom=22),

        shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),

        content=ft.Column(

            spacing=0,

            controls=[

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Text("Next test", size=14,

                                weight=ft.FontWeight.W_800, color=DARK),

                        ft.Container(

                            content=ft.Text("Weekly", size=11,

                                            color=PURPLE, weight=ft.FontWeight.W_700),

                            bgcolor="#EDE7FF", border_radius=20,

                            padding=ft.Padding(left=10, right=10, top=4, bottom=4),

                        ),

                    ],

                ),

                ft.Container(height=14),

                ft.Row(

                    spacing=14,

                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Container(

                            width=46, height=46, border_radius=13,

                            bgcolor="#EDE7FF", alignment=CENTER,

                            content=ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED,

                                            color=PURPLE, size=22),

                        ),

                        ft.Column(

                            spacing=2,

                            controls=[

                                ft.Text("Weekly Test", size=15,

                                        weight=ft.FontWeight.W_800, color=DARK),

                                ft.Text("Test your knowledge for this week.",

                                        size=12, color=GRAY_TEXT),

                            ],

                        ),

                    ],

                ),

                ft.Container(height=18),

                ft.Row(

                    spacing=24,

                    controls=[

                        ft.Row(

                            spacing=8,

                            controls=[

                                ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED,

                                        color=GRAY_TEXT, size=16),

                                ft.Column(

                                    spacing=0,

                                    controls=[

                                        ft.Text("Start date", size=10, color=GRAY_TEXT),

                                        ft.Text("May 20, 2024", size=12,

                                                weight=ft.FontWeight.W_700, color=DARK),

                                    ],

                                ),

                            ],

                        ),

                        ft.Row(

                            spacing=8,

                            controls=[

                                ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED,

                                        color=GRAY_TEXT, size=16),

                                ft.Column(

                                    spacing=0,

                                    controls=[

                                        ft.Text("Duration",    size=10, color=GRAY_TEXT),

                                        ft.Text("45 minutes", size=12,

                                                weight=ft.FontWeight.W_700, color=DARK),

                                    ],

                                ),

                            ],

                        ),

                    ],

                ),

                ft.Container(height=16),

                ft.Text("Topics included", size=12,

                        weight=ft.FontWeight.W_700, color=DARK),

                ft.Container(height=8),

                tema("Letter recognition"),

                ft.Container(height=5),

                tema("Word reading"),

                ft.Container(height=5),

                tema("Reading comprehension"),

                ft.Container(height=20),

                ft.Container(

                    height=46,

                    bgcolor=AMBER,

                    border_radius=14,

                    alignment=CENTER,

                    ink=True,

                    on_click=on_ver_detalles,  # ✅ Conectado al nuevo evento

                    content=ft.Row(

                        alignment=ft.MainAxisAlignment.CENTER,

                        spacing=8,

                        controls=[

                            ft.Text("View test details",

                                    size=14, weight=ft.FontWeight.W_700, color=DARK),

                            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED,

                                    color=DARK, size=18),

                        ],

                    ),

                ),

            ],

        ),

    )
 
 
def resultados_card(mobile=False):

    resultados = [

        ("Weekly Test",     "May 13, 2024",  85, 100, PURPLE, ft.Icons.CALENDAR_TODAY_ROUNDED, "#EDE7FF"),

        ("Weekly Test",     "May 6, 2024",   78, 100, AMBER,  ft.Icons.CALENDAR_TODAY_ROUNDED, "#FFF8E7"),

        ("Monthly Test",     "May 1, 2024",   92, 100, BLUE,   ft.Icons.CALENDAR_TODAY_ROUNDED, "#E3F2FD"),

        ("Quarterly Test",  "April 1, 2024",  88, 100, ORANGE, ft.Icons.CALENDAR_TODAY_ROUNDED, "#FBE9E7"),

    ]

    return ft.Container(

        expand=True, bgcolor=WHITE, border_radius=16,

        padding=ft.Padding(left=24, right=24, top=22, bottom=22),

        shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),

        content=ft.Column(

            spacing=0,

            controls=[

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Text("Previous results", size=14,

                                weight=ft.FontWeight.W_800, color=DARK),

                        ft.Row(

                            spacing=4,

                            controls=[

                                ft.Text("All types", size=12,

                                        color=GRAY_TEXT, weight=ft.FontWeight.W_600),

                                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,

                                        color=GRAY_TEXT, size=18),

                            ],

                        ),

                    ],

                ),

                ft.Container(height=14),

                ft.Column(

                    spacing=10,

                    controls=[result_row(*r, mobile=mobile) for r in resultados],

                ),

            ],

        ),

    )
 
 
def footer_bar(on_estadisticas=None):

    return ft.Container(

        bgcolor=WHITE, border_radius=16,

        padding=ft.Padding(left=28, right=28, top=18, bottom=18),

        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),

        content=ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Row(

                    spacing=14,

                    controls=[

                        ft.Container(

                            width=44, height=44, border_radius=12,

                            bgcolor="#EDE7FF", alignment=CENTER,

                            content=ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED,

                                            color=PURPLE, size=24),

                        ),

                        ft.Column(

                            spacing=2,

                            controls=[

                                ft.Text("You can do it!", size=14,

                                        weight=ft.FontWeight.W_800, color=DARK),

                                ft.Text("Keep preparing and improve your score on every test.",

                                        size=12, color=GRAY_TEXT),

                            ],

                        ),

                    ],

                ),

                ft.Row(

                    spacing=6,

                    controls=[

                        ft.Icon(ft.Icons.TRENDING_UP_ROUNDED, color=GREEN, size=26),

                        ft.Column(

                            spacing=1,

                            controls=[

                                ft.Text("Overall average", size=11, color=GRAY_TEXT),

                                ft.Text("85%", size=22,

                                        weight=ft.FontWeight.W_900, color=DARK),

                            ],

                        ),

                    ],

                ),

                ft.Container(

                    content=ft.Row(

                        spacing=8,

                        controls=[

                            ft.Text("View statistics", size=13,

                                    weight=ft.FontWeight.W_700, color=DARK),

                            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=DARK, size=16),

                        ],

                    ),

                    bgcolor=BG, border_radius=14,

                    border=ft.Border.all(1, "#DDDDDD"),

                    padding=ft.Padding(left=18, right=18, top=11, bottom=11),

                    ink=True,

                    on_click=on_estadisticas,

                ),

            ],

        ),

    )
 
 
# ──────────────────────────────────────────────────

#  Pantalla principal de Tests

# ──────────────────────────────────────────────────
 
def build_pruebas(page: ft.Page, usuario: str, on_inicio=None,

                  on_lecciones=None, on_estadisticas=None, on_logros=None,

                  on_configuracion=None, on_ver_detalles=None):

    """Builds the Tests screen."""
 
    usuario_doc = obtener_usuario(usuario) or {}
    foto_b64 = usuario_doc.get("foto")
    puntos = prog.obtener_progreso(usuario).get("puntos", 0)
    mobile = is_mobile(page)
 
    # Fila superior de info

    info_row = stack_or_row(mobile, spacing=16, controls=[

            info_card(

                icon=ft.Icons.CALENDAR_TODAY_ROUNDED,

                icon_bg=PURPLE,

                title="Your next test",

                subtitle="Weekly Test",

                extra=ft.Row(

                    spacing=5,

                    controls=[

                        ft.Text("Starts in:", size=11, color=GRAY_TEXT),

                        ft.Text("2 days", size=11,

                                color=BLUE, weight=ft.FontWeight.W_700),

                    ],

                ),

            ),

            info_card(

                icon=ft.Icons.CALENDAR_TODAY_ROUNDED,

                icon_bg=AMBER,

                title="Active test type",

                subtitle="Weekly",

                extra=ft.Text("Every week", size=11, color=GRAY_TEXT),

            ),

            info_card(

                icon=ft.Icons.INFO_OUTLINED,

                icon_bg=GREEN,

                title="About the tests",

                subtitle="",

                extra=ft.Text(

                    "Tests are evaluative and have\na score. "

                    "Not part of the lessons.",

                    size=11, color=GRAY_TEXT,

                ),

            ),

        ],

    )
 
    # Cuerpo: próxima prueba + resultados

    body_row = stack_or_row(mobile, spacing=16, controls=[

        proxima_prueba_card(on_ver_detalles=on_ver_detalles),  # ✅ Conectado

        resultados_card(mobile=mobile),

    ])
 
    # Mascota abeja (emoji decorativo)

    bee = ft.Container(

        alignment=ft.Alignment(1, -1),

        content=ft.Image(src="imagenes/abeja.png", width=80, height=80, fit="contain",
                          error_content=ft.Text("🐝", size=80)),

    )
 
    header_row = ft.Stack(

        controls=[

            ft.Container(

                content=ft.Column(

                    spacing=4,

                    controls=[

                        ft.Text("Tests", size=26 if mobile else 34,

                                weight=ft.FontWeight.W_900, color=DARK),

                        ft.Text("Test your knowledge and show what you've learned.",

                                size=13 if mobile else 14, color=GRAY_TEXT),

                    ],

                ),

            ),

            ft.Container(

                alignment=ft.Alignment(1, -1),

                padding=ft.Padding(left=0, right=0, top=0, bottom=0),

                content=ft.Image(src="imagenes/abeja.png", width=76 if mobile else 100, height=76 if mobile else 100, fit="contain",
                                  error_content=ft.Text("🐝", size=76 if mobile else 100)),

            ),

        ],

        height=100,

    )
 
    main_content = ft.Container(

        expand=True, bgcolor=BG,

        content=ft.Column(

            expand=True, spacing=0,

            controls=[

                topbar_widget(usuario,

                              on_lecciones=on_lecciones,

                              on_estadisticas=on_estadisticas,

                              foto_b64=foto_b64,

                              puntos=puntos),

                ft.Container(

                    expand=True,

                    content=ft.ListView(

                        expand=True,

                        padding=content_padding(page),

                        spacing=20,

                        controls=[

                            header_row,

                            info_row,

                            body_row,

                            footer_bar(on_estadisticas),

                        ],

                    ),

                ),

            ],

        ),

    )
 
    sidebar = sidebar_widget(usuario, foto_b64, on_inicio=on_inicio, on_lecciones=on_lecciones,
                             on_estadisticas=on_estadisticas, on_logros=on_logros,
                             on_configuracion=on_configuracion)
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
            mobile_bottom_nav("pruebas", on_inicio=on_inicio, on_lecciones=on_lecciones,
                               on_estadisticas=on_estadisticas, on_logros=on_logros,
                               on_configuracion=on_configuracion),
        ])
    return body
 