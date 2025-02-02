import csv
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

# Configurações dos Access Points
APs = {
    "A": {"loc": [0, 0], "cap": 64},
    "B": {"loc": [80, 0], "cap": 64},
    "C": {"loc": [0, 80], "cap": 128},
    "D": {"loc": [80, 80], "cap": 128},
}


# Função para calcular a distância entre dois pontos
def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


# Carregar posições dos clientes do arquivo CSV
def load_clients(file_path):
    clients = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Pular cabeçalho
        for row in reader:
            clients.append([int(row[1]), int(row[2])])  # Adicionar as coordenadas como uma lista
    return clients


# Carregar resultados de um arquivo CSV
def load_result(file_path):
    df = pd.read_csv(file_path)
    return df


# Inicializar população aleatória
## Recebe o número de clientes no ambiente e gera uma lista de tamanho pop_size,
## em que cada item da lista contém a alocação de cada cliente a um AP.
## Retorna uma lista, onde cada item é uma possível solução ["A", "A", "C", ...]
def initialize_population(num_clients, pop_size):
    return [
        [random.choice(list(APs.keys())) for _ in range(num_clients)]  # Atribui aleatoriamente um AP a cada cliente
        for _ in range(pop_size)  # Cria pop_size soluções
    ]


# Avaliação da fitness (distância total e capacidade dos APs)
## Esta função calcula a distância total dos clientes aos APs e aplica uma penalização
## caso algum AP exceda sua capacidade.
def evaluate_fitness(solution, clients):
    total_distance = 0
    capacity_violation = 0
    ap_loads = {ap: 0 for ap in APs.keys()}  # Inicializa cargas dos APs

    for i, ap in enumerate(solution):
        # Aumenta a carga do AP correspondente ao cliente
        ap_loads[ap] += 1
        # Calcula a distância total do cliente ao AP
        total_distance += calculate_distance(clients[i], APs[ap]["loc"])

    # Penalidade por violação de capacidade
    for ap, load in ap_loads.items():
        if load > APs[ap]["cap"]:
            # Se a carga excede a capacidade, calcula a penalidade
            capacity_violation += (load - APs[ap]["cap"]) * 110

    # Retorna a soma da distância total com a penalização
    return total_distance + capacity_violation


# Seleção por torneio
## Selecionamos aleatoriamente 5 indivíduos da população e verificamos qual deles apresenta
## o menor valor de fitness, retornando esse indivíduo.
def tournament_selection(population, fitnesses, k=7):
    selected = random.sample(list(zip(population, fitnesses)), k)  # Seleciona k indivíduos aleatórios
    return min(selected, key=lambda x: x[1])[0]  # Retorna o com menor fitness


# Crossover de um ponto
## Realiza o crossover entre duas soluções possíveis (pais) para gerar dois filhos.
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)  # Ponto de divisão aleatório
    child1 = parent1[:point] + parent2[point:]  # Gera o primeiro filho
    child2 = parent2[:point] + parent1[point:]  # Gera o segundo filho
    return child1, child2


# Mutação
## Realiza uma mutação em uma solução possível, alterando aleatoriamente alguns dos genes.
def mutate(solution, mutation_rate=0.009):
    for i in range(len(solution)):
        if random.random() < mutation_rate:  # Verifica se ocorre a mutação
            solution[i] = random.choice(list(APs.keys()))  # Seleciona um novo AP aleatório
    return solution


# Algoritmo genético
## Calcula inicialmente uma população e, a cada geração, avalia a fitness da população atual.
## Realiza crossover e mutação sobre metade da população selecionada e forma a nova população.
## Ao final, seleciona a melhor solução encontrada.
def genetic_algorithm(clients, pop_size=300, generations=600, mutation_rate=0.009):
    population = initialize_population(len(clients), pop_size)  # Inicializa a população

    for generation in range(generations):
        fitnesses = [evaluate_fitness(individual, clients) for individual in population]  # Avalia a fitness
        next_population = []  # Inicializa a próxima população

        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)  # Seleciona pai
            parent2 = tournament_selection(population, fitnesses)  # Seleciona mãe
            child1, child2 = crossover(parent1, parent2)  # Realiza crossover
            next_population.append(mutate(child1, mutation_rate))  # Aplica mutação ao primeiro filho
            next_population.append(mutate(child2, mutation_rate))  # Aplica mutação ao segundo filho

        population = next_population  # Atualiza a população para a próxima geração

    # Melhor solução
    fitnesses = [evaluate_fitness(individual, clients) for individual in population]  # Avalia fitness da nova população
    best_solution = population[np.argmin(fitnesses)]  # Encontra a melhor solução (minimo fitness)
    return best_solution, min(fitnesses)


# Calcula a média das distâncias dos clientes
def calculate_average_distance(result):
    distance_elements = []

    for elements in result:
        if elements[0] == "Cliente":
            continue  # Ignora cabeçalho

        # Calcula a distância entre as coordenadas do cliente e a localização do AP
        distance_elements.append(calculate_distance([elements[2], elements[3]], APs[elements[1]]["loc"]))

    print(len(distance_elements))  # Exibe o número de distâncias calculadas
    return sum(distance_elements) / len(distance_elements)  # Retorna a média


# Salvar resultados em um arquivo CSV
def save_results_to_csv(clients, solution, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Cliente", "AP Conectado", "X", "Y"])  # Cabeçalho do CSV
        for i, ap in enumerate(solution):
            writer.writerow([f"{i + 1}", ap, clients[i][0], clients[i][1]])  # Escreve informação de cada cliente


input_file_path = "clientes.csv"  # Caminho do arquivo de entrada
output_file_path = "alocacao_clientes.csv"  # Caminho do arquivo de saída

clients = load_clients(input_file_path)  # Carrega a lista de clientes
best_solution, best_fitness = genetic_algorithm(clients)  # Executa o algoritmo genético

print("Melhor solução encontrada:", best_solution)  # Exibe a melhor solução
print("Fitness da solução:", best_fitness)  # Exibe a fitness da melhor solução

save_results_to_csv(clients, best_solution, output_file_path)  # Salva resultados no CSV
print(f"Resultados salvos no arquivo: {output_file_path}")  # Mensagem de confirmação

# Carrega os resultados salvos para plotar
result = load_result(output_file_path)
x = result["X"].to_numpy()  # Coordenadas X dos clientes
y = result["Y"].to_numpy()  # Coordenadas Y dos clientes
colors = result["AP Conectado"].to_numpy()  # APs conectados pelos clientes

# Dicionário de cores para visualização
colors_dict = {
    "A": "green",
    "B": "yellow",
    "C": "blue",
    "D": "red"
}
new_colors = [colors_dict[char] for char in colors]  # Mapeia cores para os APs

unique, counts = np.unique(colors, return_counts=True)  # Conta quantidade de clientes para cada AP

for ap, count in zip(unique, counts):
    print(f"AP-{ap}: {count}")

print(
    f"A média das distâncias é {calculate_average_distance(result.to_numpy())}")  # Calcula e exibe média das distâncias

# Plota as alocações dos clientes
fig, ax = plt.subplots()
green_patch = mpatches.Patch(color="green", label="AP A")
yellow_patch = mpatches.Patch(color="yellow", label="AP B")
blue_patch = mpatches.Patch(color="blue", label="AP C")
red_patch = mpatches.Patch(color="red", label="AP D")

ax.scatter(x, y, s=50, c=new_colors)  # Plota os clientes com suas respectivas cores

ax.set(xlim=(0, 80), ylim=(0, 80))  # Define limite dos eixos

# Adiciona legenda ao gráfico
fig.legend(loc="outside lower left", handles=[green_patch])
fig.legend(loc="outside lower right", handles=[yellow_patch])
fig.legend(loc="outside upper left", handles=[blue_patch])
fig.legend(loc="outside upper right", handles=[red_patch])

plt.show()  # Exibe o gráfico


# Parâmetros Bons:
## pop_size=100, generations=200, mutation_rate=0.008
## k=5
## penalidade de capacidade ultrapassada = 110