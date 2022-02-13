@dataclass
class Wall(Line):
    id_hash : int = field(init=False, default_factory=id_generator.get_new_id)
    height: float = 0.5
    position: typing.NDArray[float] = np.array([0.0, 0.0, 0.0])
    force: typing.NDArray[float] = np.array([0.0, 0.0, 0.0])
    fill_opacity: float = field(default=1)
    stroke_width: float = field(default=3)
    fill_color: str = field(default=None)
    sheen_direciton: typing.NDArray[float] = field(default=UP)
    sheen_factor: float = field(default=0.5)

    def __hash__(self):
        return self.id_hash

    def __post_init__(self):

        super(Wall, self).__init__(start=DOWN, end=UP*self.height, color=self.fill_color,
                                     fill_opacity=self.fill_opacity,
                                     stroke_width=self.stroke_width, sheen_direction=self.sheen_direciton,
                                     sheen_factor=self.sheen_factor)
