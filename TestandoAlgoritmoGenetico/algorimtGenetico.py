import random

# Parâmetros do AG
TAMANHO_POP =  16 # Tamanho da população
GERACOES = 20  # Número de gerações
TAXA_MUTACAO = 0.1  # 1% de chance de mutação
# Definir novo limite máximo
NUM_BITS = 10  #10 bits
VALOR_MAX = (1 << NUM_BITS) - 1  # 1023

# Função de fitness (objetivo: maximizar f(x) = x²)
def fitness(x):
    return x ** 2

# Gerar indivíduo aleatório (10 bits) 0 até 1023
def gerar_individuo():
    return random.randint(0, VALOR_MAX)




# Gerar população inicial
def gerar_populacao():
    return [gerar_individuo() for _ in range(TAMANHO_POP)]

# Seleção dos pais (torneio)
def selecao(populacao):
    a, b = random.sample(populacao, 2)
    return a if fitness(a) > fitness(b) else b

# Cruzamento de um ponto
def cruzamento(pai1, pai2):
    ponto = random.randint(1, NUM_BITS - 1)  # Alterado para suportar 10 bits
    bin_pai1 = f"{pai1:0{NUM_BITS}b}"
    bin_pai2 = f"{pai2:0{NUM_BITS}b}"
    
    filho1 = int(bin_pai1[:ponto] + bin_pai2[ponto:], 2)
    filho2 = int(bin_pai2[:ponto] + bin_pai1[ponto:], 2)
    
    return filho1, filho2

# Mutação (troca um bit aleatório)
def mutacao(individuo):
    if random.random() < TAXA_MUTACAO:
        bit = random.randint(0, NUM_BITS - 1)
        individuo ^= (1 << bit)  # Inverte o bit escolhido
    return individuo

# Algoritmo Genético
populacao = gerar_populacao()

for geracao in range(GERACOES):
    # Avaliação da população
    populacao = sorted(populacao, key=fitness, reverse=True)
    
    print(f"Geração {geracao + 1}: Melhor indivíduo = {populacao[0]} (Fitness: {fitness(populacao[0])})")
    
    nova_populacao = []
    
    # Gerar nova população por seleção, cruzamento e mutação
    for _ in range(TAMANHO_POP // 2):
        pai1 = selecao(populacao)
        pai2 = selecao(populacao)
        filho1, filho2 = cruzamento(pai1, pai2)
        nova_populacao.extend([mutacao(filho1), mutacao(filho2)])
    
    populacao = nova_populacao

# Melhor solução encontrada
melhor_x = max(populacao, key=fitness)
print(f"Melhor solução encontrada: x = {melhor_x}, f(x) = {fitness(melhor_x)}")

