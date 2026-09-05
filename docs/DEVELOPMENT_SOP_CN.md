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

4. 在 GitHub 网页开 PR 到 `main`。
5. 在 PR 页面检查 diff 和 GitHub CI。
6. 选择 `Squash and merge` 作为默认合并方式。

如果 CI 还没有跑完，可以在 PR 页面启用 `Enable auto-merge`。启用后，GitHub 会在 required reviews 和 status checks 都通过后自动 merge。`Allow auto-merge` 只代表允许 PR 自动合并；它不会自动创建 PR。

7. Repo 设置开启：

```text
Settings -> General -> Pull Requests -> Automatically delete head branches
```

已开启后，PR merge 后 GitHub 会自动删除远端 feature branch。

8. 用户在 GitHub 完成 PR merge 后，通知 Codex：

```text
merge 了，帮我清理本地 branch 并回 main
```

9. Codex 回本地同步 `main`：

```powershell
git switch main
git pull origin main
```

10. Codex 删除本地功能分支：

```powershell
git branch -D <branch>
```

使用 `Squash and merge` 时，本地原 feature branch commit 不会以同一个 commit hash 出现在 `main`，所以 `git branch -d` 可能会拒绝删除。确认 PR 已经 merge 后，用 `git branch -D` 删除本地 branch。

11. 更新阶段进度 tracker：

```text
docs/Lifelikegame_Phase_Progress_Tracker_CN.xlsx
```

至少更新：

1. 对应 tracker ID 的进度 / 状态。
2. 完成日期。
3. 必要时补充备注，例如 commit、PR、测试结果或遗留事项。

## 下一项计划

每次开始下一项前，以 tracker 为准，不在 SOP 里长期写死某一个 ID。

选择下一项时：

1. 读取 `docs/Lifelikegame_Phase_Progress_Tracker_CN.xlsx`。
2. 优先选择当前 Phase 中 `Required = yes`、依赖已完成、进度未完成的最高优先级任务。
3. 对照 `docs/Lifelikegame Technical Development Plan.md`，确认该任务是否应该现在做。
4. 向用户说明建议做的 tracker ID、原因、范围和不做范围。
5. 用户确认后，才进入 branch 流程。

## Superpowers 使用规则

每个任务开始前先判断是否需要使用 superpowers skill。

常见规则：

1. 新功能或行为变更：先用 `superpowers:brainstorming`。
2. bug、测试失败、环境异常：先用 `superpowers:systematic-debugging`。
3. 写代码修 bug 或做功能：使用 `superpowers:test-driven-development`。
4. 声称完成前：使用 `superpowers:verification-before-completion`。
5. 功能完成后决定 merge、push 或 PR：使用 `superpowers:finishing-a-development-branch`。

用户指示优先于默认流程；如果用户要求先检查，就必须停在检查点，不能直接提交或推送。
