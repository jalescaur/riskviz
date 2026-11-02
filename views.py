# views.py — conteúdo de cada aba (opções do gráfico + figura)
#
# Cada função recebe o DataFrame já filtrado e o dict `controls` devolvido por
# sidebar.render_sidebar(). As opções específicas de cada tipo de gráfico
# ficam num expander "⚙️ Opções do gráfico" dentro da própria aba.

import io
import streamlit as st
from charts import (
    make_scatter, make_heatmap, make_bar, make_bar_dimensions, make_radar,
    make_radar_compare, make_hierarchy, make_distribution, make_bubble_matrix,
    make_parallel, make_scatter3d, make_splom, make_stacked, make_donut,
)
from charts.style import add_credit
from config import METRIC_COLUMNS
from i18n import t
from keys import options_key

_AGGS = ["mean", "median", "min", "max"]
_AGGS_SUM = _AGGS + ["sum"]


# ── helpers ───────────────────────────────────────────────────────────────────

def _chart_config(controls: dict) -> dict:
    """Configuração da barra do Plotly; o botão de câmera usa o formato e a
    resolução escolhidos na personalização."""
    exp = controls["export"]
    return {
        "displayModeBar": True,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines",
        ],
        "toImageButtonOptions": {"format": exp["format"], "scale": exp["scale"],
                                 "filename": "risk_visualizer"},
        "displaylogo": False,
    }


def _show(fig, controls: dict):
    add_credit(fig, controls["style"], controls["credit"])
    st.plotly_chart(fig, width="stretch", config=_chart_config(controls))


def _options(lang: str):
    return st.expander(f"⚙️ {t('opts.header', lang)}", expanded=False)


def _title(controls, key):
    st.markdown(f"**{controls['texts'][key]}**")


# ── abas ──────────────────────────────────────────────────────────────────────

def scatter_view(df, controls):
    lang = controls["lang"]
    _title(controls, "scatter_title")
    fig = make_scatter(df, controls["style"], controls["scatter"])
    _show(fig, controls)
    o = controls["scatter"]
    if (o.x_axis, o.y_axis) == ("IMPACT", "PROB_DV_IV"):
        st.caption(t("scatter.caption_quadrants", lang))
    st.caption(f"🔴 {t('scatter.caption_overlap', lang)}")


def heatmap_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "heatmap_title")
    with _options(lang):
        c1, c2, c3 = st.columns(3)
        agg = c1.selectbox(t("opts.aggregation", lang), _AGGS, key="hm_agg",
                           format_func=lambda v: t(f"agg.{v}", lang))
        decimals = c2.slider(t("opts.decimals", lang), 0, 3, 2, key="hm_dec")
        value_font = c3.slider(t("opts.value_font", lang), 8, 22, 11, key="hm_font")
        c1, c2, c3 = st.columns(3)
        show_values = c1.toggle(t("opts.show_values", lang), True, key="hm_vals")
        transpose = c2.toggle(t("opts.transpose", lang), False, key="hm_tr")
        show_cb = c3.toggle(t("opts.colorbar", lang), True, key="hm_cb")
    _show(make_heatmap(df, style, agg, show_values, decimals, value_font, transpose, show_cb),
          controls)


def ranking_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    mode = st.radio(t("rank.by", lang), ["event", "dimension"], horizontal=True,
                    format_func=lambda v: t(f"rank.by_{v}", lang), key="rk_mode",
                    label_visibility="collapsed")
    _title(controls, "bar_title" if mode == "event" else "dims_title")
    with _options(lang):
        c1, c2, c3 = st.columns(3)
        sort = c1.selectbox(t("opts.sort", lang), ["asc", "desc", "alpha"], key="rk_sort",
                            format_func=lambda v: t(f"sort.{v}", lang))
        value_font = c2.slider(t("opts.value_font", lang), 8, 22, 11, key="rk_font")
        bar_gap = c3.slider(t("opts.bar_gap", lang), 0.0, 0.6, 0.15, 0.05, key="rk_gap")
        c1, c2, c3 = st.columns(3)
        show_values = c1.toggle(t("opts.show_values", lang), True, key="rk_vals")
        if mode == "event":
            agg = c2.selectbox(t("opts.aggregation", lang), _AGGS_SUM, key="rk_agg",
                               format_func=lambda v: t(f"agg.{v}", lang))
        else:
            top_n = c2.slider(t("opts.top_n", lang), 0, max(len(df), 1), 0, key="rk_top",
                              help=t("opts.top_n_help", lang))
            color_by = c3.radio(t("sidebar.color_by", lang), ["risk", "event"], horizontal=True,
                                format_func=lambda v: t(f"colorby.{v}", lang), key="rk_color")
    if mode == "event":
        fig = make_bar(df, style, agg, sort, show_values, value_font, bar_gap)
    else:
        fig = make_bar_dimensions(df, style, sort, top_n, color_by, show_values, value_font, bar_gap)
    _show(fig, controls)


def radar_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "radar_title")
    events = sorted(df["EVENT_LETTER"].unique())
    names = df.drop_duplicates("EVENT_LETTER").set_index("EVENT_LETTER")["SHORT_EVENT"].to_dict()
    mode = st.radio(t("radar.mode", lang), ["single", "compare"], horizontal=True,
                    format_func=lambda v: t(f"radar.mode_{v}", lang), key="rd_mode",
                    label_visibility="collapsed")
    with _options(lang):
        c1, c2, c3 = st.columns(3)
        range_mode = c1.radio(t("radar.range", lang), ["fixed", "auto"], horizontal=True,
                              format_func=lambda v: t(f"radar.range_{v}", lang), key="rd_range")
        fill = c2.slider(t("radar.fill", lang), 0.0, 0.6, 0.15, 0.05, key="rd_fill")
        markers = c3.toggle(t("radar.markers", lang), True, key="rd_mark")
        use_numbers = False
        if mode == "single":
            use_numbers = st.toggle(t("radar.use_numbers", lang), False, key="rd_num",
                                    help=t("radar.use_numbers_help", lang))

    if mode == "single":
        sel = st.selectbox(t("radar.select_event", lang), events,
                           key=options_key("radar_sel", events))
        fig = make_radar(df, sel, style, range_mode, fill, markers, use_numbers)
        if fig:
            st.caption(f"**{sel}** — {names[sel]}")
    else:
        sel = st.multiselect(t("radar.select_events", lang), events,
                             default=events[:3], key=options_key("rd_multi", events))
        fig = make_radar_compare(df, sel, style, range_mode, fill, markers) if sel else None
    if fig:
        _show(fig, controls)
    else:
        st.info(t("radar.no_data", lang))


def hierarchy_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "hierarchy_title")
    with _options(lang):
        c1, c2, c3 = st.columns(3)
        kind = c1.radio(t("opts.kind", lang), ["treemap", "sunburst"],
                        format_func=lambda v: t(f"hier.{v}", lang), key="hi_kind")
        size_mode = c2.radio(t("hier.size", lang), ["abs", "equal"],
                             format_func=lambda v: t(f"hier.size_{v}", lang), key="hi_size")
        font = c3.slider(t("opts.value_font", lang), 8, 24, 14, key="hi_font")
        height = st.slider(t("scatter.height", lang), 350, 1000, 560, 10, key="hi_h")
    _show(make_hierarchy(df, style, kind, size_mode, font, height), controls)


def distribution_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "dist_title")
    with _options(lang):
        c1, c2 = st.columns(2)
        kind = c1.radio(t("opts.kind", lang), ["box", "violin", "histogram"], horizontal=True,
                        format_func=lambda v: t(f"dist.{v}", lang), key="ds_kind")
        metric = c2.selectbox(t("dist.metric", lang), METRIC_COLUMNS, key="ds_metric",
                              format_func=lambda c: t(f"axis.{c}", lang))
        c1, c2, c3 = st.columns(3)
        by_event = c1.toggle(t("dist.by_event", lang), True, key="ds_evt")
        points = c2.toggle(t("dist.points", lang), True, key="ds_pts",
                           disabled=kind == "histogram")
        bins = c3.slider(t("dist.bins", lang), 4, 30, 10, key="ds_bins",
                         disabled=kind != "histogram")
    _show(make_distribution(df, style, kind, metric, by_event, points, bins), controls)


def matrix_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "matrix_title")
    with _options(lang):
        c1, c2, c3 = st.columns(3)
        agg = c1.selectbox(t("opts.aggregation", lang), _AGGS, key="mx_agg",
                           format_func=lambda v: t(f"agg.{v}", lang))
        max_b = c2.slider(t("scatter.max_bubble", lang), 20, 90, 46, key="mx_size")
        font = c3.slider(t("opts.value_font", lang), 8, 22, 11, key="mx_font")
        show_values = st.toggle(t("opts.show_values", lang), True, key="mx_vals")
    _show(make_bubble_matrix(df, style, agg, max_b, show_values, font), controls)


def factors_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "factors_title")
    kind = st.radio(t("opts.kind", lang), ["parallel", "3d", "splom"], horizontal=True,
                    format_func=lambda v: t(f"fac.{v}", lang), key="fc_kind",
                    label_visibility="collapsed")
    st.caption(t(f"fac.{kind}_help", lang))
    if kind == "parallel":
        fig = make_parallel(df, style)
    else:
        with _options(lang):
            color_by = st.radio(t("sidebar.color_by", lang), ["risk", "event"], horizontal=True,
                                format_func=lambda v: t(f"colorby.{v}", lang), key="fc_color")
            labels = st.toggle(t("fac.labels", lang), True, key="fc_labels") if kind == "3d" else False
        fig = (make_scatter3d(df, style, color_by, labels) if kind == "3d"
               else make_splom(df, style, color_by))
    _show(fig, controls)


def composition_view(df, controls):
    lang, style = controls["lang"], controls["style"]
    _title(controls, "comp_title")
    kind = st.radio(t("opts.kind", lang), ["stacked", "percent", "donut"], horizontal=True,
                    format_func=lambda v: t(f"comp.{v}", lang), key="cp_kind",
                    label_visibility="collapsed")
    with _options(lang):
        show_values = st.toggle(t("opts.show_values", lang), True, key="cp_vals")
    fig = (make_donut(df, style, show_values) if kind == "donut"
           else make_stacked(df, style, kind == "percent", show_values))
    _show(fig, controls)


# ── tabela detalhada ──────────────────────────────────────────────────────────

_TABLE_COLUMNS = [
    "MARK_LABEL", "ID_DIMENSION", "EVENT_KEYWORD", "DIM_LABEL",
    "PROB_DV_IV", "IMPACT", "TRUSTABILITY", "RISK_SCORE", "RISK_LABEL",
]


def detail_table(df, controls):
    lang, style = controls["lang"], controls["style"]
    table = df[[c for c in _TABLE_COLUMNS if c in df.columns]].copy()
    table["RISK_LABEL"] = table["RISK_LABEL"].map(style.risk_name)
    table = (table.sort_values("RISK_SCORE")
                  .rename(columns={c: t(f"table.{c}", lang) for c in table.columns}))
    st.dataframe(table, width="stretch", hide_index=True)

    buf = io.BytesIO()
    table.to_excel(buf, index=False)
    st.download_button(t("table.download", lang), data=buf.getvalue(),
                       file_name="risk_visualizer_table.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key="dl_table")


# (chave do rótulo da aba, função)
TABS = [
    ("scatter",   scatter_view),
    ("heatmap",   heatmap_view),
    ("ranking",   ranking_view),
    ("radar",     radar_view),
    ("hierarchy", hierarchy_view),
    ("dist",      distribution_view),
    ("matrix",    matrix_view),
    ("factors",   factors_view),
    ("comp",      composition_view),
]
