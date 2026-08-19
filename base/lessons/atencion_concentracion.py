"""Lesson - Attention and Concentration - Level 4, Lesson 1.

Redesigned "horizontal" (PC) layout, with the same visual style
as reconoce_letras.py:

  - Fixed instruction panel on the left (title + text + Dixi).
  - Interactive area on the right, using all of the remaining width.
  - Random image background + floating decorations (clouds, sparkles).
  - Option cards, result banner and "Tip" pill,
    consistent with the rest of the app.

The public API stays the same: build_atencion_concentracion(page, usuario,
on_lecciones, on_inicio).
"""

import asyncio
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
NIVEL = 4

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


def mostrar_resultado(banner, icono, texto_ctrl, mensaje, ok=True, alerta=False):
    texto_ctrl.value = mensaje
    if alerta:
        icono.name = ft.Icons.INFO_ROUNDED
        icono.color = AMBER
        texto_ctrl.color = "#B8860B"
        banner.bgcolor = "#FFF8E7"
        banner.border = ft.Border.all(1.5, "#F3E0AC")
    elif ok:
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


def marcar_correcta_incorrecta(card, es_correcta, es_elegida):
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
        subtitulo="We'll train your attention and concentration with fun activities to improve your focus.",
        mascota_texto="Attention is like a lighthouse: it helps you focus on what matters.",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Stack(
                    width=250, height=190,
                    controls=[
                        ft.Container(
                            left=0, top=34, width=230,
                            bgcolor=WHITE, border_radius=18,
                            padding=ft.Padding(left=18, right=18, top=16, bottom=16),
                            shadow=_shadow(14, 4, "16"),
                            content=ft.Text(
                                "Today we\'ll play with\nyour eyes, your ears,\nand your memory.",
                                size=16, color=DARK, style=ft.TextStyle(height=1.35),
                            ),
                        ),
                        ft.Container(left=14, top=0, content=ft.Text("⭐", size=22)),
                    ],
                ),
                ft.Text("🐝", size=90),
                ft.Container(
                    width=280, bgcolor=WHITE, border_radius=24,
                    padding=ft.Padding(left=22, right=22, top=18, bottom=18),
                    shadow=_shadow(20, 7, "18"),
                    content=ft.Text(
                        "Each challenge will\nhelp improve your focus\nand your mind.",
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
#  STEP 2 -- Focus your gaze
# ===================================================

def build_paso_2(on_next, on_prev):
    filas = [
        {"elementos": ["🟢", "🟢", "🟢", "🟢", "🔴"], "diferente_idx": 4},
        {"elementos": ["⭐", "⭐", "✨", "⭐", "⭐"], "diferente_idx": 2},
        {"elementos": ["☕", "☕", "🍵", "☕", "☕"], "diferente_idx": 2},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Calmly look at each row and find the different item.",
        siguiente_visible=False,
    )

    panel = panel_instrucciones(
        titulo="Focus your gaze",
        subtitulo="Find the different object in each of the three rows.",
        mascota_texto="Look row by row, without rushing. You can find them!",
    )

    encontrados = [False, False, False]
    feedback = ft.Text("", size=15, weight=ft.FontWeight.W_700)
    contador = ft.Text("Found: 0/3", size=15, color=GRAY_TEXT, weight=ft.FontWeight.W_700)

    def on_tocar(fila_idx, elemento_idx, card):
        def handler(e):
            if encontrados[fila_idx]:
                return
            if elemento_idx == filas[fila_idx]["diferente_idx"]:
                encontrados[fila_idx] = True
                card.bgcolor = SUCCESS_BG
                card.border = ft.Border.all(3, GREEN)
                total_encontrados = sum(encontrados)
                contador.value = f"Found: {total_encontrados}/3"
                if total_encontrados >= 3:
                    feedback.value = "Excellent! You found all the different ones 🎉"
                    feedback.color = GREEN
                    btn_continuar.visible = True
            else:
                card.bgcolor = ERROR_BG
                card.border = ft.Border.all(3, ERROR_RED)
            e.page.update()
        return handler

    filas_controls = []
    for f_idx, fila in enumerate(filas):
        cards = []
        for e_idx, elem in enumerate(fila["elementos"]):
            card = ft.Container(
                width=48, height=48, border_radius=14,
                bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
                alignment=CENTER, ink=True, animate=_anim(180),
                shadow=_shadow(8, 2, "10"),
                content=ft.Text(elem, size=24),
            )
            card.on_click = on_tocar(f_idx, e_idx, card)
            cards.append(card)
        filas_controls.append(ft.Row(spacing=8, alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=cards))

    tarjeta_filas = ft.Container(
        bgcolor=WHITE, border_radius=28,
        padding=ft.Padding(left=12, right=12, top=24, bottom=24),
        shadow=_shadow(18, 6, "16"),
        content=ft.Column(spacing=18, controls=filas_controls),
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            tarjeta_filas,
            ft.Row(
                spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, color=AMBER, size=22),
                    ft.Text("Take your time to observe", size=15, color=GRAY_TEXT),
                ],
            ),
            contador,
            feedback,
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
#  STEP 3 -- Follow the pattern
# ===================================================

def build_paso_3(on_next, on_prev):
    opciones = [
        {"emoji": "🔵", "texto": "a", "correcto": True},
        {"emoji": "🔺", "texto": "b", "correcto": False},
        {"emoji": "🟡", "texto": "c", "correcto": False},
        {"emoji": "🟢", "texto": "d", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Look at the pattern and choose the shape that comes next.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Follow the pattern",
        subtitulo="Look at the sequence and select the option that continues it.",
        mascota_texto="Notice how the shapes repeat: circle, triangle, square...",
    )

    correct_idx = next(j for j, o in enumerate(opciones) if o["correcto"])
    cards_refs = []

    def on_elegir(idx_elegido):
        def handler(e):
            for i, card in enumerate(cards_refs):
                marcar_correcta_incorrecta(card, i == correct_idx, i == idx_elegido)
            if idx_elegido == correct_idx:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Correct! 🎉 The pattern continues with a circle.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Try again 🙂 Look at the pattern.", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=130, height=130, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            on_click=on_elegir(i),
            shadow=_shadow(12, 4, "12"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Text(op["texto"], size=15, weight=ft.FontWeight.W_700, color=GRAY_TEXT),
                    ft.Text(op["emoji"], size=48),
                ],
            ),
        )
        cards_refs.append(card)
        cards.append(card)

    patron_controls = [
        ft.Text("🔵", size=32), ft.Text("🔺", size=32), ft.Text("🟡", size=32),
        ft.Text("🔵", size=32), ft.Text("🔺", size=32), ft.Text("🟡", size=32),
        ft.Container(
            width=40, height=40, border_radius=10,
            border=ft.Border.all(2, PURPLE),
            alignment=CENTER,
            content=ft.Text("?", size=24, weight=ft.FontWeight.W_900, color=PURPLE),
        ),
    ]

    tarjeta_patron = ft.Container(
        bgcolor=WHITE, border_radius=24,
        padding=ft.Padding(left=14, right=14, top=20, bottom=20),
        shadow=_shadow(16, 5, "14"),
        content=ft.Row(spacing=8, alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=patron_controls),
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=26,
        controls=[
            tarjeta_patron,
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=18, wrap=True, controls=cards),
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
#  STEP 4 -- Auditory concentration
# ===================================================

def build_paso_4(on_next, on_prev):
    opciones = ["2", "3", "4", "5"]
    respuesta_correcta = "4"

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Press the speaker and listen carefully.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Auditory concentration",
        subtitulo="Listen closely to the sound and count how many times the high-pitched tone plays.",
        mascota_texto="Close your eyes and listen with all your attention.",
    )

    correct_idx = opciones.index(respuesta_correcta)
    cards_refs = []

    def on_elegir(idx_elegido, opcion):
        def handler(e):
            for i, card in enumerate(cards_refs):
                marcar_correcta_incorrecta(card, i == correct_idx, i == idx_elegido)
            if opcion == respuesta_correcta:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Correct! 🎉 The high-pitched sound played 4 times.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Try again 🙂 Listen carefully.", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=90, height=90, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            on_click=on_elegir(i, op),
            shadow=_shadow(10, 3, "10"),
            content=ft.Text(op, size=34, weight=ft.FontWeight.W_900, color=DARK),
        )
        cards_refs.append(card)
        cards.append(card)

    reproducir_txt = ft.Text("", size=13, color=BLUE)

    def reproducir_sonido(e):
        reproducir_txt.value = "🔊 Listening... (simulated) The high-pitched sound played 4 times."
        e.page.update()

    columna_audio = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            ft.Stack(
                width=190, height=190,
                alignment=CENTER,
                controls=[
                    ft.Container(width=190, height=190, border_radius=95, bgcolor=WHITE, opacity=0.30),
                    ft.Container(width=150, height=150, border_radius=75, bgcolor=WHITE, opacity=0.5,
                                left=20, top=20),
                    ft.Container(
                        left=38, top=38, width=114, height=114, border_radius=57,
                        bgcolor=WHITE, alignment=CENTER, shadow=_shadow(18, 6, "20"),
                        on_click=reproducir_sonido, ink=True,
                        content=ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, color=PURPLE, size=48),
                    ),
                    ft.Container(left=8, top=6, content=ft.Text("✨", size=16)),
                ],
            ),
            reproducir_txt,
        ],
    )

    columna_pregunta = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            ft.Text("How many times did\nthe higher-pitched sound play?", size=18, weight=ft.FontWeight.W_800,
                    color=PURPLE, text_align=ft.TextAlign.CENTER),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=14, wrap=True, controls=cards),
            banner,
        ],
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[columna_audio, columna_pregunta],
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
#  STEP 5 -- Observe and remember
# ===================================================

def build_paso_5(on_next, on_prev):
    opciones = [
        {"emoji": "🪴", "texto": "A", "correcto": False},
        {"emoji": "🛋️", "texto": "B", "correcto": False},
        {"emoji": "🐱", "texto": "C", "correcto": False},
        {"emoji": "🐠", "texto": "D", "correcto": True},  # Fishbowl - was NOT there
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Look closely at the scene before it disappears.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Observe and remember",
        subtitulo="Look at the image for 20 seconds, then answer which object was missing.",
        mascota_texto="Memorize every detail: the clock, the plant, the cat, and the sofa.",
    )

    timer_text = ft.Text("Time: 20 seconds to look", size=17, color=AMBER, weight=ft.FontWeight.W_700)

    escena = ft.Container(
        bgcolor=WHITE, border_radius=24,
        padding=ft.Padding(left=20, right=20, top=20, bottom=20),
        width=300, height=200,
        shadow=_shadow(16, 5, "14"),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Text("🕐  🪴", size=42),
                ft.Text("🛋️  🐱", size=52),
                ft.Text("🛋️", size=52),
            ],
        ),
    )

    correct_idx = next(j for j, o in enumerate(opciones) if o["correcto"])
    cards_refs = []

    def on_elegir(idx_elegido):
        def handler(e):
            for i, card in enumerate(cards_refs):
                marcar_correcta_incorrecta(card, i == correct_idx, i == idx_elegido)
            if idx_elegido == correct_idx:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Correct! 🎉 The fishbowl was NOT in the image.", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto,
                                  "Try again 🙂 Remember the image carefully.", ok=False)
            e.page.update()
        return handler

    cards = []
    for i, op in enumerate(opciones):
        card = ft.Container(
            width=110, height=110, border_radius=18,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            alignment=CENTER, ink=True, animate=_anim(180),
            on_click=on_elegir(i),
            shadow=_shadow(10, 3, "10"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Text(op["texto"], size=13, weight=ft.FontWeight.W_700, color=GRAY_TEXT),
                    ft.Text(op["emoji"], size=38),
                ],
            ),
        )
        cards_refs.append(card)
        cards.append(card)

    pregunta_container = ft.Container(
        visible=False,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("Which object was NOT in the image?", size=17, weight=ft.FontWeight.W_800, color=DARK),
                ft.Row(spacing=14, alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=cards),
            ],
        ),
    )

    btn_observar = ft.ElevatedButton(
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.VISIBILITY_ROUNDED, color=WHITE, size=20),
                ft.Text("Start observing", color=WHITE, size=15, weight=ft.FontWeight.W_700),
            ],
        ),
        bgcolor=AMBER,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22),
            padding=ft.Padding(left=28, right=28, top=14, bottom=14),
        ),
    )

    def iniciar_observacion(e):
        escena.visible = True
        pregunta_container.visible = False
        btn_continuar.visible = False
        btn_observar.disabled = True
        banner.visible = False
        e.page.update()

        async def countdown():
            for i in range(20, 0, -1):
                timer_text.value = f"Time: {i} seconds to look"
                e.page.update()
                await asyncio.sleep(1)
            escena.visible = False
            pregunta_container.visible = True
            timer_text.value = "Which object was missing? Choose below."
            timer_text.color = PURPLE
            e.page.update()

        e.page.run_task(countdown)

    btn_observar.on_click = iniciar_observacion

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        controls=[
            escena,
            timer_text,
            btn_observar,
            pregunta_container,
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
#  STEP 6 -- Keep your focus
# ===================================================

def build_paso_6(on_next, on_prev):
    simbolos = [
        "🟣", "🔷", "🟦", "🔺", "🔺", "🔷", "🟦", "🔷", "❤️",
        "🔷", "❤️", "🔷", "🔷", "🟣", "❤️", "⭐", "🔷", "🟦",
        "🔺", "🔷", "🟦", "📄", "⭐", "❤️", "🔷", "⭐", "🔷",
    ]
    simbolo_a_contar = "❤️"
    respuesta_correcta = simbolos.count(simbolo_a_contar)

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto=f"Calmly count how many times {simbolo_a_contar} appears.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Keep your focus",
        subtitulo=f"Count how many times this symbol appears: {simbolo_a_contar}",
        mascota_texto="Go through the grid in order, row by row, without skipping any.",
    )

    filas_simbolos = []
    for i in range(0, len(simbolos), 9):
        fila = simbolos[i:i + 9]
        filas_simbolos.append(
            ft.Row(spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                   controls=[ft.Text(s, size=22) for s in fila])
        )

    tarjeta_simbolos = ft.Container(
        bgcolor=WHITE, border_radius=24,
        padding=ft.Padding(left=12, right=12, top=18, bottom=18),
        shadow=_shadow(16, 5, "14"),
        content=ft.Column(spacing=10, controls=filas_simbolos),
    )

    input_respuesta = ft.TextField(
        width=120, height=64,
        border_radius=16,
        border_color=PURPLE,
        text_size=20,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def verificar_respuesta(e):
        try:
            respuesta = int(input_respuesta.value)
        except (TypeError, ValueError):
            mostrar_resultado(banner, banner_icono, banner_texto, "Enter a number.", alerta=True)
            e.page.update()
            return
        if respuesta == respuesta_correcta:
            mostrar_resultado(banner, banner_icono, banner_texto,
                              f"Correct! 🎉 The symbol appears {respuesta_correcta} times.", ok=True)
            btn_continuar.visible = True
        else:
            mostrar_resultado(banner, banner_icono, banner_texto, "Incorrect. Try again 🙂", ok=False)
        e.page.update()

    tarjeta_respuesta = ft.Container(
        bgcolor=WHITE, border_radius=22,
        padding=ft.Padding(left=22, right=22, top=18, bottom=18),
        shadow=_shadow(12, 4, "12"),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Text("Your answer:", size=14, color=GRAY_TEXT),
                input_respuesta,
                ft.ElevatedButton(
                    "Check",
                    bgcolor=GREEN, color=WHITE,
                    on_click=verificar_respuesta,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=14),
                        padding=ft.Padding(left=30, right=30, top=14, bottom=14),
                    ),
                ),
            ],
        ),
    )

    area = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            tarjeta_simbolos,
            tarjeta_respuesta,
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

def build_atencion_concentracion(page: ft.Page, usuario: str = "",
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
                num=1,
                titulo="Attention and concentration",
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
