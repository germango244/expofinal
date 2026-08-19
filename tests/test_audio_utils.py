import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "base"))

from audio_utils import resolve_audio_path


def test_resolve_audio_path_uses_expected_project_structure():
    assert resolve_audio_path("vowels", "a") == "audios/vowels/a.mp3"
    assert resolve_audio_path("syllables", "ca") == "audios/syllables/ca.mp3"
    assert resolve_audio_path("words", "Apple") == "audios/words/apple.mp3"
