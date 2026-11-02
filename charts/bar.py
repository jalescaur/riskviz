# charts/bar.py — rankings horizontais: por evento e por dimensão

import plotly.graph_objects as go
from config import COLOR_H2, COLOR_H3
from charts.style import Style, base_layout, axis
from data import risk_color


def _order(frame, sort: str, label_col: str):
    if sort == "desc":
        return frame.sort_values("RISK_SCORE", ascending=False)
    if sort == "alpha":
        return frame.sort_values(label_col)
    return frame.sort_values("RISK_SCORE")


def _x_range(values, agg: str = "mean") -> list[float]:
    """Range fixo (-1.2..1.2) para médias/medianas/extremos; ajustado quando
    a soma pode passar de ±1."""
    peak = max((abs(v) for v in values), default=1.0)
    if agg == "sum" or peak > 1.0:
        return [-peak * 1.25, peak * 1.25]
    return [-1.2, 1.2]


def make_bar(df, style: Style, agg: str = "mean", sort: str = "asc",
             show_values: bool = True, value_font: int = 11,
             bar_gap: float = 0.15) -> go.Figure:
    """Ranking horizontal do risk score por evento (agregado por `agg`)."""
    frame = (
        df.groupby(["EVENT_LETTER", "SHORT_EVENT"])["RISK_SCORE"]
          .agg(agg)
          .reset_index()
    )
    agg_df = _order(frame, sort, "SHORT_EVENT")
    colors = [risk_color(s, style.thresholds, style.palette) for s in agg_df["RISK_SCORE"]]

    fig = go.Figure(go.Bar(
        x=agg_df["RISK_SCORE"],
        y=agg_df["SHORT_EVENT"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0), opacity=0.88),
        text=[f"{v:+.2f}" for v in agg_df["RISK_SCORE"]] if show_values else None,
        textposition="outside",
        textfont=dict(size=value_font, family=style.font_family, color=COLOR_H2),
        hovertemplate=f"<b>%{{y}}</b><br>{style.t('bar.hover_event')}: <b>%{{x:+.3f}}</b><extra></extra>",
    ))
    fig.add_vline(x=0, line_color=COLOR_H2, line_width=1.5)

    fig.update_layout(
        **base_layout(max(260, len(agg_df) * 64 + 80), style),
        margin=dict(l=0, r=80, t=16, b=16),
        bargap=bar_gap,
        xaxis=axis(style, style.t(f"bar.axis_{agg}"), 11,
                   range=_x_range(agg_df["RISK_SCORE"], agg)),
        yaxis=dict(title="", tickfont=dict(size=11, color=COLOR_H2, family=style.font_family),
                   categoryorder="array", categoryarray=agg_df["SHORT_EVENT"].tolist()),
    )
    return fig


def make_bar_dimensions(df, style: Style, sort: str = "asc", top_n: int = 0,
                        color_by: str = "risk", show_values: bool = True,
                        value_font: int = 11, bar_gap: float = 0.15) -> go.Figure:
    """Ranking de todas as dimensões, com o mesmo "número - dimensão" da
    legenda do scatter no eixo Y."""
    frame = _order(df, sort, "LEGEND_TEXT")
    if top_n and top_n > 0:
        # "top N" = os N de maior magnitude de risco, mantendo a ordenação pedida
        keep = df.assign(_abs=df["RISK_SCORE"].abs()).nlargest(top_n, "_abs").index
        frame = frame[frame.index.isin(keep)]
    events = sorted(df["EVENT_LETTER"].unique())
    if color_by == "risk":
        colors = frame["RISK_COLOR"].tolist()
    else:
        colors = [style.event_color(events.index(e)) for e in frame["EVENT_LETTER"]]

    # os mesmos nomes podem se repetir entre eventos: o número desambigua
    labels = frame["LEGEND_TEXT"].tolist()
    fig = go.Figure(go.Bar(
        x=frame["RISK_SCORE"],
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0), opacity=0.88),
        text=[f"{v:+.2f}" for v in frame["RISK_SCORE"]] if show_values else None,
        textposition="outside",
        textfont=dict(size=value_font, family=style.font_family, color=COLOR_H2),
        customdata=list(zip(frame["SHORT_EVENT"], frame["IMPACT"],
                            frame["PROB_DV_IV"], frame["TRUSTABILITY"])),
        hovertemplate=(
            "<b>%{y}</b><br><i>%{customdata[0]}</i><br>"
            f"{style.t('hover.risk_score')}: <b>%{{x:+.3f}}</b><br>"
            f"{style.t('axis.IMPACT')}: %{{customdata[1]:.2f}}<br>"
            f"{style.t('axis.PROB_DV_IV')}: %{{customdata[2]:.2f}}<br>"
            f"{style.t('axis.TRUSTABILITY')}: %{{customdata[3]:.2f}}<extra></extra>"
        ),
    ))
    fig.add_vline(x=0, line_color=COLOR_H2, line_width=1.5)
    fig.update_layout(
        **base_layout(max(260, len(frame) * 34 + 90), style),
        margin=dict(l=0, r=80, t=16, b=16),
        bargap=bar_gap,
        xaxis=axis(style, style.t("axis.RISK_SCORE"), 11, range=_x_range(frame["RISK_SCORE"])),
        yaxis=dict(title="", tickfont=dict(size=12, color=COLOR_H2, family=style.font_family),
                   categoryorder="array", categoryarray=labels),
    )
    return fig

