from playwright.sync_api import sync_playwright
from json import dumps

CONCURSOS_PAGE = 'https://www.estrategiaconcursos.com.br/blog/concursos-abertos/'
concursosEncontrados = []

valorMinimo = float(input('Digite o valor do salário desejado: '))

with sync_playwright() as p:
    print('Iniciando o navegador...')
    navegador = p.firefox.launch()
    # navegador = p.firefox.launch(headless=False)
    print('Acessando a página de concursos...')
    pagina = navegador.new_page()
    pagina.goto(CONCURSOS_PAGE)

    print('Realizando scraping...')
    items = pagina.locator('h3, ul')
    
    print('Filtrando concursos...')
    concurso = {}
    for i in range(items.count()):
        element = items.nth(i)
        texto = element.inner_text()
        if texto.startswith('Concurso '):
            if 'Orgão' in concurso:
                concursosEncontrados.append(concurso)
                concurso = {}
            concurso['Orgão'] = texto[9:]
        elif texto.startswith('Banca'):
            for linha in texto.split('\n'):
                if ':' in linha:
                    key, value = linha.split(':')[0], ''.join(linha.split(':')[1:])
                    if key == 'Salário' or key == 'Remuneração':
                        value = float(value.split('R$')[-1].replace('.', '').
                                                            replace(',', '.').
                                                            replace('+', '').
                                                            replace('gratificações', '').
                                                            replace('benefícios', '').
                                                            replace('adicionais', '').
                                                            replace('(2º Tenente)', '').
                                                            replace('(Aluno Oficial 2º Sargento)', ''))
                        key = 'Salário'
                    concurso[key] = value

    concursosFiltrados = []
    for e in concursosEncontrados:
        if 'Salário' in e and e['Salário'] >= valorMinimo:
            concursosFiltrados.append(e)
        if 'Remuneração' in e and e['Remuneração'] >= valorMinimo:
            concursosFiltrados.append(e)

    print(dumps(sorted(concursosFiltrados, key=lambda e:e['Salário']), indent=2, ensure_ascii=False))
