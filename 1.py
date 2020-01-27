import random
import time
import copy

def generisi_graf(n):
  m = 2**n
  lista = []
  for i in range(n):
    broj = random.randrange(0, m)
    #obezbedjuje se da je sam taj cvor ukljucen u spisku cvorova 
    #za taj cvor
    broj = broj | (1 << n-i-1)
    lista.append(broj)
  return lista

def generisi_graf_sa_manje_grana(n):
  lista = []
  for i in range(n):
    broj = 0
    for j in range(random.randrange(n-random.randrange(n))):
      broj = broj | (1 << random.randrange(n))
    
   
    if broj==0 or broj == (1 << n-i-1):
      rand=0
      while(True):
        rand = random.randrange(n)
        if(rand!=i):
          break
      broj = broj | (1 << n-rand-1)
    broj = broj | (1 << n-i-1)
    lista.append(broj)
  return lista

def generisi_neusmereni_graf(n):
  lista = []
  for i in range(n):
    broj = 0
    for j in range(random.randrange(n-random.randrange(n))):
      broj = broj | (1 << random.randrange(n))
    
   
    if broj==0 or broj == (1 << n-i-1):
      rand=0
      while(True):
        rand = random.randrange(n)
        if(rand!=i):
          break
      broj = broj | (1 << n-rand-1)
    #obezbedjuje se da je sam taj cvor ukljucen u spisku cvorova 
    #za taj cvor
    broj = broj | (1 << n-i-1)
    lista.append(broj)

  for i in range(n):
    for j in range(n):
      if (1 << n-j-1) & lista[i] != 0:
        lista[j] |= (1<<n-i-1)
  return lista


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

def validno(broj, graf):
      for el in graf:
        if(broj & el == 0):
          return False
      return True


def brute_force_algorithm(n, graf, genetic_algorithm):
  min_resenje = float('inf')
  resenja = []
  m = 2**n
  for broj in range(m):
    if validno(broj, graf):
      fitness = genetic_algorithm.calculate_fitness(broj)
      if fitness < min_resenje:
        resenja = [(broj, fitness)]
        min_resenje = fitness
      elif fitness == min_resenje:
          resenja.append((broj, fitness))
  return resenja

def ispisi_graf(graf):
  n = len(graf)
  for i in range(n):
    print("{}:".format(i+1), end=' ')
    print("[ ", end='')
    for j in range(n):
      if(i!=j):
        if(graf[i]&(1<<(n-j-1))):
          print("{}".format(j+1), end=' ')
    print("]")
      
def ispisi_resenje(resenje, n):
  print("[ ", end='')
  for i in range(n):
    if(resenje&(1<<(n-i-1))):
      print("{}".format(i+1), end=' ')
  print("]") 


"""
---------------------------------------------------------------------------------------------------------------
"""

def calculate_fitness(graf):
  count_global = -1
  jedinka_global = -1
  for jedinka in graf:
    count = 0
    jedina_copy = jedinka
    while (jedinka): 
      jedinka = jedinka & (jedinka-1)  
      count+= 1
    if(count_global < count):
      count_global = count
      jedinka_global = jedina_copy
  return jedinka_global




def prva_fja(graf):
  for a in graf:
    for b in graf:
      if a != b:
        if a & b == a:
          return a
        elif a & b == b:
          return b
  return -1

def druga_fja(graf):
  count = 0
  unique = -1
  vrednost = calculate_fitness(graf)
  k = 0
  while( (1<<k) <= vrednost):
    k+=1
  
  for i in range(k):
    for j in graf:
      if 1 << (k-i-1) & j:
        if count==0:
          count += 1
          unique = j
        else:
          count = 0
          unique = -1
          break
    if(count==1):
      return unique 
  return -1


def delet(graf, vrednost):
  i = 0
  while( (1<<i) <= vrednost):
    i+=1
  maska = (1 << i)-1
  maska = maska&vrednost
  for i in range(len(graf)):
    if graf[i] & maska != 0:
      graf[i] = graf[i] - (graf[i] & maska)
  graf = list(filter(lambda x: x!=0, graf))
  return graf

def obrisi(graf, promenljiva):
  graf = copy.copy(graf)
  graf.remove(promenljiva)
  return graf

def MSC(graf):
  if(len(graf)==0):
    return 0

  promenljiva = prva_fja(graf)
  if promenljiva != -1:
    graf = obrisi(graf,promenljiva)
    return MSC(graf)

  vrednost = druga_fja(graf)
  if(vrednost!=-1):
    graf = delet(graf,vrednost)
    return 1 + MSC(graf)

  s = calculate_fitness(graf)
  pom_graf = copy.copy(graf)
  return min( MSC(obrisi(pom_graf,s)),
              1 + MSC(delet(pom_graf,s)))



"""
---------------------------------------------------------------------------------------------------------------
"""

#count = 0
s = 1
n = int(input("Број чворова у графу: "))
genetic_algorithm_time = 0
brute_force_algorithm_time = 0
for i in range(s):
  
  a = generisi_neusmereni_graf(n)
  #ispisi_graf(a)
  genetic_algorithm = GeneticAlgorithm(a, n)
  start_time = time.time()
  best_solution = genetic_algorithm.optimize()
  #print("Време генетског алгоритма: ")
  genetic_algorithm_time += (time.time() - start_time)
  #print("%s сек" % (genetic_algorithm_time))
  print(best_solution.fitness )
  #print("Решење пронађено генетским алгоритмом:")
  #ispisi_resenje(best_solution.genetic_code, n)

  #start_time = time.time()
  #resenje_brute_force = brute_force_algorithm(n,a, genetic_algorithm)
  #brute_force_algorithm_time += (time.time() - start_time)
  #print("Алгоритам грубе силе: ")
  #print("%s сек" % (brute_force_algorithm_time))

  #print("Решења:")
  #for resenje in resenje_brute_force:
  #  ispisi_resenje(resenje[0], n)
  #resenje_brute_force = [resenje[0] for resenje in resenje_brute_force]
  #if best_solution.genetic_code in resenje_brute_force:
  #  print("Решење је тачно")
  #  count+=1
    #print()
  #else:
  #  print("Решење је нетачно")
  #  print("Право решење има {} чворова".format(genetic_algorithm.calculate_fitness(resenje_brute_force[0])))


#print("Алгоритам је погодио у %.2f%% случајева" % (count/s*100))
print("Време генетског алгоритма: ")
print("%s сек" % (genetic_algorithm_time))

#print("Алгоритам грубе силе: ")
#print("--- %s сек ---" % (brute_force_algorithm_time))

#start_time = time.time()
#msc = MSC(a)
#print("MSC алгоритам: ")
#print("%s сек" % (time.time() - start_time))
#print("Резултат MSC алгоритма: " + str(msc))
