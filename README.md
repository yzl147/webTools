# 文件转换与翻译工具

支持文件格式转换和文件翻译的 Web 工具。

## 功能

### 格式转换
- DOCX ↔ PDF 互转
- Markdown (MD) 与 DOCX/PDF 互转

### 文件翻译
支持两种翻译模式：
- **LibreTranslate**：开源翻译服务，可自部署
- **大模型翻译**：支持 OpenAI GPT 和 Anthropic Claude

## 技术栈

- **后端**：Python FastAPI
- **文件转换**：docx2pdf, pdf2docx, Pandoc
- **翻译**：LibreTranslate API / OpenAI / Anthropic

## 安装

### 1. 安装系统依赖

```bash
# Ubuntu/Debian
apt update
apt install pandoc

# macOS
brew install pandoc
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

或使用启动脚本：

```bash
chmod +x start.sh
./start.sh
```

访问 http://localhost:8000

## 支持的文件格式

| 格式 | 转换 | 翻译 |
|------|------|------|
| DOCX | ✓ | ✓ |
| PDF | ✓ | ✓ |
| MD | ✓ | ✓ |

## API 接口

### 格式转换
```
POST /api/convert
Content-Type: multipart/form-data

file: 上传文件
target_format: pdf | docx | md
```

### 文件翻译
```
POST /api/translate
Content-Type: multipart/form-data

file: 上传文件
mode: libretranslate | llm
target_language: 目标语言代码 (如 zh, en, ja)

# LibreTranslate 模式
lt_host: 服务器地址
lt_port: 端口
lt_api_key: API Key (可选)

# 大模型模式
llm_type: openai | anthropic
api_base: API 地址 (可选)
api_key: API Key
model: 模型名称
```

## 环境要求

- Python 3.8+
- Pandoc (用于 Markdown 转换)
