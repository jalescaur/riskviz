# charts/factors.py — visão dos fatores do risco: coordenadas paralelas,
# scatter 3D (Impacto × Probabilidade × Confiabilidade) e matriz de dispersão

import plotly.graph_objects as go
from config import AXIS_RANGES, METRIC_COLUMNS, COLOR_H2, COLOR_H3
from charts.style import Style, base_layout

_RANGES = {"IMPACT": [-1, 1], "PROB_DV_IV": [0, 1], "TRUSTABILITY": [0, 1], "RISK_SCORE": [-1, 1]}


def _colors(df, style: Style, color_by: str) -> list[str]:
    if color_by == "risk":
        return df["RISK_COLOR"].tolist()
    events = sorted(df["EVENT_LETTER"].unique())
    return [style.event_color(events.index(e)) for e in df["EVENT_LETTER"]]


def make_parallel(df, style: Style, height: int = 480) -> go.Figure:
    """Cada dimensão do risco vira uma linha que atravessa os 4 fatores;
    a cor da linha é o risk score."""
    fig = go.Figure(go.Parcoords(
        line=dict(color=df["RISK_SCORE"], colorscale=style.colorscale(),
                  cmin=-1, cmax=1, showscale=True,
                  colorbar=dict(title=dict(text=style.t("axis.RISK_SCORE")),
                                tickvals=[-1, -0.5, 0, 0.5, 1], len=0.8)),
        dimensions=[
            dict(label=style.t(f"axis.{c}"), values=df[c], range=_RANGES[c])
            for c in ["IMPACT", "PROB_DV_IV", "TRUSTABILITY", "RISK_SCORE"]
        ],
        labelfont=dict(size=14, color=COLOR_H2),
        tickfont=dict(size=11, color=COLOR_H3),
    ))
    fig.update_layout(height=style.h(height), margin=dict(l=60, r=60, t=60, b=30),
                      paper_bgcolor="white",
                      font=dict(family=style.font_family, color=COLOR_H2))
    return fig


def make_scatter3d(df, style: Style, color_by: str = "risk", show_labels: bool = True,
                   max_marker: int = 28, height: int = 620) -> go.Figure:
    events = sorted(df["EVENT_LETTER"].unique())
    max_abs = df["RISK_SCORE"].abs().max() or 1.0
    fig = go.Figure()
    for i, evt in enumerate(events):
        sub = df[df["EVENT_LETTER"] == evt]
        colors = (sub["RISK_COLOR"].tolist() if color_by == "risk"
                  else [style.event_color(i)] * len(sub))
        fig.add_trace(go.Scatter3d(
            x=sub["IMPACT"], y=sub["PROB_DV_IV"], z=sub["TRUSTABILITY"],
            mode="markers+text" if show_labels else "markers",
            name=f"{evt} — {sub['SHORT_EVENT'].iloc[0]}",
            text=sub["MARK_LABEL"], textposition="top center",
            textfont=dict(size=13, color=COLOR_H2),
            marker=dict(size=[6 + max_marker * abs(s) / max_abs for s in sub["RISK_SCORE"]],
                        color=colors, opacity=0.88, line=dict(width=1, color="white")),
            customdata=list(zip(sub["LEGEND_TEXT"], sub["RISK_SCORE"])),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                f"{style.t('hover.risk_score')}: <b>%{{customdata[1]:+.3f}}</b><br>"
                f"{style.t('axis.IMPACT')}: %{{x:.2f}}<br>"
                f"{style.t('axis.PROB_DV_IV')}: %{{y:.2f}}<br>"
                f"{style.t('axis.TRUSTABILITY')}: %{{z:.2f}}<extra></extra>"
            ),
        ))
    ax = lambda col: dict(title=style.t(f"axis.{col}"), range=_RANGES[col],
                          gridcolor=style.grid, backgroundcolor=style.plot_bg)
    fig.update_layout(
        height=style.h(height), margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor="white",
        scene=dict(xaxis=ax("IMPACT"), yaxis=ax("PROB_DV_IV"), zaxis=ax("TRUSTABILITY")),
        legend=dict(orientation="h", y=1.04, x=0, font=dict(size=13)),
        font=dict(family=style.font_family, color=COLOR_H2),
    )
    return fig


def make_splom(df, style: Style, color_by: str = "risk", height: int = 640) -> go.Figure:
    fig = go.Figure(go.Splom(
        dimensions=[dict(label=style.t(f"axis.{c}"), values=df[c]) for c in METRIC_COLUMNS],
        text=df["LEGEND_TEXT"],
        marker=dict(color=_colors(df, style, color_by), size=10, opacity=0.85,
                    line=dict(width=1, color="white")),
        diagonal_visible=False, showupperhalf=False,
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(
        **base_layout(height, style), margin=dict(l=10, r=10, t=20, b=10),
        dragmode="select",
    )
    grid = dict(gridcolor=style.grid, showgrid=style.show_grid)
    fig.update_layout(**{f"{a}axis{'' if i == 1 else i}": grid
                         for i in range(1, len(METRIC_COLUMNS) + 1) for a in "xy"})
    return fig
