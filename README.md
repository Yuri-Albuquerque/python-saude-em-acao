# Python em Ação: da Epidemia ao Planejamento em Saúde

**Uma investigação visual com dados de dengue, população e renda**

Microcurso de 2 horas para a **Semana Acadêmica de Saúde e Desenvolvimento — UEG Itumbiara**, voltado a estudantes e docentes de Medicina e Economia.

> O objetivo não é ensinar toda a linguagem Python. É mostrar como Python transforma dados públicos em evidências para vigilância epidemiológica, gestão e planejamento.

## Pergunta condutora

**Como identificar onde e quando a dengue pressiona mais o sistema de saúde — e como população e vulnerabilidade socioeconômica mudam a interpretação dos números?**

## Roteiro

| Tempo | Etapa | Notebook | Produto visual |
|---:|---|---|---|
| 0–15 min | Python, Jupyter e pergunta de gestão | `00_abertura.ipynb` | DataFrame e série temporal |
| 15–45 min | Curva epidemiológica e surto | `01_curva_epidemiologica.ipynb` | média móvel e sinal de alerta |
| 45–80 min | Território, população e incidência | `02_territorio_e_incidencia.ipynb` | ranking e mapa interativo |
| 80–110 min | Renda, vulnerabilidade e prioridade | `03_vulnerabilidade_e_gestao.ipynb` | correlação, clusters e painel |
| 110–120 min | Síntese | todos | recomendações e limitações |

## Instalação

```bash
git clone https://github.com/Yuri-Albuquerque/python-saude-em-acao.git
cd python-saude-em-acao
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/gerar_dados_demo.py
jupyter lab
```

Também é possível usar `conda env create -f environment.yml`.

## Preparação dos dados oficiais

A oficina permanece funcional offline com a base demo. Para preparar dados oficiais agregados:

```bash
# conferir disponibilidade sem baixar
python scripts/baixar_sinan_dengue.py --ano 2024 --origem saude --listar

# baixar notificações e gerar série semanal municipal de Goiás
python scripts/baixar_sinan_dengue.py --ano 2024 --origem saude

# obter denominadores populacionais e preparar cadastro municipal
python scripts/baixar_ibge_populacao.py --periodo 2024
python scripts/preparar_municipios.py
```

Se a origem OpenDataSUS não contiver o ano desejado, use `--origem ftp`. Consulte `FONTES_E_METODOLOGIA.md` e `CHECKLIST_DADOS.md` antes de interpretar os resultados.

## Estrutura

```text
notebooks/        narrativa da oficina em quatro atos
data/demo/        base sintética reproduzível
data/raw/         extrações oficiais locais, não versionadas
data/processed/   agregados municipais prontos para análise
scripts/          download, validação, agregação e carregamento
GUIA_DOCENTE.md   minutagem, mensagens e contingência
```

## Bibliotecas

`pandas`, `seaborn`, `matplotlib`, `plotly`, `geopandas`, `scikit-learn` e `PySUS`.

## Dados e ética

A base de contingência é **sintética, agregada e identificada como demonstração**. O fluxo oficial usa SINAN/DATASUS para notificações e IBGE/SIDRA para população. Nenhum registro individual deve ser versionado. Resultados agregados não demonstram causalidade nem orientam decisões clínicas individuais.

## Fluxo apresentado

**pergunta de gestão → dados → limpeza → indicador → visualização → priorização → decisão**

## Situação do projeto

A infraestrutura para extração e rastreabilidade de dados oficiais está implementada. A renda oficial e a execução integral/exportação HTML dos notebooks constituem as próximas etapas.
