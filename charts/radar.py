# charts/radar.py — radar de risco por evento (único ou comparativo)

import plotly.graph_objects as go
from config import COLOR_TEXT, COLOR_H2, COLOR_H3, COLOR_BG_BODY
from charts.style import Style, hex_to_rgba
from charts.legend import layout_legend, add_bottom_legend
from data import risk_color


def _radial_range(values, mode: str) -> list[float]:
    if mode == "auto" and len(values):
        lo, hi = min(min(values), 0), max(max(values), 0)
        pad = (hi - lo) * 0.1 or 0.1
        return [lo - pad, hi + pad]
    return [-1, 1]


def _polar(style: Style, rng, use_numbers: bool = False) -> dict:
    return dict(
        bgcolor=style.plot_bg,
        radialaxis=dict(
            visible=True, range=rng,
            tickfont=dict(size=9, color=COLOR_H3),
            gridcolor=style.grid, showgrid=style.show_grid,
            tickvals=[-1, -0.5, 0, 0.5, 1] if rng == [-1, 1] else None,
        ),
        angularaxis=dict(
            tickfont=dict(size=13 if use_numbers else 10, color=COLOR_H2, family=style.font_family),
            gridcolor=style.grid, showgrid=style.show_grid,
        ),
    )


def make_radar(df, event_letter: str, style: Style, range_mode: str = "fixed",
               fill_opacity: float = 0.15, show_markers: bool = True,
               use_numbers: bool = False, legend_font: int = 14) -> go.Figure | None:
    """Radar das dimensões de um evento. use_numbers troca os nomes dos
    eixos pelo número da dimensão e desenha a legenda "número - nome" abaixo."""
    sub = df[df["EVENT_LETTER"] == event_letter].copy()
    if sub.empty:
        return None

    col = "MARK_LABEL" if use_numbers else "DIM_LABEL"
    categories = sub[col].tolist() + [sub[col].iloc[0]]
    scores     = sub["RISK_SCORE"].tolist() + [sub["RISK_SCORE"].iloc[0]]

    line_color = risk_color(sub["RISK_SCORE"].mean(), style.thresholds, style.palette)
    rng = _radial_range(scores, range_mode)

    fig = go.Figure(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill="toself",
        fillcolor=hex_to_rgba(line_color, fill_opacity),
        line=dict(color=line_color, width=2),
        mode="lines+markers" if show_markers else "lines",
        marker=dict(size=7, color=line_color),
        customdata=sub["LEGEND_TEXT"].tolist() + [sub["LEGEND_TEXT"].iloc[0]],
        hovertemplate=f"<b>%{{customdata}}</b><br>{style.t('hover.risk_score')}: <b>%{{r:+.3f}}</b><extra></extra>",
    ))

    height, bottom = style.h(400), 40
    if use_numbers:
        entries = [(r.MARK_LABEL, r.DIM_LABEL, r.RISK_COLOR)
                   for r in sub.sort_values("SEQ_NUM").itertuples()]
        ncols, rows, legend_h = layout_legend(entries, 0, legend_font)
        add_bottom_legend(fig, entries, style, ncols, rows, legend_font, y_offset=24)
        bottom += 24 + legend_h
        height += 24 + legend_h

    fig.update_layout(
        height=height,
        margin=dict(l=60, r=60, t=40, b=bottom),
        paper_bgcolor=COLOR_BG_BODY,
        polar=_polar(style, rng, use_numbers),
        font=dict(family=style.font_family, size=11, color=COLOR_TEXT),
        showlegend=False,
    )
    return fig


def make_radar_compare(df, events: list[str], style: Style, range_mode: str = "fixed",
                       fill_opacity: float = 0.12, show_markers: bool = True) -> go.Figure | None:
    """Sobrepõe o radar de vários eventos (um traço por evento). Os eixos são
    as dimensões (por nome) presentes em pelo menos um dos eventos."""
    sub = df[df["EVENT_LETTER"].isin(events)]
    if sub.empty:
        return None
    all_events = sorted(df["EVENT_LETTER"].unique())
    dims = list(dict.fromkeys(sub.sort_values("SEQ_NUM")["DIM_LABEL"]))

    fig = go.Figure()
    all_scores = []
    for evt in events:
        e = sub[sub["EVENT_LETTER"] == evt]
        if e.empty:
            continue
        by_dim = e.groupby("DIM_LABEL")["RISK_SCORE"].mean()
        scores = [by_dim.get(d) for d in dims]
        all_scores += [s for s in scores if s is not None]
        color = style.event_color(all_events.index(evt))
        # fecha o polígono; dimensões ausentes no evento ficam como lacuna
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]], theta=dims + [dims[0]],
            name=f"{evt} — {e['SHORT_EVENT'].iloc[0]}",
            fill="toself", fillcolor=hex_to_rgba(color, fill_opacity),
            line=dict(color=color, width=2),
            mode="lines+markers" if show_markers else "lines",
            marker=dict(size=7, color=color),
            connectgaps=True,
            hovertemplate=f"<b>%{{theta}}</b><br>{style.t('hover.risk_score')}: <b>%{{r:+.3f}}</b><extra></extra>",
        ))

    fig.update_layout(
        height=style.h(480),
        margin=dict(l=60, r=60, t=40, b=70),
        paper_bgcolor=COLOR_BG_BODY,
        polar=_polar(style, _radial_range(all_scores, range_mode)),
        font=dict(family=style.font_family, size=11, color=COLOR_TEXT),
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="left", x=0,
                    font=dict(size=13, family=style.font_family)),
    )
    return fig
