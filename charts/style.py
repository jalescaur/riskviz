# charts/style.py — estilo, layout e cálculo de eixo compartilhados entre os gráficos

from dataclasses import dataclass, field
from config import (
    COLOR_BG_BODY, COLOR_TEXT, COLOR_H3, FONT_UI, RISK_PALETTE,
    RISK_THRESHOLDS, EVENT_PALETTE,
)
from i18n import t as _t

BG_PLOT = "#fafaf8"
GRID    = "#e8e3dc"
NEUTRAL = "#f5f5f0"


@dataclass
class Style:
    """Aparência e idioma compartilhados por todos os gráficos.

    Os defaults reproduzem exatamente o visual original da aplicação; a
    sidebar só sobrescreve o que o usuário mexer na personalização.
    """
    lang:         str   = "pt"
    palette:      dict  = field(default_factory=lambda: dict(RISK_PALETTE))
    thresholds:   list  = field(default_factory=lambda: list(RISK_THRESHOLDS))
    event_colors: list  = field(default_factory=lambda: list(EVENT_PALETTE))
    font_family:  str   = FONT_UI
    plot_bg:      str   = BG_PLOT
    neutral:      str   = NEUTRAL
    show_grid:    bool  = True
    height_scale: float = 1.0

    def t(self, key: str, **kw) -> str:
        return _t(key, self.lang, **kw)

    @property
    def grid(self) -> str:
        return GRID if self.show_grid else "rgba(0,0,0,0)"

    def h(self, px: float) -> int:
        """Altura em px já multiplicada pelo ajuste de altura global."""
        return int(round(px * self.height_scale))

    def event_color(self, i: int) -> str:
        return self.event_colors[i % len(self.event_colors)]

    def risk_name(self, label: str) -> str:
        return self.t(f"risk.{label}")

    def colorscale(self) -> list:
        """Gradiente de 5 pontos (vermelho → neutro → azul) a partir da paleta."""
        p = self.palette
        return [
            [0.00, p["critical"]],
            [0.35, p["high"]],
            [0.50, self.neutral],
            [0.65, p["low"]],
            [1.00, p["positive"]],
        ]


def hex_to_rgba(h: str, a: float) -> str:
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def base_layout(height: int, style: Style, scale: bool = True) -> dict:
    return dict(
        height=style.h(height) if scale else height,
        paper_bgcolor=COLOR_BG_BODY,
        plot_bgcolor=style.plot_bg,
        font=dict(family=style.font_family, size=15, color=COLOR_TEXT),
    )


def add_credit(fig, style: Style, opts: dict | None = None) -> None:
    """Marca d'água / crédito institucional.

    opts: show (bool), text (vazio = crédito padrão do idioma), size (px) e
    position ("top_left" | "top_right" | "bottom_left" | "bottom_right").
    Cresce a margem do lado escolhido em size+14 px para não cobrir nada; é
    anotação da figura, então também sai no PNG baixado. No topo, fica acima
    da caixa de legenda dos eventos: o scatter informa a altura dela em
    fig.layout.meta["credit_top_offset"].
    """
    o = {"show": True, "text": "", "size": 12, "position": "top_left", **(opts or {})}
    text = (o["text"] or "").strip() or style.t("credit")
    if not o["show"] or not text:
        return
    size, (vside, hside) = o["size"], o["position"].split("_")
    extra = size + 14
    side, default = ("t", 100) if vside == "top" else ("b", 80)
    current = getattr(fig.layout.margin, side)
    margin = (default if current is None else current) + extra
    fig.update_layout(margin={side: margin})
    if fig.layout.height:
        fig.update_layout(height=fig.layout.height + extra)
    if vside == "top":
        y, yanchor = 1, "bottom"
        yshift = (fig.layout.meta or {}).get("credit_top_offset", 4)
    else:
        y, yanchor, yshift = 0, "bottom", 4 - margin
    fig.add_annotation(
        xref="paper", yref="paper", y=y, yanchor=yanchor, yshift=yshift,
        x=0 if hside == "left" else 1, xanchor=hside, text=text, showarrow=False,
        font=dict(size=size, color=COLOR_H3, family=style.font_family),
    )


def axis(style: Style, title: str | None = None, size: int = 15, **kw) -> dict:
    """Eixo cartesiano com o estilo ativo (grade, fonte, título)."""
    d = dict(
        gridcolor=style.grid, showgrid=style.show_grid, zeroline=False,
        tickfont=dict(size=size, color=COLOR_H3, family=style.font_family),
    )
    if title is not None:
        d["title"] = dict(text=title, font=dict(size=size, color=COLOR_H3))
    d.update(kw)
    return d


def compute_axis_range(values, mode: str, fixed_range: tuple[float, float],
                        pad_frac: float = 0.12, min_span: float = 0.2) -> tuple[float, float]:
    """
    mode="fixed"   -> devolve fixed_range inalterado (comportamento padrão).
    mode="dynamic" -> devolve [min-pad, max+pad] a partir dos dados reais,
                       com piso min_span para não esticar demais um cluster
                       estreito de pontos.
    """
    if mode != "dynamic":
        return fixed_range
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return fixed_range
    vmin, vmax = min(vals), max(vals)
    span = vmax - vmin
    if span < min_span:
        center = (vmax + vmin) / 2
        vmin, vmax = center - min_span / 2, center + min_span / 2
        span = min_span
    pad = span * pad_frac
    return (vmin - pad, vmax + pad)
