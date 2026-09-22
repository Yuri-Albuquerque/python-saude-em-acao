# Checklist antes da oficina

- [ ] Definir o ano epidemiológico principal.
- [ ] Executar `python scripts/baixar_sinan_dengue.py --ano ANO --origem saude --listar`.
- [ ] Baixar e agregar o SINAN.
- [ ] Baixar a população do mesmo ano ou da estimativa mais próxima.
- [ ] Executar `python scripts/preparar_municipios.py`.
- [ ] Conferir Itumbiara, valores ausentes, duplicatas e semanas.
- [ ] Comparar totais com painel/boletim oficial.
- [ ] Registrar data de acesso e versão dos pacotes.
- [ ] Executar todos os notebooks do início ao fim.
- [ ] Exportar HTMLs de contingência.
