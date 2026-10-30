# KPIs — Copiloto de Margem do Parceiro

Indicadores que o copiloto calcula e acompanha. Cada KPI tem fórmula, tipo, frequência e meta.

- **Principal:** o que o projeto quer melhorar.
- **Diagnóstico:** explica por que a principal subiu ou caiu.
- **Proteção:** não pode piorar enquanto a principal melhora.

"Linha de base" significa que a meta será definida depois da primeira medição com os dados (Módulo 3).

## Métrica principal
| KPI | Fórmula | Frequência | Meta |
|---|---|---|---|
| Margem de contribuição por pedido (R$) | Ver "Como calcular a margem" | Semanal | Linha de base |
| Margem de contribuição (%) | Margem de contribuição ÷ valor de venda | Semanal | Linha de base |

### Como calcular a margem
```
Valor de venda do pedido (preço no app)
− Desconto da promoção pago pelo restaurante
− Comissão da plataforma
− Taxa de pagamento:
    online → taxa de transação da plataforma
    na entrega → taxa da maquininha, por bandeira e modalidade
− Taxa do plano de repasse
− Frete pago pelo restaurante (quando houver)
− CMV
− Kit de envio: sacola, lacres, talheres, guardanapo, sachê de álcool em gel
− Custo de recuperação: brinde ou frete dado como desculpa por um erro
= Margem de contribuição (R$)
```

Ficam fora da margem do pedido: a mensalidade da plataforma (custo fixo, entra só no custo efetivo da plataforma) e o IRRF retido (imposto antecipado, não é custo).

## Diagnóstico
| KPI | Fórmula | Frequência | Meta |
|---|---|---|---|
| Taxa de divergência de repasse | Pedidos com diferença acima de R$ 0,01 entre o recebido e o esperado ÷ pedidos com repasse | Diária | Abaixo de 2% |
| Valor a recuperar (R$) | Soma de (esperado − recebido) nos pedidos pagos a menor e ainda dentro do prazo de contestação | Diária | Zerar a cada ciclo |
| Valor perdido por prazo (R$) | Soma das divergências não contestadas dentro do prazo | Mensal | R$ 0 |
| Custo efetivo da plataforma (%) | (Comissão + taxa de transação + taxa do plano de repasse + mensalidade) ÷ valor de venda | Mensal | Linha de base |
| Custo das promoções pago pelo restaurante (R$) | Soma dos descontos bancados pelo restaurante | Por campanha | Linha de base |
| Diferença de margem delivery × salão (p.p.) | Margem (%) do prato no delivery − margem (%) do mesmo prato no salão | Mensal | Linha de base |
| Ticket médio (R$) | Valor de venda ÷ número de pedidos | Semanal | — |

## Proteção
| KPI | Fórmula | Frequência | Meta |
|---|---|---|---|
| Taxa de reclamações | Pedidos com reclamação ÷ total de pedidos | Semanal | Não subir durante promoções |
| Taxa de cancelamento | Pedidos cancelados ÷ total de pedidos | Semanal | Não subir durante promoções |
| Custo de recuperação (R$) | Soma de brindes e fretes dados como desculpa por erro | Semanal | Não subir |

## Fontes dos dados (geradas no Módulo 2)
- **Pedidos (PDV):** valor de venda, itens, meio de pagamento, status, reclamações
- **Extrato da plataforma:** comissão, taxas, promoções, valor esperado e recebido, data do repasse
- **Cardápio:** preço no app, preço no salão e CMV de cada prato
- **Custos do restaurante:** kit de envio e taxas da maquininha por bandeira e modalidade