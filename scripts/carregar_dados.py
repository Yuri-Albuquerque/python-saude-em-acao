"""Resolve os arquivos oficiais agregados exigidos pelos notebooks.

O projeto não usa dados sintéticos: os notebooks exigem as bases oficiais em
data/processed/. Execute os scripts de download antes de abrir os notebooks.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def caminhos():
    oficial=ROOT/"data"/"processed"
    casos=oficial/"dengue_semanal_goias.csv"
    municipios=oficial/"municipios_goias.csv"
    if casos.exists() and municipios.exists():
        return casos, municipios, "SINAN/DATASUS + IBGE (dados oficiais agregados)"
    raise FileNotFoundError(
        "Bases oficiais ausentes em data/processed/. Execute nesta ordem:\n"
        "  python scripts/baixar_sinan_dengue.py --ano 2024 --origem ftp\n"
        "  python scripts/baixar_ibge_populacao.py --periodo 2024\n"
        "  python scripts/preparar_municipios.py\n"
        "  python scripts/baixar_ibge_renda.py")