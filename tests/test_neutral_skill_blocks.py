from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


VARIANTS = {
    "paper-plan": [
        SKILLS / "paper-plan" / "SKILL.md",
        SKILLS / "skills-codex" / "paper-plan" / "SKILL.md",
        SKILLS / "skills-codex-claude-review" / "paper-plan" / "SKILL.md",
        SKILLS / "skills-codex-gemini-review" / "paper-plan" / "SKILL.md",
    ],
    "paper-write": [
        SKILLS / "paper-write" / "SKILL.md",
        SKILLS / "skills-codex" / "paper-write" / "SKILL.md",
        SKILLS / "skills-codex-claude-review" / "paper-write" / "SKILL.md",
        SKILLS / "skills-codex-gemini-review" / "paper-write" / "SKILL.md",
    ],
    "paper-figure": [
        SKILLS / "paper-figure" / "SKILL.md",
        SKILLS / "skills-codex" / "paper-figure" / "SKILL.md",
        SKILLS / "skills-codex-claude-review" / "paper-figure" / "SKILL.md",
        SKILLS / "skills-codex-gemini-review" / "paper-figure" / "SKILL.md",
    ],
    "paper-compile": [
        SKILLS / "paper-compile" / "SKILL.md",
        SKILLS / "skills-codex" / "paper-compile" / "SKILL.md",
    ],
}

PAPER_WRITING_ORCHESTRATORS = [
    SKILLS / "paper-writing" / "SKILL.md",
    SKILLS / "skills-codex" / "paper-writing" / "SKILL.md",
    SKILLS / "skills-codex-gemini-review" / "paper-writing" / "SKILL.md",
]
PAPER_PLAN_TEMPLATE = REPO_ROOT / "templates" / "PAPER_PLAN_TEMPLATE.md"

CLAIM_LEDGER_HEADER = (
    "| Claim ID | Role | Exact claim | Comparator or N/A | "
    "Evidence (experiment/table/figure/theorem/proof) | Scope/data access | "
    "Selection/training/adaptation or N/A | Limitation | Forbidden expansion |"
)
COVERAGE_INDEX_HEADER = (
    "| Claim ID | Abstract move | Intro bullet | Body subsection | "
    "Evidence location | Conclusion sentence |"
)
LAYOUT_CONTRACT_HEADER = (
    "| Label | Kind | Width class | Preferred placement | Must preserve | "
    "Caption budget | Priority |"
)


EXPECTED_DESCRIPTIONS = {
    "paper-plan": "Plan and structure a research paper from available project evidence. Use for paper outlines, claim-to-section plans, Abstract plans, Introduction contribution plans, Method organization, Conclusion plans, and figure/table plans; common requests include 写大纲, 论文规划, paper outline, and plan the paper. In a new or context-free folder, inspect local artifacts first and request only missing blocking input.",
    "paper-write": "Write, rewrite, or polish research-paper prose and LaTeX from available project evidence. Use for a full draft or individual sections, especially the Abstract, Introduction and contribution bullets, Method, Conclusion, limitations, and future work; common requests include 写论文, 改摘要, write paper, rewrite abstract, and polish conclusion. In a new or context-free folder, inspect local artifacts first and request only missing blocking input.",
    "paper-figure": "Create or revise standalone publication-quality paper figures and tables from plans, data, or existing artifacts. Use for plots, comparison and ablation tables, multi-panel figures, diagrams, captions, table typography, and standalone figure/table layout; common requests include 画图, 画表, 改表格, paper figures, and redesign this table. In a new or context-free folder, inspect local artifacts first and request only missing blocking input.",
    "paper-compile": "Compile, repair, format, and visually verify integrated LaTeX papers and PDFs. Use for building a PDF, fixing LaTeX errors or warnings, layout-only changes, typography, page limits, and integrated figure/table placement; common requests include 编译论文, 排版论文, build PDF, fix LaTeX, and move this figure or table. In a new or context-free folder, inspect local build instructions and sources first and request only missing blocking input.",
}


BEGIN_COLD = "<!-- BEGIN ARIS NEUTRAL: COLD START -->"
END_COLD = "<!-- END ARIS NEUTRAL: COLD START -->"
BEGIN_LAYOUT = "<!-- BEGIN ARIS NEUTRAL: PUBLICATION LAYOUT -->"
END_LAYOUT = "<!-- END ARIS NEUTRAL: PUBLICATION LAYOUT -->"
BEGIN_BACKENDS = "<!-- BEGIN ARIS NEUTRAL: DIAGRAM BACKENDS -->"
END_BACKENDS = "<!-- END ARIS NEUTRAL: DIAGRAM BACKENDS -->"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def description(text: str) -> str:
    match = re.search(r'^description: "([^\n]*)"$', text, flags=re.MULTILINE)
    assert match, "missing one-line quoted description"
    return match.group(1)


def marked_block(text: str, begin: str, end: str) -> str:
    assert text.count(begin) == 1
    assert text.count(end) == 1
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    return text[start:finish]


def test_cold_start_contract_is_complete_and_variant_neutral() -> None:
    banned = ("ViTWeave", "SensorScope", "DFormerv2", "0.678", "Fig. 7", "page 7")
    for name, paths in VARIANTS.items():
        texts = []
        for path in paths:
            assert path.is_file(), path
            text = read(path)
            texts.append(text)
            assert description(text) == EXPECTED_DESCRIPTIONS[name]
            block = marked_block(text, BEGIN_COLD, END_COLD)
            assert text.index("# ") < text.index(BEGIN_COLD)
            for token in banned:
                assert token not in description(text)
                assert token not in block

        blocks = {marked_block(text, BEGIN_COLD, END_COLD) for text in texts}
        assert len(blocks) == 1, f"{name} cold-start contract drifted across variants"
        block = next(iter(blocks)).lower()
        assert "prior chat" in block or "prior conversation" in block
        assert "current directory" in block
        assert "proceed" in block
        assert "smallest blocking" in block or "minimum blocking" in block


def test_figure_publication_layout_block_is_variant_neutral() -> None:
    texts = [read(path) for path in VARIANTS["paper-figure"]]
    blocks = {marked_block(text, BEGIN_LAYOUT, END_LAYOUT) for text in texts}
    assert len(blocks) == 1
    block = next(iter(blocks))
    assert "standalone artifact gate" in block
    assert "integrated-page validation" in block
    assert "publication-layout-gates.md" in block


def test_figure_backend_routing_is_explicit_and_variant_neutral() -> None:
    texts = [read(path) for path in VARIANTS["paper-figure"]]
    blocks = {marked_block(text, BEGIN_BACKENDS, END_BACKENDS) for text in texts}
    assert len(blocks) == 1
    block = next(iter(blocks))
    for value, delegate in (
        ("figurespec", "figure-spec"),
        ("drawio", "drawio-paper-diagram"),
        ("gemini", "paper-illustration"),
        ("codex-image2", "paper-illustration-image2"),
        ("mermaid", "mermaid-diagram"),
    ):
        assert f"| `{value}` | `{delegate}` |" in block
    assert "`manual` or `false`" in block
    assert "resume this skill" in block
    assert "mandatory standalone artifact gate" in block


def test_new_shared_references_are_mirrored_byte_for_byte() -> None:
    for name in (
        "section-blueprints.md",
        "writing-principles.md",
        "publication-layout-gates.md",
    ):
        main = (SKILLS / "shared-references" / name).read_bytes()
        codex = (SKILLS / "skills-codex" / "shared-references" / name).read_bytes()
        assert main == codex, f"shared reference mirror drift: {name}"


def test_empirical_ai_method_front_matter_profile_is_fixed_and_mirrored() -> None:
    blueprint = read(SKILLS / "shared-references" / "section-blueprints.md")
    required_profile_lines = (
        "### Empirical AI method default: exactly 10 sentences",
        "### Empirical AI method default: exactly 3 bullets with 2 / 3 / 3 sentences",
        "### Empirical AI method default: exactly 8 sentences",
        "Never copy exemplar phrasing or invent an",
    )
    for line in required_profile_lines:
        assert line in blueprint

    abstract_roles = (
        "**Setting:**",
        "**Limitation:**",
        "**Reframing:**",
        "**Method contract:**",
        "**Mechanism 1:**",
        "**Mechanism 2:**",
        "**Design boundary:**",
        "**Primary evidence:**",
        "**Secondary evidence:**",
        "**Takeaway:**",
    )
    contribution_roles = (
        "**Problem/formulation — 2 sentences:**",
        "**Method/mechanism — 3 sentences:**",
        "**Evidence/scope — 3 sentences:**",
    )
    conclusion_roles = (
        "**Answer:**",
        "**Mechanism:**",
        "**Primary evidence:**",
        "**Secondary evidence:**",
        "**Interpretation:**",
        "**Limitation:**",
        "**Practical takeaway:**",
        "**Significance:**",
    )
    role_blocks = (
        (blueprint.split("## 2. Abstract Blueprint", 1)[1].split("## 3.", 1)[0], abstract_roles),
        (blueprint.split("## 3. Introduction Contribution Blueprint", 1)[1].split("## 4.", 1)[0], contribution_roles),
        (blueprint.split("## 5. Conclusion Blueprint", 1)[1].split("## 6.", 1)[0], conclusion_roles),
    )
    for block, roles in role_blocks:
        positions = [block.index(role) for role in roles]
        assert positions == sorted(positions), f"role order drifted: {roles}"

    for path in VARIANTS["paper-plan"]:
        text = read(path)
        assert "Abstract = 10 sentences" in text
        assert "`2 / 3 / 3` sentences" in text
        assert "Conclusion = 8 sentences" in text
        assert "roles and counts are fixed" in text
        assert "content remain specific to the paper's Claim Ledger" in text

    for path in VARIANTS["paper-write"]:
        text = read(path)
        assert "Abstract = exactly 10 sentences" in text
        assert "exactly 3 bullets with `2 / 3 / 3` sentences" in text
        assert "Conclusion = exactly 8 sentences" in text
        assert "prose and content must come from the paper's Claim Ledger" in text


def test_reference_ownership_and_routing() -> None:
    for path in VARIANTS["paper-plan"]:
        text = read(path)
        assert "section-blueprints.md" in text
        assert "publication-layout-gates.md" in text
        assert "Canonical Claim Ledger" in text
        assert "Front-Matter Coverage Index" in text

    for path in VARIANTS["paper-write"]:
        text = read(path)
        assert "section-blueprints.md" in text
        assert "Conclusion introduces no new" in text

    for path in VARIANTS["paper-figure"]:
        text = read(path)
        assert "standalone artifact gate" in text
        assert "dedicated publication-diagram skill" in text

    for path in VARIANTS["paper-compile"]:
        text = read(path)
        assert "publication-layout-gates.md" in text
        assert "integrated-page" in text
        assert "tlmgr install" not in text


def test_canonical_ledger_and_width_contract_have_no_legacy_conflicts() -> None:
    claim_texts = [
        read(path)
        for name in ("paper-plan", "paper-write")
        for path in VARIANTS[name]
    ]
    claim_texts.extend(
        read(SKILLS / root / "shared-references" / "section-blueprints.md")
        for root in (Path("."), Path("skills-codex"))
    )
    for text in claim_texts:
        assert "Claims-Evidence Matrix" not in text
        assert not re.search(r"claims?[- ]?(?:evidence[- ]?)?matrix", text, re.IGNORECASE)
        assert "Canonical Claim Ledger" in text

    for path in VARIANTS["paper-figure"]:
        text = read(path)
        assert r"0.48\textwidth" not in text
        assert r"0.95\textwidth" not in text
        assert r"\includegraphics[width=\columnwidth]" in text
        assert "Default Width Class" in text


def test_workflow3_and_plan_template_enforce_downstream_contracts() -> None:
    plan_texts = [read(path) for path in VARIANTS["paper-plan"]]
    template = read(PAPER_PLAN_TEMPLATE)

    for text in plan_texts:
        assert "## Figure Plan" not in text
        assert CLAIM_LEDGER_HEADER in text
        assert COVERAGE_INDEX_HEADER in text
        assert LAYOUT_CONTRACT_HEADER in text

    assert "## Claims-Evidence Matrix" not in template
    assert "## Figure Plan" not in template
    assert "## Canonical Claim Ledger" in template
    assert "## Front-Matter Coverage Index" in template
    assert "## Figure/Table Layout Contract" in template
    assert CLAIM_LEDGER_HEADER in template
    assert COVERAGE_INDEX_HEADER in template
    assert LAYOUT_CONTRACT_HEADER in template

    direct_backend_call = re.compile(
        r"^/(?:figure-spec|paper-illustration(?:-image2)?|"
        r"mermaid-diagram|drawio-paper-diagram)\b",
        flags=re.MULTILINE,
    )
    for path in PAPER_WRITING_ORCHESTRATORS:
        text = read(path)
        assert "Existing-plan compatibility gate" in text
        assert "Canonical Claim Ledger" in text
        assert "Front-Matter Coverage Index" in text
        assert "Figure/Table Layout Contract" in text
        assert CLAIM_LEDGER_HEADER.strip("| ") in text
        assert COVERAGE_INDEX_HEADER.strip("| ") in text
        assert LAYOUT_CONTRACT_HEADER.strip("| ") in text
        assert "Claims-Evidence Matrix" not in text
        assert not direct_backend_call.search(text)
        assert "paper-figure" in text
        assert "standalone artifact gate" in text

        improvement = text.index("### Phase 5: Auto Improvement Loop")
        final_layout = text.index("### Phase 5.95: Final Integrated-Page Gate")
        final_report = text.index("### Phase 6: Final Report")
        assert improvement < final_layout < final_report
        gate = text[final_layout:final_report]
        assert "/paper-compile" in gate
        assert "neighbor" in gate.lower()
        assert "all-page" in gate.lower() or "every page" in gate.lower()

    main_orchestrator = read(PAPER_WRITING_ORCHESTRATORS[0])
    assert "diagram-backend: manual" in main_orchestrator
    for path in PAPER_WRITING_ORCHESTRATORS:
        text = read(path)
        assert not re.search(
            r"illustration:\s*false.{0,100}skip\s+entirely",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )


def test_cold_start_descriptions_are_project_neutral() -> None:
    all_descriptions = "\n".join(
        description(read(path)) for paths in VARIANTS.values() for path in paths
    )
    assert "new or context-free folder" in all_descriptions
    for project_token in ("ViTWeave", "SensorScope", "MAIN", "DFormerv2"):
        assert project_token not in all_descriptions
