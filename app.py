"""
app.py
------
PIM-PAM Digital Workspace \u2014 a single Dash app that aggregates three
World Bank PIM-PAM tools (PIA, GoAT, CBD) behind one workbench, so a user
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
)
from utils import (
    eyebrow,
    hero_tool_card,
    workbench_tabs,
    workbench_panel,
)

app = dash.Dash(__name__, title=APP_TITLE, update_title=None)
server = app.server


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
                        html.Div(APP_TITLE, className="brand-wordmark"),
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
                                eyebrow("The toolkit"),
                                html.H2("Pick a tool to open it below", className="section-heading"),
                                html.P(
                                    "Each card opens the tool directly in the workbench \u2014 "
                                    "no separate tab, no separate login.",
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
                                html.H2("Everything opens right here", className="section-heading"),
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
                            "PIA, GoAT, and the Country Benchmarking Dashboard were each "
                            "built to answer a different question \u2014 where should new "
                            "infrastructure go, what is the Bank's portfolio already saying "
                            "about a theme, and how does a country compare to its peers. "
                            "In practice those questions get asked together, in the same "
                            "meeting, by the same analyst. This workspace exists so that "
                            "the tools can be used together too.",
                            className="about-text",
                        ),
                        html.P(
                            "Tool embeds are served live from their original World Bank / "
                            "Posit Connect deployments \u2014 this workspace is a frame around "
                            "them, not a copy of them. If a browser blocks an embed for "
                            "security reasons, use the \u201cOpen full window\u201d link that "
                            "appears above it.",
                            className="about-note",
                        ),
                    ],
                    className="section-inner about-inner",
                ),
                className="about-section",
                id="about",
            ),

            html.Footer(
                html.Div(
                    "PIM-PAM Digital Workspace \u00b7 an internal aggregator for PIA, GoAT, "
                    "and the Country Benchmarking Dashboard.",
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