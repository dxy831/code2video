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
    
    # 只获取必要的描述，移除 profile_prompt 调用以减少重复
    age_desc = user_profile.get_age_group_description()
    diff_desc = user_profile.get_difficulty_description()
    lang_desc = user_profile.get_language_description()
    
    return f"""
    你是一位精通 Manim 的 Python 专家。请编写代码生成一个**解释复杂算法执行逻辑**的视频片段。

    {regenerate_note}

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

    ### 核心任务：通用算法可视化
    不要硬编码特定的形状，而是根据算法逻辑选择最合适的 Manim 对象。

    ### 1. 动态布局系统
    **【重要】左侧三层垂直布局，严禁重叠：**
    ```python
    # 左侧垂直布局 (从上到下):
    # Layer 1: 标题 title -> to_edge(UP, buff=0.1)
    # Layer 2: 讲解文字 lecture -> 标题下方, 高度限制 2.5 单位
    # Layer 3: 代码 code_obj -> to_edge(DOWN, buff=0.3), 高度限制 3.0 单位
    # 右侧: 动画区域

    # === 布局模板 ===
    title.to_edge(UP, buff=0.1)
    self.lecture.next_to(title, DOWN, buff=0.15).to_edge(LEFT, buff=0.3)
    if self.lecture.height > 2.5:
        self.lecture.scale_to_fit_height(2.5)
    
    code_obj.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.3)
    if code_obj.height > 3.0:
        code_obj.scale_to_fit_height(3.0)
    
    # 确保讲解与代码不重叠
    if self.lecture.get_bottom()[1] < code_obj.get_top()[1] + 0.3:
        code_obj.scale(0.85)
        code_obj.to_edge(DOWN, buff=0.3)
    ```

    **【代码注释必须用中文】**
    ```python
    code_obj = Code(
        code=code_text,
        language="{lang_desc['name'].lower()}",
        font="Noto Sans Mono CJK SC",
        background="rectangle",
        font_size=16
    )
    ```

    **【代码高亮框精确定位】使用 code_obj[2] 访问代码行 VGroup：**
    ```python
    code_lines = code_obj[2]
    highlight = SurroundingRectangle(code_lines[0], color=YELLOW, buff=0.05)
    self.play(Create(highlight))
    
    # ✅ 移动高亮框 (使用 Transform)
    new_highlight = SurroundingRectangle(code_lines[2], color=YELLOW, buff=0.05)
    self.play(Transform(highlight, new_highlight))
    
    # ❌ 禁用 move_to 和 Indicate
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

    ### 任务输入
    - 标题: {section.title}
    - 脚本: {section.lecture_lines}
    - 动画指令: {section.animations}

    ### 代码规范
    - 继承 `TeachingScene`，变量先定义后使用
    - 节奏：`self.wait(1)` 给观众思考时间
    - 代码语言: **{lang_desc['name']}**

    ### 参考代码结构
    ```python
    from manim import *
    {base_class}

    class {section.id.title().replace('_', '')}Scene(TeachingScene):
        def construct(self):
            # 1. Setup Layout
            code_raw = \"\"\"# {lang_desc['name']} 示例
def algo(data):
    # 核心逻辑
    pass\"\"\"
            code = Code(code=code_raw, language="{lang_desc['name'].lower()}", font="Noto Sans Mono CJK SC")
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

    ### 强制约束
    - 颜色使用明亮的 hex 颜色
    - 禁止 3D 场景，保持 2D 清晰图解
    - 讲解文字只改颜色，不改位置大小

    ### 防遮挡规则
    - **宽度安全**: Text/MathTex 设置 `max_width=5` 或 `.scale_to_fit_width()`
    - **背景保护**: 叠加标签加 `.add_background_rectangle(color=BLACK, opacity=0.8)`
    - **间距预留**: VGroup 使用 `.arrange(DOWN, buff=0.5)`
    - **智能清理**: 新元素出现前，若旧元素会被遮挡且不再使用，先 `FadeOut`
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
