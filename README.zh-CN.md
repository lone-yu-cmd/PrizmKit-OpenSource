# PrizmKit

[English](README.md)

PrizmKit 是一套平台无关的 Agent Skills 工具集，用于通过结构化流程完成一个正式软件需求：

```text
plan → implement → code-review → test → retrospective → committer
```

这套工具为每个阶段定义清晰职责，保存阶段交接状态，按照变更范围路由修复，并在创建本地 Git commit 前要求用户确认。

## PrizmKit 解决什么问题？

AI 编程会话经常把需求规划、实现、评审、测试、文档维护和提交混在一起。PrizmKit 将这些职责拆开，同时保持流程连续：

- 需求从明确目标和验收标准开始；
- 实现遵循经过评审的任务计划；
- Main Agent 在最终测试前评审并修复完整变更；
- 项目原生测试验证最终评审后的工作区；
- 在提交前同步持久化项目知识；
- 只有用户确认具体范围和提交信息后，才创建本地 Git commit。

## Skill 能力地图

```text
PrizmKit
├── prizmkit
│   └── 框架介绍与导航
├── prizmkit-workflow
│   └── 正式需求流程的一键编排入口
├── prizmkit-init
│   └── 推荐的一次性项目初始化
├── 正式需求开发流程
│   ├── prizmkit-plan
│   ├── prizmkit-implement
│   ├── prizmkit-code-review
│   ├── prizmkit-test
│   ├── prizmkit-retrospective
│   └── prizmkit-committer
├── prizmkit-prizm-docs
│   └── 独立的 Prizm 文档管理
└── prizmkit-deploy
    └── 独立的部署与运维入口
```

## 安装

使用兼容 skills 的安装器安装本仓库：

```bash
npx skills add <owner>/<repository>
```

按照安装器提示选择需要的 skills。若要使用完整需求闭环，请安装六个正式流程 skills。

本仓库发布的是平台无关的 `SKILL.md` 源文件。具体安装位置、可用工具以及是否支持 skill 之间自动调用，由宿主平台决定。

## 快速开始

### 1. 第一次进入项目

第一次进入项目时，建议运行：

```text
/prizmkit-init
```

初始化会扫描项目并生成有用的 PrizmKit 上下文。

初始化是推荐步骤，不是硬依赖。如果没有执行初始化，`prizmkit-plan` 会说明初始化的价值，并使用 README、项目清单、项目规则、源码结构和相关源文件作为 fallback 上下文继续工作。

### 2. 开始一个正式需求

如果希望一键串联完整流程，可以调用：

```text
/prizmkit-workflow <需求描述>
```

它会协调同样的六个阶段并保留需求上下文。如果希望手动控制流程，也可以直接调用 `/prizmkit-plan`。

正式流程固定为：

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

正式需求必须执行六个阶段。每个阶段可以根据变更类型选择合适的执行深度，但不能静默跳过。

### 3. 确认提交

在修改本地 Git 历史之前，`prizmkit-committer` 会展示：

- 计划提交的文件；
- 新增、修改、删除和重命名文件摘要；
- 敏感文件警告；
- diff 摘要；
- 建议的 Conventional Commit 信息。

只有用户确认后才会创建 commit。Push 是独立且需要明确授权的动作。

### 4. 独立部署

部署不是正式需求流程的第七个门禁。需要时单独调用：

```text
/prizmkit-deploy
```

## 正式需求开发流程

### Plan

`prizmkit-plan` 创建并评审：

```text
.prizmkit/specs/<需求>/
├── spec.md
└── plan.md
```

它是需求流程入口，并为后续所有阶段保留同一个 `artifact_dir`。

### Implement

`prizmkit-implement` 执行经过评审的任务，记录 checkpoint，并进行实现阶段的本地验证。初次实现完成后固定进入 code review。

### Code Review

`prizmkit-code-review` 是一个由 Main Agent 执行的有边界 review loop。Main Agent 会：

1. 评审完整变更；
2. 判断具体 findings；
3. 直接修复接受的 findings；
4. 对修复执行定向验证；
5. 持续循环直到 `PASS` 或 `NEEDS_FIXES`。

完整测试在 review 之后执行，以保证最终测试证据对应最终评审后的工作区。

### Test

`prizmkit-test` 使用项目原生工具和可审计证据验证最终评审后的变更。有效终态包括：

- `TEST_PASS`：适用于当前范围的验证成功；
- `TEST_FAIL`：可靠证据证明实现或已确定的合约存在问题；
- `TEST_BLOCKED`：环境、范围、证据或可靠性问题导致无法得出可信结论。

纯文档或纯格式需求仍然会执行确定性的轻量验证，成功后返回 `TEST_PASS`。

### Retrospective

`prizmkit-retrospective` 检查最终通过 review 和 test 的变更，并且：

- 更新持久化的 Prizm 文档；或
- 记录 `NO_DOC_CHANGE` 及原因。

两者都代表 retrospective 阶段成功完成。第一次文档初始化和文档漂移修复应使用独立的 `prizmkit-prizm-docs`。

### Committer

`prizmkit-committer` 验证同一需求的所有前置门禁，预览待提交内容，等待用户确认，安全暂存，创建 Conventional Commit 并验证结果。它不会自动 push。

## 修复路由

修复只重新经过受本轮变更影响的门禁：

```text
REVIEW_NEEDS_FIXES
  → implement
  → code-review

TEST_FAIL，且只影响测试、fixture 或测试运行配置
  → implement
  → test

TEST_FAIL，且影响生产代码、运行时配置、Schema、依赖或公开接口
  → implement
  → code-review
  → test

TEST_BLOCKED
  → 暂停，不进行推测性的生产代码修改
  → 环境恢复后从 test 继续
```

外层流程最多自动修复三轮。code review 内部也有独立的 review-round 上限。当达到上限或外部阻塞导致无法完成时，流程会保留证据并提供确定性的恢复入口，不会谎报成功。

## 自动交接与手动恢复

PrizmKit 定义的是语义交接，而不是绑定某个平台的编排 API：

```text
阶段完成
  → 持久化真实状态
  → 请求下一个语义 skill
```

- 如果宿主支持 skill 之间的调用，流程可以从 `prizmkit-plan` 自动继续；
- 如果宿主不支持，当前阶段会输出唯一的下一个 skill，并保存恢复上下文。

不支持自动交接的宿主仍然可以通过调用提示的下一个 skill 完整执行相同流程。

## Workflow State

一个正在执行的需求可能生成：

```text
.prizmkit/state/workflows/<需求-slug>.json
```

该文件记录当前阶段、终态、修复轮次、修复范围、下一阶段和恢复入口。它只是流程索引：

| 信息 | 权威来源 |
|---|---|
| 目标和验收标准 | `spec.md` |
| 任务和完成情况 | `plan.md` |
| Review findings 和结论 | `review-report.md` |
| 测试结果和执行证据 | Test evidence package |
| 持久化架构知识 | `.prizmkit/prizm-docs/` |
| 当前阶段和恢复入口 | Workflow state |

详细协议见 [WORKFLOW-STATE.md](WORKFLOW-STATE.md)。

PrizmKit 不规定目标项目是否提交、忽略或共享生成的 `.prizmkit/` 状态文件。

## 独立 Skills

### `prizmkit-workflow`

提供正式需求的一键入口。它协调六个现有 lifecycle skills，始终复用同一个 `artifact_dir`，执行 review/test 修复路由，在环境阻塞时暂停，并最终进入 commit 确认。它仍然是 L1 交互式编排 skill，不是 L2 批量 pipeline runtime。

### `prizmkit`

介绍框架并将用户引导到正确的 skill。它不执行或协调正式需求流程。

### `prizmkit-init`

提供推荐的一次性项目初始化。它是软前置，可以跳过。

### `prizmkit-prizm-docs`

初始化、验证、迁移、修复或重建 Prizm 文档。它不是每个正式需求都要额外经过的阶段。

### `prizmkit-deploy`

提供独立的部署与运维入口。不同目标的支持程度可能不同，并且始终受宿主权限、凭据和基础设施可用性限制。

## 平台兼容性

兼容性分为三个不同层次：

| 层次 | 含义 |
|---|---|
| 可安装 | 宿主可以安装并暴露标准 Agent Skills。 |
| 可恢复 | 宿主可以保存生成的项目 artifacts，用户可以调用确定性的下一个 skill。 |
| 自动交接 | 宿主可以在当前生命周期中语义化调用下一个已安装 skill。 |

协议本身平台无关。平台名称和命令形式只是示例，不是协议标识或允许列表。

## 范围与非目标

第一版开源版本**不包含也不要求**：

- `app-planner` 或其他 L2 planner；
- feature、bug 或 refactor 批量任务列表；
- pipeline launcher 或自治 pipeline runtime；
- 多需求排队、调度或并行编排；
- 每个平台都具备通用自动交接；
- 每个部署目标都具备同等自动化能力；
- 自动远程 push、包发布或版本管理；
- 超出宿主沙箱、工具、凭据和环境范围的权限。

未来可以将 `app-planner` 作为复杂绿地项目产品和架构规划的可选扩展，但它不是 L1 生命周期的隐藏依赖。

## 仓库结构

```text
PrizmKit-OpenSource/
├── README.md
├── README.zh-CN.md
├── WORKFLOW-STATE.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── scripts/
└── <skill-name>/
    ├── SKILL.md
    ├── assets/
    ├── references/
    ├── scripts/
    └── tests/
```

每个 skill 目录只包含自身所需的 assets、references、scripts 和 tests。

## 安全

Skills 会在宿主的权限和安全模型下执行，不会绕过审批要求、沙箱、密钥策略或基础设施授权。

安全问题请按照 [SECURITY.md](SECURITY.md) 中的私下报告流程提交。不要在公开 issue 中发布密钥或可利用的漏洞细节。

## 贡献

贡献规范、生命周期不变量、校验和测试要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。社区协作遵循 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可证

PrizmKit 使用 [MIT License](LICENSE)。
