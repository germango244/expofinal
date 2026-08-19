import flet as ft
import math

# ── Paleta exacta ──────────────────────────────────────────────────────────
PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
BG        = "#FDFAF3"
SEC2_BG   = "#E8EAF0"
SEC3_BG   = "#EAE4F5"
SEC5_BG   = "#EFF4FF"
FOOTER_BG = "#FFF8E7"
DARK      = "#1A1A1A"
GRAY      = "#777777"
NAVY      = "#1A2C5B"
PURPLE    = "#7B61FF"
AMBER     = "#F5A623"
GREEN     = "#2ECC71"
BLUE      = "#1E88E5"
RED       = "#E53935"

# Usamos esta constante segura para el centro en toda la app
CENTER_ALIGN = ft.Alignment(0, 0)

# ── Rutas de imágenes (relativas a assets_dir) ────────────────────────────
IMG_BEE       = "imagenes/abeja.png"
IMG_LOGO      = "imagenes/logo.png"
IMG_GAMEPAD   = "imagenes/control.png"
IMG_CLIPBOARD = "imagenes/listo.png"
IMG_STUDENT   = "imagenes/nino.png"
IMG_FAMILY    = "imagenes/familia.png"
IMG_SCHOOL    = "imagenes/escuela.png"
IMG_PSYCH     = "imagenes/psicologa.png"
IMG_PORTFOLIO = "imagenes/portafolio.png"
IMG_BOOK      = "imagenes/libro.png"


# ── Utilidades ─────────────────────────────────────────────────────────────

def badge_circle(letter, bg, size=18, fs=9):
    return ft.Container(
        width=size, height=size, border_radius=size // 2,
        bgcolor=bg, alignment=CENTER_ALIGN,
        content=ft.Text(letter, size=fs, weight=ft.FontWeight.W_900, color=WHITE),
    )


def num_badge(n, color=AMBER):
    return ft.Container(
        width=36, height=36, border_radius=18,
        bgcolor=color, alignment=CENTER_ALIGN,
        content=ft.Text(str(n), size=16, weight=ft.FontWeight.W_900, color=WHITE),
    )


def hline(color, h=9, w=None):
    return ft.Container(
        height=h, border_radius=5, bgcolor=color,
        width=w, expand=(w is None),
    )


def deco_icon(icon, color, size=26, box=54, opacity=0.16,
              top=None, left=None, right=None, bottom=None, rotate=0.0):
    """Small floating decorative icon bubble for section backgrounds."""
    return ft.Container(
        top=top, left=left, right=right, bottom=bottom,
        rotate=ft.Rotate(rotate),
        width=box, height=box, border_radius=box / 2,
        bgcolor=color, opacity=opacity, alignment=CENTER_ALIGN,
        content=ft.Icon(icon, color=color, size=size),
    )


def deco_dot(color, size=14, opacity=0.35,
             top=None, left=None, right=None, bottom=None):
    """Tiny solid decorative dot."""
    return ft.Container(
        top=top, left=left, right=right, bottom=bottom,
        width=size, height=size, border_radius=size / 2,
        bgcolor=color, opacity=opacity,
    )


def asset_image(src, width, height, fallback_emoji, fallback_size=60):
    """Image with emoji fallback if it fails to load."""
    return ft.Image(
        src=src,
        width=width,
        height=height,
        fit="contain",
        error_content=ft.Text(fallback_emoji, size=fallback_size),
    )


# ══════════════════════════════════════════════════════════════════════════
#  LOGO PROFESIONAL (Integrado desde confusable_letters_logo.py)
# ══════════════════════════════════════════════════════════════════════════

def logo_widget(size: float = 120) -> ft.Container:
    """
    Official DixLearn logo widget (real image), with the same
    circular frame and shadow as the hand-drawn version.
    """
    base_size = 280
    scale = size / base_size

    return ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        bgcolor="#FFFFFF",
        alignment=CENTER_ALIGN,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20 * scale,
            color="#1F000000",  # Equivalente a 12% de opacidad en negro
            offset=ft.Offset(0, 6 * scale),
        ),
        content=ft.Image(
            src=IMG_LOGO,
            width=size * 0.82,
            height=size * 0.82,
            fit="contain",
            error_content=ft.Text("📚", size=size * 0.4),
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  SECCIÓN 1 — HERO  (texto a la DERECHA, más grande)
# ══════════════════════════════════════════════════════════════════════════

def hero_section(on_comenzar, on_login, mobile=False):

    btn_comenzar = ft.Container(
        content=ft.Row(
            spacing=10, alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Get started", color=WHITE,
                        weight=ft.FontWeight.W_700, size=15 if mobile else 17),
                ft.Text("→", color=WHITE, size=15 if mobile else 17),
            ],
        ),
        bgcolor=AMBER, border_radius=30,
        height=50 if mobile else 54, width=150 if mobile else 190,
        ink=True, on_click=on_comenzar,
        shadow=ft.BoxShadow(blur_radius=14, color="#66F5A623",
                            offset=ft.Offset(0, 6)),
    )
    btn_login = ft.Container(
        content=ft.Text("Log in", color=DARK,
                        weight=ft.FontWeight.W_600, size=15 if mobile else 16),
        bgcolor=WHITE, border_radius=30,
        height=50 if mobile else 54, width=150 if mobile else 190,
        alignment=CENTER_ALIGN, ink=True, on_click=on_login,
        border=ft.Border.all(1.5, "#CCCCCC"),
        shadow=ft.BoxShadow(blur_radius=6, color="#18000000",
                            offset=ft.Offset(0, 2)),
    )

    def fl(src, top=None, left=None, right=None, bottom=None):
        return ft.Container(
            content=asset_image(src, 36, 36, "📚", 28),
            top=top, left=left, right=right, bottom=bottom,
        )

    bee_size = 300 if mobile else 460
    bee_stack = ft.Stack(
        width=bee_size, height=bee_size,
        controls=[
            ft.Container(
                content=ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=34),
                top=10, right=110,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.STAR_ROUNDED, color=PURPLE, size=18),
                top=60, right=40,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=GREEN, size=24),
                top=200, left=0,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.ADD, color="#C9B8F0", size=26),
                top=130, left=24,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.ADD, color=AMBER, size=20),
                bottom=130, right=110,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.ADD, color=BLUE, size=16),
                bottom=60, left=60,
            ),
            ft.Container(
                width=150, height=150,
                border=ft.Border.all(2, AMBER),
                border_radius=75, opacity=0.28,
                top=180, right=20,
            ),
            ft.Container(
                width=60, height=60,
                bgcolor=PURPLE, border_radius=30, opacity=0.18,
                bottom=10, right=170,
            ),
            ft.Container(
                width=26, height=26,
                bgcolor=GREEN, border_radius=13, opacity=0.4,
                top=40, left=0,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.FAVORITE_ROUNDED, color=RED, size=20),
                bottom=90, right=0,
                rotate=ft.Rotate(0.15),
            ),
            ft.Container(
                content=asset_image(IMG_BEE, 230 if mobile else 320, 230 if mobile else 320, "🐝", 150 if mobile else 190),
                top=14 if mobile else 20, left=35 if mobile else 40,
            ),
        ],
    )

    left_col = ft.Column(
        spacing=0,
        controls=[
            logo_widget(88 if mobile else 120),
            ft.Container(height=12 if mobile else 24),
            bee_stack,
        ],
    )

    right_text = ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.END,
        controls=[
            ft.Text(
                "Your way of learning\nmatters.\nWelcome to DixLearn",
                size=32 if mobile else 52,
                weight=ft.FontWeight.W_900,
                color=DARK,
                text_align=ft.TextAlign.CENTER if mobile else ft.TextAlign.RIGHT,
            ),
            ft.Container(height=14 if mobile else 20),
            ft.Text(
                "An app designed to support you\n"
                "your learning journey with tools\n"
                "created especially for you.",
                size=14 if mobile else 17,
                color=GRAY,
                text_align=ft.TextAlign.CENTER if mobile else ft.TextAlign.RIGHT,
            ),
            ft.Container(height=24 if mobile else 36),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER if mobile else ft.MainAxisAlignment.END,
                wrap=mobile,
                spacing=14,
                controls=[btn_comenzar, btn_login],
            ),
        ],
    )

    right_col = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=AMBER, size=30),
                top=-18, right=30,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.STAR_ROUNDED, color=PURPLE, size=20),
                top=6, left=0,
            ),
            ft.Container(
                width=18, height=18, border_radius=9,
                bgcolor=GREEN, opacity=0.5,
                top=140, left=-10,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.BOLT_ROUNDED, color=BLUE, size=22),
                bottom=70, left=-26,
            ),
            right_text,
        ],
    )

    def hill(w, h, color, op=1.0):
        return ft.Container(
            width=w, height=h, opacity=op, bgcolor=color,
            border_radius=ft.BorderRadius(
                top_left=w // 2, top_right=w // 2,
                bottom_left=0, bottom_right=0),
        )

    hills = ft.Container(
        height=72,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Row(
            spacing=-20,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                hill(220, 70, "#B8D8B0"),
                hill(180, 56, "#C8E6C9", 0.85),
                hill(320, 65, "#A5D6A7", 0.75),
                hill(200, 58, "#C5E1A5", 0.9),
                hill(280, 68, "#B2DFDB", 0.65),
                hill(220, 60, "#C8E6C9", 0.8),
                hill(160, 54, "#B8D8B0", 0.7),
            ],
        ),
    )

    hero_layout = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[left_col, right_col],
    ) if mobile else ft.Row(
        controls=[left_col, ft.Container(expand=True), right_col],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        bgcolor=BG,
        padding=ft.Padding(left=16 if mobile else 60, right=16 if mobile else 60, top=20 if mobile else 30, bottom=0),
        content=ft.Column(
            spacing=0,
            controls=[
                hero_layout,
                ft.Container(height=8 if mobile else 10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
                                      color="#AAAAAA", size=30)],
                ),
                ft.Container(height=4),
                hills,
            ],
        ),
    )


# ═════════════════════════════════════════════════════════════════════════
#  SECCIÓN 2 — LECCIONES ADAPTADAS
# ══════════════════════════════════════════════════════════════════════════

def ui_mockup_lecciones():
    def tab_pill(label, active):
        return ft.Container(
            content=ft.Text(
                label, size=9,
                color=WHITE if active else "#999999",
                weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_400,
            ),
            bgcolor=AMBER if active else "#EEEEEE",
            border_radius=8,
            padding=ft.Padding(left=8, right=8, top=4, bottom=4),
        )

    mockup = ft.Container(
        width=315, height=205,
        bgcolor=WHITE,
        border_radius=18,
        shadow=ft.BoxShadow(blur_radius=22, color="#22000000",
                            offset=ft.Offset(0, 8)),
        padding=ft.Padding(left=16, right=16, top=14, bottom=14),
        content=ft.Column(
            spacing=9,
            controls=[
                ft.Row(spacing=5, controls=[
                    tab_pill("Lessons",  True),
                    tab_pill("Exercises", False),
                    tab_pill("Evaluation", False),
                ]),
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.MENU_BOOK_ROUNDED, color=AMBER, size=22),
                        ft.Text("Lesson 1", size=15,
                                weight=ft.FontWeight.W_700, color=DARK),
                    ],
                ),
                hline("#E0E0E0"),
                hline("#E0E0E0", w=190),
                hline(AMBER),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Container(
                            width=36, height=36, border_radius=18,
                            bgcolor=GREEN, alignment=CENTER_ALIGN,
                            content=ft.Icon(ft.Icons.CHECK_ROUNDED,
                                            color=WHITE, size=20),
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.Stack(
        width=360, height=240,
        controls=[
            ft.Container(content=mockup, top=0, left=20),
            ft.Container(content=ft.Text("🪴", size=66), bottom=0, left=0),
            ft.Container(content=asset_image(IMG_BOOK, 54, 54, "📚", 40), bottom=0, right=0),
        ],
    )


def section_lecciones():
    right = ft.Column(
        spacing=10,
        controls=[
            num_badge(1, AMBER),
            ft.Text("Lessons adapted\nto you",
                    size=28, weight=ft.FontWeight.W_900, color=DARK),
            ft.Text(
                "Explore interactive lessons designed\n"
                "according to your learning style and advance\n"
                "at your own pace.",
                size=14, color=GRAY,
            ),
        ],
    )
    return ft.Container(
        bgcolor=SEC2_BG,
        padding=ft.Padding(left=50, right=70, top=36, bottom=36),
        content=ft.Stack(
            controls=[
                deco_icon(ft.Icons.AUTO_AWESOME_ROUNDED, AMBER, size=26, box=52,
                          opacity=0.30, top=6, right=90),
                deco_icon(ft.Icons.EDIT_ROUNDED, PURPLE, size=24, box=48,
                          opacity=0.26, bottom=4, right=20),
                deco_icon(ft.Icons.MENU_BOOK_ROUNDED, NAVY, size=22, box=44,
                          opacity=0.20, top=30, left=0),
                deco_icon(ft.Icons.STAR_ROUNDED, GREEN, size=18, box=36,
                          opacity=0.22, bottom=60, left=40),
                deco_dot(AMBER, size=16, opacity=0.5, top=60, right=40),
                deco_dot(NAVY, size=12, opacity=0.35, bottom=30, left=10),
                deco_dot(PURPLE, size=10, opacity=0.35, top=100, right=200),
                ft.Row(
                    controls=[
                        ui_mockup_lecciones(),
                        ft.Container(width=50),
                        right,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  SECCIÓN 3 — APRENDE JUGANDO
# ══════════════════════════════════════════════════════════════════════════

def gamepad_area():
    gamepad = ft.Container(
        width=220,
        height=160,
        alignment=CENTER_ALIGN,
        content=asset_image(IMG_GAMEPAD, 190, 140, "🎮", 90),
    )

    clipboard = ft.Container(
        width=180,
        height=200,
        bgcolor="#FFFBF0",
        border=ft.Border.all(8, "#FFD54F"),
        border_radius=16,
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=60,
                    height=28,
                    bgcolor="#2C5F8D",
                    border_radius=ft.BorderRadius(8, 8, 4, 4),
                    top=-14,
                    left=60,
                ),
                ft.Column(
                    spacing=14,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Icon(ft.Icons.CHECK, color="#FFC107", size=24),
                                ft.Container(width=70, height=8, bgcolor="#E0E0E0", border_radius=4),
                            ],
                        ),
                        ft.Row(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Icon(ft.Icons.CHECK, color="#42A5F5", size=24),
                                ft.Container(width=70, height=8, bgcolor="#E0E0E0", border_radius=4),
                            ],
                        ),
                        ft.Row(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Icon(ft.Icons.CHECK, color="#EF5350", size=24),
                                ft.Container(width=70, height=8, bgcolor="#E0E0E0", border_radius=4),
                            ],
                        ),
                    ],
                    left=15,
                    top=20,
                ),
            ],
            width=180,
            height=200,
        ),
    )

    star = ft.Container(
        content=ft.Icon(ft.Icons.STAR, color="#FFD54F", size=48),
        bottom=10,
        right=10,
    )

    return ft.Stack(
        width=420,
        height=220,
        controls=[
            ft.Container(content=gamepad, top=30, left=10),
            ft.Container(content=clipboard, top=0, right=20),
            star,
        ],
    )


def section_aprende_jugando():
    right = ft.Column(
        spacing=10,
        controls=[
            num_badge(2, PURPLE),
            ft.Text("Learn\nby playing",
                    size=28, weight=ft.FontWeight.W_900, color=DARK),
            ft.Text(
                "Interactive and fun exercises that\n"
                "turn every lesson into a game, ideal\n"
                "for the whole family.",
                size=14, color=GRAY,
            ),
        ],
    )
    return ft.Container(
        bgcolor=SEC3_BG,
        padding=ft.Padding(left=50, right=70, top=36, bottom=36),
        content=ft.Stack(
            controls=[
                deco_icon(ft.Icons.CELEBRATION_ROUNDED, PURPLE, size=26, box=52,
                          opacity=0.28, top=4, right=60),
                deco_icon(ft.Icons.SPORTS_ESPORTS_ROUNDED, AMBER, size=24, box=48,
                          opacity=0.26, bottom=8, left=30, rotate=-0.15),
                deco_icon(ft.Icons.EMOJI_EMOTIONS_ROUNDED, GREEN, size=20, box=40,
                          opacity=0.22, top=40, left=0),
                deco_icon(ft.Icons.STAR_ROUNDED, BLUE, size=18, box=36,
                          opacity=0.22, bottom=70, right=10),
                deco_dot(PURPLE, size=14, opacity=0.45, top=90, left=8),
                deco_dot(GREEN, size=12, opacity=0.4, bottom=20, right=140),
                deco_dot(AMBER, size=10, opacity=0.35, top=20, left=180),
                ft.Row(
                    controls=[
                        gamepad_area(),
                        ft.Container(width=50),
                        right,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  SECCIÓN 4 — PROGRESO
# ══════════════════════════════════════════════════════════════════════════

def progress_mockup():
    ring = ft.Container(
        width=68, height=68, border_radius=34,
        border=ft.Border.all(6, AMBER),
        alignment=CENTER_ALIGN,
        content=ft.Text("100%", size=12,
                        weight=ft.FontWeight.W_900, color=DARK),
    )

    mini_bars = ft.Row(
        spacing=5,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Container(width=16, height=38, border_radius=4, bgcolor="#C9B8F0"),
            ft.Container(width=16, height=56, border_radius=4, bgcolor=AMBER),
            ft.Container(width=16, height=30, border_radius=4, bgcolor=GREEN),
            ft.Container(width=16, height=46, border_radius=4, bgcolor=BLUE),
        ],
    )

    stats = ft.Column(
        spacing=10, expand=True,
        controls=[
            ft.Row(spacing=8,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER,
                   controls=[
                       ft.Text("Aa", size=14, color=BLUE,
                               weight=ft.FontWeight.W_700),
                       ft.Container(expand=True, height=10, border_radius=5,
                                    bgcolor="#C9B8F0"),
                   ]),
            ft.Row(spacing=8,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER,
                   controls=[
                       ft.Icon(ft.Icons.BOLT, color=AMBER, size=17),
                       ft.Container(expand=True, height=10, border_radius=5,
                                    bgcolor=AMBER, opacity=0.6),
                   ]),
            ft.Row(spacing=8,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER,
                   controls=[
                       ft.Icon(ft.Icons.VISIBILITY, color=GREEN, size=17),
                       ft.Container(expand=True, height=10, border_radius=5,
                                    bgcolor=GREEN, opacity=0.6),
                   ]),
        ],
    )

    return ft.Container(
        width=370, height=210,
        bgcolor=WHITE, border_radius=18,
        shadow=ft.BoxShadow(blur_radius=22, color="#1C000000",
                            offset=ft.Offset(0, 6)),
        padding=ft.Padding(left=20, right=20, top=16, bottom=16),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Overall Progress", size=13,
                                weight=ft.FontWeight.W_700, color=DARK),
                        ft.Container(expand=True),
                        ring,
                    ],
                ),
                ft.Container(height=11, border_radius=6, bgcolor=AMBER),
                ft.Divider(color="#EEEEEE", height=1),
                ft.Row(
                    spacing=16,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        mini_bars,
                        stats,
                    ],
                ),
            ],
        ),
    )


def section_progreso():
    right = ft.Column(
        spacing=12,
        controls=[
            num_badge(3, GREEN),
            ft.Text("Track your progress\nand celebrate your achievements",
                    size=28, weight=ft.FontWeight.W_900, color=DARK),
            ft.Text(
                "View your stats, identify your\n"
                "strengths and celebrate every small achievement\n"
                "along the way.",
                size=14, color=GRAY,
            ),
        ],
    )
    return ft.Container(
        bgcolor=BG,
        padding=ft.Padding(left=50, right=70, top=36, bottom=36),
        content=ft.Stack(
            controls=[
                deco_icon(ft.Icons.EMOJI_EVENTS_ROUNDED, GREEN, size=26, box=52,
                          opacity=0.28, top=2, right=100),
                deco_icon(ft.Icons.TRENDING_UP_ROUNDED, AMBER, size=24, box=48,
                          opacity=0.26, bottom=10, left=20),
                deco_icon(ft.Icons.INSIGHTS_ROUNDED, BLUE, size=20, box=40,
                          opacity=0.20, top=40, left=0),
                deco_icon(ft.Icons.STAR_ROUNDED, PURPLE, size=18, box=36,
                          opacity=0.22, bottom=90, right=10),
                deco_dot(GREEN, size=14, opacity=0.45, bottom=50, right=30),
                deco_dot(BLUE, size=12, opacity=0.4, top=70, left=200),
                deco_dot(AMBER, size=10, opacity=0.35, top=100, right=250),
                ft.Row(
                    controls=[
                        progress_mockup(),
                        ft.Container(width=55),
                        right,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  SECCIÓN 5 — PARA TODOS
# ══════════════════════════════════════════════════════════════════════════

def audience_card(img_src, fallback_emoji, label):
    return ft.Container(
        width=104,
        bgcolor=WHITE, border_radius=18,
        padding=ft.Padding(left=8, right=8, top=16, bottom=12),
        shadow=ft.BoxShadow(blur_radius=12, color="#16000000",
                            offset=ft.Offset(0, 4)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                asset_image(img_src, 58, 58, fallback_emoji, 40),
                ft.Text(label, size=11, color=DARK,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_600),
            ],
        ),
    )


def section_para_todos():
    left = ft.Column(
        spacing=10,
        controls=[
            num_badge(4, BLUE),
            ft.Text("DixLearn is\nfor everyone",
                    size=28, weight=ft.FontWeight.W_900, color=DARK),
            ft.Text(
                "Students, families, teachers, and professionals\n"
                "united to support learning\n"
                "more inclusive and meaningful.",
                size=14, color=GRAY,
            ),
        ],
    )
    cards = ft.Row(
        spacing=12,
        controls=[
            audience_card(IMG_STUDENT,   "🎓", "Students"),
            audience_card(IMG_FAMILY,    "👩‍👧", "Parents\nand families"),
            audience_card(IMG_SCHOOL,    "🏫",    "Educational\ncenters"),
            audience_card(IMG_PSYCH,     "👩‍⚕️",  "Psychologists"),
            audience_card(IMG_PORTFOLIO, "💼",   "Professionals"),
        ],
    )
    return ft.Container(
        bgcolor=SEC5_BG,
        padding=ft.Padding(left=50, right=50, top=36, bottom=36),
        content=ft.Stack(
            controls=[
                deco_icon(ft.Icons.GROUPS_ROUNDED, BLUE, size=26, box=52,
                          opacity=0.28, top=4, left=10),
                deco_icon(ft.Icons.FAVORITE_ROUNDED, PURPLE, size=22, box=44,
                          opacity=0.24, bottom=6, right=20),
                deco_icon(ft.Icons.SCHOOL_ROUNDED, AMBER, size=20, box=40,
                          opacity=0.22, top=50, right=250),
                deco_icon(ft.Icons.STAR_ROUNDED, GREEN, size=18, box=36,
                          opacity=0.22, bottom=60, left=260),
                deco_dot(BLUE, size=14, opacity=0.45, top=60, right=180),
                deco_dot(AMBER, size=12, opacity=0.4, bottom=40, left=250),
                deco_dot(PURPLE, size=10, opacity=0.35, top=20, left=350),
                ft.Row(
                    controls=[left, ft.Container(expand=True), cards],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  FOOTER CTA
# ══════════════════════════════════════════════════════════════════════════

def footer_cta():
    heart = ft.Container(
        width=40, height=40, border_radius=20,
        bgcolor="#EAD8FF", alignment=CENTER_ALIGN,
        content=ft.Icon(ft.Icons.FAVORITE_ROUNDED, color=PURPLE, size=22),
    )
    return ft.Container(
        bgcolor=FOOTER_BG,
        padding=ft.Padding(left=60, right=50, top=44, bottom=44),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=10, expand=True,
                    controls=[
                        ft.Row(
                            spacing=14,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                heart,
                                ft.Text(
                                    "At DixLearn, we believe that\nlearning differently is shining.",
                                    size=22, weight=ft.FontWeight.W_900, color=DARK,
                                ),
                            ],
                        ),
                        ft.Text(
                            "You're in the right place to grow, overcome challenges\n"
                            "and discover your full potential.",
                            size=13, color=GRAY,
                        ),
                    ],
                ),
                asset_image(IMG_BEE, 150, 150, "🐝", 95),
            ],
        ),
    )


def scroll_hint_bar():
    return ft.Container(
        bgcolor=BG, height=46,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
                        color="#AAAAAA", size=20),
                ft.Text("Swipe to discover more",
                        size=12, color="#AAAAAA"),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════════════════
#  BUILDER PRINCIPAL — compatible con main.py
# ═════════════════════════════════════════════════════════════════════════

def build_welcome_screen(page: ft.Page, on_comenzar, on_login):
    """
    Complete welcome screen with all sections.
    """
    # Modo exclusivo para teléfono: siempre se usa el layout apilado
    # (una columna), sin importar el ancho de la ventana.
    mobile = True
    return ft.Container(
        expand=True,
        image=ft.DecorationImage(src="imagenes/fondo.png", fit="cover"),
        content=ft.ListView(
            expand=True,
            spacing=0,
            padding=ft.Padding(0, 0, 0, 0),
            controls=[
                hero_section(on_comenzar, on_login, mobile=mobile),
                section_lecciones(),
                section_aprende_jugando(),
                section_progreso(),
                section_para_todos(),
                footer_cta(),
                scroll_hint_bar(),
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "DixLearn - Your way of learning matters"
    page.bgcolor = BG
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    
    def handle_comenzar(e):
        print("Start button pressed")
    
    def handle_login(e):
        print("Log in button pressed")
    
    welcome_screen = build_welcome_screen(page, handle_comenzar, handle_login)
    page.add(welcome_screen)


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="imagenes",
        view=ft.AppView.WEB_BROWSER,
    )