"""Lesson 4: Basic Reading.

English version: same behavior and same public API as the original
file (build_lectura_basica, build_paso_1..6, top_progress_bar), but
with the same "horizontal" PC-format layout used in
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
from audio_utils import play_audio
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
NIVEL = 1

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
GRAD_PINK = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])
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
        subtitulo="Today we're going to read some very easy words. Let's discover a world of adventures together.",
        mascota_texto="Reading is discovering a world of adventures.",
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
                    padding=ft.Padding(left=22, right=22, top=26, bottom=26),
                    width=280,
                    shadow=_shadow(20, 8, "16"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Text("🐝", size=90),
                            ft.Text(
                                "Reading is discovering a world of adventures.",
                                size=18, color=PURPLE, weight=ft.FontWeight.W_700,
                                text_align=ft.TextAlign.CENTER,
                                style=ft.TextStyle(height=1.4),
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
#  STEP 2 -- Read the word (tap and listen)
# ===================================================

def build_paso_2(on_next, on_prev=None):
    palabras = [
        {"texto": "apple", "emoji": "🍎"},
        {"texto": "dog", "emoji": "🐶"},
        {"texto": "sun", "emoji": "☀️"},
    ]
    tocadas = set()

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Tap each word to hear it.",
        siguiente_visible=False,
    )

    panel = panel_instrucciones(
        titulo="Read the word",
        subtitulo="Tap each word and listen to it carefully.",
        mascota_texto="Tap the three cards, one by one, and listen to how they sound.",
    )

    tarjetas = []
    for p in palabras:
        card_bg = ft.Container(
            bgcolor=WHITE,
            border_radius=20,
            width=300,
            padding=ft.Padding(left=20, right=20, top=14, bottom=14),
            border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            shadow=_shadow(12, 4, "10"),
            ink=True, animate=_anim(180),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(spacing=16, controls=[
                        ft.Text(p["emoji"], size=44),
                        ft.Text(p["texto"], size=28, weight=ft.FontWeight.W_800, color=PURPLE),
                    ]),
                    ft.IconButton(
                        icon=ft.Icons.VOLUME_UP_ROUNDED,
                        icon_color=PURPLE,
                        icon_size=30,
                        on_click=lambda e, word=p["texto"]: play_audio(e.page, "words", word),
                    ),
                ],
            ),
        )

        def make_handler(palabra, card):
            def on_tap(e):
                tocadas.add(palabra)
                marcar_seleccion(card, True, ok=True)
                if len(tocadas) >= len(palabras):
                    btn_continuar.visible = True
                e.page.update()
            return on_tap

        card_bg.on_click = make_handler(p["texto"], card_bg)
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
#  STEP 3 -- Match word and picture (tap-based drag simulation)
# ===================================================

def build_paso_3(on_next, on_prev=None):
    pares = [
        {"palabra": "moon", "emoji": "🌙"},
        {"palabra": "cat", "emoji": "🐱"},
        {"palabra": "house", "emoji": "🏠"},
    ]
    estado = {"seleccion": None, "aciertos": 0}

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Tap a word, then its picture.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Match word and picture",
        subtitulo="Tap a word on the left, then its matching picture.",
        mascota_texto="First choose the word, then find its picture.",
    )

    word_cards = {}
    img_cards = {}

    def on_select_word(palabra):
        def handler(e):
            estado["seleccion"] = palabra
            for p, c in word_cards.items():
                marcar_seleccion(c, p == palabra, ok=True) if p == palabra else marcar_seleccion(c, False)
            e.page.update()
        return handler

    def on_select_img(emoji, palabra_correcta):
        def handler(e):
            sel = estado["seleccion"]
            if sel is None:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "First tap a word on the left.", ok=False)
                e.page.update()
                return
            if sel == palabra_correcta:
                marcar_seleccion(word_cards[sel], True, ok=True)
                marcar_seleccion(img_cards[emoji], True, ok=True)
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
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                                  "Try again 🙂", ok=False)
            e.page.update()
        return handler

    left_col = []
    for p in pares:
        c = ft.Container(
            width=150, height=64, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Text(p["palabra"], size=22, weight=ft.FontWeight.W_800, color=DARK),
        )
        c.on_click = on_select_word(p["palabra"])
        word_cards[p["palabra"]] = c
        left_col.append(c)

    pares_mezclados = pares[:]
    random.shuffle(pares_mezclados)
    right_col = []
    for p in pares_mezclados:
        c = ft.Container(
            width=110, height=88, border_radius=16,
            bgcolor=WHITE, border=ft.Border.all(1.5, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(8, 3, "0A"),
            content=ft.Text(p["emoji"], size=48),
        )
        c.on_click = on_select_img(p["emoji"], p["palabra"])
        img_cards[p["emoji"]] = c
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
#  STEP 4 -- Read the sentence
# ===================================================

def build_paso_4(on_next, on_prev=None):
    oracion = "The cat sleeps."

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Press the speaker and read out loud.",
        siguiente_visible=False,
    )

    panel = panel_instrucciones(
        titulo="Read the sentence",
        subtitulo="Listen and read the sentence out loud, following each word with your finger.",
        mascota_texto="Great job! Keep reading slowly and with confidence.",
    )

    def on_escuchar(e):
        btn_continuar.visible = True
        e.page.update()

    def on_click_audio(e):
        play_audio(e.page, "words", "cat")
        on_escuchar(e)

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Container(
                    bgcolor=WHITE,
                    border_radius=28,
                    padding=ft.Padding(left=20, right=20, top=22, bottom=22),
                    shadow=_shadow(18, 6, "14"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=14,
                        controls=[
                            ft.Container(
                                width=54, height=54, border_radius=27, bgcolor=PURPLE,
                                alignment=CENTER, ink=True,
                                content=ft.IconButton(
                                    icon=ft.Icons.VOLUME_UP_ROUNDED,
                                    icon_color=WHITE,
                                    icon_size=26,
                                    on_click=on_click_audio,
                                ),
                            ),
                            ft.Text(
                                oracion, size=26, weight=ft.FontWeight.W_900, color=DARK,
                                expand=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                ),
                ft.Text("🐝", size=90),
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
#  STEP 5 -- What does it say? (Read and choose the picture)
# ===================================================

def build_paso_5(on_next, on_prev=None):
    oracion = "The girl drinks milk."
    opciones = [
        {"emoji": "👦", "correcto": False},
        {"emoji": "👧🥛", "correcto": True},
        {"emoji": "👧📖", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Read the sentence and choose the correct picture.",
        siguiente_visible=False,
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="What does it say?",
        subtitulo="Read the sentence and choose the picture that shows what it says.",
        mascota_texto="Read calmly and find the matching picture.",
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
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Correct! 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        if op["emoji"] == "👧🥛":
            contenido_tarjeta = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text("👧", size=42),
                    ft.Text("🥛", size=24),
                ],
            )
        elif op["emoji"] == "👧📖":
            contenido_tarjeta = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text("👧", size=42),
                    ft.Text("📖", size=24),
                ],
            )
        else:
            contenido_tarjeta = ft.Text(op["emoji"], size=54)

        card = ft.Container(
            width=90, height=90, border_radius=20,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180), shadow=_shadow(12, 4, "10"),
            on_click=on_elegir(i),
            content=contenido_tarjeta,
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
                    bgcolor=WHITE,
                    border_radius=28,
                    padding=ft.Padding(left=22, right=22, top=18, bottom=18),
                    shadow=_shadow(14, 5, "12"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Container(
                                width=54, height=54, border_radius=27,
                                bgcolor=PURPLE, alignment=CENTER,
                                content=ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=WHITE, size=26),
                            ),
                            ft.Text(
                                oracion, size=22, weight=ft.FontWeight.W_700, color=DARK,
                                expand=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                ),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True,
                      spacing=14, run_spacing=14, controls=cards),
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
#  STEP 6 -- Put the story in order
# ===================================================

def build_paso_6(on_next, on_prev=None):
    oraciones = [
        "The boy plants the seed.",
        "He waters the plant every day.",
        "The plant grows happy.",
    ]
    emojis = ["🌱", "🌿", "🌳"]

    barra, btn_continuar = barra_inferior(
        on_prev or (lambda e: None), on_next,
        hint_texto="Select the sentences in the correct order.",
        siguiente_visible=False,
        texto_siguiente="Finish",
    )
    feedback_banner, feedback_icono, feedback_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Put the story in order",
        subtitulo="Select the correct sentence for each box, in the right order.",
        mascota_texto="Think about what happens first, what happens next, and how it ends.",
    )

    dropdowns = []
    for i in range(3):
        dd = ft.Dropdown(
            width=200, height=54, border_radius=16,
            bgcolor=WHITE, border_color=CARD_BORDER_IDLE, text_size=14,
            hint_text=f"Select sentence {i + 1}",
            options=[ft.dropdown.Option(o) for o in oraciones],
        )
        dropdowns.append(dd)

    def on_comprobar(e):
        seleccionadas = [dd.value for dd in dropdowns]
        if None in seleccionadas or "" in seleccionadas:
            mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Select all 3 sentences 🙂", ok=False)
            e.page.update()
            return
        if seleccionadas == oraciones:
            mostrar_resultado(feedback_banner, feedback_icono, feedback_texto, "Perfect order! 🎉", ok=True)
            btn_continuar.visible = True
        else:
            mostrar_resultado(feedback_banner, feedback_icono, feedback_texto,
                              "That's not the right order. Try again 🙂", ok=False)
        e.page.update()

    filas = [
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Container(
                    width=36, height=36, border_radius=18, bgcolor=PURPLE,
                    alignment=CENTER,
                    content=ft.Text(str(i + 1), size=16, weight=ft.FontWeight.W_900, color=WHITE),
                ),
                dropdowns[i],
                ft.Text(emojis[i], size=32),
            ],
        )
        for i in range(3)
    ]

    area = ft.Container(
        width=300,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                *filas,
                ft.Container(height=6),
                ft.Button(
                    "Check",
                    bgcolor=AMBER, color=WHITE,
                    on_click=on_comprobar,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=22),
                        padding=ft.Padding(left=40, right=40, top=16, bottom=16),
                    ),
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
    return fondo_pantalla(GRAD_GREEN, contenido)


# ===================================================
#  MAIN BUILDER
# ===================================================

def build_lectura_basica(
    page: ft.Page,
    usuario: str = "",
    on_lecciones=None,
    on_inicio=None,
    on_siguiente=None,
    num_leccion: int = 3,
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
                on_continuar=(lambda e: (on_siguiente(e) if on_siguiente else (on_lecciones(e) if on_lecciones else None))),
                usuario=usuario,
                nivel=1, num=num_leccion,
                titulo='Basic Words',
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
