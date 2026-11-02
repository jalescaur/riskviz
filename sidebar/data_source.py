# sidebar/data_source.py — upload do .xlsx, modelos para baixar e validação

import streamlit as st
import pandas as pd
from data import load_file, missing_columns, REQUIRED_COLUMNS
from i18n import t
from template import build_template_xlsx, example_dataframe

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@st.cache_data(show_spinner=False)
def _template_bytes(lang: str, with_example: bool) -> bytes:
    return build_template_xlsx(lang, with_example)


def render_template_downloads(lang: str, prefix: str = "side"):
    """Botões de download do modelo (com exemplo e em branco). `prefix`
    diferencia as chaves quando os botões aparecem em mais de um lugar."""
    st.download_button(
        t("data.download_example", lang),
        data=_template_bytes(lang, True),
        file_name=t("data.example_filename", lang),
        mime=XLSX_MIME,
        help=t("data.download_example_help", lang),
        key=f"dl_example_{prefix}",
    )
    st.download_button(
        t("data.download_blank", lang),
        data=_template_bytes(lang, False),
        file_name=t("data.blank_filename", lang),
        mime=XLSX_MIME,
        help=t("data.download_blank_help", lang),
        key=f"dl_blank_{prefix}",
    )


def render_data_source(lang: str) -> pd.DataFrame | None:
    """Renderiza o upload de .xlsx + botões de modelo. Retorna o DataFrame
    bruto (ainda sem preprocess) ou None se não há dados."""
    st.markdown(f"**{t('data.header', lang)}**")
    render_template_downloads(lang)
    uploaded = st.file_uploader(t("data.uploader", lang), type=["xlsx"], key="uploaded_file")
    use_example = st.checkbox(
        t("data.use_example", lang), value=False, key="use_example",
        help=t("data.use_example_help", lang),
        disabled=uploaded is not None,
    )

    if not uploaded:
        if use_example:
            df_raw = example_dataframe(lang)
            st.info(t("data.example_loaded", lang, n=len(df_raw)))
            return df_raw
        return None

    try:
        df_raw = load_file(uploaded, lang)
    except Exception as e:
        st.error(t("err.load", lang, err=e))
        return None

    missing = missing_columns(df_raw)
    if missing:
        st.error(t("err.missing_cols", lang,
                   missing=", ".join(missing), expected=", ".join(REQUIRED_COLUMNS)))
        return None

    st.success(t("data.loaded", lang, n=len(df_raw)))
    return df_raw
