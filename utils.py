"""
utils.py
--------
Reusable component builders for the PIM-PAM Digital Workspace app.
Keeping these out of app.py keeps the layout/callback file readable.
"""

from dash import html, dcc

from constants import (
    TOOLS,
    PIA_COUNTRIES,
    pia_url_for,
    IFRAME_HEIGHT,
)


def grid_overlay():
    """A faint background grid, echoing the marketing site's hero texture."""
    return html.Div(className="grid-overlay", **{"aria-hidden": "true"})


def eyebrow(text, extra_class=""):
    return html.P(text, className=f"eyebrow {extra_class}".strip())


def tool_badge(tool):
    """A logo-free acronym badge used instead of any imagery/branding."""
    return html.Div(
        tool["acronym"],
        className="tool-badge",
        style={
            "background": f"linear-gradient(135deg, {tool['accent']}22, {tool['accent']}0d)",
            "color": tool["accent"],
            "borderColor": f"{tool['accent']}55",
        },
    )


def hero_tool_card(tool):
    """One of the three top-level cards in the hero's tool overview strip."""
    return html.Button(
        [
            html.Div(
                [
                    tool_badge(tool),
                    html.Span(tool["family"], className="tool-family-tag"),
                ],
                className="tool-card-top",
            ),
            html.H3(tool["name"], className="tool-card-name"),
            html.P(tool["summary"], className="tool-card-summary"),
            html.Div("Open in workspace \u2192", className="tool-card-cta"),
        ],
        id={"type": "tool-select", "index": tool["id"]},
        n_clicks=0,
        className="tool-card",
    )


def workbench_tab(tool, is_active):
    return html.Button(
        [
            html.Span(tool["acronym"], className="tab-acronym"),
            html.Span(tool["name"], className="tab-name"),
        ],
        id={"type": "tool-select", "index": tool["id"]},
        n_clicks=0,
        className=f"workbench-tab {'is-active' if is_active else ''}",
    )


def workbench_tabs(active_tool_id):
    return [workbench_tab(t, t["id"] == active_tool_id) for t in TOOLS]


def country_chip(country, is_active):
    return html.Button(
        [
            html.Span(country["flag"], className="chip-flag"),
            html.Span(country["name"], className="chip-name"),
        ],
        id={"type": "country-select", "index": country["id"]},
        n_clicks=0,
        className=f"country-chip {'is-active' if is_active else ''}",
        title=country["region"],
    )


def country_switcher(active_country_id):
    return html.Div(
        [
            html.Span("Country instance:", className="switcher-label"),
            html.Div(
                [country_chip(c, c["id"] == active_country_id) for c in PIA_COUNTRIES],
                className="country-chip-row",
            ),
        ],
        className="country-switcher",
    )


def embedded_frame(url, key):
    """An iframe embed with a fallback 'open in new tab' affordance.

    World Bank / Posit Connect deployments may set frame-ancestor or
    X-Frame-Options headers that block embedding entirely; the fallback
    link is provided so the tool is always reachable even if the frame
    itself renders blank.
    """
    return html.Div(
        [
            html.Div(
                [
                    # html.Span("Live embed", className="frame-status-dot-label"),
                    html.A(
                        "Open full window \u2197",
                        href=url,
                        target="_blank",
                        rel="noopener noreferrer",
                        className="frame-fallback-link",
                    ),
                ],
                className="frame-toolbar",
            ),
            html.Iframe(
                src=url,
                key=key,
                className="tool-iframe",
                style={"height": IFRAME_HEIGHT},
            ),
        ],
        className="frame-wrapper",
    )


def tool_detail_panel(tool):
    """Description block shown above the embed for the active tool."""
    return html.Div(
        [
            html.Div(
                [
                    tool_badge(tool),
                    html.Div(
                        [
                            html.Span(tool["family"], className="tool-family-tag"),
                            html.H2(tool["name"], className="panel-title"),
                        ]
                    ),
                ],
                className="panel-header",
            ),
            html.P(tool["description"], className="panel-description"),
            html.Ul(
                [html.Li(b) for b in tool["bullets"]],
                className="panel-bullets",
            ),
        ],
        className="panel-detail",
    )


def workbench_panel(active_tool_id, active_country_id, tools_by_id):
    tool = tools_by_id[active_tool_id]
    children = [tool_detail_panel(tool)]

    if tool["kind"] == "pia":
        children.append(country_switcher(active_country_id))
        url = pia_url_for(active_country_id)
        children.append(embedded_frame(url, key=f"pia-{active_country_id}"))
    else:
        children.append(embedded_frame(tool["url"], key=tool["id"]))

    return children