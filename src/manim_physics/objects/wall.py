from dataclasses import dataclass, field, InitVar
from numpy import array
from numpy.typing import NDArray

from manim import *

from ..utils.id_generator import Id_generator

@dataclass
class Wall(Line):
    id_hash : int = field(init=False, default_factory=Id_generator.get_new_id)
    height: float = 0.5
    position: InitVar[NDArray[float]] = field(default=np.array([0.0, 0.0, 0.0]), init=True)
    force: NDArray[float] = np.array([0.0, 0.0, 0.0])
    fill_opacity: float = field(default=1)
    stroke_width: float = field(default=3)
    fill_color: str = field(default=None)
    sheen_direction: NDArray[float] = field(default=UP)
    sheen_factor: float = field(default=0.5)

    def __hash__(self):
        return self.id_hash


    def __post_init__(self, position):

        super(Wall, self).__init__(start=DOWN * self.height + position, end=UP*self.height + position, color=self.fill_color,
                                     fill_opacity=self.fill_opacity,
                                     stroke_width=self.stroke_width, sheen_direction=self.sheen_direction,
                                     sheen_factor=self.sheen_factor)
