# 实验 Skills 与交接提示词

用途：给下一篇研究的实验负责人使用。范围是实验设计、实现、运行、消融和结果交付。按本机当前可用的 Skills 筛选，不包含论文写作流程。

## 下载来源

- [本机更新版的公开实验分支](https://github.com/hansu650/Auto-claude-code-research-in-sleep/tree/codex/experiment-skills-share-20260915)
- [Codex 版本与安装说明](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/README.md)

本分支基于本人公开仓库的 2026-09-06 更新（8ae1353），补齐截至 2026-09-15 的实验相关本机修改。下列 7 个 Skill 的正文与本机当前安装文件一致，并同步了 6 份实验相关共享规则。机器专用的盘符和环境偏好由使用者自行配置，共享环境说明保留跨平台版本。源文件校验记录见 [实验快照清单](EXPERIMENT_SKILLS_MANIFEST.json)。

如果使用 Codex，使用仓库的 `skills/skills-codex/` 版本。保留完整仓库，按说明安装；Skills 会引用 `shared-references/`，部分核查还依赖仓库的 `tools/`。安装时用 --skills 选择下面七个实验入口；安装器会补充其声明的必要依赖。其他工具先读取仓库相应的适配说明。


上游项目为 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)，本次交接使用 hansu650 仓库的指定分支。

下载到本地普通文件夹：在打算保存仓库的父目录执行以下命令。

```bash
git clone --branch codex/experiment-skills-share-20260915 --single-branch https://github.com/hansu650/Auto-claude-code-research-in-sleep.git aris-experiment-skills
```

Codex 安装示例（Bash / Git Bash；将项目路径替换成实际路径，仓库文件夹需要保留）：

```bash
bash aris-experiment-skills/tools/install_aris_codex.sh /path/to/your-project --skills experiment-plan,run-experiment,analyze-results,result-to-claim,ablation-planner,experiment-audit,monitor-experiment
```

先根据实际系统、现有安装及权限核对安装方式；此处提供安装入口，本次交接没有在接收方机器上执行安装或运行实验。

## 使用清单

| Skill | 实验中的作用 | 使用时机 |
|---|---|---|
| [experiment-plan](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/experiment-plan/SKILL.md) | 定义数据划分、指标、实验矩阵、运行顺序和预算 | 实验开始前 |
| [run-experiment](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/run-experiment/SKILL.md) | 检查环境，运行我们的方法及必要对照，保留日志 | 运行阶段 |
| [analyze-results](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/analyze-results/SKILL.md) | 从原始输出汇总指标和表格，分析失败与差异 | 每批结果完成后 |
| [result-to-claim](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/result-to-claim/SKILL.md) | 判断已有结果支持哪些结论、还缺哪些证据 | 主实验完成后及最终交付前 |
| [ablation-planner](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/ablation-planner/SKILL.md) | 设计能隔离模块贡献的消融和替代方案对照 | 主结果初步支持方案、需要补充消融时 |
| [experiment-audit](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/experiment-audit/SKILL.md) | 核查标签、评估代码、数据泄漏及数字与文件的对应关系 | 结果交付前 |
| [monitor-experiment](https://github.com/hansu650/Auto-claude-code-research-in-sleep/blob/codex/experiment-skills-share-20260915/skills/skills-codex/monitor-experiment/SKILL.md) | 查看进度、错误和输出 | 长任务按需使用 |

主线：实验计划 → 小规模试跑 → 主实验 → 结果分析与结论核对 → 必要的补充消融 → 最终核查与交付。

计划阶段就列出必要消融，按已有结果决定补充运行的顺序。只做验证核心问题所需的实验，不把默认轮数或实验数量当作必须完成的配额。独立审查是否运行、由什么能力完成，按实际记录；能力缺失时不写“审核通过”。

## 可直接复制给实验负责人的 AI

```text
你负责这项研究的实验工作，交付可复现代码、数据说明、原始结果和实验报告。论文正文由其他人负责，不启动论文写作或投稿流程。

先读取我提供的项目代码、方法说明、数据和已有结果，确定实验要检验的问题。资料已经足够时直接推进；如果缺少研究方案、数据或算力等会影响执行的关键信息，只问缺失项。

一、准备 Skills
从 https://github.com/hansu650/Auto-claude-code-research-in-sleep 获取 codex/experiment-skills-share-20260915 分支，这是本机更新版的实验分享入口。使用 Codex 时，先读 skills/skills-codex/README.md，再按当前环境的安装说明准备以下 Skills：
- experiment-plan：实验计划。
- run-experiment：运行实验。
- analyze-results：汇总与分析结果。
- result-to-claim：判断结果支持哪些结论。
- ablation-planner：按需要细化消融。
- experiment-audit：交付前核查实验。
- monitor-experiment：长任务按需查看进度。
保留共享引用和必要工具，记录版本。结合已有安装和当前可用能力执行，不覆盖无关配置。这里只使用实验阶段；实际未完成的审查如实注明。

二、实验范围
主要运行我们的方法，以及验证模块贡献所必需的自身消融和简单对照。按实际结构设计原始骨干、加单个模块、完整方法等配置；原始骨干用于自身消融时也需要按相同设置运行。

其他论文的方法优先引用原论文或官方仓库已经公布的结果，不默认逐个重跑。每个引用数字记录来源链接、表格或文件位置、数据版本、划分、指标定义和评估协议。比较条件一致时才进行直接对比；不同条件的结果单列为文献参考，不据此宣称性能提升。

三、运行要求
先冻结数据划分、预处理、指标实现、阈值规则和调参范围，再做小规模试跑，随后开展必要的正式实验。模型选择和调参使用训练集或验证集，不能根据测试结果反复挑选最优配置。

在当前项目中使用专用环境，先核对现有数据与缓存能否复用。实际训练、推理和缓存复算分别记录。有随机性的实验根据预算安排重复运行；确定性流程不机械增加重复次数。优先完成主结果和必要消融，效率、敏感性或案例分析只在能回答具体问题时增加。

四、结果要求
表格区分“本项目运行”和“文献报告”，不把引用结果写成我们复现。不用只有汇总数值的文献结果编造逐样本检验、方差或显著性。结果不好时保留失败记录并解释原因，不补造提升数字或日志。

保存代码版本、环境依赖、配置、随机种子、数据来源与划分、运行命令、日志、原始预测或分数、评估脚本和汇总脚本。结果表要能追溯到这些输出；缓存复算不能冒充重新训练或完整流程重跑。

五、最终交付
整理一个普通文件夹，至少包含：
README、实验计划、代码与配置、环境说明、数据说明及划分、运行日志、原始输出、结果表、baseline 来源与可比性说明，以及必要的分析图和实验报告。
报告写清楚：实际跑了什么、哪些结果来自引用、哪些结论得到支持、哪些仍不确定，以及怎样复现。

先检查现有材料，形成最小必要实验计划，然后在已有授权和算力预算内推进代码与实验。
```

转交时同时提供已有方法说明、项目代码或仓库、数据位置和可用算力；提示词本身不替代这些输入。
