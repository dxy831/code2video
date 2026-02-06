# Code2Video 前后端对接文档

## 目录

- [一、项目概述](#一项目概述)
- [二、环境准备](#二环境准备)
- [三、核心接口说明](#三核心接口说明)
- [四、输入参数详解](#四输入参数详解)
- [五、输出结果说明](#五输出结果说明)
- [六、调用方式](#六调用方式)
- [七、错误处理](#七错误处理)
- [八、性能与资源](#八性能与资源)
- [九、完整示例](#九完整示例)

---

## 一、项目概述

### 1.1 功能简介

Code2Video 是一个**AI 驱动的教学视频自动生成系统**。用户输入一个知识点（如"二分搜索"、"快速排序"），系统会自动：

1. 📝 生成教学大纲（Outline）
2. 🎬 生成分镜脚本（Storyboard）
3. 💻 生成 Manim 动画代码
4. 🎥 渲染视频片段
5. 🔗 合并成完整教学视频

### 1.2 技术栈

- **Python 3.9+**
- **Manim Community** (动画渲染引擎)
- **LLM API** (Claude/GPT/Gemini)
- **FFmpeg** (视频处理)

### 1.3 核心流程

```
用户输入 → 大纲生成 → 分镜生成 → 代码生成 → 视频渲染 → 视频合并 → 输出
   ↓           ↓           ↓           ↓           ↓           ↓
知识点    outline.json  storyboard.json  section_*.py  section_*.mp4  final.mp4
用户画像
```

---

## 二、环境准备

### 2.1 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 10 / Ubuntu 20.04 | Windows 11 / Ubuntu 22.04 |
| Python | 3.9+ | 3.10+ |
| 内存 | 8GB | 16GB+ |
| CPU | 4 核 | 8 核+ |
| 磁盘空间 | 10GB | 20GB+ |

### 2.2 依赖安装

```bash
cd code2video/src/
pip install -r requirements.txt
```

### 2.3 LaTeX 安装（必需）

视频中的数学公式渲染需要 LaTeX 支持。请根据操作系统安装：

#### Windows

```bash
# 方法1: 使用 winget（推荐）
winget install MiKTeX.MiKTeX

# 方法2: 手动下载安装
# 访问 https://miktex.org/download 下载安装程序
```

#### macOS

```bash
# 使用 Homebrew
brew install --cask mactex-no-gui

# 或安装更小的版本
brew install --cask basictex
```

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
```

#### 验证安装

安装后重启终端，运行以下命令验证：

```bash
# Windows
where latex

# macOS / Linux
which latex
```

如果显示 LaTeX 路径，说明安装成功。

> ⚠️ **重要提示**：如果没有安装 LaTeX，视频中的数学公式（如 `O(log n)`、`2^7 = 128`）将无法正常显示！

### 2.4 API 密钥配置

编辑 `src/api_config.json`：

```json
{
    "openai": {
        "api_key": "sk-xxx",
        "base_url": "https://api.openai.com/v1"
    },
    "claude": {
        "api_key": "sk-ant-xxx"
    },
    "gemini": {
        "api_key": "AIzaxxx"
    },
    "iconfinder": {
        "api_key": "xxx"  // 可选，用于下载图标素材
    }
}
```

---

## 三、核心接口说明

### 3.1 命令行调用（推荐用于后端集成）

**⚠️ 重要提示**：必须在 `code2video/src/` 目录下执行命令！

```bash
cd code2video/src/

python agent.py \
  --API "claude" \
  --folder_prefix "USER_001" \
  --knowledge_point "二分搜索" \
  --user_profile "我是17岁的高中生,想学习入门级的Python编程" \
  --duration 5
```

**完整调用示例（包含所有常用参数）**：

```bash
python agent.py \
  --API "claude" \
  --folder_prefix "USER_001" \
  --knowledge_point "二分搜索" \
  --user_profile "我是17岁的高中生,想要的学习难度是入门级,选择的编程语言是Python,目标是利用暑假成功入门Python" \
  --duration 5 \
  --max_code_token_length 20000 \
  --max_regenerate_tries 10 \
  --use_feedback \
  --feedback_rounds 2
```

**完整参数调用**：

这是包含所有参数的完整调用：

```batch
python agent.py \
  --API "claude" \
  --folder_prefix "USER_001" \
  --use_feedback \
  --use_assets \
  --max_code_token_length 20000 \
  --max_fix_bug_tries 10 \
  --max_regenerate_tries 10 \
  --max_feedback_gen_code_tries 5 \
  --max_mllm_fix_bugs_tries 5 \
  --feedback_rounds 2 \
  --knowledge_point "二分搜索" \
  --user_profile "我是17岁的高中生,想要的学习难度是入门级,选择的编程语言是Python,目标是利用暑假成功入门Python,完成一个自己的小项目,目前已有的知识储备是Python的输入输出语法和最基础的函数的语法"
```

**⚠️ 注意事项**：
- `--user_profile` 的值如果包含空格，需要用引号包裹
- 必须先配置好 `api_config.json` 中的 API 密钥

### 3.2 Python 模块调用

```python
from agent import TeachingVideoAgent, RunConfig
from gpt_request import request_claude_token
from prompts.user_profile import create_profile_from_text, parse_profile_with_ai_sync

# 1. 创建用户画像
user_profile = create_profile_from_text("我是17岁的高中生，想学习入门级的Python编程")

# 2. 可选：使用 AI 解析用户画像（获得更精准的配置）
parsed = parse_profile_with_ai_sync(user_profile.raw_input, request_claude_token)
if parsed:
    user_profile.update_with_parsed_profile(parsed)

# 3. 创建配置
cfg = RunConfig(
    api=request_claude_token,
    user_profile=user_profile,
    duration=5,  # 目标视频时长（分钟）
    use_feedback=False,  # 是否使用 MLLM 反馈优化
    use_assets=False,    # 是否下载外部图标素材
)

# 4. 创建 Agent 并生成视频
agent = TeachingVideoAgent(
    idx=0,
    knowledge_point="二分搜索",
    folder="CASES/USER_001_OUTPUT",
    cfg=cfg,
)

# 5. 执行完整流程
video_path = agent.GENERATE_VIDEO()
print(f"视频已生成: {video_path}")
```

---

## 四、输入参数详解

### 4.1 必需参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `--knowledge_point` | string | 要生成视频的知识点 | `"二分搜索"` |
| `--API` | string | 使用的 LLM API | `"claude"` / `"gpt-4o"` / `"Gemini"` |

### 4.2 用户画像参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `--user_profile` | string | 用户画像的自然语言描述 | `"我是17岁的高中生，想要的学习难度是入门级，选择的编程语言是Python，目标是利用暑假成功入门Python，目前已有的知识储备是Python的输入输出语法"` |

**用户画像会影响：**
- 讲解的深度和风格
- 示例的复杂度
- 代码注释的详细程度
- 类比场景的选择
- 动画节奏

### 4.3 可选参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `--duration` | int | 5 | 目标视频时长（分钟） |
| `--folder_prefix` | string | "TEST" | 输出文件夹前缀 |
| `--use_feedback` | flag | False | 是否启用 MLLM 视觉反馈优化 |
| `--use_assets` | flag | False | 是否下载外部图标素材 |
| `--max_code_token_length` | int | 10000 | API 最大输出 token |
| `--max_regenerate_tries` | int | 10 | 生成失败时的最大重试次数 |
| `--feedback_rounds` | int | 2 | MLLM 反馈优化轮数 |

### 4.4 支持的 API 选项

| API 名称 | 参数值 | 推荐场景 |
|----------|--------|---------|
| Claude | `"claude"` | **推荐**，Manim 代码质量最高 |
| GPT-4o | `"gpt-4o"` | 通用场景 |
| GPT-4.1 | `"gpt-41"` | 高质量需求 |
| GPT-5 | `"gpt-5"` | 最新模型 |
| GPT-o4mini | `"gpt-o4mini"` | 成本敏感场景 |
| Gemini | `"Gemini"` | 视觉反馈优化 |

---

## 五、输出结果说明

### 5.1 输出目录结构

```
src/CASES/{folder_prefix}_{API}/
└── {idx}-{knowledge_point}/
    ├── outline.json           # 教学大纲
    ├── storyboard.json        # 分镜脚本
    ├── storyboard_with_assets.json  # 带素材的分镜（可选）
    ├── section_0_intro.py     # 章节0的 Manim 代码
    ├── section_1.py           # 章节1的 Manim 代码
    ├── section_2.py           # ...
    ├── ...
    ├── media/                 # Manim 渲染的中间文件
    │   └── videos/
    │       └── section_*/
    │           └── 480p15/
    │               └── *.mp4  # 各章节视频
    ├── optimized_videos/      # MLLM 优化后的视频（可选）
    ├── video_list.txt         # 视频合并列表
    └── {knowledge_point}.mp4  # ⭐ 最终输出视频
```

### 5.2 关键输出文件

#### 5.2.1 `outline.json` - 教学大纲

```json
{
    "topic": "二分搜索：高效查找的艺术",
    "target_audience": "17岁高中生，Python入门学习者",
    "programming_language": "Python",
    "difficulty_level": "入门级",
    "data_case_definition": "有序数组 [1, 3, 5, 7, 9, 11, 13]，查找目标 7",
    "algorithm_components": ["有序数组", "双指针"],
    "sections": [
        {
            "id": "section_0_intro",
            "title": "场景引入",
            "content": "查字典的类比...",
            "code_mapping": "None"
        },
        // ...
    ]
}
```

#### 5.2.2 `storyboard.json` - 分镜脚本

```json
{
    "sections": [
        {
            "id": "section_0_intro",
            "title": "场景引入：你是怎么查字典的？",
            "estimated_duration": 45,
            "lecture_lines": [
                "想象一下，你手里有一本厚厚的英语词典...",
                "笨方法：从第一页开始，一页一页翻...",
                "聪明方法：先翻到中间..."
            ],
            "animations": [
                "Visual: FadeIn title at top center.",
                "Visual: Create dictionary book icon.",
                "Animation: Show page flipping animation."
            ]
        },
        // ...
    ]
}
```

#### 5.2.3 最终视频

- **路径**: `{output_dir}/{knowledge_point}.mp4`
- **格式**: MP4 (H.264)
- **分辨率**: 480p (可配置)
- **时长**: 根据 `--duration` 参数和内容复杂度决定

---

## 六、调用方式

### 6.1 同步调用（简单场景）

直接调用 `agent.GENERATE_VIDEO()`，会阻塞直到视频生成完成。

```python
video_path = agent.GENERATE_VIDEO()
```

**适用场景**: 后台任务、CLI 工具

### 6.2 异步调用（Web 服务推荐）

将视频生成任务放入异步队列（如 Celery、RQ）：

```python
# tasks.py (Celery 示例)
from celery import Celery
from agent import TeachingVideoAgent, RunConfig
from gpt_request import request_claude_token

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True)
def generate_video_task(self, knowledge_point, user_profile_text, user_id):
    """异步视频生成任务"""
    from prompts.user_profile import create_profile_from_text
    
    user_profile = create_profile_from_text(user_profile_text)
    
    cfg = RunConfig(
        api=request_claude_token,
        user_profile=user_profile,
        duration=5,
    )
    
    agent = TeachingVideoAgent(
        idx=0,
        knowledge_point=knowledge_point,
        folder=f"CASES/USER_{user_id}",
        cfg=cfg,
    )
    
    # 可以在这里更新任务进度
    self.update_state(state='PROGRESS', meta={'stage': '生成大纲'})
    agent.generate_outline()
    
    self.update_state(state='PROGRESS', meta={'stage': '生成分镜'})
    agent.generate_storyboard()
    
    self.update_state(state='PROGRESS', meta={'stage': '生成代码'})
    agent.generate_codes()
    
    self.update_state(state='PROGRESS', meta={'stage': '渲染视频'})
    agent.render_all_sections()
    
    self.update_state(state='PROGRESS', meta={'stage': '合并视频'})
    video_path = agent.merge_videos()
    
    return video_path
```

### 6.3 分步调用（精细控制）

如果需要在各阶段之间进行干预或保存中间状态：

```python
# 1. 生成大纲
outline = agent.generate_outline()
# 可以在这里让用户确认/修改大纲

# 2. 生成分镜
sections = agent.generate_storyboard()
# 可以在这里让用户确认/修改分镜

# 3. 生成代码（并行）
codes = agent.generate_codes()

# 4. 渲染所有章节（并行）
results = agent.render_all_sections()

# 5. 合并视频
final_video = agent.merge_videos()
```

---

## 七、错误处理

### 7.1 常见错误及解决方案

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `JSON Error: Expecting ',' delimiter` | LLM 输出被截断或格式错误 | 增加 `--max_code_token_length` |
| `API 请求多次失败` | API 密钥无效或网络问题 | 检查 `api_config.json` |
| `大纲格式多次无效` | LLM 未按 JSON 格式输出 | 增加重试次数或更换 API |
| `Manim 渲染超时` | 代码复杂度过高或死循环 | 检查生成的代码 |
| `没有可用视频进行合并` | 所有章节渲染失败 | 检查 Manim 环境和代码 |

### 7.2 错误码设计建议

```python
class VideoGenerationError(Exception):
    """视频生成错误基类"""
    pass

class OutlineGenerationError(VideoGenerationError):
    """大纲生成失败"""
    code = 1001

class StoryboardGenerationError(VideoGenerationError):
    """分镜生成失败"""
    code = 1002

class CodeGenerationError(VideoGenerationError):
    """代码生成失败"""
    code = 1003

class RenderingError(VideoGenerationError):
    """渲染失败"""
    code = 1004

class MergingError(VideoGenerationError):
    """合并失败"""
    code = 1005
```

### 7.3 重试机制

系统内置重试机制：

- 大纲生成：最多 10 次（`--max_regenerate_tries`）
- 分镜生成：最多 10 次
- 代码修复：最多 10 次（`--max_fix_bug_tries`）
- MLLM 优化：最多 3 次（`--max_feedback_gen_code_tries`）

---

## 八、性能与资源

### 8.1 生成时间估算

| 视频时长目标 | 章节数 | 预计生成时间 | Token 消耗 |
|-------------|-------|-------------|-----------|
| 3 分钟 | 6-8 | 5-10 分钟 | 50,000+ |
| 5 分钟 | 8-12 | 10-20 分钟 | 80,000+ |
| 10 分钟 | 12-18 | 30-50 分钟 | 150,000+ |

### 8.2 资源消耗

- **CPU**: 渲染期间会占用多核（可通过 `--max_workers` 控制并行数）
- **内存**: 峰值约 4-8GB
- **磁盘**: 每个视频约 100-500MB（含中间文件）

### 8.3 并行渲染配置

```bash
# 限制并行进程数（默认自动检测）
python agent.py ... --max_workers 4
```

---

## 九、完整示例

### 9.1 最简调用

```bash
cd code2video/src/

python agent.py \
  --knowledge_point "二分搜索" \
  --API "claude"
```

### 9.2 带用户画像调用

```bash
python agent.py \
  --knowledge_point "二分搜索" \
  --API "claude" \
  --user_profile "我是17岁的高中生，想要的学习难度是入门级，选择的编程语言是Python，目标是利用暑假成功入门Python，完成一个自己的小项目，目前已有的知识储备是Python的输入输出语法和最基础的函数的语法" \
  --duration 5 \
  --folder_prefix "STUDENT_001"
```

### 9.3 完整生产环境调用

```bash
python agent.py \
  --knowledge_point "快速排序" \
  --API "claude" \
  --user_profile "我是计算机专业大二学生，已经学过数据结构基础，想深入理解快排的分治思想和时间复杂度分析" \
  --duration 8 \
  --folder_prefix "PROD_USER_12345" \
  --use_feedback \
  --feedback_rounds 2 \
  --max_code_token_length 15000 \
  --max_regenerate_tries 5
```

### 9.4 Web API 封装示例（Flask）

```python
from flask import Flask, request, jsonify
from threading import Thread
import uuid
import os

app = Flask(__name__)

# 存储任务状态
tasks = {}

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """发起视频生成任务"""
    data = request.json
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'pending', 'progress': 0}
    
    # 在后台线程中执行（生产环境建议用 Celery）
    thread = Thread(target=run_generation, args=(
        task_id,
        data.get('knowledge_point'),
        data.get('user_profile', ''),
        data.get('duration', 5),
    ))
    thread.start()
    
    return jsonify({'task_id': task_id})

@app.route('/api/status/<task_id>')
def get_status(task_id):
    """查询任务状态"""
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(tasks[task_id])

@app.route('/api/download/<task_id>')
def download_video(task_id):
    """下载生成的视频"""
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    if task['status'] != 'completed':
        return jsonify({'error': 'Video not ready'}), 400
    
    return send_file(task['video_path'])

def run_generation(task_id, knowledge_point, user_profile_text, duration):
    """后台执行视频生成"""
    from agent import TeachingVideoAgent, RunConfig
    from gpt_request import request_claude_token
    from prompts.user_profile import create_profile_from_text
    
    try:
        tasks[task_id]['status'] = 'running'
        
        user_profile = create_profile_from_text(user_profile_text)
        cfg = RunConfig(
            api=request_claude_token,
            user_profile=user_profile,
            duration=duration,
        )
        
        agent = TeachingVideoAgent(
            idx=0,
            knowledge_point=knowledge_point,
            folder=f"CASES/TASK_{task_id}",
            cfg=cfg,
        )
        
        tasks[task_id]['progress'] = 10
        agent.generate_outline()
        
        tasks[task_id]['progress'] = 25
        agent.generate_storyboard()
        
        tasks[task_id]['progress'] = 40
        agent.generate_codes()
        
        tasks[task_id]['progress'] = 60
        agent.render_all_sections()
        
        tasks[task_id]['progress'] = 90
        video_path = agent.merge_videos()
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        tasks[task_id]['video_path'] = video_path
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 附录

### A. API 配置模板

```json
{
    "openai": {
        "api_key": "YOUR_OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1"
    },
    "claude": {
        "api_key": "YOUR_CLAUDE_API_KEY"
    },
    "gemini": {
        "api_key": "YOUR_GEMINI_API_KEY"
    },
    "iconfinder": {
        "api_key": "YOUR_ICONFINDER_API_KEY"
    }
}
```

### B. 用户画像字段说明

用户画像可以包含以下信息（自然语言描述即可，AI 会自动解析）：

- **年龄/身份**: 高中生、大学生、在职人员等
- **知识背景**: 已有的编程基础、数学基础
- **学习目标**: 考试、项目、兴趣等
- **编程语言偏好**: Python、Java、C++ 等
- **难度偏好**: 入门级、进阶、专家级
- **时间安排**: 学习的时间规划

---

*文档版本: 1.0.0*  
*最后更新: 2026-01-28*
