"""
constants.py
------------
All static content and configuration for the Digital Workspace app.
Keeping this separate from app.py means new tools / countries can be added
here without touching any layout or callback logic.
"""

# ---------------------------------------------------------------------------
# Brand / design tokens (mirrors the Digital Workspace marketing site palette so the
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
    "World Bank builds digital tools for governments to plan, finance, and manage public "
    "infrastructure more effectively. Historically these tools have lived on separate "
    "domains, each requiring its own link, login screen, and browser tab. This workspace "
    "brings three of them together in one place \u2014 so an analyst comparing a country's "
    "governance operations, its infrastructure access gaps, and its benchmarking scores "
    "can do it in one session, without losing their place."
)

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
# used on the marketing site (geospatial planning / analytics & AI /
# data benchmarking) purely as an organizing label, not a UI dependency.
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "id": "pia",
        "acronym": "PIA",
        "name": "Public Infrastructure Access",
        "family": "Geospatial Planning",
        "summary": "Geospatial optimizer that helps governments decide where to place new hospital to maximize how many people gain access to it.",
        "description": (
            "PIA is a geospatial optimizer that helps governments decide where to place new "
            "hospital to maximize how many people gain "
            "reasonable access to it. It runs a maximum covering location model over hexagonal "
            "grids of population and travel-time data, then lets planners explore the "
            "recommended sites on an interactive map."
        ),
        "bullets": [
            "Deployed separately for five countries: Zambia, Malawi, Serbia, Nepal, and Uzbekistan.",
            "Built on H3 hexagonal indexing, population rasters, and OpenStreetMap data.",
            "PIA gives planners and policymakers an interactive way to explore infrastructure gaps on the ground",
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
        "summary": "Helps rapidly identify and analyze World Bank operations across lending instruments, sectors, and thematic areas.",
        "description": (
            "GoAT helps analysts rapidly identify and analyze World Bank operations across lending instruments, sectors, and thematic areas."
        ),
        "bullets": [
            "Supports keyword-driven searches across Development Policy Operations (DPOs), Investment Project Financing (IPFs), and Program-for-Results (PforR) operations.",
            "Leverages customizable thematic keyword hierarchies to match project development objectives, prior actions, and results indicators.",
            "Offers real-time filtering, interactive dashboards, and downloadable project datasets to facilitate operational analysis and portfolio insights.",
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
        "summary": "Benchmarks a country's public financial management performance against regional and global peers.",
        "description": (
            "CBD benchmarks a country's public financial management performance against regional "
            "and global peers using indicators such as Infrastructure Efficiency Scores, the "
            "GovTech Maturity Index, and the Climate Change Institutional Assessment, presented "
            "through interactive graphs and maps."
        ),
        "bullets": [
            "Combines global indices with regional and country-level datasets to support comparative analysis.",
            "Integrates metrics and indicators derived from established World Bank methodologies and assessment frameworks.",
            "Enables users to explore regional trends, benchmark countries against peers, and analyze country-level performance across multiple dimensions.",
        ],
        "accent": COLORS["accent_4"],
        "url": "https://datanalytics.worldbank.org/content/4522077e-7857-468c-ab5a-366588a11dd0/",
        "kind": "simple",
    },
]

TOOLS_BY_ID = {t["id"]: t for t in TOOLS}
DEFAULT_TOOL_ID = "pia"

# Embedded tools render inside a fixed-aspect-ratio box rather than a flat
# pixel height, so they resize cleanly across screen widths. These
# dashboards are landscape (map + side panels), so a widescreen 16:9 ratio
# is used -- change this one value to reshape every embed at once.
IFRAME_ASPECT_RATIO = "16 / 9"