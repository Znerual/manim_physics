import pytest

from manim_physics.utils.id_generator import Id_generator
from manim_physics.objects.mass import Mass
from manim_physics.objects.wall import Wall
from manim_physics.objects.spring2D import Spring2D


def test_generation1(reset_id_generator):
    """ Create multiple objects and check id generation"""
    mass1 = Mass(12)
    assert mass1.id_hash == 1
    mass2 = Mass(12)
    assert mass2.id_hash == 2
    mass3 = Mass(13)
    assert mass3.id_hash == 3

def test_generation2(reset_id_generator):
    """ Create multiple objects and check id generation"""
    mass1 = Mass(12)
    mass2 = Mass(12)
    assert mass2.id_hash == 2
    mass3 = Mass(13)

