# charts/scatter.py — scatter de bolhas (padrão: Impacto × Probabilidade)

from dataclasses import dataclass, field
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config import (
    AXIS_RANGES, SIGNED_COLUMNS, OVERLAP_COLOR,
    COLOR_H2, COLOR_H3, COLOR_TEXT,
)
from charts.style import Style, base_layout, axis, compute_axis_range
from charts.legend import layout_legend, add_bottom_legend, X_AXIS_SPACE

_ROTATE_POSITIONS = ["top center", "bottom center", "top right",
                     "bottom right", "top left", "bottom left"]

# posição do rótulo -> (direção x, direção y, âncora x, âncora y). A direção
# vale -1/0/+1; nas diagonais o vetor é normalizado, para o canto do texto
# ficar à mesma distância da borda da bolha em qualquer posição.
_LABEL_ANCHORS = {
    "top center":    (0,  1, "center", "bottom"),
    "top left":      (-1, 1, "right",  "bottom"),
    "top right":     (1,  1, "left",   "bottom"),
    "middle center": (0,  0, "center", "middle"),
    "middle left":   (-1, 0, "right",  "middle"),
    "middle right":  (1,  0, "left",   "middle"),
    "bottom center": (0, -1, "center", "top"),
    "bottom left":   (-1, -1, "right", "top"),
    "bottom right":  (1, -1, "left",   "top"),
}
_LABEL_GAP = 2  # px entre a borda da bolha e o texto


@dataclass
class ScatterOpts:
    """Opções do scatter. Os defaults reproduzem o gráfico original."""
    x_axis:       str   = "IMPACT"
    y_axis:       str   = "PROB_DV_IV"
    size_col:     str   = "RISK_SCORE"     # RISK_SCORE | TRUSTABILITY | PROB_DV_IV | IMPACT | none
    color_by:     str   = "risk"           # risk | event
    # rótulos junto às bolhas
    show_labels:  bool  = True
    label_mode:   str   = "number"         # number | number_name | name
    font_size:    int   = 17
    position_mode: str  = "rotate"         # rotate | fixed | individual
    fixed_position: str = "top center"
    individual_positions: dict = field(default_factory=dict)
    # eixos e textos
    axis_mode:    str   = "fixed"          # fixed | dynamic
    x_label:      str | None = None
    y_label:      str | None = None
    # bolhas
    opacity:      float = 0.85
    max_bubble:   int   = 55
    min_bubble:   int   = 17
    height:       int   = 600
    show_quadrants: bool = True
    show_midlines:  bool = True
    # legenda dos eventos (topo)
    event_legend_font: int = 17
    # legenda das dimensões (rodapé)
    show_legend:  bool  = True
    legend_cols:  int   = 0                # 0 = automático
    legend_font:  int   = 15
    legend_swatch: bool = True


def apply_overlap_jitter(df: pd.DataFrame, x_col: str, y_col: str) -> pd.DataFrame:
    """
    Detecta pontos com X/Y muito próximos (mesmo cluster visual) e aplica
    um pequeno deslocamento circular para separá-los, sem alterar os
    valores reais usados no hover/eixos.

    Tolerância: 1.5% do range de cada eixo — pontos dentro dessa
    distância em AMBOS os eixos são considerados sobrepostos.

    Retorna o df com colunas extras:
      _X_PLOT, _Y_PLOT   — coordenadas com jitter aplicado (para plotagem)
      _CLUSTER_SIZE      — quantos pontos compartilham o mesmo cluster
      _CLUSTER_ID        — id do cluster (-1 se o ponto está sozinho)
      _CX, _CY           — centro (valores reais) do cluster
    """
    df = df.copy()
    df["_X_PLOT"] = df[x_col].astype(float)
    df["_Y_PLOT"] = df[y_col].astype(float)
    df["_CLUSTER_SIZE"] = 1
    df["_CLUSTER_ID"] = -1
    df["_CX"] = df[x_col].astype(float)
    df["_CY"] = df[y_col].astype(float)
    if df.empty:
        return df

    x_range = df[x_col].max() - df[x_col].min() or 1.0
    y_range = df[y_col].max() - df[y_col].min() or 1.0
    tol_x = x_range * 0.015
    tol_y = y_range * 0.015

    # clustering simples: quantiza as coordenadas na grade de tolerância
    key = ((df[x_col] / tol_x).round().astype(int).astype(str) + "_"
           + (df[y_col] / tol_y).round().astype(int).astype(str))

    jitter_radius_x = x_range * 0.025
    jitter_radius_y = y_range * 0.025

    for cid, (_, group) in enumerate(df.groupby(key)):
        n = len(group)
        if n <= 1:
            continue
        cx, cy = group[x_col].mean(), group[y_col].mean()
        for j, idx in enumerate(group.index):
            angle = 2 * np.pi * j / n
            df.loc[idx, "_X_PLOT"] = df.loc[idx, x_col] + jitter_radius_x * np.cos(angle)
            df.loc[idx, "_Y_PLOT"] = df.loc[idx, y_col] + jitter_radius_y * np.sin(angle)
            df.loc[idx, "_CLUSTER_SIZE"] = n
            df.loc[idx, "_CLUSTER_ID"] = cid
            df.loc[idx, "_CX"] = cx
            df.loc[idx, "_CY"] = cy
    return df


def _label_text(sub: pd.DataFrame, mode: str) -> pd.Series:
    if mode == "name":
        return sub["DIM_LABEL"]
    if mode == "number_name":
        return sub["LEGEND_TEXT"]
    return sub["MARK_LABEL"]


def _text_positions(sub: pd.DataFrame, o: ScatterOpts) -> list[str]:
    if o.position_mode == "individual":
        return [o.individual_positions.get(dim_id, o.fixed_position)
                for dim_id in sub["ID_DIMENSION"]]
    if o.position_mode == "fixed":
        return [o.fixed_position] * len(sub)
    return [_ROTATE_POSITIONS[j % len(_ROTATE_POSITIONS)] for j in range(len(sub))]


def make_scatter(df: pd.DataFrame, style: Style, o: ScatterOpts | None = None) -> go.Figure:
    """
    Tamanho da bola = |coluna escolhida| (padrão: |RISK_SCORE|), em sizemode
    "area". Cor = RISK_COLOR (por risco, já calculada em data.preprocess com
    a paleta/thresholds ativos) ou a cor do evento.

    Junto de cada bolha aparece o número da dimensão (MARK_LABEL); a legenda
    no rodapé do gráfico lista "número - dimensão".

    Bolhas sobrepostas (mesmo X/Y dentro da tolerância) são afastadas por um
    pequeno jitter e destacadas em vermelho: borda vermelha + selo "+N".
    """
    o = o or ScatterOpts()
    x_col, y_col = o.x_axis, o.y_axis
    fig = go.Figure()
    df = apply_overlap_jitter(df, x_col, y_col)
    events = sorted(df["EVENT_LETTER"].unique())

    # sizeref: sizemode="area" — maior valor → max_bubble px de diâmetro
    sizes_all = (df[o.size_col].abs() if o.size_col != "none"
                 else pd.Series(1.0, index=df.index))
    max_size = sizes_all.max() if len(sizes_all) else 1.0
    sizeref  = 2.0 * (max_size or 1.0) / (o.max_bubble ** 2)

    def axis_name(col):
        return style.t(f"axis.{col}")

    hover = (
        "<b>%{customdata[0]} - %{customdata[1]}</b><br>"
        "<i>%{customdata[2]}</i><br>"
        f"{axis_name('RISK_SCORE')}: <b>%{{customdata[3]:+.3f}}</b><br>"
        f"{axis_name('IMPACT')}: %{{customdata[4]:.2f}}<br>"
        f"{axis_name('PROB_DV_IV')}: %{{customdata[5]:.2f}}<br>"
        f"{axis_name('TRUSTABILITY')}: %{{customdata[6]:.2f}}"
        "%{customdata[7]}"
        "<extra></extra>"
    )

    for i, evt in enumerate(events):
        sub = df[df["EVENT_LETTER"] == evt].copy().reset_index(drop=True)
        if sub.empty:
            continue
        evt_name = sub["SHORT_EVENT"].iloc[0]

        marker_sizes = (sub[o.size_col].abs() if o.size_col != "none"
                        else pd.Series(1.0, index=sub.index)).tolist()
        marker_colors = (sub["RISK_COLOR"].tolist() if o.color_by == "risk"
                         else [style.event_color(i)] * len(sub))

        cluster_suffix = [
            f"<br><i>📍 {style.t('scatter.overlap_hover', n=n)}</i>" if n > 1 else ""
            for n in sub["_CLUSTER_SIZE"]
        ]
        custom = list(zip(
            sub["MARK_LABEL"], sub["DIM_LABEL"], sub["SHORT_EVENT"],
            sub["RISK_SCORE"], sub["IMPACT"], sub["PROB_DV_IV"], sub["TRUSTABILITY"],
            cluster_suffix,
        ))

        fig.add_trace(go.Scatter(
            x=sub["_X_PLOT"],
            y=sub["_Y_PLOT"],
            mode="markers",
            name=f"<b>{evt_name}</b>",
            marker=dict(
                size=marker_sizes,
                sizemode="area",
                sizeref=sizeref,
                sizemin=o.min_bubble,
                color=marker_colors,
                opacity=o.opacity,
                line=dict(
                    width=[2.5 if n > 1 else 1.5 for n in sub["_CLUSTER_SIZE"]],
                    color=[OVERLAP_COLOR if n > 1 else "white" for n in sub["_CLUSTER_SIZE"]],
                ),
            ),
            customdata=custom,
            hovertemplate=hover,
        ))

        if o.show_labels:
            # rótulos como anotações: o Plotly afasta o texto diagonal do
            # marcador em √2 × raio, o que deixava "top right" longe da bolha.
            for px, py, text, pos, size in zip(sub["_X_PLOT"], sub["_Y_PLOT"],
                                               _label_text(sub, o.label_mode),
                                               _text_positions(sub, o), marker_sizes):
                diameter = (o.max_bubble * (size / max_size) ** 0.5) if max_size else o.min_bubble
                dist = max(diameter, o.min_bubble) / 2 + _LABEL_GAP
                ux, uy, xanc, yanc = _LABEL_ANCHORS[pos]
                norm = (ux * ux + uy * uy) ** 0.5 or 1.0
                fig.add_annotation(
                    x=px, y=py, text=str(text), showarrow=False,
                    xanchor=xanc, yanchor=yanc,
                    xshift=dist * ux / norm, yshift=dist * uy / norm,
                    font=dict(size=o.font_size, color=COLOR_H2, family=style.font_family),
                )

    # selo "+N" — um por cluster de bolhas sobrepostas (efeito vermelho)
    clusters = df[df["_CLUSTER_ID"] >= 0].drop_duplicates("_CLUSTER_ID")
    for _, row in clusters.iterrows():
        fig.add_annotation(
            x=row["_CX"], y=row["_CY"],
            text=f"+{row['_CLUSTER_SIZE']}",
            showarrow=False,
            font=dict(size=11, color="white", family=style.font_family),
            bgcolor=OVERLAP_COLOR,
            borderpad=3,
            xanchor="center", yanchor="middle",
            xshift=14, yshift=14,
        )

    x_range = compute_axis_range(df["_X_PLOT"], o.axis_mode, AXIS_RANGES[x_col])
    y_range = compute_axis_range(df["_Y_PLOT"], o.axis_mode, AXIS_RANGES[y_col])

    # linhas de referência: 0 nas escalas com sinal, 0.5 nas escalas 0..1
    if o.show_midlines:
        y_mid = 0.0 if y_col in SIGNED_COLUMNS else 0.5
        x_mid = 0.0 if x_col in SIGNED_COLUMNS else 0.5
        fig.add_hline(y=y_mid, line_dash="dot", line_color=style.grid if style.show_grid else COLOR_H3,
                      line_width=1)
        fig.add_vline(x=x_mid, line_dash="dot", line_color=COLOR_H3, line_width=1, opacity=0.5)

    # rótulos de quadrante — presos aos 4 cantos do gráfico em coordenadas
    # de domínio (0-1), não em coordenadas de dado, para nunca "flutuarem"
    # em cima das bolhas. Só fazem sentido nos eixos padrão (Impacto × Prob.).
    if o.show_quadrants and (x_col, y_col) == ("IMPACT", "PROB_DV_IV"):
        for dx, dy, xanc, yanc, key in [
            (0.01, 0.99, "left",  "top",    "scatter.q_high_neg"),
            (0.99, 0.99, "right", "top",    "scatter.q_high_pos"),
            (0.01, 0.01, "left",  "bottom", "scatter.q_low_neg"),
            (0.99, 0.01, "right", "bottom", "scatter.q_low_pos"),
        ]:
            fig.add_annotation(
                xref="x domain", yref="y domain",
                x=dx, y=dy, text=f"<b>{style.t(key)}</b>", showarrow=False,
                font=dict(size=14, color="#c0bdb5", family=style.font_family),
                xanchor=xanc, yanchor=yanc,
                bgcolor="rgba(250,250,248,0.75)",
            )

    # layout: altura = área do gráfico + margens (a legenda cresce a margem inferior)
    plot_h   = style.h(o.height)
    # legenda dos eventos no topo: caixa de 1 linha ≈ fonte×1,45 + 18 px; estima
    # quantas linhas ela ocupa para a margem (e o crédito acima dela) acompanharem
    ev_font = o.event_legend_font
    ev_names = [df.loc[df["EVENT_LETTER"] == e, "SHORT_EVENT"].iloc[0] for e in events]
    ev_width = sum(len(n) * ev_font * 0.62 + 45 for n in ev_names)
    ev_rows = max(1, math.ceil(ev_width / 780))
    legend_top = 0.02 * plot_h + ev_rows * (ev_font * 1.45 + 8) + 10
    top_m, bottom_m = max(80, round(legend_top) + 14), 20
    if o.show_legend and len(df):
        ordered = df.sort_values("SEQ_NUM")
        entries = [(r.MARK_LABEL, r.DIM_LABEL,
                    r.RISK_COLOR if o.color_by == "risk"
                    else style.event_color(events.index(r.EVENT_LETTER)))
                   for r in ordered.itertuples()]
        ncols, rows, legend_h = layout_legend(entries, o.legend_cols, o.legend_font,
                                              o.legend_swatch)
        add_bottom_legend(fig, entries, style, ncols, rows, o.legend_font,
                          show_swatch=o.legend_swatch)
        bottom_m += X_AXIS_SPACE + legend_h

    fig.update_layout(
        **base_layout(plot_h + top_m + bottom_m, style, scale=False),
        margin=dict(l=10, r=20, t=top_m, b=bottom_m),
        showlegend=True,
        meta=dict(credit_top_offset=round(legend_top) + 4),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0,
            font=dict(size=ev_font, family=style.font_family, color=COLOR_TEXT),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=style.grid, borderwidth=1,
            itemsizing="constant",
            tracegroupgap=4,
        ),
        xaxis=axis(style, o.x_label or axis_name(x_col), 17,
                   range=list(x_range), automargin=False),
        yaxis=axis(style, o.y_label or axis_name(y_col), 17,
                   range=list(y_range)),
    )
    return fig
