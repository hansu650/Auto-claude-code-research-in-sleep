# `skills-codex` 说明

这是主线 `skills/` 的 Codex 原生镜像 / 适配层，不是独立主线产品。

## 当前范围

- 基座覆盖：主线 `skills/` 的 `81` 个 skill 全量同步
- 支持目录：`shared-references/`，与主线 `30/30` 名称完整对齐
- reviewer-heavy skill 的默认 reviewer 契约：
  - 首轮：`spawn_agent`
  - 续接：当前宿主提供的工具（`send_input` 或 `followup_task`）
  - 推理强度：`xhigh`；明确标记的 deep-audit skill 使用 `ultra`
  - 基础 Codex 自审：`review_independence: same-family`、
    `acceptance_status: provisional`
  - Claude/Gemini overlay 或确定性验证：`acceptance_status: accepted`
- 可选 overlay：
  - `skills-codex-claude-review`
  - `skills-codex-gemini-review`

## 推荐安装方式

Codex 路线默认推荐项目级安装：

```bash
git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git ~/aris_repo
cd ~/your-project

bash ~/aris_repo/tools/install_aris_codex.sh .
```

安装后会形成扁平布局：

```text
.agents/skills/<skill-name> -> ~/aris_repo/skills/skills-codex/<skill-name>
.aris/installed-skills-codex.txt
AGENTS.md   # 自动写入 Codex 管理块
```

上游更新后收敛：

```bash
cd ~/aris_repo && git pull
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile
```

只卸载受管的 Codex skill：

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --uninstall
```

## Overlay 安装

先装基座，再选装 overlay：

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile --with-claude-review-overlay
```

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile --with-gemini-review-overlay
```

overlay 只替换 reviewer 路由，不替换基座 mirror，也不改变 executor 语义。

## Copy 安装与更新

如果你明确想用 copy 安装，而不是受管 symlink：

```bash
mkdir -p ~/.codex/skills
cp -a ~/aris_repo/skills/skills-codex/. ~/.codex/skills/
```

更新 copy 安装请使用：

```bash
bash ~/aris_repo/tools/smart_update_codex.sh
bash ~/aris_repo/tools/smart_update_codex.sh --apply
```

项目级 copy 安装则使用：

```bash
bash ~/aris_repo/tools/smart_update_codex.sh --project ~/your-project
bash ~/aris_repo/tools/smart_update_codex.sh --project ~/your-project --apply
```

`smart_update_codex.sh` 会拒绝更新由 `install_aris_codex.sh` 管理的 symlink 安装，并提示改用 `install_aris_codex.sh --reconcile`。

## 按任务范围执行

以用户要求的交付物和会话中已有授权为准。草稿流程使用合理默认值继续；只有缺失信息会实质改变范围、成本或不可逆结果时才询问。工作量档位和默认轮数是规划上限，不是必须做满的配额；完成交付和必要检查后即可结束。

某项审查或验证不可用时，只阻塞依赖它的结论和步骤，继续其他有用且已授权的工作，并如实报告验证状态。基座 reviewer 仍是同族审查，结果保持 provisional。本机路径和环境管理偏好保存在用户自己的配置中。

## 不允许降级的 Skill

以下 4 个 skill 不允许静默降级：

- `comm-lit-review`
- `research-lit`
- `paper-poster-html`
- `pixel-art`

缺少必需来源、reviewer 或预览能力时，明确说明缺少什么以及所需配置，不得把不完整覆盖或未验证结果写成通过。`research-lit` 可以继续其他已授权来源并标明覆盖缺口；用户要求独占来源时仍需该来源。制品流程可继续支持的准备和导出，依赖缺失能力的验收保持未验证。
