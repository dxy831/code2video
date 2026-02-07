base_class = """
class TeachingScene(Scene):
    def setup_layout(self, title_text, lecture_lines):
        # BASE - 温暖配色方案
        self.camera.background_color = "#FFFDF4"  # 温暖米白色背景
        
        # 大标题 - 必须使用加粗 weight="BOLD"，颜色 #BE8944
        # 使用 Noto Sans SC 字体（跨平台：Linux/Windows/macOS）
        self.title = Text(title_text, font="Noto Sans SC", font_size=28, color="#BE8944", weight="BOLD").to_edge(UP)
        self.add(self.title)

        # Left-side lecture content (bullets with "-")
        # ⚠️ 讲解文字从左上角开始，严禁Y轴居中
        lecture_texts = [Text(line, font="Noto Sans SC", font_size=25, color="#2C1608") for line in lecture_lines]  # 深棕色普通文字
        self.lecture = VGroup(*lecture_texts).arrange(DOWN, aligned_edge=LEFT).scale(0.8)
        self.lecture.next_to(self.title, DOWN, buff=1.0).to_edge(LEFT, buff=0.3)
        self.add(self.lecture) 

        # Define fine-grained animation grid (4x4 grid on right side)
        self.grid = {}
        rows = ["A", "B", "C", "D", "E", "F"]  # Top to bottom
        cols = ["1", "2", "3", "4", "5", "6"]  # Left to right

        for i, row in enumerate(rows):
            for j, col in enumerate(cols):
                x = 0.5 + j * 1
                y = 2.2 - i * 1
                self.grid[f"{row}{col}"] = np.array([x, y, 0])

    def create_code_block(self, code_text, language="python"):
        \"\"\"
        创建标准化的浅色背景代码块
        直接复制以下代码，不要修改任何参数，否则会导致样式不一致！！！
        必须使用 tango 格式化风格，背景颜色必须是浅金色配色方案，且必须有边框。
        
        Args:
            code_text: 代码文本字符串
            language: 编程语言，默认 python
        
        Returns:
            Code 对象
        \"\"\"
        return Code(
            code_string=code_text,  # 使用 code_string 而不是 code
            language=language,
            background="rectangle",  # 🔴 必须有
            formatter_style="tango",  # 🔴 必须是 tango，不能是其他值
            background_config={  # 🔴 必须有，且必须是这个配色
                "fill_color": "#fff7e8",   # 浅金色背景
                "stroke_color": "#e4c8a6", # 金色边框
                "stroke_width": 2
            }
        )
    )

    def place_at_grid(self, mobject, grid_pos, scale_factor=1.0):
        mobject.scale(scale_factor)
        mobject.move_to(self.grid[grid_pos])
        return mobject

    def place_in_area(self, mobject, top_left, bottom_right, scale_factor=1.0):
        tl_pos = self.grid[top_left]
        br_pos = self.grid[bottom_right]
        
        # Calculate center of the area
        center_x = (tl_pos[0] + br_pos[0]) / 2
        center_y = (tl_pos[1] + br_pos[1]) / 2
        center = np.array([center_x, center_y, 0])
        
        mobject.scale(scale_factor)
        mobject.move_to(center)
        return mobject
"""
