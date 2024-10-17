#!/bin/bash

# Defina os valores padrão para os argumentos
INTERVALO=5
SOUND=false
BACKGROUND=false
PROVINCIA="Valencia"
TRAMITE="POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA), RENOVACIÓN DE TARJETA DE LARGA DURACIÓN Y DUPLICADO"
NACIONALIDADE="BRASIL"
NIE=""
NOME=""

# Função para exibir a ajuda
show_help() {
    echo "Uso: $0 [opções]"
    echo "Opções:"
    echo "  -i, --intervalo MINUTOS    Intervalo entre tentativas em minutos (padrão: 5)"
    echo "  -s, --sound                Ativar sons de notificação"
    echo "  -b, --background           Executar em modo headless"
    echo "  -p, --provincia PROVINCIA  Província para seleção (padrão: Valencia)"
    echo "  -t, --tramite TRAMITE      Tipo de trâmite"
    echo "  -n, --nacionalidade PAIS   Nacionalidade (padrão: BRASIL)"
    echo "  --nie NIE                  Número de Identidade de Estrangeiro (NIE) (obrigatório)"
    echo "  --nome NOME                Nome completo (obrigatório)"
    echo "  -h, --help                 Exibir esta mensagem de ajuda"
}

# Processar os argumentos da linha de comando
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--intervalo)
            INTERVALO="$2"
            shift 2
            ;;
        -s|--sound)
            SOUND=true
            shift
            ;;
        -b|--background)
            BACKGROUND=true
            shift
            ;;
        -p|--provincia)
            PROVINCIA="$2"
            shift 2
            ;;
        -t|--tramite)
            TRAMITE="$2"
            shift 2
            ;;
        -n|--nacionalidade)
            NACIONALIDADE="$2"
            shift 2
            ;;
        --nie)
            NIE="$2"
            shift 2
            ;;
        --nome)
            NOME="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar se NIE e NOME foram fornecidos
if [ -z "$NIE" ] || [ -z "$NOME" ]; then
    echo "Erro: NIE e NOME são obrigatórios."
    show_help
    exit 1
fi

PYTHON_CMD="python3 script_agendamento.py"
PYTHON_CMD+=" --intervalo $INTERVALO"
PYTHON_CMD+=" --provincia \"$PROVINCIA\""
PYTHON_CMD+=" --tramite \"$TRAMITE\""
PYTHON_CMD+=" --nacionalidade \"$NACIONALIDADE\""
PYTHON_CMD+=" --nie \"$NIE\""
PYTHON_CMD+=" --nome \"$NOME\""

if [ "$SOUND" = true ]; then
    PYTHON_CMD+=" --sound"
fi

if [ "$BACKGROUND" = true ]; then
    PYTHON_CMD+=" --background"
fi

echo "Executando o script Python com os seguintes parâmetros:"
echo "$PYTHON_CMD"
eval "$PYTHON_CMD"