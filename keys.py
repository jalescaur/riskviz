# keys.py — chaves estáveis para widgets do Streamlit
#
# Sem `key`, o Streamlit identifica o widget pelo rótulo; como os rótulos são
# traduzidos, trocar de idioma resetaria filtros, upload e opções. Com `key`
# fixa o estado sobrevive à troca. Para widgets cujas opções vêm dos dados
# (eventos, dimensões), a chave inclui um hash das opções: ao carregar outro
# arquivo a seleção volta ao padrão em vez de apontar para opções inexistentes.

import hashlib


def options_key(prefix: str, options) -> str:
    digest = hashlib.md5("|".join(map(str, options)).encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{digest}"
