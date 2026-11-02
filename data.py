# data.py — parsing, pré-processamento e lógica de negócio

import re
import pandas as pd
from config import RISK_PALETTE, RISK_THRESHOLDS, RISK_DEFAULT_LABEL
from i18n import t


REQUIRED_COLUMNS = [
    "ID_DIMENSION", "EVENT_KEYWORD", "DIMENSION_KEYWORD",
    "IMPACT", "PROB_DV_IV", "TRUSTABILITY",
]

# Modos de numeração das dimensões (número que aparece junto à bolha e na legenda)
NUM_MODES = ["seq", "id", "evt"]


def missing_columns(df: pd.DataFrame) -> list[str]:
    """Retorna as colunas obrigatórias ausentes no DataFrame."""
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


# ── helpers de classificação ──────────────────────────────────────────────────

def risk_label(score: float, thresholds: list[tuple[float, str]] | None = None) -> str:
    """Classifica um risk score em categoria textual.

    thresholds: lista opcional [(corte, label), ...] em ordem ascendente,
    para sobrescrever config.RISK_THRESHOLDS (usado pela personalização
    na sidebar).
    """
    for threshold, label in (thresholds or RISK_THRESHOLDS):
        if score <= threshold:
            return label
    return RISK_DEFAULT_LABEL


def risk_color(score: float, thresholds: list[tuple[float, str]] | None = None,
                palette: dict | None = None) -> str:
    """Retorna a cor hex correspondente ao risk score.

    palette: dict opcional {label: cor_hex} para sobrescrever
    config.RISK_PALETTE (usado pela personalização na sidebar).
    """
    return (palette or RISK_PALETTE)[risk_label(score, thresholds)]


# ── parsing de IDs ────────────────────────────────────────────────────────────

def parse_event_id(id_str: str) -> tuple[str, str, str]:
    """
    Extrai componentes do ID_DIMENSION.

    Aceita três formatos:
      EVT_YYYY_M_D_LETRA_NUM  (6 partes, ex.: EVT_2026_6_16_A_1)
      EVT_YYYY_M_D_EVT_NUM    (6 partes, evento numérico — ex.: EVT_2026_10_25_1_3)
      EVT_YYYY_M_D_NUM        (5 partes, sem evento — ex.: EVT_2026_6_16_1)

    Com evento numérico, EVENT_LETTER é "YYYY_M_D_EVT": as dimensões do mesmo
    evento ficam juntas e o ID completo não vira um "evento" por dimensão.
    No formato sem evento, EVENT_LETTER é derivado da combinação YYYY_M_D
    (todas as dimensões com a mesma data caem no mesmo "evento"), e o NUM
    final é usado como dim_num.

    Retorna: (date_str, event_letter, dim_num)
    """
    parts = id_str.split("_")

    if len(parts) == 6 and parts[4].isdigit():
        date_str     = f"{parts[1]}-{parts[2].zfill(2)}-{parts[3].zfill(2)}"
        event_letter = f"{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}"
        return date_str, event_letter, parts[5]

    if len(parts) >= 6 and re.fullmatch(r"[A-Za-z]+", parts[4]):
        # formato completo: EVT_YYYY_M_D_LETRA_NUM
        date_str     = f"{parts[1]}-{parts[2].zfill(2)}-{parts[3].zfill(2)}"
        event_letter = parts[4]
        dim_num      = parts[5]
        return date_str, event_letter, dim_num

    if len(parts) == 5:
        # formato sem letra: EVT_YYYY_M_D_NUM
        date_str     = f"{parts[1]}-{parts[2].zfill(2)}-{parts[3].zfill(2)}"
        event_letter = f"{parts[1]}_{parts[2]}_{parts[3]}"  # agrupa por data
        dim_num      = parts[4]
        return date_str, event_letter, dim_num

    return "unknown", id_str, "1"


# ── limpeza ───────────────────────────────────────────────────────────────────

def drop_invalid_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove linhas sem ID ou com impacto/probabilidade/confiabilidade
    não numéricos (ex.: linhas em branco no fim da planilha).
    Retorna (df_limpo, quantidade_removida)."""
    df = df.copy()
    for col in ["IMPACT", "PROB_DV_IV", "TRUSTABILITY"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    valid = (
        df["ID_DIMENSION"].notna()
        & df[["IMPACT", "PROB_DV_IV", "TRUSTABILITY"]].notna().all(axis=1)
    )
    return df[valid].reset_index(drop=True), int((~valid).sum())


# ── numeração das dimensões ───────────────────────────────────────────────────

def _mark_labels(df: pd.DataFrame, num_mode: str) -> pd.Series:
    if num_mode == "id":
        return df["DIM_NUM"].astype(str)
    if num_mode == "evt":
        short = df["EVENT_LETTER"].astype(str).str.len() <= 3
        return (df["EVENT_LETTER"].astype(str) + df["DIM_NUM"].astype(str)).where(
            short, df["SEQ_NUM"].astype(str))
    return df["SEQ_NUM"].astype(str)


# ── pré-processamento principal ───────────────────────────────────────────────

def preprocess(df: pd.DataFrame, thresholds: list[tuple[float, str]] | None = None,
                palette: dict | None = None, num_mode: str = "seq") -> pd.DataFrame:
    """
    Recebe o DataFrame bruto e devolve um enriquecido com colunas derivadas.

    thresholds/palette: overrides opcionais vindos da personalização na
    sidebar (default: config.RISK_THRESHOLDS/RISK_PALETTE).
    num_mode: como numerar as dimensões — "seq" (1..N em todo o conjunto),
    "id" (o NUM do ID_DIMENSION) ou "evt" (letra do evento + NUM, ex.: A1).

    Colunas adicionadas:
      DATE, EVENT_LETTER, DIM_NUM  — desmembradas de ID_DIMENSION
      RISK_SCORE                   — recalculado se necessário
      RISK_LABEL, RISK_COLOR       — classificação e cor
      DIM_LABEL                    — rótulo legível da dimensão
      SEQ_NUM, MARK_LABEL          — número da dimensão (junto à bolha)
      LEGEND_TEXT                  — "número - dimensão", usado nas legendas
      SHORT_EVENT                  — versão truncada de EVENT_KEYWORD
      EVENT_AGG_SCORE              — média do risk score por evento
    """
    df = df.copy().reset_index(drop=True)

    # parse ID
    parsed = [parse_event_id(str(x)) for x in df["ID_DIMENSION"]]
    df["DATE"]         = [p[0] for p in parsed]
    df["EVENT_LETTER"] = [p[1] for p in parsed]
    df["DIM_NUM"]      = [p[2] for p in parsed]

    # tipos numéricos
    for col in ["RISK_SCORE","IMPACT","PROB_DV_IV","TRUSTABILITY","PROB_DV","PROB_VIT"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # RISK_SCORE: calcula onde estiver em branco (coluna ausente ou células vazias)
    computed = df["PROB_DV_IV"] * df["IMPACT"] * df["TRUSTABILITY"]
    if "RISK_SCORE" not in df.columns:
        df["RISK_SCORE"] = computed
    else:
        df["RISK_SCORE"] = df["RISK_SCORE"].fillna(computed)

    # classificação
    df["RISK_LABEL"] = df["RISK_SCORE"].apply(lambda s: risk_label(s, thresholds))
    df["RISK_COLOR"] = df["RISK_SCORE"].apply(lambda s: risk_color(s, thresholds, palette))

    # rótulo da dimensão: usa DIMENSION_KEYWORD se preenchido, senão "Dim N"
    df["DIM_LABEL"] = [
        str(kw).strip() if pd.notna(kw) and str(kw).strip() else f"Dim {num}"
        for kw, num in zip(df["DIMENSION_KEYWORD"], df["DIM_NUM"])
    ]

    # numeração: ordena por evento e pelo NUM do ID (numérico quando possível)
    df["_NUM_INT"] = pd.to_numeric(df["DIM_NUM"], errors="coerce").fillna(10**6)
    order = df.sort_values(["EVENT_LETTER", "_NUM_INT"], kind="stable").index
    df.loc[order, "SEQ_NUM"] = range(1, len(df) + 1)
    df["SEQ_NUM"]    = df["SEQ_NUM"].astype(int)
    df["MARK_LABEL"] = _mark_labels(df, num_mode)
    df["LEGEND_TEXT"] = df["MARK_LABEL"] + " - " + df["DIM_LABEL"]
    df = df.drop(columns=["_NUM_INT"])

    # evento truncado para legenda
    df["SHORT_EVENT"] = df["EVENT_KEYWORD"].apply(
        lambda x: (str(x)[:40] + "…") if len(str(x)) > 40 else str(x)
    )

    # score agregado por evento (média)
    df["EVENT_AGG_SCORE"] = df.groupby("EVENT_LETTER")["RISK_SCORE"].transform("mean")

    return df


# ── loader de arquivo ─────────────────────────────────────────────────────────

def load_file(uploaded_file, lang: str = "pt") -> pd.DataFrame:
    """Carrega .xlsx a partir de um st.file_uploader object."""
    name = uploaded_file.name.lower()
    if not name.endswith(".xlsx"):
        raise ValueError(t("err.format", lang, name=name))
    return pd.read_excel(uploaded_file)
