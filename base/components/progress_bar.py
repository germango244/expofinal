"""Barra superior con indicador de progreso por puntos."""

import flet as ft
from config import WHITE, DARK, PURPLE, AMBER


def top_progress_bar(paso: int, total: int, on_home):
    """Crea la barra superior con puntos de progreso y botón home."""
    dots = []
    for i in range(total):
        if i <= paso:
            color = PURPLE
            size  = 12
        else:
            color = "#CCCCCC"
            size  = 10
        dots.append(
            ft.Container(
                width=size, height=size, border_radius=size // 2, bgcolor=color,
            )
        )

    # Líneas entre dots
    dot_row_controls = []
    for idx, d in enumerate(dots):
        dot_row_controls.append(d)
        if idx < len(dots) - 1:
            dot_row_controls.append(
                ft.Container(
                    width=24, height=3, border_radius=2,
                    bgcolor=PURPLE if idx < paso else "#CCCCCC",
                )
            )

    return ft.Container(
        bgcolor=WHITE,
        padding=ft.Padding(left=20, right=20, top=16, bottom=16),
        shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.HOME_ROUNDED,
                    icon_color=DARK,
                    icon_size=24,
                    on_click=on_home,
                ),
                ft.Row(spacing=4, controls=dot_row_controls),
                ft.Icon(ft.Icons.STAR_OUTLINE_ROUNDED, color=AMBER, size=24),
            ],
        ),
    )