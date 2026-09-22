"""Exemplo de consumo da API de Agregados do IBGE/SIDRA.
Revise tabela, variável e período antes de uso analítico real.
"""
from pathlib import Path
import requests
import pandas as pd
URL="https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/-1/variaveis/9324?localidades=N6[N3[52]]"
resp=requests.get(URL,timeout=60); resp.raise_for_status()
data=resp.json()[0]["resultados"][0]["series"]
rows=[{"municipio":s["localidade"]["nome"],"codigo_ibge":s["localidade"]["id"],"populacao":next(iter(s["serie"].values()))} for s in data]
out=Path(__file__).resolve().parents[1]/"data"/"raw"; out.mkdir(parents=True,exist_ok=True)
pd.DataFrame(rows).to_csv(out/"populacao_goias_ibge.csv",index=False)
print("Arquivo salvo. Registre a data de acesso e confira os metadados da tabela 6579.")
