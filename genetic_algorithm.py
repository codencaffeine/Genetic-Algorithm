import numpy as np
import math

##################################### Test inputs #####################################

outlook_conditions = [[0,0,0], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [1,1,1]]
Temperature_conditions = [[0,0,0], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [1,1,1]]
humidity_conditions = [[0,0], [0,1], [1,0], [1,1]]
wind_conditions = [[0,0], [0,1], [1,0], [1,1]]

member = [1,1,0,1,1,1,1,0,1,1]
population  = [[1,1,0,1,1,1,0,0,1,1], [0,0,1,1,1,0,1,0,1,0], [1,1,0,1,1,1,0,0,1,1], [1,1,0,1,1,1,0,0,1,1], [1,1,0,1,1,1,1,0,1,1]]
sample = ["Sunny", "Hot", "High", "Weak", "Yes"]
data = [["Sunny", "Hot", "High", "Weak", "Yes"], ["Rain", "Hot", "High", "Weak", "No"], ["Sunny", "Hot", "High", "Strong", "Yes"], ["Rain", "Mild", "High", "Weak", "No"]]
print(np.array(data))


##################################### initializing a population #####################################
def initialise_population(pop_size):
    population  = []
    boolean_value = [0,1]
    for i in range(pop_size):
        pops = []
        for j in range(len(num_bits)):
            p = list(np.random.choice(boolean_value, size=num_bits[j])) 
            print(p)
            pops = pops + p
            # " ".join(str(i)for i in list)
        population.append(pops)
    return population 

##################################### Performing Crossover operation #####################################
def crossover_operator(parent1, parent2):
    parent_length = min(len(parent1), len(parent2))
    options = list(range(1, parent_length-1))
    print(options)
    crossover_point = np.random.choice(options)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2, crossover_point
    
##################################### Performing Mutation operation #####################################
def mutation_operator(member):
    options = list(range(len(member)))
    mutation_point = np.random.choice(options)
    if member[mutation_point] == 1:
        member[mutation_point] = 0
    else:
        member[mutation_point] = 1
    return member, mutation_point

##################################### Getting attribute index in the members #####################################
def get_attributes_index():
    index = {}
    idx = 0
    for i in range(len(tennis_attributes)):
        for j in range(1, len(tennis_attributes[i])):
            index[tennis_attributes[i][j]] = idx
            idx += 1
    return index

##################################### Checking correctness of the members #####################################
def check_correctness(member, sample, index):
    for i in sample[:-1]:
        if member[index[i]] == 0:
            return False
    
    return True

##################################### Getting the parameters from user #####################################
def get_parameters():
    fitness_threshold = float(input("Enter a fitness threshold value: "))
    crossover_replacement_rate = float(input("Enter a crossover replacement rate value: "))
    mutation_rate = float(input("Enter a mutation rate value: "))
    return fitness_threshold, crossover_replacement_rate, mutation_rate


##################################### Getting the fitness probability #####################################
def get_probability_of_fitness(population_fitness):
    fitness_sum = sum(population_fitness)
    fitness_probability = []
    idx = -1
    for fitness in population_fitness:
        idx += 1
        print(fitness)
        fitness_probability.append(fitness / fitness_sum)
    return fitness_probability


##################################### Calculating the fitness #####################################
def calculate_fitness(population, data):
    population_fitness = []
    correct = []
    print("#####################################################\n#####################################################")
    for member in population:
        print("member: ",member)
        idx = 0
        num_correct = 0
        for sample in data:
            print("sample", sample)
            member_result = check_correctness(member, sample, index)
            print("member_result", member_result)
            sample_result = check_sample(sample)
            print("sample_result", sample_result)
            if sample_result == member_result:
                num_correct += 1
                print("num_correct", num_correct)
                correct.append(member)
            idx += 1
        fitness_of_member = num_correct/ len(data)
        print("num_correct", num_correct)
        print("fitness of the member", fitness_of_member)
        print("data length", len(data))
        population_fitness.append(fitness_of_member)
    return population_fitness


##################################### Checking the sample target value #####################################
def check_sample(sample):
    if sample[-1] == "Yes":
        sample_result = True
    else:
        sample_result = False
    return sample_result

##################################### Iterating over generations #####################################
def creating_generations(population):
    while max(population_fitness) > fitness_threshold:
        fitness_probability = get_probability_of_fitness(population_fitness)
        next_population = []
        for i in range(int(crossovered_population / 2)):
            print(population)
            parent1 = np.random.choice(population, fitness_probability)
            population.pop(parent1)
            parent2 = np.random.choice(population, fitness_probability)
            population.append(parent1)
            child1, child2, _ = crossover_operator(parent1, parent2)
            next_population.append(child1)
            next_population.append(child2)
        for i in range(repeated_population):
            same_member = np.random.choice(population, fitness_probability)
            next_population.append(same_member)
        for i in range(mutated_population):
            mutation_choice = np.random.choice(next_population)
            new_member, _ = mutation_operator(mutation_choice)
            next_population.append(new_member)
            next_population.pop(mutation_choice)
        population = next_population


##################################### Getting the best hypothesis #####################################
def best_hypothesis(population):       
    final_population = creating_generations(population)
    population_fitness = calculate_fitness(final_population, data)
    best_hypothesis = population(population_fitness.index(max(population_fitness)))
    return best_hypothesis



##################################### Reading the tennis data #####################################
f = open("/Users/nitish/Documents/Aishwarya/Machine_Learning/tennis_attributes.txt", "r")
tennis_attributes = f.readlines()

print("\n\n=============================================\nThe tennis attributes are: \n", tennis_attributes)


f.close()
num_bits = []
for i in range(len(tennis_attributes)):
    tennis_attributes[i] = tennis_attributes[i].split(" ")
    tennis_attributes[i][-1] = tennis_attributes[i][-1].split("\n")[0]
tennis_attributes.pop()
print(f"\n\n=============================================\nthe tennis attributes list: {tennis_attributes}")

##################################### Obtaining attributes from the data #####################################

print("the len:", len(tennis_attributes[2]))
for attributes in range(len(tennis_attributes)):
    if attributes == len(tennis_attributes)-1:
        num_bits.append(int(len(tennis_attributes[attributes]) - 2))
        
    else:
        num_bits.append(int(len(tennis_attributes[attributes]) - 1))
        
    
print("\n\n=============================================\n The num bits: ", num_bits)

index = {'Sunny': 0, 'Overcast': 1, 'Rain': 2, 'Hot': 3, 'Mild': 4, 'Cool': 5, 'High': 6, 'Normal': 7, 'Weak': 8, 'Strong': 9}






                

print(tennis_attributes)



population_fitness = calculate_fitness(population, data)
print("The population fitness is", population_fitness)


result = check_correctness(member, sample, index)
print("result = ", result)



fitness_threshold, crossover_replacement_rate, mutation_rate = 0.8, 0.5, 0.2
crossovered_population = int(len(population) * crossover_replacement_rate)
mutated_population = int(len(population) * mutation_rate)
repeated_population = len(population) - crossovered_population
print("Crossovered population size: ", crossovered_population)
print("Mutated population size: ", mutated_population)


def get_parameters():
    fitness_threshold = float(input("Enter a fitness threshold value: "))
    crossover_replacement_rate = float(input("Enter a crossover replacement rate value: "))
    mutation_rate = float(input("Enter a mutation rate value: "))
    #--------------------------------------------------------------------------#
    crossovered_population = int(len(population) * crossover_replacement_rate)
    mutated_population = int(len(population) * mutation_rate)
    repeated_population = len(population) - crossovered_population  
    
    return crossovered_population, mutated_population, repeated_population

crossovered_population, mutated_population, repeated_population = get_parameters()
fitness_probability = get_probability_of_fitness(population_fitness)
print("fitness probability", fitness_probability)


print("The best hypothesis: ", best_hypothesis = best_hypothesis(population))