# charts/composition.py — composição das classificações de risco
# (barras empilhadas por evento e rosca geral)

import plotly.graph_objects as go
from config import RISK_ORDER, COLOR_H2, COLOR_H3
from charts.style import Style, base_layout, axis


def _counts(df):
    """Contagem de dimensões por (evento, categoria de risco)."""
    return (df.groupby(["SHORT_EVENT", "RISK_LABEL"]).size()
              .unstack(fill_value=0)
              .reindex(columns=RISK_ORDER, fill_value=0))


def make_stacked(df, style: Style, percent: bool = False, show_values: bool = True) -> go.Figure:
    counts = _counts(df)
    events = sorted(df["SHORT_EVENT"].unique())
    counts = counts.reindex(events)
    fig = go.Figure()
    for label in RISK_ORDER:
        vals = counts[label]
        fig.add_trace(go.Bar(
            y=counts.index, x=vals, orientation="h",
            name=style.risk_name(label), marker_color=style.palette[label],
            text=[str(v) if v else "" for v in vals] if show_values else None,
            textposition="inside", insidetextanchor="middle",
            textfont=dict(color="white", size=13, family=style.font_family),
            hovertemplate=f"<b>%{{y}}</b><br>{style.risk_name(label)}: %{{x}}<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", barnorm="percent" if percent else None,
        **base_layout(max(260, len(counts) * 64 + 120), style),
        margin=dict(l=0, r=20, t=40, b=20),
        xaxis=axis(style, style.t("comp.pct") if percent else style.t("comp.count"), 12,
                   ticksuffix="%" if percent else ""),
        yaxis=dict(title="", autorange="reversed",
                   tickfont=dict(size=11, color=COLOR_H2, family=style.font_family)),
        legend=dict(orientation="h", y=1.12, x=0, traceorder="normal",
                    font=dict(size=13, family=style.font_family)),
    )
    return fig


def make_donut(df, style: Style, show_values: bool = True) -> go.Figure:
    counts = df["RISK_LABEL"].value_counts().reindex(RISK_ORDER, fill_value=0)
    counts = counts[counts > 0]
    fig = go.Figure(go.Pie(
        labels=[style.risk_name(l) for l in counts.index], values=counts.values,
        hole=0.55, sort=False, direction="clockwise",
        marker=dict(colors=[style.palette[l] for l in counts.index],
                    line=dict(color="white", width=2)),
        textinfo="label+value+percent" if show_values else "none",
        textfont=dict(size=13, family=style.font_family),
        hovertemplate="<b>%{label}</b><br>%{value} (%{percent})<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>{len(df)}</b><br>{style.t('comp.dimensions')}", showarrow=False,
        font=dict(size=18, color=COLOR_H2, family=style.font_family),
    )
    fig.update_layout(height=style.h(440), margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor="white", showlegend=True,
                      legend=dict(font=dict(size=13, family=style.font_family)))
    return fig
