"""
Docstring
"""

import numpy as np

from dataclasses import dataclass, field, InitVar
from numpy.typing import NDArray
from manim import *

from ..utils.id_generator import Id_generator

@dataclass
class Mass(Circle):
    id_hash: int = field(init=False, default_factory=Id_generator.get_new_id)
    mass: float
    position: InitVar[NDArray[float]] = field(default=np.array([0.0,0.0,0.0]), init=True)
    velocity: NDArray[float] = field(default=np.array([0.0, 0.0, 0.0]), compare=True, hash=False)
    force: NDArray[float] = field(default=np.array([0.0, 0.0, 0.0]), compare=True, hash=False)
    radius: float = field(default=None)
    label_text: str = field(default=None)
    label_scale_value: float = field(default=0.8)
    fill_opacity: float = field(default=1)
    stroke_width: float = field(default=3)
    fill_color: str = field(default=None)
    sheen_direction: NDArray[float] = field(default=UP)
    sheen_factor: float = field(default=0.5)

    def __hash__(self):
        return self.id_hash

    def __post_init__(self, position):
        def update_position(mobj, dt):
            tmp_position = mobj.get_center()
            mobj.velocity += mobj.force / mobj.mass * dt
            tmp_position += mobj.velocity * dt
            mobj.move_to(tmp_position)
            mobj.force = np.zeros((3,))

        # Remove dependencies on input arrays
        self.velocity = self.velocity.copy()
        self.force = self.force.copy()

        if self.radius is None:
            object.__setattr__(self, "radius", self.mass_to_radius(self.mass))

        if self.fill_color is None:
            object.__setattr__(self, "fill_color", self.mass_to_color(self.mass))

        if self.label_text is None:
            object.__setattr__(self, "label_text", self.mass_to_label_text(self.mass))

        super(Mass, self).__init__(radius=self.radius, color=self.fill_color, fill_opacity=self.fill_opacity,
                                   stroke_width=self.stroke_width, sheen_direction=self.sheen_direction,
                                   sheen_factor=self.sheen_factor)

        self.move_to(position)

        # add label
        if self.label_text:
            self.label = self.get_label()
            self.add(self.label)

        self.add_updater(update_position)

    def get_points_defining_boundary(self):
        return self.points

    def mass_to_radius(self, mass):
        return 0.25 * np.log10(mass)

    def mass_to_color(self, mass):
        colors = [
            GREY_B,
            BLUE_D,
            BLUE_D,
            BLUE_E,
            BLUE_E,
            GREY_D,
            GREY_D,
            BLACK,
        ]
        index = min(int(np.log10(mass)), len(colors) - 1)
        return colors[index]

    def mass_to_label_text(self, mass):
        return "{:,}\\,kg".format(int(mass))

    def get_label(self):
        label = Tex(self.label_text)
        label.scale(self.label_scale_value)
        label.next_to(self, UP, SMALL_BUFF)
        return label