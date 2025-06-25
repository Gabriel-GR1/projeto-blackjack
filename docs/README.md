# projeto-blackjack
Este projeto é um trabalho prático da disciplina de Redes de Computadores. Implementa o jogo de cartas "21" (Blackjack) com comunicação cliente-servidor via sockets UDP.

## 👥 Desenvolvedor
- Gabriel Rodrigo dos Santos Miguel


## 🧠 Objetivo
Criar uma aplicação cliente-servidor usando sockets UDP, implementando as regras básicas do jogo "21", também conhecido como Blackjack.

## 🛠️ Tecnologias
- Linguagem: Python 3.13.5
- Comunicação: Sockets UDP
- Execução via terminal (sem interface gráfica)

## 📁 Estrutura do Projeto
projeto-21/
├── cliente/
│ └── cliente.py
├── servidor/
│ └── servidor.py
├── docs/
│ └── relatorio.pdf
└── README.md

## 📡 Protocolo de Comunicação

As mensagens trocadas entre cliente e servidor seguem um protocolo textual simples via sockets UDP. Os comandos são:

- `ENTRAR:<nome>` → Enviado pelo cliente para entrar no jogo.
- `CARTA:<valor>` → Enviado pelo servidor para informar uma nova carta ao cliente.
- `PEDIR_CARTA` → Enviado pelo cliente para pedir uma nova carta.
- `PARAR` → Enviado pelo cliente quando decidir parar.
- `RESULTADO:<ganhou/perdeu>` → Enviado pelo servidor com o resultado final.
- `MENSAGEM:<texto>` → Mensagens gerais do servidor para o cliente.

### Exemplo de Conversa
1. ENTRAR: Gabriel (cliente)
2. CARTA:9 (servidor)
3. PEDIR_CARTA (cliente)
4. CARTA:10 (servidor)
5. PARAR (cliente)
6. RESULTADO:ganhou (servidor)
7. MENSAGEM:Jogador João perdeu por ultrapassar 21 (servidor)
