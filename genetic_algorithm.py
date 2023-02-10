from typing import List, Tuple, Optional
import random

class GeneticAlgorithm(object):
	'''A generic genetic algorithm
		
		We implemented this to train the shark neural network.
		Genetic algorithm follows 6 steps:
			1. initialization, the population
			2. we compute the fitness of every individual in the population
			3. we select the best individual and remove the worst
			4. the very best individuals reproduce to replace the worst, through crossover (gene mixing)
			5. at random, genes of individuals may mutate
			6. goto step 2
	'''

	def __init__(
		self, 
		population: List[List[any]],
		fitness: callable,
		nb_replacement: int,
		mutate_gene: callable,
		mutation_rate: float
	):
		'''constuctor of the Genetic lgorithm object
			inputs:
				* population is a list of individuals that are themselves a list of genes of any type
				* fitness is a function that takes an individual as input and returns a numeric score
				* nb_replacement is how many individuals are replaced at every iteration
				* mutate_gene is a function that given a gene returns another of the same type
				* mutation_rate is the odds of a mutation occuring
		'''

		super(GeneticAlgorithm, self).__init__()

		self.population = [(individual, None) for individual in population]
		self.fitness = fitness
		self.nb_replacement = nb_replacement
		self.mutate_gene  = mutate_gene
		self.mutation_rate = mutation_rate

	def crossover(self, first_parent, second_parent) -> Tuple[List[any], List[any]]:
		cutoff = random.randint(0, len(first_parent) - 1)

		first_sibling = first_parent[:cutoff] + second_parent[cutoff:]
		second_sibling = second_parent[:cutoff] + first_parent[cutoff:]

		return (first_sibling, second_sibling)

	def mutate(self, individual: List[any]) -> List[any]:
		if random.random() < self.mutation_rate:
			gene = random.randint(0, len(individual) - 1)
			individual[gene] = self.mutate_gene(individual[gene])
		return individual

	def darwinist_selection(self) -> None:
		self.population.sort(reverse=True, key=lambda x: x[1])

		for i in range(0, self.nb_replacement, 2):
			parent_a = self.population[i][0]
			parent_b = self.population[i + 1][0]
			first_sibling, second_sibling = self.crossover(parent_a, parent_b)

			self.population[-i-1] = (self.mutate(first_sibling), None)
			self.population[-i-2] = (self.mutate(second_sibling), None)

	def run(self, nb_steps: int, recorder: Optional[callable]):
		for _ in range(nb_steps):
			self.population = [(individual[0], self.fitness(individual)) for individual in self.population]
			self.darwinist_selection()
			recorder(self.population) # logs the update
		

class PrintRecorder(object):
	def __init__(self):
		super(PrintRecorder, self).__init__()
		self.counter = 0

	def __call__(self, arg):
		print(f"{self.counter}:")#" [{out}]")
		print(f"{[x[1] for x in arg]}")
		print("")
		if (self.counter % 100 == 0):
			for p in arg:
			    print(p)
		self.counter += 1

class BigFitTestRecorder(object):
	def __init__(self):
		super(BigFitTestRecorder, self).__init__()
		self.counter = 0
		self.results = []

	def __call__(self, arg):
		out = sum(map(lambda x: 0 if x[1] is None else x[1], arg))
		self.results.append(out)
		self.counter += 1

	def test(self):
		avg_val = sum(self.results) / len(self.results)
		assert self.results[0] <= avg_val and avg_val <= self.results[-1] 

def big_is_better_fit(individual):
	return individual[0][0] + individual[0][1] + individual[0][2]

def naive_genetic_algorithm_test():
	pr = BigFitTestRecorder()
	pop = [[random.randint(0, 10) for _ in range(3)] for _ in range(5)]
	ga = GeneticAlgorithm(
		pop,
		big_is_better_fit,
		1,
		lambda x: x * 1.1,
		0.1
	)
	ga.run(5000, pr)
	pr.test()
	print("PASSED NAIVE GA TEST")

if __name__ == '__main__':
	pr = PrintRecorder()
	pop = [[random.randint(0, 10) for _ in range(3)] for _ in range(5)]
	ga = GeneticAlgorithm(
		pop,
		big_is_better_fit,
		1,
		lambda x: x * 1.1,
		0.1
	)
	ga.run(5000, pr)
	naive_genetic_algorithm_test()