# charts/legend.py — legenda de dimensões no rodapé do gráfico ("1 - Ormuz")
#
# A legenda é desenhada como anotações dentro da própria figura (e não como
# um elemento da página), assim ela também sai no PNG baixado pelo botão de
# câmera do Plotly. Preenche as colunas de cima para baixo, da esquerda para
# a direita. Nomes longos quebram em várias linhas (com recuo), nunca são cortados.

import html
import math
import textwrap
from charts.style import Style
from config import COLOR_H2

# espaço (px) abaixo do eixo X reservado a ticks + título do eixo
X_AXIS_SPACE = 72


def _column_lines(col: list[tuple[str, str, str]], max_chars: int,
                  show_swatch: bool) -> list[str]:
    """Linhas HTML de uma coluna; as de continuação ficam recuadas sob o nome."""
    lines = []
    for num, name, color in col:
        swatch = f'<span style="color:{color}">●</span> ' if show_swatch else ""
        prefix_chars = len(str(num)) + 3 + (2 if show_swatch else 0)
        wrapped = textwrap.wrap(str(name), max(8, max_chars - prefix_chars)) or [""]
        lines.append(f"{swatch}<b>{html.escape(str(num), quote=False)}</b> - "
                     f"{html.escape(wrapped[0], quote=False)}")
        # recuo em espaços fixos: largura do prefixo (~0,28 em cada) ≈ 2 por dígito + 3
        indent = " " * (2 * len(str(num)) + (6 if show_swatch else 3))
        lines += [indent + html.escape(w, quote=False) for w in wrapped[1:]]
    return lines


def _split(entries, ncols: int, font_size: int, show_swatch: bool, usable_px: int):
    """(colunas, linhas por coluna de entradas, linhas HTML de cada coluna)."""
    n = len(entries)
    rows = math.ceil(n / ncols)
    max_chars = max(12, int(usable_px / ncols / (font_size * 0.55)) - 2)
    columns = [entries[c * rows:(c + 1) * rows] for c in range(ncols)]
    return rows, [_column_lines(col, max_chars, show_swatch) for col in columns]


def layout_legend(entries: list[tuple[str, str, str]], ncols: int = 0, font_size: int = 15,
                  show_swatch: bool = True, usable_px: int = 780) -> tuple[int, int, int]:
    """Retorna (colunas, linhas, altura_em_px) da legenda, já contando as
    quebras de linha dos nomes longos.
    ncols=0 escolhe o número de colunas conforme a quantidade de entradas."""
    n = len(entries)
    if n <= 0:
        return 1, 0, 0
    if ncols <= 0:
        ncols = 1 if n <= 6 else 2 if n <= 14 else 3 if n <= 30 else 4
    ncols = max(1, min(ncols, n))
    rows, col_lines = _split(entries, ncols, font_size, show_swatch, usable_px)
    line_px = round(font_size * 1.45)
    return ncols, rows, max(len(lines) for lines in col_lines) * line_px + 14


def add_bottom_legend(fig, entries: list[tuple[str, str, str]], style: Style,
                      ncols: int, rows: int, font_size: int = 15,
                      show_swatch: bool = True, y_offset: int = X_AXIS_SPACE,
                      usable_px: int = 780) -> None:
    """Adiciona a legenda abaixo da área do gráfico.

    entries: lista de (número, nome, cor_da_amostra).
    y_offset: distância (px) abaixo da base do gráfico onde a legenda começa.
    usable_px: largura aproximada disponível, usada para quebrar nomes longos
    (os mesmos valores devem ser passados a layout_legend).
    """
    _, col_lines = _split(entries, ncols, font_size, show_swatch, usable_px)
    for c, lines in enumerate(col_lines):
        if not lines:
            continue
        fig.add_annotation(
            xref="paper", yref="paper", x=c / ncols, y=0,
            xanchor="left", yanchor="top", yshift=-y_offset,
            text="<br>".join(lines), showarrow=False, align="left",
            font=dict(size=font_size, color=COLOR_H2, family=style.font_family),
        )
