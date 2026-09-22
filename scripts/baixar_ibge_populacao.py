"""Baixa a população estimada dos municípios de Goiás pela API SIDRA/IBGE."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import requests
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument("--periodo",default="-1",help="Ano SIDRA ou -1 para o último disponível")
a=p.parse_args()
url=f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{a.periodo}/variaveis/9324?localidades=N6[N3[52]]"
r=requests.get(url,timeout=60); r.raise_for_status(); payload=r.json()
series=payload[0]["resultados"][0]["series"]
rows=[]
for s in series:
    valor=next(iter(s["serie"].values()))
    nome=s["localidade"]["nome"].removesuffix(" - GO").strip()
    rows.append({"municipio":nome,"codigo_ibge":str(s["localidade"]["id"]),"populacao":pd.to_numeric(valor,errors="coerce")})
out=ROOT/"data"/"raw"; out.mkdir(parents=True,exist_ok=True)
df=pd.DataFrame(rows).dropna(subset=["populacao"]); df["populacao"]=df.populacao.astype("int64")
df.to_csv(out/"populacao_goias_ibge.csv",index=False)
meta={"fonte":"IBGE/SIDRA","tabela":6579,"variavel":9324,"periodo_solicitado":a.periodo,"url":url,"acesso_utc":datetime.now(timezone.utc).isoformat(),"municipios":len(df)}
(out/"metadados_ibge_populacao.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
print(df.head()); print(json.dumps(meta,ensure_ascii=False,indent=2))
