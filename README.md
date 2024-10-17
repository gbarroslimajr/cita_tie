# Projeto de Agendamento Automatizado

Este projeto consiste em um script Python para automatizar o processo de agendamento na extranjeria da Espanha, juntamente com um shell script para facilitar sua execução.

## Stack Tecnológica

- **Python 3.x**: Linguagem principal do script de automação
- **Selenium WebDriver**: Utilizado para automação web
- **ChromeDriver**: Driver específico para o Google Chrome
- **Bash**: Utilizado no shell script para execução facilitada

## Bibliotecas Python Principais

- `selenium`: Para automação web
- `webdriver_manager`: Para gerenciamento automático do ChromeDriver
- `argparse`: Para processamento de argumentos de linha de comando
- `logging`: Para registro de eventos e depuração

## Sobre o Script Python

O script Python (`script_agendamento.py`) automatiza o processo de verificação e agendamento. Ele realiza as seguintes operações principais:

1. Navega até o site especificado
2. Preenche formulários com informações fornecidas (província, tipo de trâmite, nacionalidade, NIE, nome)
3. Verifica a disponibilidade de datas
4. Repete o processo em intervalos definidos se não houver datas disponíveis
5. Emite notificações sonoras de sucesso ou falha (se ativado)

O script é configurável através de argumentos de linha de comando, permitindo personalização de parâmetros.

## Executando o Shell Script

O shell script (`executar_agendamento.sh`) fornece uma interface para executar o script Python.

### Pré-requisitos

1. Python 3.x instalado
2. Dependências Python instaladas (`pip install selenium webdriver_manager`)
3. Bash shell (padrão em sistemas Unix/Linux e macOS, disponível através do WSL ou Git Bash no Windows)

### Como Executar

1. Torne o script executável:
   ```
   chmod +x executar_agendamento.sh
   ```

2. Execute o script com os parâmetros desejados:
   ```
   ./executar_agendamento.sh [opções]
   ```

### Parâmetros Disponíveis

- `-i, --intervalo MINUTOS`: Intervalo entre tentativas em minutos (padrão: 5)
- `-s, --sound`: Ativar sons de notificação
- `-b, --background`: Executar em modo headless (sem interface gráfica)
- `-p, --provincia PROVINCIA`: Província para seleção (padrão: Valencia)
- `-t, --tramite TRAMITE`: Tipo de trâmite
- `-n, --nacionalidade PAIS`: Nacionalidade (padrão: BRASIL)
- `--nie NIE`: Número de Identidade de Estrangeiro (NIE) (obrigatório)
- `--nome NOME`: Nome completo (obrigatório)
- `-h, --help`: Exibir mensagem de ajuda

### Exemplo de Uso

```bash
./executar_agendamento.sh --nie "Z1234567Y" --nome "JOÃO DA SILVA" --intervalo 10 --sound --provincia "Barcelona"
```

Este comando executará o script para o NIE "Z1234567Y", nome "JOÃO DA SILVA", com intervalo de 10 minutos entre tentativas, sons ativados, para a província de Barcelona.

## Licença

Este projeto está licenciado sob a GNU General Public License v3.0 (GPLv3). Veja o arquivo `LICENSE` para mais detalhes.