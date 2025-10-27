import multiprocessing 
import zmq
from time import sleep
from datetime import datetime 
from const import PORT 

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    
    socket.bind("tcp://*:" + PORT)
    print(f"Servidor ZeroMQ REP iniciado na porta {PORT}...")

    while True:
        try:
            message = socket.recv().decode()
            print(f"\nRecebido: {message}")
        except zmq.error.ZMQError as e:
            print(f"Erro ao receber mensagem: {e}")
            break

        partes = message.upper().split(' ', 1)
        comando = partes[0]
        dados = partes[1] if len(partes) > 1 else ""
        
        reply = ""
        
        if comando == "STOP":
            reply = "OK, Servidor encerrando."
            socket.send(reply.encode())
            print(f"Enviado: {reply}")
            break  

        elif comando == "SOMA":
            try:
                num1, num2 = map(float, dados.replace(" ", "").split(','))
                resultado = num1 + num2
                reply = f"Resultado da SOMA: {resultado}"
            except ValueError:
                reply = "ERRO: Formato inválido para SOMA."

        elif comando == "SUBTRAI":
            try:
                num1, num2 = map(float, dados.replace(" ", "").split(','))
                resultado = num1 - num2
                reply = f"Resultado da SUBTRAÇÃO: {resultado}"
            except ValueError:
                reply = "ERRO: Formato inválido para SUBTRAI."

        elif comando == "DATA_HORA":
            reply = datetime.now().strftime("Data/Hora Atual: %Y-%m-%d %H:%M:%S")

        else:
            reply = f"ERRO: Comando '{comando}' desconhecido."

        socket.send(reply.encode())
        print(f"Enviado: {reply}")

    socket.close()
    context.term()
    print("Servidor ZeroMQ encerrado.")

