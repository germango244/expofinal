"""Helpers compartidos para que todas las pantallas se adapten a
celular/tablet/PC, y se re-acomoden en vivo cuando se cambia el
tamaño de la ventana (no solo la primera vez que se dibujan).

Uso típico dentro de cualquier pantalla:

    from pantalla.responsive import is_mobile, stack_or_row, mobile_bottom_nav

    mobile = is_mobile(page)
    sidebar.visible = not mobile
    ...
    if mobile:
        return ft.Column(expand=True, spacing=0, controls=[
            ft.Row(expand=True, spacing=0, controls=[sidebar, main_content]),
            mobile_bottom_nav("inicio", on_inicio=..., on_lecciones=..., ...),
        ])
    return ft.Row(expand=True, spacing=0, controls=[sidebar, main_content])
"""

import flet as ft

# ══════════════════════════════════════════════════════════════════════
#  MODO EXCLUSIVO PARA TELÉFONO
#  La app ya no tiene layout de escritorio: is_mobile() siempre devuelve
#  True, sin importar el ancho real de la ventana/navegador, así que el
#  sidebar fijo queda siempre oculto y se usa la barra de navegación de
#  abajo (mobile_bottom_nav) en todas las pantallas.
#  Para volver a tener un layout de PC, alcanza con poner
#  FORZAR_SOLO_TELEFONO = False.
# ══════════════════════════════════════════════════════════════════════
FORZAR_SOLO_TELEFONO = True

# Por debajo de este ancho (en pixeles) consideramos que estamos en celular:
# se oculta el sidebar fijo de 205px y aparece una barra de navegación abajo.
MOBILE_BP = 700

# Por debajo de este ancho, además, achicamos paddings/tamaños de texto.
SMALL_MOBILE_BP = 420

PRIMARY   = "#D94F2B"
WHITE     = "#FFFFFF"
GRAY_TEXT = "#777777"
DARK      = "#1A1A1A"


def is_mobile(page: ft.Page) -> bool:
    """True si la ventana/pantalla es angosta (celular).

    En modo exclusivo para teléfono siempre devuelve True."""
    if FORZAR_SOLO_TELEFONO:
        return True
    return (page.width or 1150) < MOBILE_BP


def is_small_mobile(page: ft.Page) -> bool:
    """True si es un celular chico (para achicar todavía más)."""
    return (page.width or 1150) < SMALL_MOBILE_BP


def content_padding(page: ft.Page, top=28, bottom=36):
    """Padding horizontal del contenido principal: se achica en celular
    para que no se corten las tarjetas contra el borde."""
    side = 14 if is_mobile(page) else 32
    return ft.Padding(left=side, right=side, top=top, bottom=bottom)


def stack_or_row(mobile: bool, controls, spacing=16, expand=True,
                  vertical_alignment=ft.CrossAxisAlignment.START):
    """Devuelve un ft.Column (apilado, uno debajo del otro) si `mobile`
    es True, o un ft.Row (lado a lado) si es False. Así una fila de
    tarjetas que en PC va horizontal, en celular se acomoda vertical
    en vez de aplastarse o cortarse."""
    if mobile:
        return ft.Column(controls=controls, spacing=spacing, expand=expand)
    return ft.Row(controls=controls, spacing=spacing, expand=expand,
                  vertical_alignment=vertical_alignment)


def _nav_button(icon, label, active, on_click):
    color = PRIMARY if active else GRAY_TEXT
    return ft.Container(
        expand=True,
        ink=on_click is not None,
        on_click=on_click,
        padding=ft.Padding(left=2, right=2, top=8, bottom=6),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
            controls=[
                ft.Icon(icon, color=color, size=22),
                ft.Text(label, color=color, size=9,
                        weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_500),
            ],
        ),
    )


def mobile_bottom_nav(active: str, on_inicio=None, on_lecciones=None, on_pruebas=None,
                       on_estadisticas=None, on_logros=None, on_configuracion=None):
    """Barra de navegación fija abajo, para usar en vez del sidebar
    cuando la pantalla es angosta (celular). `active` es la clave de
    la pantalla actual: 'inicio' | 'lecciones' | 'pruebas' |
    'estadisticas' | 'logros' | 'configuracion'."""
    items = [
        ("inicio",        ft.Icons.HOME_ROUNDED,         "Home",     on_inicio),
        ("lecciones",     ft.Icons.MENU_BOOK_ROUNDED,    "Lessons",  on_lecciones),
        ("pruebas",       ft.Icons.ASSIGNMENT_ROUNDED,   "Tests",    on_pruebas),
        ("estadisticas",  ft.Icons.BAR_CHART_ROUNDED,    "Stats",    on_estadisticas),
        ("logros",        ft.Icons.EMOJI_EVENTS_ROUNDED, "Awards",   on_logros),
        ("configuracion", ft.Icons.SETTINGS_ROUNDED,     "Settings", on_configuracion),
    ]
    return ft.Container(
        bgcolor=WHITE,
        shadow=ft.BoxShadow(blur_radius=16, color="#20000000", offset=ft.Offset(0, -2)),
        padding=ft.Padding(left=2, right=2, top=4, bottom=6),
        content=ft.Row(
            controls=[_nav_button(icon, label, key == active, cb)
                      for key, icon, label, cb in items],
        ),
    )
