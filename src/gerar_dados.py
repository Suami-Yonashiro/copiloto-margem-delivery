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
DATA_INICIO = "2026-07-01"
DATA_FIM = "2026-09-30"
PEDIDOS_POR_DIA = 55  # média de segunda a quinta; sexta a domingo vende 30% mais

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


def sortear_horario(rng: np.random.Generator, dia: pd.Timestamp) -> pd.Timestamp:
    """Horário do pedido: pico do almoço (55%) ou do jantar (45%)."""
    if rng.random() < 0.55:
        hora = rng.normal(12.5, 0.8)
    else:
        hora = rng.normal(20.0, 1.1)
    hora = float(np.clip(hora, 10.5, 23.5))
    return dia + pd.Timedelta(hours=hora)


def gerar_pedidos_pdv(
    rng: np.random.Generator, cardapio: pd.DataFrame, taxas: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pedidos registrados no PDV do restaurante e os itens de cada pedido.

    O PDV é a fonte do restaurante: aqui não há erros plantados. Os erros
    entram depois, no extrato da plataforma.
    """
    # Pratos e lanches saem mais que bebidas, sobremesas e acompanhamentos
    peso_categoria = {
        "prato": 5,
        "lanche": 3,
        "acompanhamento": 1,
        "sobremesa": 1,
        "bebida": 2,
    }
    pesos_itens = cardapio["categoria"].map(peso_categoria).to_numpy(dtype=float)
    pesos_itens = pesos_itens / pesos_itens.sum()

    # Meios de pagamento na entrega (pix e cartões são os mais usados)
    peso_meio = {"dinheiro": 1, "pix": 3, "débito": 2, "crédito": 2, "vale-refeição": 1}
    contagem_meio = taxas["meio"].map(taxas["meio"].value_counts())
    pesos_meios = (taxas["meio"].map(peso_meio) / contagem_meio).to_numpy(dtype=float)
    pesos_meios = pesos_meios / pesos_meios.sum()

    pedidos, itens = [], []
    numero = 0
    for dia in pd.date_range(DATA_INICIO, DATA_FIM, freq="D"):
        fator = 1.3 if dia.dayofweek >= 4 else 1.0  # sexta, sábado e domingo
        for _ in range(rng.poisson(PEDIDOS_POR_DIA * fator)):
            numero += 1
            pedido_id = f"PDV{numero:06d}"
            data_hora = sortear_horario(rng, dia)

            # Entrega: pela plataforma (70%) ou pelo entregador do restaurante (30%)
            modelo = rng.choice(["plataforma", "propria"], p=[0.7, 0.3])

            # Pagamento na entrega só existe com entregador próprio
            if modelo == "propria" and rng.random() < 0.4:
                forma = "entrega"
                linha = taxas.iloc[rng.choice(len(taxas), p=pesos_meios)]
                meio, bandeira = linha["meio"], linha["bandeira"]
            else:
                forma, meio, bandeira = "online", "online", "-"

            # Itens do pedido
            qtd_itens = rng.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
            escolhidos = rng.choice(
                len(cardapio), size=qtd_itens, replace=False, p=pesos_itens
            )
            valor_itens = 0.0
            for i in escolhidos:
                qtd = int(rng.choice([1, 2], p=[0.9, 0.1]))
                preco = float(cardapio.iloc[i]["preco_app"])
                itens.append(
                    {
                        "pedido_id": pedido_id,
                        "item_id": cardapio.iloc[i]["item_id"],
                        "quantidade": qtd,
                        "preco_unitario": preco,
                    }
                )
                valor_itens += qtd * preco

            # Frete cobrado do cliente: só na entrega própria fica com o restaurante
            frete = (
                float(rng.choice([5.99, 6.99, 7.99])) if modelo == "propria" else 0.0
            )

            # Promoções: 18% dos pedidos
            tipo_promo, valor_promo, custeado_por = "nenhuma", 0.0, "-"
            if rng.random() < 0.18:
                tipo_promo = rng.choice(
                    ["cupom_loja", "cupom_plataforma", "frete_gratis"],
                    p=[0.4, 0.3, 0.3],
                )
                if tipo_promo == "frete_gratis":
                    valor_promo = frete if frete > 0 else 6.99  # a loja banca o frete
                    frete = 0.0
                    custeado_por = "loja"
                else:
                    valor_promo = round(min(valor_itens * 0.10, 15.0), 2)
                    custeado_por = (
                        "loja" if tipo_promo == "cupom_loja" else "plataforma"
                    )

            desconto_cliente = valor_promo if tipo_promo.startswith("cupom") else 0.0
            total_cliente = round(valor_itens + frete - desconto_cliente, 2)

            # Cancelamentos: 4% dos pedidos, entre 5 e 40 minutos depois
            status, cancelado_por, data_cancelamento = "concluido", "-", pd.NaT
            if rng.random() < 0.04:
                status = "cancelado"
                cancelado_por = rng.choice(
                    ["cliente", "loja", "plataforma"], p=[0.5, 0.3, 0.2]
                )
                data_cancelamento = data_hora + pd.Timedelta(
                    minutes=int(rng.integers(5, 41))
                )

            # Custo de recuperação: brinde ou frete por erro em 2% dos pedidos concluídos
            recuperacao = 0.0
            if status == "concluido" and rng.random() < 0.02:
                recuperacao = float(rng.choice([6.00, 8.00, 12.00]))

            pedidos.append(
                {
                    "pedido_id": pedido_id,
                    "plataforma": CONFIG["plataforma"]["nome"],
                    "data_hora_pedido": data_hora.floor("min"),
                    "modelo_entrega": modelo,
                    "forma_pagamento": forma,
                    "meio_pagamento": meio,
                    "bandeira": bandeira,
                    "valor_itens": round(valor_itens, 2),
                    "frete_cliente": frete,
                    "tipo_promocao": tipo_promo,
                    "valor_promocao": valor_promo,
                    "custeado_por": custeado_por,
                    "total_cliente": total_cliente,
                    "status": status,
                    "cancelado_por": cancelado_por,
                    "data_hora_cancelamento": data_cancelamento,
                    "custo_recuperacao": recuperacao,
                }
            )

    pedidos = pd.DataFrame(pedidos)
    itens = pd.DataFrame(itens)
    pedidos["data_hora_cancelamento"] = pedidos["data_hora_cancelamento"].dt.floor(
        "min"
    )

    # Renumera em ordem cronológica, como um PDV de verdade faria
    pedidos = pedidos.sort_values("data_hora_pedido", kind="stable").reset_index(
        drop=True
    )
    novo_id = {
        antigo: f"PDV{i:06d}" for i, antigo in enumerate(pedidos["pedido_id"], start=1)
    }
    pedidos["pedido_id"] = pedidos["pedido_id"].map(novo_id)
    itens["pedido_id"] = itens["pedido_id"].map(novo_id)
    itens = itens.sort_values("pedido_id", kind="stable").reset_index(drop=True)
    return pedidos, itens


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

    pedidos, itens = gerar_pedidos_pdv(rng, cardapio, taxas)
    pedidos.to_csv(PASTA_SAIDA / "pdv_pedidos.csv", index=False)
    itens.to_csv(PASTA_SAIDA / "pdv_itens.csv", index=False)
    print(f"pdv_pedidos.csv: {len(pedidos)} pedidos de {DATA_INICIO} a {DATA_FIM}")
    print(f"pdv_itens.csv: {len(itens)} linhas de itens")
    print(f"Ticket médio: R$ {pedidos['total_cliente'].mean():.2f}")


if __name__ == "__main__":
    main()
