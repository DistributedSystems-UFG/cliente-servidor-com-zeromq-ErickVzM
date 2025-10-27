import zmq
from time import sleep
from const import HOST, PORT 


def client():
    """
    Função cliente ZeroMQ: (SOMA, DATA_HORA, SUBTRAI, STOP).
    """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    connection_string = f"tcp://{HOST}:{PORT}"
    
    try:
        socket.connect(connection_string)
        print(f"Cliente ZeroMQ conectado em {connection_string}")
    except Exception as e:
        print(f"ERRO: Falha ao conectar em {connection_string}.")
        print(f"Detalhes: {e}")
        return

    requisicoes = [
        ("SOMA 15, 27", "SOMA"),
        ("DATA_HORA", "DATA/HORA ATUAL"),
        ("SUBTRAI 100, 35", "SUBTRAÇÃO")
    ]
    
    for operacao, descricao in requisicoes:
        print(f"\nTESTE: {descricao}")
        print(f"Enviando: {operacao}")
        
        socket.send(operacao.encode('utf-8'))
        
        try:
            resposta = socket.recv()
            print(f"Resposta do Servidor: {resposta.decode()}")
        except zmq.error.Again:
            print("ERRO: Timeout ou falha de comunicação ao receber a resposta.")
            break 

    print("\nTESTE: ENCERRAMENTO")
    print("Enviando sinal de STOP para o servidor.")
    socket.send(b"STOP")
    
    try:
        confirmacao_stop = socket.recv() 
        print(f"Confirmação do Servidor: {confirmacao_stop.decode()}")
    except zmq.error.Again:
        print("ERRO: Timeout ao esperar pela confirmação de STOP.")

    socket.close()
    context.term()
    print("\nCliente encerrado.")
