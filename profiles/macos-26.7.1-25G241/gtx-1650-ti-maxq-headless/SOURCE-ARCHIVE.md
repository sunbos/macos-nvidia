# 固定源码与复现边界

这份归档保存 2026-10-17 盘点到的历史混合组件来源。它不代表 upstream v2.3.1，也不是经过干净环境验证的构建、安装或恢复包。完整的 4 个 kernel、7 个用户态文件摘要见 [components.json](components.json)。这些是二进制文件身份，不能证明相应功能可用。

## 包含的源码差异

所有补丁都相对于明确的旧基线，未覆盖 fork 根目录的当前上游源码。`source_sha256` 是冻结源码的文件摘要；`base_sha256` 是补丁前的精确文件摘要，`null` 表示当时不存在该文件。仅选定源文件进入清单。

| 组件 | 原始基线 | 归档内容与构建入口 |
| --- | --- | --- |
| NVRM / NVAccel headless | NullMoth `c7dc26239bf85a648d5318fde135ebc09dc094a3` | [6 文件补丁](sources/patches/nvrm-nvaccel-headless.patch)：4 个生产源文件及 `build/build_nvrm_local.py`、`build/accel_build.sh`。4 个生产文件同时吻合原始 NVRM 构建 manifest。两项构建入口随补丁保留，但仍需完整基线源码和外部依赖。 |
| NVMTLDriver observer | NullMoth `592b8df746371b523d5db0315f9794a57bff5c8e` | [9 文件差异](sources/patches/nvmtl-observer.patch)重建冻结快照内选定的 26 个 plugin 源文件。另 34 个 Vulkan-Headers 文件只保留固定 commit 和逐文件 hash。原有 `build_static.py` 含私有路径和历史 staging 策略，不随归档发布；编译参数、工具与 SDK 摘要已摘录。 |
| AIR translator | NullMoth `592b8df746371b523d5db0315f9794a57bff5c8e` 中的 `translator/` | [40 文件差异](sources/patches/air-translator-nested-switch.patch)重建 `nested-switch-exit-source` 中选定的 276 个文件，保留生产 Rust 文件、两份 Cargo.toml/Cargo.lock。补丁路径相对于 NullMoth 仓库根。外部 tests、examples、`.ll` fixtures 和文档未打包；生产文件内的合成 unit-test 代码保持原字节，完整历史测试集不在归档范围内。 |
| NVK | Mesa `17ca6174dcc6cb22059ac343bc29f8af7800f42e` | [原样保留的补丁](sources/patches/nvk-macos-candidate.patch) SHA-256 为 `e907eba3f0b070c61fad3107dfba4bf778417ed15729d371dde4015c023c3db9`。精确 source-only archive SHA-256 为 `827ab5337856ef7f24ac0bf278bd1f427a3328514bbffadacecd1315885f75b0`；81 个输出文件均已校验。archive 未在本仓库复制。 |

每组的 [source manifest](sources/manifests/) 固定基线 commit、补丁 SHA 和输入/输出文件 SHA。未修改的上游文件依赖相应精确基线，未重复复制。这个选择避免把上游完整源码、依赖树及诊断目录混在一起。

## 离线校验

本轮已从本地 Git object 或已固定 hash 的原始 Mesa archive 重新取得基线，在临时目录执行 `git apply --check`、`git apply` 并比较输出摘要。结果见 [VALIDATION.json](sources/VALIDATION.json)：四组共 389 个选定源文件通过。此步骤不编译、不加载驱动、不运行 GPU，也不修改提供的原始基线。

准备各自**尚未打补丁**的源码目录。前三组可从已经含有上述 commit 的本地 NullMoth Git clone 用 `git archive <commit>` 导出；Mesa 使用 manifest 中固定的原始 archive，解包时去掉一个顶层目录。无需为了校验抓取大型外部依赖。

例如，在本 profile 目录执行：

```sh
python3 sources/verify_archive.py --component nvrm-nvaccel-headless --base "$ARCHIVE_HEADLESS_BASE"
python3 sources/verify_archive.py --component nvmtl-observer --base "$ARCHIVE_USERSPACE_BASE"
python3 sources/verify_archive.py --component air-translator-nested-switch --base "$ARCHIVE_USERSPACE_BASE"
python3 sources/verify_archive.py --component nvk-mesa --base "$ARCHIVE_MESA_BASE"
```

需要 Python 3.9+ 与 Git。环境变量分别指向对应 commit 的导出目录。校验器先检查所有选定输入的摘要，再复制到独立临时目录应用补丁；错误基线会拒绝。它只检查 manifest 白名单内的文件，不声称验证整个上游树。源树名称和本机目录不会写入成功结果。

## 外部输入与尚未完成的构建链

[build-inputs.json](sources/build-inputs.json) 摘录了历史工具版本、编译参数、source/receipt hash 及依赖 pin，没有复制原始日志。

- **NVRM / NVAccel**：还需 NVIDIA OGKM `e4a5faa2567f28c8eabe0ebb6422b6d0abcf37eb`、KDK `26.7.1_25G241`、SDK `26.5`、兼容 IOKit headers，以及原 RM 编译命令和依赖环境。不能仅凭这 6 个补丁文件构建。未发布 KDK、Apple 二进制或 firmware。
- **Observer**：历史构建以已存在的完整 bundle 为基础，仅替换 main executable；主源码和编译参数不等于 bundle 的 codecs、runtime、resources 与签名材料已经齐备。此版本用于注册观测，不是 CPU-first compression 的功能修复。
- **Translator**：历史命令为 `cargo build --release --offline --locked`，Rust `1.90.0`；外部 Cargo cache、工具链、链接和签名环境没有形成统一可移植锁定入口。保留两份 Cargo.lock 不等于所有缓存已提供，也不保证在另一系统生成相同签名 bytes。
- **NVK**：原 `build-nvk.sh`、`configure-nvk.sh`、`env.sh` 因含私有绝对路径未直接发布，其原始 SHA 和关键参数已记录。Mesa CLC、LLVM/SPIRV、Rust、Meson/Ninja、OGKM 和 subproject archives 仍是外部输入。没有在本轮建立从源码到现装 signed NVK 的逐字节重建结果。
- **NVRMFB / NVRMAGDC**：本轮只重新读取二进制和 Info.plist 的 SHA；没有确认这两个现装二进制的精确源码、构建和签名链，不能从上游存在同名源文件推定它们已可重建。

上述各项都没有完成新的 clean-machine build、安装、重启验收或恢复演练。源补丁 apply 成功只证明源文件复原。

## Codec 的特殊边界

[H.264 binary recipes](sources/h264-binary-recipes.json) 保存两段 encode 补丁及一个 decode code-byte 补丁的精确 offset、旧/新 bytes、完整 baseline/pre-sign/signed SHA 和历史签名命令。原始输入库、候选库及任何 codec 二进制均未上传。

此次只读检查独立验证了内存 byte transform 所得 pre-sign SHA；signed SHA 是已有产物的核验结果。没有重新执行签名，也没有验证跨 macOS / codesign 版本能生成相同签名 bytes。配方使用完整 baseline SHA 和 old bytes 作为输入约束。

这不是四个 codec 的完整源码构建链。固定上游来源只定位到 decoder 二进制派生脚本和 plugin 加载入口；encode assembly 只对应局部补丁。HEVC 两项仅保留现装 hash，完整 source-to-binary chain 仍是 gap。也没有建立这些预编译库各自的独立许可与再分发来源，因此本 profile 仅提供可审计配方和摘要。

## 来源、许可与公开范围

复制的许可与 Notice 位于 [sources/licenses/](sources/licenses/)，保留原文：

- NullMoth kernel/plugin 的精确基线根 LICENSE 为 **PolyForm Noncommercial 1.0.0**，保留其 Required Notice 和第三方 NOTICE。两个旧基线的文件分别存档；H.264 配方所引用的 `cd8e2bb04da48d2fa70cf1895879608f3588dbfb` 根 LICENSE/NOTICE 的 SHA 与这些副本相同。[上游来源](https://github.com/nullmoth/nvidia-macos-driver)
- Translator 原有 **LGPL v3.0 or later** 关系来自上游 NOTICE；保留冻结来源的 `LICENSE` 和 `COPYING`。[原项目 metal2vulkan](https://github.com/steelbrain/metal2vulkan)
- Mesa 补丁按历史字节原样保存，并从上述精确 source archive 复制 `licenses/MIT`；各文件仍受其原许可约束。历史补丁对 `src/nouveau/vulkan/nvk_acceleration_structure.c` 替换了版权头，原始说明在此保留：`Copyright © 2022 Collabora Ltd. and Red Hat Inc.`；`SPDX-License-Identifier: MIT`。补丁的新说明为 Valve 2023 / MIT。这里记录此差异，未改写固定补丁或为它重新授权。[Mesa 来源](https://gitlab.freedesktop.org/mesa/mesa)
- Vulkan-Headers commit `ee2ec5fd83dafce291024683b50dc89219333076` 的 LICENSE.md 保留为依赖来源记录。34 个外部 header 内容没有打包。[Vulkan-Headers 来源](https://github.com/KhronosGroup/Vulkan-Headers)
- OGKM 只记录固定来源 commit，其自身许可仍适用。[OGKM 来源](https://github.com/NVIDIA/open-gpu-kernel-modules)

这些文件没有将第三方内容重新标为统一 MIT。归档不包含用户绝对目录、机器序列号、MAC/IP、EFI、原始日志、Apple/KDK 二进制，或从商业 benchmark 提取的 shader 和测试数据。二进制 hash、源码 commit 和库本身的签名 identifier 是 artifact 身份，不能作为机器身份或功能验收证明。
