# Lifelikegame Development SOP

## 目标

一个功能一个 branch，一个功能一个 PR，`main` 永远保持可运行。

每次开发都先明确要做的 tracker ID、影响范围和验收方式。开 branch 前，先参考技术开发计划，判断本次计划是否符合整体架构方向，并把准备怎么做告诉用户。用户确认后，才进入开 branch 和实作流程。

实作完成后，先让用户检查改动；用户确认没问题后，才进入 `git add`、`commit`、`push` 和 PR 流程。

## 每次开始新功能前的计划检查

1. 读取整体技术计划：

```text
docs/Lifelikegame Technical Development Plan.md
```

2. 读取阶段进度 tracker：

```text
docs/Lifelikegame_Phase_Progress_Tracker_CN.xlsx
```

3. 确认本次任务：

- 当前 tracker ID。
- 所属 Phase。
- 依赖任务是否已经完成。
- 主要范围。
- 完成 / 测试标准。

4. 对照技术计划判断本次做法是否合理：

- 简单 CRUD 是否继续使用 `Router -> Service -> Repository`。
- 复杂业务流程是否应该等待 `Command -> Mediator -> Handler -> Unit of Work` 基础完成。
- 是否误把 Phase 2 以后的架构工作提前塞进当前任务。
- 是否有超出当前 tracker ID 的重构。

5. 向用户说明：

- 本次要做什么。
- 会动到哪些文件。
- 不会做什么。
- 准备怎么测试。
- 是否建议继续、拆小、或先做其他依赖。

6. 用户确认计划后，才进入 branch 流程。

## Branch 开始流程

1. 确认当前工作区状态：

```powershell
git status --short --branch
```

2. 切回 `main` 并拉最新代码：

```powershell
git switch main
git pull origin main
```

3. 跑本地 backend 测试，确认起点是绿的：

```powershell
.\backend\scripts\test.ps1
```

4. 从 `main` 开新分支：

```powershell
git switch -c codex/phase-<n>-<short-task-name>
```

例：

```powershell
git switch -c codex/phase-1-interface-types
```

## 分支命名

使用：

```text
codex/phase-<phase-number>-<short-task-name>
```

例：

```text
codex/phase-1-domain-errors
codex/phase-1-interface-types
codex/phase-2-unit-of-work
```

## 实作流程

1. 读 `docs/Lifelikegame_Phase_Progress_Tracker_CN.xlsx`，确认当前任务 ID、依赖任务、主要范围和完成标准。
2. 读相关代码，确认现有实现和 tracker 是否一致。
3. 说明本次会做什么、会动到什么、不做什么。
4. 用户确认计划后，开始实作。
5. 写 failing test。
6. 跑目标测试，确认失败原因正确。
7. 实作最小代码。
8. 跑目标测试，确认通过。
9. 跑完整 backend 测试：

```powershell
.\backend\scripts\test.ps1
```

10. 输出改动摘要和 diff 检查清单，让用户检查。
11. 用户确认没问题后，才进入 git 步骤。

## 用户检查点

实作完成后，先停在检查点，不直接 commit 或 push。

检查内容包括：

1. 改了哪些文件。
2. 每个文件为什么要改。
3. 测试结果。
4. 是否有超出本次 tracker ID 的改动。
5. 是否有未纳入本次工作的其他本地改动。

常用检查命令：

```powershell
git status --short
git diff
```

如果用户要求看某个文件的具体 diff：

```powershell
git diff -- path\to\file
```

用户确认后再执行：

```powershell
git add <files>
git commit -m "<type>: <summary>"
git push -u origin <branch>
```

## 本地测试

默认测试命令：

```powershell
.\backend\scripts\test.ps1
```

跑单个测试：

```powershell
.\backend\scripts\test.ps1 tests\test_auth.py::test_duplicate_signup_returns_domain_error_payload -v
```

脚本负责：

1. 启动 Docker Compose 的 `db` service。
2. 确认 `lifelikegame_test` 测试库存在。
3. 设置测试用 `DATABASE_URL` 和 `TEST_DATABASE_URL`。
4. 设置测试用 JWT 配置。
5. 执行 pytest。
6. 将 pytest exit code 传回 PowerShell。

前提：Docker Desktop 必须已经打开。

## 完成后流程

用户确认 diff 后：

1. Stage 本次功能相关文件：

```powershell
git add <files>
```

2. Commit：

```powershell
git commit -m "<type>: <summary>"
```

3. Push feature branch：

```powershell
git push -u origin <branch>
```

4. 在 GitHub 开 PR 到 `main`。
5. 等 GitHub CI 通过。
6. Merge PR。
7. 回本地同步 `main`：

```powershell
git switch main
git pull origin main
```

8. 删除已合并的本地功能分支：

```powershell
git branch -d <branch>
```

## 下一项计划

当前下一项是 Phase 1 ID 9：补完整 Interface 参数与返回类型。

目标：

```text
Pyright/Mypy 不再报告 Interface 签名不一致。
```

主要范围：

```text
backend/app/*/interfaces.py
```

预计会检查：

```text
backend/app/auth/interfaces.py
backend/app/users/interfaces.py
backend/app/goals/interfaces.py
backend/app/tasks/interfaces.py
backend/app/task_schedules/interfaces.py
backend/app/task_instances/interfaces.py
backend/app/scoring_schemes/interfaces.py
backend/app/point_ledgers/interfaces.py
backend/app/rewards/interfaces.py
backend/app/redemptions/interfaces.py
backend/app/workflows/*/interfaces.py
backend/app/ai_planner/interfaces.py
```

对应读取：

```text
backend/app/*/service.py
backend/app/*/schemas.py
backend/app/*/models.py
```

## ID 9 不做什么

ID 9 只收紧 interface 类型边界。

本任务不做：

1. UnitOfWork。
2. CQRS。
3. Transaction ownership 改造。
4. Repository 去除 commit。
5. 大规模 DTO migration。
6. 业务流程重写。

这些留到 Phase 2。

## Superpowers 使用规则

每个任务开始前先判断是否需要使用 superpowers skill。

常见规则：

1. 新功能或行为变更：先用 `superpowers:brainstorming`。
2. bug、测试失败、环境异常：先用 `superpowers:systematic-debugging`。
3. 写代码修 bug 或做功能：使用 `superpowers:test-driven-development`。
4. 声称完成前：使用 `superpowers:verification-before-completion`。
5. 功能完成后决定 merge、push 或 PR：使用 `superpowers:finishing-a-development-branch`。

用户指示优先于默认流程；如果用户要求先检查，就必须停在检查点，不能直接提交或推送。
