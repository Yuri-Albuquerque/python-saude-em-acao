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

## Estrutura

```text
notebooks/       narrativa da oficina em quatro atos
data/demo/       base sintética gerada localmente
data/raw/        arquivos oficiais locais (não versionados)
scripts/         geração demo e exemplo de acesso ao IBGE
GUIA_DOCENTE.md  minutagem, mensagens e contingência
```

## Bibliotecas

`pandas`, `seaborn`, `matplotlib`, `plotly`, `geopandas` e `scikit-learn`.

## Dados e ética

A primeira versão usa dados **sintéticos, agregados e identificados como demonstração**, garantindo funcionamento offline e evitando qualquer dado pessoal. Para análises reais, a estrutura prevê:

- SINAN/DATASUS para notificações de dengue;
- IBGE/SIDRA para população e indicadores socioeconômicos;
- Ministério da Saúde para monitoramento de arboviroses.

Resultados agregados não demonstram causalidade e não devem orientar decisões clínicas individuais.

## Fluxo apresentado

**pergunta de gestão → dados → limpeza → indicador → visualização → priorização → decisão**

## Situação do projeto

Versão inicial em desenvolvimento. Antes do evento, serão incorporadas extrações oficiais auditáveis e uma versão de contingência em HTML.
