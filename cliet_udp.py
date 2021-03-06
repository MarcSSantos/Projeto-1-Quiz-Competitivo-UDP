from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred


def esperar(partida_iniciada):
    print()

    if partida_iniciada == qtd_clientes:
        print("Aguardando Jogadores... \r\n")
        resposta_servidor = socket_cliente.recvfrom(1024)

        print(str(resposta_servidor[0].decode()))
        print()
        responder()


def responder():

    resposta_servidor = socket_cliente.recvfrom(1024)

    if str(resposta_servidor[0].decode()) != "500":
        print(str(resposta_servidor[0].decode()))
        try:
            mensagem = inputimeout(prompt="Digite sua resposta: ", timeout=10) #tempo para o jogador responder uma pergunta
        except TimeoutOccurred:
            print("Tempo esgotado.")
            mensagem = "Sem nenhuma resposta"

        mensagem_codificada = mensagem.encode()
        socket_cliente.sendto(mensagem_codificada, ("localhost", 9090))
        print("Resposta enviada... \r\n")
        resposta_servidor = socket_cliente.recvfrom(1024)
        print(str(resposta_servidor[0].decode()))
        responder()

    else:

        print("\nFim de jogo. \n")
        resposta_servidor = socket_cliente.recvfrom(1024)
        totalJogadores = int(resposta_servidor[0].decode())

        ranking(totalJogadores)


def ranking(totalJogadores):

    print("Ranking")
    for _ in range(totalJogadores): 
        resposta_servidor = socket_cliente.recvfrom(1024)
        print(str(resposta_servidor[0].decode()))
    socket_cliente.close()


iniciar = True
socket_cliente = socket(AF_INET, SOCK_DGRAM)

qtd_clientes = 5 

partida_iniciada = []
while iniciar:
    print()
    mensagem = input("Digite o seu login para se conectar: ")
    if mensagem != "":
        mensagem_codificada = mensagem.encode()
        socket_cliente.sendto(mensagem_codificada, ("localhost", 9090))
        resposta_servidor = socket_cliente.recvfrom(1024)

        if partida_iniciada == []:
            cont = 0
            partida_iniciada.append(cont)

        if str(resposta_servidor[0].decode()) == "101":
            print(f"O(A) jogadoror(a) {mensagem} foi Cadastrado(a).")

            iniciar = False

            partida_iniciada[0] += qtd_clientes
            
            if partida_iniciada[0] <= qtd_clientes:
                Thread(target=esperar, args=(partida_iniciada)).start()

        else:

            if resposta_servidor[0].decode() == "410":  # nega????o de acesso
                print("\nPartida em andamento, tente novamente mais tarde.\n")
                socket_cliente.close()
                iniciar = False

    else:
        protocolo_erro = "401"
        print("Nome inv??lido, tente novamente.  \r\n")
        print(f"Nega????o de acesso {protocolo_erro}.  \r\n")
