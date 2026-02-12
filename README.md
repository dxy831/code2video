curl -N -X POST http://localhost:8081/api/v1/generate-video -H "Content-Type: application/json" -H "X-API-Key: dev-api-key-12345" -d @request.json


# Code2Video Docker 部署指南

本文档介绍如何使用 Docker 部署 Code2Video API 服务。

## 📋 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB 内存（Manim 渲染需要）
- 至少 10GB 磁盘空间（LaTeX 和字体包较大）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/dxy831/code2video.git
cd code2video
```

### 2. 配置 LLM API 密钥

编辑 `src/api_config.json` 文件，填入你的 API 密钥：

```bash
nano src/api_config.json
```

配置文件格式：
```json
{
    "claude": {
        "base_url": "https://api.anthropic.com/v1",
        "api_version": "",
        "api_key": "sk-ant-xxxxx",
        "model": "claude-opus-4-5-20251101-cc"
    },
    "gpt4o": {
        "base_url": "https://api.openai.com/v1",
        "api_version": "2024-03-01-preview",
        "api_key": "sk-xxxxx",
        "model": "gpt-4o"
    },
    "gpt-41": {
        "base_url": "https://api.openai.com/v1",
        "api_version": "2024-03-01-preview",
        "api_key": "sk-xxxxx",
        "model": "gpt-4o"
    },
    "gpt5": {
        "base_url": "https://api.openai.com/v1",
        "api_version": "",
        "api_key": "sk-xxxxx",
        "model": "gpt-5"
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1",
        "api_version": "",
        "api_key": "xxxxx",
        "model": "gemini-2.5-pro"
    },
    "iconfinder": {
        "api_key": "YOUR_ICONFINDER_KEY"
    }
}
```

**支持的 LLM 模型**：
| 配置名 | 说明 |
|--------|------|
| `claude` | Claude 模型（默认） |
| `gpt4o` | GPT-4o 模型 |
| `gpt-41` | GPT-4 系列模型 |
| `gpt5` | GPT-5 模型 |
| `gemini` | Google Gemini 模型 |

> **注意**：`src/api_config.json` 会被打包进 Docker 镜像。如果需要在部署后修改密钥而不重新构建镜像，可以取消 `docker-compose.yml` 中的 Volume 挂载注释。

### 3. 配置环境变量（可选）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

主要配置项：
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `API_KEYS` | API 认证密钥（前端调用时需要） | `dev-api-key-12345` |
| `DEFAULT_API` | 默认 LLM（claude/gpt4o/gpt-41/gpt5/gemini） | `claude` |
| `API_PORT` | API 服务端口 | `8081` |
| `DEBUG` | 调试模式 | `false` |

### 4. 启动服务

```bash
# 构建并启动所有服务（后台运行）
docker-compose up -d --build

# 查看启动日志
docker-compose logs -f
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8081/health

# 查看 API 文档
# 浏览器打开: http://localhost:8081/docs
```

## 📡 API 使用

### 认证方式

所有 `/api/v1/*` 接口需要在请求头中携带 API Key：

```bash
curl -H "X-API-Key: dev-api-key-12345" http://localhost:8081/api/v1/...
```

---

## 📋 API 接口列表

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/` | GET | ❌ | 服务信息（根路径） |
| `/health` | GET | ❌ | 健康检查 |
| `/docs` | GET | ❌ | Swagger API 文档 |
| `/api/v1/generate-video` | POST | ✅ | 生成视频（SSE 流式返回） |
| `/api/v1/tasks/{task_id}` | GET | ✅ | 查询任务状态 |
| `/api/v1/files/{filename}` | GET | ✅ | 下载视频文件 |
| `/api/v1/files/{filename}` | HEAD | ✅ | 获取文件信息 |
| `/api/v1/files/{filename}/metadata` | GET | ✅ | 获取视频元信息 |

---

### 1. 服务信息

```bash
curl http://localhost:8081/
```

**响应示例**：
```json
{
    "service": "Code2Video API",
    "version": "1.0.0",
    "docs": "/docs",
    "health": "/health"
}
```

---

### 2. 健康检查

```bash
curl http://localhost:8081/health
```

**响应示例**：
```json
{
    "status": "ok",
    "redis": "connected",
    "workers": 4,
    "version": "1.0.0"
}
```

---

### 3. 生成视频（SSE 流式返回）

```bash
curl -N \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -H "X-API-Key: dev-api-key-12345" \
  -X POST http://localhost:8081/api/v1/generate-video \
  -d '{
    "knowledge_point": "冒泡排序",
    "age": 20,
    "gender": "男",
    "language": "Python",
    "duration": 5,
    "extra_info": "我是大一学生，有一定编程基础，目标是利用寒假完成一个小项目"
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_point` | string | ✅ | 要生成视频的知识点 |
| `age` | int | ❌ | 用户年龄（1-120） |
| `gender` | string | ❌ | 用户性别（"男"/"女"） |
| `language` | string | ❌ | 编程语言，默认 "Python" |
| `duration` | int | ❌ | 视频时长（分钟），范围 1-30，默认 5 |
| `extra_info` | string | ❌ | 额外的用户信息描述（自然语言） |
| `use_feedback` | bool | ❌ | 是否使用 MLLM 反馈优化，默认 true |
| `use_assets` | bool | ❌ | 是否使用外部素材，默认 true |
| `api_model` | string | ❌ | 指定 LLM 模型（claude/gpt4o/gpt-41/gpt5/gemini），默认使用环境变量 DEFAULT_API |

**响应格式**（SSE 事件流）：

SSE 事件类型：
- `running`: 任务进行中
- `finished`: 子任务完成
- `failed`: 任务失败
- `result`: 最终结果

```
event: running
data: {"task_id":"uuid","message":"正在解析用户画像。"}

event: finished
data: {"task_id":"uuid","message":"用户画像解析成功。"}

event: running
data: {"task_id":"uuid","message":"正在生成视频大纲..."}

event: finished
data: {"task_id":"uuid","message":"大纲生成成功。"}

event: running
data: {"task_id":"uuid","message":"正在生成 Manim 代码..."}

event: running
data: {"task_id":"uuid","message":"正在渲染视频..."}

event: result
data: {"message":"视频生成成功。","data":{"video_file":"a1b2c3...sha256.mp4"}}
```

**失败响应示例**：
```
event: failed
data: {"task_id":"uuid","message":"视频渲染失败: 内存不足"}
```

---

### 4. 查询任务状态

用于断线重连后查询任务的最终状态。

```bash
curl -H "X-API-Key: dev-api-key-12345" \
  http://localhost:8081/api/v1/tasks/{task_id}
```

**响应示例**：
```json
{
    "task_id": "abc123-def456-...",
    "status": "SUCCESS",
    "result": {
        "video_file": "a1b2c3...sha256.mp4"
    },
    "error": null
}
```

**任务状态说明**：
| 状态 | 说明 |
|------|------|
| `PENDING` | 等待执行 |
| `STARTED` | 正在执行 |
| `SUCCESS` | 执行成功 |
| `FAILURE` | 执行失败 |

---

### 5. 下载视频文件

支持 Range 请求（断点续传）。

```bash
# 下载完整文件
curl -H "X-API-Key: dev-api-key-12345" \
  http://localhost:8081/api/v1/files/a1b2c3...sha256.mp4 \
  -o video.mp4

# 断点续传（Range 请求）
curl -H "X-API-Key: dev-api-key-12345" \
  -H "Range: bytes=0-1023" \
  http://localhost:8081/api/v1/files/a1b2c3...sha256.mp4 \
  -o video_part.mp4
```

**响应状态码**：
| 状态码 | 说明 |
|--------|------|
| 200 | 完整文件 |
| 206 | 部分内容（Range 请求） |
| 404 | 文件不存在 |
| 416 | Range 范围无效 |

---

### 6. 获取文件信息（HEAD 请求）

用于检查文件是否存在和获取文件大小，不返回文件内容。

```bash
curl -I -H "X-API-Key: dev-api-key-12345" \
  http://localhost:8081/api/v1/files/a1b2c3...sha256.mp4
```

**响应头**：
```
HTTP/1.1 200 OK
Content-Type: video/mp4
Content-Length: 12345678
Accept-Ranges: bytes
```

---

### 7. 获取视频元信息

```bash
curl -H "X-API-Key: dev-api-key-12345" \
  http://localhost:8081/api/v1/files/a1b2c3...sha256.mp4/metadata
```

**响应示例**：
```json
{
    "knowledge_point": "二分搜索",
    "language": "Python",
    "duration": 5,
    "token_usage": {
        "prompt_tokens": 10000,
        "completion_tokens": 5000,
        "total_tokens": 15000
    },
    "created_at": "2024-01-01T12:00:00"
}
```

## 🔧 运维命令

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 所有服务
docker-compose logs -f

# 只看 API 服务
docker-compose logs -f api

# 只看 Worker
docker-compose logs -f worker
```

### 重启服务

```bash
# 重启所有
docker-compose restart

# 只重启 API
docker-compose restart api
```

### 停止服务

```bash
docker-compose down
```

### 清理数据

```bash
# 停止并删除数据卷（会删除所有生成的视频！）
docker-compose down -v
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 🏗️ 架构说明

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │     API      │  │    Worker    │  │    Redis     │   │
│  │  (FastAPI)   │  │   (Celery)   │  │   (队列)     │   │
│  │   :8081      │  │              │  │   :6379      │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘   │
│         │                 │                              │
│         └────────┬────────┘                              │
│                  │                                       │
│         ┌───────────────┐                               │
│         │  video_data   │  (共享 Volume)                │
│         │  /app/data/   │                               │
│         └───────────────┘                               │
└─────────────────────────────────────────────────────────┘
```

| 服务 | 说明 | 端口 |
|------|------|------|
| **api** | FastAPI 服务，处理 HTTP 请求 | 8081 |
| **worker** | Celery Worker，执行视频生成任务 | - |
| **redis** | 消息队列 + 任务结果存储 | 6379 |

## ⚠️ 常见问题

### 1. 镜像构建很慢

首次构建需要下载 LaTeX 包（约 2GB），请耐心等待。后续构建会使用缓存。

### 2. 内存不足

Manim 渲染需要较多内存，建议至少 4GB。如果遇到 OOM，可以：
- 增加服务器内存
- 减少 Worker 并发数（`--concurrency=1`）

### 3. 中文显示乱码

确保 Docker 镜像中安装了 `fonts-noto-cjk` 字体包（Dockerfile 中已包含）。

### 4. LaTeX 渲染失败

检查 Dockerfile 中是否安装了完整的 texlive 包：
- `texlive-latex-base`
- `texlive-latex-extra`
- `texlive-fonts-recommended`
- `texlive-science`

### 5. 视频文件无法下载

检查 `video_data` Volume 是否正确挂载，API 和 Worker 需要共享同一个 Volume。

## 📝 生产环境建议

1. **修改 API_KEYS**：使用强密码，不要用默认值
2. **配置 HTTPS**：在前面加 Nginx 反向代理
3. **日志收集**：配置日志输出到文件或日志服务
4. **监控告警**：监控 `/health` 端点
5. **定期清理**：定期清理旧的视频文件

