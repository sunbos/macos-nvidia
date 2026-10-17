# 维护与发布规则

本 fork 是 NullMoth 社区驱动的适配与复现记录，不是 NVIDIA 官方驱动。保留上游 Git 历史和许可证；原始说明保存在 `README.upstream.md`。

## 仓库分工

- `sunbos/macos-nvidia`：驱动源码、本地补丁、按系统/GPU/显示模式划分的 profile、来源与实测记录。
- 原 Yoga 仓库：保持已有 Intel 核显方案不变。本 fork 不修改它的分支、Release、EFI 或构建工作流。
- 私有离线备份：完整机器 EFI、Windows 引导、当前二进制和恢复所需文件。不要上传原始系统日志、网络信息、SMBIOS、KDK 或 Apple 系统文件。

## 同步不是安装

1. 用 `upstream` remote 读取上游。当前 `main` 保留 fork 创建时的上游历史；适配工作在单独分支进行。
2. 记录上游完整 commit、Release tag、资产 SHA-256 和核验日期。候选更新在独立分支比较，不重置已有 profile 的组件锁。
3. 对照组件逐项判断本地补丁是否已合并、仍需移植或已不适用。旧基线补丁只用于对应提交，不能直接套到最新版。
4. 编译/安装/新启动/实际应用的验收分别记录。CI 成功和设备名称出现都不能替代实际 NVIDIA 工作负载。
5. 通过验收后才更新 profile 并发布该 profile 的新版本；保留前一个可恢复组合。版本标签示例：`macos-26.7.1-25G241-gtx1650ti-maxq-r1`。示例不是已经发布的 Release。

无需为每个显卡型号创建一个仓库。新 profile 必须写清 PCI ID、架构、VRAM/BAR、显示路由及测试 OS build；同属 GTX 16 系不能自动继承 TU117 笔记本的验证结果。

## 当前上游核验

2026-10-17 核验：最新 Release [v2.3.1](https://github.com/nullmoth/nvidia-macos-driver/releases/tag/v2.3.1)，main/tag 均为 `418051b47f219e1751c30e361f509e71a1101132`。

- [安装器](https://github.com/nullmoth/nvidia-macos-driver/blob/418051b47f219e1751c30e361f509e71a1101132/package/install.sh#L118-L135)接受 macOS 15 和 26；支持表覆盖 GTX 16/Turing，但[实机验证表](https://github.com/nullmoth/nvidia-macos-driver/blob/418051b47f219e1751c30e361f509e71a1101132/docs/CARD-SUPPORT.md)不等于本 profile 已获上游验证。
- v2.3.1 的新增内容主要是启动回退；不是本机 translator/codec 修复的替代证明。
- 安装器会整包替换用户态组件。[lastgood 回退](https://github.com/nullmoth/nvidia-macos-driver/blob/418051b47f219e1751c30e361f509e71a1101132/package/install.sh#L310-L356)会恢复包含 AuxKC 在内的文件并自动重启。
- 其启动成功判断与 framebuffer 路径有关，本地 `nvheadless=1` 分支绕过该显示路径。直接整合可能产生冲突，目前只是源码评估，未在本机进行该冲突复现。

## 对外贡献与许可

保留 [LICENSE](../LICENSE)、[NOTICE](../NOTICE) 与各子组件声明。主仓库和 translator 等组件许可证不同；不得把整个归档重新标成单一宽松许可证。未核实分发许可和可恢复性前不发布预编译驱动包。

遵守上游 [CONTRIBUTING.md](../CONTRIBUTING.md) 与 [AGENTS.md](../AGENTS.md)。本次只创建用户自己的 fork 和归档，没有向上游创建 Issue、PR 或评论。
