import pytest

from manim_physics.utils.id_generator import Id_generator


@pytest.fixture
def reset_id_generator(monkeypatch):
    """ Rests the count of the id_generator"""
    monkeypatch.setattr(Id_generator, "counter", 0)