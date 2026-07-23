"""
app.py
------
Digital Workspace \u2014 a single Dash app that aggregates three
World Bank tools (PIA, GoAT, CBD) behind one workbench, so a user
never has to juggle separate tabs/logins for tools built at different times
on different stacks.

Run locally with:  python app.py
"""

import dash
from dash import html, dcc, Input, Output, State, MATCH, ALL, ctx
import dash.exceptions

from constants import (
    APP_TITLE,
    APP_TAGLINE,
    MISSION_STATEMENT,
    TOOLS,
    TOOLS_BY_ID,
    DEFAULT_TOOL_ID,
    PIA_DEFAULT_COUNTRY,
    pia_url_for,
)
from utils import (
    eyebrow,
    workbench_tabs,
    country_switcher,
    embedded_frame,
)

app = dash.Dash(__name__, title=APP_TITLE, update_title=None)
server = app.server


def tool_badge(tool):
    """Render either a tool logo asset or a text fallback acronym badge."""
    logo = tool.get("logo")
    if logo:
        return html.Div(
            html.Img(
                src=app.get_asset_url(logo),
                alt=tool["name"],
                className="tool-badge-logo",
            ),
            className="tool-badge tool-badge-image",
        )

    return html.Div(
        tool["acronym"],
        className="tool-badge",
        style={
            "color": tool["accent"],
            "borderBottomColor": tool["accent"],
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
            html.A(
                "Open in workspace \u2192",
                href=tool["url"],
                target="_blank",
                rel="noopener noreferrer",
                className="tool-card-cta",
            ),
        ],
        id={"type": "tool-select", "index": tool["id"]},
        n_clicks=0,
        className="tool-card",
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


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def build_layout():
    return html.Div(
        [
            # ---- stores (client-side state, no server session needed) ----
            dcc.Store(id="active-tool-store", data=DEFAULT_TOOL_ID),
            dcc.Store(id="active-country-store", data=PIA_DEFAULT_COUNTRY),

            # ---- top nav ----
            html.Header(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src= app.get_asset_url("PIM-PAM_Logo_Dark.png"),
                                    alt="PIM-PAM logo",
                                    className="brand-logo",
                                ),
                                html.Div(APP_TITLE, className="brand-wordmark"),
                            ],
                            className="brand-lockup",
                        ),
                        html.Nav(
                            [
                                html.A("Overview", href="#overview", className="nav-link"),
                                html.A("Workbench", href="#workbench", className="nav-link"),
                                html.A("About", href="#about", className="nav-link"),
                            ],
                            className="top-nav-links",
                        ),
                    ],
                    className="top-nav-inner",
                ),
                className="top-nav",
            ),

            # ---- hero ----
            # html.Section(
            #     html.Div(
            #         [
            #             eyebrow("Digital Workspace Aggregator"),
            #             html.H1(
            #                 [
            #                     "Three tools. Five countries. ",
            #                     html.Span("One workspace.", className="accent"),
            #                 ],
            #                 className="hero-heading",
            #             ),
            #             html.P(APP_TAGLINE, className="hero-tagline"),
            #             html.P(MISSION_STATEMENT, className="hero-mission"),
            #         ],
            #         className="hero-inner",
            #         id="overview",
            #     ),
            #     className="hero-section",
            # ),

            # ---- tool overview strip ----
            html.Section(
                html.Div(
                    [
                        html.Div(
                            [
                                # eyebrow("Global Digital Demonstrations Support Tools"),
                                html.H2("Global Scalable Digital Demonstrations Support Tools", className="section-heading"),
                                html.P(
                                    "Suite of data-driven tools designed to improve public investment and asset management.",
                                    
                                    className="section-subheading",
                                ),
                            ],
                            className="section-heading-block",
                        ),
                        html.Div(
                            [hero_tool_card(t) for t in TOOLS],
                            className="tool-card-row",
                        ),
                    ],
                    className="section-inner",
                ),
                className="tools-section",
            ),

            # ---- workbench ----
            html.Section(
                html.Div(
                    [
                        html.Div(
                            [
                                eyebrow("The workbench"),
                                html.H2("Data Analytics and Visualization Platforms", className="section-heading"),
                            ],
                            className="section-heading-block",
                        ),
                        html.Div(id="workbench-tabs", className="workbench-tab-row"),
                        html.Div(id="workbench-panel", className="workbench-panel"),
                    ],
                    className="section-inner",
                ),
                className="workbench-section",
                id="workbench",
            ),

            # ---- about / mission footer ----
            html.Section(
                html.Div(
                    [
                        html.H2("Why one workspace?", className="section-heading"),
                        html.P(
                            [
                                "PIA, GoAT, and the Country Benchmarking Dashboard were each "
                                "designed to answer a different question: ",
                                html.Strong(
                                    "Where should new "
                                    "infrastructure investments be prioritized? What does the "
                                    "World Bank's operational portfolio reveal about a particular "
                                    "theme? How does a country compare with its peers? "
                                ),
                                "In practice, however, these questions are rarely asked in "
                                "isolation. They often arise in the same discussion, inform "
                                "the same analytical process, and are addressed by the same "
                                "teams. \n",
                                "This workspace brings these tools together in a single "
                                "environment, allowing users to move seamlessly from "
                                "infrastructure needs assessment to portfolio analysis "
                                "and country benchmarking without switching between "
                                "platforms."
                                
                            ],
                            className="about-text",
                        ),
                        # html.P(
                        #     "Tool embeds are served live from their original World Bank / "
                        #     "Posit Connect deployments \u2014 this workspace is a frame around "
                        #     "them, not a copy of them. If a browser blocks an embed for "
                        #     "security reasons, use the \u201cOpen full window\u201d link that "
                        #     "appears above it.",
                        #     className="about-note",
                        # ),
                    ],
                    className="section-inner about-inner",
                ),
                className="about-section",
                id="about",
            ),

            html.Footer(
                html.Div(
                    "© PIM-PAM Digital Workspace \u00b7 The World Bank", #\u00b7 Contact: ksingh12@worldbank.org
                    className="footer-inner",
                ),
                className="footer",
            ),
        ],
        className="app-shell",
    )


app.layout = build_layout


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("active-tool-store", "data"),
    Input({"type": "tool-select", "index": ALL}, "n_clicks"),
    State("active-tool-store", "data"),
    prevent_initial_call=True,
)
def set_active_tool(_n_clicks, current_tool_id):
    """Any 'tool-select' control (hero card or workbench tab) updates the
    same store, so both stay in sync regardless of which one was clicked.
    """
    triggered = ctx.triggered_id
    if not triggered or not any(_n_clicks):
        raise dash.exceptions.PreventUpdate
    new_tool_id = triggered["index"]
    if new_tool_id == current_tool_id:
        raise dash.exceptions.PreventUpdate
    return new_tool_id


@app.callback(
    Output("active-country-store", "data"),
    Input({"type": "country-select", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def set_active_country(_n_clicks):
    triggered = ctx.triggered_id
    if not triggered or not any(_n_clicks):
        raise dash.exceptions.PreventUpdate
    return triggered["index"]


@app.callback(
    Output("workbench-tabs", "children"),
    Input("active-tool-store", "data"),
)
def render_workbench_tabs(active_tool_id):
    return workbench_tabs(active_tool_id)


@app.callback(
    Output("workbench-panel", "children"),
    Input("active-tool-store", "data"),
    Input("active-country-store", "data"),
)
def render_workbench_panel(active_tool_id, active_country_id):
    return workbench_panel(active_tool_id, active_country_id, TOOLS_BY_ID)


# Smoothly scroll the workbench into view whenever the active tool changes
# via a hero card click (keeps the "pick a tool up top -> see it below" flow
# feeling like one continuous action rather than a page jump).
app.clientside_callback(
    """
    function(active_tool) {
        var el = document.getElementById('workbench');
        if (el) {
            el.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("workbench", "title"),
    Input("active-tool-store", "data"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run(debug=True)