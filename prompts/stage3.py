import os
from typing import Optional
from .user_profile import UserProfile, get_default_profile


def get_prompt3_code(
    regenerate_note: str,
    section,
    base_class: str,
    user_profile: Optional[UserProfile] = None,
    estimated_duration: Optional[int] = None,
    solution_code: Optional[str] = None
):
    """
    生成Manim代码的提示词
    
    Args:
        regenerate_note: 重新生成的注意事项
        section: 章节信息对象
        base_class: 基类代码
        user_profile: 用户配置，可选
        estimated_duration: 该章节的预计时长（秒），可选
        solution_code: 用户提供的标准答案代码（不可修改），可选
    
    Returns:
        完整的提示词字符串
    """
    # 如果没有提供用户配置，使用默认配置
    if user_profile is None:
        user_profile = get_default_profile()
    
    # 获取 AI 智能生成的用户画像提示词
    profile_prompt = user_profile.get_stage3_prompt()
    target_language = user_profile.get_language()
    
    # 生成时长指导说明
    duration_guidance = ""
    if estimated_duration:
        duration_guidance = f"""
    ### 时长控制要求
    - **目标时长**: 本章节预计时长为 **{estimated_duration} 秒**
    - **节奏分配建议**:
        - 每句旁白约 3-5 秒（共 {len(section.lecture_lines)} 句，约 {len(section.lecture_lines) * 4} 秒）
        - 剩余 {max(0, estimated_duration - len(section.lecture_lines) * 4)} 秒用于动画演示和停顿
    - **wait() 使用指南**:
        - 简单动画后：`self.wait(0.5)` 到 `self.wait(1)`
        - 重要概念展示后：`self.wait(1.5)` 到 `self.wait(2)`
        - 章节结束前：`self.wait(2)` 到 `self.wait(3)`
    - **⚠️ 必须严格遵守**: 确保动画总时长接近目标时长 **{estimated_duration} 秒**，严禁过短！
"""
    
    # 生成标准答案代码提示词片段
    solution_code_prompt = ""
    if solution_code:
        solution_code_prompt = f"""
    ## 🔴🔴🔴 标准答案代码（严禁修改，必须原封不动使用！）🔴🔴🔴
    
    **以下是用户提供的标准答案代码，在视频中展示代码时，必须使用这段代码原文，严禁修改、重写、简化或省略任何部分，一个字都不能改！**
    
    ```{target_language.lower()}
{solution_code}
    ```
    
    **当需要在 Manim 中展示代码块时，必须使用上述标准答案代码的原文内容传入 `self.create_code_block()`。**
"""
    
    return f"""
    你是一位精通 Manim 的 Python 专家。请编写代码生成一个**讲解编程题目代码答案**的视频片段。

    {regenerate_note}
    {duration_guidance}

    {profile_prompt}
    
    {solution_code_prompt}

    ## 🔴🔴🔴 关键规则摘要（必须首先阅读！）🔴🔴🔴
    
    **在生成任何代码之前，请确保理解并遵守以下最重要的规则：**
    
    ### 规则 1：数学公式和特殊符号必须用 MathTex
    
    **🔴 以下内容必须使用 MathTex，严禁使用 Text()：**
    - 所有数学公式（如 `O(log n)`, `n²`, `2^7`等）
    - 比较表达式（如 `5 > 3`, `mid = 5`等）
    - **勾号 ✓ 和叉号 ✗ / ×**（Text 无法显示！）
    
    ```python
    # ✅ 正确：数学表达式用 MathTex
    MathTex(r"O(\log_2 n)", color="#9B6D0B").scale(0.8)
    MathTex(r"2^7 = 128", color="#9B6D0B").scale(0.8)
    
    # ✅ 正确：勾和叉必须用 MathTex
    correct_mark = MathTex(r"\checkmark", color="#478211").scale(1.2)  # 绿色勾 ✓
    wrong_mark = MathTex(r"\times", color="#C84A2B").scale(1.2)        # 红色叉 ✗
    
    # ❌ 错误：用 Text 显示会变成方框！
    Text("O(log₂n)")  # ❌ 会显示方框
    Text("✓")         # ❌ 会显示方框
    Text("✗")         # ❌ 会显示方框
    Text("×")         # ❌ 会显示方框
    ```
    
    ### 🔴🔴🔴 规则 1.1：勾号和叉号的唯一正确写法（违反此规则 = 代码无法渲染 = 生成失败）🔴🔴🔴
    
    **这是最容易犯错的地方！AI 经常错误地使用 Text("✓") 或 Text("✗")！**
    
    **✅ 唯一正确的写法（必须完全按照这个格式）：**
    ```python
    # 绿色勾号 ✓ - 表示正确
    correct_mark = MathTex(r"\\checkmark", color="#478211").scale(1.2)
    
    # 红色叉号 ✗ - 表示错误 
    wrong_mark = MathTex(r"\\times", color="#C84A2B").scale(1.2)
    ```
    
    **❌ 以下写法全部是错误的（会显示方框或乱码）：**
    ```python
    # ❌ 错误写法 1：直接在 Text 中使用 Unicode 符号
    Text("✗")           # ❌ 显示方框
    Text("×")           # ❌ 显示方框
    
    # ❌ 错误写法 2：在注释中写"勾"或"叉"然后用 Text
    # 红叉表示不需要交换
    wrong_mark = Text("✗", font="Noto Sans SC", font_size=28, color="#C84A2B")  # ❌ 错误！
    ```
    
    **🔍 自检：如果你的代码中出现以下任何内容，必须改为 MathTex：**
    - `Text("✓"` → 改为 `MathTex(r"\\checkmark"`
    - `Text("✗"` → 改为 `MathTex(r"\\times"`
    - `Text("×"` → 改为 `MathTex(r"\\times"`
    - `Text("√"` → 改为 `MathTex(r"\\checkmark"`
    
    ### 规则 2：代码块必须使用 self.create_code_block()
    
    **🔴 严禁手动创建 Code 对象！必须使用基类提供的 `self.create_code_block()` 方法！**
    
    ```python
    # ✅ 正确：使用 self.create_code_block() 创建代码块
    code_obj = self.create_code_block(code_text, language="{target_language.lower()}")
    code_obj.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
    
    # ❌ 错误：手动创建 Code 对象（容易遗漏参数导致深色背景）
    Code(code_string=code_text, language="python")  # ❌ 会是深色背景
    ```
    
    **`create_code_block()` 已经内置了正确的配置：**
    - `formatter_style="tango"` - tango 语法高亮主题
    - `background="rectangle"` - 矩形背景
    - `background_config` - 浅金色背景 + 金色边框
    
    ### 规则 3：元素位置边界限制（严禁出框！）
    
    **屏幕安全区域（Manim 坐标系）：**
    - **X 轴范围**: [-7.0, 7.0]（左右边界）
    - **Y 轴范围**: [-4.0, 4.0]（上下边界）
    
    **左侧区域（代码+讲解）：**
    - X ∈ [-7.0, 0]
    - 代码块：`to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)`
    - 讲解文字：`to_edge(LEFT, buff=0.3)`，高度限制 2.5
    
    **右侧区域（动画演示）：**
    - X ∈ [0.3, 6.5]，Y ∈ [-3.5, 3.0]
    - 中心点：`RIGHT_CENTER = [3.5, -0.5, 0]`
    - 最大尺寸：宽 6.0，高 5.5
    
    ```python
    # ✅ 正确：创建元素后检查边界
    obj.move_to(RIGHT_CENTER)
    if obj.width > 6.0: obj.scale_to_fit_width(6.0)
    if obj.height > 5.5: obj.scale_to_fit_height(5.5)
    
    # 检查是否超出边界
    if obj.get_right()[0] > 6.5:
        obj.shift(LEFT * (obj.get_right()[0] - 6.5 + 0.2))
    if obj.get_bottom()[1] < -3.5:
        obj.shift(UP * (-3.5 - obj.get_bottom()[1] + 0.2))
    if obj.get_top()[1] > 3.0:
        obj.shift(DOWN * (obj.get_top()[1] - 3.0 + 0.2))
    ```
    
    **❌ 常见错误：**
    - 数组/表格太长超出右边界
    - 文字/代码块太多超出下边界
    - 动画元素与标题重叠（超出上边界 Y=3.0）
    
    ### 规则 4：讲解文字必须使用 font_size=20
    
    **🔴 左侧讲解文字的字体大小必须固定为 20！**
    
    ```python
    # ✅ 正确：讲解文字必须使用 font_size=20
    new_lecture_texts = [
        Text(line, font="Noto Sans SC", font_size=20, color="#2C1608") 
        for line in new_lecture_lines
    ]
    new_lecture = VGroup(*new_lecture_texts).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    new_lecture.align_to(lecture_pos, UL)          
    ```

    **字体大小规范：**
    | 元素类型 | font_size | 说明 |
    |---------|-----------|------|
    | 大标题 | 28 | 顶部标题，加粗 |
    | **讲解文字** | **20** | **左侧讲解区域，必须固定** |
    
    ### 规则 5：construct() 开头必须调用 setup_layout()
    
    **🔴🔴🔴 严禁跳过 setup_layout()！这是设置背景色的关键！🔴🔴🔴**
    
    `setup_layout()` 方法会设置奶油白背景色 `#FFFDF4`，如果不调用，背景会是黑色！
    
    ```python
    # ✅ 正确：construct() 第一行必须调用 setup_layout()
    class MyScene(TeachingScene):
        def construct(self):
            # 🔴 第一行必须调用 setup_layout()！
            self.setup_layout("标题文字", ["讲解文字1", "讲解文字2"])
            
            # 然后再创建其他元素...
    
    # ❌ 错误：不调用 setup_layout() 会导致黑色背景！
    class MyScene(TeachingScene):
        def construct(self):
            # ❌ 直接创建元素，没有调用 setup_layout()
            title = Text("标题", ...)  # 背景是黑色！
    ```

    ---

    ### 🔴 思路分析章节的特殊要求 🔴
    如果当前章节属于**思路分析**（标题中包含"思路"、"暴力"、"优化"、"核心思想"等关键词），必须遵守：
    - **动画必须细致**：每一步推理都要有对应的可视化动画，不能只用文字讲解
    - **严禁跳步**：不能突然跳到结论，必须展示完整的思考过程
    - **必须用具体例子**：用数组、表格等具体数据演示思路，先跑例子再总结规律
    - **核心三问都要体现在动画中**：
      1. "怎么想到的" → 用动画高亮题目关键条件，展示推理链
      2. "具体怎么做" → 用具体数据逐步演示算法流程
      3. "为什么能解决" → 用动画对比说明正确性
    - **讲解文字必须连贯**：每批 lecture_lines 之间要有逻辑衔接，前因后果清晰
    - **wait() 要充足**：重要推理步骤后 `self.wait(2)` 以上，给观众思考时间

    ### 核心任务：通用算法可视化
    不要硬编码特定的形状，而是根据算法逻辑选择最合适的 Manim 对象。

    ### 1. 动态布局系统
    **【重要】左侧三层垂直布局，严禁重叠：**
    ```python
    # 左侧垂直布局 (从上到下):
    # Layer 1: 标题 title -> to_edge(UP, buff=0.2)
    # Layer 2: 讲解文字 lecture -> 标题下方, 高度限制 2.5 单位
    # Layer 3: 代码 code_obj -> to_edge(DOWN, buff=0.2), 高度限制 3.5 单位
    # 左侧区域: X ∈ [-7.0, 0], 右侧区域: X ∈ [0.3, 6.5]

    # === 布局模板 ===
    LEFT_MAX_WIDTH = 6.5  # 左侧元素最大宽度，防止与右侧重叠
    
    title.to_edge(UP, buff=0.2)
    # ⚠️ 讲解文字从左上角开始，严禁Y轴居中
    self.lecture.next_to(title, DOWN, buff=1.0).to_edge(LEFT, buff=0.3)
    
    if self.lecture.height > 2.5:
        self.lecture.scale_to_fit_height(2.5)
    if self.lecture.width > LEFT_MAX_WIDTH:
        self.lecture.scale_to_fit_width(LEFT_MAX_WIDTH)
    
    code_obj.to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.3)
    if code_obj.height > 3.5:
        code_obj.scale_to_fit_height(3.5)
    if code_obj.width > LEFT_MAX_WIDTH:
        code_obj.scale_to_fit_width(LEFT_MAX_WIDTH)
    
    # 确保讲解与代码不重叠
    if self.lecture.get_bottom()[1] < code_obj.get_top()[1] + 0.3:
        code_obj.scale(0.85)
        code_obj.to_edge(DOWN, buff=0.3)
    ```

    **【⚠️ 讲解文字分批显示 - 硬性规则】**
    - **每批最多4行**：屏幕上同时显示的讲解文字行数 **≤4**，严禁超过
    - **按语义分组**：优先按语义完整性分组（如3+3而非4+2），但单组不超过4行
    - **左上对齐**：讲解文字必须 `.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.3)`，从**左上角**开始，**严禁Y轴居中**
    - **位置固定**：首批出现时记录 `lecture_pos = self.lecture.get_corner(UL)`，后续批次用 `.align_to(lecture_pos, UL)` 保持左上对齐
    - **切换方式**：当前批次讲完 → `FadeOut` + `self.remove()` → 新批次在**原位置左上对齐**显示
    - **示例**：7行文字 → 按语义分为[1-3行] + [4-7行]，或[1-4行] + [5-7行]

    **【关键】右侧动画区域（严禁出框，必须在标题下方）：**
    ```python
    # 右侧区域: 中心(3.5, -0.5), 最大宽6.0/高5.5
    # ⚠️ Y范围: [-3.5, 3.0]，上边界必须在标题下方（标题在 Y≈3.5）
    RIGHT_CENTER = np.array([3.5, -0.5, 0])  # 中心点下移，避免与标题重叠
    RIGHT_TOP_Y = 3.0    # 右侧区域上边界（在标题下方）
    RIGHT_BOTTOM_Y = -3.5  # 右侧区域下边界
    
    # 所有右侧元素：先 move_to(RIGHT_CENTER)，再检查尺寸和边界
    if obj.width > 6.0: obj.scale_to_fit_width(6.0)
    if obj.height > 5.5: obj.scale_to_fit_height(5.5)
    
    # ⚠️ 检查上下边界
    if obj.get_top()[1] > RIGHT_TOP_Y:
        obj.shift(DOWN * (obj.get_top()[1] - RIGHT_TOP_Y + 0.2))
    if obj.get_bottom()[1] < RIGHT_BOTTOM_Y:
        obj.shift(UP * (RIGHT_BOTTOM_Y - obj.get_bottom()[1] + 0.2))
    ```

    **【🚨🚨🚨 代码展示 - 必须使用 self.create_code_block() 🚨🚨🚨】**
    
    ⚠️ **严禁用 Text() 显示代码！必须使用基类的 `self.create_code_block()` 方法！**
    
    ```python
    # ✅✅✅ 唯一正确的写法 ✅✅✅
    code_text = \"\"\"# {target_language} 示例
def algo(data):
    # 核心逻辑
    pass\"\"\"
    code_obj = self.create_code_block(code_text, language="{target_language.lower()}")
    code_obj.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
    self.play(Create(code_obj))
    
    # ❌ 错误：手动创建 Code 对象
    Code(code_string=code_text, language="python")  # ❌ 容易遗漏参数
    ```
    
    **`create_code_block()` 已内置正确配置：**
    - `formatter_style="tango"` - tango 语法高亮
    - `background="rectangle"` - 矩形背景
    - `background_config` - 浅金色背景 #fff7e8 + 金色边框 #e4c8a6
    
    **【代码注释规则 - 必须使用中文】**
    - **代码注释必须全部使用中文**，方便观众理解

    **【代码高亮框精确定位】使用 code_obj[2] 访问代码行 VGroup：**
    ```python
    code_lines = code_obj[2]
    highlight = SurroundingRectangle(code_lines[0], color=YELLOW, buff=0.05)
    self.play(Create(highlight))
    
    # ✅ 移动高亮框 (使用 Transform)
    new_highlight = SurroundingRectangle(code_lines[2], color=YELLOW, buff=0.05)
    self.play(Transform(highlight, new_highlight))
    ```

    ### 2. 交互与逻辑表现
    - **代码高亮**: 使用 `SurroundingRectangle` 精确框选，禁止用 `Indicate` 高亮代码块
    - **呼吸感时序**: 文字高亮结束后必须 `self.wait(0.5)`，先左上文字→停顿→再右侧动画
    - **逻辑外显化**: 条件判断显示 `MathTex("5 > 3")`，成立变绿/不成立变红
    - **递归**: 在屏幕一角维护 Stack VGroup，每层递归 add 矩形，返回时 remove

    ### 3. 数据结构映射
    - **Array/DP Table**: `VGroup` of `Square`，必须标 Index
    - **Tree/Graph**: `Graph` 类或 `Circle` + `Line`
    - **Pointer**: `Arrow` 指向当前操作对象
    - 禁止 3D 场景，保持 2D 清晰图解

    ### 任务输入
    - 标题: {section.title}
    - 脚本: {section.lecture_lines}
    - 动画指令: {section.animations}

    ### 代码规范
    - 继承 `TeachingScene`，变量先定义后使用
    - 节奏：`self.wait(1)` 给观众思考时间
    - 代码语言: **{target_language}**

    ### 参考代码结构
    ```python
    from manim import *
    {base_class}

    class {section.id.title().replace('_', '')}Scene(TeachingScene):
        def construct(self):
            # 🔴🔴🔴 第一行必须调用 setup_layout()！设置背景色和基础布局 🔴🔴🔴
            self.setup_layout("{section.title}", {section.lecture_lines[:4]})
            
            # 1. 创建代码块 - 🔴 必须使用 self.create_code_block()！
            code_raw = \"\"\"# {target_language} 示例
def algo(data):
    # 核心逻辑
    pass\"\"\"
            code = self.create_code_block(code_raw, language="{target_language.lower()}")
            code.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
            self.play(Create(code))
            
            # 2. Data Structures
            array_group = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)
            
            # 3. 勾叉标记 - 🔴 必须用 MathTex，严禁用 Text！
            correct_mark = MathTex(r"\\checkmark", color="#478211").scale(1.2)  # 绿色勾 ✓
            wrong_mark = MathTex(r"\\times", color="#C84A2B").scale(1.2)        # 红色叉 ✗
            
            # 3. Execution Trace
            code_lines = code[2]
            highlight = SurroundingRectangle(code_lines[0], color=YELLOW, buff=0.05)
            self.play(Create(highlight))
            
            # 移动高亮
            new_hl = SurroundingRectangle(code_lines[1], color=YELLOW, buff=0.05)
            self.play(Transform(highlight, new_hl))
            
            self.wait(2)
    ```

    ### 强制约束 - 字体与配色
    **【字体规则】** 所有 `Text()` 必须使用 `font="Noto Sans SC"`（跨平台中文字体）
    ```python
    # ✅ 正确示例
    Text("标题文字", font="Noto Sans SC", font_size=28, color="#BE8944", weight="BOLD")
    Text("讲解文字", font="Noto Sans SC", font_size=20, color="#2C1608")  # 讲解文字必须 font_size=20
    ```
    
    **【🚨🚨🚨 数学表达式与特殊符号 - 必须用 MathTex！🚨🚨🚨】**
    
    **完整规则详见上方规则 1 和规则 1.1，以下是快速参考：**
    
    **核心原则：** Text() 无法渲染数学符号和特殊符号（会变方框），必须用 MathTex。
    
    ```python
    # ✅ 正确示例
    MathTex(r"O(\log_2 n)", color="#9B6D0B").scale(0.8)        # 复杂度
    MathTex(r"2^7 = 128 > 100", color="#9B6D0B").scale(0.8)    # 数学表达式
    MathTex(r"\\checkmark", color="#478211").scale(1.2)          # 绿色勾 ✓
    MathTex(r"\\times", color="#C84A2B").scale(1.2)              # 红色叉 ✗
    
    # ✅ 中文+数学混排
    VGroup(
        Text("因为：", font="Noto Sans SC", font_size=20, color="#2C1608"),
        MathTex(r"2^7 = 128 > 100", color="#9B6D0B").scale(0.8)
    ).arrange(RIGHT, buff=0.2)
    
    # ❌ 错误：以下写法全部会显示方框！
    # Text("✓")  Text("✗")  Text("×")  Text("O(n²)")  Text("log₂n")
    ```
    
    **【需要用 MathTex 的符号速查表】**
    | 符号类型 | 常见符号 | MathTex 写法 |
    |---------|---------|-------------|
    | 上标/下标 | ², ³, ₂, ₙ | `r"^2"`, `r"^3"`, `r"_2"`, `r"_n"` |
    | 运算符 | ×, ÷, ≤, ≥, ≠ | `r"\\times"`, `r"\\div"`, `r"\\leq"`, `r"\\geq"`, `r"\\neq"` |
    | 对数/无穷 | log₂, ∞ | `r"\\log_2"`, `r"\\infty"` |
    | **勾/叉** | **✓, ✗** | **`r"\\checkmark"`（绿勾）, `r"\\times"`（红叉）** |
    
    **⚠️ 违反此规则 = 显示方框 = 生成失败**
    
    **【配色表】** `背景颜色: #FFFDF4` 【奶油白色背景，严禁使用纯黑背景】
    | 语义 | 文字色 | 背景色 | 边框色 | 样式 |
    |------|--------|--------|--------|------|
    | 普通文字 | #2C1608 | - | - | 普通 |
    | 大标题 | #BE8944 | - | - | **加粗 weight="BOLD"** |
    | 重要概念 | #9B6D0B | #FAECD2 | #f2cf7f | - |
    | 警告/错误 | #C84A2B | #FBDDD6 | #f4b1a1 | - |
    | 强调/高亮 | #C35101 | #FDDFCA | #f7bc93 | - |
    | 提示/信息 | #1A7F99 | #ecf6fa | #bde0ee | - |
    | 成功/正确 | #478211 | #effce3 | #c7e7aa | - |
    | 代码块 | - | #fff7e8 | #e4c8a6 | **必须用 tango + background_config** |
    
    **【配色原则】**
    - 每个场景最多 3-4 种强调色，确保整体和谐
    - 讲解文字讲到对应句子时只改变颜色，不改位置大小
    - 小框标题用语义色（成功框用绿、错误框用红），不允许使用大标题色
    - 顶部的大标题颜色必须为 #BE8944，且必须加粗
    - 边框色与标题色配套
    - 代码块必须使用指定的浅色背景和 tango 语法高亮主题，不能使用默认的深色主题和其余语法高亮主题
    - 禁止使用纯白/纯黑的文字，禁止调色板外颜色


    ### 防遮挡规则
    - **宽度安全**: Text/MathTex 设置 `max_width=5` 或 `.scale_to_fit_width()`
    - **⚠️ 右边界硬性限制（必须遵守）**：
        - 右侧区域 X ∈ [0.3, 6.5]，宽度最大 6.2
        - 创建元素后检查并缩放：
          ```python
          if obj.get_right()[0] > 6.5 or obj.get_left()[0] < 0.3:
              obj.scale_to_fit_width(6.2).move_to([3.4, obj.get_center()[1], 0])
          ```
        - VGroup 的 arrange() 后必须检查并缩放
    - **背景保护**: 叠加标签加 `.add_background_rectangle(color=BLACK, opacity=0.8)`
    - **间距预留**: VGroup 使用 `.arrange(DOWN, buff=0.5)`
    - **智能清理**: 新元素出现前，若旧元素会被遮挡且不再使用，先 `FadeOut` 后必须 `self.remove(obj)` 彻底移除

    ### 🔴🔴🔴 生成代码后必须执行的自检（Final Check）🔴🔴🔴
    
    **生成完代码后，你必须逐行扫描你的代码，如果发现以下任何模式，必须立即修正：**
    
    | 发现这个模式 | 必须改为 |
    |-------------|---------|
    | `Text("✓"` 或 `Text("✔"` 或 `Text("√"` | `MathTex(r"\\checkmark", color=...).scale(1.2)` |
    | `Text("✗"` 或 `Text("✘"` 或 `Text("×"` | `MathTex(r"\\times", color=...).scale(1.2)` |
    | `Text("O(` 或 `Text("log` | 拆分为 Text + MathTex 的 VGroup |
    | `Code(code_string=` | 改为 `self.create_code_block(` |
    
    **⚠️ 如果你的最终代码中仍然包含 `Text("✓")` 或 `Text("✗")` 或 `Text("×")`，这段代码将无法渲染，视为生成失败。**
    
    **自检步骤：**
    1. 在你的代码中搜索所有 `Text(` 调用
    2. 检查每个 `Text()` 的内容是否包含 ✓、✗、×、√、O(、log 等
    3. 如果包含，立即替换为 MathTex 写法
    4. 确认所有勾叉都使用了 `MathTex(r"\\checkmark"` 或 `MathTex(r"\\times"`
"""


def get_regenerate_note(attempt, MAX_REGENERATE_TRIES, error_message: str = None):
    """
    生成重试提示词（仅用于运行失败的情况）
    
    Args:
        attempt: 当前尝试次数
        MAX_REGENERATE_TRIES: 最大尝试次数
        error_message: 运行失败的错误信息（可选）
    """
    base_note = f"""⚠️ 注意：这是第 {attempt}/{MAX_REGENERATE_TRIES} 次尝试生成代码。

"""
    
    if error_message:
        # 运行失败的情况 - 提供错误信息，要求修复但保持动画效果
        return base_note + f"""**上次代码运行失败，错误信息如下：**
```
{error_message}
```

## 🔴🔴🔴 修复要求（必须严格遵守！）🔴🔴🔴

**1. 只修复错误，不删除内容！**
- 仅针对错误信息中指出的具体问题进行修复
- **严禁删除任何讲解文字、动画步骤或 wait() 调用**
- **严禁缩短视频时长或减少内容**
- **严禁将复杂动画简化为只显示标题和文字**

**2. 保持完整性检查清单：**
- [ ] 所有原有的讲解文字是否都保留了？
- [ ] 所有原有的动画步骤是否都保留了？
- [ ] wait() 调用的总时长是否与原来相近？
- [ ] 数据结构可视化（数组、指针、高亮等）是否完整？
- [ ] 代码块和代码高亮是否保留？

**3. 常见错误的正确修复方式：**
| 错误类型 | ✅ 正确做法 | ❌ 错误做法 |
|---------|-----------|-----------|
| 变量未定义 | 添加变量定义 | 删除使用该变量的代码 |
| 索引越界 | 修复索引计算或添加边界检查 | 减少数组元素数量 |
| 对象属性错误 | 修正属性名或方法调用 | 删除该对象 |
| 动画冲突 | 调整动画顺序或使用 AnimationGroup | 删除动画 |
| LaTeX 错误 | 修复 LaTeX 语法 | 改用纯文本（会显示方框） |
| **引号嵌套错误** | 内层用单引号 `'` | 内层用中文双引号 `"` |

**🔴 引号嵌套规则（非常重要！）：**
- 如果 Text() 外层使用双引号 `"`，内层必须使用**英文单引号** `'`
- ❌ 错误：`Text("最大的数"浮"到最后！")` - 中文双引号会导致语法错误
- ✅ 正确：`Text("最大的数'浮'到最后！")` - 使用英文单引号

**4. 如果实在无法修复某个复杂动画：**
- 用等效的简单动画替代，而不是直接删除
- 保持相同的讲解内容和时长
- 例如：复杂的数组交换动画 → 简单的 FadeOut + FadeIn，但保留数值变化的展示

**5. 绝对禁止的行为：**
- ❌ 删除整个动画演示部分，只保留标题和讲解文字
- ❌ 将 30 秒的视频缩短为 5 秒
- ❌ 删除代码块展示
- ❌ 删除数据结构可视化
"""
    
    else:
        # 无具体信息时的通用提示
        return base_note + """请检查并改进代码：
- 确保所有变量在使用前已定义
- 检查 `self.wait()` 是否充足
- **保持动画效果完整，不要过度简化**
- **严禁删除任何讲解文字、动画步骤或数据结构可视化**
"""
