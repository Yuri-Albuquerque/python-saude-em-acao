# Python em Ação: da Epidemia ao Planejamento em Saúde

**Investigação visual com dados de dengue, população, renda e saneamento**

Microcurso de 2 horas para a **V Semana Acadêmica de Saúde e Desenvolvimento (V SEASD) — UEG Itumbiara**, voltado a estudantes e docentes da área da Saúde e Economia.

> O objetivo: Mostrar como Python transforma dados públicos em evidências para vigilância epidemiológica, gestão e planejamento.

## Motivação

**Como identificar onde e quando a dengue pressiona mais o sistema de saúde — e como população e vulnerabilidade socioeconômica mudam a interpretação dos números?**

## Roteiro

| Tempo | Etapa | Notebook | Produto visual |
|---:|---|---|---|
| 0–15 min | Python, Jupyter | `00_abertura.ipynb` | DataFrame e série temporal |
| 15–45 min | Curva epidemiológica e surto | `01_curva_epidemiologica.ipynb` | média móvel e sinal de alerta |
| 45–80 min | Território, população e incidência | `02_territorio_e_incidencia.ipynb` | ranking e mapa interativo |
| 80–110 min | Renda, vulnerabilidade e prioridade | `03_vulnerabilidade_e_gestao.ipynb` | dispersão interativa, clusters e painel |
| 110–120 min | Síntese | todos | recomendações e limitações |

## Instalação

```bash
git clone https://github.com/Yuri-Albuquerque/python-saude-em-acao.git
cd python-saude-em-acao
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Também é possível usar `conda env create -f environment.yml`.

## Preparação dos dados (100% oficiais)

A oficina usa exclusivamente dados públicos: SINAN/DATASUS e IBGE/Censo 2022. Para reproduzir os agregados em `data/processed/`:

```bash
# 1) notificações de dengue: série semanal municipal de Goiás (parquet oficial do SINAN)
#    um arquivo por ano: data/processed/dengue_semanal_goias_<ano>.csv
python scripts/baixar_sinan_dengue.py --ano 2024 --origem ftp
python scripts/baixar_sinan_dengue.py --ano 2025 --origem ftp

# 2) população IBGE e cadastro municipal
python scripts/baixar_ibge_populacao.py --periodo 2024
python scripts/preparar_municipios.py

# 3) indicadores do Censo 2022 (SIDRA) e índice de vulnerabilidade composto
python scripts/baixar_ibge_renda.py

# 4) executar os notebooks ponta a ponta
jupyter lab
```

O script do SINAN valida a extração e recusa amostras esparsas (a origem `saude` do OpenDataSUS devolve uma amostra não representativa para Goiás; use `--origem ftp`). Sem os agregados, os notebooks interrompem com a instrução de download.

## Índice de vulnerabilidade

Composto por quatro componentes min–max (25% cada), todos do Censo 2022 via API SIDRA: renda domiciliar per capita (tabela 10295), % de domicílios com água da rede geral (t6803), % com esgoto ligado à rede (t6805) e % com lixo coletado (t6892). A fórmula, as fontes e um exemplo computado (Águas Lindas de Goiás, que passa de 0,89 no índice só-renda para 0,35 no multidimensional) estão no notebook 03 e em `data/raw/metadados_ibge_renda.json`.

## Estrutura

```text
notebooks/        narrativa da oficina em quatro atos
data/raw/         extrações oficiais locais, não versionadas
data/processed/   agregados municipais prontos para análise
scripts/          download, validação, agregação e carregamento
GUIA_DOCENTE.md   minutagem, mensagens e contingência
```

## Bibliotecas

`pandas`, `seaborn`, `matplotlib`, `plotly`, `geopandas`, `scikit-learn` e `PySUS`.

## Dados e ética

Todas as fontes são oficiais e agregadas: SINAN/DATASUS para notificações, IBGE/SIDRA para população, renda e saneamento. Nenhum registro individual é exportado ou versionado. Resultados agregados não demonstram causalidade nem orientam decisões clínicas individuais.

## Fluxo apresentado

**pergunta de gestão → dados → limpeza → indicador → visualização → priorização → decisão**

## Situação do projeto

Pipeline oficial completo e validado: os quatro notebooks executam ponta a ponta com SINAN/DATASUS 2024 (334.555 notificações, 246 municípios), população IBGE e indicadores do Censo 2022, com vulnerabilidade multidimensional auditável e gráficos interativos (Plotly) embutidos e exportados em HTML. Próxima etapa pendente: exportação HTML dos próprios notebooks.