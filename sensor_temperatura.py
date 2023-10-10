import socket
import time
import random
import equipamentos_pb2
import threading

# Temperatura inicial (ambiente)
temp_lida = 27

def receber_temperatura_ar_condicionado():
    global temp_lida
    ar_condicionado_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ar_condicionado_socket.bind(("127.0.0.1", 5002))

    while True:
        data, _ = ar_condicionado_socket.recvfrom(1024)
        dados_str = data.decode('utf-8')
        temp_lida = float(dados_str)
        print("Dados recebidos:", temp_lida)  # Adicione esta linha para depuração

        time.sleep(5)  # 5 segundos antes de receber a próxima temperatura

def gerar_temperatura(sensor_socket):
    global temp_lida
    while True:
        temperatura = random.uniform(temp_lida - 1.5, temp_lida + 1.5)

        leitura = equipamentos_pb2.SensorData()
        leitura.temperature = temperatura

        mensagem = leitura.SerializeToString()
        sensor_socket.send(mensagem)  # Envie a leitura para o Gateway
        print(f"Temperatura enviada pelo sensor: {temperatura}°C")

        time.sleep(10)


def main():
    sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sensor_socket.connect(("127.0.0.1", 5003))
    # print("Sensor de temperatura pronto para receber leituras.")

    # Thread para receber a temperatura do ar_condicionado
    ar_condicionado_thread = threading.Thread(target=receber_temperatura_ar_condicionado)
    ar_condicionado_thread.start()

    # Thread para gerar temperaturas com base em temp_lida
    gerar_temperatura_thread = threading.Thread(target=gerar_temperatura, args=(sensor_socket,))
    gerar_temperatura_thread.start()


if __name__ == "__main__":
    main()
