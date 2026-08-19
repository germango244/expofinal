"""Lesson - Reading Speed - Level 2, Lesson 2.

Polished visual design, PC layout: same visual system as the other
lessons (fixed instructions panel on the left + interactive area
on the right, background image, cards with transitions, result
banner). The logic of the timers (asyncio) and of each step is
the same as in the original file.
"""

import random
import sys
import time
import asyncio
from pathlib import Path

import flet as ft
from pantalla import progreso as prog
from components.celebration import build_celebracion

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Color palette (this file does not depend on config.py, same as the original) ──
PURPLE = "#7B61FF"
AMBER = "#F5A623"
WHITE = "#FFFFFF"
DARK = "#1A1A2E"
GREEN = "#4CAF50"
RED = "#E53935"
BLUE = "#2196F3"
GRAY_TEXT = "#888888"
LIGHT_PURPLE = "#EDE7FF"

ERROR_RED = "#E5484D"
SUCCESS_BG = "#EEFBF1"
SUCCESS_BORDER = "#C3ECCB"
ERROR_BG = "#FDEEEE"
ERROR_BORDER = "#F3C7C7"
CARD_BORDER_IDLE = "#EFECF9"

CENTER = ft.Alignment(0, 0)

SIDE_PANEL_WIDTH = 320
TOTAL_PASOS = 6  # 6 steps + celebration
NIVEL = 2

FONDOS_IMAGENES = [
    "imagenes/fondo1.png",
    "imagenes/fondo2.png",
    "imagenes/fondo3.png",
]

_GRAD_TOP = ft.Alignment(0, -1)
_GRAD_BOTTOM = ft.Alignment(0, 1)


def _anim(ms=180, curva="easeOut"):
    return ft.Animation(ms, curva)


def _shadow(blur=10, dy=3, alpha="0F"):
    return ft.BoxShadow(blur_radius=blur, color=f"#{alpha}000000", offset=ft.Offset(0, dy))


GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])
GRAD_GREEN = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])
GRAD_BLUE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EEF6FF", "#D9EBFF"])
GRAD_LILAC = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F8EEFF", "#EBD9FA"])
GRAD_ROSE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F3", "#FFE1DF"])


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


# ══════════════════════════════════════════════════════════════════════════════
#  TOP BAR WITH PROGRESS DOTS
# ══════════════════════════════════════════════════════════════════════════════
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


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 – Introduction
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_1(on_next, on_prev):
    barra, _ = barra_inferior(
        on_prev, on_next,
        hint_texto=None,
        mostrar_atras=False,
        texto_siguiente="Let's start!",
    )

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="We're going to train your reading speed. You'll read words quickly. Try to beat your best score!",
        mascota_texto="Reading gets better every day you practice. Let's get started!",
    )

    area = ft.Container(
        width=300,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Container(
                    bgcolor=WHITE,
                    border_radius=24,
                    padding=ft.Padding(20, 20, 20, 20),
                    shadow=_shadow(16, 5, "16"),
                    width=280,
                    content=ft.Text(
                        "You'll read words quickly.\nTry to beat your best score!",
                        size=18, color=PURPLE,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[ft.Text("⚡", size=56), ft.Text("🐝", size=76)],
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


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 – Ready, set... (First reading)
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_2(on_next, on_prev, page, on_tiempo=None):
    palabras_grupo1 = [
        ["sun", "moon", "sea", "bread"],
        ["house", "flower", "book", "fish"],
        ["cat", "tree", "cloud", "light"],
        ["table", "fruit", "chair", "clock"],
    ]

    tiempo_inicio = [None]
    tiempo_transcurrido = [0]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Read these words as fast as you can.",
        siguiente_visible=False,
    )

    timer_activo = [False]
    tarea_timer = [None]

    btn_comenzar = ft.Button(
        content=ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700),
        bgcolor=AMBER,
        on_click=lambda e: iniciar_lectura_1(e, page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22),
            padding=ft.Padding(left=32, right=32, top=12, bottom=12),
        ),
    )

    timer_text = ft.Text("", size=20, weight=ft.FontWeight.W_700, color=AMBER)

    def iniciar_lectura_1(e, page):
        if timer_activo[0]:
            timer_activo[0] = False
            if tarea_timer[0] is not None:
                tarea_timer[0].cancel()
            tarea_timer[0] = None
            btn_continuar.visible = True
            timer_text.value = f"✅ Final time: {tiempo_transcurrido[0]} seconds"
            timer_text.color = GREEN
            btn_comenzar.content = ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
            btn_comenzar.bgcolor = AMBER
            if on_tiempo is not None:
                on_tiempo(tiempo_transcurrido[0])
            page.update()
            return

        timer_activo[0] = True
        tiempo_inicio[0] = time.time()
        tiempo_transcurrido[0] = 0
        btn_comenzar.content = ft.Text("Stop ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
        btn_comenzar.bgcolor = RED
        timer_text.value = "⏱️ Time: 0 seconds"
        timer_text.color = AMBER

        async def update_timer():
            while timer_activo[0]:
                await asyncio.sleep(1)
                if not timer_activo[0]:
                    break
                tiempo_transcurrido[0] = int(time.time() - tiempo_inicio[0])
                timer_text.value = f"⏱️ Time: {tiempo_transcurrido[0]} seconds"
                page.update()

        tarea_timer[0] = asyncio.create_task(update_timer())
        page.update()

    panel = panel_instrucciones(
        titulo="Ready, set...",
        subtitulo="Read these words as fast as you can once you press start.",
        mascota_texto="Take a breath, focus, and read each word out loud.",
    )

    palabras_container = ft.Container(
        bgcolor=WHITE,
        border_radius=24,
        padding=ft.Padding(20, 20, 20, 20),
        width=300,
        shadow=_shadow(14, 4, "12"),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    spacing=16,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text(p, size=18, weight=ft.FontWeight.W_600, color=DARK, width=110) for p in par]
                )
                for fila in palabras_grupo1
                for par in (fila[:2], fila[2:])
            ],
        ),
    )

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            palabras_container,
            ft.Text("🐝", size=64),
            timer_text,
            btn_comenzar,
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


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 – Now it's your turn! (Second reading)
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_3(on_next, on_prev, page, on_tiempo=None):
    palabras_grupo2 = [
        ["friend", "dog", "boat", "hand"],
        ["child", "school", "beach", "rain"],
        ["bird", "star", "village", "stone"],
        ["road", "mountain", "river", "fire"],
    ]

    tiempo_inicio = [None]
    tiempo_transcurrido = [0]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Read the next group of words as fast as possible.",
        siguiente_visible=False,
    )

    timer_activo = [False]
    tarea_timer = [None]

    btn_comenzar = ft.Button(
        content=ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700),
        bgcolor=GREEN,
        on_click=lambda e: iniciar_lectura_2(e, page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22),
            padding=ft.Padding(left=32, right=32, top=12, bottom=12),
        ),
    )

    timer_text = ft.Text("", size=20, weight=ft.FontWeight.W_700, color=GREEN)

    def iniciar_lectura_2(e, page):
        if timer_activo[0]:
            timer_activo[0] = False
            if tarea_timer[0] is not None:
                tarea_timer[0].cancel()
            tarea_timer[0] = None
            btn_continuar.visible = True
            timer_text.value = f"✅ Final time: {tiempo_transcurrido[0]} seconds"
            timer_text.color = GREEN
            btn_comenzar.content = ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
            btn_comenzar.bgcolor = GREEN
            if on_tiempo is not None:
                on_tiempo(tiempo_transcurrido[0])
            page.update()
            return

        timer_activo[0] = True
        tiempo_inicio[0] = time.time()
        tiempo_transcurrido[0] = 0
        btn_comenzar.content = ft.Text("Stop ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
        btn_comenzar.bgcolor = RED
        timer_text.value = "⏱️ Time: 0 seconds"
        timer_text.color = GREEN

        async def update_timer():
            while timer_activo[0]:
                await asyncio.sleep(1)
                if not timer_activo[0]:
                    break
                tiempo_transcurrido[0] = int(time.time() - tiempo_inicio[0])
                timer_text.value = f"⏱️ Time: {tiempo_transcurrido[0]} seconds"
                page.update()

        tarea_timer[0] = asyncio.create_task(update_timer())
        page.update()

    panel = panel_instrucciones(
        titulo="Now it's your turn!",
        subtitulo="Read the next group of words as fast as possible.",
        mascota_texto="You've warmed up. Now try to go even faster!",
    )

    palabras_container = ft.Container(
        bgcolor=WHITE,
        border_radius=24,
        padding=ft.Padding(20, 20, 20, 20),
        width=300,
        shadow=_shadow(14, 4, "12"),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    spacing=16,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text(p, size=18, weight=ft.FontWeight.W_600, color=DARK, width=110) for p in par]
                )
                for fila in palabras_grupo2
                for par in (fila[:2], fila[2:])
            ],
        ),
    )

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            palabras_container,
            ft.Text("🐝", size=64),
            timer_text,
            btn_comenzar,
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


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 – How fast did you read? (Results)
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_4(on_next, on_prev, ultimo_tiempo=0, mejor_tiempo=0):
    barra, _ = barra_inferior(
        on_prev, on_next,
        hint_texto="Check your time and beat your record.",
    )

    panel = panel_instrucciones(
        titulo="How fast did you read?",
        subtitulo="Check your time and beat your record in the next round.",
        mascota_texto="Keep practicing! You can improve every day.",
    )

    tarjeta_resultados = ft.Container(
        bgcolor=WHITE,
        border_radius=30,
        padding=ft.Padding(24, 22, 24, 22),
        width=300,
        shadow=_shadow(18, 6, "14"),
        content=ft.Column(
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=6,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.ACCESS_TIME, color=BLUE, size=24),
                                ft.Text("Your time", size=15, color=GRAY_TEXT),
                            ],
                        ),
                        ft.Text(str(ultimo_tiempo), size=44, weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text("seconds", size=14, color=GRAY_TEXT),
                    ],
                ),
                ft.Container(height=1, bgcolor=CARD_BORDER_IDLE, width=200),
                ft.Column(
                    spacing=6,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.EMOJI_EVENTS, color=AMBER, size=24),
                                ft.Text("Your best score", size=15, color=GRAY_TEXT),
                            ],
                        ),
                        ft.Text(str(mejor_tiempo), size=44, weight=ft.FontWeight.W_900, color=AMBER),
                        ft.Text("seconds", size=14, color=GRAY_TEXT),
                    ],
                ),
            ],
        ),
    )

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=24,
        controls=[
            tarjeta_resultados,
            ft.Container(
                bgcolor=WHITE, border_radius=18,
                padding=ft.Padding(10, 16, 10, 16),
                shadow=_shadow(10, 3, "10"),
                content=ft.Text(
                    "Keep practicing! You can improve every day.",
                    size=17, color=PURPLE, text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.W_600,
                ),
            ),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=16,
                  controls=[ft.Text("🚀", size=68), ft.Text("🐝", size=64)]),
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


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 5 – Faster (Text reading)
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_5(on_next, on_prev, page, on_tiempo=None):
    texto = ("Dixi loves learning new things every day. She reads stories, discovers new "
             "places, and dreams of grand adventures. Reading gives wings to her "
             "imagination and lets her fly far, far away.")

    tiempo_inicio = [None]
    tiempo_transcurrido = [0]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Read this text as fast as you can. Don't go back.",
        siguiente_visible=False,
    )

    timer_activo = [False]
    tarea_timer = [None]

    btn_comenzar = ft.Button(
        content=ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700),
        bgcolor=PURPLE,
        on_click=lambda e: iniciar_lectura_texto(e, page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22),
            padding=ft.Padding(left=32, right=32, top=12, bottom=12),
        ),
    )

    timer_text = ft.Text("", size=18, weight=ft.FontWeight.W_700, color=PURPLE)

    def iniciar_lectura_texto(e, page):
        if timer_activo[0]:
            timer_activo[0] = False
            if tarea_timer[0] is not None:
                tarea_timer[0].cancel()
            tarea_timer[0] = None
            btn_continuar.visible = True
            timer_text.value = f"✅ Final time: {tiempo_transcurrido[0]} seconds"
            timer_text.color = GREEN
            btn_comenzar.content = ft.Text("Start ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
            btn_comenzar.bgcolor = PURPLE
            if on_tiempo is not None:
                on_tiempo(tiempo_transcurrido[0])
            page.update()
            return

        timer_activo[0] = True
        tiempo_inicio[0] = time.time()
        tiempo_transcurrido[0] = 0
        btn_comenzar.content = ft.Text("Stop ⏱️", color=WHITE, size=15, weight=ft.FontWeight.W_700)
        btn_comenzar.bgcolor = RED
        timer_text.value = "⏱️ Time: 0 seconds"
        timer_text.color = PURPLE

        async def update_timer():
            while timer_activo[0]:
                await asyncio.sleep(1)
                if not timer_activo[0]:
                    break
                tiempo_transcurrido[0] = int(time.time() - tiempo_inicio[0])
                timer_text.value = f"⏱️ Time: {tiempo_transcurrido[0]} seconds"
                page.update()

        tarea_timer[0] = asyncio.create_task(update_timer())
        page.update()

    panel = panel_instrucciones(
        titulo="Faster",
        subtitulo="Read this text as fast as you can. Focus and don't stop!",
        mascota_texto="Don't go back. Keep reading without stopping.",
    )

    texto_container = ft.Container(
        bgcolor=WHITE,
        border_radius=28,
        padding=ft.Padding(20, 20, 20, 20),
        width=300,
        shadow=_shadow(16, 5, "14"),
        content=ft.Text(
            texto,
            size=16, color=DARK,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500,
            style=ft.TextStyle(height=1.4),
        ),
    )

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            texto_container,
            timer_text,
            ft.Text("🐝", size=60),
            btn_comenzar,
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
    return fondo_pantalla(GRAD_LILAC, contenido)


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 6 – Choose your level
# ══════════════════════════════════════════════════════════════════════════════
def build_paso_6(on_next, on_prev):
    barra, btn_continuar = barra_inferior(
        on_prev, on_next,
        hint_texto="Each level is faster. Pick one and challenge yourself!",
        siguiente_visible=False,
    )

    panel = panel_instrucciones(
        titulo="Choose your level",
        subtitulo="Each level is faster. You'll beat your record with practice and focus.",
        mascota_texto="Choose the level that challenges you most today.",
    )

    niveles = [
        ("Easy", "🌱", "60 sec", "🐌"),
        ("Medium", "⚡", "45 sec", "🐝"),
        ("Hard", "🚀", "30 sec", "🔥"),
    ]
    cards = {}

    def seleccionar_nivel(nombre):
        def handler(e):
            for n, c in cards.items():
                c.border = ft.Border.all(3, PURPLE) if n == nombre else ft.Border.all(2, CARD_BORDER_IDLE)
                c.bgcolor = LIGHT_PURPLE if n == nombre else WHITE
            btn_continuar.visible = True
            e.page.update()
        return handler

    cards_row = []
    for nombre, emoji, tiempo, emoji2 in niveles:
        card = ft.Container(
            width=96, height=140, border_radius=20,
            bgcolor=WHITE, border=ft.Border.all(2, CARD_BORDER_IDLE),
            ink=True, animate=_anim(180),
            shadow=_shadow(12, 4, "10"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Text(emoji, size=30),
                    ft.Text(nombre, size=15, weight=ft.FontWeight.W_700, color=DARK),
                    ft.Text(tiempo, size=13, color=GRAY_TEXT),
                    ft.Text(emoji2, size=22),
                ],
            ),
        )
        card.on_click = seleccionar_nivel(nombre)
        cards[nombre] = card
        cards_row.append(card)

    area = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=26,
        controls=[
            ft.Row(spacing=12, run_spacing=12, wrap=True, alignment=ft.MainAxisAlignment.CENTER, controls=cards_row),
            ft.Container(
                bgcolor=WHITE, border_radius=18,
                padding=ft.Padding(10, 14, 10, 14),
                shadow=_shadow(10, 3, "10"),
                content=ft.Row(
                    spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.EMOJI_EVENTS, color=AMBER, size=26),
                        ft.Text("You'll beat your record with practice and focus.", size=15, color=DARK),
                    ],
                ),
            ),
            ft.Text("🐝", size=64),
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
    return fondo_pantalla(GRAD_ROSE, contenido)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_velocidad_lectora(
    page: ft.Page,
    usuario: str = "",
    on_lecciones=None,
    on_inicio=None,
):
    paso_actual = [0]
    puntos_state = {"val": prog.obtener_progreso(usuario).get("puntos", 0)}

    barra = ft.Container()
    contenido = ft.Container(expand=True)

    def on_prev_generico(e=None):
        ir_a_paso(max(0, paso_actual[0] - 1))

    resultado_tiempos = {"ultimo": 0, "record": 0}

    def registrar_tiempo(segundos):
        if segundos <= 0:
            return
        resultado_tiempos["ultimo"] = segundos
        if resultado_tiempos["record"] == 0 or segundos < resultado_tiempos["record"]:
            resultado_tiempos["record"] = segundos

    def ir_a_paso(n):
        paso_actual[0] = n
        puntos_state["val"] = prog.obtener_progreso(usuario).get("puntos", 0)
        if n >= TOTAL_PASOS:
            barra.visible = False
            contenido.content = build_celebracion(
                on_repasar=lambda e: ir_a_paso(0),
                on_continuar=lambda e: (on_lecciones(e) if on_lecciones else None),
                usuario=usuario,
                nivel=NIVEL, num=2,
                titulo='Reading Speed',
            )
        else:
            barra.visible = True
            barra.content = build_top_bar_rico(
                n, TOTAL_PASOS, puntos_state["val"],
                on_home=on_lecciones,
                on_settings=lambda e: (on_inicio(e) if on_inicio else None),
            )
            on_next = lambda e: ir_a_paso(paso_actual[0] + 1)
            builders = [
                lambda: build_paso_1(on_next, on_prev_generico),
                lambda: build_paso_2(on_next, on_prev_generico, page, registrar_tiempo),
                lambda: build_paso_3(on_next, on_prev_generico, page, registrar_tiempo),
                lambda: build_paso_4(on_next, on_prev_generico, resultado_tiempos["ultimo"], resultado_tiempos["record"]),
                lambda: build_paso_5(on_next, on_prev_generico, page, registrar_tiempo),
                lambda: build_paso_6(on_next, on_prev_generico),
            ]
            contenido.content = builders[n]()
        page.update()

    barra.content = build_top_bar_rico(
        0, TOTAL_PASOS, puntos_state["val"],
        on_home=on_lecciones,
        on_settings=lambda e: (on_inicio(e) if on_inicio else None),
    )
    contenido.content = build_paso_1(
        lambda e: ir_a_paso(1),
        on_prev_generico,
    )

    return ft.Column(
        expand=True, spacing=0,
        controls=[barra, contenido],
    )
