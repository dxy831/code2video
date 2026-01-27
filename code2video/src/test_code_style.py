"""
测试 Manim Code 对象的浅色背景
关键发现：
- formatter_style: 控制语法高亮颜色
- background_config={"fill_color": "#FFF5D6"}: 控制背景颜色
"""
from manim import *

class TestCodeStyles(Scene):
    def construct(self):
        self.camera.background_color = "#FFFDF4"
        
        code_text = """// 二分搜索
int binarySearch(int arr[], int target) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == target) return mid;
    }
    return -1;
}"""
        
        # 测试1: 
        code1 = Code(
            code_string=code_text,
            language="c",
            background="rectangle",
            formatter_style="paraiso-light",
            background_config={
                "fill_color": "#FFF4DB",    # 浅金色背景！
                "stroke_color": "#ffecc1",  # 金色边框
                "stroke_width": 2
            },
            add_line_numbers=False
        )
        code1.scale(0.45).to_edge(LEFT, buff=0.3)
        self.add(code1)
        label1 = Text("浅色背景 ✅", font_size=14, color="#2C1608").next_to(code1, DOWN)
        self.add(label1)
        
        # 测试2:
        code2 = Code(
            code_string=code_text,
            language="c", 
            background="rectangle",
            formatter_style="tango",
            background_config={
                "fill_color": "#fff7e8",    # 浅金色背景！
                "stroke_color": "#FFEECE",  # 金色边框
                "stroke_width": 2
            },
            add_line_numbers=False
        )
        code2.scale(0.45).move_to(ORIGIN)
        self.add(code2)
        label2 = Text("浅金色背景", font_size=14, color="#2C1608").next_to(code2, DOWN)
        self.add(label2)
        
        # 测试3:
        code3 = Code(
        code_string=code_text,
            language="c", 
            background="rectangle",
            formatter_style="trac",
            background_config={
                "fill_color": "#FEF1D2",    # 浅金色背景！
                "stroke_color": "#ffcd68",  # 金色边框
                "stroke_width": 2
            },
            add_line_numbers=False
        )
        code3.scale(0.45).to_edge(RIGHT, buff=0.3)
        self.add(code3)
        label3 = Text("默认深色 ❌", font_size=14, color="#2C1608").next_to(code3, DOWN)
        self.add(label3)
        
        self.wait(3)

# 运行命令: manim -pql test_code_style.py TestCodeStyles
# 可用： paraiso-light 、tango