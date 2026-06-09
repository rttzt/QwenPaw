---
trigger: model_decision
description: QwenPaw 存量项目改造 Spec 文档生成规范，融合 OpenSpec spec-driven schema 4 段精髓到一份文档
---

# 改造 Spec 模板 · QwenPaw 存量项目改造规范

> 本模板融合 OpenSpec spec-driven schema (Fission-AI/OpenSpec v1.4.1) 的 4 段精髓（proposal + spec + design + tasks）到一份文档。
> 所有由 Qoder Spec 模式生成的改造文档**必须**遵循本模板。
> 适用范围：QwenPaw 存量项目的新需求改造。
> 学员仅需在 Qoder Spec 模式中跟着模板填空，无需安装 OpenSpec CLI。

---

## 第 1 段：Proposal（WHY + WHAT）

> 1-2 页篇幅。回答"为什么改 + 改什么"，**不写"怎么改"**（怎么改放第 3 段）。

### 1.1 Why
<!-- 1-2 句问题陈述 + 为什么现在做 -->

### 1.2 What Changes
<!-- bullet list，标注 BREAKING -->

- ……
- ……

### 1.3 Capabilities

> 把改造拆成多个独立 capability，每个 capability 后面会单独写一段 spec。
> 命名用 kebab-case，如 `presales-demo-skill`。

**New Capabilities**（新建）：
- `<capability-name>`: <一句话描述>

**Modified Capabilities**（改造现有）：
- `<existing-capability-name>`: <要改什么 requirement>

### 1.4 Impact
<!-- 影响面：哪些代码 / API / 依赖 / 系统会被触及 -->

| 类别 | 影响 |
|---|---|
| 新增文件 | `<path>` |
| 修改文件 | `<path>`（**慎重**：列影响面，下文 Decisions 段必须有对应分析） |
| 配置 | …… |
| 不影响 | …… |

---

## 第 2 段：Specs（WHAT 详细要求，按 Capability 分小节）

> 用 SHALL / MUST / SHOULD 表达正式要求；每个 Requirement **至少**一个 Scenario，用 WHEN/THEN 描述。
> 用 ADDED / MODIFIED / REMOVED 标注 delta 类型。

### 2.x Capability: `<capability-name>`（ADDED / MODIFIED / REMOVED）

**ADDED** Requirements:

#### Requirement: <一句话需求陈述，含 SHALL/MUST>

##### Scenario: <场景名>
- **WHEN** <条件>
- **THEN** <预期结果>

##### Scenario: <边界场景名>
- **WHEN** <边界条件>
- **THEN** <边界处理结果>

> ⚠️ **Scenario 必须用 4 个 hashtag** `####`，不得用 3 个或 bullet —— 否则 OpenSpec 风格校验会静默失败。
> ⚠️ **MODIFIED Requirement 必须复制原文整段**再修改，避免归档时丢失上下文。

---

## 第 3 段：Design（HOW + 关键决策）

> 关键澄清点（陷阱）的答案集中落在 **Decisions** 段，每个决策独立成小节，写明"为什么选 X 不是 Y"。

### 3.1 Context
<!-- 既有架构简述 + 改造点上下文 -->

### 3.2 Goals / Non-Goals

**Goals**：
- ……

**Non-Goals**（明确不做）：
- ……

### 3.3 Decisions（关键决策）

> 每个决策**必须**写清楚选项、最终选择、为什么不选其他选项。
> 这是避免 Cargo Cult（盲目跟风）的核心机制。

#### D1: <决策点名称>
- **选项**：A) … / B) … / C) …
- **决策**：<选 X>
- **为什么选 X**：……
- **为什么不选 Y**：……
- **为什么不选 Z**：……

#### D2: <决策点名称>
（同上格式）

### 3.4 Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| …… | …… |

### 3.5 Migration Plan
<!-- 部署/回滚策略，如不需迁移请明确写"不需要" -->

### 3.6 Open Questions
<!-- 暂时无法回答的问题，留待主讲彩排或 review 阶段补 -->
- [ ] ……

---

## 第 4 段：Tasks（拆分到 3 人协同，按 OpenSpec checkbox 格式）

> 严格 `- [ ] X.Y` 格式，便于 Qoder 跟踪进度。
> 按 3 人角色分组（Spec Owner / Feature Owner / Test Owner），每人独立成一组。

### 1. Spec Owner 任务（统筹 + 仲裁 + 集成）
- [ ] 1.1 维护本 Spec 文档完整性
- [ ] 1.2 ……（涉及 registry / 全局 prompt 等改既有文件的事）
- [ ] 1.x 协调最终 merge + 跑集成验证

### 2. Feature Owner 任务（主流程实现）
- [ ] 2.1 ……（新建 skill / tool / schema 等新文件的事）
- [ ] 2.2 ……
- [ ] 2.x ……

### 3. Test Owner 任务（测试 + 边界）
- [ ] 3.1 ……（每个 Spec Scenario 对应一条测试）
- [ ] 3.2 准备 fixtures / mock 数据
- [ ] 3.x 在 M5 用 spec-tester 跑测试质量审计

---

## 附录：模板使用规则（强制）

### A1. 完整性铁律
1. **必须 4 段都填**——任何一段为空视为不合规
2. **Requirement 必须有 Scenario**——空 Requirement 视为不合规
3. **Tasks 必须用 `- [ ] X.Y` 格式**——保证 Qoder 进度跟踪可解析
4. **Decisions 必须写"为什么不选其他选项"**——避免 Cargo Cult

### A2. Delta 标注铁律
- ADDED：全新内容，正常写
- **MODIFIED**：必须复制原 Requirement 全文，避免归档时信息丢失
- REMOVED：必须含 **Reason** + **Migration** 两行
- RENAMED：用 FROM:/TO: 格式

### A3. 影响面铁律（存量项目特有）
- 任何对**既有文件**的修改（如 `prompt_builder.py` / `registry.py`），Decisions 段**必须**有对应小节分析"为什么这么改 + 影响其他模块吗"
- 任何对**全局行为**的改造（如系统 prompt），Risks 段**必须**列出回归测试范围

### A4. 协同铁律
- Spec Owner 负责改既有文件 + merge 仲裁
- Feature Owner 负责新建文件 + 主流程
- Test Owner 负责测试 + 边界 + fixtures
- 三人**不允许**改同一个既有文件，避免 merge 冲突

---

## 模板引用来源

本规范结构借鉴：
- **OpenSpec spec-driven schema** (Fission-AI/OpenSpec v1.4.1)：proposal/spec/design/tasks 4 段式 + ADDED/MODIFIED 语法 + WHEN/THEN Scenario
- **QwenPaw 项目编码规范**（`.qoder/rules/backend_specification.md`）：Python 代码层约束
