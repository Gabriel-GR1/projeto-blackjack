import socket
import threading
import time

IP_SERVIDOR = '127.0.0.1' 
PORTA_SERVIDOR = 12345
ENDERECO_SERVIDOR = (IP_SERVIDOR, PORTA_SERVIDOR)

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(5)

nome = input("Digite seu nome para entrar no jogo: ")
mensagem_entrada = f"ENTRAR:{nome}"
cliente.sendto(mensagem_entrada.encode(), ENDERECO_SERVIDOR)

try:
    resposta, _ = cliente.recvfrom(1024)
    print(resposta.decode())
except socket.timeout:
    print("Servidor não respondeu. Tente novamente mais tarde.")
    exit()

pontuacao = 0

def enviar_keepalive():
    while True:
        time.sleep(10)
        try:
            cliente.sendto("KEEPALIVE".encode(), ENDERECO_SERVIDOR)
        except:
            break

threading.Thread(target=enviar_keepalive, daemon=True).start()

jogando = True
while jogando:
    print("\nEscolha uma ação:")
    print("1 - Pedir carta")
    print("2 - Parar")

    opcao = input("Opção: ")

    if opcao == '1':
        cliente.sendto("PEDIR_CARTA".encode(), ENDERECO_SERVIDOR)

        try:
            resposta, _ = cliente.recvfrom(1024)
            mensagem = resposta.decode()
            print(f"🟡 {mensagem}")

            if mensagem.startswith("CARTA:"):
                valor = int(mensagem.split(":")[1])
                pontuacao += valor
                print(f"🟢 Sua pontuação atual: {pontuacao}")

            elif mensagem.startswith("RESULTADO:"):
                print("🏁 Rodada finalizada.")
                jogando = False

        except socket.timeout:
            print("⚠️ Servidor não respondeu ao pedido de carta.")

    elif opcao == '2':
        cliente.sendto("PARAR".encode(), ENDERECO_SERVIDOR)
        print("⏳ Aguardando resultado final...")

        while True:
            try:
                resposta, _ = cliente.recvfrom(1024)
                mensagem = resposta.decode()
                print(f"🟡 {mensagem}")

                if mensagem.startswith("RESULTADO:"):
                    print("🏁 Rodada finalizada.")
                    jogando = False
                    break

            except socket.timeout:
                print("⏳ Esperando os outros jogadores pararem...")
    else:
        print("⚠️ Opção inválida. Tente novamente.")
