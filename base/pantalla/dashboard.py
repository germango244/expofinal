import flet as ft
from pantalla import progreso as prog
from pantalla.db import obtener_usuario
from pantalla.responsive import is_mobile, stack_or_row, content_padding, mobile_bottom_nav

# ── Colores ──
PRIMARY    = "#D94F2B"
WHITE      = "#FFFFFF"
BG         = "#FDFAF3"
GRAY_TEXT  = "#777777"
DARK       = "#1A1A1A"
NAV_BG     = "#FFFFFF"
NAVY       = "#1A2C5B"
PURPLE     = "#7B61FF"
AMBER      = "#F5A623"
GREEN      = "#2ECC71"
BLUE       = "#1E88E5"

CENTER = ft.Alignment(0, 0)


def avatar_widget(iniciales, foto_b64=None, size=38, text_size=13, on_click=None):
    """Muestra la foto real del usuario (si existe) o sus iniciales como respaldo."""
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ink=on_click is not None, on_click=on_click,
            content=ft.Image(src=foto_b64, width=size, height=size, fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor="#C9B8F0", alignment=CENTER,
        ink=on_click is not None, on_click=on_click,
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_700),
    )


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
        bgcolor=bg,
        border_radius=12,
        padding=ft.Padding(left=14, right=14, top=11, bottom=11),
        ink=True,
        on_click=on_click,
    )


def sidebar_widget(usuario: str, foto_b64=None, on_lecciones=None, on_pruebas=None, on_estadisticas=None, on_logros=None, on_configuracion=None):
    """Dashboard sidebar."""
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,          "Home",        True,  None),
        (ft.Icons.MENU_BOOK_ROUNDED,     "Lessons",     False, on_lecciones),
        (ft.Icons.ASSIGNMENT_ROUNDED,    "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,     "Statistics",  False, on_estadisticas),
        (ft.Icons.EMOJI_EVENTS_ROUNDED,  "Achievements",        False, on_logros),
        (ft.Icons.SETTINGS_ROUNDED,      "Settings", False, on_configuracion),
    ]
    return ft.Container(
        width=205,
        bgcolor=NAV_BG,
        shadow=ft.BoxShadow(blur_radius=16, color="#18000000", offset=ft.Offset(2, 0)),
        content=ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Container(height=20),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    controls=[
                        logo_icon(),
                        ft.Text("DixLearn", size=16, weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text("Makes you learn", size=11, color=GRAY_TEXT),
                    ],
                ),
                ft.Container(height=20),
                ft.Column(
                    expand=True,
                    spacing=2,
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
                                spacing=0,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=18),
                        ],
                        spacing=10,
                    ),
                ),
            ],
        ),
    )


def topbar_widget(usuario: str, puntos: int = 0, foto_b64=None, on_perfil=None):
    """Dashboard topbar."""
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(f"Hello, {usuario}! 👋",
                                size=22, weight=ft.FontWeight.W_800, color=DARK),
                        ft.Text("Continue your learning where you left off.",
                                size=13, color=GRAY_TEXT),
                    ],
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                                    ft.Text(f"{puntos} puntos", size=14,
                                            weight=ft.FontWeight.W_700, color=DARK),
                                ],
                                spacing=6,
                            ),
                            bgcolor=WHITE,
                            border_radius=24,
                            border=ft.Border.all(1, "#EEEEEE"),
                            padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                            shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                                                offset=ft.Offset(0, 2)),
                        ),
                        avatar_widget(iniciales, foto_b64, size=44, text_size=15, on_click=on_perfil),
                    ],
                ),
            ],
        ),
    )


def hero_section(mobile=False):
    """Hero section with multicolor title."""
    letter_size = 44 if mobile else 54
    dix = ft.Text("Dix", size=letter_size, weight=ft.FontWeight.W_900, color=NAVY)
    learn_letters = [
        ft.Text("L", size=letter_size, weight=ft.FontWeight.W_900, color=AMBER),
        ft.Text("e", size=letter_size, weight=ft.FontWeight.W_900, color="#E53935"),
        ft.Text("a", size=letter_size, weight=ft.FontWeight.W_900, color=GREEN),
        ft.Text("r", size=letter_size, weight=ft.FontWeight.W_900, color=PURPLE),
        ft.Text("n", size=letter_size, weight=ft.FontWeight.W_900, color=BLUE),
    ]

    brand_row = ft.Row(
        controls=[dix, *learn_letters],
        spacing=0,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER if mobile else ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    hero_text = ft.Column(
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.START,
        controls=[
            brand_row,
            ft.Text("Learn differently, learn brilliantly.",
                    size=18, weight=ft.FontWeight.W_800, color=DARK,
                    text_align=ft.TextAlign.CENTER if mobile else ft.TextAlign.START),
            ft.Container(height=4),
            ft.Text(
                "DixLearn is here to help you discover your potential,\n"
                "strengthen your skills and reach your goals, your way.",
                size=13, color=GRAY_TEXT,
                text_align=ft.TextAlign.CENTER if mobile else ft.TextAlign.START,
            ),
        ],
    )

    bee_px = 200 if mobile else 220
    bee_image = ft.Container(
        width=bee_px, height=bee_px,
        content=ft.Image(
            src="imagenes/abeja.png",
            width=bee_px,
            height=bee_px,
            fit="contain",
            error_content=ft.Text("🐝", size=80 if mobile else 120),
        ),
        alignment=ft.Alignment(1, 1),
    )

    dashed_circle = ft.Container(
        width=70, height=70,
        border=ft.Border.all(1.5, "#CCCCCC"),
        border_radius=35,
        opacity=0.3,
        bottom=10, right=200 if not mobile else 100,
    )

    bee_area = ft.Stack(
        width=240 if mobile else 300,
        height=190 if mobile else 210,
        controls=[
            ft.Container(
                top=0, right=15,
                width=54, height=54, border_radius=27,
                bgcolor=WHITE, alignment=CENTER,
                shadow=ft.BoxShadow(blur_radius=10, color="#1A000000", offset=ft.Offset(0, 3)),
                content=ft.Image(
                    src="imagenes/logo.png", width=42, height=42, fit="contain",
                    error_content=ft.Text("📚", size=22),
                ),
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                top=30, right=55,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.CIRCLE_OUTLINED, color="#C9B8F0", size=10),
                bottom=85, right=45,
            ),
            dashed_circle,
            ft.Container(
                content=bee_image,
                bottom=0, right=0,
            ),
        ],
    )

    if mobile:
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                hero_text,
                ft.Container(content=bee_area, alignment=CENTER),
            ],
        )

    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(content=hero_text, expand=True),
            bee_area,
        ],
    )


def progress_card(title, subtitle, pct, bar_color, icon_widget):
    """Progress card."""
    return ft.Container(
        expand=True,
        bgcolor=WHITE,
        border_radius=16,
        padding=ft.Padding(left=18, right=18, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=14, color="#10000000", offset=ft.Offset(0, 4)),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                icon_widget,
                ft.Column(
                    expand=True,
                    spacing=5,
                    controls=[
                        ft.Text(title, size=13, weight=ft.FontWeight.W_800, color=DARK),
                        ft.Text(subtitle, size=12, color=GRAY_TEXT),
                        ft.Row(
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.ProgressBar(
                                    expand=True,
                                    value=pct / 100,
                                    height=9,
                                    border_radius=ft.BorderRadius(5, 5, 5, 5),
                                    bgcolor="#EEEEEE",
                                    color=bar_color,
                                ),
                                ft.Text(f"{pct}%", size=12,
                                        color=bar_color, weight=ft.FontWeight.W_800),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def progress_row_widget(mobile=False):
    """Progress card row."""
    icon1 = ft.Container(
        width=58, height=58,
        border_radius=14,
        bgcolor="#FFF3DE",
        alignment=CENTER,
        content=ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color=AMBER, size=28),
    )
    icon2 = ft.Container(
        width=58, height=58,
        border_radius=14,
        bgcolor="#EDE7FF",
        alignment=CENTER,
        content=ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, color=PURPLE, size=28),
    )
    return stack_or_row(mobile, spacing=16, controls=[
        progress_card("Current lesson",        "Reading comprehension", 75, AMBER,  icon1),
        progress_card("Assessment test",  "Your overall progress", 60, PURPLE, icon2),
    ])


def cat_card(label, desc, icon, bg_color, icon_bg, label_color, on_click=None):
    """Category card."""
    return ft.Container(
        expand=True,
        bgcolor=bg_color,
        border_radius=16,
        padding=ft.Padding(left=18, right=18, top=18, bottom=18),
        ink=True,
        on_click=on_click,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    width=48, height=48,
                    border_radius=14,
                    bgcolor=icon_bg,
                    alignment=CENTER,
                    content=ft.Icon(icon, color=WHITE, size=24),
                ),
                ft.Text(label, size=14, weight=ft.FontWeight.W_800, color=label_color),
                ft.Text(desc, size=11.5, color=GRAY_TEXT),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=label_color, size=18),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
        ),
    )


def cat_row_widget(on_lecciones=None, on_pruebas=None, on_estadisticas=None, mobile=False):
    """Category row (2x2 grid on phone, one row of 4 on wider screens)."""
    cards = [
        cat_card("Lessons",    "Explore resources and activities designed for you.",
                 ft.Icons.MENU_BOOK_ROUNDED,      "#EDE7FF", PURPLE,  PURPLE, on_click=on_lecciones),
        cat_card("Games",       "Have fun while improving your reading, writing, and more.",
                 ft.Icons.SPORTS_ESPORTS_ROUNDED, "#E8F8F0", GREEN,   GREEN),
        cat_card("Tests",      "Evaluate your skills and get recommendations.",
                 ft.Icons.ASSIGNMENT_ROUNDED,     "#FEF0EC", PRIMARY, PRIMARY, on_click=on_pruebas),
        cat_card("Statistics", "Track your progress and celebrate every achievement.",
                 ft.Icons.BAR_CHART_ROUNDED,      "#FFF8E7", AMBER,   AMBER, on_click=on_estadisticas),
    ]
    if mobile:
        return ft.Column(spacing=14, controls=[
            ft.Row(spacing=14, controls=[cards[0], cards[1]]),
            ft.Row(spacing=14, controls=[cards[2], cards[3]]),
        ])
    return ft.Row(spacing=14, controls=cards)


def for_all_card(mobile=False):
    """Card "Para todos"."""
    def item(icon, color, lines):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(icon, color=color, size=30),
                ft.Text(lines, size=11.5, color=GRAY_TEXT,
                        text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_600),
            ],
        )
    icon_items = [
        item(ft.Icons.PEOPLE_ROUNDED,          "#5B9BD5",
             "Students\nof all ages"),
        item(ft.Icons.FAMILY_RESTROOM,          GREEN,
             "Parents\nand families"),
        item(ft.Icons.ACCOUNT_BALANCE_ROUNDED,  AMBER,
             "Educational\ncenters"),
        item(ft.Icons.PSYCHOLOGY_ROUNDED,       PURPLE,
             "Psychologists and\nprofessionals"),
    ]
    content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            ft.Text("DixLearn is for everyone",
                    size=15, weight=ft.FontWeight.W_800, color=DARK,
                    text_align=ft.TextAlign.CENTER),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=28 if mobile else 40,
                wrap=True,
                run_spacing=18,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=icon_items,
            ),
        ],
    )
    return ft.Container(
        bgcolor=WHITE,
        border_radius=16,
        padding=ft.Padding(left=18 if mobile else 28, right=18 if mobile else 28, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=content,
    )


def build_dashboard(page: ft.Page, usuario: str, on_lecciones=None, on_pruebas=None, on_estadisticas=None, on_logros=None, on_configuracion=None, on_perfil=None):
    """Builds the dashboard screen."""
    progreso_usuario = prog.obtener_progreso(usuario)
    puntos = progreso_usuario.get("puntos", 0)

    usuario_doc = obtener_usuario(usuario) or {}
    foto_b64 = usuario_doc.get("foto")

    mobile = is_mobile(page)

    main_content = ft.Container(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(src="imagenes/fondo.png", fit="cover"),
                ),
                ft.Container(
                    expand=True,
                    blur=ft.Blur(sigma_x=5, sigma_y=5),
                ),
                ft.Container(expand=True, bgcolor="#60F9F3CC"),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        topbar_widget(usuario, puntos=puntos, foto_b64=foto_b64, on_perfil=on_perfil),
                        ft.Container(
                            expand=True,
                            content=ft.ListView(
                                expand=True,
                                padding=content_padding(page),
                                spacing=20,
                                controls=[
                                    hero_section(mobile),
                                    progress_row_widget(mobile),
                                    cat_row_widget(on_lecciones=on_lecciones, on_pruebas=on_pruebas, on_estadisticas=on_estadisticas, mobile=mobile),
                                    for_all_card(mobile),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    sidebar = sidebar_widget(usuario, foto_b64, on_lecciones=on_lecciones, on_pruebas=on_pruebas, on_estadisticas=on_estadisticas, on_logros=on_logros, on_configuracion=on_configuracion)
    sidebar.visible = not mobile

    body = ft.Row(
        expand=True,
        spacing=0,
        controls=[sidebar, main_content],
    )
    if mobile:
        return ft.Column(expand=True, spacing=0, controls=[
            body,
            mobile_bottom_nav("inicio", on_lecciones=on_lecciones, on_pruebas=on_pruebas,
                               on_estadisticas=on_estadisticas, on_logros=on_logros,
                               on_configuracion=on_configuracion),
        ])
    return body