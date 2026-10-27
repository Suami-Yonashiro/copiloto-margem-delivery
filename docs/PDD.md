# Conciliação de repasses e decisão de promoções (AS-IS)
**PDD — Documento de Definição de Processo**

**Objetivo do processo:** garantir que o restaurante recebeu o que deveria em cada pedido e decidir quais promoções manter.
**Atores:** dono(a), gerente administrativo(a), gerente de operações e plataforma de delivery.
**Sistemas:** portal da plataforma, gestor de pedidos, PDV, planilha e extrato bancário.

| Nº | Etapa | Quem | Sistema | Frequência | Dor |
|---|---|---|---|---|---|
| 1 | Decide entrar em promoção ou campanha | Dono(a) | Portal da plataforma | Por campanha | Sem projeção da margem nem clareza de quem paga o desconto |
| 2 | Pedido entra pela plataforma e é lançado no PDV | Gerente de operações | Gestor de pedidos + PDV | A cada pedido | Lançamento manual com erros de digitação |
| 3 | Pedido é preparado e entregue | Operação | — | A cada pedido | Volume de promoção pressiona a cozinha |
| 4 | Cliente paga online ou na entrega | Cliente | App ou maquininha | A cada pedido | Meios de pagamento com regras diferentes |
| 5 | Fecha o caixa diário | Gerente de operações | PDV + planilha | Diária | Mistura de meios de pagamento |
| 6 | Analisa reclamações e reembolsos debitados | Operação + administrativo | Portal | Diária | Avaliar se o reembolso procede |
| 7 | Plataforma fecha o ciclo e desconta as cobranças | Plataforma | — | A cada 7 dias | Descontos pouco visíveis por pedido |
| 8 | Repasse cai na conta | Banco | Extrato bancário | Conforme o plano de repasse | Valor líquido difícil de ligar às vendas |
| 9 | Confere repasse × vendas | Gerente administrativo(a) | Extrato + planilha | Conforme o plano de repasse | Manual, cerca de 4 dias intercalados com outras atividades |
| 10 | Contesta divergências | Gerente administrativo(a) | Portal | Após a conferência | Prazo de 7 dias para contestar cancelamento pode já ter passado |
| 11 | Corrige a operação no prazo definido | Gerente de operações | — | Após a contestação | Correção chega tarde |

## Fluxo

```mermaid
flowchart TD
    subgraph DONO["<br/>Dono(a)"]
        E1["1. Decide entrar na promoção"]
    end
    subgraph OPS["<br/>Gerente de operações e equipe"]
        E2["2. Lança o pedido no PDV"]
        E3["3. Prepara e entrega"]
        E5["5. Fecha o caixa diário"]
        E11["11. Corrige a operação"]
    end
    subgraph CLI["<br/>Cliente"]
        E4["4. Paga online ou na entrega"]
    end
    subgraph PLAT["<br/>Plataforma e banco"]
        E7["7. Fecha o ciclo de 7 dias e desconta cobranças"]
        E8["8. Repasse cai na conta"]
    end
    subgraph ADM["<br/>Gerente administrativo(a)"]
        E6["6. Analisa reclamações e reembolsos"]
        E9["9. Confere repasse × vendas"]
        E10["10. Contesta divergências"]
    end
    E1 --> E2 --> E3 --> E4 --> E5
    E5 --> E6
    E4 --> E7 --> E8 --> E9
    E6 --> E9
    E9 -->|"divergência"| E10 --> E11
    E9 -->|"bateu"| FIM(["Fim do ciclo"])
    classDef dor fill:#fbebeb,stroke:#c0392b,color:#000
    class E1,E2,E5,E9,E10 dor
```