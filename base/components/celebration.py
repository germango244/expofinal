"""Pantalla de celebración al completar una lección."""

import flet as ft
from config import WHITE, DARK, GRAY_TEXT, PURPLE, AMBER, CENTER

try:
    from pantalla import progreso as prog
except Exception:
    prog = None


def build_celebracion(on_repasar, on_continuar, usuario: str = None,
                      nivel: int = None, num: int = None,
                      titulo: str = None, puntaje: int = 100):
    """Pantalla final con confeti, mensaje de éxito y botones de acción.

    Si se pasan `usuario`, `nivel` y `num`, esta pantalla guarda automáticamente
    la lección como completada (puntos, % de progreso y desbloqueo de la
    siguiente lección) en la cuenta del usuario en MongoDB. Así, cada lección
    del proyecto solo necesita llamar a build_celecion(...) pasando esos datos
    al terminar el ejercicio, sin preocuparse de nada más.
    """
    if prog is not None and usuario and nivel is not None and num is not None:
        try:
            prog.marcar_leccion_completada(usuario, nivel, num, puntaje=puntaje)
        except Exception as ex:
            print(f"⚠️ No se pudo guardar el progreso: {ex}")

    mensaje = f'Aprendiste "{titulo}".' if titulo else 'Aprendiste la letra "A".'

    return ft.Container(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(src="imagenes/fondo.png", fit="cover"),
                ),
                ft.Container(
                    expand=True,
                    blur=ft.Blur(sigma_x=5, sigma_y=5),
                ),
                ft.Container(expand=True, bgcolor="#60F9F3CC"),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Container(expand=True),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("🎊", size=30),
                                ft.Text("🎉", size=30),
                                ft.Text("🎊", size=30),
                            ],
                            spacing=16,
                        ),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Image(
                                src="imagenes/completoabeja.png",
                                width=220,
                                height=220,
                                fit="contain",
                                error_content=ft.Text("🐝", size=120),
                            ),
                            alignment=CENTER,
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            width=300,
                            border_radius=20,
                            bgcolor=WHITE,
                            padding=ft.Padding(left=24, right=24, top=24, bottom=24),
                            shadow=ft.BoxShadow(
                                blur_radius=20,
                                color="#30000000",
                                offset=ft.Offset(0, 6),
                            ),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=12,
                                controls=[
                                    ft.Text(
                                        "¡Lo hiciste increíble!",
                                        size=22,
                                        weight=ft.FontWeight.W_900,
                                        color=DARK,
                                    ),
                                    ft.Text(
                                        mensaje,
                                        size=14,
                                        color=GRAY_TEXT,
                                    ),
                                    ft.Text(
                                        "Sigue así, tú puedes hacer\ngrandes cosas.",
                                        size=14,
                                        color=GRAY_TEXT,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(height=4),
                                    ft.Container(
                                        width=64,
                                        height=64,
                                        border_radius=32,
                                        bgcolor=AMBER,
                                        alignment=CENTER,
                                        shadow=ft.BoxShadow(
                                            blur_radius=12,
                                            color="#40F5A623",
                                            offset=ft.Offset(0, 4),
                                        ),
                                        content=ft.Text("⭐", size=34),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(height=30),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=16,
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.REFRESH_ROUNDED,
                                                color=PURPLE,
                                                size=18,
                                            ),
                                            ft.Text(
                                                "Repasar",
                                                color=PURPLE,
                                                size=14,
                                                weight=ft.FontWeight.W_700,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    bgcolor=WHITE,
                                    on_click=on_repasar,
                                    style=ft.ButtonStyle(
                                        side=ft.BorderSide(0, "transparent"),
                                        shape=ft.RoundedRectangleBorder(radius=24),
                                        elevation=2,
                                        padding=ft.Padding(
                                            left=22, right=22, top=14, bottom=14
                                        ),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "Continuar",
                                                color=WHITE,
                                                size=14,
                                                weight=ft.FontWeight.W_700,
                                            ),
                                            ft.Icon(
                                                ft.Icons.ARROW_FORWARD_ROUNDED,
                                                color=WHITE,
                                                size=18,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    bgcolor=AMBER,
                                    on_click=on_continuar,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=24),
                                        elevation=2,
                                        padding=ft.Padding(
                                            left=22, right=22, top=14, bottom=14
                                        ),
                                    ),
                                ),
                            ],
                        ),
                        ft.Container(expand=True),
                    ],
                ),
            ],
        ),
    )