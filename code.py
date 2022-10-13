from manim import *

#----------------------------------------------------------------------------------# Code to create a simple circle
class Draw_Circle(Scene):
    def construct(self):
        circle = Circle()

        self.wait()
        self.play(Create(circle))

#----------------------------------------------------------------------------------# Code to create the vectore field animation
class ContinuousMotion(Scene):
    def construct(self):
        func = lambda pos: np.cos(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=40)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)

#----------------------------------------------------------------------------------# Code to create a Linear Transformation scene
class LTScene(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
        )

    def construct(self):
        matrix = [[-1, 1], [0, 1]]
        self.apply_matrix(matrix)
        self.wait()

#----------------------------------------------------------------------------------# Code to create the Bohr atomic model

class Bohr(Scene):
    def construct(self):
        
        red_circle = Circle().scale(0.2).set_color(RED_A).set_fill(RED_A, opacity = 1)
        blue_circle = Dot().set_color(BLUE_B)
        positive = Text("+").scale(0.8)
        negative = Text("-").scale(0.5)
        
        nucleus = VGroup(red_circle, positive)
        electron = VGroup(blue_circle, negative)

        

        orbit_1 = Circle(stroke_width = 0.5).scale(1).set_color(WHITE)
        orbit_2 = Circle(stroke_width = 0.5).scale(1.5).set_color(WHITE)
        orbit_3 = Circle(stroke_width = 0.5).scale(2).set_color(LIGHT_GREY)
        orbit_4 = Circle(stroke_width = 0.5).scale(2.5).set_color(GREY)
        orbit_5 = Circle(stroke_width = 0.5).scale(3).set_color(DARK_GREY)

          
        
        electron_1 = electron.copy().move_to(UP)
        electron_2 = electron.copy().move_to(LEFT*1.5)
        electron_3 = electron.copy().move_to(DOWN*2)
        electron_4 = electron.copy().move_to(RIGHT*2.5)
        electron_5 = electron.copy().move_to(UP*3)

        orbits = [orbit_1, orbit_2, orbit_3, orbit_4, orbit_5]
        electrons = [electron_1, electron_2, electron_3, electron_4, electron_5]
        index = [1,2,3,4,5]

        self.wait()
        self.play(Write(nucleus))
        orbit_animation = [Write(orbit) for orbit in orbits]
        self.play(*orbit_animation)
        electron_animation = [Write(elect) for elect in electrons]
        self.play(*electron_animation)
        animations = [Rotate(elec, angle = (220*i)*DEGREES , about_point= ORIGIN) for elec, i in zip(electrons, index)]
        self.wait()
        self.play(*animations, run_time = 10)

        
        electron_2_trans = electron.copy().move_to(LEFT*1.5)
        electron_3_trans = electron.copy().move_to(LEFT*2)
        electron_4_trans = electron.copy().move_to(LEFT*2.5)
        electron_5_trans = electron.copy().move_to(LEFT*3)
        
        self.play(FadeOut(electron_1, electron_2, electron_3, electron_4, electron_5))
        self.wait()
        self.play(Write(electron_3_trans))
        

        dr = 0.02
        red_light = VGroup(*[Annulus(inner_radius=rings*dr, outer_radius=(rings+1)*dr, fill_opacity=1-rings*0.2, color=RED) for rings in range(5)]).move_to(electron_3_trans)
        blue_light = VGroup(*[Annulus(inner_radius=rings*dr, outer_radius=(rings+1)*dr, fill_opacity=1-rings*0.2, color=BLUE) for rings in range(5)]).move_to(electron_4_trans)
        purple_light = VGroup(*[Annulus(inner_radius=rings*dr, outer_radius=(rings+1)*dr, fill_opacity=1-rings*0.2, color=PURPLE) for rings in range(5)]).move_to(electron_5_trans)
        red_text = Text(r"656 nm", color = RED).scale(0.4)
        blue_text = Text(r"486 nm", color = BLUE).scale(0.4)
        purple_text = Text(r"434 nm", color = PURPLE).scale(0.4)

        self.wait()
        self.play(Transform(electron_3_trans, electron_2_trans), red_light.animate.shift(LEFT*6), Write(red_light.copy().move_to([-6,-2,0])), Write(red_text.move_to([-5,-2,0])))
        self.wait()
        self.play(FadeOut(electron_3_trans))
        self.wait()
        self.play(Write(electron_4_trans))
        self.wait()
        self.play(Transform(electron_4_trans, electron_2_trans), blue_light.animate.shift(LEFT*6.5), Write(blue_light.copy().move_to([-6,-2.5,0])), Write(blue_text.move_to([-5,-2.5,0])))
        self.wait()
        self.play(FadeOut(electron_4_trans))
        self.wait()
        self.play(Write(electron_5_trans))
        self.wait()
        self.play(Transform(electron_5_trans, electron_2_trans), purple_light.animate.shift(LEFT*7), Write(purple_light.copy().move_to([-6,-3,0])), Write(purple_text.move_to([-5,-3,0])))
        self.wait(3)

#---------------------------------------------------------------------------------------------# Code to create the Momentum Conservation Law scene

class Box(Rectangle):
    CONFIG = {
        "width": 1,
        "height":0.5,
        "fill_color": BLUE,
        "fill_opacity": 1,
        "color": BLUE 
    }

    def __init__(self,  **kwargs):
        Rectangle.__init__(self, **kwargs)
        self.velocity = 2

    def get_right_edge(self):
        return self.get_center()[0] + (self.width / 2)

    def get_left_edge(self):
        return self.get_center()[0] - (self.width / 2)


class Momentum(Scene):
    def construct(self):
        
        fixer = Dot().shift(UP*9)
        self.add(fixer)
        obj_1 = Box(color = BLUE, fill_opacity = 1).shift(RIGHT*3).scale(0.5)
        obj_2 = Box(color = RED, fill_opacity = 1).shift(LEFT*3).scale(0.5)
        obj_2.velocity = 3
              
        mass1 = MathTex("m_2").move_to(obj_1).scale(0.8)
        mass1.add_updater(lambda mob: mob.move_to(obj_1))
        mass2 = MathTex("m_1").move_to(obj_2).scale(0.8)
        mass2.add_updater(lambda mob: mob.move_to(obj_2))
        Baseline = Line([-7,-0.5,0],[8,-0.5,0])
        wall = Line([-7,-0.5,0],[-7,4,0])

        def collision(obj_1, obj_2):
            if obj_1.get_left_edge() < obj_2.get_right_edge():
                obj_1.velocity = -0.5
                obj_2.velocity = -2
            if obj_2.get_right_edge() < -5:
                obj_2.velocity = 2

        def update_obj1(obj_1, dt):
            obj_1.shift(LEFT*obj_1.velocity * dt)
            collision(obj_1, obj_2)
        
        def update_obj2(obj_2, dt):
            obj_2.shift(RIGHT*obj_2.velocity * dt)
            collision(obj_1, obj_2)

        mom_eq = MathTex(r"m_1",r"\vec{v_1}","+","m_2",r"\vec{v_2}","=","m_1",r"\vec{v_1}'","+","m_2",r"\vec{v_2}'").shift(UP*2)
        mom_eq.set_color_by_tex("m_1", RED)
        mom_eq.set_color_by_tex("m_2", BLUE)
        mom_eq.set_color_by_tex(r"\vec{v_1}", YELLOW)
        mom_eq.set_color_by_tex(r"\vec{v_1} '", YELLOW)
        mom_eq.set_color_by_tex(r"\vec{v_2}", GREEN)
        mom_eq.set_color_by_tex(r"\vec{v_2} '", GREEN)

        title = Tex("Conservation of Momentum").scale(2).shift(DOWN*2)
        
        arrow1before = Arrow([0,0,0],[1,0,0]).next_to(obj_2, RIGHT, buff=0)
        v1 = MathTex(r"\vec{v_1}", color = YELLOW).next_to(arrow1before, UP*0.5).scale(0.5)
        arrow2before = Arrow([0,0,0],[-1,0,0]).next_to(obj_1, LEFT, buff=0)
        v2 = MathTex(r"\vec{v_2}", color = GREEN).next_to(arrow2before, UP*0.5).scale(0.5)

        arrow1after = Arrow([3,0,0],[4,0,0], buff = 0)
        v1_after = MathTex(r"\vec{v_2}'", color = GREEN).next_to(arrow1after, UP*0.5).scale(0.5)
        arrow2after = Arrow([0,0,0],[-1,0,0]).next_to(obj_2, LEFT, buff=0)
        v2_after = MathTex(r"\vec{v_1}'", color = YELLOW).next_to(arrow2after, UP*0.5).scale(0.5)

        pause_bar = Rectangle(width = 0.3, height = 1, fill_opacity = 1)
        pause_bar2 = pause_bar.copy().next_to(pause_bar, RIGHT, buff = 0.5)
        pause_obj = VGroup(pause_bar, pause_bar2).scale(1).shift(-3)

        resume = Triangle(fill_opacity = 1, color = TEAL).rotate(30*DEGREES).shift(-3).scale(0.6)
        
        self.wait()
        self.play(Write(Baseline), Write(wall))
        self.play(FadeIn(obj_1, obj_2, mass1, mass2))
        self.wait()
        self.play(FadeIn(arrow1before, arrow2before, v1, v2))
        self.wait(3)
        self.play(FadeOut(arrow1before, arrow2before, v1, v2))
        obj_1.add_updater(update_obj1)
        obj_2.add_updater(update_obj2)
        self.wait(2)
        obj_1.remove_updater(update_obj1)
        obj_2.remove_updater(update_obj2)
        self.play(FadeIn(arrow1after, arrow2after, v1_after, v2_after))
        self.wait(3)
        self.play(FadeOut(arrow1after, arrow2after, v1_after, v2_after))
        self.wait()
        obj_1.add_updater(update_obj1)
        obj_2.add_updater(update_obj2)
        self.wait(3)
        obj_1.remove_updater(update_obj1)
        obj_2.remove_updater(update_obj2)
        self.play(Write(mom_eq))
        self.wait(2)
        self.play(FadeIn(title))
        self.wait(3)

#----------------------------------------------------------------------------------#