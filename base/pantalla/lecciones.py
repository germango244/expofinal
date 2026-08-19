"""Lessons Screen — Levels with lessons."""

import flet as ft
from pantalla import progreso as prog
from pantalla.db import obtener_usuario
from pantalla.responsive import is_mobile, content_padding, mobile_bottom_nav

# ── Colores ──
PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
BG        = "#FDFAF3"
GRAY_TEXT = "#777777"
DARK      = "#1A1A1A"
NAV_BG    = "#FFFFFF"
NAVY      = "#1A2C5B"
PURPLE    = "#7B61FF"
AMBER     = "#F5A623"
GREEN     = "#2ECC71"
BLUE      = "#1E88E5"

ALIGN_CENTER = ft.Alignment(0, 0)


def avatar_widget(iniciales, foto_b64=None, size=38, text_size=13):
    """Muestra la foto real del usuario (si existe) o sus iniciales como respaldo."""
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(src=foto_b64, width=size, height=size, fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor="#C9B8F0", alignment=ALIGN_CENTER,
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_700),
    )


# ──────────────────────────────────────────────────
#  Componentes compartidos
# ──────────────────────────────────────────────────

def logo_icon():
    return ft.Container(
        width=64, height=64, border_radius=18, bgcolor="#F0E8FF", alignment=ALIGN_CENTER,
        content=ft.Image(
            src="imagenes/logo.png", width=52, height=52, fit="contain",
            error_content=ft.Text("📚", size=24),
        ),
    )



def nav_item_widget(icon, label, active, on_click=None):
    bg    = "#FFF3C4" if active else "transparent"
    color = DARK      if active else GRAY_TEXT
    w     = ft.FontWeight.W_700 if active else ft.FontWeight.W_500
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=color, size=21),
                ft.Text(label, color=color, size=14, weight=w),
            ],
            spacing=13,
        ),
        bgcolor=bg, border_radius=12,
        padding=ft.Padding(left=14, right=14, top=11, bottom=11),
        ink=True, on_click=on_click,
    )


def sidebar_widget(usuario: str, foto_b64=None, on_inicio=None, on_pruebas=None, on_estadisticas=None, on_logros=None, on_configuracion=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,         "Home",        False, on_inicio),
        (ft.Icons.MENU_BOOK_ROUNDED,    "Lessons",     True,  None),
        (ft.Icons.ASSIGNMENT_ROUNDED,   "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,    "Statistics",  False, on_estadisticas),
        (ft.Icons.EMOJI_EVENTS_ROUNDED, "Achievements",        False, on_logros),
        (ft.Icons.SETTINGS_ROUNDED,     "Settings", False, on_configuracion),
    ]
    return ft.Container(
        width=205, bgcolor=NAV_BG,
        shadow=ft.BoxShadow(blur_radius=16, color="#18000000", offset=ft.Offset(2, 0)),
        content=ft.Column(
            spacing=0, expand=True,
            controls=[
                ft.Container(height=20),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
                    controls=[
                        logo_icon(),
                        ft.Text("DixLearn", size=16, weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text("Makes you learn", size=11, color=GRAY_TEXT),
                    ],
                ),
                ft.Container(height=20),
                ft.Column(
                    expand=True, spacing=2,
                    controls=[nav_item_widget(i, l, a, cb) for i, l, a, cb in nav_items],
                ),
                ft.Divider(color="#EEEEEE", height=1),
                ft.Container(
                    padding=ft.Padding(left=12, right=12, top=10, bottom=20),
                    content=ft.Row(
                        controls=[
                            avatar_widget(iniciales, foto_b64, size=38, text_size=13),
                            ft.Column(
                                controls=[
                                    ft.Text(usuario, size=13, weight=ft.FontWeight.W_700, color=DARK),
                                    ft.Text("Student", size=11, color=GRAY_TEXT),
                                ],
                                spacing=0, expand=True,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=18),
                        ],
                        spacing=10,
                    ),
                ),
            ],
        ),
    )


def topbar_widget(usuario: str, on_pruebas=None, on_estadisticas=None, puntos=0, foto_b64=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"

    def nav_btn(icon, label, active=False, on_click=None):
        bg    = AMBER if active else "transparent"
        color = DARK  if active else GRAY_TEXT
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=18),
                    ft.Text(label, color=DARK, size=14, weight=ft.FontWeight.W_700),
                ],
                spacing=8,
            ),
            bgcolor=bg, border_radius=24, ink=True, on_click=on_click,
            padding=ft.Padding(left=18, right=18, top=10, bottom=10),
        )

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=14, bottom=14),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=44, height=44, border_radius=12,
                            bgcolor="#F0E8FF", alignment=ALIGN_CENTER,
                            content=ft.Text("📚", size=20),
                        ),
                        ft.Column(
                            spacing=1,
                            controls=[
                                ft.Text("DixLearn", size=15,
                                        weight=ft.FontWeight.W_900, color=DARK),
                                ft.Text("Learn differently, learn brilliantly.",
                                        size=10, color=GRAY_TEXT),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
                                    ft.Text(f"{puntos} points", size=14,
                                            weight=ft.FontWeight.W_700, color=DARK),
                                ],
                                spacing=6,
                            ),
                            bgcolor=WHITE, border_radius=24,
                            border=ft.Border.all(1, "#EEEEEE"),
                            padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                            shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                                                offset=ft.Offset(0, 2)),
                        ),
                        avatar_widget(iniciales, foto_b64, size=44, text_size=15),
                    ],
                ),
            ],
        ),
    )


# ──────────────────────────────────────────────────
#  Componentes propios de Lessons
# ──────────────────────────────────────────────────

def leccion_card(numero: str, titulo: str, color_nivel: str,
                 completada: bool = False, desbloqueada: bool = True,
                 puntaje=None, on_click=None):
    """Individual lesson card, with desktop layout.

    States:
      - Locked        -> dimmed, with a lock, not clickable.
      - Unlocked      -> ready to do, button "Get started".
      - Completed      -> green check, full bar, score, can be reviewed.
    """
    if completada:
        estado_txt, estado_color, estado_bg = "Completed", GREEN, "#E8F8F0"
        icono_estado = ft.Icons.CHECK_CIRCLE_ROUNDED
        pct = 1.0
        accion_txt = "Review"
    elif desbloqueada:
        estado_txt, estado_color, estado_bg = "Available", color_nivel, "#FFFFFF"
        icono_estado = ft.Icons.PLAY_CIRCLE_ROUNDED
        pct = 0.0
        accion_txt = "Get started"
    else:
        estado_txt, estado_color, estado_bg = "Locked", GRAY_TEXT, "#F2F2F2"
        icono_estado = ft.Icons.LOCK_ROUNDED
        pct = 0.0
        accion_txt = "Locked"

    clickable = desbloqueada and on_click is not None

    icono_num = ft.Container(
        width=42, height=42, border_radius=12,
        bgcolor=(color_nivel if (completada or desbloqueada) else "#DDDDDD"),
        alignment=ALIGN_CENTER,
        content=ft.Text(numero, size=17, weight=ft.FontWeight.W_900, color=WHITE),
    )

    footer = ft.Container(
        border_radius=10,
        bgcolor=estado_bg,
        padding=ft.Padding(left=10, right=10, top=7, bottom=7),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Icon(icono_estado, color=estado_color, size=16),
                ft.Text(accion_txt, size=12, weight=ft.FontWeight.W_800, color=estado_color),
            ],
        ),
    )

    puntaje_row = []
    if completada and puntaje is not None:
        puntaje_row = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER, spacing=4,
                controls=[
                    ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=13),
                    ft.Text(f"{puntaje}%", size=11, color=GRAY_TEXT, weight=ft.FontWeight.W_700),
                ],
            )
        ]

    return ft.Container(
        width=210,
        bgcolor=WHITE,
        border_radius=16,
        padding=ft.Padding(left=16, right=16, top=16, bottom=14),
        border=ft.Border.all(1.5, estado_color if completada or not desbloqueada else "#EEEEEE"),
        shadow=ft.BoxShadow(blur_radius=10, color="#0C000000", offset=ft.Offset(0, 3)),
        opacity=1.0 if desbloqueada else 0.6,
        ink=clickable,
        on_click=on_click if clickable else None,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        icono_num,
                        ft.Icon(
                            ft.Icons.LOCK_ROUNDED if not desbloqueada
                            else (ft.Icons.CHECK_CIRCLE_ROUNDED if completada
                                  else ft.Icons.RADIO_BUTTON_UNCHECKED),
                            color=estado_color if not desbloqueada or completada else "#CCCCCC",
                            size=22,
                        ),
                    ],
                ),
                ft.Text(f"Lesson {numero}", size=11, color=GRAY_TEXT, weight=ft.FontWeight.W_700),
                ft.Text(titulo, size=14.5, weight=ft.FontWeight.W_800, color=DARK,
                        max_lines=2),
                ft.Container(
                    width=178,  # 210 (ancho de la card) - 16*2 (padding izq/der)
                    height=6, border_radius=3, bgcolor="#EEEEEE",
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Container(
                        width=178 * pct, height=6, border_radius=3,
                        bgcolor=GREEN if completada else color_nivel,
                    ),
                ),
                *puntaje_row,
                footer,
            ],
        ),
    )


def footer_hint():
    return ft.Container(
        alignment=ALIGN_CENTER,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.INFO_OUTLINE, color=GRAY_TEXT, size=16),
                ft.Text("Complete lessons in order to unlock new levels.",
                        size=12, color=GRAY_TEXT),
            ],
        ),
    )


# ──────────────────────────────────────────────────
#  Pantalla principal de Lessons (ESTA ES LA FUNCIÓN QUE FALTABA)
# ──────────────────────────────────────────────────

def build_lecciones(page: ft.Page, usuario: str, on_inicio=None,
                    on_pruebas=None, on_estadisticas=None, on_logros=None,
                    on_configuracion=None, on_abrir_leccion=None):
    """Builds the Lessons screen."""

    # ═══════════════════════════════════════════════════════════════
    #  📝 ACÁ CAMBIÁS LOS NOMBRES DE LAS LECCIONES
    # ═══════════════════════════════════════════════════════════════
    
    # NIVEL 1 - 5 LECCIONES
    nivel1_lecciones = [
        "Recognizes letters",              # Lesson 1
        "Simple syllables",         # Lección 2
        "Basic words",        # Lección 3
        "Beginning reading",         # Lección 4
        "Level review",        # Lección 5
    ]
    
    # NIVEL 2 - 3 LECCIONES
    nivel2_lecciones = [
        "Similar words",      # Lesson 1
        "Reading speed",        # Lección 2
        "Advanced comprehension",        # Lección 3
    ]
    
    # NIVEL 3 - 2 LECCIONES
    nivel3_lecciones = [
        "Expert comprehension",       # Lesson 1
        "Fun spelling",    # Lección 2
    ]
    
    # NIVEL 4 - 2 LECCIONES
    nivel4_lecciones = [
        "Attention and focus",          # Lesson 1
        "Final challenge",           # Lección 2
    ]
    
    # ═══════════════════════════════════════════════════════════════

    header_row = ft.Stack(
        height=90,
        controls=[
            ft.Container(
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Lessons", size=34,
                                weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text("Progress through levels and complete all lessons.",
                                size=14, color=GRAY_TEXT),
                    ],
                ),
            ),
            ft.Container(
                alignment=ft.Alignment(1, -1),
                content=ft.Image(src="imagenes/abeja.png", width=90, height=90, fit="contain", error_content=ft.Text("🐝", size=72)),
            ),
        ],
    )

    # ── Progress real del usuario (Mongo) ──
    progreso_usuario = prog.obtener_progreso(usuario)

    usuario_doc = obtener_usuario(usuario) or {}
    foto_b64 = usuario_doc.get("foto")

    COLOR_NIVEL = {1: AMBER, 2: PURPLE, 3: GREEN, 4: BLUE}

    # Función para crear callbacks de lecciones (solo si está desbloqueada)
    def crear_callbacks(nivel, lecciones):
        callbacks = []
        for i, titulo in enumerate(lecciones):
            num = i + 1
            if prog.leccion_desbloqueada(progreso_usuario, nivel, num):
                cb = (lambda e, n=nivel, num=num, t=titulo:
                      on_abrir_leccion(n, num, t) if on_abrir_leccion else None)
            else:
                cb = None
            callbacks.append(cb)
        return callbacks

    # Crear tarjetas de lecciones para cada nivel (en grilla, estilo escritorio)
    def crear_seccion_lecciones(lecciones, nivel_num, color_fondo):
        callbacks = crear_callbacks(nivel_num, lecciones)
        color_nivel = COLOR_NIVEL.get(nivel_num, PRIMARY)
        cards = []
        for i, (t, cb) in enumerate(zip(lecciones, callbacks)):
            num = i + 1
            completada = prog.leccion_completada(progreso_usuario, nivel_num, num)
            desbloqueada = prog.leccion_desbloqueada(progreso_usuario, nivel_num, num)
            puntaje = prog.leccion_puntaje(progreso_usuario, nivel_num, num)
            cards.append(
                leccion_card(str(num), t, color_nivel,
                            completada=completada, desbloqueada=desbloqueada,
                            puntaje=puntaje, on_click=cb)
            )

        # Grilla: máximo 4 tarjetas por fila para verse bien en pantallas de escritorio
        filas = []
        for i in range(0, len(cards), 4):
            grupo = cards[i:i + 4]
            filas.append(ft.Row(spacing=14, controls=grupo, wrap=True))

        return ft.Container(
            bgcolor=color_fondo,
            border_radius=14,
            padding=ft.Padding(left=18, right=18, top=18, bottom=18),
            content=ft.Column(spacing=14, controls=filas),
        )

    def nivel_header(num, color, nombre, subtitulo, desc, lecciones, mobile=False):
        pct = prog.porcentaje_nivel(progreso_usuario, num)
        desbloqueado = prog.leccion_desbloqueada(progreso_usuario, num, 1)
        icono_estado = (ft.Icons.CHECK_CIRCLE_ROUNDED if pct == 100
                        else (ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED if desbloqueado
                              else ft.Icons.LOCK_ROUNDED))
        color_icono = GREEN if pct == 100 else (GRAY_TEXT if not desbloqueado else color)

        left = ft.Row(
            spacing=16,
            controls=[
                ft.Container(
                    width=48, height=48, border_radius=24,
                    bgcolor=color if desbloqueado else "#CCCCCC", alignment=ALIGN_CENTER,
                    content=ft.Text(str(num), size=20,
                                    weight=ft.FontWeight.W_900, color=WHITE),
                ),
                ft.Column(
                    spacing=2,
                    expand=True,
                    controls=[
                        ft.Text(f"Level {num}", size=16,
                                weight=ft.FontWeight.W_900, color=DARK),
                        ft.Text(subtitulo, size=13,
                                weight=ft.FontWeight.W_700, color=DARK),
                        ft.Text(desc, size=12, color=GRAY_TEXT),
                    ],
                ),
            ],
        )

        progress_bar = ft.ProgressBar(
            value=pct / 100,
            height=10,
            border_radius=ft.BorderRadius(5, 5, 5, 5),
            bgcolor="#EEEEEE",
            color=GREEN if pct == 100 else color,
        )

        if mobile:
            # On mobile the progress bar stacks below the level info,
            # using the full card width so it never spills outside.
            progress_row = ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=6,
                        expand=True,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Progress", size=11, color=GRAY_TEXT),
                                    ft.Text(f"{pct}%", size=13,
                                            weight=ft.FontWeight.W_900, color=DARK),
                                ],
                            ),
                            ft.Container(content=progress_bar, expand=True),
                        ],
                    ),
                    ft.Icon(icono_estado, color=color_icono, size=24),
                ],
            )
            return ft.Column(spacing=14, controls=[left, progress_row])

        right = ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Text("Progress", size=11, color=GRAY_TEXT),
                        ft.Text(f"{pct}%", size=14,
                                weight=ft.FontWeight.W_900, color=DARK),
                        ft.Container(width=140, content=progress_bar),
                    ],
                ),
                ft.Icon(icono_estado, color=color_icono, size=24),
            ],
        )
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[left, right],
        )

    mobile = is_mobile(page)

    nivel1_header = nivel_header(1, AMBER, "Level 1", "Fundamentals",
                                 "Learn the basics to start your journey.", nivel1_lecciones, mobile=mobile)
    nivel2_header = nivel_header(2, PURPLE, "Level 2", "Intermediate",
                                 "Improve your reading and comprehension.", nivel2_lecciones, mobile=mobile)
    nivel3_header = nivel_header(3, GREEN, "Level 3", "Advanced",
                                 "Develop more complex skills.", nivel3_lecciones, mobile=mobile)
    nivel4_header = nivel_header(4, BLUE, "Level 4", "Expert",
                                 "Master reading and reach your full potential.", nivel4_lecciones, mobile=mobile)

    main_content = ft.Container(
        expand=True, bgcolor=BG,
        content=ft.Column(
            expand=True, spacing=0,
            controls=[
                topbar_widget(usuario,
                              on_pruebas=on_pruebas,
                              on_estadisticas=on_estadisticas,
                              puntos=progreso_usuario.get("puntos", 0),
                              foto_b64=foto_b64),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        padding=content_padding(page),
                        spacing=16,
                        controls=[
                            header_row,
                            
                            # NIVEL 1 COMPLETO
                            ft.Container(
                                bgcolor=WHITE, border_radius=16,
                                padding=ft.Padding(left=24, right=24, top=20, bottom=20),
                                shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        nivel1_header,
                                        crear_seccion_lecciones(nivel1_lecciones, 1, "#FFF8E7"),
                                    ],
                                ),
                            ),
                            
                            # NIVEL 2 CON 3 LECCIONES
                            ft.Container(
                                bgcolor=WHITE, border_radius=16,
                                padding=ft.Padding(left=24, right=24, top=20, bottom=20),
                                shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        nivel2_header,
                                        crear_seccion_lecciones(nivel2_lecciones, 2, "#F3E5F5"),
                                    ],
                                ),
                            ),
                            
                            # NIVEL 3 CON 2 LECCIONES
                            ft.Container(
                                bgcolor=WHITE, border_radius=16,
                                padding=ft.Padding(left=24, right=24, top=20, bottom=20),
                                shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        nivel3_header,
                                        crear_seccion_lecciones(nivel3_lecciones, 3, "#E8F5E9"),
                                    ],
                                ),
                            ),
                            
                            # NIVEL 4 CON 2 LECCIONES
                            ft.Container(
                                bgcolor=WHITE, border_radius=16,
                                padding=ft.Padding(left=24, right=24, top=20, bottom=20),
                                shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 2)),
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        nivel4_header,
                                        crear_seccion_lecciones(nivel4_lecciones, 4, "#E3F2FD"),
                                    ],
                                ),
                            ),
                            
                            footer_hint(),
                        ],
                    ),
                ),
            ],
        ),
    )

    sidebar = sidebar_widget(usuario, foto_b64, on_inicio=on_inicio, on_pruebas=on_pruebas,
                             on_estadisticas=on_estadisticas, on_logros=on_logros,
                             on_configuracion=on_configuracion)
    sidebar.visible = not mobile

    body = ft.Row(
        expand=True, spacing=0,
        controls=[
            sidebar,
            main_content,
        ],
    )
    if mobile:
        return ft.Column(expand=True, spacing=0, controls=[
            body,
            mobile_bottom_nav("lecciones", on_inicio=on_inicio, on_pruebas=on_pruebas,
                               on_estadisticas=on_estadisticas, on_logros=on_logros,
                               on_configuracion=on_configuracion),
        ])
    return body