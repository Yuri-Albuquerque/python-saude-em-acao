# Dados

| Pasta | Conteúdo | Versionamento |
|---|---|---|
| `raw/` | arquivos obtidos das fontes oficiais | não versionada |
| `processed/` | agregados municipais preparados para os notebooks | somente após validação |

O projeto usa exclusivamente dados oficiais — não existe base sintética. Os notebooks exigem os agregados em `processed/`; sem eles, `scripts/carregar_dados.py` interrompe com instrução de download.

## Produtos

- `processed/dengue_semanal_goias.csv`: `codigo_ibge`, `municipio`, `semana`, `casos` (SINAN/DATASUS via PySUS, parquet oficial; a origem `saude` do OpenDataSUS retorna amostra esparsa e é rejeitada);
- `processed/municipios_goias.csv`: população IBGE, coordenadas e indicadores do Censo 2022: renda domiciliar per capita (t10295), % água de rede (t6803), % esgoto de rede (t6805), % lixo coletado (t6892), e o índice de vulnerabilidade composto;
- `processed/metadados_sinan.json` e `raw/metadados_ibge_renda.json`: procedência e parâmetros de cada extração.

Reprodução completa:

```bash
python scripts/baixar_sinan_dengue.py --ano 2024 --origem ftp
python scripts/baixar_ibge_populacao.py --periodo 2024
python scripts/preparar_municipios.py
python scripts/baixar_ibge_renda.py
```

Consulte `FONTES_E_METODOLOGIA.md` antes de interpretar os resultados.