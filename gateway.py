import socket
import threading
from threading import Lock
import equipamentos_pb2
import struct
import time

equips = []
nome = ""

equipamentos = {
    "lampada": {"type": equipamentos_pb2.Command.EquipmentType.LAMPADA,
                "status": False},
    "ar_condicionado": {"type": equipamentos_pb2.Command.EquipmentType.AR_CONDICIONADO,
                        "status": False, "temperatura": 25},
    "sensor_temperatura": {"type": equipamentos_pb2.Command.EquipmentType.SensorData}
}

class Gateway:
    def __init__(self):
        self.equipamentos = equipamentos
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_udp.bind(("127.0.0.1", 5000))
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.bind(("127.0.0.1", 7000))  # Porta do servidor principal
        self.conexoes = []
        self.menu_lock = Lock()

    def enviar_mensagem_udp(self, mensagem, endereco):
        self.socket_udp.sendto(mensagem, endereco)

    def enviar_mensagem_tcp(self, mensagem, conexao):
        try:
            conexao.send(mensagem)
        except Exception as e:
            print("\nErro ao enviar mensagem via TCP:", e)

    def lidar_com_cliente(self, conexao, endereco, nome=None):

        global equips

        while True:
            if conexao.fileno() == -1:
                print("\n>> Conexão encerrada por", endereco)
                self.conexoes.remove((conexao, endereco))
                break

            i = 1

            print("Lista de dispositivos atualmente conectados:")
            for equip, soc in equips:
                print(f"{i}. {equip}")
                i = i + 1

            with self.menu_lock:
                try:
                    disp = int(input("Qual dispositivo voce deseja controlar? "))
                except Exception as e:
                    print("\n>> Dispositivo Inválido")
                    continue

                if disp <= len(equips):

                    if equips[disp-1][0] == "Lâmpada":
                        print("\n")
                        print("1. Ligar a lâmpada")
                        print("2. Desligar a lâmpada")
                        print("3. Desconectar lâmpada")

                        comando = int(input("\nQual comando você deseja executar? "))

                        if comando == 1:
                            if self.equipamentos["lampada"]["status"] == False:
                                mensagem = equipamentos_pb2.Command()
                                mensagem.type = equipamentos_pb2.Command.LAMPADA
                                mensagem.action = equipamentos_pb2.Command.ON
                            else:
                                print("\n>> A lâmpada já está ligada.\n")
                                continue
                        elif comando == 2:
                            if self.equipamentos["lampada"]["status"] != False:
                                mensagem = equipamentos_pb2.Command()
                                mensagem.type = equipamentos_pb2.Command.LAMPADA
                                mensagem.action = equipamentos_pb2.Command.OFF
                            else:
                                print("\n>> A lâmpada já está desligada.\n")
                                continue
                        elif comando == 3:
                            mensagem = equipamentos_pb2.Command()
                            mensagem.type = equipamentos_pb2.Command.LAMPADA
                            mensagem.action = equipamentos_pb2.Command.SAIR
                        else:
                            print("Comando inválido")
                            continue

                    elif equips[disp-1][0] == "Ar-Condicionado":
                        print("\n")
                        print("1. Ligar o ar-condicionado")
                        print("2. Desligar o ar-condicionado")
                        print("3. Ajustar a temperatura do ar-condicionado")
                        print("4. Desconectar ar-condicionado")

                        comando = input("\nQual comando você deseja executar? ")
                        comando = int(comando)

                        if comando == 1:
                            if self.equipamentos["ar_condicionado"]["status"] == False:
                                mensagem = equipamentos_pb2.Command()
                                mensagem.type = equipamentos_pb2.Command.AR_CONDICIONADO
                                mensagem.action = equipamentos_pb2.Command.ON
                            else:
                                print("\n>> O ar-condicionado já está ligado.\n")
                                continue
                        elif comando == 2:
                            if self.equipamentos["ar_condicionado"]["status"] != False:
                                mensagem = equipamentos_pb2.Command()
                                mensagem.type = equipamentos_pb2.Command.AR_CONDICIONADO
                                mensagem.action = equipamentos_pb2.Command.OFF
                            else:
                                print("\n>> O ar-condicionado já está desligado.\n")
                                continue
                        elif comando == 3:
                            if self.equipamentos["ar_condicionado"]["status"] != False:
                                ent = input("\n>> Digite a temperatura desejada (em °C): ")
                                temp = int(ent)
                                if(temp <= 26.0 and temp >= 17.0):
                                    # Extrair a temperatura do comando SET_TEMPERATURE
                                    temp_lida = ent
                                    # Enviar a temperatura para o sensor_temperatura por UDP
                                    sensor_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                    sensor_udp_socket.sendto(str(temp_lida).encode(), ("127.0.0.1", 5002))
                                    sensor_udp_socket.close()

                                    mensagem = equipamentos_pb2.Command()
                                    mensagem.type = equipamentos_pb2.Command.AR_CONDICIONADO
                                    mensagem.action = equipamentos_pb2.Command.SET_TEMPERATURE
                                    mensagem.temperature = temp
                                else:
                                    print("\n> O ar-condicionado só permite temperaturas entre 17ºC e 26ºC.\n")
                                    continue
                            else:
                                print("\n>> Não é possível alterar a temperatura porque o ar-condicionado está desligado.\n")
                                continue

                        elif comando == 4:
                            mensagem = equipamentos_pb2.Command()
                            mensagem.type = equipamentos_pb2.Command.AR_CONDICIONADO
                            mensagem.action = equipamentos_pb2.Command.SAIR
                        else:
                            print("Comando inválido")
                            continue

                    conexao.send(mensagem.SerializeToString())
                else:
                    print("Dispositivo inválido")
                    continue

                mensagem = conexao.recv(1024)

                # Desserializa a mensagem recebida
                comando = equipamentos_pb2.Command()
                comando.ParseFromString(mensagem)

                # Processa mensagens com base no tipo
                if comando.type == equipamentos_pb2.Command.LAMPADA:
                    if comando.action == equipamentos_pb2.Command.ON:
                        self.equipamentos["lampada"]["status"] = True
                        print("\n>> Lâmpada ligada.\n")
                        continue
                    elif comando.action == equipamentos_pb2.Command.OFF:
                        self.equipamentos["lampada"]["status"] = False
                        print("\n>> Lâmpada desligada.\n")
                        continue
                    elif comando.action == equipamentos_pb2.Command.SAIR:
                        print("\n>> Lâmpada desconectada.\n")
                        nome = "Lâmpada"

                        # Encerre a conexão com a lâmpada
                        conexao.close()

                        # Remova a entrada correspondente da lista de conexões ativas e do dicionário de nomes
                        if (conexao, endereco) in self.conexoes:
                            self.conexoes.remove((conexao, endereco))

                        break

                elif comando.type == equipamentos_pb2.Command.AR_CONDICIONADO:
                    if comando.action == equipamentos_pb2.Command.ON:
                        self.equipamentos["ar_condicionado"]["status"] = True
                        print("\n>> Ar-condicionado ligado.\n")
                        continue
                    elif comando.action == equipamentos_pb2.Command.OFF:
                        self.equipamentos["ar_condicionado"]["status"] = False
                        print("\n>> Ar-condicionado desligado.\n")
                        continue
                    elif comando.action == equipamentos_pb2.Command.SET_TEMPERATURE:
                        self.equipamentos["ar_condicionado"]["temperatura"] = comando.temperature
                        print(f"\n>> Temperatura do ar-condicionado ajustada para {comando.temperature}°C.\n")
                        continue
                    elif comando.action == equipamentos_pb2.Command.SAIR:
                        print("\n>> Ar-condicionado desconectado.\n")
                        nome = "Ar-Condicionado"
                        break

        print("\n>> Conexão encerrada por", endereco)
        equips.remove((nome, equips[disp-1][1]))
        conexao.close()


    def sensor_temperatura_continuo(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("127.0.0.1", 5003))
        while True:
            data, addr = udp_socket.recvfrom(1024)
            leitura = equipamentos_pb2.SensorData()
            leitura.ParseFromString(data)

            temperatura = leitura.temperature
            print(f"\n>> Temperatura recebida do sensor de temperatura: {temperatura}°C\n")
            time.sleep(5)  # Aguarde 5 segundos antes de receber a próxima leitura

    def iniciar(self):

        global equips

        # Iniciar thread para o sensor de temperatura contínuo
        sensor_thread = threading.Thread(target=self.sensor_temperatura_continuo)
        sensor_thread.start()

        # Iniciar o servidor TCP para comunicação com os equipamentos
        print("\n>> Gateway iniciado. Aguardando conexões...")
        self.socket_tcp.listen(5)

        while True:
            conexao, endereco = self.socket_tcp.accept()

            mensagem = conexao.recv(1024)

            # Desserializa a mensagem recebida
            comando = equipamentos_pb2.Command()
            comando.ParseFromString(mensagem)

            # Processa mensagens com base no tipo
            if comando.type == equipamentos_pb2.Command.LAMPADA and comando.action == equipamentos_pb2.Command.NULL:
                mensagem = "Lâmpada"
                equips.append(("Lâmpada", conexao))

            elif comando.type == equipamentos_pb2.Command.AR_CONDICIONADO and comando.action == equipamentos_pb2.Command.NULL:
                mensagem = "Ar-Condicionado"
                equips.append(("Ar-Condicionado", conexao))

            print("\n\n>> Nova conexão de", mensagem, endereco)

            cliente_thread = threading.Thread(target=self.lidar_com_cliente, args=(conexao, endereco))
            cliente_thread.start()
            self.conexoes.append((conexao, endereco))


if __name__ == "__main__":
    # Inicia o Gateway
    gateway = Gateway()
    gateway.iniciar()