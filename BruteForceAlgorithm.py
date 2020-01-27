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
