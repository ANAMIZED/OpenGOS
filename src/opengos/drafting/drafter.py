"""
Proposal Drafter

Generates structured draft outlines and narrative scaffolding for grant
and public-goods funding applications. Designed to be grounded in a
ProjectProfile and a specific opportunity.
"""

from __future__ import annotations

from typing import Any

from opengos.profile.steward import ProjectProfile, get_steward


class ProposalDrafter:
    """Lightweight drafting helper that produces grounded structured outlines."""

    def draft_outline(
        self,
        profile: ProjectProfile,
        opportunity_title: str,
        opportunity_description: str | None = None,
        opportunity_type: str = "grant",
    ) -> dict[str, Any]:
        focus = (
            ", ".join(profile.focus_areas)
            if profile.focus_areas
            else "open-source AI and public goods"
        )

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
            sections.insert(
                1,
                {
                    "section": "Why This Public-Goods Funding Vehicle",
                    "guidance": (
                        "Explain why a donation / sponsorship / quadratic funding mechanism "
                        "is the right fit versus a traditional grant, and how transparency "
                        "and community governance will be maintained."
                    ),
                },
            )

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
        focus = ", ".join(profile.focus_areas[:3]) if profile.focus_areas else "open-source AI"
        return (
            f"{profile.name} is an open-source effort focused on {focus}. "
            f"We are seeking support through '{opportunity_title}' to accelerate "
            f"development, documentation, and community growth while keeping all outputs "
            f"publicly available under a permissive license. "
            f"{profile.description or 'Our work directly advances public-goods AI infrastructure.'}"
        )


async def outline(opportunity_id: str, project_name: str | None = None) -> dict[str, Any]:
    """MCP-facing helper: build an outline for an opportunity + optional project name."""
    from opengos.grants_client import get_client

    client = await get_client()
    results = await client.search(keyword=opportunity_id, rows=10)
    match = None
    for g in results:
        if g.id == opportunity_id or (
            g.opportunity_number and opportunity_id in str(g.opportunity_number)
        ):
            match = g
            break
    if not match and results:
        match = results[0]

    steward = get_steward()
    profiles = steward.list_profiles()
    if project_name:
        profile = next((p for p in profiles if p.name.lower() == project_name.lower()), None)
        if profile is None:
            profile = steward.from_text(
                profile_id=project_name.lower().replace(" ", "-"),
                name=project_name,
                description=project_name,
            )
    elif profiles:
        profile = profiles[0]
    else:
        profile = steward.from_text(
            profile_id="default",
            name=project_name or "Open Source Project",
            description="Open-source public goods project",
            focus_areas=["open-source", "ai"],
        )

    title = match.title if match else opportunity_id
    description = match.description if match else None
    drafter = ProposalDrafter()
    result = drafter.draft_outline(
        profile=profile,
        opportunity_title=title,
        opportunity_description=description,
    )
    if match:
        result["opportunity_id"] = match.id
        result["source_url"] = match.source_url
        result["provenance"] = {
            "source": match.source,
            "retrieved_at": match.retrieved_at,
        }
    return result
