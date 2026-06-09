# 培训学员快速起步

> 本仓库是阿里云伙伴 Qoder 培训专用 fork（基于 [agentscope-ai/QwenPaw](https://github.com/agentscope-ai/QwenPaw)），已为培训预置必要资源。
>
> **直接 clone 本 fork，不要 fork 上游 QwenPaw**——上游没有培训资源。

## 仓库已预置（你 clone 后立即可用）

| 路径 | 用途 |
|---|---|
| `.qoder/rules/spec-template.md` | M3 Spec 模式 4 段式硬模板（Qoder 自动加载） |
| `.qoder/rules/backend_specification.md` | M3 Vibe-Coding 对照演示用编码规范 |
| `.qoder/agents/env-doctor.md` | 环境诊断 Custom Agent（用 `@env-doctor` 调用） |
| `.qoder/repowiki/` | 预生成的项目知识地图（319 文件 / 3.3 MB），M1 直接可用 |
| `.training/mcp-setup/add_presales_mock_to_agent.py` | MCP mock 接入脚本（C8/C10 修复） |
| `.training/mcp-setup/接入指南.md` | MCP 接入操作步骤 |

## 三步起步

### Step 1：装环境

QwenPaw 要求 Python `>=3.10, <3.14`：

```bash
# macOS / Linux（Windows 用 WSL）
python3.12 -m venv .venv && source .venv/bin/activate

# 用阿里云镜像加速
pip install -i https://mirrors.aliyun.com/pypi/simple -e .
```

> 装依赖大约 3-5 分钟（200+ 包）。看到 `Successfully installed qwenpaw-1.x.x` 即可。

### Step 2：配 LLM Key（讲师课前在钉钉群发）

```bash
qwenpaw models config-key   # 选 dashscope，粘贴 sk-xxx
qwenpaw models set-llm      # 选 deepseek-v3.2 或 qwen-max
```

### Step 3：启动 + 接入 MCP（两个终端）

```bash
# 终端 A：启动 QwenPaw
qwenpaw app
# 看到 "QwenPaw Ready / Address: http://127.0.0.1:8088" 即成功

# 终端 B：把讲师 mock MCP server 登记到 default Agent
python3 .training/mcp-setup/add_presales_mock_to_agent.py \
    --url http://47.96.133.214:9876/mcp
# 看到 "✅ presales_mock 已加入" 即成功
```

> AgentConfigWatcher 2 秒内热重载，**无需重启 qwenpaw app**。终端 A 日志会出现 `MCP client connected: presales_mock`。

## 验证全链路打通

第二个终端跑：

```bash
curl -N -X POST http://localhost:8088/api/console/chat \
  -H 'Content-Type: application/json' \
  -d '{"input":[{"role":"user","type":"message",
       "content":[{"type":"text","text":"你好"}]}],
       "session_id":"smoke-001"}'
```

看到 SSE 流式回复 = 完整链路打通（Channel → Agent → Skill → MCP → LLM → Channel）。

## 排错入口

环境异常时直接在 Qoder 对话里说：

```
@env-doctor 帮我体检环境
```

env-doctor Custom Agent 会按 5 层检查清单（基础环境 / 项目就绪 / 服务运行态 / Qoder 客户端 / 可选增强）输出红黄绿诊断报告。

## 重要约束

- ❌ **不要 sync upstream**（同步上游会覆盖培训资源）
- ❌ **不要把 DashScope API Key 提交进仓库**（已在 .gitignore 保护，但请自检）
- ✅ M3 Spec 实操时确认 Qoder 侧栏 Active Rules 含 `spec-template`，没看到说明 Qoder 没扫到——重启 Qoder 即可

## 培训当天

| 模块 | 你要做的事 |
|---|---|
| 开场 | 跟讲师，看 60 秒震撼演示 |
| M1 Wiki | 跟讲师，按 [`m1-wiki-exercises.md`](https://your-dingtalk-doc) 做三档操练 |
| M2 Rules | 跟讲师，理解 `.qoder/rules/spec-template.md` 是怎么"自动加载"的 |
| **M3 Spec**（重头戏） | **3 人协同**做"售前演示助手改造"，按桌位卡分工 |
| M5 测试 | 跟 Test Owner 写测试 |
| M6 部署 | 跟讲师看 Qoder CLI 推上云 |

详细操练物料见钉钉知识库《Qoder 培训 · 学员包》。

---

讲师联系方式 / 钉钉群号：见课前邮件。
