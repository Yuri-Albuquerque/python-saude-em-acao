# Evidências de validação

Validação realizada em 22/09/2026 em ambiente temporário, a partir da branch `feat/dados-oficiais-sinan-ibge`.

## Resultados

- compilação sintática de todos os scripts: **aprovada**;
- geração determinística da base demo: **aprovada**;
- execução sequencial de todas as células dos quatro notebooks: **aprovada**;
- carregamento automático da base demo quando não há agregados oficiais: **aprovado**;
- carregamento do esquema oficial simulado nos notebooks 00, 01 e 02: **aprovado**;
- cruzamento territorial por código IBGE padronizado em sete dígitos: **aprovado**;
- consulta SIDRA/IBGE, tabela 6579 e período 2024: **246 municípios**, sem duplicatas ou população ausente;
- Itumbiara: código IBGE `5211503`, localizada corretamente;
- listagem PySUS/SINAN 2024 via fallback FTP: `DENGBR24.parquet` localizado.

## Ocorrências corrigidas durante o teste

1. inclusão do `Jinja2`, necessário ao `pandas.DataFrame.style`;
2. remoção do sufixo ` - GO` dos nomes retornados pelo SIDRA;
3. padronização de códigos IBGE como texto com sete dígitos;
4. fallback automático de OpenDataSUS para FTP;
5. inclusão de identificadores nas células Jupyter.

## Limitação do ambiente

A execução com kernel Jupyter foi bloqueada pela política de sockets locais do contêiner de validação. Como alternativa, cada célula foi executada sequencialmente no mesmo processo Python, preservando o estado. A exportação HTML deve ser repetida em um ambiente Jupyter convencional antes do evento.

A base nacional de notificações não foi baixada durante esta validação; somente sua disponibilidade foi consultada. Isso evita transferir milhões de registros antes da escolha definitiva do ano e da revisão dos parâmetros.
