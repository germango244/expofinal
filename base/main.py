import flet as ft
import asyncio
import os
import sys
import socket
from pathlib import Path


print("====================================")
print("TU VERSION DE FLET ES:", ft.__version__)
print("====================================")

# Asegurar que la carpeta raíz del proyecto esté en sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from pantalla.login import build_login_screen, BG
from pantalla.dashboard import build_dashboard
from pantalla.pruebas import build_pruebas
from pantalla.lecciones import build_lecciones
from pantalla.estadisticas import build_estadisticas
from pantalla.logros import build_logros
from pantalla.configuracion import build_configuracion
from pantalla.perfil import build_perfil
from pantalla.welcome import build_welcome_screen


from lessons.reconoce_letras import build_reconoce_letras
from lessons.sonidos_vocales import build_sonidos_vocales
from lessons.silabas_simples import build_silabas_simples
from lessons.palabras_basica import build_lectura_basica
from lessons.comprension_lectora import build_comprension_lectora
from lessons.palabras_similares import build_palabras_similares
from lessons.velocidad_lectora import build_velocidad_lectora
from lessons.comprension_avanzada import build_comprension_avanzada
from lessons.comprension_experta import build_comprension_experta
from lessons.ortografia_divertida import build_ortografia_divertida
from lessons.atencion_concentracion import build_atencion_concentracion
from lessons.lectura_completa import build_lectura_completa


def main(page: ft.Page):
    page.title = "DixLearn - Makes you learn"
    page.bgcolor = BG
    page.padding = 0
    page.bgimage = "imagenes/fondo.png"
    page.bgopacity = 0.16

    # ══════════════════════════════════════════
    #  🖼️ FONDO DE PANTALLA
    #  Nota: Si usas assets_dir="img", solo pon el nombre del archivo.
    # ═════════════════════════════════════════
    # page.bgimage = "fondo_general.png"  # ✅ Sin "img/" porque ya está en assets_dir
    # page.bgopacity = 0.15

    # ══════════════════════════════════════════════════════════════════
    #  📱 MODO EXCLUSIVO PARA TELÉFONO
    #  El layout de PC (sidebar fijo, etc.) queda desactivado en
    #  pantalla/responsive.py (FORZAR_SOLO_TELEFONO = True). Acá además:
    #  - si la app corre como ventana de escritorio, la abrimos y la
    #    bloqueamos con proporciones de celular (no se puede agrandar);
    #  - si corre en el navegador, envolvemos todo el contenido en un
    #    "marco" centrado del mismo ancho, para que en una PC con
    #    pantalla ancha se vea igual que en un celular, en vez de
    #    estirarse a lo ancho.
    # ══════════════════════════════════════════════════════════════════
    PHONE_WIDTH = 430
    PHONE_HEIGHT = 900

    page.window.width = PHONE_WIDTH
    page.window.height = PHONE_HEIGHT
    page.window.min_width = PHONE_WIDTH
    page.window.max_width = PHONE_WIDTH
    page.window.resizable = False
    page.window.maximizable = False

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"usuario": "", "pantalla_actual": None, "resize_pendiente": False}

    # ── Responsivo: re-dibuja la pantalla actual cada vez que la
    #    ventana cambia de tamaño (achicar/agrandar en PC, o rotar/abrir
    #    en el celular), para que el sidebar/menú y las tarjetas se
    #    reacomoden solas sin tener que recargar la app.
    #    Se hace con un pequeño "debounce" para no redibujar en cada
    #    pixel mientras se arrastra el borde de la ventana. ──
    async def _resize_debounced():
        await asyncio.sleep(0.15)
        estado["resize_pendiente"] = False
        renderizar = estado.get("pantalla_actual")
        if renderizar:
            renderizar()

    def on_resize(e=None):
        if estado["resize_pendiente"]:
            return
        estado["resize_pendiente"] = True
        page.run_task(_resize_debounced)

    page.on_resize = on_resize

    # ── Navegación ──
    def go_welcome(e=None):
        estado["pantalla_actual"] = go_welcome
        try:
            switcher.content = build_welcome_screen(
                page, on_comenzar=go_login, on_login=go_login,
            )
            page.update()
        except Exception as ex:
            import traceback
            print(f"Error en welcome: {ex}")
            traceback.print_exc()

    def go_login(e=None):
        estado["pantalla_actual"] = go_login
        switcher.content = build_login_screen(
            page,
            on_login_success=on_login_success,
            on_register_success=on_login_success,
        )
        page.update()

    def on_login_success(usuario: str):
        estado["usuario"] = usuario
        go_dashboard()

    def go_dashboard(e=None):
        estado["pantalla_actual"] = go_dashboard
        switcher.content = build_dashboard(
            page, estado["usuario"],
            on_lecciones=go_lecciones,
            on_pruebas=go_pruebas,
            on_estadisticas=go_estadisticas,
            on_logros=go_logros,
            on_configuracion=go_configuracion,
            on_perfil=go_perfil,
        )
        page.update()

    def go_pruebas(e=None):
        estado["pantalla_actual"] = go_pruebas
        switcher.content = build_pruebas(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_lecciones=go_lecciones,
            on_estadisticas=go_estadisticas,
            on_logros=go_logros,
            on_configuracion=go_configuracion,
        )
        page.update()

    def go_lecciones(e=None):
        estado["pantalla_actual"] = go_lecciones
        switcher.content = build_lecciones(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_pruebas=go_pruebas,
            on_estadisticas=go_estadisticas,
            on_logros=go_logros,
            on_configuracion=go_configuracion,
            on_abrir_leccion=on_abrir_leccion,
        )
        page.update()

    def go_estadisticas(e=None):
        estado["pantalla_actual"] = go_estadisticas
        switcher.content = build_estadisticas(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_lecciones=go_lecciones,
            on_pruebas=go_pruebas,
            on_logros=go_logros,
            on_configuracion=go_configuracion,
        )
        page.update()

    def go_logros(e=None):
        estado["pantalla_actual"] = go_logros
        switcher.content = build_logros(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_lecciones=go_lecciones,
            on_pruebas=go_pruebas,
            on_estadisticas=go_estadisticas,
            on_configuracion=go_configuracion,
        )
        page.update()

    def go_logout(e=None):
        estado["usuario"] = ""
        go_login()

    def go_configuracion(e=None):
        estado["pantalla_actual"] = go_configuracion
        switcher.content = build_configuracion(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_lecciones=go_lecciones,
            on_pruebas=go_pruebas,
            on_estadisticas=go_estadisticas,
            on_logros=go_logros,
            on_logout=go_logout,
        )
        page.update()

    def go_perfil(e=None):
        estado["pantalla_actual"] = go_perfil
        switcher.content = build_perfil(
            page, estado["usuario"],
            on_inicio=go_dashboard,
            on_lecciones=go_lecciones,
            on_pruebas=go_pruebas,
            on_estadisticas=go_estadisticas,
            on_logros=go_logros,
            on_configuracion=go_configuracion,
        )
        page.update()

    # ── Abrir lección específica ──
    def on_abrir_leccion(*args):
        ints = [a for a in args if isinstance(a, int)]
        if len(ints) >= 2:
            nivel, num = ints[0], ints[1]
        elif len(args) == 2:
            nivel, num = args[0], args[1]
        elif len(args) == 3:
            _, nivel, num = args
        else:
            return

        estado["pantalla_actual"] = lambda: on_abrir_leccion(nivel, num)

        # NIVEL 1
        if nivel == 1 and num == 1:
            switcher.content = build_reconoce_letras(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 1 and num == 2:
            switcher.content = build_sonidos_vocales(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 1 and num == 3:
            switcher.content = build_silabas_simples(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 1 and num == 4:
            switcher.content = build_lectura_basica(
                page=page,
                usuario=estado["usuario"],
                on_lecciones=go_lecciones,
                on_inicio=go_dashboard,
                on_siguiente=lambda e: on_abrir_leccion(1, 5),
                num_leccion=4,
            )
        elif nivel == 1 and num == 5:
            switcher.content = build_comprension_lectora(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        
        # NIVEL 2
        elif nivel == 2 and num == 1:
            switcher.content = build_palabras_similares(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 2 and num == 2:
            switcher.content = build_velocidad_lectora(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 2 and num == 3:
            switcher.content = build_comprension_avanzada(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        
        # NIVEL 3
        elif nivel == 3 and num == 1:
            switcher.content = build_comprension_experta(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 3 and num == 2:
            switcher.content = build_ortografia_divertida(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        
        # NIVEL 4
        elif nivel == 4 and num == 1:
            switcher.content = build_atencion_concentracion(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        elif nivel == 4 and num == 2:
            switcher.content = build_lectura_completa(page=page, usuario=estado["usuario"], on_lecciones=go_lecciones, on_inicio=go_dashboard)
        
        page.update()

    # ── Switcher ──
    estado["pantalla_actual"] = go_welcome
    switcher = ft.AnimatedSwitcher(
        content=build_welcome_screen(page, on_comenzar=go_login, on_login=go_login),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        expand=True,
    )
    # Marco de ancho fijo tipo celular: en el navegador (donde page.window
    # no aplica), esto evita que el contenido se estire a lo ancho de una
    # pantalla de PC. En escritorio, page.window ya deja la ventana fija
    # en PHONE_WIDTH, así que este contenedor simplemente ocupa todo.
    page.add(
        ft.Container(
            width=PHONE_WIDTH,
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=switcher,
        )
    )

    # ── Splash timer ──
    async def splash_timer():
        await asyncio.sleep(2.5)
        go_welcome()

    page.run_task(splash_timer)


def obtener_puerto_libre(host: str = "127.0.0.1", preferido: int = 8550) -> int:
    """
    Intenta usar el puerto 'preferido'. Si ya está ocupado (por ejemplo,
    una instancia anterior de la app que quedó colgada), le pide al
    sistema operativo un puerto libre cualquiera, así nunca hay que
    andar cambiando el número a mano ni matando procesos.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, preferido))
            return preferido
        except OSError:
            s.bind((host, 0))  # 0 = "dame cualquier puerto libre"
            puerto_libre = s.getsockname()[1]
            print(f"⚠️  El puerto {preferido} estaba ocupado. Usando el puerto {puerto_libre} en su lugar.")
            return puerto_libre


if __name__ == "__main__":
    # La carpeta de imágenes está junto a la carpeta del proyecto, no dentro de base.
    assets_dir = str(PROJECT_ROOT.parent)
    host = os.getenv("HOST", "0.0.0.0")
    puerto = int(os.getenv("PORT", "8550"))
    print(f"🚀 Abriendo DixLearn en http://{host}:{puerto}")
    ft.run(
        main,
        assets_dir=assets_dir,
        view=ft.AppView.WEB_BROWSER,
        host=host,
        port=puerto,
    )