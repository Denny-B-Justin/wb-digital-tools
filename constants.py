"""
constants.py
------------
All static content and configuration for the PIM-PAM Digital Workspace app.
Keeping this separate from app.py means new tools / countries can be added
here without touching any layout or callback logic.
"""

# ---------------------------------------------------------------------------
# Brand / design tokens (mirrors the PIM-PAM marketing site palette so the
# workspace feels like a natural extension of it, without reusing its logo
# or copy).
# ---------------------------------------------------------------------------
COLORS = {
    "bg": "#FFFFFF",
    "surface": "#F7F8FB",
    "surface_2": "#FFFFFF",
    "text": "#14192B",
    "muted": "#5B6478",
    "accent_1": "#4345aa",   # indigo
    "accent_2": "#1f9d67",   # green (deepened for contrast on white)
    "accent_3": "#1a92a1",   # teal (deepened for contrast on white)
    "accent_4": "#d9560f",   # orange (deepened for contrast on white)
}

APP_TITLE = "PIM-PAM Digital Workspace"
APP_TAGLINE = "One workspace for the Public Infrastructure & Asset Management toolkit."

MISSION_STATEMENT = (
    ""
)

# MISSION_STATEMENT = (
#     "PIM-PAM builds digital tools for governments to plan, finance, and manage public "
#     "infrastructure more effectively. Historically these tools have lived on separate "
#     "domains, each requiring its own link, login screen, and browser tab. This workspace "
#     "brings three of them together in one place \u2014 so an analyst comparing a country's "
#     "governance operations, its infrastructure access gaps, and its benchmarking scores "
#     "can do it in one session, without losing their place."
# )

# ---------------------------------------------------------------------------
# PIA \u2014 Public Infrastructure Access tool
# One base Posit Connect app, five country instances served via a query
# string (?country=slug). We model these as a single tool with a country
# switcher rather than five separate tool entries.
# ---------------------------------------------------------------------------
PIA_BASE_URL = "https://datanalytics.worldbank.org/content/1cc36c57-f12d-4aa8-92a2-196bb0ea605f/"

PIA_COUNTRIES = [
    {"id": "zambia", "name": "Zambia", "flag": "\U0001F1FF\U0001F1F2", "region": "Southern Africa"},
    {"id": "malawi", "name": "Malawi", "flag": "\U0001F1F2\U0001F1FC", "region": "Southern Africa"},
    {"id": "serbia", "name": "Serbia", "flag": "\U0001F1F7\U0001F1F8", "region": "Western Balkans"},
    {"id": "nepal", "name": "Nepal", "flag": "\U0001F1F3\U0001F1F5", "region": "South Asia"},
    {"id": "uzbekistan", "name": "Uzbekistan", "flag": "\U0001F1FA\U0001F1FF", "region": "Central Asia"},
]
PIA_DEFAULT_COUNTRY = "zambia"


def pia_url_for(country_id: str) -> str:
    """Build the PIA deployment URL for a given country slug."""
    valid_ids = {c["id"] for c in PIA_COUNTRIES}
    if country_id not in valid_ids:
        return PIA_BASE_URL
    return f"{PIA_BASE_URL}?country={country_id}"


# ---------------------------------------------------------------------------
# The three tools that make up the workspace. "family" mirrors the grouping
# used on the PIM-PAM marketing site (geospatial planning / analytics & AI /
# data benchmarking) purely as an organizing label, not a UI dependency.
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "id": "pia",
        "acronym": "PIA",
        "name": "Public Infrastructure Access",
        "family": "Geospatial Planning",
        "summary": "Optimize where new roads, bridges, and health facilities go to widen access.",
        "description": (
            "PIA is a geospatial optimizer that helps governments decide where to place new "
            "infrastructure \u2014 clinics, roads, bridges \u2014 to maximize how many people gain "
            "reasonable access to it. It runs a maximum covering location model over hexagonal "
            "grids of population and travel-time data, then lets planners explore the "
            "recommended sites on an interactive map."
        ),
        "bullets": [
            "Deployed separately for five countries: Zambia, Malawi, Serbia, Nepal, and Uzbekistan.",
            "Built on H3 hexagonal indexing, population rasters, and OpenStreetMap road networks.",
            "Uses a greedy approximation algorithm with a proven (1\u22121/e) coverage guarantee.",
        ],
        "accent": COLORS["accent_2"],
        "url": PIA_BASE_URL,
        "kind": "pia",  # special-cased in the workbench (has a country switcher)
    },
    {
        "id": "goat",
        "acronym": "GoAT",
        "name": "Governance Operations Analytics Tool",
        "family": "Analytics & AI",
        "summary": "Search World Bank lending operations for PIM, PAM, and SOE-related themes.",
        "description": (
            "GoAT lets analysts search across the World Bank's Development Policy Operations, "
            "Investment Project Financing, and Program-for-Results lending for language related "
            "to public investment management, public asset management, and state-owned "
            "enterprises \u2014 across more than ten thousand projects."
        ),
        "bullets": [
            "Keyword hierarchies map raw project text to thematic areas (PIM / PAM / SOE).",
            "Sunburst and stacked-bar views summarize how themes trend across regions and time.",
            "Results are exportable to CSV for further offline analysis.",
        ],
        "accent": COLORS["accent_3"],
        "url": "https://datanalytics.worldbank.org/content/5e009cdd-7b07-4567-8f45-eb3a3f476abc/",
        "kind": "simple",
    },
    {
        "id": "cbd",
        "acronym": "CBD",
        "name": "Country Benchmarking Dashboard",
        "family": "Data Benchmarking",
        "summary": "Compare countries on governance, climate, and infrastructure indices via choropleth maps.",
        "description": (
            "CBD benchmarks a country's public financial management for climate action against "
            "its peers, using indices such as the GovTech Maturity Index, the Climate Change "
            "Institutional Assessment, and infrastructure efficiency scores, all rendered as "
            "interactive choropleth maps."
        ),
        "bullets": [
            "Blends global indices (GTMI, PEFA) with regional ECA-specific datasets (CCIA, PIIAG).",
            "Every indicator traces back to its source \u2014 World Bank, IMF, or WBG.",
            "Built as a Dash app on Unity Catalog Delta tables for governments and finance ministries.",
        ],
        "accent": COLORS["accent_4"],
        "url": "https://datanalytics.worldbank.org/content/4522077e-7857-468c-ab5a-366588a11dd0/",
        "kind": "simple",
    },
]

TOOLS_BY_ID = {t["id"]: t for t in TOOLS}
DEFAULT_TOOL_ID = "pia"

IFRAME_HEIGHT = "780px"