# charts/bubble_matrix.py — matriz evento × dimensão com bolhas
# (tamanho = |risk score|, cor = risk score)

import numpy as np
import plotly.graph_objects as go
from config import COLOR_H2, COLOR_H3
from charts.style import Style, base_layout, axis


def make_bubble_matrix(df, style: Style, agg: str = "mean", max_bubble: int = 46,
                       show_values: bool = True, value_font: int = 11) -> go.Figure:
    pivot = df.pivot_table(index="SHORT_EVENT", columns="DIM_LABEL",
                           values="RISK_SCORE", aggfunc=agg)
    xs, ys, zs = [], [], []
    for event in pivot.index:
        for dim in pivot.columns:
            v = pivot.loc[event, dim]
            if not np.isnan(v):
                xs.append(dim); ys.append(event); zs.append(float(v))

    sizes = [abs(z) for z in zs]
    sizeref = 2.0 * (max(sizes) if sizes else 1.0) / (max_bubble ** 2)

    fig = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers+text" if show_values else "markers",
        text=[f"{z:+.2f}" for z in zs],
        textposition="middle center",
        textfont=dict(size=value_font, color=COLOR_H2, family=style.font_family),
        marker=dict(
            size=sizes, sizemode="area", sizeref=sizeref or 1, sizemin=14,
            color=zs, colorscale=style.colorscale(), cmid=0, cmin=-1, cmax=1,
            line=dict(width=1.5, color="white"),
            colorbar=dict(title=dict(text=style.t("axis.RISK_SCORE"),
                                     font=dict(size=10, color=COLOR_H3)),
                          tickvals=[-1, -0.5, 0, 0.5, 1], len=0.8),
        ),
        hovertemplate=f"<b>%{{y}}</b><br>%{{x}}<br>{style.t('hover.risk_score')}: <b>%{{marker.color:+.3f}}</b><extra></extra>",
    ))
    fig.update_layout(
        **base_layout(max(300, len(pivot) * 90 + 120), style),
        margin=dict(l=0, r=20, t=16, b=16),
        xaxis=axis(style, None, 11, side="top", tickangle=-30, type="category",
                   categoryorder="array", categoryarray=pivot.columns.tolist()),
        yaxis=axis(style, None, 11, type="category", autorange="reversed",
                   categoryorder="array", categoryarray=pivot.index.tolist()),
    )
    return fig
