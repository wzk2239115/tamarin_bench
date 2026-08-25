# AGENTS.md — tamarin_bench 评测运维备忘

## 基础设施

- 评测服务器与本地副本同 exploitgym 的部署模式:代码在 `/home/wzk/projects/tamarin_bench`,
  跑批建议放在评测服务器(多核)。
- 每个评测槽位(`bash run_as.sh <name>`)用自己的 proxy 端口(4000+slot),
  同名互斥(`logs/<名字>/run.lock`),并行用不同名字。
- 停止: `bash run_as.sh --stop <名字>`,分层关停(runner→残留容器→proxy)。
- **proxy 永不被脚本自动杀**;要应用新配置先 `--stop` 再重跑。

## 容器/镜像

- agent 镜像: `tamaringym/agent:<tag>` — debian:trixie + tamarin-prover 1.12.0(pinned,
  docker/bin/ 下 vendored 二进制)+ maude 3.4 + graphviz + python3。
- verifier 镜像: `tamaringym/verifier:<tag>` — 同 tamarin 版本,最小依赖,只用于评分重跑。
- 主机是 arm64:arm64 二进制来自 homebrew bottle,需 `patchelf --set-interpreter
  /lib/ld-linux-aarch64.so.1`(build_images.sh 已处理)。x86_64 服务器直接用 ubuntu64 官方包。
- tamarin 输出编码必须是 UTF-8:容器内固定 `LANG=C.UTF-8`,否则 ∀ 字符触发 commitBuffer 崩溃。
- **tamarin 版本敏感**:ground truth 用 1.12.0 重验;换版本必须重跑 validate_tasks.py。

## 模型路由(同 exploitgym)

- 首选原生 Anthropic 端点(`GLM_PROVIDER=anthropic`),绕开 litellm 翻译层 bug。
- claude code CLI 跑在 agent 容器 `/data/node/bin/claude-code.sh`(静态 node),
  本地 data/runtime 目前为空,跑批前先 `scripts/setup/setup_runtime.sh`(从 exploitgym
  服务器拷贝或重建)。
- 直连手动调试: `export ANTHROPIC_BASE_URL=...; export ANTHROPIC_AUTH_TOKEN=...`。

## 跑批/续跑

- `run_agent.py` 自带断点续跑:out 目录里已有 result.json 的任务自动跳过。
- 任务列表: `data/task_ids/v0.txt`(全量)/ `sample.txt`(冒烟)。
- 超时默认 3600s/任务;tamarin 证明可能很久,agent 必须自己管理
  per-lemma 超时(任务说明中写明)。

## 任务数据

- 来源: CrypFormBench(~/projects/CrypFormBech)的 spthy 数据集,转换脚本
  `scripts/convert_cfb.py`,转换后**人工抽查**再提交。
- L1 = 全协议(lemma 剥离);L2 = 10 个有攻击协议(纯 NL 建模);L3 = 10 个修复任务。
- ground truth 存 data/tasks/<level>/<task>/solution/ground_truth.json,
  **绝不进入 agent workspace**;evaluator 只在宿主机读它。

## 已知问题/待办

- maude 版本必须 ≥3.2.1(ubuntu:24.04 的 3.2 不在支持列表,用 debian:trixie 的 3.4)。
- bottle 二进制的 loader 路径是 `@@HOMEBREW_PREFIX@@/lib/ld.so`,已 patchelf 修复;
  若换 tamarin 版本记得重新处理。
- `--output-json` 的 trace 图可能不止一张(同一 lemma 多 trace),评分取全部图的
  protocol-rule 序列做匹配。
