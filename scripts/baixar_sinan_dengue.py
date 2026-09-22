"""Baixa e agrega notificações de dengue do SINAN/OpenDataSUS para Goiás.

Uso:
  python scripts/baixar_sinan_dengue.py --ano 2024 --origem saude
  python scripts/baixar_sinan_dengue.py --ano 2023 --origem ftp

A saída contém apenas contagens municipais semanais; nenhum registro individual é exportado.
A disponibilidade dos anos varia entre as origens. Consulte primeiro com --listar.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import pysus
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"processed"

def primeira_coluna(df, candidatos):
    mapa={c.upper():c for c in df.columns}
    for nome in candidatos:
        if nome in mapa: return mapa[nome]
    raise KeyError(f"Nenhuma das colunas {candidatos} foi encontrada. Disponíveis: {list(df.columns)}")

def municipios_ibge():
    url="https://servicodados.ibge.gov.br/api/v1/localidades/estados/52/municipios"
    r=requests.get(url,timeout=60); r.raise_for_status()
    m=pd.DataFrame({"codigo_ibge":[str(x["id"]) for x in r.json()],"municipio":[x["nome"] for x in r.json()]})
    m["codigo_sinan"]=m.codigo_ibge.str[:6]
    return m

def baixar(ano, origem):
    if origem=="saude":
        return pysus.saude.arboviroses(disease="dengue",year=ano,as_dataframe=True)
    return pysus.ftp.sinan(disease="deng",year=ano,as_dataframe=True)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--ano",type=int,required=True); p.add_argument("--origem",choices=["saude","ftp"],default="saude"); p.add_argument("--listar",action="store_true")
    a=p.parse_args()
    if a.listar:
        bag=(pysus.saude.arboviroses(disease="dengue",year=a.ano,download=False) if a.origem=="saude" else pysus.ftp.sinan(disease="deng",year=a.ano,download=False))
        print(bag); return
    df=baixar(a.ano,a.origem)
    col_mun=primeira_coluna(df,["ID_MN_RESI","CO_MUN_RES","ID_MUNICIP"])
    col_data=primeira_coluna(df,["DT_SIN_PRI","DT_NOTIFIC"])
    cod=df[col_mun].astype("string").str.replace(r"\.0$","",regex=True).str.zfill(6).str[:6]
    datas=pd.to_datetime(df[col_data],errors="coerce",dayfirst=True)
    base=pd.DataFrame({"codigo_sinan":cod,"data":datas}).dropna()
    base=base[base.codigo_sinan.str.startswith("52")].copy()
    base["semana"]=base.data.dt.to_period("W-SAT").dt.start_time
    nomes=municipios_ibge()
    semanal=(base.groupby(["codigo_sinan","semana"],as_index=False).size().rename(columns={"size":"casos"}).merge(nomes,on="codigo_sinan",how="left"))
    semanal=semanal[["codigo_ibge","municipio","semana","casos"]].sort_values(["municipio","semana"])
    OUT.mkdir(parents=True,exist_ok=True)
    semanal.to_csv(OUT/"dengue_semanal_goias.csv",index=False)
    meta={"fonte":"SINAN/DATASUS via PySUS","origem_pysus":a.origem,"ano":a.ano,"acesso_utc":datetime.now(timezone.utc).isoformat(),"linhas_originais":len(df),"notificacoes_goias_validas":len(base),"municipios":int(semanal.municipio.nunique()),"coluna_municipio":col_mun,"coluna_data":col_data}
    (OUT/"metadados_sinan.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    print(semanal.head()); print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
