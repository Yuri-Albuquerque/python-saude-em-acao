"""Combina população oficial do IBGE com coordenadas da API de localidades.

Nada é imputado: coordenadas vêm da API oficial de malhas/localidades do IBGE;
se um município não retorna coordenada, permanece ausente.
"""
from pathlib import Path

import pandas as pd
import requests

ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/"data"/"raw"; out=ROOT/"data"/"processed"; out.mkdir(parents=True,exist_ok=True)

def coordenadas_ibge():
    """Centroide municipal via API de localidades (servicodados.ibge.gov.br)."""
    r=requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados/52/municipios",timeout=60)
    r.raise_for_status()
    codigos=[str(x["id"]) for x in r.json()]
    centroide={}
    for cod in codigos:
        try:
            rr=requests.get(f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{cod}?formato=application/vnd.geo+json",timeout=60)
            if rr.status_code==200:
                g=rr.json()
                # centroide da caixa delimitadora do polígono (resposta: FeatureCollection)
                xs=[]; ys=[]
                def walk(obj):
                    if isinstance(obj,list):
                        if len(obj)>=2 and all(isinstance(v,(int,float)) for v in obj[:2]):
                            xs.append(obj[0]); ys.append(obj[1])
                        else:
                            for it in obj: walk(it)
                    elif isinstance(obj,dict):
                        for k in ("coordinates","features","geometry"):
                            if k in obj: walk(obj[k])
                walk(g)
                if xs: centroide[cod]=(sum(xs)/len(xs),sum(ys)/len(ys))
        except Exception:
            continue
    df=pd.DataFrame({"codigo_ibge":list(centroide.keys()),
                     "longitude":[v[0] for v in centroide.values()],
                     "latitude":[v[1] for v in centroide.values()]})
    return df

def main():
    pop=pd.read_csv(raw/"populacao_goias_ibge.csv",dtype={"codigo_ibge":"string"})
    pop["codigo_ibge"]=pop.codigo_ibge.str.zfill(7)
    coords=coordenadas_ibge()
    coords["codigo_ibge"]=coords.codigo_ibge.astype(str).str.zfill(7)
    pop=pop.drop(columns=[c for c in ["latitude","longitude"] if c in pop.columns]).merge(coords,on="codigo_ibge",how="left")
    pop.to_csv(out/"municipios_goias.csv",index=False)
    print(f"{len(pop)} municípios gravados; com coordenada: {int(pop[['latitude','longitude']].notna().all(axis=1).sum())}")

if __name__=="__main__": main()