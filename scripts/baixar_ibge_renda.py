"""Baixa indicadores sociais oficiais dos municípios de Goiás e integra ao cadastro municipal.

Fontes (todas oficiais, Censo Demográfico 2022, via API SIDRA):
- Renda: tabela 10295, variável 13431 (rendimento nominal médio mensal domiciliar per capita)
- Água: tabela 6803, categoria 72144 (possui ligação à rede geral e a utiliza como forma principal)
- Esgoto: tabela 6805, categoria 46290 (rede geral, rede pluvial ou fossa ligada à rede)
- Lixo: tabela 6892, categoria 2520 (coletado)

Índice de vulnerabilidade (0 = menos vulnerável, 1 = mais vulnerável):
média aritmética de quatro componentes min-max normalizados:
- renda (invertida), % sem água de rede, % sem esgoto de rede, % sem lixo coletado.

Nenhum valor é imputado: quando uma fonte não retorna dado, o componente fica ausente
e o índice usa a média dos componentes disponíveis do município.
"""
import json
from pathlib import Path

import pandas as pd
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"processed"
BASE="https://apisidra.ibge.gov.br/values"

def sidra(tid, cls=None, cat=None):
    """Conta de domicílios por município goiano, com filtro opcional de categoria."""
    url=f"{BASE}/t/{tid}/n6/in%20n3%2052/v/allxp/p/all"
    if cls is not None and cat is not None:
        url+=f"/c{cls}/{cat}"
    r=requests.get(url,timeout=120); r.raise_for_status()
    linhas=r.json()
    if not isinstance(linhas,list) or len(linhas)<2:
        raise RuntimeError(f"Resposta inesperada da API SIDRA (t{tid}): {str(linhas)[:200]}")
    df=pd.DataFrame(linhas[1:])[["D1C","V"]].rename(columns={"D1C":"codigo_ibge","V":"valor"})
    df["codigo_ibge"]=df.codigo_ibge.astype(str).str.zfill(7)
    df["valor"]=pd.to_numeric(df.valor,errors="coerce")
    return df.dropna().set_index("codigo_ibge")["valor"]

def renda_municipios():
    """Rendimento domiciliar per capita (t10295, variável 13431)."""
    r=requests.get(f"{BASE}/t/10295/n6/in%20n3%2052/v/13431/p/all",timeout=120); r.raise_for_status()
    linhas=r.json()
    df=pd.DataFrame(linhas[1:])[["D1C","V"]].rename(columns={"D1C":"codigo_ibge","V":"valor"})
    df["codigo_ibge"]=df.codigo_ibge.astype(str).str.zfill(7)
    df["valor"]=pd.to_numeric(df.valor,errors="coerce")
    return df.dropna().set_index("codigo_ibge")["valor"].rename("renda_pc")

def minmax(s,invert=False):
    lo,hi=s.min(),s.max()
    v=(s-lo)/(hi-lo)
    return 1-v if invert else v

def main():
    # 1. Obtaining the raw data from the IBGE SIDRA API
    renda=renda_municipios()
    tot_agua=sidra(6803).rename("dom_agua_total")
    rede_agua=sidra(6803,cls=1821,cat=72144).rename("dom_agua_rede")
    tot_esg=sidra(6805).rename("dom_esgoto_total")
    rede_esg=sidra(6805,cls=11558,cat=46290).rename("dom_esgoto_rede")
    tot_lixo=sidra(6892).rename("dom_lixo_total")
    col_lixo=sidra(6892,cls=67,cat=2520).rename("dom_lixo_coletado")

    # 1.5. Reading the list of municipalities in Goiás
    mun=pd.read_csv(OUT/"municipios_goias.csv",dtype={"codigo_ibge":"string"})
    mun["codigo_ibge"]=mun.codigo_ibge.str.zfill(7)
    # 1.6. Cleaning up previously calculated indicators from the municipality list
    limpar=["renda_pc","vulnerabilidade","pct_agua_rede","pct_esgoto_rede","pct_lixo_coletado",
            "dom_agua_total","dom_agua_rede","dom_esgoto_total","dom_esgoto_rede","dom_lixo_total","dom_lixo_coletado"]
    mun=mun.drop(columns=[c for c in limpar if c in mun.columns])
    # 1.7. Merging the raw data with the cleaned municipality list
    comp=pd.concat([renda,tot_agua,rede_agua,tot_esg,rede_esg,tot_lixo,col_lixo],axis=1).reset_index()
    mun=mun.merge(comp,on="codigo_ibge",how="left")
    # 1.8. Calculating the percentages of households with access to services
    mun["pct_agua_rede"]=100*mun.dom_agua_rede/mun.dom_agua_total
    mun["pct_esgoto_rede"]=100*mun.dom_esgoto_rede/mun.dom_esgoto_total
    mun["pct_lixo_coletado"]=100*mun.dom_lixo_coletado/mun.dom_lixo_total

    # 2. Calculating the vulnerability index based on the obtained data
    mun["vulnerabilidade"]=pd.concat([minmax(mun.renda_pc,invert=True),
                                      minmax(mun.pct_agua_rede,invert=True),
                                      minmax(mun.pct_esgoto_rede,invert=True),
                                      minmax(mun.pct_lixo_coletado,invert=True)],axis=1).mean(axis=1).round(4)

    # 3. Saving the processed data and metadata
    mun.to_csv(OUT/"municipios_goias.csv",index=False)
    meta={
        "fonte":"IBGE, Censo Demográfico 2022 (API SIDRA)",
        "componentes":{
            "renda_pc":{"tabela":10295,"variavel":13431},
            "pct_agua_rede":{"tabela":6803,"classificacao":1821,"categoria":72144},
            "pct_esgoto_rede":{"tabela":6805,"classificacao":11558,"categoria":46290},
            "pct_lixo_coletado":{"tabela":6892,"classificacao":67,"categoria":2520}},
        "vulnerabilidade":"média de 4 componentes min-max: renda (invertida), % sem água de rede, % sem esgoto de rede, % sem lixo coletado",
        "municipios_com_indicador":int(mun.vulnerabilidade.notna().sum())}
    (ROOT/"data"/"raw"/"metadados_ibge_renda.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

    # 4. Displaying a preview of the processed data and confirmation of the saved file
    print(mun[["municipio","renda_pc","pct_agua_rede","pct_esgoto_rede","pct_lixo_coletado","vulnerabilidade"]].head(8))
    print(f"Gravado: {OUT/'municipios_goias.csv'}")

if __name__=="__main__": main()