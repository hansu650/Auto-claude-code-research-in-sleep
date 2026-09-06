# `skills-codex`

Codex-native mirror and adaptation layer for the main ARIS `skills/` package.

## Scope

- Base mirror coverage: all `81` mainline skills under `skills/`
- Support directory: `shared-references/`, with all `30/30` mainline reference names mirrored
- Default reviewer contract for reviewer-heavy skills:
  - round 1: `spawn_agent`
  - follow-up: the live host's continuation tool (`send_input` or `followup_task`)
  - reasoning effort: `xhigh`, or `ultra` for the declared deep-audit skills
  - base Codex self-review: `review_independence: same-family`,
    `acceptance_status: provisional`
  - Claude/Gemini overlays or deterministic verification: `acceptance_status: accepted`
- Optional overlays:
  - `skills-codex-claude-review`
  - `skills-codex-gemini-review`

This package is still an appendage to the Claude mainline, not a separate Codex-first product line.

## Recommended Install

Project-local install is the default path for Codex:

```bash
git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git ~/aris_repo
cd ~/your-project

bash ~/aris_repo/tools/install_aris_codex.sh .
```

This creates a flat managed layout:

```text
.agents/skills/<skill-name> -> ~/aris_repo/skills/skills-codex/<skill-name>
.aris/installed-skills-codex.txt
AGENTS.md   # managed Codex block
```

Reconcile after upstream changes:

```bash
cd ~/aris_repo && git pull
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile
```

Uninstall only managed Codex entries:

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --uninstall
```

## Optional Overlays

Install the base first, then choose an overlay:

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile --with-claude-review-overlay
```

```bash
bash ~/aris_repo/tools/install_aris_codex.sh ~/your-project --reconcile --with-gemini-review-overlay
```

Overlays only replace reviewer routing. They do not replace the base mirror or the executor model.

## Copy Install and Update

If you intentionally use a copied Codex install instead of managed project symlinks:

```bash
mkdir -p ~/.codex/skills
cp -a ~/aris_repo/skills/skills-codex/. ~/.codex/skills/
```

Update copied installs with:

```bash
bash ~/aris_repo/tools/smart_update_codex.sh
bash ~/aris_repo/tools/smart_update_codex.sh --apply
```

For a copied project-local Codex install:

```bash
bash ~/aris_repo/tools/smart_update_codex.sh --project ~/your-project
bash ~/aris_repo/tools/smart_update_codex.sh --project ~/your-project --apply
```

`smart_update_codex.sh` refuses symlink-managed installs and redirects them to `install_aris_codex.sh --reconcile`.

## Scoped Execution

Follow the requested deliverable and existing session authorization. Drafting workflows proceed with reasonable defaults; ask when missing information materially changes scope, cost or irreversible outcomes. Workload profiles and default round counts are planning bounds, not quotas. Stop after the requested outcome and required checks are satisfied.

A missing review or verification capability blocks only the verdict and dependent steps. Continue useful authorized work and report its actual validation status. The base reviewer remains same-family and provisional. Machine-specific paths and environment preferences belong in the user's configuration.

## Non-Degrading Skills

The following Codex skills must not silently degrade when their required capability is missing:

- `comm-lit-review`
- `research-lit`
- `paper-poster-html`
- `pixel-art`

Report a missing required source, reviewer or preview capability and what setup is needed. Do not silently claim complete coverage or a verified result. In `research-lit`, continue other authorized sources with incomplete coverage marked; an exclusive-source request still depends on that source. For artifact workflows, continue supported preparation and exports while leaving dependent assurance unverified.
