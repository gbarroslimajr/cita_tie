import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
import argparse

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f'logs/automation_{current_time}.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_filename,
                    filemode='a')
logger = logging.getLogger()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Automação de agendamento com parâmetros customizáveis.')
    parser.add_argument('--intervalo', type=int, default=5, help='Intervalo entre tentativas em minutos (padrão: 5)')
    parser.add_argument('--sound', action='store_true', help='Ativar sons de notificação')
    parser.add_argument('--background', action='store_true', help='Executar em modo headless')
    parser.add_argument('--provincia', type=str, default="Valencia", help='Província para seleção')
    parser.add_argument('--tramite', type=str,
                        default="POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA), RENOVACIÓN DE TARJETA DE LARGA DURACIÓN Y DUPLICADO",
                        help='Tipo de trâmite')
    parser.add_argument('--nacionalidade', type=str, default="BRASIL", help='Nacionalidade')
    parser.add_argument('--nie', type=str, required=True, help='Número de Identidade de Estrangeiro (NIE)')
    parser.add_argument('--nome', type=str, required=True, help='Nome completo')
    return parser.parse_args()


def play_sound(file_path, sound_enabled):
    if sound_enabled and os.path.exists(file_path):
        subprocess.call(['afplay', file_path])
        logger.info(f"Arquivo de som reproduzido: {file_path}")
    elif sound_enabled:
        logger.error(f"Arquivo de som não encontrado: {file_path}")


def play_success_sound(sound_enabled):
    play_sound('resources/sucess.mp4', sound_enabled)


def play_failure_sound(sound_enabled):
    play_sound('resources/failure.mp4', sound_enabled)


def iniciar_processo(args):
    chrome_options = Options()
    if args.background:
        chrome_options.add_argument("--headless")
        print("Modo headless ativado.")
        logger.info("Modo headless ativado.")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url_inicial = "https://icp.administracionelectronica.gob.es/icpplus/index"

    while True:
        try:
            driver.get(url_inicial)

            combobox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "form"))
            )
            select = Select(combobox)
            select.select_by_visible_text(args.provincia)

            selected_option = select.first_selected_option
            if selected_option.text == args.provincia:
                logger.info(f"{args.provincia} foi selecionada com sucesso!")
                print(f"{args.provincia} foi selecionada com sucesso!")
            else:
                logger.error(f"Erro: {args.provincia} não foi selecionada.")
                print(f"Erro: {args.provincia} não foi selecionada.")

            botao_aceptar1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            botao_aceptar1.click()

            novo_combobox = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "tramiteGrupo[0]"))
            )
            novo_select = Select(novo_combobox)
            novo_select.select_by_visible_text(args.tramite)

            novo_selected_option = novo_select.first_selected_option
            if novo_selected_option.text == args.tramite:
                logger.info(f"Opção '{args.tramite}' foi selecionada com sucesso!")
                print(f"Opção '{args.tramite}' foi selecionada com sucesso!")
            else:
                logger.error(f"Erro: A opção '{args.tramite}' não foi selecionada.")
                print(f"Erro: A opção '{args.tramite}' não foi selecionada.")

            botao_aceptar2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            botao_aceptar2.click()
            logger.info("Segundo botão 'Aceptar' clicado com sucesso!")
            print("Segundo botão 'Aceptar' clicado com sucesso!")

            opcao_sin_clave = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "btnEntrar"))
            )
            opcao_sin_clave.click()
            logger.info("Opção 'Presentación sin Cl@ve' selecionada com sucesso!")
            print("Opção 'Presentación sin Cl@ve' selecionada com sucesso!")

            combobox_nacionalidade = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "txtPaisNac"))
            )
            select_nacionalidade = Select(combobox_nacionalidade)
            select_nacionalidade.select_by_visible_text(args.nacionalidade)

            selected_nacionalidade = select_nacionalidade.first_selected_option
            if selected_nacionalidade.text == args.nacionalidade:
                logger.info(f"{args.nacionalidade} foi selecionado com sucesso como nacionalidade!")
                print(f"{args.nacionalidade} foi selecionado com sucesso como nacionalidade!")
            else:
                logger.error(f"Erro: {args.nacionalidade} não foi selecionado como nacionalidade.")
                print(f"Erro: {args.nacionalidade} não foi selecionado como nacionalidade.")

            campo_nie = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtIdCitado"))
            )
            campo_nie.send_keys(args.nie)
            logger.info("N.I.E. preenchido com sucesso!")
            print(f'N.I.E. preenchido com sucesso: {args.nie}')

            campo_nome = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtDesCitado"))
            )
            campo_nome.send_keys(args.nome)
            logger.info("Nome completo preenchido com sucesso!")
            print(f'Nome completo preenchido com sucesso: {args.nome}')

            botao_aceptar_final = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnEnviar"))
            )
            botao_aceptar_final.click()
            logger.info("Botão 'Aceptar' final clicado com sucesso!")
            print("Botão 'Aceptar' final clicado com sucesso!")

            botao_solicitar_cita = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Solicitar Cita']"))
            )
            botao_solicitar_cita.click()
            logger.info("Botão 'Solicitar Cita' clicado com sucesso!")
            print("Botão 'Solicitar Cita' clicado com sucesso!")

            try:
                mensagem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[@class='mf-msg__info']"))
                )
                if "En breve, la Oficina pondrá a su disposición nuevas citas." in mensagem.text:
                    logger.info("Não há citas disponíveis. Tentando novamente...")
                    print("Não há citas disponíveis. Tentando novamente...")
                    play_failure_sound(args.sound)

                    botao_salir = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "btnSalir"))
                    )
                    botao_salir.click()
                    logger.info(f"Aguardando {args.intervalo} minutos antes da próxima tentativa.")
                    print(f"Aguardando {args.intervalo} minutos antes da próxima tentativa.")
                    time.sleep(args.intervalo)
                else:
                    logger.info("Possivel cita encontrada. Verifique!")
                    while True:
                        play_success_sound(args.sound)
                        time.sleep(13)
                        if input("Pressione Enter para parar o beep e encerrar o programa..."):
                            return
            except:
                logger.warning("Não foi possível encontrar a mensagem esperada. Verificando a página...")
                print("Não foi possível encontrar a mensagem esperada. Verificando a página...")
                while True:
                    play_failure_sound(args.sound)
                    time.sleep(13)
                    if input("Pressione Enter para parar o beep e encerrar o programa..."):
                        return
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            print(f"Erro inesperado: {str(e)}")
            time.sleep(args.intervalo)


if __name__ == "__main__":
    args = parse_arguments()
    msg = f"Iniciando processo com os seguintes parâmetros: intervalo={args.intervalo}, sound={args.sound}, background={args.background}, provincia={args.provincia}, tramite={args.tramite}, nacionalidade={args.nacionalidade}, nie={args.nie}, nome={args.nome}"
    logger.info(msg)
    iniciar_processo(args)
    print(msg)
