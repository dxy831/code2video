"""
测试 MathTex 与 Text 混合使用的正确方法
验证提示词中给出的方法是否实际可用
"""

from manim import *

class TestMathTexWithText(Scene):
    def construct(self):
        self.camera.background_color = "#FFFDF4"  # 奶油白背景
        
        title = Text("数学符号混合测试", font="Noto Sans SC", font_size=32, color="#BE8944", weight="BOLD")
        title.to_edge(UP, buff=0.5)
        self.add(title)
        
        # ============ 测试1: 2^7 = 128 > 100 ============
        # 错误写法（会显示方框）
        wrong_text = Text("错误写法: 2⁷ = 128 > 100", font="Noto Sans SC", font_size=24, color="#C84A2B")
        wrong_text.move_to(UP * 2)
        
        # 正确写法1: 纯 MathTex（整个表达式都是数学）
        correct_math = VGroup(
            Text("正确写法1: ", font="Noto Sans SC", font_size=24, color="#478211"),
            MathTex(r"2^7 = 128 > 100", color="#478211").scale(0.9)
        ).arrange(RIGHT, buff=0.2)
        correct_math.move_to(UP * 1)
        
        # 正确写法2: Text + MathTex 混合（中文+数学）
        correct_mixed = VGroup(
            Text("正确写法2: 因为 ", font="Noto Sans SC", font_size=24, color="#478211"),
            MathTex(r"2^7", color="#9B6D0B").scale(0.9),
            Text(" = 128 > 100", font="Noto Sans SC", font_size=24, color="#478211"),
        ).arrange(RIGHT, buff=0.1)
        correct_mixed.move_to(ORIGIN)
        
        # 正确写法3: 复杂表达式 O(log₂n)
        correct_log = VGroup(
            Text("时间复杂度是 ", font="Noto Sans SC", font_size=24, color="#2C1608"),
            MathTex(r"O(\log_2 n)", color="#9B6D0B").scale(0.9),
        ).arrange(RIGHT, buff=0.1)
        correct_log.move_to(DOWN * 1)
        
        # 正确写法4: 乘号
        correct_times = VGroup(
            Text("100 ", font="Noto Sans SC", font_size=24, color="#2C1608"),
            MathTex(r"\times", color="#2C1608").scale(0.9),
            Text(" 10 = 1000", font="Noto Sans SC", font_size=24, color="#2C1608"),
        ).arrange(RIGHT, buff=0.1)
        correct_times.move_to(DOWN * 2)
        
        # 显示所有测试
        self.play(FadeIn(wrong_text))
        self.wait(1)
        self.play(FadeIn(correct_math))
        self.wait(1)
        self.play(FadeIn(correct_mixed))
        self.wait(1)
        self.play(FadeIn(correct_log))
        self.wait(1)
        self.play(FadeIn(correct_times))
        self.wait(2)


if __name__ == "__main__":
    # 运行命令: manim -pql test_mathtex.py TestMathTexWithText
    pass
