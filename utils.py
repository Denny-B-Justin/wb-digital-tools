"""
utils.py
--------
Reusable component builders for the Digital Workspace app.
Keeping these out of app.py keeps the layout/callback file readable.
"""

from dash import html, dcc

from constants import (
    TOOLS,
    PIA_COUNTRIES,
    pia_url_for,
    IFRAME_ASPECT_RATIO,
)


def eyebrow(text, extra_class=""):
    return html.P(text, className=f"eyebrow {extra_class}".strip())


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
            # html.Span(country["flag"], className="chip-flag"),
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

    The iframe sits inside a fixed-aspect-ratio container (instead of a
    flat pixel height) so it scales cleanly at any screen width without
    cropping the bottom of the embedded dashboard.
    """
    return html.Div(
        [
            html.Div(
                html.A(
                    "Open full window \u2197",
                    href=url,
                    target="_blank",
                    rel="noopener noreferrer",
                    className="frame-fallback-link",
                ),
                className="frame-toolbar",
            ),
            html.Div(
                html.Iframe(src=url, key=key, className="tool-iframe"),
                className="tool-iframe-aspect",
                style={"aspectRatio": IFRAME_ASPECT_RATIO},
            ),
        ],
        className="frame-wrapper",
    )


