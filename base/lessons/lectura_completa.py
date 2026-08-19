"""Lesson - Complete Reading: Mateo and the Library - Level 4, Lesson 2

Redesigned in horizontal PC format (same visual pattern as
reconoce_letras.py): instruction panel fixed to the left + interactive
area on the right that uses the full width of the screen, image
background with floating decorations, Dixi mascot integrated into the
panel, animated option cards, result banner and tip pill.
Same public API as the original file (build_lectura_completa,
build_paso_1..6).
"""

import random
import sys
from pathlib import Path

import flet as ft
from components.celebration import build_celebracion

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Color palette ───────────────────────────────────────────────────────
PURPLE       = "#7B61FF"
LIGHT_PURPLE = "#EDE7FF"
AMBER        = "#F5A623"
WHITE        = "#FFFFFF"
DARK         = "#1A1A2E"
GREEN        = "#4CAF50"
RED          = "#E53935"
BLUE         = "#2196F3"
GRAY_TEXT    = "#888888"

ERROR_RED       = "#E5484D"
SUCCESS_BG      = "#EEFBF1"
SUCCESS_BORDER  = "#C3ECCB"
ERROR_BG        = "#FDEEEE"
ERROR_BORDER    = "#F3C7C7"
CARD_BORDER_IDLE = "#EFECF9"

CENTER = ft.Alignment(0, 0)
_GRAD_TOP = ft.Alignment(0, -1)
_GRAD_BOTTOM = ft.Alignment(0, 1)

SIDE_PANEL_WIDTH = 320
NIVEL = 4
TOTAL_PASOS = 6

FONDOS_IMAGENES = [
    "imagenes/fondo1.png",
    "imagenes/fondo2.png",
    "imagenes/fondo3.png",
]


def _anim(ms=180, curva="easeOut"):
    return ft.Animation(ms, curva)


def _shadow(blur=10, dy=3, alpha="0F"):
    return ft.BoxShadow(blur_radius=blur, color=f"#{alpha}000000", offset=ft.Offset(0, dy))


# ===================================================
#  GRADIENT BACKGROUNDS (preserved for compatibility)
# ===================================================
GRAD_PURPLE = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2EEFF", "#E1D6FF"])
GRAD_PEACH  = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFBEF", "#FFF1D2"])
GRAD_PINK   = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFF3F5", "#FFDEE6"])
GRAD_GREEN  = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#F2FFF5", "#DBFAE3"])
GRAD_BLUE   = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#EFF7FF", "#D7ECFF"])
GRAD_YELLOW = ft.LinearGradient(begin=_GRAD_TOP, end=_GRAD_BOTTOM, colors=["#FFFDF2", "#FFF4CE"])


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
                width=tamano, height=tamano * 1.08,
                controls=[
                    ft.Container(top=tamano * 0.14, content=ft.Text("🦉", size=tamano)),
                    ft.Container(left=tamano * 0.30, top=0,
                                 content=ft.Text("🎓", size=tamano * 0.34, rotate=ft.Rotate(-0.18))),
                ],
            ),
            ft.Container(
                width=ancho_globo, bgcolor=WHITE, border_radius=16,
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                shadow=_shadow(14, 5, "18"),
                content=ft.Column(
                    spacing=4, tight=True,
                    controls=[
                        ft.Row(spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                            ft.Container(width=20, height=20, border_radius=10, bgcolor=LIGHT_PURPLE,
                                         alignment=CENTER, content=ft.Text("💜", size=10)),
                            ft.Text("You can do it!", size=12, weight=ft.FontWeight.W_800, color=PURPLE),
                        ]),
                        ft.Text(mensaje, size=12, color=DARK, style=ft.TextStyle(height=1.3)),
                    ],
                ),
            ),
        ],
    )


def fondo_pantalla(gradiente, contenido_centro, mascota_texto=None):
    capas = [
        *fondo_decorativo(),
        ft.Container(expand=True, padding=ft.Padding(left=14, right=14, top=14, bottom=0), content=contenido_centro),
    ]
    if mascota_texto:
        capas.append(ft.Container(left=20, bottom=92, content=dixi_mascota(mascota_texto)))
    return ft.Container(
        expand=True,
        image=ft.DecorationImage(src=random.choice(FONDOS_IMAGENES), fit=ft.BoxFit.COVER),
        content=ft.Stack(expand=True, controls=capas),
    )


# ===================================================
#  TOP BAR (level + progress + %)
# ===================================================
def top_progress_bar(paso, total, on_home, on_settings=None):
    dot_row = []
    for i in range(total):
        filled = i <= paso
        size = 16 if filled else 12
        dot_row.append(ft.Container(width=size, height=size, border_radius=size // 2,
                                     bgcolor=PURPLE if filled else "#D9D9D9", animate=_anim(220)))
        if i < total - 1:
            dot_row.append(ft.Container(width=14, height=4, border_radius=2,
                                         bgcolor=PURPLE if i < paso else "#D9D9D9", animate=_anim(220)))
    porcentaje = int(round((paso / total) * 100)) if total else 0
    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=12, right=12, top=8, bottom=8),
        shadow=_shadow(12, 3, "14"),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(icon=ft.Icons.HOME_ROUNDED, icon_color=PURPLE, icon_size=26, on_click=on_home),
                ft.Row(spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Row(spacing=0, controls=dot_row),
                ]),
                ft.Row(spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Column(spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                        ft.Text(f"{porcentaje}%", size=16, weight=ft.FontWeight.W_800, color=PURPLE),
                        ft.Text("completed", size=12, color=GRAY_TEXT),
                    ]),
                    ft.IconButton(icon=ft.Icons.SETTINGS_ROUNDED, icon_color=PURPLE, icon_size=24, on_click=on_settings),
                ]),
            ],
        ),
    )


# ===================================================
#  HINT, RESULT BANNER AND CARDS
# ===================================================
def hint_pill(texto):
    return ft.Container(
        bgcolor=WHITE, border_radius=22,
        padding=ft.Padding(left=14, right=22, top=6, bottom=6),
        shadow=_shadow(10, 3, "12"),
        content=ft.Row(spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Container(width=34, height=34, border_radius=17, bgcolor=LIGHT_PURPLE, alignment=CENTER,
                         content=ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=AMBER, size=18)),
            ft.Column(spacing=0, tight=True, width=220, controls=[
                ft.Text("Tip", size=12, weight=ft.FontWeight.W_800, color=PURPLE),
                ft.Text(texto, size=14, color=GRAY_TEXT, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ]),
        ]),
    )


def crear_banner_resultado():
    icono = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=GREEN, size=22)
    texto = ft.Text("", size=15, weight=ft.FontWeight.W_700, color=GREEN)
    banner = ft.Container(
        visible=False, bgcolor=SUCCESS_BG, border=ft.Border.all(1.5, SUCCESS_BORDER), border_radius=16,
        padding=ft.Padding(left=20, right=22, top=12, bottom=12), animate_opacity=_anim(200),
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


def marcar_tarjeta(card, estado):
    if estado is None:
        card.bgcolor = WHITE
        card.border = ft.Border.all(2, CARD_BORDER_IDLE)
    elif estado is True:
        card.bgcolor = SUCCESS_BG
        card.border = ft.Border.all(3, GREEN)
    else:
        card.bgcolor = ERROR_BG
        card.border = ft.Border.all(3, ERROR_RED)


def _tarjeta_opcion(texto, width=440, height=68, size_texto=17, on_click=None):
    return ft.Container(
        width=width, height=height, border_radius=18, bgcolor=WHITE,
        border=ft.Border.all(2, CARD_BORDER_IDLE), ink=True, animate=_anim(180),
        shadow=_shadow(10, 3, "10"), on_click=on_click,
        padding=ft.Padding(left=20, right=20, top=0, bottom=0),
        content=ft.Row(vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Text(texto, size=size_texto, weight=ft.FontWeight.W_600, color=DARK),
        ]),
    )


def _tarjeta_emoji(texto, emoji, width=190, height=170, on_click=None):
    return ft.Container(
        width=width, height=height, border_radius=18, bgcolor=WHITE,
        border=ft.Border.all(2, CARD_BORDER_IDLE), ink=True, animate=_anim(180),
        shadow=_shadow(10, 3, "10"), on_click=on_click,
        padding=ft.Padding(left=14, right=14, top=16, bottom=16),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10,
            controls=[
                ft.Text(emoji, size=44),
                ft.Text(texto, size=14, weight=ft.FontWeight.W_600, color=DARK, text_align=ft.TextAlign.CENTER),
            ],
        ),
    )


def barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=True,
                    texto_siguiente="Next", siguiente_visible=True):
    atras_btn = ft.Button(
        content=ft.Row(spacing=8, controls=[
            ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, color=PURPLE, size=18),
            ft.Text("Back", color=PURPLE, size=16, weight=ft.FontWeight.W_700),
        ]),
        bgcolor=WHITE, on_click=on_prev, visible=mostrar_atras,
        style=ft.ButtonStyle(side=ft.BorderSide(2, "#EDEAFB"), shape=ft.RoundedRectangleBorder(radius=28),
                              elevation=0, padding=ft.Padding(left=26, right=26, top=10, bottom=10)),
    )
    siguiente_btn = ft.Button(
        content=ft.Row(spacing=8, controls=[
            ft.Text(texto_siguiente, color=WHITE, size=16, weight=ft.FontWeight.W_700),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=WHITE, size=18),
        ]),
        bgcolor=PURPLE, on_click=on_next, visible=siguiente_visible,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=28), elevation=2,
                              padding=ft.Padding(left=32, right=32, top=10, bottom=10)),
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
        bgcolor=WHITE, border_radius=24,
        padding=ft.Padding(left=26, right=26, top=30, bottom=26), shadow=_shadow(18, 6, "12"),
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
#  STEP 1 -- Hi! I'm Dixi
# ===================================================
def build_paso_1(on_next, on_prev=None):
    barra, _ = barra_inferior(on_prev, on_next, hint_texto=None, mostrar_atras=False, texto_siguiente="Let's start!")

    panel = panel_instrucciones(
        titulo="Hi! I'm Dixi",
        subtitulo="We're going to complete a reading from start to finish. Read carefully, understand, and answer like a great reader.",
        mascota_texto="Complete reading helps you understand better and remember what you read.",
    )

    area = ft.Container(
        width=460,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=26,
            controls=[
                ft.Text("🐝", size=140),
                ft.Container(
                    width=380, bgcolor=WHITE, border_radius=24,
                    padding=ft.Padding(left=26, right=26, top=22, bottom=22),
                    shadow=_shadow(18, 6, "16"),
                    content=ft.Text(
                        "Complete reading helps you understand better and remember what you read.",
                        size=19, color=PURPLE, weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER, style=ft.TextStyle(height=1.4),
                    ),
                ),
            ],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_PURPLE, contenido)


# ===================================================
#  STEP 2 -- Read the text
# ===================================================
def build_paso_2(on_next, on_prev=None):
    barra, _ = barra_inferior(on_prev, on_next, hint_texto="Read calmly, paying attention to every detail of the story.", texto_siguiente="Continue")

    panel = panel_instrucciones(
        titulo="Read the text",
        subtitulo="Read the following text carefully. You'll need it for the next questions.",
        mascota_texto="Pay attention to why Mateo enjoys reading so much.",
    )

    area = ft.Container(
        width=560,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=30, padding=ft.Padding(left=28, right=28, top=24, bottom=24),
                    shadow=_shadow(18, 6, "14"),
                    content=ft.Column(
                        spacing=16,
                        controls=[
                            ft.Container(
                                bgcolor="#E3F2FD", border_radius=18, padding=ft.Padding(left=18, right=18, top=16, bottom=16),
                                content=ft.Text(
                                    "🌳 On weekends, Mateo visits his neighborhood library. There he looks for "
                                    "adventure and mystery books. He likes to sit by the window and read in "
                                    "silence. Every story takes him to new places and teaches him something "
                                    "different. Mateo knows that reading every day helps him imagine more and "
                                    "learn without even realizing it.",
                                    size=17, color=DARK, style=ft.TextStyle(height=1.5), weight=ft.FontWeight.W_500,
                                ),
                            ),
                            ft.Row(
                                spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME, color=AMBER, size=24),
                                    ft.Text("Estimated time: 3 minutes", size=15, color=GRAY_TEXT),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Text("🐝", size=64),
            ],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_YELLOW, contenido)


# ===================================================
#  STEP 3 -- Comprehend
# ===================================================
def build_paso_3(on_next, on_prev=None):
    preguntas = [
        {
            "titulo": "1. Where does Mateo go on weekends?",
            "opciones": [
                {"texto": "a) To the park", "correcto": False},
                {"texto": "b) To the movies", "correcto": False},
                {"texto": "c) To the library", "correcto": True},
            ],
        },
        {
            "titulo": "2. What kind of books does Mateo like to read?",
            "opciones": [
                {"texto": "a) Cooking books", "correcto": False},
                {"texto": "b) Adventure and mystery books", "correcto": True},
                {"texto": "c) Sports books", "correcto": False},
            ],
        },
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next, hint_texto="Answer both questions using what you read about Mateo.",
        siguiente_visible=False,
    )
    respuestas = [None, None]
    feedback = ft.Text("", size=15, weight=ft.FontWeight.W_700)

    panel = panel_instrucciones(
        titulo="Comprehend",
        subtitulo="Answer the questions based on the text you read.",
        mascota_texto="Think again about the library and the books Mateo likes.",
    )

    def on_seleccionar(preg_idx, op_idx, es_correcto, cards_preg, page_ref):
        respuestas[preg_idx] = op_idx
        for i, card in enumerate(cards_preg):
            marcar_tarjeta(card, es_correcto if i == op_idx else None)
        if all(r is not None for r in respuestas):
            correctas = sum(1 for i, r in enumerate(respuestas) if preguntas[i]["opciones"][r]["correcto"])
            if correctas == 2:
                feedback.value = "Correct! You got everything right 🎉"
                feedback.color = GREEN
                btn_continuar.visible = True
            else:
                feedback.value = f"You have {correctas}/2 correct. Check your answers."
                feedback.color = AMBER
        page_ref.update()

    bloques_preguntas = []
    for q_idx, preg in enumerate(preguntas):
        cards_preg = []
        for o_idx, op in enumerate(preg["opciones"]):
            card = _tarjeta_opcion(op["texto"], width=440, height=58, size_texto=15)
            cards_preg.append(card)
        for o_idx, op in enumerate(preg["opciones"]):
            cards_preg[o_idx].on_click = lambda e, qi=q_idx, oi=o_idx, ec=op["correcto"], cp=cards_preg: on_seleccionar(qi, oi, ec, cp, e.page)
        bloques_preguntas.append(
            ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.START, controls=[
                ft.Text(preg["titulo"], size=16, weight=ft.FontWeight.W_700, color=DARK),
                *cards_preg,
            ])
        )

    area = ft.Container(
        width=520,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=22,
            controls=[*bloques_preguntas, feedback],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_GREEN, contenido)


# ===================================================
#  STEP 4 -- Analyze and reflect
# ===================================================
def build_paso_4(on_next, on_prev=None):
    opciones = [
        {"texto": "Mateo collects old and expensive books.", "emoji": "📚", "correcto": False},
        {"texto": "Mateo enjoys reading at the library and learns every day.", "emoji": "💡", "correcto": True},
        {"texto": "Mateo prefers playing video games at home.", "emoji": "🎮", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next, hint_texto="Think about the idea that best sums up Mateo and his weekends.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Analyze and reflect",
        subtitulo="Select the main idea of the text you read about Mateo.",
        mascota_texto="Look for the option that best summarizes the whole story.",
    )

    tarjetas = []

    def on_elegir(idx_elegido, idx_correcto):
        def handler(e):
            for i, card in enumerate(tarjetas):
                if i == idx_correcto:
                    marcar_tarjeta(card, True)
                elif i == idx_elegido:
                    marcar_tarjeta(card, False)
                else:
                    marcar_tarjeta(card, None)
            if idx_elegido == idx_correcto:
                mostrar_resultado(banner, banner_icono, banner_texto, "Correct! Mateo enjoys reading and learning 💡", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    correct_idx = next(i for i, o in enumerate(opciones) if o["correcto"])
    for i, op in enumerate(opciones):
        card = _tarjeta_emoji(op["texto"], op["emoji"])
        card.on_click = on_elegir(i, correct_idx)
        tarjetas.append(card)

    area = ft.Container(
        width=600,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
            controls=[
                ft.Row(spacing=18, alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=tarjetas),
                banner,
            ],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_BLUE, contenido)


# ===================================================
#  STEP 5 -- Vocabulary in context
# ===================================================
def build_paso_5(on_next, on_prev=None):
    opciones = [
        {"texto": "carries", "correcto": True},
        {"texto": "forgets", "correcto": False},
        {"texto": "changes", "correcto": False},
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next, hint_texto="Think about what 'takes' means when moving someone from one place to another.",
        siguiente_visible=False,
    )
    banner, banner_icono, banner_texto = crear_banner_resultado()

    panel = panel_instrucciones(
        titulo="Vocabulary in context",
        subtitulo="Select the meaning of the underlined word in the sentence.",
        mascota_texto="Understanding words helps you better comprehend what you read.",
    )

    tarjetas = []

    def on_elegir(idx_elegido, idx_correcto):
        def handler(e):
            for i, card in enumerate(tarjetas):
                if i == idx_correcto:
                    marcar_tarjeta(card, True)
                elif i == idx_elegido:
                    marcar_tarjeta(card, False)
                else:
                    marcar_tarjeta(card, None)
            if idx_elegido == idx_correcto:
                mostrar_resultado(banner, banner_icono, banner_texto, "Great job! Understanding words helps you comprehend better 🎉", ok=True)
                btn_continuar.visible = True
            else:
                mostrar_resultado(banner, banner_icono, banner_texto, "Try again 🙂", ok=False)
            e.page.update()
        return handler

    correct_idx = next(i for i, o in enumerate(opciones) if o["correcto"])
    for i, op in enumerate(opciones):
        card = _tarjeta_opcion(f"{chr(97 + i)}) {op['texto']}", width=420, height=60, size_texto=17)
        card.on_click = on_elegir(i, correct_idx)
        tarjetas.append(card)

    area = ft.Container(
        width=520,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=18,
            controls=[
                ft.Container(
                    bgcolor=WHITE, border_radius=24, padding=ft.Padding(left=20, right=20, top=16, bottom=16),
                    width=460, shadow=_shadow(12, 4, "12"),
                    content=ft.Text(
                        "Every story takes him to new places.",
                        size=19, color=DARK, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_600,
                    ),
                ),
                ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=tarjetas),
                banner,
            ],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_PURPLE, contenido)


# ===================================================
#  STEP 6 -- Order the sequence
# ===================================================
def build_paso_6(on_next, on_prev=None):
    eventos = [
        "Mateo goes to the library.",
        "He looks for adventure and mystery books.",
        "He reads by the window in silence.",
        "Every story takes him to new places.",
        "He learns and grows his imagination.",
    ]

    barra, btn_continuar = barra_inferior(
        on_prev, on_next, hint_texto="Put the events in order as they happen in Mateo's story.",
        siguiente_visible=False,
    )
    feedback = ft.Text("", size=15, weight=ft.FontWeight.W_700)

    panel = panel_instrucciones(
        titulo="Order the sequence",
        subtitulo="Order the events as they occur in the text, from first to last.",
        mascota_texto="Mentally review everything Mateo does at the library.",
    )

    dropdowns = []
    for i in range(5):
        dd = ft.Dropdown(
            width=420, height=58, border_radius=16, bgcolor=WHITE, border_color="#DDDDDD",
            text_size=13, hint_text=f"Event {i + 1}",
            options=[ft.dropdown.Option(o) for o in eventos],
        )
        dropdowns.append(dd)

    def on_comprobar(e):
        seleccionadas = [dd.value for dd in dropdowns]
        if None in seleccionadas or "" in seleccionadas:
            feedback.value = "Select all 5 events 🙂"
            feedback.color = RED
        elif seleccionadas == eventos:
            feedback.value = "Perfect order! 🎉"
            feedback.color = GREEN
            btn_continuar.visible = True
        else:
            feedback.value = "That's not the correct order. Try again 🙂"
            feedback.color = RED
        e.page.update()

    filas = []
    for i in range(5):
        filas.append(ft.Row(
            alignment=ft.MainAxisAlignment.CENTER, spacing=13,
            controls=[
                ft.Container(width=38, height=38, border_radius=19, bgcolor=PURPLE, alignment=CENTER,
                             content=ft.Text(str(i + 1), size=17, weight=ft.FontWeight.W_900, color=WHITE)),
                dropdowns[i],
            ],
        ))

    area = ft.Container(
        width=540,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14,
            controls=[
                *filas,
                ft.Container(height=6),
                ft.Button(
                    content=ft.Text("Check", color=WHITE, size=16, weight=ft.FontWeight.W_700),
                    bgcolor=AMBER, on_click=on_comprobar,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=24),
                                         padding=ft.Padding(left=44, right=44, top=16, bottom=16)),
                ),
                feedback,
            ],
        ),
    )

    contenido = ft.Column(expand=True, spacing=0, controls=[ft.Container(height=10), fila_principal(panel, area), barra])
    return fondo_pantalla(GRAD_PINK, contenido)


# ===================================================
#  MAIN CONTROLLER
# ===================================================
def build_lectura_completa(
    page: ft.Page,
    usuario: str = "",
    on_lecciones=None,
    on_inicio=None,
):
    paso_actual = {"idx": 0}

    def get_paso_widget(idx):
        builders = [build_paso_1, build_paso_2, build_paso_3, build_paso_4, build_paso_5, build_paso_6]
        if idx < len(builders):
            return builders[idx](on_next, on_prev)
        return build_celebracion(
            on_repasar=lambda e: go_to(0),
            on_continuar=lambda e: (on_lecciones(e) if on_lecciones else None),
            usuario=usuario, nivel=4, num=2,
            titulo="Final Challenge",
        )

    def on_next(e=None):
        go_to(paso_actual["idx"] + 1)

    def on_prev(e=None):
        go_to(max(0, paso_actual["idx"] - 1))

    def on_settings(e=None):
        if on_inicio:
            on_inicio(e)

    def go_to(idx):
        paso_actual["idx"] = idx
        barra_wrapper.visible = idx < TOTAL_PASOS
        if idx < TOTAL_PASOS:
            barra_wrapper.content = top_progress_bar(idx, TOTAL_PASOS, on_home=on_lecciones, on_settings=on_settings)
        contenido_wrapper.content = get_paso_widget(idx)
        page.update()

    barra_wrapper = ft.Container(content=top_progress_bar(0, TOTAL_PASOS, on_home=on_lecciones, on_settings=on_settings))
    contenido_wrapper = ft.Container(expand=True, content=get_paso_widget(0))

    return ft.Column(expand=True, spacing=0, controls=[barra_wrapper, contenido_wrapper])
