from manim import *
from manim_physics.objects.mass import Mass
from manim_physics.objects.wall import Wall
from manim_physics.objects.spring2D import Spring2D


class Spring(Scene):
    def construct(self):
        mass1 = Mass(3, LEFT.copy())
        mass2 = Mass(1.5, RIGHT.copy())
        mass3 = Mass(10, 2 * RIGHT.copy())
        mass4 = Mass(2, UP.copy())
        wall1 = Wall(0.5, RIGHT.copy() * 3)

        spring1 = Spring2D(2.0, mass1, mass2, height=0.25, length=16)
        spring2 = Spring2D(0.5, mass2, mass3, height=0.25, length=4)
        spring3 = Spring2D(0.125, mass3, wall1,  height=0.25, length=2)
        spring4 = Spring2D(1, mass2, mass4, height=0.25, length=8)

        self.play(Create(mass1), Create(mass2), Create(mass3), Create(mass4), Create(wall1))
        self.wait()
        self.play(Create(spring1), Create(spring2), Create(spring3), Create(spring4))
        self.wait(2)

        mass1.velocity += LEFT * 0.25

        self.wait(30)

if __name__ == "__main__":
    import os

    os.system("manim -p -ql visual_test.py Spring")