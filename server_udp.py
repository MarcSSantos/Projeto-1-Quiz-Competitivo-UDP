from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred
import random



def quicksort(vetor, indiceinicial=0, indiceparada=None):
    if indiceparada == None:
        indiceparada = len(vetor) - 1

    if indiceinicial < indiceparada:
        pivor = particao(vetor, indiceinicial, indiceparada)
        quicksort(vetor, indiceinicial, pivor - 1)
        quicksort(vetor, pivor + 1, indiceparada)


def particao(vetor, indiceinicial, indiceparada):
    indice_de_inicio = indiceinicial
    pivor = vetor[indiceparada][1]
    for i in range(indiceinicial, indiceparada):
        if vetor[i][1] >= pivor:
            vetor[indice_de_inicio], vetor[i] = vetor[i], vetor[indice_de_inicio]
            indice_de_inicio += 1

    else:
        vetor[indice_de_inicio], vetor[indiceparada] = vetor[indiceparada], vetor[indice_de_inicio]

    return indice_de_inicio


def ler_arquivo():

    arquivo = open("perguntas_respostas.txt", "r")
    dados = arquivo.readlines()

    dadosModificado = []

    lista_tuplas = []

    for x in dados:
        dadosModificado.append(x.strip())

    cont = 0
    while cont < len(dadosModificado)-1:
        lista_tuplas.append((dadosModificado[cont], dadosModificado[cont+1]))
        cont += 2

    return lista_tuplas


def iniciarPerguntas(mensagem_cliente, participantes, valor):

    for endereco in participantes.keys():
        socket_servidor.sendto(str.encode(mensagem_cliente), (endereco))
        print("A pergunta foi enviada aos jogadores \n")

    pergutaResposta(participantes, perguntas_e_respostas, valor, contador_indice_pergunta, sub_lista_n_pergunta)


def pergutaResposta(participantes, perguntas_e_respostas, valor, contador, indicesP):

    for endereco in participantes:
        pergunta = str.encode(
            perguntas_e_respostas[indicesP[contador]][0])
        socket_servidor.sendto(pergunta, (endereco))

    qtd_msg = 0
    dic_resposta = {}
    while qtd_msg < qtd_clientes:  

        mensagem_cliente, endereco_cliente = socket_servidor.recvfrom(1024)
        if endereco_cliente in participantes.keys():
            dic_resposta[endereco_cliente] = mensagem_cliente.decode()
            print(f"MSG: {mensagem_cliente.decode()} do(a) jogador(a) {participantes[endereco_cliente][0].decode()}")
            qtd_msg += 1

        else:
            resposta_nega????o = "410"
            print(">>>Jogador tentando se conetar, mas foi recusado<<<")
            socket_servidor.sendto(resposta_nega????o.encode(), (endereco_cliente))

    for k, v in dic_resposta.items():
        if v == perguntas_e_respostas[indicesP[contador]][1]:

            print(f"O(A) jogador(a) {participantes[k][0].decode()} acertou a resposta")
            participantes[k][1] += 25
            resposta_1_cliente = str.encode(f"Parab??ns! Voc?? acertou a resposta e ganhou 25 pontos. Sua pontua????o atual ?? {participantes[k][1]}")

            socket_servidor.sendto(resposta_1_cliente, (k))
        else:
            if v == "nao respondeu":
                participantes[k][1] -= 1
            else:
                participantes[k][1] -= 5

            print(f"O(A) jogador(a) {participantes[k][0].decode()} errou a resposta")

            resposta_1_cliente = str.encode(f"Infelizmente, voc?? errou a resposta e perdeu 5 pontos. Sua pontua????o atual ?? {participantes[k][1]}\n")
            socket_servidor.sendto(resposta_1_cliente, (k))

    valor += 1
    contador += 1

    if valor != 5 and contador != 5:  #Defini????o de quantidade de iniciarPerguntas

        Thread(target=pergutaResposta, args=(participantes,
               perguntas_e_respostas, valor, contador, indicesP)).start()

    else:
 
        resposta = "500"
        resposta_cliente = str.encode(resposta)
        for x, y in dic_resposta.items():
            socket_servidor.sendto(resposta_cliente, x)

        listao = []
        for x in participantes.values():
            listao.append(x)

        ordena_listao = quicksort(listao)

        totalJogadores = str(qtd_clientes).encode()
        for p in participantes.keys():
            socket_servidor.sendto(totalJogadores, p)

        for x in listao:
            for y in participantes.keys():
                classificacao = str.encode(
                    f"A pontua????o do(a) jogardor(a) {x[0].decode()} foi de: {x[1]} pontos.")
                socket_servidor.sendto(classificacao, y)
        socket_servidor.close()

socket_servidor = socket(AF_INET, SOCK_DGRAM)
socket_servidor.bind(("localhost", 9090))
perguntas_e_respostas = ler_arquivo()

# implementa????o randomifica????o
sub_lista_n_pergunta = []
while len(sub_lista_n_pergunta) < 20:
    indice_aleatorio = random.randint(0, 19)

    if indice_aleatorio not in sub_lista_n_pergunta:
        sub_lista_n_pergunta.append(indice_aleatorio)



contador_indice_pergunta = 0
conexao_start = True
valor = 0
participantes = {}
qtd_clientes = 0
max_jogadores = 5
min_jogadores = 1
aceitar_mais_jogadores = True

while conexao_start and len(participantes) < max_jogadores and aceitar_mais_jogadores == True:

    print()
    try:
        print("Aguardando requisi????es... \r\n")
        socket_servidor.settimeout(20) #tempo para incri????o de participantes
        
        mensagem_cliente, endereco_cliente = socket_servidor.recvfrom(1024)
        participantes[endereco_cliente] = [mensagem_cliente, 0]
        print(f"O/A participante {mensagem_cliente.decode()} entrou")
        resposta = "101"
        resposta_cliente = str.encode(resposta)
        socket_servidor.sendto(resposta_cliente, endereco_cliente)
        print("Resposta enviada para o/a participante \r\n")
    except:
        qtd_clientes = len(participantes)
        aceitar_mais_jogadores = False

    qtd_clientes = len(participantes)


if len(participantes) == qtd_clientes and len(participantes) >= min_jogadores:  
   
    mensagem_start = "Quiz de conhecimentos gerais comecou!"

    Thread(target=iniciarPerguntas, args=(mensagem_start, participantes, valor)).start()

else:
    print('N??o h?? jogadores suficientes para come??ar a partida.')
    socket_servidor.close()

