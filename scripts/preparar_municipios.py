"""Combina população oficial do IBGE com coordenadas e renda opcional.
A renda não é imputada: quando não houver fonte oficial, permanece ausente.
"""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/"data"/"raw"; out=ROOT/"data"/"processed"; out.mkdir(parents=True,exist_ok=True)
pop=pd.read_csv(raw/"populacao_goias_ibge.csv",dtype={"codigo_ibge":"string"})
pop["codigo_ibge"]=pop.codigo_ibge.str.zfill(7)
# Coordenadas aproximadas são herdadas da base demo somente para os 12 municípios da oficina.
demo_path=ROOT/"data"/"demo"/"municipios_demo.csv"
if demo_path.exists():
    demo=pd.read_csv(demo_path)[["municipio","latitude","longitude"]]
    pop=pop.merge(demo,on="municipio",how="left")
pop["renda_pc"]=pd.NA
pop["vulnerabilidade"]=pd.NA
pop.to_csv(out/"municipios_goias.csv",index=False)
print(f"{len(pop)} municípios gravados em {out/'municipios_goias.csv'}")
