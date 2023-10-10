import socket
import equipamentos_pb2


def enviar_comando_ar_condicionado(acao, socket_tcp, temperatura=None):
    mensagem = equipamentos_pb2.Command()
    mensagem.type = equipamentos_pb2.Command.AR_CONDICIONADO
    mensagem.action = acao

    if temperatura is not None:
        mensagem.temperature = temperatura

    try:
        socket_tcp.send(mensagem.SerializeToString())
        #socket_tcp.close()
    except Exception as e:
        print("Erro ao enviar comando para o ar-condicionado:", e)

def main():

    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_tcp.bind(("127.0.0.1", 0))
    socket_tcp.connect(("127.0.0.1", 7000))

    enviar_comando_ar_condicionado(equipamentos_pb2.Command.NULL, socket_tcp)

    while True:

        mensagem = socket_tcp.recv(1024)

        escolha = equipamentos_pb2.Command()
        escolha.ParseFromString(mensagem)

        print(escolha.action)

        if escolha.action == 1:
            enviar_comando_ar_condicionado(equipamentos_pb2.Command.ON, socket_tcp)
        elif escolha.action == 2:
            enviar_comando_ar_condicionado(equipamentos_pb2.Command.OFF, socket_tcp)
        elif escolha.action == 0:
            print(f"Temperatura escolhida: {escolha.temperature}")
            enviar_comando_ar_condicionado(equipamentos_pb2.Command.SET_TEMPERATURE, socket_tcp, temperatura=escolha.temperature)
        elif escolha.action == 3:
            enviar_comando_ar_condicionado(equipamentos_pb2.Command.SAIR, socket_tcp)
            break
        else:
            print("Opção inválida.")

    socket_tcp.close()

if __name__ == "__main__":
    main()