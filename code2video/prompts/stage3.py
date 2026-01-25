import os
from typing import Optional
from .user_profile import UserProfile, get_default_profile


def get_prompt3_code(
    regenerate_note: str,
    section,
    base_class: str,
    user_profile: Optional[UserProfile] = None
):
    """
    生成Manim代码的提示词
    
    Args:
        regenerate_note: 重新生成的注意事项
        section: 章节信息对象
        base_class: 基类代码
        user_profile: 用户配置（年龄段、编程语言、难度），可选
    
    Returns:
        完整的提示词字符串
    """
    # 如果没有提供用户配置，使用默认配置
    if user_profile is None:
        user_profile = get_default_profile()
    
    # 获取用户配置的提示词片段
    profile_prompt = user_profile.generate_profile_prompt()
    
    # 获取具体的配置描述
    age_desc = user_profile.get_age_group_description()
    diff_desc = user_profile.get_difficulty_description()
    lang_desc = user_profile.get_language_description()
    
    return f"""
    你是一位精通 Manim 的 Python 专家。请编写代码生成一个**解释复杂算法执行逻辑**的视频片段。

    {regenerate_note}

    {profile_prompt}

    ## 根据用户配置的代码生成要求

    ### 受众适配
    - 目标观众：**{age_desc['audience']}**
    - 讲解节奏：{age_desc['pace']}
    - 内容深度：{age_desc['depth']}
    
    ### 难度适配
    - 难度级别：**{diff_desc['level']}**
    - 动画风格：{diff_desc['visual_style']}
    - 代码注释风格：{diff_desc['code_style']}
    
    ### 编程语言
    - 示例代码语言：**{lang_desc['name']}**
    - 代码风格：{lang_desc['style']}
    - 语言特性：{lang_desc['features']}

    ### 核心任务：通用算法可视化 (Universal Algorithm Visualization)
    
    不要硬编码特定的形状，而是根据算法逻辑选择最合适的 Manim 对象。

    ### 1. 动态布局系统 (Dynamic Layout System)
    **【重要】左侧三层垂直布局，严禁重叠：**
    ```python
    # 左侧垂直布局 (从上到下):
    # Layer 1: 标题 title -> to_edge(UP, buff=0.2)
    # Layer 2: 讲解文字 lecture -> 标题下方, 高度限制 2.5 单位
    # Layer 3: 代码 code_obj -> to_edge(DOWN, buff=0.3), 高度限制 3.0 单位
    # 右侧: 动画区域 main_group -> to_edge(RIGHT, buff=0.3)

    # === 布局模板 ===
    # 1. 标题固定顶部
    title.to_edge(UP, buff=0.2)
    
    # 2. 讲解文字: 紧贴标题下方, 限制高度防止与代码重叠
    self.lecture.next_to(title, DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
    if self.lecture.height > 2.5:
        self.lecture.scale_to_fit_height(2.5)
    
    # 3. 代码区域: 固定底部, 限制高度
    code_obj.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
    if code_obj.height > 3.0:
        code_obj.scale_to_fit_height(3.0)
    
    # 4. 确保讲解与代码不重叠 (最小间距 0.5)
    if self.lecture.get_bottom()[1] < code_obj.get_top()[1] + 0.5:
        self.lecture.scale(0.8)  # 缩小讲解文字
    ```

    **【代码注释必须用中文】算法代码中的注释必须使用中文，并指定中文字体：**
    ```python
    # ✅ 正确: 中文注释 + 中文字体
    code_text = '''# 二分查找算法
def binary_search(nums, target):
    low = 0  # 左边界
    high = len(nums) - 1  # 右边界'''
    
    code_obj = Code(
        code=code_text,
        language="python",
        font="Noto Sans Mono CJK SC",  # 支持中文的等宽字体
        background="rectangle",
        font_size=16
    )
    
    # ❌ 错误: 英文注释
    code_text = '''# Binary search algorithm
def binary_search(nums, target):'''
    ```

    **【代码高亮框精确定位】使用 code_obj[2] 访问代码行 VGroup：**
    ```python
    # Manim Code对象结构: code_obj[0]=背景, code_obj[1]=行号, code_obj[2]=代码行VGroup
    code_lines = code_obj[2]  # 获取代码行 VGroup
    
    # ✅ 正确: 对单行创建高亮框
    highlight = SurroundingRectangle(code_lines[0], color=YELLOW, buff=0.05)
    self.play(Create(highlight))
    
    # ✅ 正确: 移动高亮框到指定行 (使用 Transform 而非 move_to)
    new_highlight = SurroundingRectangle(code_lines[2], color=YELLOW, buff=0.05)
    self.play(Transform(highlight, new_highlight))
    
    # ❌ 错误: move_to 会导致位置偏移
    # self.play(highlight.animate.move_to(code_lines[2]))
    ```
    
    - **代码语言**: 代码示例必须使用 **{lang_desc['name']}** 语法。

    ### 2. 交互与逻辑表现 (Interaction & Logic)
    - **代码高亮**: 使用 `SurroundingRectangle` 精确框选代码行，禁止用 `Indicate` 高亮代码块
    - **呼吸感时序 (Breathing Timing)**:
      - **关键规则**: 在 `self.play(Indicate(self.lecture))` (文字高亮) 结束之后，**必须强制插入** `self.wait(0.5)`。
      - **视线引导**: 先看左上文字 -> 停顿 0.5s -> 再看右侧动画或左下代码。严禁文字高亮与复杂动画同时开始。
      - **节奏控制**：根据难度"{diff_desc['level']}"，{diff_desc['visual_style']}
    - **逻辑外显化**: 
      - 不要只让数据变色。如果代码里有 `if a > b`，你必须在屏幕上写出 `MathTex("5 > 3")`，显示它成立（变绿）或不成立（变红），然后再执行后续动作。
      - **递归**: 如果涉及递归，请在屏幕一角维护一个 `VGroup` 代表 Stack，每层递归 `add` 一个矩形，返回时 `remove`。

    ### 3. 数据结构映射库 (Mapping Library)
    - **Array/DP Table**: 使用 `VGroup` of `Square` 或 `Table` 类。必须标 `Index`。
    - **Tree/Graph**: 优先使用 `Graph` 类（如果节点关系固定），或者手动通过 `Circle` 和 `Line` 构建，以便灵活移动节点。
    - **Pointer/Reference**: `Arrow` 是必须的。不要只改变颜色，要用箭头指向当前操作的对象。

    ### 任务输入
    - 标题: {section.title}
    - 脚本: {section.lecture_lines}
    - 动画指令: {section.animations}

    ### 代码规范
    - 必须继承 `TeachingScene`。
    - 确保代码逻辑完整：变量先定义后使用。
    - 节奏：`self.wait(1)` 非常重要，给观众思考时间。
    - **代码示例语言**: 视频中展示的算法代码必须使用 **{lang_desc['name']}**

    ### 参考代码结构
    ```python
    from manim import *
    {base_class}

    class {section.id.title().replace('_', '')}Scene(TeachingScene):
        def construct(self):
            # 1. Setup Layout
            # 注意：这里的代码示例应使用 {lang_desc['name']} 语法
            code_raw = \"\"\"// {lang_desc['name']} 代码示例
def complex_algo(data):
    if check(data):
        optimize(data)
    else:
        process(data)\"\"\"
            code = Code(code=code_raw, language="{lang_desc['name'].lower()}", ...).to_edge(LEFT)
            self.play(Create(code))
            
            # 2. Setup Data Structures (Example: A composite structure)
            # Main Data (e.g., Array)
            array_group = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT).to_edge(UP)
            # Aux Data (e.g., Stack)
            stack_group = VGroup().to_edge(DOWN)
            
            # 3. Execution Trace with SurroundingRectangle
            code_lines = code[2]  # 获取代码行 VGroup
            
            # Step 1: Create highlight box for code line
            highlight = SurroundingRectangle(code_lines[1], color=YELLOW, buff=0.05)
            self.play(Create(highlight))
            check_label = MathTex("Check: Is Valid?").next_to(array_group, DOWN)
            self.play(Write(check_label))
            
            # Step 2: Visual Feedback
            self.play(array_group[0].animate.set_color(GREEN))
            self.play(FadeOut(check_label))
            
            # Step 3: Move highlight to next line (使用 Transform)
            new_highlight = SurroundingRectangle(code_lines[2], color=YELLOW, buff=0.05)
            self.play(Transform(highlight, new_highlight))
            # Show optimization effect
            self.play(ReplacementTransform(array_group[0], array_group[1]))
            
            self.wait(2)
    ```

6. **强制约束**:
- 颜色使用明亮的 hex 颜色。
- 严禁使用复杂的 3D 场景（除非必要），保持 2D 清晰图解。
- 不要在动画中改变左侧 lecture_lines 的位置或大小，只改变颜色。

7. **Anti-Occlusion Rules (防遮挡规则)**:
- **Rule 1: 宽度安全** - Text/MathTex 必须设置 `max_width=5` 或 `.scale_to_fit_width()`
- **Rule 2: 背景保护** - 叠加在图形上的标签必须 `.add_background_rectangle(color=BLACK, opacity=0.8)`
- **Rule 3: 间距预留** - VGroup 使用 `.arrange(DOWN, buff=0.5)` 保持呼吸感
- **Rule 4: 智能清理** - **在新元素出现前，若旧元素会被遮挡且后续不再使用，先 `FadeOut` 清除它：**
  ```python
  # ✅ 正确: 新元素出现前清理会被遮挡且无用的旧元素
  self.play(FadeOut(old_label))  # old_label 后续不再需要+会被新元素遮挡
  self.play(FadeIn(new_element))  # 新元素安全出现
  
  # ❌ 错误: 直接叠加导致遮挡
  self.play(FadeIn(new_element))  # new_element 盖住 old_label
  ```
"""


def get_regenerate_note(attempt, MAX_REGENERATE_TRIES):
    return f"""注意：这是第 {attempt}/{MAX_REGENERATE_TRIES} 次尝试生成代码。上一次生成的代码运行失败或效果不佳。请：
简化复杂的动画逻辑，优先保证运行成功。
确保所有的变量在使用前都已定义。
检查 self.wait () 是否充足。
"""
