from __future__ import annotations

import asyncio
import re
from pathlib import Path

import flet as ft

try:
    import pygame

    pygame.mixer.init()
    _MIXER_OK = True
except Exception:
    _MIXER_OK = False


PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_ROOT = PROJECT_ROOT / "audios"

# Un pygame.mixer.Sound cargado en memoria por cada ruta de audio,
# para no releer el mp3 de disco cada vez que se toca el altavoz.
_SOUND_CACHE: dict[str, "pygame.mixer.Sound"] = {}


def _normalize_name(name: str) -> str:
    value = str(name).strip().lower()
    value = value.replace(" ", "_")
    value = value.replace("-", "_")
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    return value.strip("_")


def resolve_audio_path(category: str, name: str) -> str:
    """Return the relative asset path for a lesson sound file."""
    folder = str(category).strip("/")
    clean_name = _normalize_name(name)
    folder_path = AUDIO_ROOT / folder
    if not folder_path.exists():
        return f"audios/{folder}/{clean_name}.mp3"

    candidate_names = []
    if str(name).strip() and Path(str(name)).suffix:
        candidate_names.append(Path(str(name)).name)
    else:
        for ext in (".mp3", ".wav", ".ogg", ".m4a"):
            candidate_names.append(f"{clean_name}{ext}")

    for candidate in candidate_names:
        full = folder_path / candidate
        if full.exists():
            return f"audios/{folder}/{full.name}"

    if candidate_names:
        return f"audios/{folder}/{candidate_names[0]}"
    return f"audios/{folder}/{clean_name}.mp3"


def _animate_audio_bar(page: ft.Page, progress_bar: ft.ProgressBar | None) -> None:
    if progress_bar is None or page is None:
        return

    async def _pulse():
        progress_bar.value = 0.05
        page.update()
        for _ in range(30):
            await asyncio.sleep(0.08)
            if progress_bar.value is None:
                break
            progress_bar.value = min(progress_bar.value + 0.04, 1.0)
            page.update()
        progress_bar.value = 0.0
        page.update()

    try:
        page.run_task(_pulse)
    except Exception:
        pass


def _get_sound(rel_path: str) -> "pygame.mixer.Sound | None":
    """Load (and cache) a pygame Sound object for this audio file."""
    full_path = PROJECT_ROOT / rel_path
    if not full_path.exists():
        return None
    cached = _SOUND_CACHE.get(rel_path)
    if cached is not None:
        return cached
    try:
        sound = pygame.mixer.Sound(str(full_path))
    except Exception:
        return None
    _SOUND_CACHE[rel_path] = sound
    return sound


def play_audio(
    page: ft.Page,
    category: str,
    name: str,
    *,
    progress_bar: ft.ProgressBar | None = None,
):
    """Play a lesson sound inline, inside the app itself.

    Uses pygame.mixer (a plain Python library, not a Flet extension), so
    it works both in dev (`flet run`) and in a packaged build, and it
    never pops open Windows Media Player / the system's default app.
    """
    if page is None:
        return None

    rel_path = resolve_audio_path(category, name)

    if progress_bar is not None:
        progress_bar.value = 0.0
        _animate_audio_bar(page, progress_bar)

    if _MIXER_OK:
        sound = _get_sound(rel_path)
        if sound is not None:
            try:
                sound.stop()
                sound.play()
            except Exception:
                pass

    return rel_path


def make_audio_button(page: ft.Page, category: str, name: str, *, size: int = 24, color: str = "#7B61FF"):
    """Create a tap-to-listen button linked to the correct MP3 file."""
    return ft.IconButton(
        icon=ft.Icons.VOLUME_UP_ROUNDED,
        icon_color=color,
        icon_size=size,
        tooltip=f"Listen to {name}",
        on_click=lambda e: play_audio(page, category, name),
    )
