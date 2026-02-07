# Code2Video

将编程知识点自动转换为教学视频的 API 服务。

## 功能特性

- ✅ **SSE 流式输出**: 实时返回视频生成进度
- ✅ **任务状态追踪**: 每个子任务使用 UUID 唯一标识
- ✅ **API Key 认证**: 安全的接口访问控制
- ✅ **Redis 任务队列**: 支持并发任务管理
- ✅ **文件 SHA256 命名**: 视频文件永久存储
- ✅ **断点续传**: 支持 Range 请求下载大文件

## 快速开始

### 1. 安装依赖

使用 uv 管理项目：

```bash
cd code2video
uv sync
```

### 2. 启动 Redis

确保 Redis 服务已启动：

```bash
redis-cli ping
# 应返回: PONG
```

### 3. 启动服务

```bash
# 终端 1: 启动 Celery Worker
uv run celery -A src.api.tasks.celery_app worker --loglevel=info --pool=solo -Q video_generation

# 终端 2: 启动 FastAPI
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc
- 健康检查: http://localhost:8080/health

## API 接口

### 生成视频

```bash
curl -N -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -H "X-API-Key: dev-api-key-12345" \
  -X POST http://localhost:8080/api/v1/generate-video \
  -d '{
    "knowledge_point": "二分搜索",
    "age": 20,
    "gender": "男",
    "language": "Python",
    "duration": 5
  }'
```

### 下载视频

```bash
curl -H "X-API-Key: dev-api-key-12345" \
  -o video.mp4 \
  http://localhost:8080/api/v1/files/{filename}
```

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| API_KEYS | dev-api-key-12345 | API 密钥（逗号分隔多个） |
| REDIS_URL | redis://localhost:6379/0 | Redis 连接地址 |
| DEFAULT_API | claude | 默认 LLM 模型 |

## 许可证

MIT License
