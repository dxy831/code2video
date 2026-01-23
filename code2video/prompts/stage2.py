import json
from typing import Optional
from .user_profile import UserProfile, get_default_profile


def get_prompt2_storyboard(
    outline: str,
    reference_image_path: Optional[str] = None,
    user_profile: Optional[UserProfile] = None
):
    """
    生成分镜脚本的提示词
    
    Args:
        outline: 大纲JSON字符串
        reference_image_path: 参考图片路径（可选）
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
    
    base_prompt = f""" 
    你是一位**硬核算法可视化导演**。请将大纲转化为详细的 Manim 动画脚本。

    {profile_prompt}

    ## 根据用户配置的动画风格要求

    ### 受众适配
    - 目标观众：**{age_desc['audience']}**
    - 讲解节奏：{age_desc['pace']}
    - 用语规范：{age_desc['vocabulary']}
    
    ### 难度适配
    - 难度级别：**{diff_desc['level']}**
    - 动画风格：{diff_desc['visual_style']}
    - 代码展示风格：{diff_desc['code_style']}
    
    ### 编程语言
    - 代码语言：**{lang_desc['name']}**
    - 代码风格：{lang_desc['style']}

    # 通用视觉映射系统 (Universal Visual Mapping System)

    1.  **多维布局策略 (Layout Strategy)**:
        - **智能布局分流 (Smart Layout Branching)**:
          - **Case A: 纯理论/无代码 (No Code)** -> 保持现状：**左右对半布局**。左侧放讲解文字，右侧放可视化动画。
          - **Case B: 代码演示场景 (With Code - DEFAULT for Algorithms)** -> **采用 "左侧分割 + 右侧全屏" 布局 (Split-Left Layout)**:
            - **规则**: 凡是讲解算法具体步骤（循环、判断、交换、递归）的章节，**必须**使用此模式展示代码片段。严禁只在最后才展示代码。
            - **左上区域 (Top-Left, ~30% height)**: 放置讲解文字 (Lecture Notes)。
            - **左下区域 (Bottom-Left, ~70% height)**: 放置 **{lang_desc['name']}** 代码片段 (Code Snippet)。
            - **右侧区域 (Right Half, 100% height)**: 放置核心可视化/动画 (Main Visual)。
          - **Case C: 完整代码/纯代码 (Full Code - FINAL SECTION ONLY)**:
            - **规则**: 最后一个章节专门展示完整 **{lang_desc['name']}** 源码。
            - **布局**: **隐藏左侧文字** (Lecture Notes opacity=0)，将代码对象放大并居中 (`scale(0.8).move_to(ORIGIN)`)。
            - **分页**: 如果代码超过 20 行，必须拆分为连续的子场景 (Sub-scenes, e.g., `Scene 12.1`, `Scene 12.2`)。

        - **强制分页规则 (Pagination Protocol)**:
          - **文字量控制**: 单页讲解文字不得超过 **3行**。
          - **代码量控制**: 如果代码过长导致左下区域放不下，**必须**将内容拆分为连续的子场景。宁可多页，不可字小。
        - **State Monitor (底部/角落)**: 实时显示的变量值（Cost, Index, True/False）。
        - **Text Zoning Strategy (文本分区策略)**:
          - **Lecture Lines (旁白字幕)**: 必须严格限制在屏幕底部的 "Subtitle Bar" (Bottom 15% area)。严禁将长段解释性文字放在屏幕中央或与图形混排。
          - **Labels (标签)**: 跟随物体的标签必须简短（Max 2-3 words）。
          - **Title**: 每一节的标题固定在左上角或顶部，不可遮挡 Main Visual Area。

    2.  **抽象概念实体化**:
        - **引用/指针**: 必须画成箭头 (Arrow)。
        - **递归**: 必须画成**调用栈 (Call Stack)**，用一个个压入的矩形块表示，旁边标注参数值。
        - **比较/判断**: 必须在屏幕上显示临时的数学不等式（例如 `dist[B] > new_dist`），判定后再消失。
        - **记忆化/缓存**: 画成一个表格 (Table/Grid)，命中时高亮闪烁。

    3.  **脚本要求**:
        - 每一句旁白（Lecture Line）必须对应代码的解释。
        - 每一个动画（Animation）必须对应数据的变化（Create, Transform, FadeOut）。
        - **节奏控制**：根据难度"{diff_desc['level']}"，{diff_desc['visual_style']}

    4.  **语言适配要求**:
        - 所有代码示例必须使用 **{lang_desc['name']}**
        - 代码语法高亮应适配 {lang_desc['name']} 语法
        - 注释风格：{diff_desc['code_style']}

    ## 输入大纲
    {outline}
    """

    base_prompt += """
    请输出以下 JSON 格式：
    {
        "sections": [
            {
                "id": "section_id",
                "title": "标题",
                "lecture_lines": ["..."],
                "animations": [
                    "Define Visual Layout: Split Right Area into Top (Graph) and Bottom (Priority Queue).",
                    "Action: Highlight code line `heapq.heappush(pq, (0, start))`.",
                    "Visual: Create a Circle labeled 'Start' in Graph. Create a small Square labeled '(0, S)' appearing in the Queue area.",
                    "Monitor: Update text `Current Cost = 0`."
                ]
            }
        ]
    }
    """
    return base_prompt


def get_prompt_download_assets(storyboard_data):
    return f"""
分析这份教育视频分镜脚本，识别出最多 4 个**必须**使用下载图标/图片（而非手动绘制形状）来表示的关键视觉元素。

内容 (Content):
{storyboard_data}

选择标准 (Selection Criteria):
1. 仅选择出现在**介绍 (Introduction)** 或 **应用 (Application)** 章节中的元素，且必须满足：
   - 现实世界中可识别的物理对象
   - 视觉特征鲜明，仅用通用几何形状不足以表达
   - 具体的实物，而非抽象概念
2. 优先选择：具体的动物、角色、交通工具、工具、设备、地标、日常物品。
3. **忽略且绝不包含**：
   - 抽象概念（如：正义、交流）
   - 思想的符号或图标（如：字母、公式、图表、数据结构树）
   - 几何形状、箭头或数学相关的视觉元素
   - 任何完全由基本形状组成且无独特视觉身份的物体

输出格式 (Output format):
- **仅输出英文关键词**（为了适配搜索引擎），每个关键词占一行，全小写，无编号，无额外文本。
"""


def get_prompt_place_assets(asset_mapping, animations_structure):
    return f"""
你需要通过插入已下载的素材来增强动画描述。

可用素材列表 (Asset list):
{asset_mapping}

当前动画数据 (Current Animations Data):
{animations_structure}

指令 (Instructions):
- 对于每一个动画步骤，判断是否应该融入已下载的素材。
- 仅为需要的动画步骤选择最相关的一个素材。
- 以此格式插入素材的**抽象路径**：[Asset: XXX]。
- **仅限**在**第一个和最后一个**章节中使用素材。
- 保持结构不变：返回一个包含 section_index, section_id 和 enhanced animations 的 JSON 数组。
- 仅修改动画描述以包含素材引用。
- 不要修改 section_index 或 section_id。

仅返回增强后的动画数据，必须是有效的 JSON 数组格式：
"""
