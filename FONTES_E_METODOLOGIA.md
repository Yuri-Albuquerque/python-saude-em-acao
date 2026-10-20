# Fontes, metodologia e rastreabilidade

## Dengue

- **Sistema:** SINAN — Sistema de Informação de Agravos de Notificação.
- **Acesso programático:** PySUS, origem `ftp.sinan` (parquet oficial do DATASUS). A origem `saude.arboviroses` (OpenDataSUS) devolve, para Goiás, uma amostra esparsa não representativa (98 registros espalhados por 1999–2026) e é rejeitada pela validação do script (< 1.000 notificações).
- **Unidade original:** notificação individual.
- **Saída do projeto:** contagem agregada por município de residência e semana epidemiológica aproximada pela semana iniciada no domingo.
- **Data preferida:** início dos sintomas (`DT_SIN_PRI`); na ausência, data de notificação (`DT_NOTIFIC`).
- **Território preferido:** município de residência (`ID_MN_RESI` ou equivalente); o script informa a coluna efetivamente utilizada.

## População

- **Fonte:** API de Agregados do IBGE/SIDRA, tabela 6579, variável 9324.
- **Uso:** denominador para incidência por 100 mil habitantes.
- **Atenção:** alinhar o ano da estimativa ao período epidemiológico.

## Renda, saneamento e vulnerabilidade (Censo 2022, API SIDRA)

Todos os indicadores abaixo são por município goiano e entram no `municipios_goias.csv`:

- **renda_pc** — rendimento nominal médio mensal domiciliar per capita (tabela 10295, variável 13431);
- **pct_agua_rede** — % de domicílios com ligação à rede geral de distribuição de água como forma principal (tabela 6803, categoria 72144);
- **pct_esgoto_rede** — % de domicílios com esgotamento sanitário ligado à rede geral/pluvial (tabela 6805, categoria 46290);
- **pct_lixo_coletado** — % de domicílios com lixo coletado direta ou indiretamente (tabela 6892, categoria 2520).

**Índice de vulnerabilidade** = média (25% cada) dos quatro componentes min–max sobre os 246 municípios, com renda e privações invertidas (menos renda/coveredura = mais vulnerável). Nada é imputado: município sem um indicador usa a média dos disponíveis. Procedência em `data/raw/metadados_ibge_renda.json`; demonstração computada no notebook 03 (Águas Lindas de Goiás: 0,89 só-renda → 0,35 multidimensional).

## Reprodutibilidade

Cada extração oficial gera um arquivo de metadados com ano, origem, data/hora de acesso, número de registros, colunas escolhidas e municípios encontrados (`data/processed/metadados_sinan.json`, `data/raw/metadados_ibge_renda.json`, `data/raw/metadados_ibge_populacao.json`). Arquivos individuais não são versionados. Somente agregados sem identificação poderão ser incluídos para a oficina. O projeto não usa dados sintéticos em nenhum ponto.

## Limitações

Notificações estão sujeitas a atraso, revisão, duplicidade, subnotificação e mudanças de definição. O índice de vulnerabilidade é sensível aos extremos do min–max e não inclui determinantes como densidade urbana, cobertura de APS ou clima. Associação territorial não estabelece causalidade. O material não produz prognóstico individual nem orientação clínica.