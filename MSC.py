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
