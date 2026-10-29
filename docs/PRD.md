# Copiloto de Margem do Parceiro
**PRD — Documento de Requisitos do Produto**

## 1. Problema (resumo executivo)
Hoje, donos, gerentes e operadores de restaurantes parceiros de apps de delivery operam no escuro: as vendas no marketplace passam por um emaranhado de comissões, taxas de transação, frete, cancelamentos, descontos de promoções sem clareza de quem paga, e o valor líquido só é depositado dias ou semanas depois.

O gestor só descobre que o repasse veio menor do que o esperado no fechamento do mês, quando o prazo de contestação pode ter finalizado e não há tempo nem dados estruturados para auditar as divergências.

Sem essa visibilidade a tempo, o restaurante vende em alto volume na ilusão de ter lucro, reforça a operação para atender a demanda, mas perde caixa com margens corroídas e divergências não contestadas.

## 2. Para quem
No restaurante, as decisões sobre o delivery envolvem três papéis, cada um com uma pergunta diferente:

| Papel | Pergunta | Decisão |
|---|---|---|
| Dono(a) | Vale a pena estar nesta promoção? | Mantém, ajusta ou encerra campanhas, pesando margem e posicionamento da marca |
| Gerente administrativo(a) | Recebi tudo o que deveria? | Confere repasses e descontos, abre contestações com prazo para a correção e avalia se o custo de receber mais rápido compensa |
| Gerente de operações | O que preciso corrigir e até quando? | Resolve as pendências apontadas, ajusta a operação dentro do prazo definido, sob acompanhamento do dono |

O copiloto mostra a margem e as divergências, mas a decisão final considera fatores que não estão nos dados, como a qualidade do produto e o posicionamento da marca. Por isso, toda ação passa por aprovação humana.

## 3. Objetivos
1. Apontar divergências de repasse em até 1 dia após o pagamento, classificadas pela causa.
2. Mostrar a margem de contribuição real de cada pedido e de cada promoção, considerando todas as taxas e o kit de envio.
3. Dizer se uma promoção aumenta a margem total, com estatística calculada pelo código, antes de decidir repeti-la.
4. Entregar um resumo semanal de uma página com até 3 recomendações, ordenadas pelo impacto em R$.
5. Encontrar 100% das divergências plantadas nos dados fictícios, com a causa correta.

## 4. Escopo da V1
- Um restaurante fictício (Restaurante Exemplo) em uma plataforma fictícia, com dados gerados por código
- Duas fontes de dados que não conversam: vendas do PDV e extrato de repasse da plataforma
- Cobranças da plataforma: comissão, taxa de transação, mensalidade, taxa do plano de repasse e retenção de IRRF
- Meios de pagamento online e na entrega, com entregador da plataforma ou próprio
- Cancelamentos, reembolsos e reclamações, com motivo e responsável (restaurante ou plataforma)
- Custos do restaurante: CMV por prato e kit de envio (sacola, lacres, talheres, guardanapo e sachê de álcool em gel)
- Conciliação pedido a pedido, com a causa de cada divergência
- Um teste A/B: desconto × frete grátis
- Dois agentes de IA (Conciliador e Analista), com aprovação humana
- Painel com KPIs e resumo semanal

## 5. Fora de escopo
- Dados reais ou conexão com plataformas reais
- Contestação automática: o copiloto prepara a contestação, e a pessoa decide e envia
- Reajuste de preços pela inflação dos insumos (na V1, o CMV fica fixo por período) → V2
- Mais de uma plataforma e comparação entre canais → V2 (o campo já existe nos dados)
- Agente de Experimentos e ciclo PDCA completo entre os agentes → V2
- Mais de um restaurante
- Leitura automática do texto das reclamações com IA → V2

## 6. Métricas de sucesso
- O prazo de detecção das divergências cai de semanas (fluxo atual) para até 1 dia após o repasse
- O conciliador encontra 100% das divergências plantadas, com a causa correta, e não aponta divergência falsa nos pedidos pagos na entrega
- A margem calculada pelo código bate com o cálculo manual de uma amostra de 20 pedidos
- Cada recomendação do resumo semanal traz o valor em R$ e o dado que a sustenta
- Os KPIs do restaurante estão definidos em [KPIs.md](KPIs.md)

## 7. Premissas e riscos
**Premissas**
- Os dados são fictícios, inspirados no funcionamento do mercado; os percentuais não são oficiais de nenhuma plataforma
- As regras de cobrança são simplificadas e o CMV fica fixo por período

**Riscos e como são tratados**
| Risco | Tratamento |
|---|---|
| A IA errar ou inventar números | Todo cálculo é feito pelo código; a IA só interpreta e é avaliada com testes (Módulo 13) |
| Decidir promoção só pela margem e prejudicar a marca | Taxa de reclamações como métrica de proteção e aprovação humana antes de qualquer ação |
| As regras da plataforma mudarem | Taxas e regras ficam em um arquivo de configuração, não espalhadas no código |
| Os dados fictícios não refletirem a realidade | Regras validadas com a vivência de operação de restaurante e premissas documentadas |