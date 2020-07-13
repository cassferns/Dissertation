import random
import csv
import time
import operator
import numpy as np

#Final Year Dissertation

#Test Case Generation for Software Fuzzing using Genetic Programming to Detect Vulnerabilities

#Department of Computer Science
#School of Mathematical and Computer Sciences
#Heriot Watt University Dubai

#Author: Cassandra Ann Fernandes
#Supervisor: Dr. Mohammed Hamdan
#BSc Computer Systems Hons.
#April 23, 2018


N = 100000 #Number of elements
P = 20     #Population size
G = 500     #Generations

pCO = 0.8   #crossover rate
pM = 0.2    #Mutation rate

population = []
individual = []

def partition(arr,low,high):
    i = ( low-1 )         
    pivot = arr[(high+low)/2]     
    for j in range(low , high):
        if arr[j] <= pivot:
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i+1],arr[high] = arr[high],arr[i+1]
    return ( i+1 )
 
def quickSort(arr,low,high):
    if low < high:
        pi = partition(arr,low,high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)
        
def initializeIndividual():
    ind = []
    for j in range(0,N):
        ind.append(random.randint(1,N))
    return ind

class Individual(object):
    ind = []
    fit = -1
    
    def __init__(self ,ind = initializeIndividual()):
        self.ind = ind
        self.fit = self.cal_fitness()
        
    @classmethod
    def cal_fitness(self):
        c1 = time.clock()
       # for k in range(0,R):
        quickSort(self.ind, 0, len(self.ind)-1)
        c2 = time.clock()
        fit = c2 - c1
        #fit = fit* fit
        return fit

    @classmethod
    def display(self):
        print ("Individual: ", self.ind)
        print ("size: ", len(self.ind))
        print ("fitness: ", self.fit)
        
        
def bestfit(p):
    fit = -1
    for i in p:
        if i.fit > fit :
            fit = i.fit;
    return fit   

def bestind(p):
    best = 0
    fit = -1 
    for i in p:
        if i.fit > fit :
            fit = i.fit;
            best = i
    return best.ind 


def generateFromDistribution(p, d, g):
    sum = p[0]
    prob = []
    returned = []
    for i in range(0, d):
        sum = sum + p[i]
        prob.append(sum)
    for i in range(0, g):
        proba = random.random()
        for j in range(0,d):
            if(proba<=prob[j]):
                break
        returned.append(j)
    return returned

def crossOver(i1,i2,d,nPoints): #Crossover function using two crossover points
    if(nPoints==2):
        cut1 = random.randint(0,d-1)
        cut2 = random.randint(0,d-1)
        while cut1==cut2:
            cut2 = random.randint(0,d-1)
        if(cut1>cut2):
            i=cut1
            cut1=cut2
            cut2 = i
        is1 = []
        is2  = []
        for i in range(0,cut1+1):
            is1.append(i1.ind[i])
            is2.append(i2.ind[i])
        for i in range(cut1+1,cut2+1):
            t = i1.ind[i]
            i1.ind[i] = i2.ind[i]
            i2.ind[i] = t
            is1.append(i1.ind[i])
            is2.append(i2.ind[i])
        for i in range(cut2+1,d):
            is1.append(i1.ind[i])
            is2.append(i2.ind[i])
        IS1 = Individual(is1)
        IS2 = Individual(is2)
        p = []
        p.append(IS1)
        p.append(IS2)
        return p

def mutation(ind2, d): #Mutation Function

    m1=random.randint(0,d-1)
    m2=random.randint(0,d-1)
    x = ind2.ind[m1]
    ind2.ind[m1] = ind2.ind[m2]
    ind2.ind[m2] = x
    return ind2
                 
def main():
    population = []
    nextp = []
    nCO = int(P * pCO / 2);
    nM = int(P * pM);
    probabilities = []
    for i in range(0,P):
        is0 = initializeIndividual()
        t= Individual(is0)

        population.append(t)
    for g in range(0,G):
        if (g == 0): 
            np.savetxt('popintial.csv', bestind(population))
        if (g == G-1): 
            np.savetxt('popbest.csv', bestind(population))
        print bestfit(population)
        I=0

        s=0
        for i in population:
            s = s+ i.fit
        for i in population:
            probabilities.append(i.fit/s)
        for i in range(0,nCO):
            chosenOnes = generateFromDistribution(probabilities, P, 2) #selection
            pi = crossOver(population[chosenOnes[0]],population[chosenOnes[1]], N,2)
            nextp.append(pi[0])
            nextp.append(pi[1])
            I=I+2
        for i in range(0,nM):
            chosenOnes = generateFromDistribution(probabilities, P, 1)
            nextp.append(mutation(population[chosenOnes[0]], N))
            I=I+1
        left = P-I
        chosenOnes = generateFromDistribution(probabilities, P, left)
        for i in range(I,P):
            nextp.append(population[chosenOnes[i-I]])
        population = nextp
            
if __name__ == '__main__':
    main()


