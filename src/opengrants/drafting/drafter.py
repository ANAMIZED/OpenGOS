"""
Proposal Drafter

Generates structured draft outlines and narrative scaffolding for grant
and public-goods funding applications. Designed to be grounded in a
ProjectProfile and a specific opportunity.
"""

from __future__ import annotations

from typing import Any

from opengrants.profile.steward import ProjectProfile


class ProposalDrafter:
    """
    Lightweight drafting helper.

    In full agentic mode this will call an LLM with strong grounding.
    For now it produces high-quality structured outlines that an LLM
    (or human) can expand, keeping the MCP server dependency-light.
    """

    def draft_outline(
        self,
        profile: ProjectProfile,
        opportunity_title: str,
        opportunity_description: str | None = None,
        opportunity_type: str = "grant",
    ) -> dict[str, Any]:
        """Produce a structured proposal outline tailored to the profile + opportunity."""

        focus = ", ".join(profile.focus_areas) if profile.focus_areas else "open-source AI and public goods"

        sections = [
            {
                "section": "Executive Summary / Abstract",
                "guidance": (
                    f"Summarize the project '{profile.name}' and its alignment with "
                    f"'{opportunity_title}'. Emphasize open-source outputs, public-goods impact, "
                    f"and the specific problem being solved in {focus}."
                ),
            },
            {
                "section": "Problem Statement & Motivation",
                "guidance": (
                    "Describe the gap in current open-source / AI infrastructure or research "
                    "that this work addresses. Reference the broader public-goods need."
                ),
            },
            {
                "section": "Project Description & Approach",
                "guidance": (
                    f"Detail the technical approach of {profile.name}. "
                    f"Highlight methodology, open-source licensing ({profile.open_source_license or 'permissive'}), "
                    "reproducibility, and community involvement."
                ),
            },
            {
                "section": "Open-Source & Public-Goods Commitment",
                "guidance": (
                    "Explicitly state release plans (code, models, data, documentation), "
                    "license, contribution guidelines, and how the work will remain a public good."
                ),
            },
            {
                "section": "Team & Prior Work",
                "guidance": (
                    f"Describe the team behind {profile.name}. "
                    "Reference relevant prior open-source contributions, papers, or deployments."
                ),
            },
            {
                "section": "Impact & Evaluation",
                "guidance": (
                    "Define success metrics (adoption, citations, downstream projects, "
                    "community health) and how impact will be measured and reported."
                ),
            },
            {
                "section": "Timeline & Budget Narrative",
                "guidance": (
                    "High-level milestones and budget justification. "
                    "Tie costs to open-source deliverables and community support."
                ),
            },
        ]

        if opportunity_type in ("donation", "sponsorship", "collective", "quadratic"):
            sections.insert(1, {
                "section": "Why This Public-Goods Funding Vehicle",
                "guidance": (
                    "Explain why a donation / sponsorship / quadratic funding mechanism "
                    "is the right fit versus a traditional grant, and how transparency "
                    "and community governance will be maintained."
                ),
            })

        return {
            "profile_id": profile.id,
            "profile_name": profile.name,
            "opportunity_title": opportunity_title,
            "opportunity_type": opportunity_type,
            "focus_areas": profile.focus_areas,
            "keywords": profile.keywords,
            "sections": sections,
            "suggested_title": f"{profile.name}: Advancing {focus} as a Public Good",
            "notes": (
                "This is a grounded outline. Expand each section with concrete evidence "
                "from the project README, prior releases, and the funder's own language. "
                "Always cite the opportunity source and keep claims verifiable."
            ),
        }

    def draft_short_pitch(self, profile: ProjectProfile, opportunity_title: str) -> str:
        """One-paragraph pitch useful for sponsorship or quick applications."""
        focus = ", ".join(profile.focus_areas[:3]) if profile.focus_areas else "open-source AI"
        return (
            f"{profile.name} is an open-source effort focused on {focus}. "
            f"We are seeking support through '{opportunity_title}' to accelerate "
            f"development, documentation, and community growth while keeping all outputs "
            f"publicly available under a permissive license. "
            f"{profile.description or 'Our work directly advances public-goods AI infrastructure.'}"
        )
