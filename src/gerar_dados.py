"""Gera os dados fictícios do projeto em data/raw.

Todos os valores são inventados. A semente fixa (SEMENTE) faz o resultado
ser sempre o mesmo: quem rodar o script obtém exatamente os mesmos dados.
"""

import tomllib
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PASTA_SAIDA = RAIZ / "data" / "raw"
SEMENTE = 42

with open(RAIZ / "config" / "plataforma.toml", "rb") as arquivo:
    CONFIG = tomllib.load(arquivo)

# Cardápio base: (id, nome, categoria, preço no salão, CMV em % do preço no salão)
PRATOS = [
    ("P01", "Frango grelhado com arroz e salada", "prato", 38.90, 0.30),
    ("P02", "Filé de tilápia com legumes", "prato", 46.90, 0.34),
    ("P03", "Estrogonofe de carne", "prato", 42.90, 0.33),
    ("P04", "Parmegiana de frango", "prato", 44.90, 0.31),
    ("P05", "Risoto de cogumelos", "prato", 49.90, 0.29),
    ("P06", "Feijoada individual", "prato", 39.90, 0.32),
    ("P07", "Salada caesar com frango", "prato", 34.90, 0.28),
    ("P08", "Hambúrguer artesanal com fritas", "lanche", 36.90, 0.35),
    ("P09", "Wrap de frango", "lanche", 29.90, 0.30),
    ("P10", "Porção de batata frita", "acompanhamento", 22.90, 0.22),
    ("P11", "Pudim de leite", "sobremesa", 14.90, 0.25),
    ("P12", "Brownie com sorvete", "sobremesa", 18.90, 0.30),
    ("P13", "Refrigerante lata", "bebida", 7.90, 0.45),
    ("P14", "Suco natural 500 ml", "bebida", 11.90, 0.35),
    ("P15", "Água mineral", "bebida", 5.90, 0.40),
]

# Kit de envio por pedido: (item, custo unitário em R$, quantidade por pedido)
# Sacola e lacre personalizados com a marca; a embalagem do prato já está no CMV.
KIT_ENVIO = [
    ("sacola kraft personalizada", 1.84, 1),  # 500 por R$ 919,90 (varejo, out/2026)
    ("lacre personalizado", 0.10, 2),  # estimativa
    ("kit talheres com guardanapo", 0.42, 1),  # caixa com 250 por R$ 105,30
    ("sachê de álcool em gel", 0.20, 1),  # estimativa
]

# Taxas da maquininha, usadas só nos pedidos pagos na entrega:
# (meio, bandeira, taxa em % do valor)
# Visa e Mastercard: médias da pesquisa Ipsos-Ipec para a ANR (jun-jul/2026).
# Elo e Amex: premissa do projeto, um pouco acima das demais.
TAXAS_MAQUININHA = [
    ("dinheiro", "-", 0.0),
    ("pix", "-", 0.0106),
    ("débito", "visa", 0.0177),
    ("débito", "mastercard", 0.0177),
    ("débito", "elo", 0.0199),
    ("crédito", "visa", 0.0362),
    ("crédito", "mastercard", 0.0362),
    ("crédito", "elo", 0.0389),
    ("crédito", "amex", 0.0429),
    ("vale-refeição", "-", 0.0618),
]


def preco_terminado_em_90(valor: float) -> float:
    """Arredonda para o preço 'de vitrine' terminado em ,90 mais próximo."""
    return round(np.round(valor - 0.90) + 0.90, 2)


def gerar_cardapio(rng: np.random.Generator) -> pd.DataFrame:
    """Cardápio com preço no salão, preço no app e CMV de cada item.

    O preço no app fica entre 10% e 20% acima do salão, com média perto de 15%.
    """
    cardapio = pd.DataFrame(
        PRATOS, columns=["item_id", "nome", "categoria", "preco_salao", "cmv_pct"]
    )
    acrescimo = rng.uniform(0.10, 0.20, size=len(cardapio))
    cardapio["preco_app"] = [
        preco_terminado_em_90(p * (1 + a))
        for p, a in zip(cardapio["preco_salao"], acrescimo)
    ]
    cardapio["cmv"] = (cardapio["preco_salao"] * cardapio["cmv_pct"]).round(2)
    cardapio["plataforma"] = CONFIG["plataforma"]["nome"]
    return cardapio[
        [
            "item_id",
            "nome",
            "categoria",
            "plataforma",
            "preco_salao",
            "preco_app",
            "cmv",
        ]
    ]


def gerar_kit_envio() -> pd.DataFrame:
    """Itens do kit que acompanha cada pedido e o custo total por pedido."""
    kit = pd.DataFrame(KIT_ENVIO, columns=["item", "custo_unitario", "qtd_por_pedido"])
    kit["custo_por_pedido"] = (kit["custo_unitario"] * kit["qtd_por_pedido"]).round(2)
    return kit


def gerar_taxas_maquininha() -> pd.DataFrame:
    """Taxa da maquininha por meio de pagamento e bandeira."""
    return pd.DataFrame(TAXAS_MAQUININHA, columns=["meio", "bandeira", "taxa"])


def main() -> None:
    rng = np.random.default_rng(SEMENTE)
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    cardapio = gerar_cardapio(rng)
    cardapio.to_csv(PASTA_SAIDA / "cardapio.csv", index=False)
    acrescimo_medio = (cardapio["preco_app"] / cardapio["preco_salao"] - 1).mean()
    print(f"cardapio.csv: {len(cardapio)} itens")
    print(f"Preço no app, em média, {acrescimo_medio:.1%} acima do salão")

    kit = gerar_kit_envio()
    kit.to_csv(PASTA_SAIDA / "kit_envio.csv", index=False)
    print(
        f"kit_envio.csv: {len(kit)} itens, R$ {kit['custo_por_pedido'].sum():.2f} por pedido"
    )

    taxas = gerar_taxas_maquininha()
    taxas.to_csv(PASTA_SAIDA / "taxas_maquininha.csv", index=False)
    print(f"taxas_maquininha.csv: {len(taxas)} combinações de meio e bandeira")


if __name__ == "__main__":
    main()
