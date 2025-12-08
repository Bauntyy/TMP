from manim import *
import numpy as np


class Dot3d(VGroup):
    def __init__(self, loc, size=0.2, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        dot_01 = Dot(loc, color=color).scale(size)
        self.add(dot_01)

        num = 4
        for i in range(1, num):
            dot_i = dot_01.copy().rotate(PI * i / num, axis=UP)
            self.add(dot_i)
        for i in range(1, num):
            dot_i = dot_01.copy().rotate(PI * i / num, axis=RIGHT)
            self.add(dot_i)


class Regular_Dodecahedron(VGroup):
    def __init__(
            self,
            size=3,
            vertex_size=0.2,
            vertex_color=None,
            edge_color=WHITE,
            face_color=YELLOW,
            edge_stroke=3,
            face_opacity=0.25,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.size = size
        self.vertex_size = vertex_size
        self.vertex_color = vertex_color
        self.edge_color = edge_color
        self.face_color = face_color
        self.edge_stroke = edge_stroke
        self.face_opacity = face_opacity

        self.create_vertices()
        self.create_edges()
        self.create_faces()

        self.add(self.faces, self.edges, self.vertices)
        self.scale_to_fit_height(self.size)

    def create_vertices(self):
        phi = (np.sqrt(5) + 1) / 2

        orange_points = np.array([
            [+1, +1, +1],
            [+1, -1, +1],
            [-1, -1, +1],
            [-1, +1, +1],
            [+1, +1, -1],
            [+1, -1, -1],
            [-1, -1, -1],
            [-1, +1, -1],
        ])

        green_points = np.array([
            [0, +phi, +1 / phi],
            [0, -phi, +1 / phi],
            [0, -phi, -1 / phi],
            [0, +phi, -1 / phi],
        ])

        blue_points = np.array([
            [+1 / phi, 0, +phi],
            [+1 / phi, 0, -phi],
            [-1 / phi, 0, -phi],
            [-1 / phi, 0, +phi],
        ])

        red_points = np.array([
            [+phi, +1 / phi, 0],
            [+phi, -1 / phi, 0],
            [-phi, -1 / phi, 0],
            [-phi, +1 / phi, 0],
        ])

        self.O_dots, self.G_dots, self.B_dots, self.R_dots = VGroup(), VGroup(), VGroup(), VGroup()

        for point in orange_points:
            color = ORANGE if self.vertex_color is None else self.vertex_color
            dot = Dot3d(point, color=color, size=self.vertex_size)
            self.O_dots.add(dot)

        for point in green_points:
            color = GREEN if self.vertex_color is None else self.vertex_color
            dot = Dot3d(point, color=color, size=self.vertex_size)
            self.G_dots.add(dot)

        for point in blue_points:
            color = BLUE if self.vertex_color is None else self.vertex_color
            dot = Dot3d(point, color=color, size=self.vertex_size)
            self.B_dots.add(dot)

        for point in red_points:
            color = RED if self.vertex_color is None else self.vertex_color
            dot = Dot3d(point, color=color, size=self.vertex_size)
            self.R_dots.add(dot)

        self.vertices = VGroup(self.O_dots, self.G_dots, self.B_dots, self.R_dots)

    def create_edges(self):
        def create_line(d1, d2):
            return Line(
                d1.get_center(),
                d2.get_center(),
                color=self.edge_color,
                stroke_width=self.edge_stroke
            )

        self.edges = VGroup()
        O, G, B, R = self.O_dots, self.G_dots, self.B_dots, self.R_dots

        edges_to_create = [
            (B[0], B[3]), (B[0], O[0]), (B[0], O[1]), (B[3], O[2]), (B[3], O[3]),
            (O[0], G[0]), (O[1], G[1]), (O[2], G[1]), (O[3], G[0]),
            (O[0], R[0]), (O[1], R[1]), (O[2], R[2]), (O[3], R[3]),
            (G[0], G[3]), (G[1], G[2]), (R[0], R[1]), (R[2], R[3]),
            (R[0], O[4]), (R[1], O[5]), (R[2], O[6]), (R[3], O[7]),
            (G[3], O[4]), (G[2], O[5]), (G[2], O[6]), (G[3], O[7]),
            (O[4], B[1]), (O[5], B[1]), (O[6], B[2]), (O[7], B[2]), (B[2], B[1])
        ]

        for d1, d2 in edges_to_create:
            self.edges.add(create_line(d1, d2))

    def create_faces(self):
        self.faces = VGroup()

        def create_polygon(*dots):
            vertices = [dot.get_center() for dot in dots]
            return Polygon(
                *vertices,
                color=self.edge_color,
                fill_color=self.face_color,
                fill_opacity=self.face_opacity,
                stroke_width=0
            )

        O, G, B, R = self.O_dots, self.G_dots, self.B_dots, self.R_dots

        faces_to_create = [
            (B[0], B[3], O[3], G[0], O[0]),
            (B[0], O[1], G[1], O[2], B[3]),
            (B[0], O[0], R[0], R[1], O[1]),
            (B[3], O[3], R[3], R[2], O[2]),
            (O[3], R[3], O[7], G[3], G[0]),
            (G[0], G[3], O[4], R[0], O[0]),
            (O[1], R[1], O[5], G[2], G[1]),
            (G[2], G[1], O[2], R[2], O[6]),
            (R[2], R[3], O[7], B[2], O[6]),
            (R[1], R[0], O[4], B[1], O[5]),
            (G[2], O[6], B[2], B[1], O[5]),
            (G[3], O[7], B[2], B[1], O[4])
        ]

        for face_dots in faces_to_create:
            self.faces.add(create_polygon(*face_dots))