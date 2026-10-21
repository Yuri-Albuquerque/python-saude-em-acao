"""Resolve os arquivos oficiais agregados exigidos pelos notebooks.

O projeto não usa dados sintéticos: os notebooks exigem as bases oficiais em
data/processed/. Execute os scripts de download antes de abrir os notebooks.
"""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def caminhos():
    """Retorna ({ano: csv_casos}, csv_municipios, fonte); um CSV por ano baixado."""
    oficial=ROOT/"data"/"processed"
    casos={p.stem.rsplit("_",1)[1]:p for p in sorted(oficial.glob("dengue_semanal_goias_[0-9][0-9][0-9][0-9].csv"))}
    municipios=oficial/"municipios_goias.csv"
    if casos and municipios.exists():
        return casos, municipios, "SINAN/DATASUS + IBGE (dados oficiais agregados)"
    raise FileNotFoundError(
        "Bases oficiais ausentes em data/processed/. Execute nesta ordem (um download por ano):\n"
        "  python scripts/baixar_sinan_dengue.py --ano 2024 --origem ftp\n"
        "  python scripts/baixar_sinan_dengue.py --ano 2025 --origem ftp\n"
        "  python scripts/baixar_ibge_populacao.py --periodo 2024\n"
        "  python scripts/preparar_municipios.py\n"
        "  python scripts/baixar_ibge_renda.py")

def semana_epidemiologica(semana):
    """Ano e número da semana epidemiológica (domingo-sábado) a partir do domingo inicial.

    A semana pertence ao ano que contém sua quarta-feira (regra do calendário epidemiológico).
    """
    quarta=semana+pd.Timedelta(days=3)
    return quarta.dt.year, (quarta.dt.dayofyear-1)//7+1

if __name__=="__main__":
    ano,se=semana_epidemiologica(pd.Series(pd.to_datetime(["2024-12-29","2023-12-31","2025-12-28","2024-06-02"])))
    assert ano.tolist()==[2025,2024,2025,2024] and se.tolist()==[1,1,53,23], (ano.tolist(),se.tolist())
    print(caminhos()[0])
