import os
from typing import Optional
from .user_profile import UserProfile, get_default_profile


def get_prompt3_code(
    regenerate_note: str,
    section,
    base_class: str,
    user_profile: Optional[UserProfile] = None,
    estimated_duration: Optional[int] = None
):
    """
    生成Manim代码的提示词
    
    Args:
        regenerate_note: 重新生成的注意事项
        section: 章节信息对象
        base_class: 基类代码
        user_profile: 用户配置，可选
        estimated_duration: 该章节的预计时长（秒），可选
    
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
    
    return f"""
    你是一位精通 Manim 的 Python 专家。请编写代码生成一个**解释复杂算法执行逻辑**的视频片段。

    {regenerate_note}
    {duration_guidance}

    {profile_prompt}

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

    **【代码展示 - 必须使用 Code 对象 + 浅色背景 】**
    ⚠️ **严禁用 Text() 显示代码！必须使用 Code() 对象**
    
    ```python
    # ⚠️⚠️⚠️ 【必须设置 background_config 实现浅色背景！】⚠️⚠️⚠️
    # ⚠️⚠️⚠️ 【必须使用特定的 tango 浅色语法高亮主题！】⚠️⚠️⚠️
    code_obj = Code(
        code_string=code_text,           # 使用 code_string 而不是 code
        language="{target_language.lower()}",
        background="rectangle",
        formatter_style="tango",         # ⭐⭐⭐ 关键！指定的唯一语法高亮主题 ⭐⭐⭐
        background_config={{              # ⭐⭐⭐ 关键！自定义浅色背景 ⭐⭐⭐
            "fill_color": "#fff7e8",     # 浅金色背景
            "stroke_color": "#e4c8a6",   # 金色边框
            "stroke_width": 2
        }}
    )
    # ❌ 错误示例（没有 background_config 和 tango，会是深色背景和错误的语法高亮）：
    # code_obj = Code(code_string=code_text, language="python", background="rectangle")
    ```
    
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
            # 1. Setup Layout
            code_raw = \"\"\"# {target_language} 示例
def algo(data):
    # 核心逻辑
    pass\"\"\"
            code = Code(
                code_string=code_raw, 
                language="{target_language.lower()}", 
                formatter_style="tango",
                background_config={{"fill_color": "#fff7e8", "stroke_color": "#e4c8a6", "stroke_width": 2}},
            )
            code.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
            self.play(Create(code))
            
            # 2. Data Structures
            array_group = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)
            
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
    Text("讲解文字", font="Noto Sans SC", font_size=25, color="#2C1608")
    ```
    
    **【⚠️⚠️⚠️ 数字与数学表达式 - 必须使用 MathTex！】**
    
    **🚨🚨🚨 核心规则：只要包含数字的表达式，全部使用 MathTex！🚨🚨🚨**
    
    **为什么？**
    - Text() 在 Noto Sans SC 字体下无法正确显示数学符号（`²`, `⁷`, `×`, `÷` 等会变成方框）
    - MathTex 渲染效果最好，数字和符号对齐完美
    - 保持视觉一致性
    
    **✅ 简单规则：包含数字的表达式 → 用 MathTex**
    
    ```python
    # ✅ 正确：纯数学表达式直接用 MathTex
    MathTex(r"2^7 = 128 > 100", color="#9B6D0B").scale(0.8)
    MathTex(r"O(\log_2 n)", color="#2C1608").scale(0.8)
    MathTex(r"100 \times 10 = 1000", color="#2C1608").scale(0.8)
    MathTex(r"n^2 + 2n + 1", color="#2C1608").scale(0.8)
    MathTex(r"7 < 10", color="#478211").scale(0.8)  # 比较表达式
    MathTex(r"mid = 5", color="#2C1608").scale(0.8)  # 变量赋值
    
    # ✅ 正确：中文 + 数学表达式，用 VGroup 组合
    explain_text = VGroup(
        Text("因为：", font="Noto Sans SC", font_size=20, color="#2C1608"),
        MathTex(r"2^7 = 128 > 100", color="#9B6D0B").scale(0.8)
    ).arrange(RIGHT, buff=0.2)
    
    # ✅ 正确：时间复杂度
    complexity = VGroup(
        Text("时间复杂度：", font="Noto Sans SC", font_size=20, color="#2C1608"),
        MathTex(r"O(\log_2 n)", color="#9B6D0B").scale(0.8)
    ).arrange(RIGHT, buff=0.1)
    ```
    
    **❌ 绝对禁止：在 Text() 中写数字表达式**
    ```python
    # ❌ 错误：用 Text 显示数学表达式
    Text("2⁷ = 128 > 100")      # ❌ 上标会变方框
    Text("O(log₂n)")            # ❌ 下标会变方框
    Text("100 × 10 = 1000")     # ❌ 乘号会变方框
    Text("n² + 2n")             # ❌ 上标会变方框
    ```
    
    **❌ 绝对禁止的错误写法（会导致显示异常）：**
    ```python
    # ❌ 错误：直接在 Text 中写数学符号 - 会显示方框！
    Text("时间复杂度是 O(log₂n)")      # ❌ log₂ 显示为方框
    Text("100 × 10 = 1000")            # ❌ × 显示为方框
    Text("n² + 2n")                    # ❌ ² 显示为方框
    
    # ❌ 错误：用注释说"避免LaTeX问题"然后用纯文本 - 这是错误的！
    # 不要写：if "log₂" in line: text_obj = Text(line, ...)  # ❌ 依然会显示方框
    ```
    
    **🔍 检查清单（生成代码前必须确认）：**
    - [ ] 讲解文字中是否包含 `log`、`O(`、`×`、`²`、`≤` 等？如果有，必须拆分为 Text + MathTex
    - [ ] 是否使用了 VGroup(...).arrange(RIGHT, buff=0.1) 来组合？
    - [ ] MathTex 是否设置了 .scale(0.8) 使大小与 Text 匹配？
    
    **【需要用 MathTex 的符号清单】**
    | 符号类型 | 常见符号 | MathTex 写法 |
    |---------|---------|-------------|
    | 下标 | ₂, ₃, ₙ | `r"_2"`, `r"_3"`, `r"_n"` |
    | 上标 | ², ³, ⁿ | `r"^2"`, `r"^3"`, `r"^n"` |
    | 运算符 | ×, ÷, ±, ≤, ≥, ≠ | `r"\\times"`, `r"\\div"`, `r"\\pm"`, `r"\\leq"`, `r"\\geq"`, `r"\\neq"` |
    | 对数 | log₂ | `r"\\log_2"` |
    | 希腊字母 | α, β, θ | `r"\\alpha"`, `r"\\beta"`, `r"\\theta"` |
    | 箭头 | →, ← | `r"\\rightarrow"`, `r"\\leftarrow"` |
    | 无穷 | ∞ | `r"\\infty"` |
    | **勾/叉** | ✓, ✗ | `r"\\checkmark"` (绿勾), `r"\\times"` (红叉) |
    
    **【勾和叉的正确用法】**
    ```python
    # ✅ 正确：用 MathTex 显示勾和叉
    correct_mark = MathTex(r"\\checkmark", color="#478211").scale(1.2)  # 绿色勾
    wrong_mark = MathTex(r"\\times", color="#C84A2B").scale(1.2)        # 红色叉
    
    # ❌ 错误：直接在 Text 中使用会显示方框
    # Text("✗", font="Noto Sans SC")  # 无法显示！
    ```
    
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

请根据错误信息修复代码：
- 修复导致运行失败的具体问题
- 确保所有变量在使用前已定义
- 检查 Manim 对象的属性和方法调用是否正确
- **保持原有的大致动画效果和逻辑，不要过度简化**
"""
    
    else:
        # 无具体信息时的通用提示
        return base_note + """请检查并改进代码：
- 确保所有变量在使用前已定义
- 检查 `self.wait()` 是否充足
- **保持动画效果完整，不要过度简化**
"""
