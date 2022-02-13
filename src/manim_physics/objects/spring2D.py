from dataclasses import dataclass, field


@dataclass
class Spring(Line):
    """
    Represents a spring like object that needs two masses to attach to (can also be a wall).
    Setting the spring_constant behavior changes the forces created.
    Force = k * (x_rest - x), which is added to the force variable of the attached masses.
    """
    id_hash: int = field(init=False, default_factory=id_generator.get_new_id)
    rest_width: float = field(init=False, default=None)
    spring_constant: float
    start_mass: Union[Mass, Wall]
    end_mass: Union[Mass, Wall]
    length: int = 2
    height: float = 2
    label_text: str = field(default=None)
    label_scale_value: float = field(default=0.8)
    fill_opacity: float = field(default=1)
    stroke_width: float = field(default=3)
    fill_color: str = field(default=None)
    sheen_direciton: typing.NDArray[float] = field(default=UP)
    sheen_factor: float = field(default=0.5)

    def __post_init__(self):
        """ does the non-trivial initialization, is called after the init of the dataclass"""

        def update_stretch(mobj, dt):
            """
            This is the updater that calculates the stretch of the spring, modifies the geometries and move it to
            the right place. It also calculates the creates forces and adds them to the attached masses force variable
            """

            # scaling depends on the starting and end point of the spring
            r1, r2 = mobj.get_end_points()

            # get position vectors
            end_mass_pos = self.end_mass.get_center()
            start_mass_pos = self.start_mass.get_center()

            difference_mass_vec = (end_mass_pos - start_mass_pos)
            unit_spring_vec = difference_mass_vec / np.linalg.norm(difference_mass_vec)
            difference_spring_vec = r2 - r1

            # avoid division by 0 and stretch geometry
            if abs(difference_spring_vec[0]) > 0.0000001:
                mobj.stretch(difference_mass_vec[0] / difference_spring_vec[0], dim=0)
                mobj.label.stretch(difference_spring_vec[0] / difference_mass_vec[0],
                                   dim=0)  # invert stretching on label
            if abs(difference_spring_vec[1]) > 0.0000001:
                mobj.stretch(difference_mass_vec[1] / difference_spring_vec[1], dim=1)
                mobj.label.stretch(difference_spring_vec[1] / difference_mass_vec[1],
                                   dim=1)  # invert stretching on label

            # calculate old vs new positions centers and move spring accordingly
            mobj.shift(((end_mass_pos + start_mass_pos) * 0.5 - (r1 + r2) * 0.5))

            # calculate forces
            self.start_mass.force += self.spring_constant * (
                    self.rest_width - np.linalg.norm(difference_mass_vec)) * -unit_spring_vec
            self.end_mass.force += self.spring_constant * (
                    self.rest_width - np.linalg.norm(difference_mass_vec)) * unit_spring_vec

        # create spring

        # get mass positions
        start_mass_center = self.start_mass.get_center()
        end_mass_center = self.end_mass.get_center()

        # unit vector for the direction of the spring
        direction_vec = (end_mass_center - start_mass_center)
        direction_vec /= np.linalg.norm(direction_vec)

        # unit normal vector orthogonal to direction vector
        normal_vec = np.array([direction_vec[1], - direction_vec[0], 0])

        section_length = (np.linalg.norm(end_mass_center - start_mass_center) / (
                self.length + 1)) * 0.5

        # init wiggly line directions
        horizontal = section_length * direction_vec
        up_right = normal_vec * self.height + horizontal
        down_right = -normal_vec * self.height + horizontal
        halve_height = 1 - np.absolute(normal_vec) * 0.5  # for starting and ending orthogonal

        # calculate and save rest_width for force calculation
        self.rest_width = np.linalg.norm(end_mass_center - start_mass_center)

        # draw spring lines
        # first horizontal line
        cur_start = start_mass_center
        cur_end = start_mass_center + horizontal
        super(Spring, self).__init__(start=cur_start, end=cur_end, color=self.fill_color,
                                     fill_opacity=self.fill_opacity,
                                     stroke_width=self.stroke_width, sheen_direction=self.sheen_direciton,
                                     sheen_factor=self.sheen_factor)

        # wiggly up down lines
        for j in range(2 * self.length):
            cur_start = cur_end.copy()
            if j % 2 == 0:
                if j == 0:
                    cur_end += up_right * halve_height
                else:
                    cur_end += up_right
            else:
                if j == 2 * self.length - 1:
                    cur_end += down_right * halve_height
                else:
                    cur_end += down_right

            self.add(Line(cur_start, cur_end, color=self.fill_color, fill_opacity=self.fill_opacity,
                          stroke_width=self.stroke_width, sheen_direction=self.sheen_direciton,
                          sheen_factor=self.sheen_factor))

        # last horizontal line
        self.end_line = Line(cur_end, cur_end + horizontal, color=self.fill_color, fill_opacity=self.fill_opacity,
                             stroke_width=self.stroke_width, sheen_direction=self.sheen_direciton,
                             sheen_factor=self.sheen_factor)
        self.add(self.end_line)

        self.label = self.get_label()
        self.add(self.label)
        self.add_updater(update_stretch)

    def __hash__(self):
        """ Simple hash function based on the assigned hash"""
        return self.id_hash

    def get_points_defining_boundary(self):
        """ Returns points of the start and end line"""
        return np.concatenate((self.points, self.end_line.points))

    def get_end_points(self):
        """ Returns the start and end point of the spring"""
        return self.points[0], self.end_line.points[-1]

    def get_label(self):
        """ Creates and places a label"""
        label = Tex(self.label_text)
        label.scale(self.label_scale_value)
        label.next_to(self, UP, SMALL_BUFF)
        return label