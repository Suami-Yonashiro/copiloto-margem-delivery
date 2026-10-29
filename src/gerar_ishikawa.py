"""Gera o diagrama de Ishikawa (espinha de peixe) em docs/img/ishikawa.svg.

Para mudar uma causa, edite o dicionário CATEGORIAS e rode:
    python src/gerar_ishikawa.py
"""

import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

SAIDA = Path(__file__).resolve().parent.parent / "docs" / "img" / "ishikawa.svg"

EFEITO = ["Repasse divergente", "descoberto tarde, com", "margem corroída"]
CATEGORIAS = {
    "Método": [
        "Conferência segue o repasse, não o prazo de contestação",
        "Promoção sem projeção de margem nem de quem paga o desconto",
        "Ficha técnica sem o kit de envio",
    ],
    "Sistemas": [
        "PDV não conversa com o gestor de pedidos; lançamento manual",
        "Extrato sem detalhe que bata com o PDV",
    ],
    "Pessoas": [
        "Sem tempo para conferir pedido a pedido (cerca de 4 dias)",
        "Erros de digitação ou falta de preenchimento nos lançamentos",
        "Regras conhecidas só por quem confere, sem documentação",
    ],
    "Dados": [
        "Repasse líquido, sem mostrar quem pagou a promoção",
        "Cobrança ou comissão diferente da contratada",
        "Reembolso debitado sem ser responsabilidade do restaurante",
        "Meios de pagamento com regras diferentes misturados",
    ],
    "Medição": [
        "Margem real do pedido e da promoção não calculada",
        "Sem indicador de divergência nem de valor perdido por prazo",
    ],
    "Ambiente": [
        "Inflação muda o CMV mais rápido que o preço no app (fora da V1)",
        "Pressão por resultados empurra para campanhas de volume",
        "Prazo de contestação curto, definido pela plataforma",
    ],
}

L, A = 1720, 860  # largura e altura
ESPINHA_Y = A / 2
ESPINHA_X0, ESPINHA_X1 = 70, 1390
TOPO_Y, BASE_Y = 95, A - 95  # altura das caixas de categoria
X_OSSOS = [580, 1010, 1390 - 40]  # onde cada osso encontra a espinha
DESLOCAMENTO = 300  # quanto o osso "anda" para a esquerda
FONTE = "Arial, Helvetica, sans-serif"
COR_LINHA, COR_TEXTO = "#3a3a3a", "#1f1f1f"


def quebrar(texto):
    """Quebra em até 2 linhas equilibradas, sem deixar palavra solta."""
    for largura in range(len(texto) // 2, 40):
        linhas = textwrap.wrap(texto, largura)
        if len(linhas) <= 2:
            return linhas
    return textwrap.wrap(texto, 40)


partes = [
    (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{A}" '
        f'viewBox="0 0 {L} {A}" font-family="{FONTE}">'
    ),
    f'<rect width="{L}" height="{A}" fill="#ffffff"/>',
    (
        '<defs><marker id="seta" markerWidth="12" markerHeight="12" refX="10" refY="6" '
        'orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#3a3a3a"/></marker></defs>'
    ),
    (
        f'<line x1="{ESPINHA_X0}" y1="{ESPINHA_Y}" x2="{ESPINHA_X1}" y2="{ESPINHA_Y}" '
        f'stroke="{COR_LINHA}" stroke-width="4" marker-end="url(#seta)"/>'
    ),
]

# Cabeça do peixe (efeito)
cx, cw, ch = ESPINHA_X1 + 14, 270, 150
partes.append(
    f'<rect x="{cx}" y="{ESPINHA_Y - ch / 2}" width="{cw}" height="{ch}" rx="18" '
    'fill="#fbebeb" stroke="#c0392b" stroke-width="2.5"/>'
)
partes.append(
    f'<text x="{cx + cw / 2}" y="{ESPINHA_Y - 38}" text-anchor="middle" '
    f'font-size="15" font-weight="bold" fill="#c0392b" letter-spacing="2">EFEITO</text>'
)
for i, linha in enumerate(EFEITO):
    partes.append(
        f'<text x="{cx + cw / 2}" y="{ESPINHA_Y - 6 + i * 24}" text-anchor="middle" '
        f'font-size="19" font-weight="bold" fill="{COR_TEXTO}">{escape(linha)}</text>'
    )

nomes = list(CATEGORIAS)
for idx, nome in enumerate(nomes):
    em_cima = idx < 3
    x_espinha = X_OSSOS[idx % 3]
    y_cat = TOPO_Y if em_cima else BASE_Y
    x_cat = x_espinha - DESLOCAMENTO
    # osso
    partes.append(
        f'<line x1="{x_cat}" y1="{y_cat}" x2="{x_espinha}" y2="{ESPINHA_Y}" '
        f'stroke="{COR_LINHA}" stroke-width="2.5"/>'
    )
    # caixa da categoria
    bw, bh = 150, 40
    by = y_cat - bh if em_cima else y_cat
    partes.append(
        f'<rect x="{x_cat - bw / 2}" y="{by}" width="{bw}" height="{bh}" rx="6" '
        f'fill="#f0efec" stroke="#555" stroke-width="1.5"/>'
    )
    partes.append(
        f'<text x="{x_cat}" y="{by + 26}" text-anchor="middle" font-size="18" '
        f'font-weight="bold" fill="{COR_TEXTO}">{escape(nome)}</text>'
    )
    # causas: espinhas horizontais ao longo do osso
    causas = CATEGORIAS[nome]
    n = len(causas)
    for j, causa in enumerate(causas):
        t = 0.16 + (0.78 - 0.16) * (j / (n - 1) if n > 1 else 0.5)
        px = x_cat + t * (x_espinha - x_cat)
        py = y_cat + t * (ESPINHA_Y - y_cat)
        partes.append(
            f'<line x1="{px - 34}" y1="{py}" x2="{px}" y2="{py}" '
            f'stroke="{COR_LINHA}" stroke-width="1.5"/>'
        )
        linhas = quebrar(causa)
        base = py - (len(linhas) - 1) * 8.5 + 5
        for k, linha in enumerate(linhas):
            partes.append(
                f'<text x="{px - 42}" y="{base + k * 17}" text-anchor="end" '
                f'font-size="14" fill="{COR_TEXTO}">{escape(linha)}</text>'
            )

partes.append("</svg>")
SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text("\n".join(partes), encoding="utf-8")
print(f"Diagrama gerado em {SAIDA}")
