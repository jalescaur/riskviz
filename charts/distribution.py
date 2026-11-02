# charts/distribution.py — distribuição das métricas (box, violin, histograma)

import plotly.graph_objects as go
from config import RISK_ORDER, COLOR_H2, COLOR_H3
from charts.style import Style, base_layout, axis, hex_to_rgba


def _risk_bands(fig, style: Style):
    """Faixas coloridas de fundo, uma por categoria de risco, usando os
    limites de classificação ativos."""
    cuts = [c for c, _ in style.thresholds]
    bounds = [-1.0] + cuts + [1.0]
    for lo, hi, label in zip(bounds[:-1], bounds[1:], RISK_ORDER):
        fig.add_vrect(x0=lo, x1=hi, fillcolor=hex_to_rgba(style.palette[label], 0.10),
                      line_width=0, layer="below")


def make_distribution(df, style: Style, kind: str = "box", metric: str = "RISK_SCORE",
                      group_by_event: bool = True, show_points: bool = True,
                      bins: int = 10) -> go.Figure:
    events = sorted(df["EVENT_LETTER"].unique())
    metric_name = style.t(f"axis.{metric}")
    fig = go.Figure()

    groups = ([(e, df[df["EVENT_LETTER"] == e], style.event_color(i))
               for i, e in enumerate(events)]
              if group_by_event else [(style.t("dist.all"), df, style.event_color(0))])

    if kind == "histogram":
        for name, sub, color in groups:
            label = (f"{name} — {sub['SHORT_EVENT'].iloc[0]}" if group_by_event else name)
            fig.add_trace(go.Histogram(
                x=sub[metric], name=label, marker_color=color, opacity=0.85,
                nbinsx=bins,
                hovertemplate=f"{metric_name}: %{{x}}<br>{style.t('dist.count')}: %{{y}}<extra>{label}</extra>",
            ))
        fig.update_layout(barmode="stack", bargap=0.05,
                          xaxis=axis(style, metric_name, 13),
                          yaxis=axis(style, style.t("dist.count"), 13, dtick=1))
        if metric == "RISK_SCORE":
            _risk_bands(fig, style)
    else:
        Trace = go.Violin if kind == "violin" else go.Box
        for name, sub, color in groups:
            label = (f"{name} — {sub['SHORT_EVENT'].iloc[0]}" if group_by_event else name)
            # o Plotly chama a mesma opção de "points" (violin) e "boxpoints" (box)
            pts = "all" if show_points else False
            kw = dict(jitter=0.4, pointpos=0)
            if kind == "violin":
                kw.update(points=pts, box_visible=True, meanline_visible=True)
            else:
                kw.update(boxpoints=pts)
            fig.add_trace(Trace(
                y=sub[metric], name=f"<b>{name}</b>", marker_color=color,
                line_color=color, text=sub["LEGEND_TEXT"],
                hovertemplate=f"%{{text}}<br>{metric_name}: <b>%{{y:+.3f}}</b><extra>{label}</extra>",
                **kw,
            ))
        fig.update_layout(showlegend=False,
                          xaxis=axis(style, None, 13),
                          yaxis=axis(style, metric_name, 13))
        fig.add_hline(y=0, line_color=COLOR_H2, line_width=1, opacity=0.6)

    fig.update_layout(**base_layout(460, style),
                      margin=dict(l=10, r=20, t=30, b=20),
                      legend=dict(orientation="h", y=1.08, x=0,
                                  font=dict(size=13, family=style.font_family)))
    return fig
