"""Lesson 1: Recognize the letters - Polished visual design, PC format.

English version: same behavior and same public API as the original
file (build_reconoce_letras, build_paso_1..6, build_top_bar_rico,
barra_inferior, hint_pill, fondo_pantalla, fondo_decorativo, GRAD_*),
but with a "horizontal" layout that takes advantage of the full width
of the screen (PC format), instead of stacking everything in a single
centered column:

  - Fixed instructions panel on the left (title + text + Dixi), with
    the full height of the screen.
  - Interactive area on the right, which expands and uses all the
    remaining horizontal space (cards, grid, drag zone, etc.).
  - "Dixi" mascot (owl) with a speech bubble, now integrated inside
    the instructions panel.
  - Drag zone with a real dotted border (simulated with segments) and
    decorative sparkles, just like in the design references.
  - Option cards with smooth transitions (animate) on selection.
  - Result banner (correct / incorrect) with icon and color, instead
    of plain text.
  - "Tip" pill with a circular icon, consistent throughout the app.
"""

import random

import flet as ft
from audio_utils import play_audio
from pantalla import progreso as prog
from config import TOTAL_STEPS, PURPLE, WHITE, GRAY_TEXT, DARK, AMBER, GREEN, LIGHT_PURPLE, CENTER
from components.celebration import build_celebracion

# Width of the fixed instructions panel on the left (PC horizontal format)
SIDE_PANEL_WIDTH = 320

# Available background images (inside the "imagenes" folder); one is
# chosen at random each time a lesson screen is built.
FONDOS_IMAGENES = [
    "imagenes/fondo1.png",
    "imagenes/fondo2.png",
    "imagenes/fondo3.png",
]

# Level of this lesson (for the top bar)
NIVEL = 1

# Gradient alignments (same pattern already used in other lessons of the project)
_GRAD_TOP = ft.Alignment(0, -1)
_GRAD_BOTTOM = ft.Alignment(0, 1)

# ---------------------------------------------------
#  Additional palette (only for this lesson, does not depend on config)
# ---------------------------------------------------
ERROR_RED = "#E5484D"
SUCCESS_BG = "#EEFBF1"
SUCCESS_BORDER = "#C3ECCB"
ERROR_BG = "#FDEEEE"
ERROR_BORDER = "#F3C7C7"
CARD_BORDER_IDLE = "#EFECF9"

# Reusable animations (a new instance every time one is requested, to
# avoid sharing the same object between different controls)
def _anim(ms=180, curva="easeOut"):
    return ft.Animation(ms, curva)


def _shadow(blur=10, dy=3, alpha="0F"):
    return ft.BoxShadow(blur_radius=blur, color=f"#{alpha}000000", offset=ft.Offset(0, dy))


# ===================================================
#  GRADIENT BACKGROUNDS (one per step, with more depth)
# ===================================================

GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_PEACH = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFBEF", "#FFF1D2"])
GRAD_PINK = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])
GRAD_GREEN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])


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
#  "Dixi" mascot (the app's owl) + speech bubble
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
    """Wraps a step's content with a gradient + decorations.

    Unlike the previous version (which centered the content in a
    narrow, fixed-width column), the content now receives the FULL
    available width of the screen -- each step internally builds its
    own horizontal layout (instructions panel + interactive area).
    `mascota_texto` is kept for compatibility, for steps that still
    want an extra floating Dixi bubble; the newer steps already
    integrate Dixi inside the instructions panel.
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
#  HINT PILL, RESULT BANNER AND NAVIGATION
# ===================================================

def hint_pill(texto):
    """Tip pill with a circular icon (consistent throughout the lesson)."""
    return ft.Container(
        bgcolor=WHITE, border_radius=18,
        padding=ft.Padding(left=12, right=14, top=8, bottom=8),
        shadow=_shadow(10, 3, "12"),
        content=ft.Row(
            spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=30, height=30, border_radius=15, bgcolor=LIGHT_PURPLE,
                    alignment=CENTER, content=ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=AMBER, size=16),
                ),
                ft.Column(
                    spacing=0, tight=True, width=200,
                    controls=[
                        ft.Text("Tip", size=11, weight=ft.FontWeight.W_800, color=PURPLE),
                        ft.Text(
                            texto, size=12, color=GRAY_TEXT,
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                            style=ft.TextStyle(height=1.25),
                        ),
                    ],
                ),
            ],
        ),
    )


def crear_banner_resultado():
    """Creates a result banner (correct/incorrect) with icon + text.

    Returns the container ready to insert into the layout; use
    `mostrar_resultado(banner, mensaje, ok)` to update it.
    """
    icono = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=GREEN, size=22)
    texto = ft.Text("", size=15, weight=ft.FontWeight.W_700, color=GREEN, expand=True,
                    style=ft.TextStyle(height=1.3))
    banner = ft.Container(
        visible=False,
        width=300,
        bgcolor=SUCCESS_BG,
        border=ft.Border.all(1.5, SUCCESS_BORDER),
        border_radius=16,
        padding=ft.Padding(left=18, right=18, top=12, bottom=12),
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


def marcar_seleccion(card, activo):
    """Applies the 'selected' style to an option card (border + background)."""
    card.border = ft.Border.all(4, PURPLE) if activo else ft.Border.all(2, CARD_BORDER_IDLE)
    card.bgcolor = LIGHT_PURPLE if activo else WHITE


def _opcion_pill(letra, on_click):
    """Wide pill row with the letter on the left and a circular indicator
    on the right (option-list style). Returns (container, indicator)
    so the selection state can be updated from outside."""
    indicador = ft.Container(
        width=28, height=28, border_radius=14,
        border=ft.Border.all(2, CARD_BORDER_IDLE),
        bgcolor=WHITE,
        alignment=CENTER,
        animate=_anim(160),
    )
    pill = ft.Container(
        width=270, height=68, border_radius=20,
        bgcolor=WHITE,
        border=ft.Border.all(2, CARD_BORDER_IDLE),
        ink=True, animate=_anim(180),
        shadow=_shadow(10, 3, "10"),
        on_click=on_click,
        padding=ft.Padding(left=22, right=22, top=0, bottom=0),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(letra, size=30, weight=ft.FontWeight.W_900, color=PURPLE),
                indicador,
            ],
        ),
    )
    return pill, indicador


def _marcar_pill(pill, indicador, estado):
    """Updates an option pill according to its state: None (idle),
    True (correct/selected) or False (incorrect/selected)."""
    if estado is None:
        pill.border = ft.Border.all(2, CARD_BORDER_IDLE)
        pill.bgcolor = WHITE
        indicador.bgcolor = WHITE
        indicador.border = ft.Border.all(2, CARD_BORDER_IDLE)
        indicador.content = None
    elif estado is True:
        pill.border = ft.Border.all(2.5, GREEN)
        pill.bgcolor = SUCCESS_BG
        indicador.bgcolor = GREEN
        indicador.border = ft.Border.all(2, GREEN)
        indicador.content = ft.Icon(ft.Icons.CHECK_ROUNDED, color=WHITE, size=18)
    else:
        pill.border = ft.Border.all(2.5, ERROR_RED)
        pill.bgcolor = ERROR_BG
        indicador.bgcolor = ERROR_RED
        indicador.border = ft.Border.all(2, ERROR_RED)
        indicador.content = ft.Icon(ft.Icons.CLOSE_ROUNDED, color=WHITE, size=18)


def barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=True,
                    texto_siguiente="Next", siguiente_visible=True):
    """Back / hint / Next row. Returns (row, next_button) so each step
    can show/hide 'Next' depending on the answer."""
    atras_btn = ft.Button(
        content=ft.Row(
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, color=PURPLE, size=16),
                ft.Text("Back", color=PURPLE, size=14, weight=ft.FontWeight.W_700),
            ],
        ),
        bgcolor=WHITE,
        on_click=on_prev,
        visible=mostrar_atras,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, "#EDEAFB"),
            shape=ft.RoundedRectangleBorder(radius=24),
            elevation=0,
            padding=ft.Padding(left=16, right=16, top=8, bottom=8),
        ),
    )
    siguiente_btn = ft.Button(
        content=ft.Row(
            spacing=6,
            controls=[
                ft.Text(texto_siguiente, color=WHITE, size=14, weight=ft.FontWeight.W_700),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=WHITE, size=16),
            ],
        ),
        bgcolor=PURPLE,
        on_click=on_next,
        visible=siguiente_visible,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=24),
            elevation=2,
            padding=ft.Padding(left=18, right=18, top=8, bottom=8),
        ),
    )
    centro = hint_pill(hint_texto) if hint_texto else ft.Container()
    fila = ft.Container(
        padding=ft.Padding(left=12, right=12, top=0, bottom=16),
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                centro,
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[atras_btn, siguiente_btn],
                ),
            ],
        ),
    )
    return fila, siguiente_btn


# ===================================================
#  PANEL DE INSTRUCCIONES (columna fija a la izquierda)
# ===================================================

def panel_instrucciones(titulo, subtitulo, icono_emoji=None, mascota_texto=None, extra=None):
    """White card fixed on the left, with the full height of the
    screen, that holds the step's title/instruction and (optionally)
    Dixi cheering the learner on. Each step's interactive area lives
    separately, on the right, and uses the rest of the available
    width."""
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
    vertically so everything fits on a phone-width screen. The whole
    block scrolls if the content is taller than the visible area,
    instead of overflowing off-screen."""
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
        texto_siguiente="Let's start!",
    )

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="Today we'll learn the letters. Look closely at each one, listen to it, and have fun with me.",
        mascota_texto="Look closely at the letter and listen to it. Let's get started together!",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Stack(
                    width=260, height=150,
                    controls=[
                        ft.Container(
                            left=0, top=30, width=210,
                            bgcolor=WHITE, border_radius=18,
                            padding=ft.Padding(left=18, right=18, top=16, bottom=16),
                            shadow=_shadow(14, 4, "16"),
                            content=ft.Text(
                                "This is the letter\nwe're going to\nlearn today:",
                                size=15, color=DARK, style=ft.TextStyle(height=1.35),
                            ),
                        ),
                        ft.Container(left=14, top=0, content=ft.Text("⭐", size=20)),
                        ft.Container(right=0, top=40, content=ft.Text("🐝", size=90)),
                    ],
                ),
                ft.Container(
                    width=110, height=110, border_radius=24,
                    bgcolor=WHITE,
                    alignment=CENTER,
                    shadow=_shadow(22, 8, "22"),
                    content=ft.Text("A", size=64, weight=ft.FontWeight.W_900, color=PURPLE),
                ),
                ft.Button(
                    width=220,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=18),
                            ft.Text("Listen to letter", color=PURPLE, size=14, weight=ft.FontWeight.W_700),
                        ],
                        spacing=8,
                    ),
                    bgcolor=WHITE,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(2, PURPLE),
                        shape=ft.RoundedRectangleBorder(radius=22),
                        elevation=0,
                        padding=ft.Padding(left=20, right=20, top=10, bottom=10),
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
#  STEP 2 -- Listen and choose
# ===================================================

def build_paso_2(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Listen carefully and choose the correct letter.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Listen and choose",
        subtitulo='Press the speaker, listen carefully to the sound, and tap the matching letter.',
        mascota_texto="Close your eyes, listen to the sound, and choose the matching letter.",
    )

    opciones = ["A", "E", "I"]
    correcta = "A"
    pills = {}

    def on_select(letra):
        def handler(e):
            for l, (pill, indicador) in pills.items():
                if l == letra:
                    _marcar_pill(pill, indicador, letra == correcta)
                else:
                    _marcar_pill(pill, indicador, None)
            if letra == correcta:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! 🎉", ok=True)
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            btn_continuar.visible = (letra == correcta)
            e.page.update()
        return handler

    pills_col = []
    for op in opciones:
        pill, indicador = _opcion_pill(op, None)
        pill.on_click = on_select(op)
        pills[op] = (pill, indicador)
        pills_col.append(pill)

    # Columna izquierda: boton de sonido "en ondas" + reproductor + abeja
    audio_bar = ft.ProgressBar(
        value=0.0,
        color=PURPLE,
        bgcolor="#E0D4FF",
        bar_height=8,
        border_radius=4,
        width=140,
    )

    columna_audio = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.Stack(
                width=170, height=170,
                alignment=CENTER,
                controls=[
                    ft.Container(width=170, height=170, border_radius=85, bgcolor=WHITE, opacity=0.30),
                    ft.Container(width=134, height=134, border_radius=67, bgcolor=WHITE, opacity=0.5,
                                left=18, top=18),
                    ft.Container(
                        left=33, top=33, width=104, height=104, border_radius=52,
                        bgcolor=WHITE, alignment=CENTER, shadow=_shadow(20, 7, "22"),
                        content=ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=44),
                    ),
                    ft.Container(left=6, top=4, content=ft.Text("✨", size=16)),
                    ft.Container(right=2, top=24, content=ft.Text("✦", size=14, color=AMBER)),
                ],
            ),
            ft.Container(
                bgcolor=WHITE, border_radius=24,
                shadow=_shadow(12, 3, "15"),
                padding=ft.Padding(left=18, right=18, top=12, bottom=12),
                content=ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.PLAY_ARROW_ROUNDED,
                            icon_color=PURPLE,
                            icon_size=22,
                            on_click=lambda e: play_audio(e.page, "letters", "a", progress_bar=audio_bar),
                        ),
                        audio_bar,
                    ],
                ),
            ),
            ft.Text("🐝", size=56),
        ],
    )

    # Columna derecha: pregunta + lista de opciones + resultado
    columna_opciones = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.Text("Which letter do you hear?", size=18, weight=ft.FontWeight.W_800, color=PURPLE),
            *pills_col,
            banner,
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[columna_audio, columna_opciones],
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
    return fondo_pantalla(GRAD_PEACH, contenido)


# ===================================================
#  STEP 3 -- Find the letter
# ===================================================

def build_paso_3(on_next, on_prev):
    grilla_letras = ["A", "B", "A", "C", "D", "A", "E", "F", "A", "G", "H", "A"]
    seleccionadas = set()
    total_correctas = grilla_letras.count("A")

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto='Find and tap all the letter "A"s.',
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Find the letter",
        subtitulo='Tap all the letter "A"s you find in the grid.',
        icono_emoji="🐝",
        mascota_texto='Go through the grid calmly and tap only the letter "A"s.',
    )

    grilla_cards = []

    colores = ["#C9B8F0", "#F5A623", "#2ECC71", "#E57373", "#64B5F6", "#C9B8F0",
               "#AED581", "#F06292", "#FFB74D", "#81C784", "#7986CB", "#BA68C8"]

    def on_tap(idx):
        def handler(e):
            letra = grilla_letras[idx]
            card = grilla_cards[idx]
            if letra == "A":
                if idx not in seleccionadas:
                    seleccionadas.add(idx)
                    card.bgcolor = PURPLE
                    card.content.color = WHITE
                else:
                    seleccionadas.discard(idx)
                    card.bgcolor = colores[idx % len(colores)]
                    card.content.color = WHITE
            else:
                card.bgcolor = ERROR_RED
                mostrar_resultado(banner, banner_icono, banner_texto, "That's not an A 😅", ok=False)

            if len(seleccionadas) == total_correctas:
                mostrar_resultado(banner, banner_icono, banner_texto, "You found all the A's! 🎉", ok=True)
                btn_continuar.visible = True
            e.page.update()
        return handler

    grilla_controls = []
    for i, letra in enumerate(grilla_letras):
        card = ft.Container(
            width=66, height=66, border_radius=33,
            bgcolor=colores[i % len(colores)],
            alignment=CENTER, ink=True,
            animate=_anim(180),
            shadow=_shadow(10, 3, "18"),
            on_click=on_tap(i),
            content=ft.Text(letra, size=28, weight=ft.FontWeight.W_900, color=WHITE),
        )
        grilla_cards.append(card)
        grilla_controls.append(card)

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[
            ft.Row(
                wrap=True, spacing=14, run_spacing=14,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=grilla_controls,
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
    return fondo_pantalla(GRAD_PINK, contenido)


# ===================================================
#  STEP 4 -- Drag to the right spot
# ===================================================

def _caja_punteada(width, height, color=PURPLE, grosor=3, largo=10, hueco=7):
    """Simulates a dotted border (Flet doesn't support it natively) with
    small rounded segments spread around the perimeter of the rectangle."""
    segmentos = []
    x = hueco
    while x < width - hueco - largo:
        segmentos.append(ft.Container(left=x, top=0, width=largo, height=grosor,
                                      bgcolor=color, border_radius=grosor))
        segmentos.append(ft.Container(left=x, top=height - grosor, width=largo, height=grosor,
                                      bgcolor=color, border_radius=grosor))
        x += largo + hueco
    y = hueco
    while y < height - hueco - largo:
        segmentos.append(ft.Container(left=0, top=y, width=grosor, height=largo,
                                      bgcolor=color, border_radius=grosor))
        segmentos.append(ft.Container(left=width - grosor, top=y, width=grosor, height=largo,
                                      bgcolor=color, border_radius=grosor))
        y += largo + hueco
    return ft.Stack(width=width, height=height, controls=segmentos)


def tooltip_flecha(icono, texto):
    """Small pill with icon + text, used for the drag instructions."""
    return ft.Container(
        bgcolor=WHITE, border_radius=18,
        padding=ft.Padding(left=16, right=18, top=10, bottom=10),
        shadow=_shadow(10, 3, "15"),
        content=ft.Row(
            spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icono, color=PURPLE, size=18),
                ft.Text(texto, size=14, color=DARK, weight=ft.FontWeight.W_600),
            ],
        ),
    )


def etiqueta_nombre(nombre):
    """Small white pill with the name of the picture (e.g. 'Ant')."""
    return ft.Container(
        bgcolor=WHITE, border_radius=14,
        padding=ft.Padding(left=18, right=18, top=6, bottom=6),
        shadow=_shadow(8, 2, "10"),
        content=ft.Text(nombre, size=15, weight=ft.FontWeight.W_800, color=PURPLE),
    )


def build_paso_4(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto='Look, think, and drag the letter "A" to the box.',
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Drag to the right spot",
        subtitulo='Drag the letter "A" to the dotted box to complete the challenge.',
        mascota_texto='You can do it! Look, think, and drag the letter "A" to the box.',
    )

    ZONA = 118

    zona_fondo = ft.Container(
        width=ZONA, height=ZONA, border_radius=22, bgcolor="#F1ECFF", animate=_anim(280),
    )
    zona_punteada = _caja_punteada(ZONA, ZONA, color=PURPLE)
    zona_letra = ft.Text("A", size=50, weight=ft.FontWeight.W_900, color="#C9B8F0")

    def on_accept(e):
        zona_fondo.bgcolor = PURPLE
        zona_punteada.visible = False
        zona_letra.value = "A"
        zona_letra.color = WHITE
        mostrar_resultado(banner, banner_icono, banner_texto, "Perfect! The letter A is in its place 🎉", ok=True)
        btn_continuar.visible = True
        e.page.update()

    drag = ft.Draggable(
        group="letra",
        content=ft.Container(
            width=88, height=88, border_radius=18,
            bgcolor=WHITE,
            alignment=CENTER,
            shadow=_shadow(16, 5, "22"),
            content=ft.Text("A", size=50, weight=ft.FontWeight.W_900, color=PURPLE),
        ),
        content_feedback=ft.Container(
            width=88, height=88, border_radius=18,
            bgcolor=PURPLE, alignment=CENTER, opacity=0.85,
            content=ft.Text("A", size=50, weight=ft.FontWeight.W_900, color=WHITE),
        ),
    )

    zona_stack = ft.Stack(
        width=ZONA, height=ZONA,
        controls=[
            zona_fondo,
            zona_punteada,
            ft.Container(width=ZONA, height=ZONA, alignment=CENTER, content=zona_letra),
        ],
    )
    zona = ft.DragTarget(group="letra", content=zona_stack, on_accept=on_accept)

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=26,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Text("🐜", size=56),
                            etiqueta_nombre("Ant"),
                            drag,
                        ],
                    ),
                    ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=PURPLE, size=26),
                    zona,
                ],
            ),
            tooltip_flecha(ft.Icons.TOUCH_APP_ROUNDED, "Drag the letter to the box"),
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
    return fondo_pantalla(GRAD_PURPLE, contenido)


# ===================================================
#  STEP 5 -- Where is the "A"?
# ===================================================

def build_paso_5(on_next, on_prev):
    correcta = "airplane"
    opciones = [("tree", "🌳"), ("bee", "🐝"), ("airplane", "✈️")]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto='Find the picture that starts with the letter "A".',
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo='Where is the "A"?',
        subtitulo="Say the name of each picture out loud and choose the one that starts with the letter A.",
        icono_emoji="🐝",
        mascota_texto="Say the name of each picture out loud and listen to how it starts.",
    )

    cards_dict = {}
    # A different background color behind each emoji to tell them apart,
    # but all evenly aligned (same size, no unevenness).
    circulo_colores = ["#FFE7C2", "#FFD9E4", "#D9F2E3"]

    def on_select(opcion):
        def handler(e):
            for op, card in cards_dict.items():
                marcar_seleccion(card, op == opcion)
            if opcion == correcta:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! Airplane starts with A 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "That doesn't start with A, try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, (nombre, emoji) in enumerate(opciones):
        card = ft.Container(
            width=98, height=130, border_radius=20,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            on_click=on_select(nombre),
            shadow=_shadow(14, 5, "12"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Container(
                        width=58, height=58, border_radius=29,
                        bgcolor=circulo_colores[i % len(circulo_colores)],
                        alignment=CENTER,
                        content=ft.Text(emoji, size=30),
                    ),
                    ft.Text(nombre.capitalize(), size=14, color=DARK, weight=ft.FontWeight.W_600),
                ],
            ),
        )
        cards_dict[nombre] = card
        cards.append(card)

    columna_mascota = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            ft.Text("🐝", size=64),
            ft.Container(
                width=260, bgcolor=WHITE, border_radius=18,
                padding=ft.Padding(left=18, right=18, top=14, bottom=14),
                shadow=_shadow(12, 4, "12"),
                content=ft.Text(
                    "Listen to each word and tap the picture that starts with A.",
                    size=13, color=DARK, style=ft.TextStyle(height=1.4), text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            columna_mascota,
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=14, run_spacing=14, controls=cards),
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
    return fondo_pantalla(GRAD_GREEN, contenido)


# ===================================================
#  STEP 6 -- Complete the word
# ===================================================

def build_paso_6(on_next, on_prev):
    correcta = "A"
    opciones = ["A", "E", "I"]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Choose the missing letter to complete the word.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Complete the word",
        subtitulo="Look at the picture and choose the missing letter to complete the word.",
        mascota_texto="Think about which letter is missing to complete the word AIRPLANE.",
    )

    letra_cards_dict = {}
    blank_card = None

    def on_select(opcion):
        def handler(e):
            for op, card in letra_cards_dict.items():
                marcar_seleccion(card, op == opcion)
            if opcion == correcta:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! The word is AIRPLANE 🎉", ok=True)
                btn_continuar.visible = True
                if blank_card is not None:
                    blank_card.content = ft.Text("A", size=52, weight=ft.FontWeight.W_900, color=PURPLE)
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Hmm, that's not it... try another letter 🙂", ok=False)
            e.page.update()
        return handler

    letra_cards = []
    for op in opciones:
        card = ft.Container(
            width=78, height=78, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            on_click=on_select(op),
            shadow=_shadow(12, 4, "10"),
            content=ft.Text(op, size=38, weight=ft.FontWeight.W_900, color=PURPLE),
        )
        letra_cards_dict[op] = card
        letra_cards.append(card)

    blank_card = ft.Container(
        width=68, height=68, border_radius=14,
        bgcolor=LIGHT_PURPLE,
        border=ft.Border.all(3, PURPLE),
        alignment=CENTER,
        animate=_anim(220),
        content=ft.Text("_", size=38, weight=ft.FontWeight.W_900, color=PURPLE),
    )

    # Tarjeta destacada con la palabra a formar
    tarjeta_palabra = ft.Container(
        width=300,
        bgcolor=WHITE, border_radius=28,
        shadow=_shadow(20, 8, "16"),
        padding=ft.Padding(left=20, right=20, top=28, bottom=26),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Container(
                    width=84, height=84, border_radius=42, bgcolor="#FFF4CE",
                    alignment=CENTER,
                    content=ft.Text("✈️", size=44),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        blank_card,
                        ft.Text("irplane", size=32, weight=ft.FontWeight.W_700, color=DARK),
                    ],
                ),
                ft.Container(
                    bgcolor=LIGHT_PURPLE, border_radius=12,
                    padding=ft.Padding(left=14, right=14, top=6, bottom=6),
                    content=ft.Text("A I R P L A N E", size=13, weight=ft.FontWeight.W_800, color=PURPLE),
                ),
            ],
        ),
    )

    columna_opciones = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            ft.Text("Choose the missing letter", size=17, weight=ft.FontWeight.W_800, color=PURPLE,
                    text_align=ft.TextAlign.CENTER),
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=16, run_spacing=16,
                  controls=letra_cards),
            banner,
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[tarjeta_palabra, columna_opciones],
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
#  MAIN LESSON CONTROLLER
# ===================================================

def build_reconoce_letras(page: ft.Page, usuario: str,
                          on_lecciones=None, on_inicio=None):
    paso_actual = {"idx": 0}
    # Usa el total real guardado en la base del usuario, sin inventar puntos.
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
                num=1,
                titulo="Recognize letters",
            )

    def on_next(e=None):
        go_to(paso_actual["idx"] + 1)

    def on_prev(e=None):
        go_to(max(0, paso_actual["idx"] - 1))

    def on_repasar(e=None):
        go_to(0)

    def on_continuar_final(e=None):
        if on_lecciones:
            on_lecciones()

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
