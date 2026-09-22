"""Resolve a fonte disponível sem confundir dados oficiais e demonstrativos."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def caminhos(preferir_oficial: bool=True):
    oficial=ROOT/"data"/"processed"
    demo=ROOT/"data"/"demo"
    casos_oficial=oficial/"dengue_semanal_goias.csv"
    municipios_oficial=oficial/"municipios_goias.csv"
    if preferir_oficial and casos_oficial.exists() and municipios_oficial.exists():
        return casos_oficial, municipios_oficial, "SINAN/DATASUS + IBGE (dados oficiais agregados)"
    casos_demo=demo/"dengue_semanal_demo.csv"
    municipios_demo=demo/"municipios_demo.csv"
    if casos_demo.exists() and municipios_demo.exists():
        return casos_demo, municipios_demo, "base sintética de demonstração"
    raise FileNotFoundError("Nenhuma base preparada. Execute gerar_dados_demo.py ou baixar_sinan_dengue.py e baixar_ibge_populacao.py.")
