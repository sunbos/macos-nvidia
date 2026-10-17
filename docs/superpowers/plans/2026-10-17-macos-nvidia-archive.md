# macos-nvidia archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. The user approved the public fork and preservation of the Yoga repository.

**Goal:** 发布可追溯的 macOS 26.7.1 / GTX 1650 Ti Max-Q headless 适配归档，不改变当前系统。

**Architecture:** fork 保留上游源码历史；profile 独立锁定当前混合组件与本地补丁。旧 Yoga 仓库仍为独立的核显恢复来源。

**Tech Stack:** Git/GitHub、Markdown、JSON、SHA-256、离线 patch 应用校验。

## Task 1: 来源与配置归档

- [x] 创建公开 fork 并在新目录克隆，原源码工作目录不动。
- [x] 新建 `codex/macos26-tu117-archive`，保留 `upstream` remote，读取上游 AGENTS/许可证。
- [ ] 创建 `profiles/macos-26.7.1-25G241/gtx-1650-ti-maxq-headless/`，写入组件清单、精确源码补丁与脱敏验收材料。来源以本机最新 COMPONENTS/REVIEW 为准。
- [ ] 归档可恢复的源码差异，不复制未知来源二进制、完整旧机器事务脚本或商业 benchmark shader。逐项列出尚未迁移的输入。
- [ ] 离线检查补丁应用到其精确基线，核对输出内容；JSON 全部可解析。

## Task 2: 重装与维护说明

- [ ] 修改 fork README 顶部，说明独立适配分支与已验证/未验证范围，保留上游正文及许可证。
- [ ] 编写 profile README，列出 macOS build/KDK/OCLP/EFI/组件材料、重装顺序及验收点；未演练步骤必须标注。
- [ ] 说明原 Yoga 仓库保持不变；仅恢复 EFI 不等于卸载 NVIDIA 系统文件。
- [ ] 记录当前上游 v2.3.1 的整包替换和自动重启回退边界；本次不运行安装器。

## Task 3: 审阅与发布

- [ ] 先审阅范围与证据，再审阅公开内容、来源完整性及可恢复性。
- [ ] 运行 `git diff --check`，检查新增文件的私有路径、标识符和未授权材料。
- [ ] 只暂存明确白名单文件，提交并推送适配分支，设为 fork 默认展示分支；不修改上游和 Yoga 仓库。
- [ ] GET 核对 GitHub 提交/默认分支，回报仓库链接、已归档内容及仍待完成的重装复现工作。

不发布驱动二进制 Release，不创建上游 PR，不运行编译或 GPU/codec 测试。上述检查是资料归档验证，不能转写为完整驱动功能验收。
