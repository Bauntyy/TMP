from manim import *
import numpy as np

class EulerFormula_01(Scene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = WHITE

    def construct(self):
        formula_01 = MathTex(
            '\\mathbf{{a^{k} \\over{(a-b)(a-c)}} + {b^{k} \\over{(b-c)(b-a)}}',
            color=BLACK
        )
        formula_01_2 = MathTex(
            '\\mathbf{+ {c^{k} \\over{(c-a)(c-b)}}}}',
            color=BLACK
        )

        # Установка цветов
        formula_01.set_color_by_tex('k', BLUE_D)
        formula_01.set_color_by_tex('a', RED_D)
        formula_01.set_color_by_tex('b', YELLOW_D)
        formula_01.set_color_by_tex('c', GREEN_D)

        formula_01.scale(1.6).shift(UP * 2.5)

        formula_01_2.set_color_by_tex('k', BLUE_D)
        formula_01_2.set_color_by_tex('a', RED_D)
        formula_01_2.set_color_by_tex('b', YELLOW_D)
        formula_01_2.set_color_by_tex('c', GREEN_D)
        formula_01_2[0].set_color(BLACK)
        formula_01_2.scale(1.6).next_to(formula_01, DOWN * 3).align_to(formula_01, LEFT)

        eq_symbol = MathTex('=', color=BLACK).scale(1.4).next_to(formula_01_2, RIGHT * 1.2)

        formula_02_1 = MathTex('0\\, \\, (k=0\\text{ или }1)', color=BLACK) \
            .scale(1.2).next_to(eq_symbol, RIGHT * 2.75).shift(UP * 0.9)
        formula_02_2 = MathTex('1\\, \\, (k=2)', color=BLACK) \
            .scale(1.2).next_to(eq_symbol, RIGHT * 2.75)
        formula_02_3 = MathTex('a+b+c\\, \\, (k=3)', color=BLACK) \
            .scale(1.2).next_to(eq_symbol, RIGHT * 2.75).shift(DOWN * 0.9)

        formula_02_1.set_color_by_tex('k', BLUE_D)
        formula_02_2.set_color_by_tex('k', BLUE_D)
        formula_02_3.set_color_by_tex('k', BLUE_D)
        formula_02_3.set_color_by_tex('a', RED_D)
        formula_02_3.set_color_by_tex('b', YELLOW_D)
        formula_02_3.set_color_by_tex('c', GREEN_D)

        formula_02 = VGroup(formula_02_1, formula_02_2, formula_02_3)
        brace = Brace(formula_02, LEFT, color=BLACK)

        self.play(Write(formula_01))
        self.play(Write(formula_01_2))

        self.wait(0.8)

        self.play(Write(eq_symbol), run_time=0.8)
        self.play(Create(brace), run_time=0.8)
        self.play(Write(formula_02), run_time=2)

        self.wait(10)

class Dot3d(VGroup):

    def __init__(self, loc, size=0.2, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        dot_01 = Dot(loc, color=color).scale(size)
        self.add(dot_01)

        num = 4
        for i in range(1, num):
            dot_i = dot_01.copy().rotate(PI * i/num, axis=UP)
            self.add(dot_i)
        for i in range(1, num):
            dot_i = dot_01.copy().rotate(PI * i/num, axis=RIGHT)
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

        # Создание рёбер (адаптированный список из исходного кода)
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

        # Создание граней (адаптированный список)
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


class EulerFormula_02(Scene):
    def __init__(self):
        super().__init__()
        self.camera.background_color = WHITE

    def construct(self):
        formula = MathTex('V - E + F = 2', color=BLACK) \
            .shift(DOWN * 1.6).scale(1.5)

        formula.set_color_by_tex('V', RED)
        formula.set_color_by_tex('E', BLUE_D)
        formula.set_color_by_tex('F', YELLOW_D)

        graph = Regular_Dodecahedron(
            edge_color=BLACK,
            size=4,
            vertex_color=BLACK
        ).shift(UP * 1.6)

        self.add(graph)
        self.wait()
        self.play(
            Rotate(graph, angle=(270 + 30) * DEGREES, axis=UP),
            run_time=4
        )
        self.wait()
        self.play(Write(formula), run_time=2)
        self.wait(10)


class EulerFormula_03(Scene):
    def __init__(self):
        super().__init__()
        self.camera.background_color = WHITE

    def construct(self):
        R = 2.8
        O_point = UP * 1

        def point_on_circle(theta):
            return np.array([np.cos(theta), np.sin(theta), 0]) * R + O_point

        A = point_on_circle(200 * DEGREES)
        B = point_on_circle(-20 * DEGREES)
        C = point_on_circle(60 * DEGREES)

        a = np.linalg.norm(B - C)
        b = np.linalg.norm(A - C)
        c = np.linalg.norm(A - B)

        I = (a * A + b * B + c * C) / (a + b + c)
        r = (R ** 2 - np.linalg.norm(O_point - I) ** 2) / (2 * R)

        # Создание объектов
        tri_abc = Polygon(A, B, C, color=BLACK, stroke_width=6)
        circle_o = Circle(radius=R, color=BLUE_D, stroke_width=6).move_to(O_point)
        circle_i = Circle(radius=r, color=RED, stroke_width=6).move_to(I)
        OI = DashedLine(O_point, I, color=PINK, stroke_width=4)

        # Точки
        dot_a = Dot(A, color=GREEN_D).scale(1.2)
        dot_b = Dot(B, color=GREEN_D).scale(1.2)
        dot_c = Dot(C, color=GREEN_D).scale(1.2)
        dot_o = Dot(O_point, color=BLUE_D).scale(1.2)
        dot_i = Dot(I, color=RED).scale(1.2)

        # Стрелки
        arrow_R = Arrow(
            O_point,
            point_on_circle(220 * DEGREES),
            buff=0,
            color=BLUE_D,
            stroke_width=4
        )

        arrow_r = Arrow(
            I,
            I + np.array([np.cos(45 * DEGREES), np.sin(45 * DEGREES), 0]) * r * 0.95,
            buff=0.1,
            color=RED,
            stroke_width=4
        )

        # Подписи
        tex_o = MathTex('O', color=BLUE_D).scale(0.8).next_to(O_point, LEFT + UP, buff=0.1)
        tex_i = MathTex('I', color=RED).scale(0.8).next_to(I, RIGHT + DOWN, buff=0.1)
        tex_R = MathTex('R', color=BLUE_D).scale(0.8).next_to(arrow_R.get_end(), RIGHT + UP, buff=0.1)
        tex_r = MathTex('r', color=RED).scale(0.8).next_to(arrow_r.get_end(), LEFT + DOWN, buff=0.1)

        # Формула
        formula = MathTex('OI^2 = R^2 - 2Rr', color=BLACK) \
            .scale(1.6).shift(DOWN * 2.4)

        formula.set_color_by_tex('OI', PINK)
        formula.set_color_by_tex('R', BLUE_D)
        formula.set_color_by_tex('r', RED)

        # Добавление и анимация
        all_objects = [
            tri_abc, circle_o, circle_i, OI,
            dot_a, dot_b, dot_c, dot_i, dot_o,
            arrow_R, arrow_r,
            tex_o, tex_i, tex_R, tex_r
        ]

        for obj in all_objects:
            self.add(obj)

        self.wait(1)
        self.play(Write(formula), run_time=2)
        self.wait(10)


class EulerFormula_04(Scene):
    def __init__(self):
        super().__init__()
        self.camera.background_color = WHITE

    def construct(self):
        formula = MathTex(
            'e^{ix} = \\cos{x} + i\\sin{x}',
            color=BLACK
        ).scale(1.5).shift(DOWN * 1.8)

        formula.set_color_by_tex('i', ORANGE)
        formula.set_color_by_tex('x', BLUE)
        formula.set_color_by_tex('e', GREEN)
        formula.set_color_by_tex('\\sin', YELLOW_D)
        formula.set_color_by_tex('\\cos', YELLOW_D)

        # Координатные оси
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GRAY},
            x_length=6,
            y_length=6
        ).shift(UP * 1.2)

        # Единичная окружность
        circle = Circle(color=RED_D, stroke_width=4).scale(2).shift(UP * 1.2)

        # Точка и линии
        angle = PI / 3  # 60 градусов
        point = np.array([np.cos(angle), np.sin(angle), 0]) * 2 + UP * 1.2

        dot_o = Dot(UP * 1.2, color=GRAY)
        dot_p = Dot(point, color=RED_D)

        radius_line = Line(UP * 1.2, point, color=RED_D, stroke_width=4)
        cos_line = Line(UP * 1.2, point[0] * RIGHT + UP * 1.2, color=YELLOW_D, stroke_width=3)
        sin_line = Line(point[0] * RIGHT + UP * 1.2, point, color=YELLOW_D, stroke_width=3)

        # Подписи
        tex_i = MathTex('i', color=ORANGE).scale(0.8).next_to(3 * UP + UP * 1.2, RIGHT, buff=0.1)
        tex_neg_i = MathTex('-i', color=ORANGE).scale(0.8).next_to(3 * DOWN + UP * 1.2, RIGHT, buff=0.1)
        tex_1 = MathTex('1', color=BLACK).scale(0.8).next_to(3 * RIGHT + UP * 1.2, DOWN, buff=0.1)
        tex_neg_1 = MathTex('-1', color=BLACK).scale(0.8).next_to(3 * LEFT + UP * 1.2, DOWN, buff=0.1)

        tex_cos = MathTex('\\cos x', color=YELLOW_D).scale(0.8) \
            .next_to(cos_line, DOWN, buff=0.1)
        tex_sin = MathTex('\\sin x', color=YELLOW_D).scale(0.8) \
            .next_to(sin_line, RIGHT, buff=0.1)

        # Добавление объектов
        self.add(axes, circle)
        self.add(radius_line, cos_line, sin_line)
        self.add(dot_o, dot_p)
        self.add(tex_i, tex_neg_i, tex_1, tex_neg_1, tex_cos, tex_sin)

        self.wait(1)
        self.play(Write(formula))
        self.wait(10)