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


def main() -> None:
    rng = np.random.default_rng(SEMENTE)
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    cardapio = gerar_cardapio(rng)
    cardapio.to_csv(PASTA_SAIDA / "cardapio.csv", index=False)

    acrescimo_medio = (cardapio["preco_app"] / cardapio["preco_salao"] - 1).mean()
    print(f"cardapio.csv: {len(cardapio)} itens")
    print(f"Preço no app, em média, {acrescimo_medio:.1%} acima do salão")


if __name__ == "__main__":
    main()
