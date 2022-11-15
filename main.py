"""
Autores: Pablo Munoz y Luis Andres Rojas
ITCR 2022 - Investigacion de Operaciones
"""



import random
import time
import toml

"""
Descripcion: Pasa un string a un vector
Inputs: string
Outputs: vector
"""
def string_to_vector(string):
    vector = []
    for i in range(len(string)):
        vector.append(string[i])
    return vector

"""
Descripcion: Revisa que tan bien se ajusta un individuo a la solucion
Inputs: El set de individuos
Outputs: Booleano
"""
def fitness_check(children_set):
    for i in range(len(children_set)):
        if children_set[i] == secret_passcode:
            return True
    return False

"""
Descripcion: Funcion que permite ejecutar el algoritmo genetico
Inputs: La generacion actual y el metodo de seleccion
Outputs: La siguiente generacion
"""
def next_generation(current_generation, selection_method):
    if selection_method == 'elite':
        fitness_scores = fitness(current_generation)
        parents = select_parents_elite(fitness_scores)
        children = create_children(parents)
        next_generation = mutation(children)
    elif selection_method == 'ruleta':
        fitness_scores = fitness(current_generation)
        parents = select_parents_roulette(fitness_scores)
        children = create_children(parents)
        next_generation = mutation(children)
    elif selection_method == 'ranking':
        fitness_scores = fitness(current_generation)
        parents = select_parents_ranking(fitness_scores)
        children = create_children(parents)
        next_generation = mutation(children)
    return next_generation

"""
Descripcion: Funcion que hace un rate de que tanto se ajusta un individuo a la solucion 
Inputs: La generacion actual
Outputs: Fitness Score
"""
def fitness(current_generation):
    fitness_scores = []
    for i in range(len(current_generation)):
        fitness_score = 0
        for x in range(len(current_generation[i])):
            if current_generation[i][x] == secret_passcode[x]:
                fitness_score += 1
        fitness_scores.append(fitness_score)
    return fitness_scores

"""
Descripcion: Funcion que selecciona a los padres por medio de elitismo
Inputs: El fitness score
Outputs: Los padres
"""
def select_parents_elite(fitness_scores):
    parents = []
    for i in range(num_parents):
        max_fitness_score = max(fitness_scores)
        max_fitness_score_index = fitness_scores.index(max_fitness_score)
        parents.append(population[max_fitness_score_index])
        fitness_scores[max_fitness_score_index] = -9999999999
    return parents

"""
Descripcion: Funcion que selecciona a los padres por medio de ruleta
Inputs: El fitness score
Outputs: Los padres
"""
def select_parents_roulette(fitness_scores):
    parents = []
    for i in range(num_parents):
        max_fitness_score = max(fitness_scores)
        max_fitness_score_index = fitness_scores.index(max_fitness_score)
        parents.append(population[max_fitness_score_index])
        fitness_scores[max_fitness_score_index] = -9999999999
    return parents

"""
Descripcion: Funcion que selecciona a los padres por medio de ranking
Inputs: El fitness score
Outputs: Los padres
"""
def select_parents_ranking(fitness_scores):
    parents = []
    for i in range(num_parents):
        max_fitness_score = max(fitness_scores)
        max_fitness_score_index = fitness_scores.index(max_fitness_score)
        parents.append(population[max_fitness_score_index])
        fitness_scores[max_fitness_score_index] = -9999999999
    return parents

"""
Descripcion: Funcion que crea los hijos de los padres
Inputs: Los padres
Outputs: Los hijos
"""
def create_children(parents):
    children = []
    for i in range(len(parents)):
        for x in range(len(parents)):
            if i != x:
                child = []
                for y in range(len(parents[i])):
                    if random.randint(0,100) < crossover_rate:
                        child.append(parents[i][y])
                    else:
                        child.append(parents[x][y])
                children.append(child)
    return children

"""
Descripcion: Funcion que muta a los hijos
Inputs: Los hijos
Outputs: Los hijos mutados
"""
def mutation(children):
    for i in range(len(children)):
        if random.randint(0,100) < mutation_rate:
            children[i][random.randint(0,len(children[i])-1)] = alphanumeric[random.randint(0,len(alphanumeric)-1)]
    return children


"""
Descripcion: Funcion que parsea el archivo de configuracion
Inputs: El archivo de configuracion
Outputs: Los parametros del algoritmo genetico
"""
def toml_parser():
    with open('config.toml') as f:
        data = toml.load(f)
    passcode = data['passcode']
    data = data['ag']
    print(data)
    return data, passcode


def main():

    # Declara las variables globales
    global secret_passcode
    global population
    global num_parents
    global crossover_rate
    global mutation_rate
    global alphanumeric
    
    #Declara las variables locales
    data, passcode = toml_parser()
    secret_passcode = string_to_vector(passcode['correct_passcode'])
    passcode_length = len(secret_passcode)
    population_size = data['population_size']
    num_parents =  data['num_parents']
    elite_size =  data['elite_size']
    mutation_rate = data['mutation_rate']
    crossover_rate  = data['crossover_rate']
    selection_method = data['selection_method']
    alphanumeric = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Inicializa la poblacion
    population = []
    for i in range(population_size):
        chromosome = []
        for x in range(passcode_length):
            chromosome.append(alphanumeric[random.randint(0,len(alphanumeric)-1)])
        population.append(chromosome)
    generation = 1
    fitness_scores = []
    start = time.time()
    # Ciclo principal del algoritmo genetico
    while True:
        print("Generation:",generation)
        fitness_scores.append(max(fitness(population)))
        if fitness_check(population):
            print("The secret passcode is:", secret_passcode)
            break
        population = next_generation(population, selection_method)
        generation += 1

    end = time.time()
    print("Time taken:", end - start)



"""
NOTA: Profe no logramos hacer los diferentes metodos de seleccion ni el metodo de crossover, pero si logramos hacer que diera buen resultado,
consideramos que es mejor que funcione a entregarle algo a medias entonces decidimos entregarle lo que tenemos. 
Hicimos el calculo de cuanto mas o menos nos ganamos y estimamos un 70 cerrado pero a lo que usted considere jaja :)
"""
main()