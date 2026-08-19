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

CENTER = ft.Alignment(0, 0)


def avatar_widget(iniciales, foto_b64=None, size=38, text_size=13):
    """Muestra la foto real del usuario (si existe) o sus iniciales como respaldo."""
    if foto_b64:
        return ft.Container(
            width=size, height=size, border_radius=size / 2,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(src=foto_b64, width=size, height=size, fit=ft.BoxFit.COVER),
        )
    return ft.Container(
        width=size, height=size, border_radius=size / 2, bgcolor="#C9B8F0", alignment=CENTER,
        content=ft.Text(iniciales, color=WHITE, size=text_size, weight=ft.FontWeight.W_700),
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────

def logo_icon():
    return ft.Container(
        width=64, height=64, border_radius=18, bgcolor="#F0E8FF", alignment=CENTER,
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
        content=ft.Row(controls=[
            ft.Icon(icon, color=color, size=21),
            ft.Text(label, color=color, size=14, weight=w),
        ], spacing=13),
        bgcolor=bg, border_radius=12,
        padding=ft.Padding(left=14, right=14, top=11, bottom=11),
        ink=True, on_click=on_click,
    )


def sidebar_widget(usuario: str, foto_b64=None, on_inicio=None, on_lecciones=None,
                   on_pruebas=None, on_estadisticas=None, on_configuracion=None):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"
    nav_items = [
        (ft.Icons.HOME_ROUNDED,        "Home",        False, on_inicio),
        (ft.Icons.MENU_BOOK_ROUNDED,   "Lessons",     False, on_lecciones),
        (ft.Icons.ASSIGNMENT_ROUNDED,  "Tests",       False, on_pruebas),
        (ft.Icons.BAR_CHART_ROUNDED,   "Statistics",  False, on_estadisticas),
        (ft.Icons.EMOJI_EVENTS_ROUNDED,"Achievements",        True,  None),   # activo
        (ft.Icons.SETTINGS_ROUNDED,    "Settings", False, on_configuracion),
    ]
    return ft.Container(
        width=205, bgcolor=NAV_BG,
        shadow=ft.BoxShadow(blur_radius=16, color="#18000000", offset=ft.Offset(2, 0)),
        content=ft.Column(spacing=0, expand=True, controls=[
            ft.Container(height=20),
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
                logo_icon(),
                ft.Text("DixLearn", size=16, weight=ft.FontWeight.W_900, color=DARK),
                ft.Text("Makes you learn", size=11, color=GRAY_TEXT),
            ]),
            ft.Container(height=20),
            ft.Column(expand=True, spacing=2,
                      controls=[nav_item_widget(i, l, a, cb) for i, l, a, cb in nav_items]),
            ft.Divider(color="#EEEEEE", height=1),
            ft.Container(
                padding=ft.Padding(left=12, right=12, top=10, bottom=20),
                content=ft.Row(spacing=10, controls=[
                    avatar_widget(iniciales, foto_b64, size=38, text_size=13),
                    ft.Column(spacing=0, expand=True, controls=[
                        ft.Text(usuario, size=13, weight=ft.FontWeight.W_700, color=DARK),
                        ft.Text("Student", size=11, color=GRAY_TEXT),
                    ]),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GRAY_TEXT, size=18),
                ]),
            ),
        ]),
    )


# ── Topbar ─────────────────────────────────────────────────────────────────────

def topbar_widget(usuario: str, foto_b64=None, puntos=0, mobile=False):
    iniciales = "".join([p[0].upper() for p in usuario.split()[:2]]) if usuario else "U"

    titulo = ft.Column(spacing=2, controls=[
        ft.Text("Achievements", size=24, weight=ft.FontWeight.W_800, color=DARK),
        ft.Text("Discover your achievements and keep reaching new goals.",
                size=13, color=GRAY_TEXT),
    ])

    puntos_badge = ft.Container(
        content=ft.Row(controls=[
            ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=20),
            ft.Text(f"{puntos} points", size=14,
                    weight=ft.FontWeight.W_700, color=DARK),
        ], spacing=6),
        bgcolor=WHITE, border_radius=24,
        border=ft.Border.all(1, "#EEEEEE"),
        padding=ft.Padding(left=16, right=16, top=8, bottom=8),
        shadow=ft.BoxShadow(blur_radius=6, color="#10000000",
                            offset=ft.Offset(0, 2)),
    )

    avatar = avatar_widget(iniciales, foto_b64, size=44, text_size=15)

    if mobile:
        # Stacked layout on mobile so nothing gets pushed off-screen
        # and cropped (title/avatar on top, points badge below).
        return ft.Container(
            bgcolor=WHITE,
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
            content=ft.Column(spacing=12, controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[titulo, avatar],
                ),
                puntos_badge,
            ]),
        )

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=32, right=32, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=8, color="#10000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                titulo,
                ft.Row(spacing=12, controls=[puntos_badge, avatar]),
            ],
        ),
    )


# ── Filtros (All / Obtained / In progress) ──────────────────────────────────

def filtros_widget(filtro_actual: list, on_change):
    opciones = ["All", "Obtained", "In progress"]

    def btn(label):
        active = filtro_actual[0] == label
        return ft.Container(
            content=ft.Text(label, size=13, weight=ft.FontWeight.W_700,
                            color=WHITE if active else DARK),
            bgcolor=BLUE if active else WHITE,
            border_radius=24,
            border=ft.Border.all(1, "#DDDDDD") if not active else None,
            padding=ft.Padding(left=22, right=22, top=10, bottom=10),
            ink=True,
            on_click=lambda e, l=label: on_change(l),
        )

    return ft.Row(spacing=10, wrap=True, controls=[btn(o) for o in opciones])


# ── Card de logro ───────────────────────────────────────────────────────────

def logro_card(emoji_icon, icon_bg, title, desc, puntos, obtenido,
               progreso_actual=None, progreso_total=None):
    """
    emoji_icon  : emoji string or ft.Icon
    icon_bg     : circle background color
    obtenido    : True = achievement unlocked, False = in progress
    progreso_*  : only if obtenido=False
    """
    # Icono central
    if isinstance(emoji_icon, str):
        icon_widget = ft.Text(emoji_icon, size=26)
    else:
        icon_widget = emoji_icon

    icon_circle = ft.Container(
        width=54, height=54, border_radius=27,
        bgcolor=icon_bg, alignment=CENTER,
        content=icon_widget,
    )

    # Cuerpo inferior
    bottom_controls = [
        ft.Text(title, size=12, weight=ft.FontWeight.W_800, color=DARK,
                text_align=ft.TextAlign.CENTER),
        ft.Text(desc, size=10, color=GRAY_TEXT, text_align=ft.TextAlign.CENTER),
    ]

    if not obtenido and progreso_actual is not None:
        # Barra de progreso
        pct = min(100, int((progreso_actual / progreso_total) * 100)) if progreso_total else 0
        bottom_controls.append(
            ft.Container(
                content=ft.Column(spacing=3, controls=[
                    ft.Container(
                        width=110, height=7, border_radius=4, bgcolor="#EEEEEE",
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Container(
                            width=110 * (pct / 100), height=7, border_radius=4,
                            bgcolor=BLUE,
                        ),
                    ),
                    ft.Text(f"{progreso_actual}/{progreso_total}",
                            size=9, color=GRAY_TEXT,
                            text_align=ft.TextAlign.RIGHT),
                ]),
                width=110,
            )
        )

    bottom_controls.append(
        ft.Container(
            bgcolor="#FFF8E7", border_radius=20,
            padding=ft.Padding(left=10, right=10, top=4, bottom=4),
            content=ft.Row(spacing=4, alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Icon(ft.Icons.STAR_ROUNDED, color=AMBER, size=14),
                ft.Text(f"{puntos} points", size=11,
                        weight=ft.FontWeight.W_700, color=DARK),
            ]),
        )
    )

    return ft.Container(
        bgcolor=WHITE,
        border_radius=14,
        border=ft.Border.all(1.5, "#EEEEEE"),
        padding=ft.Padding(left=14, right=14, top=18, bottom=16),
        shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[icon_circle, *bottom_controls],
        ),
    )


# ── Datos de logros ────────────────────────────────────────────────────────────

def _logro_img(src, size=32, fallback_emoji="🏅"):
    """Real achievement image (with emoji fallback if it fails to load)."""
    return ft.Image(src=src, width=size, height=size, fit="contain",
                    error_content=ft.Text(fallback_emoji, size=size * 0.85))


LOGROS_OBTENIDOS = [
    dict(emoji_icon=_logro_img("imagenes/libro.png", fallback_emoji="📖"), icon_bg="#EDE7FF",
         title="Constant Reader", desc="You bought 10 lessons",
         puntos=50,  obtenido=True),
    dict(emoji_icon=_logro_img("imagenes/estrella.png", fallback_emoji="⭐"),
         icon_bg=GREEN,
         title="Good performance", desc="You scored 80% or more\non a test",
         puntos=75,  obtenido=True),
    dict(emoji_icon=_logro_img("imagenes/fuego.png", fallback_emoji="🔥"), icon_bg=AMBER,
         title="10-day streak", desc="You studied 10 days\nin a row",
         puntos=50,  obtenido=True),
    dict(emoji_icon=_logro_img("imagenes/trofeo.png", fallback_emoji="🏆"),
         icon_bg="#E53935",
         title="Explorer", desc="You completed your\nfirst test",
         puntos=50,  obtenido=True),
    dict(emoji_icon=_logro_img("imagenes/grade.png", fallback_emoji="🎓"),
         icon_bg=BLUE,
         title="On the way", desc="You completed 5\nlessons",
         puntos=25,  obtenido=True),
]

LOGROS_EN_PROGRESO = [
    dict(emoji_icon=_logro_img("imagenes/libro.png", fallback_emoji="📖"), icon_bg=PURPLE,
         title="Dedicated learner", desc="Complete 30 lessons",
         puntos=100, obtenido=False, progreso_actual=24, progreso_total=30),
    dict(emoji_icon=_logro_img("imagenes/listo.png", fallback_emoji="✅"),
         icon_bg=BLUE,
         title="Accuracy", desc="Get a 90% average\non 5 tests",
         puntos=100, obtenido=False, progreso_actual=3, progreso_total=5),
    dict(emoji_icon=_logro_img("imagenes/fuego.png", fallback_emoji="🔥"), icon_bg="#FF7043",
         title="30-day streak", desc="Study 30 days\nin a row",
         puntos=100, obtenido=False, progreso_actual=12, progreso_total=30),
    dict(emoji_icon=_logro_img("imagenes/estrella.png", fallback_emoji="⭐"),
         icon_bg=GREEN,
         title="SuperComprehension", desc="Answer 100 questions\ncorrectly",
         puntos=100, obtenido=False, progreso_actual=65, progreso_total=100),
    dict(emoji_icon=_logro_img("imagenes/trofeo.png", fallback_emoji="🏆"),
         icon_bg=NAVY,
         title="DixLearn Master", desc="Get all\navailable achievements",
         puntos=200, obtenido=False, progreso_actual=5, progreso_total=10),
]


# ── Banner inferior ────────────────────────────────────────────────────────────

def banner_motivacion():
    return ft.Container(
        bgcolor=WHITE,
        border_radius=14,
        border=ft.Border.all(1.5, "#EEEEEE"),
        padding=ft.Padding(left=20, right=20, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
        content=ft.Row(spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                       controls=[
            ft.Container(
                width=44, height=44, border_radius=22, bgcolor="#E8F8F0",
                alignment=CENTER,
                content=ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color=GREEN, size=26),
            ),
            ft.Column(spacing=2, expand=True, controls=[
                ft.Text("Keep it up, each achievement brings you closer to mastering new skills",
                        size=13, weight=ft.FontWeight.W_700, color=DARK),
                ft.Text("Points from achievements are added to your total score.",
                        size=11, color=GRAY_TEXT),
            ]),
        ]),
    )


# ── Builder principal ──────────────────────────────────────────────────────────

def build_logros(page: ft.Page, usuario: str, on_inicio=None,
                 on_lecciones=None, on_pruebas=None, on_estadisticas=None,
                 on_configuracion=None):

    usuario_doc = obtener_usuario(usuario) or {}
    foto_b64 = usuario_doc.get("foto")
    puntos = prog.obtener_progreso(usuario).get("puntos", 0)
    puntos = prog.obtener_progreso(usuario).get("puntos", 0)

    filtro = ["All"]   # estado mutable

    def fila_logros(lista):
        # Tarjetas de ancho fijo en una fila que se acomoda sola
        # (wrap) según el espacio disponible: 5 por fila en pantallas
        # anchas, menos en celular, sin aplastarse ni cortarse.
        cards = [logro_card(**d) for d in lista]
        return ft.Row(spacing=14, run_spacing=14, wrap=True,
                      alignment=ft.MainAxisAlignment.CENTER,
                      controls=[ft.Container(content=c, width=150) for c in cards])

    contenido = ft.Ref[ft.Column]()

    def render_logros():
        f = filtro[0]
        if f == "All":
            filas = [fila_logros(LOGROS_OBTENIDOS), fila_logros(LOGROS_EN_PROGRESO)]
        elif f == "Obtained":
            filas = [fila_logros(LOGROS_OBTENIDOS)]
        else:
            filas = [fila_logros(LOGROS_EN_PROGRESO)]
        return filas

    def on_filtro(label):
        filtro[0] = label
        contenido.current.controls = [
            filtros_widget(filtro, on_filtro),
            *render_logros(),
            banner_motivacion(),
        ]
        page.update()

    main_content = ft.Container(
        expand=True, bgcolor=BG,
        content=ft.Column(expand=True, spacing=0, controls=[
            topbar_widget(usuario, foto_b64, puntos=puntos, mobile=is_mobile(page)),
            ft.Container(
                expand=True,
                content=ft.ListView(
                    expand=True,
                    padding=content_padding(page, top=24),
                    spacing=18,
                    controls=[
                        ft.Column(
                            ref=contenido,
                            spacing=18,
                            # STRETCH hace que cada fila (filtros, tarjetas de
                            # logros, banner) ocupe todo el ancho disponible,
                            # así el alignment=CENTER de la fila de tarjetas
                            # puede repartir el espacio sobrante en ambos
                            # lados en vez de quedar pegado a la izquierda.
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            controls=[
                                filtros_widget(filtro, on_filtro),
                                *render_logros(),
                                banner_motivacion(),
                            ],
                        ),
                    ],
                ),
            ),
        ]),
    )

    sidebar = sidebar_widget(usuario, foto_b64, on_inicio=on_inicio, on_lecciones=on_lecciones,
                             on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                             on_configuracion=on_configuracion)
    mobile = is_mobile(page)
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
            mobile_bottom_nav("logros", on_inicio=on_inicio, on_lecciones=on_lecciones,
                               on_pruebas=on_pruebas, on_estadisticas=on_estadisticas,
                               on_configuracion=on_configuracion),
        ])
    return body