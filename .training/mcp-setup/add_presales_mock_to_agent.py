#!/usr/bin/env python3
"""
QwenPaw Agent MCP 接入脚本：将 presales_mock 登记到指定 Agent 的 agent.json

背景（C8/C10 翻车点修复）：
- QwenPaw 实际工作目录优先级：QWENPAW_WORKING_DIR/COPAW_WORKING_DIR env > ~/.copaw（legacy）> ~/.qwenpaw
- MCP clients 配置层级在【Agent 级】（agent.json），不在全局 config.json
- AgentConfigWatcher 以 2s 频率轮询，写入后无需重启

使用方法：
    python3 add_presales_mock_to_agent.py                # 默认改 default agent
    python3 add_presales_mock_to_agent.py --agent default
    python3 add_presales_mock_to_agent.py --remove       # 卸载

学员现场可直接执行；幂等（多次执行结果一致）；自动备份 .bak。
"""
import argparse
import json
import os
import pathlib
import shutil
import sys
import time

CLIENT_NAME = "presales_mock"
DEFAULT_URL = "http://localhost:9876/mcp"

PRESALES_MOCK_CONFIG = {
    "name": CLIENT_NAME,
    "description": "售前演示助手 mock MCP server（课程实验载体）",
    "enabled": True,
    "transport": "streamable_http",
    "url": DEFAULT_URL,
    "headers": {},
    "command": "",
    "args": [],
    "env": {},
    "cwd": "",
}


def resolve_working_dir() -> pathlib.Path:
    """与 QwenPaw constant.py 中的 WORKING_DIR 解析逻辑保持一致。"""
    for env_key in ("QWENPAW_WORKING_DIR", "COPAW_WORKING_DIR"):
        v = os.environ.get(env_key)
        if v:
            return pathlib.Path(v).expanduser()
    legacy = pathlib.Path.home() / ".copaw"
    if legacy.exists():
        return legacy
    return pathlib.Path.home() / ".qwenpaw"


def main() -> int:
    parser = argparse.ArgumentParser(description="为指定 Agent 登记/卸载 presales_mock MCP client")
    parser.add_argument("--agent", default="default", help="Agent 工作区名（默认 default）")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"mock server 地址（默认 {DEFAULT_URL}）")
    parser.add_argument("--remove", action="store_true", help="移除 presales_mock client")
    args = parser.parse_args()

    working_dir = resolve_working_dir()
    agent_json = working_dir / "workspaces" / args.agent / "agent.json"

    if not agent_json.exists():
        print(f"❌ agent.json 不存在: {agent_json}")
        print(f"   请先确认 QwenPaw 已初始化、Agent '{args.agent}' 存在。")
        return 1

    # 备份
    backup = agent_json.with_suffix(f".json.bak-{int(time.time())}")
    shutil.copy(agent_json, backup)

    cfg = json.loads(agent_json.read_text(encoding="utf-8"))
    cfg.setdefault("mcp", {}).setdefault("clients", {})

    if args.remove:
        if CLIENT_NAME in cfg["mcp"]["clients"]:
            del cfg["mcp"]["clients"][CLIENT_NAME]
            agent_json.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"✅ 已移除 {CLIENT_NAME}（备份: {backup.name}）")
        else:
            print(f"ℹ️  {CLIENT_NAME} 未登记，无需移除")
        return 0

    # 写入（幂等）
    config = dict(PRESALES_MOCK_CONFIG)
    config["url"] = args.url
    cfg["mcp"]["clients"][CLIENT_NAME] = config
    agent_json.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ 已登记 {CLIENT_NAME} 到 {agent_json}")
    print(f"   URL: {args.url}")
    print(f"   备份: {backup.name}")
    print(f"   现有 clients: {list(cfg['mcp']['clients'].keys())}")
    print()
    print("⏳ 等待 AgentConfigWatcher 热重载（约 2-5 秒）...")
    print("   验证：tail -f /tmp/qwenpaw.log | grep -i presales")
    print("   期望：MCP client connected: presales_mock")
    return 0


if __name__ == "__main__":
    sys.exit(main())
