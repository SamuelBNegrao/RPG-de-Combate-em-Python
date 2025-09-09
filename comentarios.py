import random
import time

#______________________JOGADOR______________________
class Personagem:
    def __init__(self, nome, raca):
        self.nome = nome

        # Escolha de raça
        if raca == 1:
            self.raca = "Humano"
        elif raca == 2:
            self.raca = "Elfo"
        elif raca == 3:
            self.raca = "Anão"
        else:
            raise ValueError("Raça inválida!")

        # Atributos base (serão sobrescritos nas subclasses)
        self.vida = 0
        self.armor = 0
        self.dano = (1, 1)

    # Método de ataque genérico (será sobrescrito nas subclasses → POLIMORFISMO)
    def atacar(self):
        qtd, faces = self.dano
        dano = sum(random.randint(1, faces) for _ in range(qtd))
        return dano, f"{self.nome} atacou causando {dano} de dano!"


#------------------ SUBCLASSES ------------------#
# Exemplo de HERANÇA: Guerreiro herda atributos e métodos de Personagem
class Guerreiro(Personagem):
    def __init__(self, nome, raca):
        # Chama o construtor da classe-mãe (Personagem)
        super().__init__(nome, raca)
        self.classe = "Guerreiro"
        self.vida = 20
        self.armor = 12
        self.dano = (2, 12)

    # POLIMORFISMO: sobrescreve o método atacar()
    def atacar(self):
        qtd, faces = self.dano
        dano = sum(random.randint(1, faces) for _ in range(qtd))
        return dano, f'{self.nome} atacou com seu machado, causando {dano} de dano! O inimigo urra de dor!'


class Mago(Personagem):  # HERANÇA
    def __init__(self, nome, raca):
        super().__init__(nome, raca)
        self.classe = "Mago"
        self.vida = 10
        self.armor = 7
        self.dano = (5, 6)

    # POLIMORFISMO: ataque diferente do Guerreiro
    def atacar(self):
        qtd, faces = self.dano
        dano = sum(random.randint(1, faces) for _ in range(qtd))
        return dano, f'{self.nome} castou uma magia com seu orbe! Causa {dano} de dano espiritual!'


class Ladrao(Personagem):  # HERANÇA
    def __init__(self, nome, raca):
        super().__init__(nome, raca)
        self.classe = "Ladrão"
        self.vida = 15
        self.armor = 10
        self.dano = (2, 10)

    # POLIMORFISMO: ataque diferente do Mago e do Guerreiro
    def atacar(self):
        qtd, faces = self.dano
        dano = sum(random.randint(1, faces) for _ in range(qtd))
        return dano, f'{self.nome} com um pulo veloz, apunhala o oponente causando {dano} de dano!'


#______________________INIMIGOS______________________
class Inimigo:
    def __init__(self):
        # Escolhe aleatoriamente um inimigo com seus atributos
        self.nome, self.vida, self.armor_class, self.dado_dano = self.escolhe_inimigo()

    def escolhe_inimigo(self):
        inimigos = {
            "Goblin": {"vida": 10, "armor_class": 5, "dado_dano": (1, 4)},
            "Orc": {"vida": 25, "armor_class": 10, "dado_dano": (1, 6)},
            "Esqueleto": {"vida": 12, "armor_class": 3, "dado_dano": (2, 4)},
            "Dragão Vermelho": {"vida": 50, "armor_class": 15, "dado_dano": (2, 20)}
        }
        nome = random.choice(list(inimigos.keys()))
        attr = inimigos[nome]
        return nome, attr["vida"], attr["armor_class"], attr["dado_dano"]

    def atacar(self):
        qtd, faces = self.dado_dano
        dano = sum(random.randint(1, faces) for _ in range(qtd))
        return dano, f"O {self.nome} ataca causando {dano} de dano!"


#______________________COMBATE______________________
def combate(jogador, inimigo):
    # Enquanto ambos estão vivos, o combate segue em turnos
    while jogador.vida > 0 and inimigo.vida > 0:
        # Turno do jogador
        print(f"\nTurno de {jogador.nome}")
        time.sleep(2)
        rolagem = random.randint(1, 20)  # rola um d20
        print(f"Rolagem de acerto: {rolagem}")
        time.sleep(2)

        if rolagem >= inimigo.armor_class:  # acerto
            if rolagem == 20:  # crítico
                print(f"Acerto crítico!!!")
                time.sleep(2)
                print(f"Rolagem de dano: {jogador.dano}")
                time.sleep(2)
                dano, msg = jogador.atacar()
                inimigo.vida -= 2 * dano  # dano dobrado
                print(msg)

            # ataque normal
            print(f"{jogador.nome} acertou o ataque!")
            time.sleep(2)
            print(f"Rolagem de dano: {jogador.dano}")
            time.sleep(2)
            dano, msg = jogador.atacar()  # POLIMORFISMO → o método chamado depende da classe real do jogador
            inimigo.vida -= dano
            print(msg)
        else:
            print(f"{jogador.nome} errou o ataque!")
        time.sleep(2)

        if inimigo.vida <= 0:  # inimigo derrotado
            print(f"{jogador.nome} é vitorioso!")
            time.sleep(2)
            return "Você venceu!"

        # Turno do inimigo
        print(f"\nTurno de {inimigo.nome}")
        time.sleep(2)
        rolagem = random.randint(1, 20)
        print(f"Rolagem de acerto: {rolagem}")
        time.sleep(2)

        if rolagem >= jogador.armor:  # acerto
            if rolagem == 20:  # crítico
                print(f"Acerto Crítico!!!")
                time.sleep(2)
                print(f"Rolagem de dano: {inimigo.dado_dano}")
                time.sleep(2)
                dano, msg = inimigo.atacar()
                jogador.vida -= dano
                print(msg)

            print(f"{inimigo.nome} acertou o ataque!")
            time.sleep(2)
            print(f"Rolagem de dano: {inimigo.dado_dano}")
            time.sleep(2)
            dano, msg = inimigo.atacar()
            jogador.vida -= dano
            print(msg)
        else:
            print(f"{inimigo.nome} errou o ataque!")
        time.sleep(2)

        if jogador.vida <= 0:  # jogador derrotado
            print(f"{inimigo.nome} desfere um golpe fatal, matando {jogador.nome}...")
            time.sleep(2)
            return "Você morreu!"


#______________________INÍCIO DO JOGO______________________
# Entrada de dados do jogador
nome = input('Digite o nome do seu personagem: ')
raca = int(input('Qual a sua raça? 1-Humano  2-Elfo  3-Anão: '))
classe = int(input('Qual a sua classe? 1-Guerreiro  2-Mago  3-Ladrão: '))

# Instancia a classe correta (HERANÇA + POLIMORFISMO)
if classe == 1:
    jogador = Guerreiro(nome, raca)
elif classe == 2:
    jogador = Mago(nome, raca)
elif classe == 3:
    jogador = Ladrao(nome, raca)
else:
    raise ValueError("Classe inválida!")

# Cria inimigo aleatório
inimigo = Inimigo()

# Narrativa inicial
print(f"\nUm {jogador.raca} {jogador.classe} chamado {jogador.nome} entra no calabouço...")
time.sleep(2)
print("Quando de repente, um inimigo aparece em sua frente!")
time.sleep(3)
print(f"Um {inimigo.nome} → Vida: {inimigo.vida}, AC: {inimigo.armor_class}, Dano: {inimigo.dado_dano}")
time.sleep(3)
print("Hora de lutar!")
time.sleep(3)

# Executa combate
resultado = combate(jogador, inimigo)
print("\n" + resultado)
