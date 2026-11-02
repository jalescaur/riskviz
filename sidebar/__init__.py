# sidebar/__init__.py — orquestra a sidebar completa

import streamlit as st
import pandas as pd
from charts import Style, ScatterOpts
from data import preprocess, drop_invalid_rows
from i18n import LANGS, DEFAULT_LANG, t
from sidebar.data_source import render_data_source
from sidebar.customization import render_customization
from sidebar.filters import render_filters
from sidebar.label_positions import render_label_controls, render_scatter_options


def render_sidebar() -> tuple[pd.DataFrame | None, dict]:
    """
    Renderiza a sidebar completa e retorna:
      - df: DataFrame pré-processado e filtrado (ou None se sem dados)
      - controls: dict com idioma, estilo, textos, opções do scatter e
        exportação selecionados pelo usuário
    """
    with st.sidebar:
        st.markdown("### ⬡ Risk Visualizer")
        lang = st.selectbox(
            "🌐 Idioma / Language", list(LANGS), key="lang",
            index=list(LANGS).index(DEFAULT_LANG), format_func=LANGS.get,
        )
        st.markdown("---")

        df_raw = render_data_source(lang)
        custom = render_customization(lang)

        df = None
        if df_raw is not None:
            df_clean, dropped = drop_invalid_rows(df_raw)
            if dropped:
                st.warning(t("data.dropped", lang, n=dropped))
            if df_clean.empty:
                st.error(t("data.empty", lang))
            else:
                df = preprocess(df_clean, custom["thresholds"], custom["palette"], custom["num_mode"])
                df = render_filters(df, lang)

        st.markdown("---")
        color_by = st.radio(
            t("sidebar.color_by", lang), ["risk", "event"], horizontal=True,
            format_func=lambda v: t(f"colorby.{v}", lang), key="color_by",
        )

        label_controls = render_label_controls(df, lang)
        scatter_options = render_scatter_options(lang)

    style = Style(
        lang=lang,
        palette=custom["palette"],
        thresholds=custom["thresholds"],
        event_colors=custom["event_colors"],
        font_family=custom["font_family"],
        plot_bg=custom["plot_bg"],
        neutral=custom["neutral"],
        show_grid=custom["show_grid"],
        height_scale=custom["height_scale"],
    )
    texts = custom["texts"]
    x_axis, y_axis = scatter_options["x_axis"], scatter_options["y_axis"]
    scatter = ScatterOpts(
        **scatter_options, **label_controls,
        color_by=color_by,
        axis_mode=custom["axis_mode"],
        # os títulos de eixo personalizados valem só para os eixos padrão
        x_label=texts["x_label"] if x_axis == "IMPACT" else None,
        y_label=texts["y_label"] if y_axis == "PROB_DV_IV" else None,
    )
    controls = {
        "lang":     lang,
        "style":    style,
        "texts":    texts,
        "scatter":  scatter,
        "color_by": color_by,
        "export":   custom["export"],
        "credit":   custom["credit"],
    }
    return df, controls
