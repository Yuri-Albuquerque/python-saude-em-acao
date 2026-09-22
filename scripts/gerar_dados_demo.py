"""Gera dados sintéticos agregados para a oficina. Não representam estatísticas oficiais."""
from pathlib import Path
import numpy as np
import pandas as pd

RNG=np.random.default_rng(42)
OUT=Path(__file__).resolve().parents[1]/"data"/"demo"
OUT.mkdir(parents=True,exist_ok=True)
municipios=[
("Itumbiara",107970,2500,-18.41,-49.22),("Goiânia",1494599,2200,-16.68,-49.25),
("Aparecida de Goiânia",527796,1500,-16.82,-49.25),("Anápolis",398869,1750,-16.33,-48.95),
("Rio Verde",225696,2400,-17.79,-50.92),("Catalão",114427,2600,-18.17,-47.95),
("Jataí",105729,2300,-17.88,-51.72),("Caldas Novas",98622,1900,-17.74,-48.63),
("Formosa",115901,1450,-15.54,-47.34),("Luziânia",209129,1350,-16.25,-47.95),
("Mineiros",70681,2150,-17.57,-52.55),("Goianésia",73104,1650,-15.32,-49.12)]
mun=pd.DataFrame(municipios,columns=["municipio","populacao","renda_pc_demo","latitude","longitude"])
mun["vulnerabilidade_demo"]=((mun.renda_pc_demo.max()-mun.renda_pc_demo)/(mun.renda_pc_demo.max()-mun.renda_pc_demo.min()))
weeks=pd.date_range("2025-01-05",periods=52,freq="W-SUN")
rows=[]
for j,r in mun.iterrows():
    seasonal=1+2.8*np.exp(-0.5*((np.arange(52)-13)/6)**2)
    base=r.populacao/100000*(8+18*r.vulnerabilidade_demo)
    cases=RNG.poisson(base*seasonal)
    if r.municipio=="Itumbiara": cases[14:18]+=np.array([18,30,24,12])
    for w,c in zip(weeks,cases): rows.append((r.municipio,w.date(),int(c)))
casos=pd.DataFrame(rows,columns=["municipio","semana","casos"])
casos.to_csv(OUT/"dengue_semanal_demo.csv",index=False)
mun.to_csv(OUT/"municipios_demo.csv",index=False)
print(f"Dados demo gravados em {OUT}")
