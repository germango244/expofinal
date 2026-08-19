"""Lesson - Advanced Comprehension: The Lighthouse in the Storm - Level 2, Lesson 3.

Redesigned "horizontal" (PC) layout, with the same visual style
as reconoce_letras.py:

  - Fixed instruction panel on the left (title + text + Dixi).
  - Interactive area on the right, using all of the remaining width.
  - Random image background + floating decorations (clouds, sparkles).
  - Option cards, result banner and "Tip" pill,
    consistent with the rest of the app.

The public API stays the same: build_comprension_avanzada(page, usuario,
on_lecciones, on_inicio).
"""

import random

import flet as ft
from pantalla import progreso as prog
from config import TOTAL_STEPS, PURPLE, WHITE, GRAY_TEXT, DARK, AMBER, GREEN, LIGHT_PURPLE, CENTER
from components.celebration import build_celebracion

# Width of the fixed instruction panel on the left (horizontal PC layout)
SIDE_PANEL_WIDTH = 320

# Available background images (inside the "imagenes" folder)
FONDOS_IMAGENES = [
    "imagenes/fondo1.png",
    "imagenes/fondo2.png",
    "imagenes/fondo3.png",
]

# Level of this lesson (for the top bar)
NIVEL = 2

_GRAD_TOP = ft.Alignment(0, -1)
_GRAD_BOTTOM = ft.Alignment(0, 1)

# ---------------------------------------------------
#  Additional palette (only for this lesson, doesn't depend on config)
# ---------------------------------------------------
ERROR_RED = "#E5484D"
SUCCESS_BG = "#EEFBF1"
SUCCESS_BORDER = "#C3ECCB"
ERROR_BG = "#FDEEEE"
ERROR_BORDER = "#F3C7C7"
CARD_BORDER_IDLE = "#EFECF9"
BLUE = "#2196F3"


def _anim(ms=180, curva="easeOut"):
    return ft.Animation(ms, curva)


def _shadow(blur=10, dy=3, alpha="0F"):
    return ft.BoxShadow(blur_radius=blur, color=f"#{alpha}000000", offset=ft.Offset(0, dy))


# ===================================================
#  GRADIENT BACKGROUNDS (one per step)
# ===================================================

GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])
GRAD_GREEN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])
GRAD_BLUE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EFF7FF", "#D7EBFF"])
GRAD_LILA = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F7F4FF", "#EDE7FF"])
GRAD_PINK = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])


# ===================================================
#  REUSABLE DECORATIVE PIECES
# ===================================================

def _nube(size=90, opacity=0.55):
    return ft.Stack(
        width=size * 1.8, height=size * 0.95,
        controls=[
            ft.Container(left=size * 0.15, top=size * 0.30, width=size * 0.95, height=size * 0.55,
                         border_radius=size, bgcolor=WHITE, opacity=opacity),
            ft.Container(left=0, top=size * 0.40, width=size * 0.62, height=size * 0.48,
                         border_radius=size, bgcolor=WHITE, opacity=opacity),
            ft.Container(left=size * 0.78, top=size * 0.12, width=size * 0.78, height=size * 0.65,
                         border_radius=size, bgcolor=WHITE, opacity=opacity),
        ],
    )


def fondo_decorativo():
    return [
        ft.Container(left=50, top=40, content=_nube(85)),
        ft.Container(right=60, top=70, content=_nube(105)),
        ft.Container(left=90, top=300, width=60, height=60, border_radius=30, bgcolor=WHITE, opacity=0.30),
        ft.Container(right=120, top=440, width=44, height=44, border_radius=22, bgcolor=PURPLE, opacity=0.10),
        ft.Container(left=180, top=540, content=ft.Text("✦", size=20, color=WHITE, opacity=0.65)),
        ft.Container(right=200, top=170, content=ft.Text("✨", size=18, color=WHITE, opacity=0.7)),
        ft.Container(left=250, top=110, content=ft.Text("⋆", size=22, color=PURPLE, opacity=0.18)),
        ft.Container(right=260, top=520, content=ft.Text("✦", size=16, color=PURPLE, opacity=0.16)),
    ]


# ---------------------------------------------------
#  "Dixi" mascot (the app's owl) + speech bubble
# ---------------------------------------------------

def dixi_mascota(mensaje, tamano=64, ancho_globo=190):
    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Stack(
                width=tamano, height=tamano * 1.08,
                controls=[
                    ft.Container(top=tamano * 0.14, content=ft.Text("🦉", size=tamano)),
                    ft.Container(
                        left=tamano * 0.30, top=0,
                        content=ft.Text("🎓", size=tamano * 0.34, rotate=ft.Rotate(-0.18)),
                    ),
                ],
            ),
            ft.Container(
                width=ancho_globo,
                bgcolor=WHITE, border_radius=16,
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                shadow=_shadow(14, 5, "18"),
                content=ft.Column(
                    spacing=4, tight=True,
                    controls=[
                        ft.Row(
                            spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=20, height=20, border_radius=10, bgcolor=LIGHT_PURPLE,
                                    alignment=CENTER, content=ft.Text("💜", size=10),
                                ),
                                ft.Text("You can do it!", size=12, weight=ft.FontWeight.W_800, color=PURPLE),
                            ],
                        ),
                        ft.Text(mensaje, size=12, color=DARK, style=ft.TextStyle(height=1.3)),
                    ],
                ),
            ),
        ],
    )


def fondo_pantalla(gradiente, contenido_centro, mascota_texto=None):
    capas = [
        *fondo_decorativo(),
        ft.Container(
            expand=True,
            padding=ft.Padding(left=14, right=14, top=14, bottom=0),
            content=contenido_centro,
        ),
    ]
    if mascota_texto:
        capas.append(ft.Container(left=20, bottom=92, content=dixi_mascota(mascota_texto)))

    return ft.Container(
        expand=True,
        image=ft.DecorationImage(src=random.choice(FONDOS_IMAGENES), fit=ft.BoxFit.COVER),
        content=ft.Stack(expand=True, controls=capas),
    )


# ===================================================
#  FULL TOP BAR (level + progress + % + points + settings)
# ===================================================

def build_top_bar_rico(paso_idx, total, puntos, on_home, on_settings=None):
    dot_row = []
    for i in range(total):
        filled = i <= paso_idx
        size = 16 if filled else 12
        dot_row.append(
            ft.Container(
                width=size, height=size, border_radius=size // 2,
                bgcolor=PURPLE if filled else "#D9D9D9",
                animate=_anim(220),
            )
        )
        if i < total - 1:
            dot_row.append(
                ft.Container(
                    width=14, height=4, border_radius=2,
                    bgcolor=PURPLE if i < paso_idx else "#D9D9D9",
                    animate=_anim(220),
                )
            )

    porcentaje = int(round((paso_idx / total) * 100)) if total else 0

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=12, right=12, top=8, bottom=8),
        shadow=_shadow(12, 3, "14"),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(icon=ft.Icons.HOME_ROUNDED, icon_color=PURPLE, icon_size=26, on_click=on_home),
                ft.Row(
                    spacing=18,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(spacing=0, controls=dot_row),
                    ],
                ),
                ft.Row(
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(f"{porcentaje}%", size=16, weight=ft.FontWeight.W_800, color=PURPLE),
                                ft.Text("completed", size=12, color=GRAY_TEXT),
                            ],
                        ),
                        ft.Container(
                            bgcolor=LIGHT_PURPLE, border_radius=20,
                            padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                            content=ft.Row(
                                spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                                    ft.Text(str(puntos), size=16, weight=ft.FontWeight.W_800, color=PURPLE),
                                ],
                            ),
                        ),
                        ft.IconButton(icon=ft.Icons.SETTINGS_ROUNDED, icon_color=PURPLE, icon_size=24,
                                     on_click=on_settings),
                    ],
                ),
            ],
        ),
    )


# ===================================================
#  HINT, RESULT BANNER AND NAVIGATION
# ===================================================

def hint_pill(texto):
    return ft.Container(
        bgcolor=WHITE, border_radius=22,
        padding=ft.Padding(left=14, right=22, top=6, bottom=6),
        shadow=_shadow(10, 3, "12"),
        content=ft.Row(
            spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=34, height=34, border_radius=17, bgcolor=LIGHT_PURPLE,
                    alignment=CENTER, content=ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=AMBER, size=18),
                ),
                ft.Column(
                    spacing=0, tight=True, width=220,
                    controls=[
                        ft.Text("Tip", size=12, weight=ft.FontWeight.W_800, color=PURPLE),
                        ft.Text(texto, size=14, color=GRAY_TEXT, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ],
                ),
            ],
        ),
    )


def crear_banner_resultado():
    icono = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=GREEN, size=22)
    texto = ft.Text("", size=15, weight=ft.FontWeight.W_700, color=GREEN)
    banner = ft.Container(
        visible=False,
        bgcolor=SUCCESS_BG,
        border=ft.Border.all(1.5, SUCCESS_BORDER),
        border_radius=16,
        padding=ft.Padding(left=20, right=22, top=12, bottom=12),
        animate_opacity=_anim(200),
        content=ft.Row(spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[icono, texto]),
    )
    return banner, icono, texto


def mostrar_resultado(banner, icono, texto_ctrl, mensaje, ok=True):
    texto_ctrl.value = mensaje
    if ok:
        icono.name = ft.Icons.CHECK_CIRCLE_ROUNDED
        icono.color = GREEN
        texto_ctrl.color = GREEN
        banner.bgcolor = SUCCESS_BG
        banner.border = ft.Border.all(1.5, SUCCESS_BORDER)
    else:
        icono.name = ft.Icons.CANCEL_ROUNDED
        icono.color = ERROR_RED
        texto_ctrl.color = ERROR_RED
        banner.bgcolor = ERROR_BG
        banner.border = ft.Border.all(1.5, ERROR_BORDER)
    banner.visible = True


def marcar_seleccion(card, activo):
    card.border = ft.Border.all(4, PURPLE) if activo else ft.Border.all(2, CARD_BORDER_IDLE)
    card.bgcolor = LIGHT_PURPLE if activo else WHITE


def marcar_correcta_incorrecta(card, es_correcta, es_elegida):
    """Marks a card as correct (green) or as an incorrect choice (red)."""
    if es_correcta:
        card.bgcolor = SUCCESS_BG
        card.border = ft.Border.all(3, GREEN)
    elif es_elegida:
        card.bgcolor = ERROR_BG
        card.border = ft.Border.all(3, ERROR_RED)
    else:
        card.bgcolor = WHITE
        card.border = ft.Border.all(2, CARD_BORDER_IDLE)


def barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=True,
                    texto_siguiente="Next", siguiente_visible=True):
    atras_btn = ft.Button(
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, color=PURPLE, size=18),
                ft.Text("Back", color=PURPLE, size=16, weight=ft.FontWeight.W_700),
            ],
        ),
        bgcolor=WHITE,
        on_click=on_prev,
        visible=mostrar_atras,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, "#EDEAFB"),
            shape=ft.RoundedRectangleBorder(radius=28),
            elevation=0,
            padding=ft.Padding(left=26, right=26, top=10, bottom=10),
        ),
    )
    siguiente_btn = ft.Button(
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Text(texto_siguiente, color=WHITE, size=16, weight=ft.FontWeight.W_700),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=WHITE, size=18),
            ],
        ),
        bgcolor=PURPLE,
        on_click=on_next,
        visible=siguiente_visible,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=28),
            elevation=2,
            padding=ft.Padding(left=32, right=32, top=10, bottom=10),
        ),
    )
    fila_botones = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[atras_btn, siguiente_btn],
    )
    fila = ft.Container(
        padding=ft.Padding(left=40, right=40, top=0, bottom=16),
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=(
                [ft.Container(alignment=CENTER, content=hint_pill(hint_texto)), fila_botones]
                if hint_texto else [fila_botones]
            ),
        ),
    )
    return fila, siguiente_btn


# ===================================================
#  INSTRUCTION PANEL (fixed left column)
# ===================================================

def panel_instrucciones(titulo, subtitulo, icono_emoji=None, mascota_texto=None, extra=None):
    columna = []
    if icono_emoji:
        columna += [ft.Text(icono_emoji, size=46), ft.Container(height=14)]
    columna += [
        ft.Text(titulo, size=24, weight=ft.FontWeight.W_900, color=PURPLE),
        ft.Container(height=8),
        ft.Text(subtitulo, size=15, color=GRAY_TEXT, style=ft.TextStyle(height=1.45)),
    ]
    if extra:
        columna += [ft.Container(height=18), *extra]
    columna.append(ft.Container(expand=True))
    if mascota_texto:
        columna.append(dixi_mascota(mascota_texto, tamano=56, ancho_globo=190))

    return ft.Container(
        bgcolor=WHITE,
        border_radius=24,
        padding=ft.Padding(left=26, right=26, top=30, bottom=26),
        shadow=_shadow(18, 6, "12"),
        content=ft.Column(spacing=0, controls=columna),
    )


def fila_principal(panel, area_derecha):
    """Instructions panel on top, interactive area below -- stacked
    vertically (instead of side by side) so everything fits on a
    phone-width screen. Scrolls automatically if the content is
    taller than the visible area, instead of overflowing off-screen."""
    return ft.Column(
        expand=True,
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            panel,
            ft.Container(alignment=CENTER, content=area_derecha),
        ],
    )


# ===================================================
#  STEP 1 -- Introduction: Hi! I'm Dixi
# ===================================================

def build_paso_1(on_next, on_prev):
    barra, _ = barra_inferior(
        on_prev, on_next,
        hint_texto=None,
        mostrar_atras=False,
        texto_siguiente="Let's begin!",
    )

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="Today we'll work on our advanced comprehension. Read, analyze, and answer carefully.",
        mascota_texto="Thinking beyond the words makes us great readers.",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Stack(
                    width=280, height=160,
                    controls=[
                        ft.Container(
                            left=0, top=30, width=280,
                            bgcolor=WHITE, border_radius=18,
                            padding=ft.Padding(left=18, right=18, top=16, bottom=16),
                            shadow=_shadow(14, 4, "16"),
                            content=ft.Text(
                                "Today we\'ll read a\ntext and think\nbeyond the\nwords.",
                                size=16, color=DARK, style=ft.TextStyle(height=1.35),
                            ),
                        ),
                        ft.Container(left=14, top=0, content=ft.Text("⭐", size=22)),
                    ],
                ),
                ft.Text("🐝", size=76),
                ft.Container(
                    width=280, bgcolor=WHITE, border_radius=24,
                    padding=ft.Padding(left=22, right=22, top=18, bottom=18),
                    shadow=_shadow(20, 7, "18"),
                    content=ft.Text(
                        "You\'ll understand, analyze,\nand draw your own\nconclusions.",
                        size=17, color=PURPLE, weight=ft.FontWeight.W_700,
                        text_align=ft.TextAlign.CENTER, style=ft.TextStyle(height=1.4),
                    ),
                ),
            ],
        ),
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_PURPLE, contenido)


# ===================================================
#  STEP 2 -- Read the text
# ===================================================

def build_paso_2(on_next, on_prev):
    barra, _ = barra_inferior(
        on_prev, on_next,
        hint_texto="Read the text calmly, paying attention to the details.",
        texto_siguiente="Continue",
    )

    panel = panel_instrucciones(
        titulo="Read the text",
        subtitulo="Read the following text carefully. We'll ask you about it later.",
        mascota_texto="Read calmly. We'll talk about this story in the next steps.",
    )

    tarjeta_lectura = ft.Container(
        width=320,
        bgcolor=WHITE, border_radius=28,
        padding=ft.Padding(left=30, right=30, top=26, bottom=26),
        shadow=_shadow(20, 7, "16"),
        content=ft.Column(
            spacing=18,
            controls=[
                ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=52, height=52, border_radius=26, bgcolor=LIGHT_PURPLE,
                            alignment=CENTER, content=ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=26),
                        ),
                        ft.Text("The Lighthouse in the Storm", size=22, weight=ft.FontWeight.W_900, color=DARK,
                                expand=True, style=ft.TextStyle(height=1.2)),
                    ],
                ),
                ft.Text(
                    "One stormy night, the lighthouse stayed\n"
                    "lit. The sea was rough and many\n"
                    "ships were lost, but one of them saw\n"
                    "the light in the distance and made its way to\n"
                    "safe harbor.\n\n"
                    "Sometimes, a small light can make a\n"
                    "big difference.",
                    size=18, color=DARK, style=ft.TextStyle(height=1.5),
                ),
            ],
        ),
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            tarjeta_lectura,
            ft.Text("🐝", size=60),
        ],
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_YELLOW, contenido)


# ===================================================
#  STEP 3 -- What did you understand?
# ===================================================

def build_paso_3(on_next, on_prev):
    opciones = [
        {"texto": "The sea was very rough.", "emoji": "🌊", "correcto": False},
        {"texto": "The lighthouse's light helped a ship reach safety.", "emoji": "🏮", "correcto": True},
        {"texto": "There was a very strong storm.", "emoji": "⛈️", "correcto": False},
        {"texto": "Many ships set sail at night.", "emoji": "⛵", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Select the best main idea of the text.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="What did you understand?",
        subtitulo="Choose the main idea that best sums up the text you read.",
        mascota_texto="Think about the most important thing that happened in the story.",
    )

    correct_idx = next(j for j, o in enumerate(opciones) if o["correcto"])
    cards_refs = []

    def on_elegir(idx_elegido):
        def handler(e):
            for i, card in enumerate(cards_refs):
                marcar_correcta_incorrecta(card, i == correct_idx, i == idx_elegido)
            if idx_elegido == correct_idx:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Correct! The lighthouse's light helped the ship 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=300, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            ink=True, animate=_anim(180),
            shadow=_shadow(10, 3, "10"),
            on_click=on_elegir(i),
            padding=ft.Padding(left=18, right=18, top=14, bottom=14),
            content=ft.Row(
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(op["emoji"], size=32),
                    ft.Text(op["texto"], size=16, weight=ft.FontWeight.W_600, color=DARK,
                            style=ft.TextStyle(height=1.2), expand=True),
                ],
            ),
        )
        cards_refs.append(card)
        cards.append(card)

    columna_opciones = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
        controls=[*cards, banner],
    )

    area = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[columna_opciones],
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_GREEN, contenido)


# ===================================================
#  STEP 4 -- Analyze and answer
# ===================================================

def build_paso_4(on_next, on_prev):
    opciones = [
        {"texto": "To help\nthe ships.", "emoji": "❤️🏮", "correcto": True},
        {"texto": "To make\nmoney.", "emoji": "💰", "correcto": False},
        {"texto": "Because it was\nbored.", "emoji": "⚓", "correcto": False},
        {"texto": "Because it was\nnighttime.", "emoji": "🌙", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Think about the reason behind the lighthouse's action.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Analyze and answer",
        subtitulo="Why do you think the lighthouse stayed lit during the storm?",
        mascota_texto="Calmly weigh each option before choosing.",
    )

    correct_idx = next(j for j, o in enumerate(opciones) if o["correcto"])
    cards_refs = []

    def on_elegir(idx_elegido):
        def handler(e):
            for i, card in enumerate(cards_refs):
                marcar_correcta_incorrecta(card, i == correct_idx, i == idx_elegido)
            if idx_elegido == correct_idx:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Correct! The lighthouse stayed lit to help 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=150, height=150, border_radius=20,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            on_click=on_elegir(i),
            shadow=_shadow(12, 4, "12"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(op["emoji"], size=40),
                    ft.Text(op["texto"], size=15, weight=ft.FontWeight.W_600, color=DARK,
                            text_align=ft.TextAlign.CENTER),
                ],
            ),
        )
        cards_refs.append(card)
        cards.append(card)

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True,
                  spacing=16, run_spacing=16, controls=cards),
            banner,
        ],
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_BLUE, contenido)


# ===================================================
#  STEP 5 -- Relate and conclude
# ===================================================

def build_paso_5(on_next, on_prev):
    situaciones = [
        "A ship couldn\'t see anything\nin the storm.",
        "It saw the lighthouse's light.",
        "It reached a safe harbor.",
    ]
    ensenanzas = [
        "It found the help\nit needed.",
        "The light gave it\ndirection.",
        "It was saved from danger.",
    ]
    respuestas_correctas = {0: 2, 1: 1, 2: 0}

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Tap a situation and then the lesson it matches.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Relate and conclude",
        subtitulo="Match each situation with the lesson the text teaches us.",
        mascota_texto="First tap a situation, then its matching lesson.",
    )

    estado = {"seleccion": None, "aciertos": 0}
    situacion_cards = {}
    ensenanza_cards = {}

    def on_select_situacion(idx):
        def handler(e):
            estado["seleccion"] = idx
            for i, c in situacion_cards.items():
                c.bgcolor = LIGHT_PURPLE if i == idx else WHITE
                c.border = ft.Border.all(3, PURPLE) if i == idx else ft.Border.all(2, CARD_BORDER_IDLE)
            e.page.update()
        return handler

    def on_select_ensenanza(idx_ensenanza):
        def handler(e):
            sel = estado["seleccion"]
            if sel is None:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "First tap a situation on the left.", ok=False)
                e.page.update()
                return
            if respuestas_correctas.get(sel) == idx_ensenanza:
                marcar_correcta_incorrecta(situacion_cards[sel], True, False)
                marcar_correcta_incorrecta(ensenanza_cards[idx_ensenanza], True, False)
                estado["aciertos"] += 1
                estado["seleccion"] = None
                if estado["aciertos"] >= len(situaciones):
                    btn_continuar.visible = True
                    mostrar_resultado(banner, banner_icono, banner_texto,
                                      "Excellent! You matched everything correctly 🎉", ok=True)
                else:
                    mostrar_resultado(banner, banner_icono, banner_texto,
                                      f"Correct! ({estado['aciertos']}/{len(situaciones)})", ok=True)
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    left_col = []
    for i, s in enumerate(situaciones):
        c = ft.Container(
            width=130, height=110, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            shadow=_shadow(8, 3, "10"),
            on_click=on_select_situacion(i),
            content=ft.Text(s, size=13, weight=ft.FontWeight.W_600, color=DARK, text_align=ft.TextAlign.CENTER),
        )
        situacion_cards[i] = c
        left_col.append(c)

    indices_mezclados = list(range(len(ensenanzas)))
    random.shuffle(indices_mezclados)
    right_col = []
    for idx in indices_mezclados:
        c = ft.Container(
            width=130, height=110, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            shadow=_shadow(8, 3, "10"),
            on_click=on_select_ensenanza(idx),
            content=ft.Text(ensenanzas[idx], size=13, weight=ft.FontWeight.W_600, color=DARK,
                            text_align=ft.TextAlign.CENTER),
        )
        ensenanza_cards[idx] = c
        right_col.append(c)

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Column(spacing=16, controls=left_col),
                    ft.Column(spacing=16, controls=right_col),
                ],
            ),
            banner,
        ],
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_LILA, contenido)


# ===================================================
#  STEP 6 -- Reflect
# ===================================================

def build_paso_6(on_next, on_prev):
    afirmacion = "Sometimes, something small can\nchange the outcome of a situation."

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Read the statement and choose whether you agree.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Reflect",
        subtitulo="Read the statement and decide whether you agree with it.",
        mascota_texto="The lighthouse was just a light, but it was enough to save a ship.",
    )

    def on_elegir(opcion):
        def handler(e):
            if opcion == "si":
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Well done! 🎉 The lighthouse was just a light, but it saved a ship.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Think about it again 🙂 Sometimes small things make a big difference.", ok=False)
            e.page.update()
        return handler

    btn_si = ft.Button(
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.THUMB_UP_ROUNDED, color=GREEN, size=22),
                ft.Text("I agree", size=16, weight=ft.FontWeight.W_700, color=GREEN),
            ],
        ),
        bgcolor=SUCCESS_BG,
        on_click=on_elegir("si"),
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, SUCCESS_BORDER),
            shape=ft.RoundedRectangleBorder(radius=22),
            elevation=0,
            padding=ft.Padding(left=26, right=26, top=14, bottom=14),
        ),
    )
    btn_no = ft.Button(
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.THUMB_DOWN_ROUNDED, color=ERROR_RED, size=22),
                ft.Text("I disagree", size=16, weight=ft.FontWeight.W_700, color=ERROR_RED),
            ],
        ),
        bgcolor=ERROR_BG,
        on_click=on_elegir("no"),
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, ERROR_BORDER),
            shape=ft.RoundedRectangleBorder(radius=22),
            elevation=0,
            padding=ft.Padding(left=26, right=26, top=14, bottom=14),
        ),
    )

    tarjeta_afirmacion = ft.Container(
        width=320, bgcolor=WHITE, border_radius=28,
        padding=ft.Padding(left=28, right=28, top=26, bottom=26),
        shadow=_shadow(18, 6, "16"),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Text("❝", size=42, color=PURPLE),
                ft.Text(afirmacion, size=19, color=DARK, weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER, style=ft.TextStyle(height=1.35)),
                ft.Text("❞", size=42, color=PURPLE),
            ],
        ),
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            tarjeta_afirmacion,
            ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER, controls=[btn_si, btn_no]),
            banner,
        ],
    )

    contenido = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(height=10),
            fila_principal(panel, area),
            barra,
        ],
    )
    return fondo_pantalla(GRAD_PINK, contenido)


# ===================================================
#  MAIN LESSON CONTROLLER
# ===================================================

def build_comprension_avanzada(page: ft.Page, usuario: str = "",
                                on_lecciones=None, on_inicio=None):
    paso_actual = {"idx": 0}
    puntos_state = {"val": prog.obtener_progreso(usuario).get("puntos", 0)}

    def get_paso_widget(idx):
        if idx == 0:
            return build_paso_1(on_next, on_prev)
        elif idx == 1:
            return build_paso_2(on_next, on_prev)
        elif idx == 2:
            return build_paso_3(on_next, on_prev)
        elif idx == 3:
            return build_paso_4(on_next, on_prev)
        elif idx == 4:
            return build_paso_5(on_next, on_prev)
        elif idx == 5:
            return build_paso_6(on_next, on_prev)
        else:
            return build_celebracion(
                on_repasar,
                on_continuar_final,
                usuario=usuario,
                nivel=NIVEL,
                num=3,
                titulo="Advanced comprehension",
            )

    def on_next(e=None):
        go_to(paso_actual["idx"] + 1)

    def on_prev(e=None):
        go_to(max(0, paso_actual["idx"] - 1))

    def on_repasar(e=None):
        go_to(0)

    def on_continuar_final(e=None):
        if on_lecciones:
            on_lecciones(e)

    def on_settings(e=None):
        if on_inicio:
            on_inicio(e)

    def go_to(idx):
        paso_actual["idx"] = idx
        barra_wrapper.content = (
            build_top_bar_rico(idx, TOTAL_STEPS, puntos_state["val"], on_home=on_lecciones,
                               on_settings=on_settings)
            if idx < TOTAL_STEPS
            else ft.Container()
        )
        contenido_wrapper.content = get_paso_widget(idx)
        page.update()

    barra_wrapper = ft.Container(
        content=build_top_bar_rico(0, TOTAL_STEPS, puntos_state["val"], on_home=on_lecciones,
                                   on_settings=on_settings),
    )

    contenido_wrapper = ft.Container(
        expand=True,
        content=get_paso_widget(0),
    )

    return ft.Column(
        expand=True, spacing=0,
        controls=[barra_wrapper, contenido_wrapper],
    )
