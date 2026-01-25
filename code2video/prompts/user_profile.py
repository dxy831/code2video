"""
用户个性化配置模块
支持根据不同年龄段、编程语言、难度级别生成定制化的视频内容
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AgeGroup(Enum):
    """年龄段分类"""
    HIGH_SCHOOL = "high_school"      # 初高中学生
    COLLEGE = "college"              # 大学/研究生
    PROFESSIONAL = "professional"    # 工作后的人


class DifficultyLevel(Enum):
    """难度级别"""
    LOW = "low"       # 低难度 - 入门级
    MEDIUM = "medium" # 中难度 - 进阶级
    HIGH = "high"     # 高难度 - 专家级


class ProgrammingLanguage(Enum):
    """编程语言"""
    PYTHON = "Python"
    JAVA = "Java"
    C = "C"
    CPP = "C++"
    JAVASCRIPT = "JavaScript"
    GO = "Go"
    RUST = "Rust"
    CSHARP = "C#"
    PSEUDOCODE = "伪代码"  # 用于纯理论讲解


@dataclass
class UserProfile:
    """用户配置文件"""
    age_group: AgeGroup = AgeGroup.COLLEGE
    programming_language: ProgrammingLanguage = ProgrammingLanguage.PYTHON
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    
    def get_age_group_description(self) -> str:
        """获取年龄段的描述性文本"""
        descriptions = {
            AgeGroup.HIGH_SCHOOL: {
                "audience": "初高中学生",
                "background": "刚开始接触编程，数学基础为初高中水平",
                "style": "生动有趣、多用生活实例类比",
                "pace": "节奏较慢，每个概念都要详细解释",
                "vocabulary": "避免过于专业的术语，使用通俗易懂的语言",
                "examples": "使用校园生活、游戏、动漫等年轻人熟悉的场景作为例子",
                "depth": "注重概念理解和直觉培养，不深入底层实现细节"
            },
            AgeGroup.COLLEGE: {
                "audience": "大学生和研究生",
                "background": "有一定编程基础，熟悉基本数据结构",
                "style": "理论与实践结合，强调算法的数学原理",
                "pace": "中等节奏，适当跳过基础概念",
                "vocabulary": "可以使用专业术语，但需要适当解释",
                "examples": "使用课程项目、面试题、学术研究场景",
                "depth": "深入讲解算法原理，包含复杂度分析和优化思路"
            },
            AgeGroup.PROFESSIONAL: {
                "audience": "职场开发者和技术从业者",
                "background": "有丰富的工程经验，关注实际应用",
                "style": "直击重点、注重实战和工程最佳实践",
                "pace": "较快节奏，假设观众已具备基础知识",
                "vocabulary": "使用行业标准术语，无需过多解释",
                "examples": "使用真实业务场景、系统设计、性能优化案例",
                "depth": "强调工程实现、边界情况处理、性能调优和生产环境注意事项"
            }
        }
        return descriptions.get(self.age_group, descriptions[AgeGroup.COLLEGE])
    
    def get_difficulty_description(self) -> str:
        """获取难度级别的描述性文本"""
        descriptions = {
            DifficultyLevel.LOW: {
                "level": "入门级",
                "prerequisites": "仅需基本的编程概念（变量、循环、条件判断）",
                "content_focus": "核心概念、基本操作、简单示例",
                "code_style": "代码简洁明了，每行都有注释",
                "examples_complexity": "使用最简单的示例，数据量小（如5个元素的数组）",
                "skip_topics": "跳过高级优化、复杂变体、数学证明",
                "visual_style": "动画步骤细致，每一步都停顿讲解"
            },
            DifficultyLevel.MEDIUM: {
                "level": "进阶级",
                "prerequisites": "熟悉基础数据结构（数组、链表、树）和时间复杂度概念",
                "content_focus": "算法原理、常见变体、复杂度分析",
                "code_style": "包含必要注释，展示标准实现",
                "examples_complexity": "使用中等规模示例，展示典型情况和边界情况",
                "skip_topics": "简化数学证明，提及但不深入最优化技巧",
                "visual_style": "动画节奏适中，关键步骤重点展示"
            },
            DifficultyLevel.HIGH: {
                "level": "专家级",
                "prerequisites": "精通数据结构与算法，熟悉算法设计范式",
                "content_focus": "深度优化、数学证明、高级变体、工业级实现",
                "code_style": "展示多种实现方式，包括优化版本",
                "examples_complexity": "使用复杂示例，展示极端情况和性能边界",
                "skip_topics": "不跳过任何内容，全面深入讲解",
                "visual_style": "动画紧凑高效，假设观众能快速理解"
            }
        }
        return descriptions.get(self.difficulty, descriptions[DifficultyLevel.MEDIUM])
    
    def get_language_description(self) -> str:
        """获取编程语言的描述性文本"""
        descriptions = {
            ProgrammingLanguage.PYTHON: {
                "name": "Python",
                "style": "Pythonic风格，利用列表推导、内置函数等特性",
                "features": "使用Python标准库（如heapq, collections）",
                "syntax_notes": "注意缩进，使用类型提示增强可读性"
            },
            ProgrammingLanguage.JAVA: {
                "name": "Java",
                "style": "面向对象风格，使用类封装",
                "features": "使用Java集合框架（ArrayList, HashMap, PriorityQueue）",
                "syntax_notes": "明确声明类型，遵循Java命名规范"
            },
            ProgrammingLanguage.C: {
                "name": "C",
                "style": "简洁高效的过程式编程风格",
                "features": "使用指针和数组操作，手动内存管理（malloc/free）",
                "syntax_notes": "注意指针运算和内存安全，使用结构体组织数据"
            },
            ProgrammingLanguage.CPP: {
                "name": "C++",
                "style": "兼顾性能和可读性，使用现代C++特性",
                "features": "使用STL容器和算法（vector, map, priority_queue）",
                "syntax_notes": "注意内存管理，适当使用引用和指针"
            },
            ProgrammingLanguage.JAVASCRIPT: {
                "name": "JavaScript",
                "style": "函数式与面向对象混合风格",
                "features": "使用ES6+特性（箭头函数、解构、Map/Set）",
                "syntax_notes": "注意异步处理，使用const/let声明变量"
            },
            ProgrammingLanguage.GO: {
                "name": "Go",
                "style": "简洁务实的Go风格",
                "features": "使用Go标准库和slice、map等内置类型",
                "syntax_notes": "遵循Go惯例，适当使用goroutine展示并发"
            },
            ProgrammingLanguage.RUST: {
                "name": "Rust",
                "style": "安全高效的Rust风格",
                "features": "利用所有权系统和标准库集合",
                "syntax_notes": "展示Rust的内存安全特性，使用Result处理错误"
            },
            ProgrammingLanguage.CSHARP: {
                "name": "C#",
                "style": "现代C#风格，使用LINQ和泛型",
                "features": "使用.NET集合类（List, Dictionary, SortedSet）",
                "syntax_notes": "使用C#命名规范，展示属性和表达式主体成员"
            },
            ProgrammingLanguage.PSEUDOCODE: {
                "name": "伪代码",
                "style": "语言无关的伪代码风格",
                "features": "使用通用数据结构描述，不依赖特定语言",
                "syntax_notes": "注重算法逻辑的清晰表达，而非语法细节"
            }
        }
        return descriptions.get(self.programming_language, descriptions[ProgrammingLanguage.PYTHON])
    
    def generate_profile_prompt(self) -> str:
        """生成完整的用户配置提示词片段"""
        age_desc = self.get_age_group_description()
        diff_desc = self.get_difficulty_description()
        lang_desc = self.get_language_description()
        
        prompt = f"""
## 用户配置 (User Profile)

### 目标受众
- **人群**: {age_desc['audience']}
- **背景知识**: {age_desc['background']}
- **讲解风格**: {age_desc['style']}
- **节奏要求**: {age_desc['pace']}
- **用语规范**: {age_desc['vocabulary']}
- **举例偏好**: {age_desc['examples']}
- **深度要求**: {age_desc['depth']}

### 难度级别: {diff_desc['level']}
- **前置知识**: {diff_desc['prerequisites']}
- **内容重点**: {diff_desc['content_focus']}
- **代码风格**: {diff_desc['code_style']}
- **示例复杂度**: {diff_desc['examples_complexity']}
- **可跳过内容**: {diff_desc['skip_topics']}
- **动画风格**: {diff_desc['visual_style']}

### 编程语言: {lang_desc['name']}
- **代码风格**: {lang_desc['style']}
- **语言特性**: {lang_desc['features']}
- **语法注意**: {lang_desc['syntax_notes']}
"""
        return prompt
    
    def to_dict(self) -> dict:
        """转换为字典格式，便于序列化"""
        return {
            "age_group": self.age_group.value,
            "programming_language": self.programming_language.value,
            "difficulty": self.difficulty.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """从字典创建UserProfile实例"""
        return cls(
            age_group=AgeGroup(data.get("age_group", "college")),
            programming_language=ProgrammingLanguage(data.get("programming_language", "Python")),
            difficulty=DifficultyLevel(data.get("difficulty", "medium"))
        )


def get_default_profile() -> UserProfile:
    """获取默认用户配置"""
    return UserProfile()


# 便捷函数：根据字符串参数创建配置
def create_profile(
    age_group: str = "college",
    programming_language: str = "Python",
    difficulty: str = "medium"
) -> UserProfile:
    """
    根据字符串参数创建用户配置
    
    Args:
        age_group: "high_school" | "college" | "professional"
        programming_language: "Python" | "Java" | "C++" | "JavaScript" | "Go" | "Rust" | "C#" | "伪代码"
        difficulty: "low" | "medium" | "high"
    
    Returns:
        UserProfile 实例
    """
    # 映射编程语言字符串到枚举
    lang_mapping = {
        "python": ProgrammingLanguage.PYTHON,
        "java": ProgrammingLanguage.JAVA,
        "c": ProgrammingLanguage.C,
        "c++": ProgrammingLanguage.CPP,
        "cpp": ProgrammingLanguage.CPP,
        "javascript": ProgrammingLanguage.JAVASCRIPT,
        "js": ProgrammingLanguage.JAVASCRIPT,
        "go": ProgrammingLanguage.GO,
        "rust": ProgrammingLanguage.RUST,
        "c#": ProgrammingLanguage.CSHARP,
        "csharp": ProgrammingLanguage.CSHARP,
        "伪代码": ProgrammingLanguage.PSEUDOCODE,
        "pseudocode": ProgrammingLanguage.PSEUDOCODE,
    }
    
    return UserProfile(
        age_group=AgeGroup(age_group.lower()),
        programming_language=lang_mapping.get(programming_language.lower(), ProgrammingLanguage.PYTHON),
        difficulty=DifficultyLevel(difficulty.lower())
    )
