"""Lesson - Fun Spelling - Level 3, Lesson 2.

Redesigned version: same behavior and same public API as the
original file (build_ortografia_divertida, build_paso_1..6,
top_progress_bar), but with the same "horizontal" PC-format layout
used in reconoce_letras.py:

  - Instructions panel fixed to the left (title + text + Dixi),
    with the full height of the screen.
  - Interactive area on the right, which expands and uses all the
    remaining horizontal space.
  - Random image background (as in reconoce_letras.py) instead of
    each step's plain solid color.
  - "Dixi" mascot (owl) with speech bubble, integrated into the
    instructions panel.
  - Option cards and pills with smooth transitions, result banner
    with icon and color, "Tip" pill.
"""

import random

import flet as ft
from config import TOTAL_STEPS, PURPLE, WHITE, GRAY_TEXT, DARK, AMBER, GREEN, LIGHT_PURPLE, CENTER
from components.celebration import build_celebracion

# Width of the instructions panel fixed to the left (horizontal PC format)
SIDE_PANEL_WIDTH = 320

# Available image backgrounds (inside the "imagenes" folder)
FONDOS_IMAGENES = [
    "imagenes/fondo1.png",
    "imagenes/fondo2.png",
    "imagenes/fondo3.png",
]

# Level of this lesson (for the top bar)
NIVEL = 3

_GRAD_TOP = ft.Alignment(0, -1)
_GRAD_BOTTOM = ft.Alignment(0, 1)

# ---------------------------------------------------
#  Additional palette (only for this lesson, does not depend on config)
# ---------------------------------------------------
RED = "#E53935"
BLUE = "#2196F3"
ERROR_RED = "#E5484D"
SUCCESS_BG = "#EEFBF1"
SUCCESS_BORDER = "#C3ECCB"
ERROR_BG = "#FDEEEE"
ERROR_BORDER = "#F3C7C7"
CARD_BORDER_IDLE = "#EFECF9"


def _anim(ms=180, curva="easeOut"):
    return ft.Animation(ms, curva)


def _shadow(blur=10, dy=3, alpha="0F"):
    return ft.BoxShadow(blur_radius=blur, color=f"#{alpha}000000", offset=ft.Offset(0, dy))


# ===================================================
#  GRADIENT BACKGROUNDS (one per step, with more depth)
# ===================================================

GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])
GRAD_GREEN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])
GRAD_BLUE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EEF7FF", "#D9ECFF"])
GRAD_LIGHT = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FBF9FF", "#F2EEFF"])
GRAD_PINK = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])


# ===================================================
#  REUSABLE DECORATIVE PIECES
# ===================================================

def _nube(size=90, opacity=0.55):
    """A simple 'cloud' made of 3 overlapping white circles."""
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
    """Floating background elements: clouds, soft circles and sparkles."""
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
#  "Dixi" mascot (the app's bee/owl) + speech bubble
# ---------------------------------------------------

def dixi_mascota(mensaje, tamano=64, ancho_globo=190):
    """Owl mascot with its speech bubble encouraging us to keep playing."""
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
    """Wraps a step's content with image background + decorations.

    The content receives the full available screen width; each step
    internally arranges its own horizontal layout (instructions panel
    + interactive area).
    """
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
#  TOP BAR WITH PROGRESS DOTS
# ===================================================

def top_progress_bar(paso: int, total: int, on_home):
    dot_row = []
    for i in range(total):
        filled = i <= paso
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
                    bgcolor=PURPLE if i < paso else "#D9D9D9",
                    animate=_anim(220),
                )
            )

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
                ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=30),
            ],
        ),
    )


# ===================================================
#  HINT, RESULT BANNER AND NAVIGATION
# ===================================================

def hint_pill(texto):
    """Tip pill with icon in a circle (consistent throughout the lesson)."""
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
    """Creates a result banner (correct/incorrect) with icon + text."""
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
    """Updates the result banner with the message and status (correct/incorrect)."""
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


def marcar_seleccion(card, activo, ok=True):
    """Applies the 'selected' style to an option card (border + background)."""
    if activo:
        card.border = ft.Border.all(3, GREEN if ok else ERROR_RED)
        card.bgcolor = SUCCESS_BG if ok else ERROR_BG
    else:
        card.border = ft.Border.all(2, CARD_BORDER_IDLE)
        card.bgcolor = WHITE


def barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=True,
                    texto_siguiente="Next", siguiente_visible=True):
    """Back / hint / Next row. Returns (row_ready, next_button)."""
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
#  INSTRUCTIONS PANEL (fixed column on the left)
# ===================================================

def panel_instrucciones(titulo, subtitulo, icono_emoji=None, mascota_texto=None, extra=None):
    """White card fixed to the left, at the full height of the
    screen, that gathers the step's title/instruction and
    (optionally) Dixi cheering us on."""
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

def build_paso_1(on_next, on_prev=None):
    barra, _ = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto=None,
        mostrar_atras=False,
        texto_siguiente="Let's start!",
    )

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="We're going to improve your spelling in a fun way. You'll learn rules, tricks, and games to write without mistakes.",
        mascota_texto="Fun spelling makes writing well easy and exciting.",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=28,
                    padding=ft.Padding(left=22, right=22, top=28, bottom=28),
                    width=280,
                    shadow=_shadow(20, 8, "16"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Text("🐝", size=80),
                            ft.Text(
                                "Fun spelling makes writing well easy and exciting.",
                                size=18, color=PURPLE, weight=ft.FontWeight.W_700,
                                text_align=ft.TextAlign.CENTER,
                                style=ft.TextStyle(height=1.4),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=LIGHT_PURPLE, border_radius=16,
                    padding=ft.Padding(left=18, right=18, top=10, bottom=10),
                    content=ft.Text("Rules · Tricks · Games", size=14, weight=ft.FontWeight.W_800, color=PURPLE),
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
#  STEP 2 -- Read carefully
# ===================================================

def build_paso_2(on_next, on_prev=None):
    barra, _ = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Read each line calmly before continuing.",
        texto_siguiente="Continue",
    )

    panel = panel_instrucciones(
        titulo="Read carefully",
        subtitulo="Read the following text and discover the spelling mistakes hidden in it.",
        mascota_texto="Look closely at each word, some are spelled incorrectly.",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=22,
            controls=[
                ft.Container(
                    width=300,
                    bgcolor=WHITE,
                    border_radius=28,
                    padding=ft.Padding(left=22, right=22, top=28, bottom=26),
                    shadow=_shadow(18, 6, "14"),
                    content=ft.Column(
                        spacing=18,
                        controls=[
                            ft.Text(
                                "Yesterday I went to the park with my freind.\n"
                                "It was definitly sunny and we sat on the grass to eat ice cream.\n"
                                "Afterward we walked until the lake and saw alot of ducks,\n"
                                "wich was the best part of the day.",
                                size=19, color=DARK,
                                text_align=ft.TextAlign.LEFT,
                                weight=ft.FontWeight.W_500,
                                style=ft.TextStyle(height=1.5),
                            ),
                            ft.Row(
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME, color=AMBER, size=24),
                                    ft.Text("Time: 60 seconds", size=16, color=GRAY_TEXT),
                                ],
                            ),
                        ],
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
    return fondo_pantalla(GRAD_YELLOW, contenido)


# ===================================================
#  STEP 3 -- Understand and discover
# ===================================================

def build_paso_3(on_next, on_prev=None):
    palabras = [
        {"palabra": "freind", "correcta": "friend", "incorrecta": "freind"},
        {"palabra": "definitly", "correcta": "definitely", "incorrecta": "definitly"},
        {"palabra": "alot", "correcta": "a lot", "incorrecta": "alot"},
        {"palabra": "wich", "correcta": "which", "incorrecta": "wich"},
    ]
    respuestas = [None, None, None, None]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Choose the correctly spelled option for each word.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Understand and discover",
        subtitulo="Select the correct option for each highlighted word in the text.",
        mascota_texto="Calmly compare both options and choose the one that's spelled correctly.",
    )

    def on_seleccionar(idx, opcion, card_a, card_b):
        def handler(e):
            respuestas[idx] = opcion
            marcar_seleccion(card_a, opcion == "a", ok=True)
            marcar_seleccion(card_b, opcion == "b", ok=False)
            if all(r is not None for r in respuestas):
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "Great! You selected all the options 🎉", ok=True)
                btn_continuar.visible = True
            e.page.update()
        return handler

    filas = []
    for i, p in enumerate(palabras):
        card_a = ft.Container(
            width=132, height=56, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Row(
                spacing=8, alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("a)", size=15, weight=ft.FontWeight.W_800, color=GREEN),
                    ft.Text(p["correcta"], size=15, weight=ft.FontWeight.W_700, color=DARK),
                ],
            ),
        )
        card_b = ft.Container(
            width=132, height=56, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Row(
                spacing=8, alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("b)", size=15, weight=ft.FontWeight.W_800, color=GRAY_TEXT),
                    ft.Text(p["incorrecta"], size=15, weight=ft.FontWeight.W_700, color=DARK),
                ],
            ),
        )
        card_a.on_click = on_seleccionar(i, "a", card_a, card_b)
        card_b.on_click = on_seleccionar(i, "b", card_a, card_b)

        filas.append(
            ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=30, height=30, border_radius=15, bgcolor=GREEN,
                                alignment=CENTER,
                                content=ft.Text(str(i + 1), size=14, weight=ft.FontWeight.W_900, color=WHITE),
                            ),
                            ft.Text(p["palabra"], size=16, weight=ft.FontWeight.W_700, color=DARK),
                        ],
                    ),
                    ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER,
                           wrap=True, controls=[card_a, card_b]),
                ],
            )
        )

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[*filas, ft.Container(height=6), feedback_banner],
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
    return fondo_pantalla(GRAD_GREEN, contenido)


# ===================================================
#  STEP 4 -- Think deeper
# ===================================================

def build_paso_4(on_next, on_prev=None):
    opciones = [
        {"texto": "It follows the rule 'i before e, except after c'.", "emoji": "🧠", "correcto": True},
        {"texto": "It's spelled with 'e' first because of a silent letter rule.", "emoji": "📖", "correcto": False},
        {"texto": "It has a double letter because it's a compound word.", "emoji": "✏️", "correcto": False},
        {"texto": "It's written as one word because it's a single word.", "emoji": "💬", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Think about the spelling rule before choosing.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Think deeper",
        subtitulo="Choose the rule that explains why the word 'friend' is spelled this way.",
        mascota_texto="Don't rush, calmly read each option before answering.",
    )

    tarjetas_refs = []
    correct_idx = next(j for j, o in enumerate(opciones) if o["correcto"])

    def on_elegir(idx_elegido):
        def handler(e):
            for i, card in enumerate(tarjetas_refs):
                if i == correct_idx:
                    marcar_seleccion(card, True, ok=True)
                elif i == idx_elegido:
                    marcar_seleccion(card, True, ok=False)
                else:
                    marcar_seleccion(card, False)
            if idx_elegido == correct_idx:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "Correct! 🧠 It follows 'i before e, except after c'.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=230, height=170, border_radius=20,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            ink=True, animate=_anim(180), shadow=_shadow(12, 4, "10"),
            padding=ft.Padding(left=16, right=16, top=18, bottom=18),
            on_click=on_elegir(i),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(op["emoji"], size=48),
                    ft.Text(op["texto"], size=14, weight=ft.FontWeight.W_600, color=DARK,
                            text_align=ft.TextAlign.CENTER, style=ft.TextStyle(height=1.3)),
                ],
            ),
        )
        tarjetas_refs.append(card)
        cards.append(card)

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=22,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=18,
                       controls=cards[:2], wrap=True),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=18,
                       controls=cards[2:], wrap=True),
                feedback_banner,
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
    return fondo_pantalla(GRAD_BLUE, contenido)


# ===================================================
#  STEP 5 -- Practice by playing
# ===================================================

def build_paso_5(on_next, on_prev=None):
    oraciones = [
        {"texto": "Tomorrow we will go to the", "texto2": None, "respuesta": "park"},
        {"texto": "Don't forget your", "texto2": None, "respuesta": "backpack"},
        {"texto": "My favorite", "texto2": "is pizza.", "respuesta": "food"},
        {"texto": "The", "texto2": "shines a lot today.", "respuesta": "sun"},
    ]
    respuestas = [None, None, None, None]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Type the word that completes each sentence.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Practice by playing",
        subtitulo="Complete the sentences with the correct word to keep moving forward.",
        mascota_texto="Great job! You're improving every day.",
    )

    filas = []
    for i, o in enumerate(oraciones):
        input_field = ft.TextField(
            width=160, height=52, border_radius=14,
            border_color=CARD_BORDER_IDLE, text_size=15,
            text_align=ft.TextAlign.CENTER, bgcolor=WHITE,
        )

        def make_handler(idx, inp):
            def on_change(e):
                valor = inp.value
                respuestas[idx] = valor
                if valor and valor.lower().strip() == oraciones[idx]["respuesta"].lower():
                    inp.border_color = GREEN
                    inp.bgcolor = SUCCESS_BG
                else:
                    inp.border_color = ERROR_RED
                    inp.bgcolor = ERROR_BG
                if all(r is not None and r != "" for r in respuestas):
                    correctas = sum(
                        1 for j, r in enumerate(respuestas)
                        if r and r.lower().strip() == oraciones[j]["respuesta"].lower()
                    )
                    if correctas == len(oraciones):
                        mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                          "Great job! You're improving every day 🎉", ok=True)
                        btn_continuar.visible = True
                    else:
                        mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                          f"You have {correctas}/{len(oraciones)} correct. Try again.", ok=False)
                e.page.update()
            return on_change

        input_field.on_change = make_handler(i, input_field)

        segunda_fila_controles = [input_field]
        if o["texto2"]:
            segunda_fila_controles.append(ft.Text(o["texto2"], size=17, color=DARK))

        filas.append(
            ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=32, height=32, border_radius=16, bgcolor=PURPLE,
                                alignment=CENTER,
                                content=ft.Text(str(i + 1), size=14, weight=ft.FontWeight.W_900, color=WHITE),
                            ),
                            ft.Text(o["texto"], size=17, color=DARK),
                        ],
                    ),
                    ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                           wrap=True, controls=segunda_fila_controles),
                ],
            )
        )

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[*filas, ft.Container(height=6), feedback_banner],
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
    return fondo_pantalla(GRAD_LIGHT, contenido)


# ===================================================
#  STEP 6 -- Dixi's Challenge
# ===================================================

def build_paso_6(on_next, on_prev=None):
    texto_original = (
        "My brother and I went shopping downtown. We bought fruit, juice, and bread. "
        "We were in the store for more then two hours. Afterward we went home very tired but happy."
    )
    errores = {"then": "than"}
    errores_encontrados = set()

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Tap the word that has a spelling mistake.",
        siguiente_visible=False,
        texto_siguiente="Finish",
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()
    contador = ft.Text(f"Mistakes found: 0/{len(errores)}", size=15, color=GRAY_TEXT, weight=ft.FontWeight.W_600)

    panel = panel_instrucciones(
        titulo="Dixi's Challenge",
        subtitulo="Find and correct all the spelling mistakes hidden in the text.",
        mascota_texto="You can find all the mistakes! Read word by word.",
    )

    def on_click_palabra(palabra):
        def handler(e):
            if palabra in errores and palabra not in errores_encontrados:
                errores_encontrados.add(palabra)
                contador.value = f"Mistakes found: {len(errores_encontrados)}/{len(errores)}"
                if len(errores_encontrados) >= len(errores):
                    btn_continuar.visible = True
                    mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                      "Excellent! You found all the mistakes 🏆", ok=True)
                else:
                    mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                      f"Correct! '{palabra}' should be written '{errores[palabra]}' 🎉", ok=True)
            elif palabra in errores_encontrados:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  f"You already found this mistake: '{palabra}' → '{errores[palabra]}'", ok=True)
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  f"'{palabra}' is spelled correctly.", ok=False)
            e.page.update()
        return handler

    texto_controls = []
    for palabra in texto_original.split():
        palabra_limpia = palabra.strip(".,;:!?")
        texto_controls.append(
            ft.Container(
                padding=ft.Padding(left=3, right=3, top=3, bottom=3),
                border_radius=6,
                ink=True,
                on_click=on_click_palabra(palabra_limpia),
                content=ft.Text(
                    palabra_limpia, size=18,
                    color=RED if palabra_limpia in errores else DARK,
                    weight=ft.FontWeight.W_700 if palabra_limpia in errores_encontrados else ft.FontWeight.W_400,
                ),
            )
        )

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=28,
                    padding=ft.Padding(left=16, right=16, top=24, bottom=24),
                    shadow=_shadow(18, 6, "14"),
                    content=ft.Row(spacing=6, wrap=True, controls=texto_controls),
                ),
                contador,
                feedback_banner,
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
    return fondo_pantalla(GRAD_PINK, contenido)


# ===================================================
#  MAIN BUILDER
# ===================================================

def build_ortografia_divertida(
    page: ft.Page,
    usuario: str = "",
    on_lecciones=None,
    on_inicio=None,
):
    TOTAL_PASOS = 6  # 6 steps + celebration
    paso_actual = [0]

    barra = ft.Container()
    contenido = ft.Container(expand=True)

    def ir_a_paso(n):
        paso_actual[0] = n
        if n >= TOTAL_PASOS:
            barra.visible = False
            contenido.content = build_celebracion(
                on_repasar=lambda e: ir_a_paso(0),
                on_continuar=lambda e: (on_lecciones(e) if on_lecciones else None),
                usuario=usuario,
                nivel=3, num=2,
                titulo='Fun Spelling',
            )
        else:
            barra.visible = True
            barra.content = top_progress_bar(
                paso=n, total=TOTAL_PASOS,
                on_home=lambda e: (on_inicio(e) if on_inicio else None),
            )
            builders = [
                build_paso_1,
                build_paso_2,
                build_paso_3,
                build_paso_4,
                build_paso_5,
                build_paso_6,
            ]
            contenido.content = builders[n](
                on_next=lambda e: ir_a_paso(paso_actual[0] + 1),
                on_prev=lambda e: ir_a_paso(max(0, paso_actual[0] - 1)),
            )
        page.update()

    barra.content = top_progress_bar(
        paso=0, total=TOTAL_PASOS,
        on_home=lambda e: (on_inicio(e) if on_inicio else None),
    )
    contenido.content = build_paso_1(
        on_next=lambda e: ir_a_paso(1),
        on_prev=lambda e: None,
    )

    return ft.Column(
        expand=True, spacing=0,
        controls=[barra, contenido],
    )
