"""Lesson 3: Simple Syllables - Polished visual design, PC layout.

Same visual language as reconoce_letras.py: fixed instructions panel on
the left (with Dixi), interactive area on the right using the full
width, background image + decorations, cards with transitions, and a
result banner. The logic of each step (words, pairs, ordering,
etc.) is exactly the same as in the original file.
"""

import random

import flet as ft
from audio_utils import play_audio
from pantalla import progreso as prog
from config import TOTAL_STEPS, PURPLE, WHITE, GRAY_TEXT, DARK, AMBER, GREEN, LIGHT_PURPLE, CENTER, BLUE
from components.celebration import build_celebracion

# Width of the fixed instructions panel on the left (PC horizontal layout)
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

# Extra colors not in config.py
RED = "#E53935"
ORANGE = "#FF9800"
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
#  GRADIENT BACKGROUNDS (one per step)
# ===================================================

GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_PEACH = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFBEF", "#FFF1D2"])
GRAD_BLUE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EEF6FF", "#D9EBFF"])
GRAD_PINK = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])
GRAD_CYAN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EAFBFF", "#D3F3FA"])
GRAD_LILAC = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F8EEFF", "#EBD9FA"])


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


def dixi_mascota(mensaje, tamano=64, ancho_globo=190):
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
#  FULL TOP BAR
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
                                ft.Text("done", size=12, color=GRAY_TEXT),
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


def marcar_seleccion(card, activo, color_ok=None):
    """Aplica el estilo de 'seleccionado' a una tarjeta de opcion (borde + fondo).
    Si se pasa color_ok, se usa como color de fondo cuando activo=True (util
    para tarjetas de silaba que ya usan un color propio)."""
    card.border = ft.Border.all(4, PURPLE) if activo else ft.Border.all(2, CARD_BORDER_IDLE)
    card.bgcolor = (color_ok or LIGHT_PURPLE) if activo else WHITE


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
#  INSTRUCTIONS PANEL (fixed left column)
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
        texto_siguiente="Let's start!",
    )

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="Today we'll learn about syllables. Syllables are parts of words that join together to form whole words.",
        mascota_texto="Together we can build lots of words. Let's get started!",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Stack(
                            width=250, height=170,
                            controls=[
                                ft.Container(
                                    left=10, top=34, width=230,
                                    bgcolor=WHITE, border_radius=18,
                                    padding=ft.Padding(left=18, right=18, top=16, bottom=16),
                                    shadow=_shadow(14, 4, "16"),
                                    content=ft.Text(
                                        "Together we can\nbuild lots of\nwords!",
                                        size=16, color=DARK, style=ft.TextStyle(height=1.35),
                                    ),
                                ),
                                ft.Container(left=24, top=0, content=ft.Text("⭐", size=22)),
                            ],
                        ),
                        ft.Text("🐝", size=90),
                    ],
                ),
                ft.Container(
                    width=180, height=128, border_radius=24,
                    bgcolor=WHITE,
                    alignment=CENTER,
                    shadow=_shadow(22, 8, "22"),
                    content=ft.Text("SUN-NY", size=36, weight=ft.FontWeight.W_900, color=PURPLE),
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
#  STEP 2 -- Match the syllables
# ===================================================

def build_paso_2(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Tap a syllable on the left, then its matching pair on the right.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Match the syllables",
        subtitulo="Form words by joining each syllable on the left with its correct match on the right.",
        mascota_texto="Tap a syllable, then find its match to form a word.",
    )

    silabas_izq = ["rab", "pen", "mon"]
    silabas_der = ["bit", "cil", "key"]
    parejas_correctas = {("rab", "bit"), ("pen", "cil"), ("mon", "key")}
    seleccionadas = set()
    colores_silabas = {"rab": PURPLE, "pen": BLUE, "mon": RED, "bit": ORANGE, "cil": AMBER, "key": GREEN}

    izq_cards = {}
    der_cards = {}
    seleccion_izq = {"valor": None}

    def _card_silaba(silaba, on_click):
        return ft.Container(
            width=120, height=75, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            shadow=_shadow(10, 3, "10"),
            on_click=on_click,
            content=ft.Text(silaba, size=32, weight=ft.FontWeight.W_900, color=colores_silabas.get(silaba, PURPLE)),
        )

    def on_select_izq(silaba):
        def handler(e):
            seleccion_izq["valor"] = silaba
            for s, card in izq_cards.items():
                marcar_seleccion(card, s == silaba)
            e.page.update()
        return handler

    def on_select_der(silaba):
        def handler(e):
            elegido = seleccion_izq["valor"]
            if elegido is None:
                return
            par = (elegido, silaba)
            if par in parejas_correctas and par not in seleccionadas:
                seleccionadas.add(par)
                izq_cards[elegido].border = ft.Border.all(3, GREEN)
                izq_cards[elegido].bgcolor = SUCCESS_BG
                der_cards[silaba].border = ft.Border.all(3, GREEN)
                der_cards[silaba].bgcolor = SUCCESS_BG
                mostrar_resultado(banner, banner_icono, banner_texto, f"{elegido}{silaba}! 🎉", ok=True)
            elif par not in parejas_correctas:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try another combination 🙂", ok=False)
                marcar_seleccion(izq_cards[elegido], False)

            if len(seleccionadas) == len(parejas_correctas):
                btn_continuar.visible = True

            seleccion_izq["valor"] = None
            e.page.update()
        return handler

    izq_col = []
    for s in silabas_izq:
        card = _card_silaba(s, None)
        card.on_click = on_select_izq(s)
        izq_cards[s] = card
        izq_col.append(card)

    der_col = []
    for s in silabas_der:
        card = _card_silaba(s, None)
        card.on_click = on_select_der(s)
        der_cards[s] = card
        der_col.append(card)

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Text("🐝", size=90),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=60,
                controls=[
                    ft.Column(spacing=18, controls=izq_col),
                    ft.Column(spacing=18, controls=der_col),
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
    return fondo_pantalla(GRAD_PEACH, contenido)


# ===================================================
#  STEP 3 -- Put the syllables in order
# ===================================================

def build_paso_3(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Tap the syllables in the right order to form the word.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Put the syllables in order",
        subtitulo="Tap the syllables in the right order to form the word BUTTERFLY.",
        icono_emoji="🦋",
        mascota_texto="Think carefully about the order before tapping each syllable.",
    )

    silabas = ["ter", "but", "fly"]
    orden_correcto = ["but", "ter", "fly"]
    orden_usuario = []
    silaba_cards = {}

    slots = []
    for i in range(3):
        slot = ft.Container(
            width=100, height=75, border_radius=18,
            bgcolor="#F8F6FF",
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER,
            animate=_anim(180),
            content=ft.Text(str(i + 1), size=26, weight=ft.FontWeight.W_700, color="#CCCCCC"),
        )
        slots.append(slot)

    def on_select(silaba):
        def handler(e):
            if silaba in orden_usuario:
                return
            orden_usuario.append(silaba)
            idx = len(orden_usuario) - 1
            marcar_seleccion(silaba_cards[silaba], True)
            slots[idx].content = ft.Text(silaba, size=26, weight=ft.FontWeight.W_900, color=WHITE)
            slots[idx].bgcolor = PURPLE
            slots[idx].border = ft.Border.all(2, PURPLE)

            if orden_usuario == orden_correcto[:len(orden_usuario)]:
                if len(orden_usuario) == len(orden_correcto):
                    mostrar_resultado(banner, banner_icono, banner_texto, "Butterfly! Correct 🎉", ok=True)
                    btn_continuar.visible = True
                else:
                    mostrar_resultado(banner, banner_icono, banner_texto, "Keep going!", ok=True)
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
                orden_usuario.clear()
                for s, card in silaba_cards.items():
                    marcar_seleccion(card, False)
                for i, slot in enumerate(slots):
                    slot.content = ft.Text(str(i + 1), size=26, weight=ft.FontWeight.W_700, color="#CCCCCC")
                    slot.bgcolor = "#F8F6FF"
                    slot.border = ft.Border.all(2, CARD_BORDER_IDLE)

            e.page.update()
        return handler

    cards = []
    for s in silabas:
        card = ft.Container(
            width=100, height=75, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            shadow=_shadow(10, 3, "10"),
            on_click=on_select(s),
            content=ft.Text(s, size=32, weight=ft.FontWeight.W_900, color=PURPLE),
        )
        silaba_cards[s] = card
        cards.append(card)

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=26,
        controls=[
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=16, run_spacing=16, controls=cards),
            ft.Icon(ft.Icons.ARROW_DOWNWARD_ROUNDED, color=PURPLE, size=22),
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=16, run_spacing=16, controls=slots),
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
#  STEP 4 -- Complete the word
# ===================================================

def build_paso_4(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Choose the missing syllable to complete the word.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Complete the word",
        subtitulo="Look at the picture and choose the missing syllable to complete the word.",
        mascota_texto="Think about which syllable is missing to complete the word RABBIT.",
    )

    opciones = ["rab", "rib", "rob", "rub"]
    correcta = "rab"
    silaba_cards = {}
    blank_card = None

    def on_select(silaba):
        def handler(e):
            for s, card in silaba_cards.items():
                marcar_seleccion(card, s == silaba)
            if silaba == correcta:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! The word is RABBIT 🎉", ok=True)
                btn_continuar.visible = True
                if blank_card is not None:
                    blank_card.content = ft.Text("rab", size=22, weight=ft.FontWeight.W_900, color=PURPLE)
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards_row = []
    for op in opciones:
        card = ft.Container(
            width=92, height=92, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            on_click=on_select(op),
            shadow=_shadow(12, 4, "10"),
            content=ft.Text(op, size=30, weight=ft.FontWeight.W_900, color=PURPLE),
        )
        silaba_cards[op] = card
        cards_row.append(card)

    blank_card = ft.Container(
        width=90, height=68, border_radius=14,
        bgcolor=LIGHT_PURPLE,
        border=ft.Border.all(3, PURPLE),
        alignment=CENTER,
        animate=_anim(220),
        content=ft.Text("_", size=34, weight=ft.FontWeight.W_900, color=PURPLE),
    )

    tarjeta_palabra = ft.Container(
        width=290,
        bgcolor=WHITE, border_radius=28,
        shadow=_shadow(20, 8, "16"),
        padding=ft.Padding(left=26, right=26, top=34, bottom=30),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Container(
                    width=100, height=100, border_radius=50, bgcolor="#FCE4EC",
                    alignment=CENTER,
                    content=ft.Text("🐰", size=54),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                    controls=[
                        blank_card,
                        ft.Text("bit", size=32, weight=ft.FontWeight.W_700, color=DARK),
                    ],
                ),
                ft.Container(
                    bgcolor=LIGHT_PURPLE, border_radius=12,
                    padding=ft.Padding(left=14, right=14, top=6, bottom=6),
                    content=ft.Text("RAB BIT", size=13, weight=ft.FontWeight.W_800, color=PURPLE),
                ),
            ],
        ),
    )

    columna_opciones = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            ft.Text("Choose the missing syllable", size=18, weight=ft.FontWeight.W_800, color=PURPLE),
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=14, run_spacing=14,
                   controls=cards_row),
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
    return fondo_pantalla(GRAD_PINK, contenido)


# ===================================================
#  STEP 5 -- Read and choose the picture
# ===================================================

def build_paso_5(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto='Read the syllable "ca" and tap the picture that starts the same way.',
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Read and choose the picture",
        subtitulo='Read the syllable and tap the picture that starts the same way.',
        icono_emoji="🐝",
        mascota_texto="Say each picture's name out loud and find the one that starts with CA.",
    )

    opciones = [("cat", "🐱"), ("dog", "🐶"), ("pig", "🐷")]
    correcta = "cat"
    imagen_cards = {}
    circulo_colores = ["#FFE7C2", "#FFD9E4", "#D9F2E3"]

    def on_select(nombre):
        def handler(e):
            for n, card in imagen_cards.items():
                marcar_seleccion(card, n == nombre)
            if nombre == correcta:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! Cat starts with ca 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, (nombre, emoji) in enumerate(opciones):
        card = ft.Container(
            width=160, height=190, border_radius=24,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True,
            animate=_anim(180),
            on_click=on_select(nombre),
            shadow=_shadow(14, 5, "12"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Container(
                        width=76, height=76, border_radius=38,
                        bgcolor=circulo_colores[i % len(circulo_colores)],
                        alignment=CENTER,
                        content=ft.Text(emoji, size=42),
                    ),
                    ft.Text(nombre.capitalize(), size=16, color=DARK, weight=ft.FontWeight.W_600),
                ],
            ),
        )
        imagen_cards[nombre] = card
        cards.append(card)

    columna_audio = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.Container(
                width=180, height=75, border_radius=38,
                bgcolor=WHITE,
                shadow=_shadow(14, 4, "16"),
                alignment=CENTER,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.VOLUME_UP_ROUNDED,
                            icon_color=PURPLE,
                            icon_size=28,
                            on_click=lambda e: play_audio(e.page, "syllables", "ca"),
                        ),
                        ft.Text("ca", size=36, weight=ft.FontWeight.W_900, color=PURPLE),
                    ],
                ),
            ),
            ft.Text("🐝", size=90),
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=22,
        controls=[
            columna_audio,
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=16, run_spacing=16, controls=cards),
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
    return fondo_pantalla(GRAD_CYAN, contenido)


# ===================================================
#  STEP 6 -- Make more words
# ===================================================

def build_paso_6(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Combine the letters to form 3 different words.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Make more words",
        subtitulo="Use these letters to create 3 different words. Type each one and check your answer.",
        mascota_texto="Try different combinations. There are several possible words!",
    )

    silabas = ["c", "b", "m"]
    palabras_formadas = set()
    input_refs = []

    def es_palabra_valida(palabra: str) -> bool:
        return bool(palabra) and palabra.isalpha() and 2 <= len(palabra) <= 12

    def on_comprobar(e):
        nuevas_correctas = []
        hay_texto = False
        palabras_invalidas = []

        for ref in input_refs:
            palabra = (ref.value or "").strip().lower()
            if not palabra:
                ref.border_color = CARD_BORDER_IDLE
                ref.bgcolor = "#F8F6FF"
                continue

            hay_texto = True
            if es_palabra_valida(palabra) and palabra not in palabras_formadas:
                palabras_formadas.add(palabra)
                nuevas_correctas.append(palabra)
                ref.border_color = GREEN
                ref.bgcolor = "#E9F9EF"
            else:
                palabras_invalidas.append(palabra)
                ref.border_color = RED
                ref.bgcolor = "#FFF1F1"

        if not hay_texto:
            mostrar_resultado(banner, banner_icono, banner_texto, "Type a word first 🙂", ok=False)
        elif len(palabras_formadas) >= 3:
            mostrar_resultado(banner, banner_icono, banner_texto,
                              "Excellent! You found 3 words! 🎉", ok=True)
            btn_continuar.visible = True
        elif nuevas_correctas:
            ultima = nuevas_correctas[-1]
            mensaje = f"{ultima.capitalize()}! Great! ({len(palabras_formadas)}/3)"
            if palabras_invalidas:
                mensaje += " · Some words still need another try."
            mostrar_resultado(banner, banner_icono, banner_texto, mensaje, ok=True)
        else:
            mostrar_resultado(banner, banner_icono, banner_texto,
                              "Try another combination 🙂", ok=False)

        e.page.update()

    silaba_cards = []
    for s in silabas:
        card = ft.Container(
            width=90, height=68, border_radius=18,
            bgcolor=WHITE,
            border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER,
            shadow=_shadow(10, 3, "10"),
            content=ft.Text(s, size=28, weight=ft.FontWeight.W_900, color=PURPLE),
        )
        silaba_cards.append(card)

    inputs = []
    for i in range(3):
        ref = ft.TextField(
            width=230, height=60,
            border_radius=16,
            bgcolor="#F8F6FF",
            border_color=CARD_BORDER_IDLE,
            text_align=ft.TextAlign.CENTER,
            text_size=18,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700, color=DARK),
        )
        input_refs.append(ref)
        inputs.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Container(
                        width=38, height=38, border_radius=19,
                        bgcolor=PURPLE,
                        alignment=CENTER,
                        content=ft.Text(str(i + 1), size=17, weight=ft.FontWeight.W_900, color=WHITE),
                    ),
                    ref,
                ],
            )
        )

    columna_izq = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            ft.Text("🐝", size=80),
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=12, run_spacing=12, controls=silaba_cards),
        ],
    )

    columna_der = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.Column(spacing=12, controls=inputs),
            ft.Button(
                content=ft.Text("Check", color=WHITE, size=15, weight=ft.FontWeight.W_700),
                bgcolor=AMBER,
                on_click=on_comprobar,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=22),
                    padding=ft.Padding(left=32, right=32, top=12, bottom=12),
                ),
            ),
            banner,
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[columna_izq, columna_der],
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
    return fondo_pantalla(GRAD_LILAC, contenido)


# ===================================================
#  MAIN LESSON CONTROLLER
# ===================================================

def build_silabas_simples(page: ft.Page, usuario: str,
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
                titulo="Simple Syllables",
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
