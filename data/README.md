# Dados

| Pasta | Conteúdo | Versionamento |
|---|---|---|
| `demo/` | base sintética gerada por `gerar_dados_demo.py` | não necessária; reproduzível |
| `raw/` | arquivos obtidos das fontes oficiais | não versionada |
| `processed/` | agregados municipais preparados para os notebooks | somente após validação |

## Produtos esperados

- `processed/dengue_semanal_goias.csv`: `codigo_ibge`, `municipio`, `semana`, `casos`;
- `processed/municipios_goias.csv`: população e, quando disponíveis, coordenadas e indicadores socioeconômicos;
- `processed/metadados_sinan.json`: procedência e parâmetros da extração.

Nunca misture silenciosamente colunas sintéticas e oficiais. O carregador informa qual fonte foi escolhida. Consulte `FONTES_E_METODOLOGIA.md`.
