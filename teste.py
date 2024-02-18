import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

def criar_tabela():
    conn = sqlite3.connect('reclamacoes.db')
    cursor = conn.cursor()

    # Criação da tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reclamacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descricao TEXT,
            status TEXT,
            data TEXT
        )
    ''')

    conn.commit()
    conn.close()

def inserir_dados(titulo, descricao, status, data):
    conn = sqlite3.connect('reclamacoes.db')
    cursor = conn.cursor()

    # Inserindo os dados na tabela
    cursor.execute('''
        INSERT INTO reclamacoes (titulo, descricao, status, data)
        VALUES (?, ?, ?, ?)
    ''', (titulo, descricao, status, data))

    conn.commit()
    conn.close()

def obter_status(reclamacao):
    # Tentar obter o status pela primeira classe
    try:
        status = reclamacao.find_element(By.CLASS_NAME, 'sc-1pe7b5t-4.cZrVnt').text
    except:
        # Se não for possível, tentar obter pela segunda classe
        try:
            status = reclamacao.find_element(By.CLASS_NAME, 'sc-1pe7b5t-4.ihkTSQ').text
        except:
            status = 'N/A'  # Defina um valor padrão se não conseguir obter o status

    return status

def capturar_dados_ate_pagina(pagina_alvo):
    # Substitua o caminho abaixo pelo caminho onde você baixou o ChromeDriver
    chrome_driver_path = './chromedriver.exe'

    # Configurando o WebDriver
    options = webdriver.ChromeOptions()
    # Adicione opções personalizadas se necessário

    # Inicializando o navegador Chrome
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # URL do site
    url = 'https://www.reclameaqui.com.br/empresa/light-servicos-de-eletricidade/lista-reclamacoes/'

    # Abrindo a página
    driver.get(url)

    # Aceitando os cookies, se necessário
    try:
        cookies_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'cookieconsent-accept-button'))
        )
        cookies_btn.click()
    except:
        pass  # Ignorar se não houver botão de cookies

    # Iterando até a página alvo
    for pagina_atual in range(1, pagina_alvo + 1):
        # Aguardando até que os elementos desejados estejam presentes na página
        reclamacoes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-1pe7b5t-0.eJgBOc'))
        )

        # Iterando sobre as reclamações e extraindo informações
        for reclamacao in reclamacoes:
            titulo = reclamacao.find_element(By.CLASS_NAME, 'sc-1pe7b5t-1.bVKmkO').text
            descricao = reclamacao.find_element(By.CLASS_NAME, 'sc-1pe7b5t-2.fGresJ').text
            status = obter_status(reclamacao)
            data = reclamacao.find_element(By.CLASS_NAME, 'sc-1pe7b5t-5.dspDoZ').text

            # Salvando os dados no banco de dados
            inserir_dados(titulo, descricao, status, data)

        # Imprimir mensagem de sucesso
        print(f"Web scraping da página {pagina_atual} realizado com sucesso.")

        # Navegando para a próxima página, exceto na última iteração
        if pagina_atual < pagina_alvo:
            proxima_pagina = driver.find_element(By.XPATH, f'//li[text()="{pagina_atual + 1}"]')
            proxima_pagina.location_once_scrolled_into_view  # Role para a visão antes de clicar
            proxima_pagina.click()

            # Aguardando alguns segundos para a nova página carregar completamente
            time.sleep(5)  # Ajuste o tempo conforme necessário

    # Fechando o navegador
    driver.quit()

# Criando a tabela se não existir
criar_tabela()

# Capturando dados até a página 5 e salvando no banco de dados
capturar_dados_ate_pagina(100)
