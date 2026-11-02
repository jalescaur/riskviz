# template.py — gera o modelo .xlsx que alimenta a aplicação
#
# O formato do arquivo é o mesmo de sempre (mesmas colunas, em inglês, em
# qualquer idioma da interface); só as abas, instruções e o texto dos
# exemplos mudam conforme o idioma selecionado.

import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from data import REQUIRED_COLUMNS
from i18n import t

OPTIONAL_COLUMNS = ["RISK_SCORE", "PROB_DV", "IV_USED", "PROB_VIT"]
TEMPLATE_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

SHEET_NAMES = {
    "pt": ("Dados", "Instruções"),
    "en": ("Data", "Instructions"),
    "es": ("Datos", "Instrucciones"),
    "fr": ("Données", "Instructions"),
}

# Exemplo: 2 eventos × 5 dimensões. Duas dimensões do evento A têm
# impacto/probabilidade iguais de propósito, para mostrar o efeito vermelho
# de bolhas sobrepostas. Cada linha: (impacto, prob., confiabilidade).
_EXAMPLE_VALUES = [
    # evento A (2026-06-11)
    (-0.70, 0.80, 0.90), (-0.55, 0.65, 0.80), (-0.55, 0.65, 0.70),
    (-0.80, 0.40, 0.60), (-0.45, 0.55, 0.85),
    # evento B (2026-06-12)
    (-0.65, 0.70, 0.90), (-0.40, 0.60, 0.80), (0.20, 0.35, 0.50),
    (-0.25, 0.30, 0.65), (0.35, 0.55, 0.70),
]

_EXAMPLE_TEXT = {
    "pt": (["Fechamento do Estreito de Ormuz", "Tarifa de 25% dos EUA sobre o Brasil"],
           [["Preço do petróleo", "Rotas de navegação", "Custo de seguros",
             "Segurança regional", "Oferta de energia"],
            ["Política comercial", "Exportações", "Câmbio", "Investimentos", "Cadeia de suprimentos"]]),
    "en": (["Strait of Hormuz closure", "25% US tariff on Brazil"],
           [["Oil prices", "Shipping routes", "Insurance costs",
             "Regional security", "Energy supply"],
            ["Trade policy", "Exports", "Currency", "Investment", "Supply chain"]]),
    "es": (["Cierre del Estrecho de Ormuz", "Arancel del 25% de EE. UU. a Brasil"],
           [["Precio del petróleo", "Rutas de navegación", "Costo de seguros",
             "Seguridad regional", "Suministro de energía"],
            ["Política comercial", "Exportaciones", "Tipo de cambio", "Inversiones", "Cadena de suministro"]]),
    "fr": (["Fermeture du détroit d'Ormuz", "Droit de douane américain de 25 % sur le Brésil"],
           [["Prix du pétrole", "Routes maritimes", "Coût des assurances",
             "Sécurité régionale", "Approvisionnement énergétique"],
            ["Politique commerciale", "Exportations", "Taux de change", "Investissements", "Chaîne d'approvisionnement"]]),
}

_HEADER_FILL = PatternFill("solid", fgColor="26619C")
_HEADER_FONT = Font(color="FFFFFF", bold=True)


def example_dataframe(lang: str = "pt") -> pd.DataFrame:
    """DataFrame de exemplo (mesmas colunas do modelo), no idioma pedido."""
    events, dims = _EXAMPLE_TEXT.get(lang, _EXAMPLE_TEXT["en"])
    rows, k = [], 0
    for e, (event_name, dim_names) in enumerate(zip(events, dims)):
        letter, day = "AB"[e], 11 + e
        for n, dim in enumerate(dim_names, start=1):
            impact, prob, trust = _EXAMPLE_VALUES[k]
            k += 1
            rows.append({
                "ID_DIMENSION":      f"EVT_2026_6_{day}_{letter}_{n}",
                "EVENT_KEYWORD":     event_name,
                "DIMENSION_KEYWORD": dim,
                "IMPACT":            impact,
                "PROB_DV_IV":        prob,
                "TRUSTABILITY":      trust,
                "RISK_SCORE":        round(impact * prob * trust, 3),
                "PROB_DV":           prob,
                "IV_USED":           "IV_1,IV_2",
                "PROB_VIT":          1,
            })
    return pd.DataFrame(rows, columns=TEMPLATE_COLUMNS)


def _style_header(ws, widths: dict | None = None):
    for cell in ws[1]:
        cell.font = _HEADER_FONT
        cell.fill = _HEADER_FILL
        cell.alignment = Alignment(vertical="center")
    ws.freeze_panes = "A2"


def build_template_xlsx(lang: str = "pt", with_example: bool = True) -> bytes:
    """Gera um .xlsx pronto para preencher: aba de dados (com ou sem as linhas
    de exemplo, validação de intervalo e dica em cada cabeçalho) + aba de
    instruções por coluna, no idioma pedido."""
    data_name, help_name = SHEET_NAMES.get(lang, SHEET_NAMES["en"])
    wb = Workbook()

    # ── aba de dados ──────────────────────────────────────────────────────
    ws = wb.active
    ws.title = data_name
    ws.append(TEMPLATE_COLUMNS)
    _style_header(ws)
    if with_example:
        for row in example_dataframe(lang).itertuples(index=False):
            ws.append(list(row))
    widths = {"ID_DIMENSION": 24, "EVENT_KEYWORD": 42, "DIMENSION_KEYWORD": 28}
    for idx, col in enumerate(TEMPLATE_COLUMNS, start=1):
        letter = ws.cell(row=1, column=idx).column_letter
        ws.column_dimensions[letter].width = widths.get(col, max(14, len(col) + 2))
        required = col in REQUIRED_COLUMNS
        ws.cell(row=1, column=idx).comment = Comment(
            f"{t('tpl.required' if required else 'tpl.optional', lang)}\n{t(f'help.{col}', lang)}",
            "Risk Visualizer", width=320, height=140,
        )

    # validação: impacto -1..1; probabilidade, confiabilidade e prob. 0..1
    last = 500
    for col, lo, hi in [("IMPACT", -1, 1), ("PROB_DV_IV", 0, 1), ("TRUSTABILITY", 0, 1),
                        ("RISK_SCORE", -1, 1)]:
        letter = ws.cell(row=1, column=TEMPLATE_COLUMNS.index(col) + 1).column_letter
        dv = DataValidation(
            type="decimal", operator="between", formula1=str(lo), formula2=str(hi),
            allow_blank=True, showErrorMessage=True,
            errorTitle=col, error=t("tpl.range_error", lang, lo=lo, hi=hi),
        )
        dv.add(f"{letter}2:{letter}{last}")
        ws.add_data_validation(dv)

    # ── aba de instruções ─────────────────────────────────────────────────
    wh = wb.create_sheet(help_name)
    wh.append([t("tpl.col_column", lang), t("tpl.col_required", lang), t("tpl.col_description", lang)])
    _style_header(wh)
    for col in TEMPLATE_COLUMNS:
        wh.append([col,
                   t("tpl.required" if col in REQUIRED_COLUMNS else "tpl.optional", lang),
                   t(f"help.{col}", lang)])
    wh.column_dimensions["A"].width = 20
    wh.column_dimensions["B"].width = 16
    wh.column_dimensions["C"].width = 95
    for row in wh.iter_rows(min_row=2):
        row[2].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
        row[1].alignment = Alignment(vertical="top")

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()
