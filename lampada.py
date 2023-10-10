import socket
import equipamentos_pb2

def enviar_comando_lampada(acao, socket_tcp):
    mensagem = equipamentos_pb2.Command()
    mensagem.type = equipamentos_pb2.Command.LAMPADA
    mensagem.action = acao

    try:
        socket_tcp.send(mensagem.SerializeToString())
    except ConnectionRefusedError:
        print("A conexão foi recusada. Verifique se o servidor está em execução.")
    except Exception as e:
        print("Erro ao enviar comando para a lâmpada:", e)


def main():

    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_tcp.bind(("127.0.0.1", 0))
    socket_tcp.connect(("127.0.0.1", 7000))

    enviar_comando_lampada(equipamentos_pb2.Command.NULL, socket_tcp)

    while True:
        mensagem = socket_tcp.recv(1024)

        escolha = equipamentos_pb2.Command()
        escolha.ParseFromString(mensagem)

        print(escolha.action)

        if escolha.action == 1:
            enviar_comando_lampada(equipamentos_pb2.Command.ON, socket_tcp)
        elif escolha.action == 2:
            enviar_comando_lampada(equipamentos_pb2.Command.OFF, socket_tcp)
        elif escolha.action == 3:
            enviar_comando_lampada(equipamentos_pb2.Command.SAIR, socket_tcp)
            break
        else:
            print("Opção inválida.")

    socket_tcp.close()

if __name__ == "__main__":
    main()