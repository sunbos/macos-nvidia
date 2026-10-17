# macOS 26.7.1 / GTX 1650 Ti Max-Q / headless

这是一份本机适配归档，尚不是重装后可直接执行的一键安装包。fork 根目录保留的是上游 v2.3.1 代码；当前已安装组合使用多个旧源码基线和本地修改，不能把两者混同。

| 项目 | 记录 |
|---|---|
| 系统 | macOS 26.7.1，build 25G241，x86_64 |
| 机器 | Lenovo Yoga 9 15IMH5，Intel i9-10980HK |
| NVIDIA | GTX 1650 Ti with Max-Q Design，TU117，PCI `10de:1f95` |
| 内存 | VRAM 4 GB，BAR 256 MB |
| 显示路由 | Intel 驱动内屏；NVIDIA headless 计算/离屏渲染 |
| 同机共存 | OCLP-Mod 3.1.9，匹配 `KDK_26.7.1_25G241.kdk` |

## 验证范围

2026-10-17 用户完成 OCLP-Mod 无线/音频根补丁并重启后，重新核验了 NVIDIA：

- 四个 NVIDIA kext 已加载，RM ready、headless 属性成立。
- 正常 Metal 枚举明确选中 NVIDIA，物理 provider 是 PCI `10de:1f95`，与 Intel registry 分开。
- GPU private buffer 复制 16,384 bytes、1024 个整数计算、64×64 离屏渲染均与 CPU 预期值相符；测试自然退出 0。
- 本次测试仍记录一条非致命 MESA `VK_ERROR_UNKNOWN` 警告。小规模通过不代表驱动整体无错误。

历史 Geekbench 6 [结果 6937834](https://browser.geekbench.com/v6/compute/6937834)报告 NVIDIA Metal 28,278 分，设备名明确含 GTX 1650 Ti Max-Q/NVK TU117-A；当时监督程序在上传后错误终止了进程，因此不把它计为完整正常退出验收。更早选中 Intel 的结果不用于证明 NVIDIA 性能。

尚未完成：普通 VideoProc 首次编码集成、HEVC 故障、H.264 码率控制、完整跑分正常退出和长时间稳定性。H.264 指定注册路径的有限编码/解码通过，不等于 VideoProc 整体可用。

音频输出和 Wi-Fi 由用户的 OCLP-Mod 操作恢复；麦克风/输入设备未枚举，不能称音频全部正常。这些状态不作为 NVIDIA 驱动的能力宣称。

## 内容与重装入口

- `components.json`：本组合组件的精确 hash、来源与复现边界。
- [runtime-acceptance.json](runtime-acceptance.json)：脱敏的 NVIDIA 身份、测试规模、退出状态和原始证据摘要。
- `SOURCE-ARCHIVE.md`：归档源码/补丁及离线核验范围。
- [重装与恢复准备](REINSTALL.md)：材料、顺序、恢复边界和验收。
- [上游维护规则](../../../docs/MAINTENANCE.md)：如何评估同步，为什么不能直接覆盖现装组合。

不在本仓库发布机器完整 EFI、SMBIOS、原始日志或系统二进制。原 Yoga 核显仓库保持原样；其历史 EFI 不能单独恢复本 profile 的 APFS 驱动文件。
