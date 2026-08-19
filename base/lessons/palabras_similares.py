"""Lesson - Similar Words (Synonyms) - Level 2, Lesson 1.

English version: same behavior and same public API as the original
file (build_palabras_similares, build_paso_1..6, top_progress_bar),
but with the same "horizontal" PC-format layout used in
reconoce_letras.py:

  - Fixed instructions panel on the left (title + text + Dixi), with
    the full height of the screen.
  - Interactive area on the right, which expands and uses all the
    remaining horizontal space.
  - Random image background (like in reconoce_letras.py) instead of
    the flat solid color of each step.
  - "Dixi" mascot (bee) with a speech bubble, integrated inside the
    instructions panel.
  - Option cards and pills with smooth transitions, result banner
    with icon and color, "Tip" pill.
"""

import random

import flet as ft
from config import TOTAL_STEPS, PURPLE, WHITE, GRAY_TEXT, DARK, AMBER, GREEN, LIGHT_PURPLE, CENTER
from components.celebration import build_celebracion

# Width of the fixed instructions panel on the left (PC horizontal format)
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
#  Additional palette (only for this lesson, does not depend on config)
# ---------------------------------------------------
RED = "#E53935"
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
GRAD_LIGHT = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FBF9FF", "#F2EEFF"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])
GRAD_GREEN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])


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
#  "Dixi" mascot (the app's bee) + speech bubble
# ---------------------------------------------------

def dixi_mascota(mensaje, tamano=64, ancho_globo=190):
    """Owl mascot with its speech bubble cheering us on to keep playing."""
    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Stack(
                width=tamano * 1.1, height=tamano * 1.5,
                controls=[
                    ft.Container(top=tamano * 0.22, content=ft.Text("🦉", size=tamano)),
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
    """Wraps a step's content with an image background + decorations.

    The content receives the full available width of the screen; each
    step internally builds its own horizontal layout (instructions
    panel + interactive area).
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
#  HINT PILL, RESULT BANNER AND NAVIGATION
# ===================================================

def hint_pill(texto):
    """Tip pill with a circular icon (consistent throughout the lesson)."""
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
                    spacing=2, tight=True, width=230,
                    controls=[
                        ft.Text("Tip", size=12, weight=ft.FontWeight.W_800, color=PURPLE),
                        ft.Text(
                            texto, size=13, color=GRAY_TEXT,
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                            style=ft.TextStyle(height=1.25),
                        ),
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
    """Updates the result banner with the message and state (correct/incorrect)."""
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
    """Applies the 'selected'/'tapped' style to a card (border + background)."""
    if activo:
        card.border = ft.Border.all(3, GREEN if ok else ERROR_RED)
        card.bgcolor = SUCCESS_BG if ok else ERROR_BG
    else:
        card.border = ft.Border.all(1.5, CARD_BORDER_IDLE)
        card.bgcolor = WHITE


def barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=True,
                    texto_siguiente="Next", siguiente_visible=True):
    """Back / hint / Next row. Returns (row, next_button)."""
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
    """White card fixed on the left, with the full height of the
    screen, that holds the step's title/instruction and (optionally)
    Dixi cheering the learner on."""
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
#  STEP 1 -- Introduction with Dixi
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
        subtitulo="Today we're going to discover similar words: words that mean almost the same thing.",
        mascota_texto="Similar words are words that mean almost the same thing.",
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
                    padding=ft.Padding(left=20, right=20, top=26, bottom=26),
                    width=280,
                    shadow=_shadow(20, 8, "16"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Text("🐝", size=90),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                                controls=[
                                    ft.Text("happy", size=22, weight=ft.FontWeight.W_800, color=PURPLE),
                                    ft.Text("≈", size=26, weight=ft.FontWeight.W_900, color=PURPLE),
                                    ft.Text("glad", size=22, weight=ft.FontWeight.W_800, color=PURPLE),
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
    return fondo_pantalla(GRAD_PURPLE, contenido)


# ===================================================
#  STEP 2 -- Listen and learn
# ===================================================

def build_paso_2(on_next, on_prev=None):
    pares_palabras = [
        ("happy", "glad", "😊"),
        ("fast", "quick", "⚡"),
        ("small", "little", "🔹"),
    ]
    tocadas = set()

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Tap each pair to hear it.",
        siguiente_visible=False,
    )

    panel = panel_instrucciones(
        titulo="Listen and learn",
        subtitulo="Tap each pair of similar words and listen to them carefully.",
        mascota_texto="Notice how both words in each pair mean almost the same thing.",
    )

    tarjetas = []
    for p1, p2, emoji in pares_palabras:
        card_bg = ft.Container(
            bgcolor=WHITE,
            border_radius=20,
            width=300,
            padding=ft.Padding(left=18, right=18, top=14, bottom=14),
            border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            shadow=_shadow(12, 4, "10"),
            ink=True, animate=_anim(180),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Text(emoji, size=36),
                        ft.Text(p1, size=22, weight=ft.FontWeight.W_800, color=PURPLE),
                        ft.Text("≈", size=26, weight=ft.FontWeight.W_900, color=PURPLE),
                        ft.Text(p2, size=22, weight=ft.FontWeight.W_800, color=PURPLE),
                    ]),
                    ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=28),
                ],
            ),
        )

        def make_handler(par, card):
            def on_tap(e):
                tocadas.add(par)
                marcar_seleccion(card, True, ok=True)
                if len(tocadas) >= len(pares_palabras):
                    btn_continuar.visible = True
                e.page.update()
            return on_tap

        card_bg.on_click = make_handler((p1, p2), card_bg)
        tarjetas.append(card_bg)

    area = ft.Container(
        width=300,
        content=ft.Column(spacing=16, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=tarjetas),
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
#  STEP 3 -- Match the similar words
# ===================================================

def build_paso_3(on_next, on_prev=None):
    pares = [
        ("house", "home"),
        ("glad", "happy"),
        ("begin", "start"),
        ("brave", "bold"),
    ]
    estado = {"seleccion": None, "aciertos": 0}

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Tap a word, then its match.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Match the similar words",
        subtitulo="Tap a word on the left, then its similar word on the right.",
        mascota_texto="Think about the meaning of each word before matching it.",
    )

    word_cards = {}
    similar_cards = {}

    def on_select_word(palabra):
        def handler(e):
            estado["seleccion"] = palabra
            for p, c in word_cards.items():
                marcar_seleccion(c, p == palabra, ok=True) if p == palabra else marcar_seleccion(c, False)
            e.page.update()
        return handler

    def on_select_similar(similar, palabra_correcta):
        def handler(e):
            sel = estado["seleccion"]
            if sel is None:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "First tap a word on the left.", ok=False)
                e.page.update()
                return
            if sel == palabra_correcta:
                marcar_seleccion(word_cards[sel], True, ok=True)
                marcar_seleccion(similar_cards[similar], True, ok=True)
                estado["aciertos"] += 1
                estado["seleccion"] = None
                if estado["aciertos"] >= len(pares):
                    btn_continuar.visible = True
                    mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                      "Excellent! You matched everything correctly 🎉", ok=True)
                else:
                    mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                      f"Correct! ({estado['aciertos']}/{len(pares)})", ok=True)
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    left_col = []
    for p, _ in pares:
        c = ft.Container(
            width=128, height=62, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Text(p, size=17, weight=ft.FontWeight.W_800, color=DARK),
        )
        c.on_click = on_select_word(p)
        word_cards[p] = c
        left_col.append(c)

    pares_mezclados = pares[:]
    random.shuffle(pares_mezclados)
    right_col = []
    for p, s in pares_mezclados:
        c = ft.Container(
            width=128, height=62, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Text(s, size=17, weight=ft.FontWeight.W_800, color=DARK),
        )
        c.on_click = on_select_similar(s, p)
        similar_cards[s] = c
        right_col.append(c)

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
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
    return fondo_pantalla(GRAD_LIGHT, contenido)


# ===================================================
#  STEP 4 -- Choose the similar word
# ===================================================

def build_paso_4(on_next, on_prev=None):
    palabra = "sad"
    emoji = "😢"
    opciones = [
        {"texto": "happy", "correcto": False},
        {"texto": "joyful", "correcto": False},
        {"texto": "upset", "correcto": True},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Choose the word that means almost the same thing.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Choose the similar word",
        subtitulo="Select the word that means almost the same as the word shown.",
        mascota_texto="Think about the feeling the word 'sad' describes.",
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
                                  "Correct! 🎉 Sad and upset are similar.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=280, height=64, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(10, 3, "0A"),
            on_click=on_elegir(i),
            content=ft.Text(op["texto"], size=20, weight=ft.FontWeight.W_700, color=DARK),
        )
        tarjetas_refs.append(card)
        cards.append(card)

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=28,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=28,
                    padding=ft.Padding(left=24, right=24, top=20, bottom=20),
                    shadow=_shadow(14, 5, "12"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=18,
                        controls=[
                            ft.Text(emoji, size=52),
                            ft.Text(palabra, size=36, weight=ft.FontWeight.W_900, color=DARK),
                            ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=30),
                        ],
                    ),
                ),
                ft.Column(spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=cards),
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
    return fondo_pantalla(GRAD_LIGHT, contenido)


# ===================================================
#  STEP 5 -- Complete the sentence
# ===================================================

def build_paso_5(on_next, on_prev=None):
    opciones = [
        {"texto": "angry", "correcto": False},
        {"texto": "generous", "correcto": True},
        {"texto": "shy", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Choose the similar word that completes the sentence.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Complete the sentence",
        subtitulo="Choose the similar word that best completes the sentence shown.",
        mascota_texto="Read the whole sentence before choosing your answer.",
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
                                  "Correct! 🎉 'Generous' means giving without expecting anything in return.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=280, height=64, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(10, 3, "0A"),
            on_click=on_elegir(i),
            content=ft.Text(op["texto"], size=20, weight=ft.FontWeight.W_700, color=DARK),
        )
        tarjetas_refs.append(card)
        cards.append(card)

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=28,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=28,
                    padding=ft.Padding(left=26, right=26, top=22, bottom=22),
                    shadow=_shadow(14, 5, "12"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=14,
                        controls=[
                            ft.Text("My brother is very", size=24, color=DARK),
                            ft.Container(
                                content=ft.Text("________", size=30, weight=ft.FontWeight.W_900, color=GRAY_TEXT),
                                padding=ft.Padding(left=26, right=26, top=12, bottom=12),
                                bgcolor="#F5F5F5", border_radius=12,
                                border=ft.Border.all(2, CARD_BORDER_IDLE),
                            ),
                            ft.Text(", because he always helps me.", size=24, color=DARK, text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                ),
                ft.Column(spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=cards),
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
    return fondo_pantalla(GRAD_YELLOW, contenido)


# ===================================================
#  STEP 6 -- Create your pair
# ===================================================

def build_paso_6(on_next, on_prev=None):
    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Write a word and its similar word.",
        siguiente_visible=False,
        texto_siguiente="Finish",
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Create your pair",
        subtitulo="Write a word, then another one that means almost the same thing.",
        mascota_texto="Example: smart ≈ clever. Now make up your own!",
    )

    palabra_input = ft.TextField(
        label="Word", hint_text="Write a word",
        border_radius=16, border_color=PURPLE, width=220, text_size=16,
    )
    similar_input = ft.TextField(
        label="Similar word", hint_text="Write its match",
        border_radius=16, border_color=GREEN, width=220, text_size=16,
    )

    def verificar_pareja(e):
        if palabra_input.value and similar_input.value:
            mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                              f"Great pair! {palabra_input.value} ≈ {similar_input.value} 🎉", ok=True)
            btn_continuar.visible = True
        else:
            mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Write both words 🙂", ok=False)
        e.page.update()

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=28,
                    padding=ft.Padding(left=22, right=22, top=24, bottom=24),
                    shadow=_shadow(14, 5, "12"),
                    content=ft.Column(
                        spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            palabra_input,
                            ft.Text("≈", size=26, color=PURPLE, weight=ft.FontWeight.W_900),
                            similar_input,
                        ],
                    ),
                ),
                ft.Button(
                    "Check",
                    bgcolor=AMBER, color=WHITE, on_click=verificar_pareja,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=22),
                        padding=ft.Padding(left=40, right=40, top=16, bottom=16),
                    ),
                ),
                feedback_banner,
                ft.Container(
                    bgcolor=WHITE, border_radius=16,
                    padding=ft.Padding(left=16, right=16, top=10, bottom=10),
                    content=ft.Text("💡 Example: smart ≈ clever", size=15, color=DARK,
                                    text_align=ft.TextAlign.CENTER),
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
    return fondo_pantalla(GRAD_LIGHT, contenido)


# ===================================================
#  MAIN BUILDER
# ===================================================

def build_palabras_similares(
    page: ft.Page,
    usuario: str = "",
    on_lecciones=None,
    on_inicio=None,
):
    TOTAL_PASOS = 6
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
                nivel=2, num=1,
                titulo='Similar Words',
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
