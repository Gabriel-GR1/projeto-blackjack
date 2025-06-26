import socket
import random
import time

IP_SERVIDOR = '127.0.0.1'
PORTA = 12345
ENDERECO = (IP_SERVIDOR, PORTA)

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(ENDERECO)
print(f"[SERVIDOR] Aguardando jogadores em {IP_SERVIDOR}:{PORTA}...")

jogadores = {}

def sortear_carta():
    return random.randint(1, 11)

def enviar(endereco, mensagem):
    servidor.sendto(mensagem.encode(), endereco)

def resetar_jogo():
    global jogadores
    jogadores = {}

while True:
    dados, endereco = servidor.recvfrom(1024)
    mensagem = dados.decode().strip()
    print(f"[RECEBIDO] {mensagem} de {endereco}")

    if mensagem.startswith("ENTRAR:"):
        nome = mensagem.split(":")[1]

        if endereco in jogadores:
            enviar(endereco, "MENSAGEM:Você já está conectado.")
            continue

        jogadores[endereco] = {"nome": nome, "pontuacao": 0, "ativo": True}
        enviar(endereco, f"MENSAGEM:Bem-vindo, {nome}! Use PEDIR_CARTA ou PARAR.")
        print(f"[LOG] {nome} entrou no jogo.")

    elif mensagem == "PEDIR_CARTA":
        if endereco in jogadores and jogadores[endereco]["ativo"]:
            carta = sortear_carta()
            jogadores[endereco]["pontuacao"] += carta
            enviar(endereco, f"CARTA:{carta}")
            print(f"[LOG] {jogadores[endereco]['nome']} recebeu carta {carta} (Total: {jogadores[endereco]['pontuacao']})")

            if jogadores[endereco]["pontuacao"] > 21:
                jogadores[endereco]["ativo"] = False
                enviar(endereco, "RESULTADO:perdeu")
                enviar(endereco, "MENSAGEM:Você ultrapassou 21!")
                print(f"[LOG] {jogadores[endereco]['nome']} estourou com {jogadores[endereco]['pontuacao']} pontos.")

    elif mensagem == "PARAR":
        if endereco in jogadores and jogadores[endereco]["ativo"]:
            jogadores[endereco]["ativo"] = False
            enviar(endereco, "MENSAGEM:Você parou. Aguardando os outros...")
            print(f"[LOG] {jogadores[endereco]['nome']} parou com {jogadores[endereco]['pontuacao']} pontos.")

    if len(jogadores) >= 2 and all(not j["ativo"] for j in jogadores.values()):
        print("[LOG] Todos os jogadores finalizaram a rodada.")
        maior = 0
        for j in jogadores.values():
            if j["pontuacao"] <= 21 and j["pontuacao"] > maior:
                maior = j["pontuacao"]

        vencedores = [
            (e, j) for e, j in jogadores.items()
            if j["pontuacao"] == maior and j["pontuacao"] <= 21
        ]

        if not vencedores:
            for e, j in jogadores.items():
                enviar(e, "RESULTADO:perdeu")
                enviar(e, "MENSAGEM:Ninguém venceu. Todos ultrapassaram 21.")
                print(f"[LOG] {j['nome']} perdeu. Todos estouraram.")
        else:
            for e, j in jogadores.items():
                if j["pontuacao"] > 21:
                    continue
                if j["pontuacao"] == maior:
                    if len(vencedores) == 1:
                        enviar(e, "RESULTADO:ganhou")
                        enviar(e, f"MENSAGEM:Parabéns {j['nome']}, você venceu com {j['pontuacao']} pontos!")
                        print(f"[LOG] {j['nome']} venceu com {j['pontuacao']} pontos.")
                    else:
                        enviar(e, "RESULTADO:empate")
                        enviar(e, f"MENSAGEM:{j['nome']}, você empatou com {j['pontuacao']} pontos!")
                        print(f"[LOG] {j['nome']} empatou com {j['pontuacao']} pontos.")
                elif j["pontuacao"] < maior:
                    enviar(e, "RESULTADO:perdeu")
                    enviar(e, f"MENSAGEM:Outros jogadores venceram com {maior} pontos.")
                    print(f"[LOG] {j['nome']} perdeu com {j['pontuacao']} pontos.")

        time.sleep(2)
        resetar_jogo()
        print("[LOG] Jogo reiniciado. Aguardando nova rodada...")
