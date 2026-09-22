# Fontes, metodologia e rastreabilidade

## Dengue

- **Sistema:** SINAN — Sistema de Informação de Agravos de Notificação.
- **Acesso programático:** PySUS, origem `saude.arboviroses` (OpenDataSUS) ou `ftp.sinan` (catálogo do DATASUS).
- **Unidade original:** notificação individual.
- **Saída do projeto:** contagem agregada por município de residência e semana epidemiológica aproximada pela semana iniciada no domingo.
- **Data preferida:** início dos sintomas (`DT_SIN_PRI`); na ausência, data de notificação (`DT_NOTIFIC`).
- **Território preferido:** município de residência (`ID_MN_RESI` ou equivalente); o script informa a coluna efetivamente utilizada.

## População

- **Fonte:** API de Agregados do IBGE/SIDRA, tabela 6579, variável 9324.
- **Uso:** denominador para incidência por 100 mil habitantes.
- **Atenção:** alinhar o ano da estimativa ao período epidemiológico.

## Renda

A integração de renda será feita em etapa própria. Até lá, os arquivos oficiais deixam renda e vulnerabilidade ausentes; valores de demonstração não devem ser misturados com contagens oficiais.

## Reprodutibilidade

Cada extração oficial gera um arquivo de metadados com ano, origem, data/hora de acesso, número de registros, colunas escolhidas e municípios encontrados. Arquivos individuais não são versionados. Somente agregados sem identificação poderão ser incluídos para a oficina.

## Limitações

Notificações estão sujeitas a atraso, revisão, duplicidade, subnotificação e mudanças de definição. Associação territorial não estabelece causalidade. O material não produz prognóstico individual nem orientação clínica.
