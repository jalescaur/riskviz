# sidebar/label_positions.py — controles do scatter: rótulos (rodízio / fixo /
# individual por bolha), bolhas, eixos e legenda das dimensões
#
# Isolado num módulo próprio porque o loop de widgets por bolha abaixo já
# derrubou a app inteira uma vez por colisão de `key` do Streamlit — manter
# esse ponto frágil separado limita o raio de impacto de bugs futuros aqui.

import streamlit as st
import pandas as pd
from i18n import t

_POSITION_OPTS = [
    "top center", "top left", "top right",
    "middle center", "middle left", "middle right",
    "bottom center", "bottom left", "bottom right",
]
_AXIS_OPTS = ["IMPACT", "PROB_DV_IV", "TRUSTABILITY", "RISK_SCORE"]
_SIZE_OPTS = ["RISK_SCORE", "TRUSTABILITY", "PROB_DV_IV", "IMPACT", "none"]


def _pos_name(lang):
    return lambda p: t("pos." + p.replace(" ", "_"), lang)


def render_label_controls(df: pd.DataFrame | None, lang: str) -> dict:
    """Retorna show_labels, label_mode, font_size, position_mode,
    fixed_position, individual_positions."""
    st.markdown("---")
    st.markdown(f"**{t('scatter.labels_header', lang)}**")

    show_labels = st.toggle(
        t("scatter.show_labels", lang), value=True, key="lb_show",
        help=t("scatter.show_labels_help", lang),
    )
    label_mode = st.radio(
        t("scatter.label_content", lang), ["number", "number_name", "name"],
        format_func=lambda v: t(f"labelmode.{v}", lang),
        disabled=not show_labels, help=t("scatter.label_content_help", lang), key="lb_mode",
    )
    font_size = st.slider(
        t("scatter.font_size", lang), min_value=9, max_value=30, value=17, step=1,
        disabled=not show_labels, key="lb_font",
    )
    position_mode = st.radio(
        t("scatter.positioning", lang), ["rotate", "fixed", "individual"],
        format_func=lambda v: t(f"posmode.{v}", lang),
        disabled=not show_labels, help=t("scatter.positioning_help", lang), key="lb_posmode",
    )
    fixed_position = st.selectbox(
        t("scatter.label_position", lang), _POSITION_OPTS, index=0,
        format_func=_pos_name(lang),
        disabled=not show_labels or position_mode != "fixed", key="lb_fixed",
    )

    # ── posição individual por bolha ──────────────────────────────────────
    individual_positions = {}
    if show_labels and position_mode == "individual" and df is not None and not df.empty:
        with st.expander(t("scatter.each_bubble", lang, n=len(df)), expanded=True):
            for idx, row in df.sort_values("SEQ_NUM").reset_index(drop=True).iterrows():
                dim_id = row["ID_DIMENSION"]
                label  = f"{row['EVENT_LETTER']} · {row['LEGEND_TEXT']}"
                # key inclui o índice da linha (não só dim_id) para não
                # colidir quando ID_DIMENSION se repete entre linhas —
                # uma colisão de key derruba o app inteiro (inclusive a
                # legenda de eventos) com StreamlitDuplicateElementKey.
                individual_positions[dim_id] = st.selectbox(
                    label, _POSITION_OPTS, index=0, key=f"pos_{idx}_{dim_id}",
                    format_func=_pos_name(lang),
                )

    return {
        "show_labels":           show_labels,
        "label_mode":            label_mode,
        "font_size":             font_size,
        "position_mode":         position_mode,
        "fixed_position":        fixed_position,
        "individual_positions":  individual_positions,
    }


def render_scatter_options(lang: str) -> dict:
    """Eixos, tamanho/opacidade das bolhas, quadrantes e legenda do scatter."""
    with st.expander(f"⚙️ {t('scatter.options_header', lang)}", expanded=False):
        st.caption(t("scatter.axes", lang))
        c1, c2 = st.columns(2)
        x_axis = c1.selectbox(t("scatter.x_axis", lang), _AXIS_OPTS, index=0,
                              format_func=lambda c: t(f"axis.{c}", lang), key="sc_x")
        y_axis = c2.selectbox(t("scatter.y_axis", lang), _AXIS_OPTS, index=1,
                              format_func=lambda c: t(f"axis.{c}", lang), key="sc_y")

        st.caption(t("scatter.bubbles", lang))
        size_col = st.selectbox(
            t("scatter.size_by", lang), _SIZE_OPTS, index=0,
            format_func=lambda c: t("scatter.size_none", lang) if c == "none"
                                  else f"|{t(f'axis.{c}', lang)}|",
            key="sc_size",
        )
        opacity = st.slider(t("scatter.opacity", lang), 0.2, 1.0, 0.85, 0.05, key="sc_opacity")
        max_bubble = st.slider(t("scatter.max_bubble", lang), 25, 110, 55, 1, key="sc_maxb")
        min_bubble = st.slider(t("scatter.min_bubble", lang), 6, 40, 17, 1, key="sc_minb")
        height = st.slider(t("scatter.height", lang), 350, 1100, 600, 10, key="sc_height")
        show_quadrants = st.toggle(t("scatter.quadrants", lang), value=True, key="sc_quad")
        show_midlines = st.toggle(t("scatter.midlines", lang), value=True, key="sc_mid")

        event_legend_font = st.slider(t("scatter.event_legend_font", lang), 9, 30, 17, 1,
                                      key="sc_evlegfont")

        st.caption(t("scatter.legend", lang))
        show_legend = st.toggle(t("scatter.show_legend", lang), value=True, key="sc_leg",
                                help=t("scatter.show_legend_help", lang))
        legend_cols = st.select_slider(
            t("scatter.legend_cols", lang), options=[0, 1, 2, 3, 4], value=0,
            format_func=lambda v: t("scatter.auto", lang) if v == 0 else str(v),
            disabled=not show_legend, key="sc_legcols",
        )
        legend_font = st.slider(t("scatter.legend_font", lang), 9, 26, 15, 1,
                                disabled=not show_legend, key="sc_legfont")
        legend_swatch = st.toggle(t("scatter.legend_swatch", lang), value=True,
                                  disabled=not show_legend, key="sc_legsw")

    return {
        "x_axis": x_axis, "y_axis": y_axis, "size_col": size_col,
        "opacity": opacity, "max_bubble": max_bubble, "min_bubble": min_bubble,
        "height": height, "show_quadrants": show_quadrants, "show_midlines": show_midlines,
        "show_legend": show_legend, "legend_cols": legend_cols,
        "legend_font": legend_font, "legend_swatch": legend_swatch,
        "event_legend_font": event_legend_font,
    }
