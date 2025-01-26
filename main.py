import csv
import random
import numpy as np

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
        reader = csv.reader(file , delimiter=";")
        next(reader)  # Pular cabeçalho
        for row in reader:
            clients.append([int(row[0]), int(row[1])])
    return clients


# Inicializar população aleatória
def initialize_population(num_clients, pop_size):
    return [
        [random.choice(list(APs.keys())) for _ in range(num_clients)]
        for _ in range(pop_size)
    ]


# Avaliação da fitness (distância total e capacidade dos APs)
def evaluate_fitness(solution, clients):
    total_distance = 0
    capacity_violation = 0
    ap_loads = {ap: 0 for ap in APs.keys()}

    for i, ap in enumerate(solution):
        ap_loads[ap] += 1
        total_distance += calculate_distance(clients[i], APs[ap]["loc"])

    # Penalidade por violação de capacidade
    for ap, load in ap_loads.items():
        if load > APs[ap]["cap"]:
            capacity_violation += (load - APs[ap]["cap"]) * 10

    return total_distance + capacity_violation


# Seleção por torneio
def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    return min(selected, key=lambda x: x[1])[0]


# Crossover de um ponto
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# Mutação
def mutate(solution, mutation_rate=0.1):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = random.choice(list(APs.keys()))
    return solution


# Algoritmo genético
def genetic_algorithm(clients, pop_size=100, generations=200, mutation_rate=0.1):
    population = initialize_population(len(clients), pop_size)
    for generation in range(generations):
        fitnesses = [evaluate_fitness(individual, clients) for individual in population]
        next_population = []

        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            next_population.append(mutate(child1, mutation_rate))
            next_population.append(mutate(child2, mutation_rate))

        population = next_population

    # Melhor solução
    fitnesses = [evaluate_fitness(individual, clients) for individual in population]
    best_solution = population[np.argmin(fitnesses)]
    return best_solution, min(fitnesses)


# Salvar resultados em um arquivo CSV
def save_results_to_csv(clients, solution, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Cliente", "AP Conectado"])
        for i, ap in enumerate(solution):
            writer.writerow([f"Cliente {i + 1}", ap])



input_file_path = "clientes.csv"
output_file_path = "alocacao_clientes.csv"

clients = load_clients(input_file_path)
best_solution, best_fitness = genetic_algorithm(clients)

print("Melhor solução encontrada:", best_solution)
print("Fitness da solução:", best_fitness)

save_results_to_csv(clients, best_solution, output_file_path)
print(f"Resultados salvos no arquivo: {output_file_path}")
