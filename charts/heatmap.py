# charts/heatmap.py — heatmap de risk score por evento × dimensão

import numpy as np
import plotly.graph_objects as go
from config import COLOR_H2, COLOR_H3
from charts.style import Style, base_layout


def make_heatmap(df, style: Style, agg: str = "mean", show_values: bool = True,
                 decimals: int = 2, value_font: int = 11, transpose: bool = False,
                 show_colorbar: bool = True) -> go.Figure:
    pivot = df.pivot_table(
        index="SHORT_EVENT", columns="DIM_LABEL",
        values="RISK_SCORE", aggfunc=agg,
    )
    if transpose:
        pivot = pivot.T

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=style.colorscale(),
        zmid=0, zmin=-1, zmax=1,
        text=[[f"{v:+.{decimals}f}" if not np.isnan(v) else "–" for v in row]
              for row in pivot.values],
        texttemplate="%{text}" if show_values else None,
        textfont=dict(size=value_font, family=style.font_family, color=COLOR_H2),
        hovertemplate=f"<b>%{{y}}</b><br>%{{x}}<br>{style.t('hover.risk_score')}: <b>%{{z:+.3f}}</b><extra></extra>",
        showscale=show_colorbar,
        colorbar=dict(
            title=dict(text=style.t("axis.RISK_SCORE"), font=dict(size=10, color=COLOR_H3)),
            tickvals=[-1, -0.5, 0, 0.5, 1],
            tickfont=dict(size=9, color=COLOR_H3),
            len=0.8,
        ),
        xgap=2, ygap=2,
    ))

    fig.update_layout(
        **base_layout(max(300, len(pivot) * 80 + 80), style),
        margin=dict(l=0, r=20, t=16, b=16),
        xaxis=dict(
            side="top", tickangle=-30,
            tickfont=dict(size=11, color=COLOR_H3, family=style.font_family),
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=11, color=COLOR_H3, family=style.font_family),
        ),
    )
    return fig
