# charts/hierarchy.py — treemap e sunburst (evento → dimensão)

import plotly.graph_objects as go
from config import COLOR_H2, COLOR_H3
from charts.style import Style


def _nodes(df, size_mode: str):
    """Monta ids/parents/labels/valores/scores para os dois níveis
    (eventos e suas dimensões). O tamanho de cada evento é a soma dos filhos
    (branchvalues="total")."""
    ids, parents, labels, values, scores, hovers = [], [], [], [], [], []
    for evt in sorted(df["EVENT_LETTER"].unique()):
        sub = df[df["EVENT_LETTER"] == evt]
        child_vals = [max(abs(s), 0.02) if size_mode == "abs" else 1.0
                      for s in sub["RISK_SCORE"]]
        ids.append(f"evt:{evt}")
        parents.append("")
        labels.append(f"{evt} — {sub['SHORT_EVENT'].iloc[0]}")
        values.append(sum(child_vals))
        scores.append(float(sub["RISK_SCORE"].mean()))
        hovers.append(len(sub))
        for (_, r), v in zip(sub.iterrows(), child_vals):
            ids.append(f"dim:{r.name}")
            parents.append(f"evt:{evt}")
            labels.append(r["LEGEND_TEXT"])
            values.append(v)
            scores.append(float(r["RISK_SCORE"]))
            hovers.append(1)
    return ids, parents, labels, values, scores, hovers


def make_hierarchy(df, style: Style, kind: str = "treemap", size_mode: str = "abs",
                   font_size: int = 14, height: int = 560) -> go.Figure:
    ids, parents, labels, values, scores, counts = _nodes(df, size_mode)
    common = dict(
        ids=ids, parents=parents, labels=labels, values=values,
        branchvalues="total",
        customdata=list(zip(scores, counts)),
        marker=dict(
            colors=scores, colorscale=style.colorscale(), cmid=0, cmin=-1, cmax=1,
            colorbar=dict(title=dict(text=style.t("axis.RISK_SCORE"),
                                     font=dict(size=10, color=COLOR_H3)),
                          tickvals=[-1, -0.5, 0, 0.5, 1], len=0.8),
        ),
        texttemplate="%{label}<br>%{customdata[0]:+.2f}",
        hovertemplate=f"<b>%{{label}}</b><br>{style.t('hover.risk_score')}: <b>%{{customdata[0]:+.3f}}</b><extra></extra>",
        textfont=dict(size=font_size, family=style.font_family),
    )
    if kind == "sunburst":
        trace = go.Sunburst(**common)
    else:
        common["marker"]["line"] = dict(width=2, color="white")
        trace = go.Treemap(**common, tiling=dict(pad=3))
    fig = go.Figure(trace)
    fig.update_layout(
        height=style.h(height),
        margin=dict(l=0, r=0, t=16, b=0),
        paper_bgcolor="white",
        font=dict(family=style.font_family, size=13, color=COLOR_H2),
    )
    return fig
