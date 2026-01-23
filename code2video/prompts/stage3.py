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
    ```python
    # 布局坐标系统 (Layout Coordinates):
    # If Code Exists (有代码时):
    #   self.lecture (文字): 强制吸顶 (.to_edge(UP, buff=0.2).to_edge(LEFT, buff=0.5))，为下方代码腾出空间。
    #   code_obj (代码): 强制沉底 (.to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.5))，位于文字下方。
    #   main_group (动画): 锚定在 屏幕右侧居中 (.to_edge(RIGHT)), 占据右半边屏幕。
    
    if hasattr(self, 'code_obj'):
         self.lecture.to_edge(UP, buff=0.2).to_edge(LEFT, buff=0.5)
         self.code_obj.to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.5)
         self.main_group.to_edge(RIGHT)

         # Safety Scale Check (Overflow Protection)
         max_width = 6.5
         max_height = 7.5
         
         if self.main_group.width > max_width:
             self.main_group.scale_to_fit_width(max_width)
         
         if self.main_group.height > max_height:
             self.main_group.scale_to_fit_height(max_height)
    else:
         # No Code: Standard Layout -> Text Vertically Centered
         self.lecture.to_edge(LEFT, buff=0.5).set_y(0)
         self.main_group.to_edge(RIGHT)
    ```
    - **字体与可视性 (Visibility & Fonts)**:
      - **动画文字增强**: 所有位于 `main_group` (右侧动画) 内部的 `Text`/`MathTex`，字号必须 **加大一级** (Scale up by 1.2x or 1.5x)，确保在右侧区域清晰可见。
      - **代码高亮**: `code_obj` 必须启用语法高亮，背景尽量透明或深色适配，确保在左下角清晰。
      - **代码语言**: 代码示例必须使用 **{lang_desc['name']}** 语法。

    ### 2. 交互与逻辑表现 (Interaction & Logic)
    - **代码高亮**: `self.play(Indicate(code_obj.code[line_idx]))`
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
            
            # 3. Execution Trace
            # Step 1: Check
            self.play(Indicate(code.code[1]))
            check_label = MathTex("Check: Is Valid?").next_to(array_group, DOWN)
            self.play(Write(check_label))
            
            # Step 2: Visual Feedback
            self.play(array_group[0].animate.set_color(GREEN)) # Valid
            self.play(FadeOut(check_label))
            
            # Step 3: Optimization phase
            self.play(Indicate(code.code[2]))
            # Show optimization effect (e.g., merge nodes)
            self.play(ReplacementTransform(array_group[0], array_group[1]))
            
            self.wait(2)
    ```

6. **强制约束**:
- 颜色使用明亮的 hex 颜色。
- 严禁使用复杂的 3D 场景（除非必要），保持 2D 清晰图解。
- 不要在动画中改变左侧 lecture_lines 的位置或大小，只改变颜色。

7. **Anti-Occlusion Rules (防遮挡规则)**:
- **Rule 1: Text Width Safety**: 所有 Text, Paragraph, MathTex 对象必须设置 max_width (例如 max_width=config.frame_width * 0.6) 或使用 .scale_to_fit_width()，防止文字溢出屏幕。
- **Rule 2: Background Protection**: 对于可能覆盖在网格、线条或复杂图形上的文字（Labels），必须使用 .add_background_rectangle(color=BLACK, opacity=0.8)，确保文字清晰可读。
- **Rule 3: Collision Avoidance**: 在布局 VGroup 时，必须使用 buff 参数（如 .arrange(DOWN, buff=0.5)）预留足够的呼吸空间。
- **Rule 4: Subtitle Fixed Position**: 解释性文字（Lecture Lines）通常使用 .to_edge(DOWN, buff=1.0) 固定在底部，不要让它随物体移动。
"""


def get_regenerate_note(attempt, MAX_REGENERATE_TRIES):
    return f"""注意：这是第 {attempt}/{MAX_REGENERATE_TRIES} 次尝试生成代码。上一次生成的代码运行失败或效果不佳。请：
简化复杂的动画逻辑，优先保证运行成功。
确保所有的变量在使用前都已定义。
检查 self.wait () 是否充足。
"""
