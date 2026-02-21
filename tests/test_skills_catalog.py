from __future__ import annotations

from pathlib import Path


SKILLS = Path("skills")


def test_every_skill_has_frontmatter_and_references() -> None:
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    assert skill_files, "Expected at least one skill"

    for skill in skill_files:
        text = skill.read_text()
        assert text.startswith("---\nname:"), f"Missing YAML frontmatter in {skill}"
        assert "description:" in text, f"Missing description in {skill}"
        refs = list((skill.parent / "references").glob("*.md"))
        assert refs, f"Expected references files for {skill.parent.name}"


def test_skill_reference_links_cover_requested_domains() -> None:
    all_refs = "\n".join(p.read_text() for p in SKILLS.glob("*/references/*.md"))

    checks = [
        "docs.structurizr.com",
        "developer.harness.io",
        "docs.flutter.dev",
        "dart.dev",
        "developer.hashicorp.com/terraform",
        "opentofu.org",
        "helm.sh/docs",
        "kubernetes.io/docs",
        "keycloak.org",
        "docs.python.org/3.14",
        "docs.astral.sh/uv",
        "github.com/anthropics/claude-code",
    ]
    for check in checks:
        assert check in all_refs, f"Missing expected domain/link marker: {check}"
