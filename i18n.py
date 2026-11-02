# i18n.py — textos da interface em português, inglês, espanhol e francês
#
# Cada chave tem uma tupla (pt, en, es, fr). Use t(chave, idioma, **valores);
# placeholders no formato {nome} são preenchidos por str.format.
# Os nomes das colunas do arquivo .xlsx (ID_DIMENSION, IMPACT…) NÃO são
# traduzidos: o modelo de arquivo é o mesmo em todos os idiomas.

LANGS = {"pt": "Português", "en": "English", "es": "Español", "fr": "Français"}
DEFAULT_LANG = "pt"
_IDX = {code: i for i, code in enumerate(LANGS)}


def t(key: str, lang: str = DEFAULT_LANG, **kw) -> str:
    entry = _S.get(key)
    if entry is None:
        return key
    text = entry[_IDX.get(lang, 0)]
    return text.format(**kw) if kw else text


_S: dict[str, tuple[str, str, str, str]] = {
    # ── erros e mensagens do carregamento ────────────────────────────────
    "err.format": (
        "Formato não suportado: {name}. Envie um arquivo .xlsx.",
        "Unsupported format: {name}. Please upload an .xlsx file.",
        "Formato no compatible: {name}. Suba un archivo .xlsx.",
        "Format non pris en charge : {name}. Envoyez un fichier .xlsx.",
    ),
    "err.load": (
        "Erro ao carregar arquivo: {err}",
        "Error loading file: {err}",
        "Error al cargar el archivo: {err}",
        "Erreur lors du chargement du fichier : {err}",
    ),
    "err.missing_cols": (
        "Arquivo sem as colunas obrigatórias: {missing}.\n\nColunas esperadas: {expected}.",
        "File is missing required columns: {missing}.\n\nExpected columns: {expected}.",
        "Al archivo le faltan columnas obligatorias: {missing}.\n\nColumnas esperadas: {expected}.",
        "Colonnes obligatoires manquantes dans le fichier : {missing}.\n\nColonnes attendues : {expected}.",
    ),

    # ── crédito impresso nos gráficos ────────────────────────────────────
    "custom.credit": ("Marca d'água (crédito)", "Watermark (credit)",
                      "Marca de agua (crédito)", "Filigrane (crédit)"),
    "custom.credit_show": ("Mostrar marca d'água", "Show watermark",
                           "Mostrar marca de agua", "Afficher le filigrane"),
    "custom.credit_text": ("Texto da marca d'água", "Watermark text",
                           "Texto de la marca de agua", "Texte du filigrane"),
    "custom.credit_size": ("Tamanho da marca d'água", "Watermark size",
                           "Tamaño de la marca de agua", "Taille du filigrane"),
    "custom.credit_pos": ("Posição da marca d'água", "Watermark position",
                          "Posición de la marca de agua", "Position du filigrane"),
    "credit_pos.top_left": ("Topo, à esquerda (sobre a legenda de eventos)", "Top left (above the event legend)",
                            "Arriba a la izquierda (sobre la leyenda de eventos)", "En haut à gauche (au-dessus de la légende des événements)"),
    "credit_pos.top_right": ("Topo, à direita", "Top right", "Arriba a la derecha", "En haut à droite"),
    "credit_pos.bottom_left": ("Rodapé, à esquerda", "Bottom left", "Abajo a la izquierda", "En bas à gauche"),
    "credit_pos.bottom_right": ("Rodapé, à direita", "Bottom right", "Abajo a la derecha", "En bas à droite"),
    "credit": (
        "Centro de Estudos Globais/UnB",
        "Center for Global Studies/UnB",
        "Centro de Estudios Globales/UnB",
        "Centre d'études globales/UnB",
    ),

    # ── dados / modelo ───────────────────────────────────────────────────
    "data.header": ("Dados", "Data", "Datos", "Données"),
    "data.download_example": (
        "📥 Baixar modelo com exemplo (.xlsx)",
        "📥 Download template with example (.xlsx)",
        "📥 Descargar plantilla con ejemplo (.xlsx)",
        "📥 Télécharger le modèle avec exemple (.xlsx)",
    ),
    "data.download_example_help": (
        "Planilha pronta para preencher: 2 eventos de exemplo (com duas bolhas "
        "sobrepostas de propósito), validação de valores e uma aba de instruções por coluna.",
        "Ready-to-fill spreadsheet: 2 sample events (with two deliberately "
        "overlapping bubbles), value validation and an instructions sheet per column.",
        "Hoja lista para completar: 2 eventos de ejemplo (con dos burbujas "
        "superpuestas a propósito), validación de valores y una hoja de instrucciones por columna.",
        "Feuille prête à remplir : 2 événements d'exemple (avec deux bulles "
        "volontairement superposées), validation des valeurs et une feuille d'instructions par colonne.",
    ),
    "data.example_filename": (
        "modelo_risk_visualizer.xlsx", "risk_visualizer_template.xlsx",
        "plantilla_risk_visualizer.xlsx", "modele_risk_visualizer.xlsx",
    ),
    "data.download_blank": (
        "📄 Baixar modelo em branco (.xlsx)",
        "📄 Download blank template (.xlsx)",
        "📄 Descargar plantilla en blanco (.xlsx)",
        "📄 Télécharger le modèle vierge (.xlsx)",
    ),
    "data.blank_filename": (
        "modelo_risk_visualizer_em_branco.xlsx", "risk_visualizer_template_blank.xlsx",
        "plantilla_risk_visualizer_en_blanco.xlsx", "modele_risk_visualizer_vierge.xlsx",
    ),
    "data.download_blank_help": (
        "Mesmas colunas e instruções, sem as linhas de exemplo.",
        "Same columns and instructions, without the example rows.",
        "Mismas columnas e instrucciones, sin las filas de ejemplo.",
        "Mêmes colonnes et instructions, sans les lignes d'exemple.",
    ),
    "data.uploader": ("Arquivo (.xlsx)", "File (.xlsx)", "Archivo (.xlsx)", "Fichier (.xlsx)"),
    "data.use_example": (
        "Usar dados de exemplo", "Use example data",
        "Usar datos de ejemplo", "Utiliser des données d'exemple",
    ),
    "data.use_example_help": (
        "Carrega o conjunto de exemplo do modelo para você explorar todos os "
        "gráficos sem precisar de um arquivo. Desativado quando há um arquivo enviado.",
        "Loads the template's example set so you can explore every chart "
        "without a file. Disabled when a file is uploaded.",
        "Carga el conjunto de ejemplo de la plantilla para explorar todos los "
        "gráficos sin necesidad de un archivo. Desactivado si hay un archivo subido.",
        "Charge l'ensemble d'exemple du modèle pour explorer tous les graphiques "
        "sans fichier. Désactivé lorsqu'un fichier est envoyé.",
    ),
    "data.example_loaded": (
        "Dados de exemplo carregados ({n} linhas).",
        "Example data loaded ({n} rows).",
        "Datos de ejemplo cargados ({n} filas).",
        "Données d'exemple chargées ({n} lignes).",
    ),
    "data.loaded": (
        "{n} linhas carregadas", "{n} rows loaded",
        "{n} filas cargadas", "{n} lignes chargées",
    ),
    "data.empty": (
        "O arquivo não tem nenhuma linha de dados válida. Preencha o modelo e envie novamente.",
        "The file has no valid data rows. Fill in the template and upload it again.",
        "El archivo no tiene ninguna fila de datos válida. Complete la plantilla y vuelva a subirla.",
        "Le fichier ne contient aucune ligne de données valide. Remplissez le modèle et renvoyez-le.",
    ),
    "data.dropped": (
        "{n} linha(s) ignorada(s): ID ou valores de impacto/probabilidade/confiabilidade ausentes ou inválidos.",
        "{n} row(s) ignored: missing or invalid ID, impact, probability or reliability values.",
        "{n} fila(s) ignorada(s): ID o valores de impacto/probabilidad/confiabilidad ausentes o inválidos.",
        "{n} ligne(s) ignorée(s) : ID ou valeurs d'impact/probabilité/fiabilité absents ou invalides.",
    ),

    # ── tela inicial ─────────────────────────────────────────────────────
    "landing.info": (
        "Envie um arquivo .xlsx para começar — ou marque \"Usar dados de exemplo\" "
        "na barra lateral para explorar a aplicação.",
        "Upload an .xlsx file to get started — or tick \"Use example data\" "
        "in the sidebar to explore the app.",
        "Suba un archivo .xlsx para empezar — o marque \"Usar datos de ejemplo\" "
        "en la barra lateral para explorar la aplicación.",
        "Envoyez un fichier .xlsx pour commencer — ou cochez « Utiliser des données "
        "d'exemple » dans la barre latérale pour explorer l'application.",
    ),
    "landing.steps": (
        "**Como usar**\n\n1. Baixe o modelo abaixo (com exemplo ou em branco).\n"
        "2. Preencha uma linha por dimensão: ID, evento, dimensão, impacto, probabilidade e confiabilidade.\n"
        "3. Envie o arquivo na barra lateral — os gráficos aparecem na hora.",
        "**How to use**\n\n1. Download the template below (with example or blank).\n"
        "2. Fill in one row per dimension: ID, event, dimension, impact, probability and reliability.\n"
        "3. Upload the file in the sidebar — the charts appear instantly.",
        "**Cómo usar**\n\n1. Descargue la plantilla de abajo (con ejemplo o en blanco).\n"
        "2. Complete una fila por dimensión: ID, evento, dimensión, impacto, probabilidad y confiabilidad.\n"
        "3. Suba el archivo en la barra lateral — los gráficos aparecen al instante.",
        "**Mode d'emploi**\n\n1. Téléchargez le modèle ci-dessous (avec exemple ou vierge).\n"
        "2. Remplissez une ligne par dimension : ID, événement, dimension, impact, probabilité et fiabilité.\n"
        "3. Envoyez le fichier dans la barre latérale — les graphiques apparaissent aussitôt.",
    ),
    "landing.empty_filters": (
        "Nenhuma dimensão corresponde aos filtros atuais. Ajuste os filtros na barra lateral.",
        "No dimension matches the current filters. Adjust the filters in the sidebar.",
        "Ninguna dimensión coincide con los filtros actuales. Ajuste los filtros en la barra lateral.",
        "Aucune dimension ne correspond aux filtres actuels. Ajustez les filtres dans la barre latérale.",
    ),

    # ── KPIs e abas ──────────────────────────────────────────────────────
    "kpi.events":     ("Eventos", "Events", "Eventos", "Événements"),
    "kpi.dimensions": ("Dimensões", "Dimensions", "Dimensiones", "Dimensions"),
    "kpi.mean":       ("Score médio", "Mean score", "Score medio", "Score moyen"),
    "kpi.min":        ("Score mín", "Min score", "Score mín", "Score min"),
    "kpi.max":        ("Score máx", "Max score", "Score máx", "Score max"),

    "tab.scatter":   ("🔵 Scatter", "🔵 Scatter", "🔵 Dispersión", "🔵 Nuage de points"),
    "tab.heatmap":   ("🔥 Heatmap", "🔥 Heatmap", "🔥 Mapa de calor", "🔥 Carte thermique"),
    "tab.ranking":   ("📊 Ranking", "📊 Ranking", "📊 Ranking", "📊 Classement"),
    "tab.radar":     ("🕸 Radar", "🕸 Radar", "🕸 Radar", "🕸 Radar"),
    "tab.hierarchy": ("🌳 Hierarquia", "🌳 Hierarchy", "🌳 Jerarquía", "🌳 Hiérarchie"),
    "tab.dist":      ("📈 Distribuição", "📈 Distribution", "📈 Distribución", "📈 Distribution"),
    "tab.matrix":    ("⚪ Matriz de bolhas", "⚪ Bubble matrix", "⚪ Matriz de burbujas", "⚪ Matrice de bulles"),
    "tab.factors":   ("🧭 Fatores", "🧭 Factors", "🧭 Factores", "🧭 Facteurs"),
    "tab.comp":      ("🧱 Composição", "🧱 Composition", "🧱 Composición", "🧱 Composition"),

    # ── categorias de risco, eixos e hover ───────────────────────────────
    "risk.critical": ("Crítico", "Critical", "Crítico", "Critique"),
    "risk.high":     ("Alto", "High", "Alto", "Élevé"),
    "risk.moderate": ("Moderado", "Moderate", "Moderado", "Modéré"),
    "risk.low":      ("Baixo", "Low", "Bajo", "Faible"),
    "risk.positive": ("Positivo", "Positive", "Positivo", "Positif"),

    "axis.IMPACT":       ("Impacto", "Impact", "Impacto", "Impact"),
    "axis.PROB_DV_IV":   ("Probabilidade condicional", "Conditional probability",
                          "Probabilidad condicional", "Probabilité conditionnelle"),
    "axis.TRUSTABILITY": ("Confiabilidade", "Reliability", "Confiabilidad", "Fiabilité"),
    "axis.RISK_SCORE":   ("Risk Score", "Risk Score", "Risk Score", "Risk Score"),
    "hover.risk_score":  ("Risk score", "Risk score", "Risk score", "Risk score"),

    # ── textos padrão editáveis (e seus rótulos) ─────────────────────────
    "default.page_title": ("Risk Score Visualizer",) * 4,
    "default.page_subtitle": (
        "Análise de eventos geopolíticos e dimensões de risco",
        "Analysis of geopolitical events and risk dimensions",
        "Análisis de eventos geopolíticos y dimensiones de riesgo",
        "Analyse des événements géopolitiques et des dimensions de risque",
    ),
    "default.scatter_title": ("Impacto × Probabilidade", "Impact × Probability",
                              "Impacto × Probabilidad", "Impact × Probabilité"),
    "default.heatmap_title": ("Heatmap", "Heatmap", "Mapa de calor", "Carte thermique"),
    "default.bar_title": ("Risk score médio por evento", "Average risk score by event",
                          "Risk score medio por evento", "Risk score moyen par événement"),
    "default.dims_title": ("Risk score por dimensão", "Risk score by dimension",
                           "Risk score por dimensión", "Risk score par dimension"),
    "default.radar_title": ("Radar por evento", "Radar by event", "Radar por evento", "Radar par événement"),
    "default.hierarchy_title": ("Evento → dimensão", "Event → dimension",
                                "Evento → dimensión", "Événement → dimension"),
    "default.dist_title": ("Distribuição dos scores", "Score distribution",
                           "Distribución de los scores", "Distribution des scores"),
    "default.matrix_title": ("Matriz evento × dimensão", "Event × dimension matrix",
                             "Matriz evento × dimensión", "Matrice événement × dimension"),
    "default.factors_title": ("Fatores do risco", "Risk factors", "Factores del riesgo", "Facteurs de risque"),
    "default.comp_title": ("Composição por classificação", "Composition by classification",
                           "Composición por clasificación", "Composition par classification"),
    "default.x_label": ("Impacto", "Impact", "Impacto", "Impact"),
    "default.y_label": ("Probabilidade condicional", "Conditional probability",
                        "Probabilidad condicional", "Probabilité conditionnelle"),

    "textlabel.page_title":    ("Título da página", "Page title", "Título de la página", "Titre de la page"),
    "textlabel.page_subtitle": ("Subtítulo da página", "Page subtitle", "Subtítulo de la página", "Sous-titre de la page"),
    "textlabel.scatter_title": ("Título — Scatter", "Title — Scatter", "Título — Dispersión", "Titre — Nuage de points"),
    "textlabel.heatmap_title": ("Título — Heatmap", "Title — Heatmap", "Título — Mapa de calor", "Titre — Carte thermique"),
    "textlabel.bar_title":     ("Título — Ranking por evento", "Title — Ranking by event",
                                "Título — Ranking por evento", "Titre — Classement par événement"),
    "textlabel.dims_title":    ("Título — Ranking por dimensão", "Title — Ranking by dimension",
                                "Título — Ranking por dimensión", "Titre — Classement par dimension"),
    "textlabel.radar_title":   ("Título — Radar", "Title — Radar", "Título — Radar", "Titre — Radar"),
    "textlabel.hierarchy_title": ("Título — Hierarquia", "Title — Hierarchy", "Título — Jerarquía", "Titre — Hiérarchie"),
    "textlabel.dist_title":    ("Título — Distribuição", "Title — Distribution", "Título — Distribución", "Titre — Distribution"),
    "textlabel.matrix_title":  ("Título — Matriz de bolhas", "Title — Bubble matrix",
                                "Título — Matriz de burbujas", "Titre — Matrice de bulles"),
    "textlabel.factors_title": ("Título — Fatores", "Title — Factors", "Título — Factores", "Titre — Facteurs"),
    "textlabel.comp_title":    ("Título — Composição", "Title — Composition", "Título — Composición", "Titre — Composition"),
    "textlabel.x_label": ("Label do eixo X (Impacto)", "X-axis label (Impact)",
                          "Etiqueta del eje X (Impacto)", "Libellé de l'axe X (Impact)"),
    "textlabel.y_label": ("Label do eixo Y (Probabilidade)", "Y-axis label (Probability)",
                          "Etiqueta del eje Y (Probabilidad)", "Libellé de l'axe Y (Probabilité)"),

    # ── personalização ───────────────────────────────────────────────────
    "custom.header": ("Personalização", "Customization", "Personalización", "Personnalisation"),
    "custom.risk_colors": ("Cores de risco", "Risk colors", "Colores de riesgo", "Couleurs de risque"),
    "custom.event_colors": (
        "Cores dos eventos (usadas em \"Cor por evento\")",
        "Event colors (used in \"Color by event\")",
        "Colores de los eventos (usados en \"Color por evento\")",
        "Couleurs des événements (utilisées dans « Couleur par événement »)",
    ),
    "custom.thresholds": (
        "Limites de classificação (score ≤ valor → categoria)",
        "Classification limits (score ≤ value → category)",
        "Límites de clasificación (score ≤ valor → categoría)",
        "Seuils de classification (score ≤ valeur → catégorie)",
    ),
    "custom.cut_upto": ("{name} até", "{name} up to", "{name} hasta", "{name} jusqu'à"),
    "custom.cuts_warning": (
        "Os limites precisam estar em ordem crescente — usando os valores padrão.",
        "Limits must be in ascending order — using the default values.",
        "Los límites deben estar en orden creciente — usando los valores predeterminados.",
        "Les seuils doivent être en ordre croissant — valeurs par défaut utilisées.",
    ),
    "custom.texts": ("Textos", "Texts", "Textos", "Textes"),
    "custom.numbering": ("Numeração das dimensões", "Dimension numbering",
                         "Numeración de las dimensiones", "Numérotation des dimensions"),
    "custom.numbering_mode": (
        "Número junto à bolha e na legenda", "Number beside the bubble and in the legend",
        "Número junto a la burbuja y en la leyenda", "Numéro près de la bulle et dans la légende",
    ),
    "custom.numbering_help": (
        "Sequencial numera todas as dimensões de 1 a N (sem repetir entre eventos). "
        "\"Do ID\" usa o número final do ID_DIMENSION. \"Evento + número\" usa a letra do evento (A1, B2…).",
        "Sequential numbers every dimension from 1 to N (no repeats across events). "
        "\"From ID\" uses the final number of ID_DIMENSION. \"Event + number\" uses the event letter (A1, B2…).",
        "Secuencial numera todas las dimensiones de 1 a N (sin repetir entre eventos). "
        "\"Del ID\" usa el número final del ID_DIMENSION. \"Evento + número\" usa la letra del evento (A1, B2…).",
        "Séquentiel numérote toutes les dimensions de 1 à N (sans répétition entre événements). "
        "« Depuis l'ID » utilise le numéro final de l'ID_DIMENSION. « Événement + numéro » utilise la lettre de l'événement (A1, B2…).",
    ),
    "nummode.seq": ("Sequencial (1, 2, 3…)", "Sequential (1, 2, 3…)", "Secuencial (1, 2, 3…)", "Séquentiel (1, 2, 3…)"),
    "nummode.id":  ("Do ID (NUM final)", "From ID (final NUM)", "Del ID (NUM final)", "Depuis l'ID (NUM final)"),
    "nummode.evt": ("Evento + número (A1, B2…)", "Event + number (A1, B2…)",
                    "Evento + número (A1, B2…)", "Événement + numéro (A1, B2…)"),
    "custom.axis": ("Eixo do scatter", "Scatter axis", "Eje del scatter", "Axe du nuage de points"),
    "custom.axis_range": ("Range dos eixos", "Axis range", "Rango de los ejes", "Plage des axes"),
    "custom.axis_help": (
        "Fixo mantém sempre a escala completa. Ajustado encurta o eixo até onde "
        "os dados realmente vão — dá mais espaço para os rótulos.",
        "Fixed always keeps the full scale. Fitted shortens the axis to where the "
        "data actually goes — leaving more room for labels.",
        "Fijo mantiene siempre la escala completa. Ajustado acorta el eje hasta donde "
        "llegan los datos — deja más espacio para las etiquetas.",
        "Fixe conserve toujours l'échelle complète. Ajusté raccourcit l'axe jusqu'où "
        "vont réellement les données — plus de place pour les libellés.",
    ),
    "axismode.fixed":   ("Fixo (-1 a +1)", "Fixed (-1 to +1)", "Fijo (-1 a +1)", "Fixe (-1 à +1)"),
    "axismode.dynamic": ("Ajustado aos dados", "Fitted to data", "Ajustado a los datos", "Ajusté aux données"),
    "custom.appearance": ("Aparência dos gráficos", "Chart appearance", "Apariencia de los gráficos", "Apparence des graphiques"),
    "custom.font": ("Fonte", "Font", "Fuente", "Police"),
    "custom.plot_bg": ("Fundo do gráfico", "Plot background", "Fondo del gráfico", "Fond du graphique"),
    "custom.neutral": ("Cor neutra", "Neutral color", "Color neutro", "Couleur neutre"),
    "custom.neutral_help": (
        "Cor do meio (score 0) nos gradientes de heatmap, hierarquia, matriz e coordenadas paralelas.",
        "Midpoint color (score 0) in the heatmap, hierarchy, matrix and parallel-coordinates gradients.",
        "Color central (score 0) en los gradientes del mapa de calor, jerarquía, matriz y coordenadas paralelas.",
        "Couleur centrale (score 0) des dégradés de la carte thermique, hiérarchie, matrice et coordonnées parallèles.",
    ),
    "custom.grid": ("Mostrar grade", "Show grid", "Mostrar cuadrícula", "Afficher la grille"),
    "custom.height_scale": ("Ajuste de altura dos gráficos", "Chart height adjustment",
                            "Ajuste de altura de los gráficos", "Ajustement de la hauteur des graphiques"),
    "custom.height_help": (
        "Multiplica a altura de todos os gráficos (1,0 = tamanho original).",
        "Multiplies the height of all charts (1.0 = original size).",
        "Multiplica la altura de todos los gráficos (1,0 = tamaño original).",
        "Multiplie la hauteur de tous les graphiques (1,0 = taille d'origine).",
    ),
    "custom.export": (
        "Imagem baixada (botão de câmera do gráfico)",
        "Downloaded image (chart camera button)",
        "Imagen descargada (botón de cámara del gráfico)",
        "Image téléchargée (bouton appareil photo du graphique)",
    ),
    "custom.export_format": ("Formato", "Format", "Formato", "Format"),
    "custom.export_scale": ("Resolução", "Resolution", "Resolución", "Résolution"),

    # ── filtros e controles gerais ───────────────────────────────────────
    "filters.header": ("Filtros", "Filters", "Filtros", "Filtres"),
    "filters.events": ("Eventos", "Events", "Eventos", "Événements"),
    "filters.dimensions": ("Dimensões", "Dimensions", "Dimensiones", "Dimensions"),
    "filters.risk_range": ("Faixa de risk score", "Risk score range", "Rango de risk score", "Plage de risk score"),
    "filters.min_trust": ("Confiabilidade mínima", "Minimum reliability", "Confiabilidad mínima", "Fiabilité minimale"),
    "sidebar.color_by": ("Cor por", "Color by", "Color por", "Couleur par"),
    "colorby.risk":  ("Risco", "Risk", "Riesgo", "Risque"),
    "colorby.event": ("Evento", "Event", "Evento", "Événement"),

    # ── scatter: rótulos ─────────────────────────────────────────────────
    "scatter.labels_header": ("Scatter – rótulos", "Scatter – labels", "Scatter – etiquetas", "Nuage de points – libellés"),
    "scatter.show_labels": ("Mostrar rótulos nas bolhas", "Show labels on bubbles",
                            "Mostrar etiquetas en las burbujas", "Afficher les libellés sur les bulles"),
    "scatter.show_labels_help": (
        "Desative para ver só as bolhas. O hover continua disponível mesmo desativado.",
        "Turn off to see only the bubbles. Hover stays available even when off.",
        "Desactive para ver solo las burbujas. El hover sigue disponible aunque esté desactivado.",
        "Désactivez pour ne voir que les bulles. Le survol reste disponible même désactivé.",
    ),
    "scatter.label_content": ("Conteúdo do rótulo", "Label content", "Contenido de la etiqueta", "Contenu du libellé"),
    "scatter.label_content_help": (
        "Número mostra só o número da dimensão junto à bolha (o nome fica na legenda do rodapé). "
        "Os outros modos escrevem o nome na própria bolha.",
        "Number shows only the dimension number beside the bubble (the name is in the footer legend). "
        "The other modes write the name on the bubble itself.",
        "Número muestra solo el número de la dimensión junto a la burbuja (el nombre queda en la leyenda inferior). "
        "Los otros modos escriben el nombre en la propia burbuja.",
        "Numéro n'affiche que le numéro de la dimension près de la bulle (le nom est dans la légende en bas). "
        "Les autres modes écrivent le nom sur la bulle elle-même.",
    ),
    "labelmode.number":      ("Número", "Number", "Número", "Numéro"),
    "labelmode.number_name": ("Número + nome", "Number + name", "Número + nombre", "Numéro + nom"),
    "labelmode.name":        ("Nome", "Name", "Nombre", "Nom"),
    "scatter.font_size": ("Tamanho da fonte", "Font size", "Tamaño de la fuente", "Taille de la police"),
    "scatter.positioning": ("Posicionamento", "Positioning", "Posicionamiento", "Positionnement"),
    "posmode.rotate":     ("Rodízio (evita colisão)", "Rotating (avoids collisions)",
                           "Rotación (evita colisiones)", "Rotation (évite les collisions)"),
    "posmode.fixed":      ("Fixo (rente à bolha)", "Fixed (close to bubble)",
                           "Fijo (junto a la burbuja)", "Fixe (près de la bulle)"),
    "posmode.individual": ("Individual (por bolha)", "Individual (per bubble)",
                           "Individual (por burbuja)", "Individuel (par bulle)"),
    "scatter.positioning_help": (
        "Rodízio alterna a posição do texto entre 6 ângulos para reduzir sobreposição entre rótulos "
        "vizinhos. Fixo usa sempre a mesma posição. Individual permite escolher a posição de cada bolha.",
        "Rotating alternates the text position between 6 angles to reduce overlap between neighboring "
        "labels. Fixed always uses the same position. Individual lets you choose each bubble's position.",
        "Rotación alterna la posición del texto entre 6 ángulos para reducir la superposición entre "
        "etiquetas vecinas. Fijo usa siempre la misma posición. Individual permite elegir la posición de cada burbuja.",
        "Rotation alterne la position du texte entre 6 angles pour réduire le chevauchement des libellés "
        "voisins. Fixe utilise toujours la même position. Individuel permet de choisir la position de chaque bulle.",
    ),
    "scatter.label_position": ("Posição do rótulo", "Label position", "Posición de la etiqueta", "Position du libellé"),
    "scatter.each_bubble": ("Posição de cada bolha ({n})", "Position of each bubble ({n})",
                            "Posición de cada burbuja ({n})", "Position de chaque bulle ({n})"),
    "pos.top_center":    ("Acima · centro", "Top · center", "Arriba · centro", "Haut · centre"),
    "pos.top_left":      ("Acima · esquerda", "Top · left", "Arriba · izquierda", "Haut · gauche"),
    "pos.top_right":     ("Acima · direita", "Top · right", "Arriba · derecha", "Haut · droite"),
    "pos.middle_center": ("Centro", "Center", "Centro", "Centre"),
    "pos.middle_left":   ("Meio · esquerda", "Middle · left", "Medio · izquierda", "Milieu · gauche"),
    "pos.middle_right":  ("Meio · direita", "Middle · right", "Medio · derecha", "Milieu · droite"),
    "pos.bottom_center": ("Abaixo · centro", "Bottom · center", "Abajo · centro", "Bas · centre"),
    "pos.bottom_left":   ("Abaixo · esquerda", "Bottom · left", "Abajo · izquierda", "Bas · gauche"),
    "pos.bottom_right":  ("Abaixo · direita", "Bottom · right", "Abajo · derecha", "Bas · droite"),

    # ── scatter: bolhas, eixos, legenda ──────────────────────────────────
    "scatter.options_header": ("Scatter – bolhas, eixos e legenda", "Scatter – bubbles, axes and legend",
                               "Scatter – burbujas, ejes y leyenda", "Nuage de points – bulles, axes et légende"),
    "scatter.axes": ("Eixos", "Axes", "Ejes", "Axes"),
    "scatter.x_axis": ("Eixo X", "X axis", "Eje X", "Axe X"),
    "scatter.y_axis": ("Eixo Y", "Y axis", "Eje Y", "Axe Y"),
    "scatter.bubbles": ("Bolhas", "Bubbles", "Burbujas", "Bulles"),
    "scatter.size_by": ("Tamanho da bolha por", "Bubble size by", "Tamaño de la burbuja por", "Taille de la bulle selon"),
    "scatter.size_none": ("Tamanho fixo", "Fixed size", "Tamaño fijo", "Taille fixe"),
    "scatter.opacity": ("Opacidade", "Opacity", "Opacidad", "Opacité"),
    "scatter.max_bubble": ("Tamanho máximo da bolha (px)", "Maximum bubble size (px)",
                           "Tamaño máximo de la burbuja (px)", "Taille maximale de la bulle (px)"),
    "scatter.min_bubble": ("Tamanho mínimo (px)", "Minimum size (px)", "Tamaño mínimo (px)", "Taille minimale (px)"),
    "scatter.height": ("Altura do gráfico (px)", "Chart height (px)", "Altura del gráfico (px)", "Hauteur du graphique (px)"),
    "scatter.quadrants": ("Rótulos de quadrante", "Quadrant labels", "Etiquetas de cuadrante", "Libellés de quadrant"),
    "scatter.midlines": ("Linhas de referência", "Reference lines", "Líneas de referencia", "Lignes de référence"),
    "scatter.legend": ("Legenda das dimensões", "Dimension legend", "Leyenda de las dimensiones", "Légende des dimensions"),
    "scatter.show_legend": ("Mostrar legenda no rodapé", "Show footer legend",
                            "Mostrar leyenda al pie", "Afficher la légende en bas"),
    "scatter.show_legend_help": (
        "Lista \"número - dimensão\" abaixo do gráfico (também sai na imagem baixada).",
        "Lists \"number - dimension\" below the chart (also included in the downloaded image).",
        "Lista \"número - dimensión\" debajo del gráfico (también sale en la imagen descargada).",
        "Liste « numéro - dimension » sous le graphique (incluse aussi dans l'image téléchargée).",
    ),
    "scatter.legend_cols": ("Colunas da legenda", "Legend columns", "Columnas de la leyenda", "Colonnes de la légende"),
    "scatter.auto": ("Automático", "Automatic", "Automático", "Automatique"),
    "scatter.event_legend_font": (
        "Fonte da legenda de eventos (topo)", "Event legend font size (top)",
        "Fuente de la leyenda de eventos (arriba)", "Police de la légende des événements (haut)"),
    "scatter.legend_font": ("Fonte da legenda de dimensões (rodapé)", "Dimension legend font size (footer)",
                          "Fuente de la leyenda de dimensiones (pie)", "Police de la légende des dimensions (bas)"),
    "scatter.legend_swatch": ("Amostra de cor na legenda", "Color swatch in legend",
                              "Muestra de color en la leyenda", "Pastille de couleur dans la légende"),
    "scatter.caption_quadrants": (
        "Quadrantes: esquerda = impacto negativo | direita = positivo | cima = alta probabilidade",
        "Quadrants: left = negative impact | right = positive | top = high probability",
        "Cuadrantes: izquierda = impacto negativo | derecha = positivo | arriba = alta probabilidad",
        "Quadrants : gauche = impact négatif | droite = positif | haut = forte probabilité",
    ),
    "scatter.caption_overlap": (
        "Borda vermelha e selo “+N” = bolhas na mesma posição (afastadas levemente só para ficarem visíveis).",
        "Red border and “+N” badge = bubbles in the same position (nudged apart slightly just so they stay visible).",
        "Borde rojo e insignia “+N” = burbujas en la misma posición (separadas levemente solo para que se vean).",
        "Bordure rouge et pastille « +N » = bulles à la même position (légèrement écartées pour rester visibles).",
    ),
    "scatter.overlap_hover": ("{n} bolhas sobrepostas aqui", "{n} overlapping bubbles here",
                              "{n} burbujas superpuestas aquí", "{n} bulles superposées ici"),
    "scatter.q_high_neg": ("Alta prob. · Impacto negativo", "High prob. · Negative impact",
                           "Alta prob. · Impacto negativo", "Forte prob. · Impact négatif"),
    "scatter.q_high_pos": ("Alta prob. · Impacto positivo", "High prob. · Positive impact",
                           "Alta prob. · Impacto positivo", "Forte prob. · Impact positif"),
    "scatter.q_low_neg": ("Baixa prob. · Impacto negativo", "Low prob. · Negative impact",
                          "Baja prob. · Impacto negativo", "Faible prob. · Impact négatif"),
    "scatter.q_low_pos": ("Baixa prob. · Impacto positivo", "Low prob. · Positive impact",
                          "Baja prob. · Impacto positivo", "Faible prob. · Impact positif"),

    # ── opções comuns dos gráficos ───────────────────────────────────────
    "opts.header": ("Opções do gráfico", "Chart options", "Opciones del gráfico", "Options du graphique"),
    "opts.aggregation": ("Agregação", "Aggregation", "Agregación", "Agrégation"),
    "agg.mean":   ("Média", "Mean", "Media", "Moyenne"),
    "agg.median": ("Mediana", "Median", "Mediana", "Médiane"),
    "agg.min":    ("Mínimo", "Minimum", "Mínimo", "Minimum"),
    "agg.max":    ("Máximo", "Maximum", "Máximo", "Maximum"),
    "agg.sum":    ("Soma", "Sum", "Suma", "Somme"),
    "opts.decimals": ("Casas decimais", "Decimal places", "Decimales", "Décimales"),
    "opts.value_font": ("Fonte dos valores", "Value font size", "Fuente de los valores", "Police des valeurs"),
    "opts.show_values": ("Mostrar valores", "Show values", "Mostrar valores", "Afficher les valeurs"),
    "opts.transpose": ("Transpor eixos", "Transpose axes", "Transponer ejes", "Transposer les axes"),
    "opts.colorbar": ("Barra de cores", "Color bar", "Barra de colores", "Barre de couleurs"),
    "opts.sort": ("Ordenação", "Sorting", "Ordenación", "Tri"),
    "sort.asc":   ("Do menor ao maior score", "Lowest to highest score", "Del menor al mayor score", "Du plus petit au plus grand score"),
    "sort.desc":  ("Do maior ao menor score", "Highest to lowest score", "Del mayor al menor score", "Du plus grand au plus petit score"),
    "sort.alpha": ("Alfabética", "Alphabetical", "Alfabética", "Alphabétique"),
    "opts.bar_gap": ("Espaço entre barras", "Bar spacing", "Espacio entre barras", "Espacement des barres"),
    "opts.top_n": ("Só as N maiores magnitudes (0 = todas)", "Only the N largest magnitudes (0 = all)",
                   "Solo las N mayores magnitudes (0 = todas)", "Seulement les N plus grandes magnitudes (0 = toutes)"),
    "opts.top_n_help": (
        "Mostra as N dimensões com maior |score|, tanto negativo quanto positivo.",
        "Shows the N dimensions with the largest |score|, negative or positive.",
        "Muestra las N dimensiones con mayor |score|, negativo o positivo.",
        "Affiche les N dimensions avec le plus grand |score|, négatif ou positif.",
    ),
    "opts.kind": ("Tipo", "Type", "Tipo", "Type"),

    # ── ranking ──────────────────────────────────────────────────────────
    "rank.by": ("Ranking por", "Ranking by", "Ranking por", "Classement par"),
    "rank.by_event": ("Evento", "Event", "Evento", "Événement"),
    "rank.by_dimension": ("Dimensão", "Dimension", "Dimensión", "Dimension"),
    "bar.hover_event": ("Score", "Score", "Score", "Score"),
    "bar.axis_mean":   ("Risk score médio", "Mean risk score", "Risk score medio", "Risk score moyen"),
    "bar.axis_median": ("Risk score (mediana)", "Risk score (median)", "Risk score (mediana)", "Risk score (médiane)"),
    "bar.axis_min":    ("Risk score (mínimo)", "Risk score (minimum)", "Risk score (mínimo)", "Risk score (minimum)"),
    "bar.axis_max":    ("Risk score (máximo)", "Risk score (maximum)", "Risk score (máximo)", "Risk score (maximum)"),
    "bar.axis_sum":    ("Risk score (soma)", "Risk score (sum)", "Risk score (suma)", "Risk score (somme)"),

    # ── radar ────────────────────────────────────────────────────────────
    "radar.mode": ("Modo", "Mode", "Modo", "Mode"),
    "radar.mode_single": ("Evento único", "Single event", "Evento único", "Événement unique"),
    "radar.mode_compare": ("Comparar eventos", "Compare events", "Comparar eventos", "Comparer les événements"),
    "radar.range": ("Escala radial", "Radial scale", "Escala radial", "Échelle radiale"),
    "radar.range_fixed": ("Fixa (-1 a +1)", "Fixed (-1 to +1)", "Fija (-1 a +1)", "Fixe (-1 à +1)"),
    "radar.range_auto": ("Ajustada", "Fitted", "Ajustada", "Ajustée"),
    "radar.fill": ("Opacidade do preenchimento", "Fill opacity", "Opacidad del relleno", "Opacité du remplissage"),
    "radar.markers": ("Marcadores", "Markers", "Marcadores", "Marqueurs"),
    "radar.use_numbers": ("Números nos eixos (com legenda)", "Numbers on axes (with legend)",
                          "Números en los ejes (con leyenda)", "Numéros sur les axes (avec légende)"),
    "radar.use_numbers_help": (
        "Troca os nomes das dimensões por números e coloca a legenda \"número - dimensão\" abaixo.",
        "Replaces dimension names with numbers and adds a \"number - dimension\" legend below.",
        "Cambia los nombres de las dimensiones por números y añade la leyenda \"número - dimensión\" abajo.",
        "Remplace les noms des dimensions par des numéros et ajoute la légende « numéro - dimension » en dessous.",
    ),
    "radar.select_event": ("Selecione o evento", "Select the event", "Seleccione el evento", "Sélectionnez l'événement"),
    "radar.select_events": ("Selecione os eventos", "Select the events", "Seleccione los eventos", "Sélectionnez les événements"),
    "radar.no_data": ("Sem dados para exibir.", "No data to display.", "Sin datos para mostrar.", "Aucune donnée à afficher."),

    # ── hierarquia, distribuição, fatores, composição ────────────────────
    "hier.treemap": ("Treemap", "Treemap", "Treemap", "Treemap"),
    "hier.sunburst": ("Sunburst", "Sunburst", "Sunburst", "Sunburst"),
    "hier.size": ("Tamanho dos blocos", "Block size", "Tamaño de los bloques", "Taille des blocs"),
    "hier.size_abs": ("Proporcional a |score|", "Proportional to |score|", "Proporcional a |score|", "Proportionnelle à |score|"),
    "hier.size_equal": ("Iguais", "Equal", "Iguales", "Égaux"),

    "dist.box": ("Boxplot", "Boxplot", "Diagrama de caja", "Boîte à moustaches"),
    "dist.violin": ("Violino", "Violin", "Violín", "Violon"),
    "dist.histogram": ("Histograma", "Histogram", "Histograma", "Histogramme"),
    "dist.metric": ("Métrica", "Metric", "Métrica", "Métrique"),
    "dist.by_event": ("Separar por evento", "Split by event", "Separar por evento", "Séparer par événement"),
    "dist.points": ("Mostrar pontos", "Show points", "Mostrar puntos", "Afficher les points"),
    "dist.bins": ("Nº de faixas", "Number of bins", "N.º de intervalos", "Nombre de classes"),
    "dist.all": ("Todos", "All", "Todos", "Tous"),
    "dist.count": ("Quantidade", "Count", "Cantidad", "Nombre"),

    "fac.parallel": ("Coordenadas paralelas", "Parallel coordinates", "Coordenadas paralelas", "Coordonnées parallèles"),
    "fac.3d": ("Scatter 3D", "3D scatter", "Scatter 3D", "Nuage 3D"),
    "fac.splom": ("Matriz de dispersão", "Scatter matrix", "Matriz de dispersión", "Matrice de dispersion"),
    "fac.parallel_help": (
        "Cada linha é uma dimensão atravessando impacto, probabilidade, confiabilidade e risk score. "
        "Arraste sobre um eixo para filtrar uma faixa.",
        "Each line is a dimension crossing impact, probability, reliability and risk score. "
        "Drag along an axis to filter a range.",
        "Cada línea es una dimensión que cruza impacto, probabilidad, confiabilidad y risk score. "
        "Arrastre sobre un eje para filtrar un rango.",
        "Chaque ligne est une dimension traversant impact, probabilité, fiabilité et risk score. "
        "Faites glisser sur un axe pour filtrer une plage.",
    ),
    "fac.3d_help": (
        "Impacto × Probabilidade × Confiabilidade; o tamanho do ponto é |risk score|. Arraste para girar.",
        "Impact × Probability × Reliability; point size is |risk score|. Drag to rotate.",
        "Impacto × Probabilidad × Confiabilidad; el tamaño del punto es |risk score|. Arrastre para girar.",
        "Impact × Probabilité × Fiabilité ; la taille du point est |risk score|. Faites glisser pour pivoter.",
    ),
    "fac.splom_help": (
        "Todos os cruzamentos de duas variáveis, para achar correlações e outliers.",
        "Every pairwise combination of two variables, to spot correlations and outliers.",
        "Todos los cruces de dos variables, para hallar correlaciones y valores atípicos.",
        "Tous les croisements de deux variables, pour repérer corrélations et valeurs aberrantes.",
    ),
    "fac.labels": ("Mostrar números nos pontos", "Show numbers on points",
                   "Mostrar números en los puntos", "Afficher les numéros sur les points"),

    "comp.stacked": ("Barras empilhadas (qtd.)", "Stacked bars (count)", "Barras apiladas (cant.)", "Barres empilées (nb)"),
    "comp.percent": ("Barras empilhadas (%)", "Stacked bars (%)", "Barras apiladas (%)", "Barres empilées (%)"),
    "comp.donut": ("Rosca", "Donut", "Anillo", "Anneau"),
    "comp.count": ("Quantidade de dimensões", "Number of dimensions", "Cantidad de dimensiones", "Nombre de dimensions"),
    "comp.pct": ("% das dimensões", "% of dimensions", "% de las dimensiones", "% des dimensions"),
    "comp.dimensions": ("dimensões", "dimensions", "dimensiones", "dimensions"),

    # ── tabela ───────────────────────────────────────────────────────────
    "table.header": ("Tabela detalhada", "Detailed table", "Tabla detallada", "Tableau détaillé"),
    "table.MARK_LABEL": ("Nº", "No.", "N.º", "N°"),
    "table.ID_DIMENSION": ("ID_DIMENSION",) * 4,
    "table.EVENT_KEYWORD": ("Evento", "Event", "Evento", "Événement"),
    "table.DIM_LABEL": ("Dimensão", "Dimension", "Dimensión", "Dimension"),
    "table.PROB_DV_IV": ("Probabilidade", "Probability", "Probabilidad", "Probabilité"),
    "table.IMPACT": ("Impacto", "Impact", "Impacto", "Impact"),
    "table.TRUSTABILITY": ("Confiabilidade", "Reliability", "Confiabilidad", "Fiabilité"),
    "table.RISK_SCORE": ("Risk score",) * 4,
    "table.RISK_LABEL": ("Classificação", "Classification", "Clasificación", "Classification"),
    "table.download": ("Baixar tabela (.xlsx)", "Download table (.xlsx)", "Descargar tabla (.xlsx)", "Télécharger le tableau (.xlsx)"),

    # ── modelo .xlsx ─────────────────────────────────────────────────────
    "tpl.required": ("Obrigatória", "Required", "Obligatoria", "Obligatoire"),
    "tpl.optional": ("Opcional", "Optional", "Opcional", "Facultative"),
    "tpl.col_column": ("Coluna", "Column", "Columna", "Colonne"),
    "tpl.col_required": ("Obrigatoriedade", "Required?", "Obligatoriedad", "Caractère obligatoire"),
    "tpl.col_description": ("Descrição", "Description", "Descripción", "Description"),
    "tpl.range_error": (
        "Informe um valor entre {lo} e {hi}.", "Enter a value between {lo} and {hi}.",
        "Ingrese un valor entre {lo} y {hi}.", "Saisissez une valeur entre {lo} et {hi}.",
    ),
    "help.ID_DIMENSION": (
        "Identificador único da dimensão. Formato: EVT_AAAA_M_D_LETRA_NUM "
        "(ex.: EVT_2026_6_11_A_1) — LETRA agrupa dimensões do mesmo evento, "
        "NUM numera as dimensões dentro dele. O formato sem LETRA "
        "(EVT_AAAA_M_D_NUM) também é aceito: as dimensões da mesma data caem no mesmo evento.",
        "Unique identifier of the dimension. Format: EVT_YYYY_M_D_LETTER_NUM "
        "(e.g. EVT_2026_6_11_A_1) — LETTER groups dimensions of the same event, "
        "NUM numbers the dimensions within it. The format without LETTER "
        "(EVT_YYYY_M_D_NUM) is also accepted: dimensions with the same date fall into the same event.",
        "Identificador único de la dimensión. Formato: EVT_AAAA_M_D_LETRA_NUM "
        "(p. ej.: EVT_2026_6_11_A_1) — LETRA agrupa las dimensiones del mismo evento, "
        "NUM numera las dimensiones dentro de él. También se acepta el formato sin LETRA "
        "(EVT_AAAA_M_D_NUM): las dimensiones con la misma fecha caen en el mismo evento.",
        "Identifiant unique de la dimension. Format : EVT_AAAA_M_J_LETTRE_NUM "
        "(ex. : EVT_2026_6_11_A_1) — LETTRE regroupe les dimensions d'un même événement, "
        "NUM numérote les dimensions à l'intérieur. Le format sans LETTRE "
        "(EVT_AAAA_M_J_NUM) est aussi accepté : les dimensions de la même date forment le même événement.",
    ),
    "help.EVENT_KEYWORD": (
        "Nome/descrição do evento — repete o mesmo texto em todas as dimensões que pertencem a ele.",
        "Event name/description — repeat the same text on every dimension that belongs to it.",
        "Nombre/descripción del evento — repita el mismo texto en todas las dimensiones que le pertenecen.",
        "Nom/description de l'événement — répétez le même texte sur toutes les dimensions qui lui appartiennent.",
    ),
    "help.DIMENSION_KEYWORD": (
        "Nome da dimensão de risco avaliada (ex.: 'Ormuz', 'Política comercial', 'Cadeia de suprimentos'). "
        "É o nome que aparece na legenda \"número - dimensão\".",
        "Name of the risk dimension assessed (e.g. 'Hormuz', 'Trade policy', 'Supply chain'). "
        "It is the name shown in the \"number - dimension\" legend.",
        "Nombre de la dimensión de riesgo evaluada (p. ej.: 'Ormuz', 'Política comercial', 'Cadena de suministro'). "
        "Es el nombre que aparece en la leyenda \"número - dimensión\".",
        "Nom de la dimension de risque évaluée (ex. : 'Ormuz', 'Politique commerciale', 'Chaîne d'approvisionnement'). "
        "C'est le nom affiché dans la légende « numéro - dimension ».",
    ),
    "help.IMPACT": (
        "Impacto, de -1 (muito negativo) a +1 (muito positivo).",
        "Impact, from -1 (very negative) to +1 (very positive).",
        "Impacto, de -1 (muy negativo) a +1 (muy positivo).",
        "Impact, de -1 (très négatif) à +1 (très positif).",
    ),
    "help.PROB_DV_IV": (
        "Probabilidade condicional, de 0 a 1.", "Conditional probability, from 0 to 1.",
        "Probabilidad condicional, de 0 a 1.", "Probabilité conditionnelle, de 0 à 1.",
    ),
    "help.TRUSTABILITY": (
        "Confiabilidade da estimativa, de 0 a 1.", "Reliability of the estimate, from 0 to 1.",
        "Confiabilidad de la estimación, de 0 a 1.", "Fiabilité de l'estimation, de 0 à 1.",
    ),
    "help.RISK_SCORE": (
        "Se deixada em branco, é calculada automaticamente como PROB_DV_IV × IMPACT × TRUSTABILITY.",
        "If left blank, it is calculated automatically as PROB_DV_IV × IMPACT × TRUSTABILITY.",
        "Si se deja en blanco, se calcula automáticamente como PROB_DV_IV × IMPACT × TRUSTABILITY.",
        "Si elle est laissée vide, elle est calculée automatiquement : PROB_DV_IV × IMPACT × TRUSTABILITY.",
    ),
    "help.PROB_DV": (
        "Coluna de apoio/auditoria — não entra nos gráficos.",
        "Support/audit column — not used in the charts.",
        "Columna de apoyo/auditoría — no entra en los gráficos.",
        "Colonne d'appui/audit — n'entre pas dans les graphiques.",
    ),
    "help.IV_USED": (
        "Coluna de apoio/auditoria — não entra nos gráficos.",
        "Support/audit column — not used in the charts.",
        "Columna de apoyo/auditoría — no entra en los gráficos.",
        "Colonne d'appui/audit — n'entre pas dans les graphiques.",
    ),
    "help.PROB_VIT": (
        "Coluna de apoio/auditoria — não entra nos gráficos.",
        "Support/audit column — not used in the charts.",
        "Columna de apoyo/auditoría — no entra en los gráficos.",
        "Colonne d'appui/audit — n'entre pas dans les graphiques.",
    ),
}
