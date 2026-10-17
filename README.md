# macOS NVIDIA 适配与复现

按 **系统版本＋GPU＋显示模式** 管理 NullMoth NVIDIA 驱动的本地适配、源码补丁与实测记录。此项目是社区驱动 fork，不是 NVIDIA 官方驱动。

| Profile | 验证状态 |
|---|---|
| [macOS 26.7.1 (25G241) / GTX 1650 Ti Max-Q / headless](profiles/macos-26.7.1-25G241/gtx-1650-ti-maxq-headless/README.md) | 本机新启动后的基础 Metal 复制、计算、离屏渲染通过；完整应用与重装复现尚未完成 |

**当前是可追溯适配归档，不是一键安装发行包。** 根目录源码保留上游 v2.3.1；profile 的现装组合来自多个固定旧基线，必须按组件清单理解，不能直接运行根目录安装脚本来复现它。

- [组件来源与源码归档](profiles/macos-26.7.1-25G241/gtx-1650-ti-maxq-headless/SOURCE-ARCHIVE.md)
- [重装与恢复准备](profiles/macos-26.7.1-25G241/gtx-1650-ti-maxq-headless/REINSTALL.md)
- [上游同步与发布规则](docs/MAINTENANCE.md)
- [上游原始 README](README.upstream.md) · [原项目](https://github.com/nullmoth/nvidia-macos-driver) · [许可证](LICENSE) · [第三方声明](NOTICE)

原 Yoga 核显仓库保持不变，继续作为独立的核显恢复基线。显卡名称相同或同属 GTX 16 系，不意味着本 profile 的结果自动适用于其它电脑。

公开内容只包含整理后的源码、补丁、版本锁与脱敏证据；整机 EFI、个人标识、原始日志与恢复二进制另行私有保存。
