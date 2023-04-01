import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
from time import sleep

service = Service(executable_path="/path/to/chromedriver")
driver = webdriver.Chrome(service=service)


class wppBot:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=service, executable_path="/home/rocha/Área de Trabalho/geckodriver-v0.32.0-linux64.tar.gz\geckodriver.exe")

    def acessar_enviar(self):
        driver = self.driver
        driver.get("https://web.whatsapp.com/")  # Abre navegador e acessa site
        contatos_df = pd.read_csv("enviar.csv")  # Ler a planilha com os dados

        # Esperar até que a lista de contatos seja carregada
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "side")))

        enviado = 0
        erro = 0

        for i in range(len(contatos_df)):
            try:
                pessoa = contatos_df.loc[i, "Pessoa"]
                numero = contatos_df.loc[i, "Número"]
                credito = contatos_df.loc[i, "Crédito"]
                credito_valor = float(credito.replace(
                    "R$ ", "").replace(",", "."))  # transforma valor do arquivo em float
                if credito_valor > 1.20:  # compara com meu ponto de corte e define qual msg enviar
                    msg = contatos_df.loc[i, "Mensagem2"]
                else:
                    msg = contatos_df.loc[i, "Mensagem1"]
                texto = urllib.parse.quote(
                    f"Olá {pessoa}, bom dia! Tudo bem!?\n{msg}")
                link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
                driver.get(link)

                # Esperar até que o campo de mensagem seja carregado
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')))

                send = driver.find_element(
                    "xpath", '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')
                try:
                    send.send_keys(Keys.ENTER)
                except:
                    return False
                enviado += 1
                contatos_df.loc[i, "Status"] = 'S'
                contatos_df.to_csv("enviar.csv")
                print(f'Linha {i + 2}. Status: Enviado!')
                sleep(4)
            except Exception as e:
                erro += 1
                contatos_df.loc[i, "Status"] = 'S/ WPP'
                contatos_df.to_csv("enviar.csv")
                print(f'Linha {i + 2}. Status: Falha!')
                sleep(4)
            print('=' * 30)
        print(f' -> {enviado} com sucesso no envio!')
        print(f' -> {erro} com erro no envio!')


rochaBot = wppBot()
rochaBot.acessar_enviar()
