# sidebar/customization.py — paleta, thresholds, textos, aparência e exportação
#
# Tudo fica dentro de um expander fechado por padrão, e todo default aqui
# reproduz exatamente o texto/cor/eixo que a app já usava — ou seja, nada
# muda visualmente a menos que o usuário abra e edite algo.

import streamlit as st
from config import (
    RISK_PALETTE, RISK_THRESHOLDS, RISK_ORDER, EVENT_PALETTE, FONT_CHOICES,
)
from charts.style import BG_PLOT, NEUTRAL
from data import NUM_MODES
from i18n import t

# chaves dos textos editáveis (padrão em i18n: "default.<chave>")
TEXT_KEYS = [
    "page_title", "page_subtitle", "scatter_title", "heatmap_title",
    "bar_title", "dims_title", "radar_title", "hierarchy_title",
    "dist_title", "matrix_title", "factors_title", "comp_title",
    "x_label", "y_label",
]


CREDIT_POSITIONS = ["top_left", "top_right", "bottom_left", "bottom_right"]


def default_texts(lang: str) -> dict:
    return {k: t(f"default.{k}", lang) for k in TEXT_KEYS}


def render_customization(lang: str) -> dict:
    """
    Renderiza o expander "🎨 Personalização" e retorna:
      palette, thresholds, texts, axis_mode, event_colors, font_family,
      plot_bg, neutral, show_grid, height_scale, num_mode, export, credit
    """
    st.markdown("---")
    with st.expander(f"🎨 {t('custom.header', lang)}", expanded=False):
        # ── cores de risco ────────────────────────────────────────────────
        st.caption(t("custom.risk_colors", lang))
        palette = {
            key: st.color_picker(t(f"risk.{key}", lang), RISK_PALETTE[key], key=f"pal_{key}")
            for key in RISK_ORDER
        }

        # ── cores dos eventos ─────────────────────────────────────────────
        st.caption(t("custom.event_colors", lang))
        cols = st.columns(3)
        event_colors = [
            cols[i % 3].color_picker(f"#{i + 1}", EVENT_PALETTE[i], key=f"evtpal_{i}")
            for i in range(len(EVENT_PALETTE))
        ]

        # ── limites de classificação ──────────────────────────────────────
        st.caption(t("custom.thresholds", lang))
        default_cuts = [c for c, _ in RISK_THRESHOLDS]
        cols = st.columns(4)
        cuts = [
            col.number_input(t("custom.cut_upto", lang, name=t(f"risk.{label}", lang)),
                             -1.0, 1.0, float(default), 0.05, key=f"cut_{i}")
            for i, (col, (default, label)) in enumerate(zip(cols, RISK_THRESHOLDS))
        ]
        if not all(cuts[i] < cuts[i + 1] for i in range(len(cuts) - 1)):
            st.warning(t("custom.cuts_warning", lang))
            cuts = default_cuts
        thresholds = list(zip(cuts, [label for _, label in RISK_THRESHOLDS]))

        # ── textos (um conjunto por idioma, para não misturar edições) ───
        st.caption(t("custom.texts", lang))
        defaults = default_texts(lang)
        texts = {
            k: st.text_input(t(f"textlabel.{k}", lang), defaults[k], key=f"txt_{lang}_{k}")
            for k in TEXT_KEYS
        }

        # ── numeração das dimensões ───────────────────────────────────────
        st.caption(t("custom.numbering", lang))
        num_mode = st.radio(
            t("custom.numbering_mode", lang), NUM_MODES,
            format_func=lambda v: t(f"nummode.{v}", lang),
            help=t("custom.numbering_help", lang), key="num_mode",
        )

        # ── eixo do scatter ───────────────────────────────────────────────
        st.caption(t("custom.axis", lang))
        axis_mode = st.radio(
            t("custom.axis_range", lang), ["fixed", "dynamic"], horizontal=True,
            format_func=lambda v: t(f"axismode.{v}", lang),
            help=t("custom.axis_help", lang), key="axis_mode",
        )

        # ── aparência dos gráficos ────────────────────────────────────────
        st.caption(t("custom.appearance", lang))
        font_name = st.selectbox(t("custom.font", lang), list(FONT_CHOICES), key="font_name")
        c1, c2 = st.columns(2)
        plot_bg = c1.color_picker(t("custom.plot_bg", lang), BG_PLOT, key="plot_bg")
        neutral = c2.color_picker(t("custom.neutral", lang), NEUTRAL, key="neutral",
                                  help=t("custom.neutral_help", lang))
        show_grid = st.toggle(t("custom.grid", lang), value=True, key="show_grid")
        height_scale = st.slider(t("custom.height_scale", lang), 0.7, 1.6, 1.0, 0.05,
                                 key="height_scale", help=t("custom.height_help", lang))

        # ── exportação da imagem (botão de câmera do gráfico) ─────────────
        st.caption(t("custom.export", lang))
        c1, c2 = st.columns(2)
        export_format = c1.selectbox(t("custom.export_format", lang),
                                     ["png", "svg", "jpeg", "webp"], key="export_format")
        export_scale = c2.selectbox(t("custom.export_scale", lang), [1, 2, 3, 4], index=1,
                                    format_func=lambda v: f"{v}×", key="export_scale")

        # ── marca d'água / crédito ────────────────────────────────────────
        st.caption(t("custom.credit", lang))
        credit_show = st.toggle(t("custom.credit_show", lang), value=True, key="credit_show")
        credit_text = st.text_input(t("custom.credit_text", lang), t("credit", lang),
                                    disabled=not credit_show, key=f"credit_text_{lang}")
        c1, c2 = st.columns(2)
        credit_pos = c1.selectbox(t("custom.credit_pos", lang), CREDIT_POSITIONS,
                                  format_func=lambda v: t(f"credit_pos.{v}", lang),
                                  disabled=not credit_show, key="credit_pos")
        credit_size = c2.slider(t("custom.credit_size", lang), 8, 30, 12, 1,
                                disabled=not credit_show, key="credit_size")

    return {
        "palette":      palette,
        "event_colors": event_colors,
        "thresholds":   thresholds,
        "texts":        texts,
        "num_mode":     num_mode,
        "axis_mode":    axis_mode,
        "font_family":  FONT_CHOICES[font_name],
        "plot_bg":      plot_bg,
        "neutral":      neutral,
        "show_grid":    show_grid,
        "height_scale": height_scale,
        "export":       {"format": export_format, "scale": export_scale},
        "credit":       {"show": credit_show, "text": credit_text,
                         "size": credit_size, "position": credit_pos},
    }
