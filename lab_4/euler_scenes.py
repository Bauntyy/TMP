from manim import *
import numpy as np
from geometry_classes import Dot3d, Regular_Dodecahedron

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
