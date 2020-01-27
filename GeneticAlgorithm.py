class Chromosome:
  def __init__(self, genetic_code, fitness):
      self.genetic_code = genetic_code
      self.fitness = fitness
  def __str__(self):
      return str(self.genetic_code) + " " + str(self.fitness)


class GeneticAlgorithm:
    def __init__(self, graf, n):
      self.n = n #broj cvorova u grafu
      self.m = 2**n #broj do kog je moguce birati brojeve    
      self.graf = graf
      
      if(n < 7):
        self.generation_size = 25           
        self.reproduction_size = 5            
        self.max_iterations = 15           
        self.mutation_rate = 0.1              
        self.tournament_size = 4            
        self.elitism = 3
      elif(6 < n < 11):
        self.generation_size = 67           
        self.reproduction_size = 17          
        self.max_iterations = 45           
        self.mutation_rate = 0.1              
        self.tournament_size = 8           
        self.elitism = 4
      elif(n < 16):
        self.generation_size = 200          
        self.reproduction_size = 50           
        self.max_iterations = 120         
        self.mutation_rate = 0.1             
        self.tournament_size = 30            
        self.elitism = 15
      elif(n < 20):
        self.generation_size = 250      
        self.reproduction_size = 70         
        self.max_iterations = 250        
        self.mutation_rate = 0.1           
        self.tournament_size = 40       
        self.elitism = 20
      else:
        self.generation_size = 300       
        self.reproduction_size = 100   
        self.max_iterations = 300       
        self.mutation_rate = 0.1        
        self.tournament_size = 50     
        self.elitism = 30

    def calculate_fitness(self, broj):
        count = 0
        while (broj): 
          broj = broj & (broj-1)  
          count+= 1
        return count 

    def sredi(self, broj):
      for el in self.graf:
        if(broj & el == 0):
          broj = (broj | el)
      return broj

    def initial_population(self):
      init_population = []
      for i in range(self.generation_size):
          broj = random.randrange(0, self.m)
          broj = self.sredi(broj)
          fitness = self.calculate_fitness(broj)
          new_chromosome = Chromosome(broj, fitness)
          init_population.append(new_chromosome)
      return init_population

    def selection(self, chromosomes):
        selected = []
        for i in range(self.reproduction_size):
          selected = random.sample(chromosomes, self.tournament_size)
          winner = min(selected, key = lambda x: x.fitness)
          selected.append(winner)
        return selected

    def crossover(self, parent1, parent2):
        break_point = random.randrange(1, self.n)
        child1 = ((parent1 >> self.n-break_point) << (self.n-break_point)) | parent2 & ((1<<n-break_point)-1)
        child2 = ((parent2 >> self.n-break_point) << (self.n-break_point)) | parent1 & ((1<<n-break_point)-1)
        return (child1, child2)

    def mutate(self, genetic_code):
      random_value = random.random()
        
      if random_value < self.mutation_rate:
        random_index = random.randrange(self.n)
        pom_broj = 1 << self.n-random_index-1
        if( (genetic_code | pom_broj) == genetic_code):
          return genetic_code - pom_broj                
        return genetic_code | pom_broj
      return genetic_code


    def create_generation(self, selected_chromosomes, all_chromosomes):
        generation = []
        generation_size = self.elitism
        
        for i in range(self.elitism):
          generation.append(all_chromosomes[i])


        while generation_size < self.generation_size-self.elitism:
            [parent1, parent2] = random.sample(selected_chromosomes, 2)
            child1_code, child2_code = self.crossover(parent1.genetic_code, parent2.genetic_code)
            
            child1_code = self.mutate(child1_code)
            child2_code = self.mutate(child2_code)

            child1_code = self.sredi(child1_code)
            child2_code = self.sredi(child2_code)
            
            child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))
            child2 = Chromosome(child2_code, self.calculate_fitness(child2_code))
            
            generation.append(child1)
            generation.append(child2)
            
            generation_size += 2
            
        return generation


    def optimize(self):
        population = self.initial_population()
        population.sort(key=lambda x: x.fitness)
        for i in range(0, self.max_iterations):
            selected = self.selection(population)
            population = self.create_generation(selected, population)
            population.sort(key=lambda x: x.fitness)    
        return population[0]
