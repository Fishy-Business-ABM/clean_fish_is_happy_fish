from functools import reduce
from math import sin, cos
from model import Model
from agent import Agent
from typing import Tuple, List

class Neuron(object):
	def __init__(
		self,
		weights,
		sigmoid # the normalization function used
	):
		super(Neuron, self).__init__()
		self.weights = weights
		self.sigmoid = sigmoid

	def __call__(self, input_data):
		return self.sigmoid(sum([self.weights[i] * input_data[i] for i in range(len(self.weights))]))

	def __str__(self):
		return str(self.weights)


class Shark(Agent):
	"""docstring for Shark"""
	def __init__(
		self,
		model: Model,
		pos: Tuple[float],
		perception: float,
		nb_seeable_fish: int,
		nb_deep_neurons: int,
		weights: List[float],
		eat_radius: float,
		energy: float,
		metabolism: float	
	):
		super(Shark, self).__init__(pos)

		self.model = model
		self.model.add_entity(self)
		self.perception = perception
		self.nb_seeable_fish = nb_seeable_fish
		self.eat_radius = eat_radius
		self.energy = energy
		self.metabolism = metabolism
		
		# now we create the brain, which is basically putting structure to the weigts		
		nb_weight_per_deep_neuron = nb_seeable_fish * 2
		end_deep_neurons = nb_weight_per_deep_neuron * nb_deep_neurons

		deep_layer = [
			Neuron(
				weights[i * nb_weight_per_deep_neuron: (i + 1) *nb_weight_per_deep_neuron],
				lambda x: x
			)
			for i in range(nb_deep_neurons)
		]

		# assuming 2D, 1 for angle 1 for norm
		end_angle_out = end_deep_neurons + nb_deep_neurons

		# maybe make a better sigmoid for the output if we notice gradient explosions?
		# also, for the angle output, we want to restrain that
		# for the norm out, we also want to restrain that, so there a sigmoid is needed
		angle_out = Neuron(weights[end_deep_neurons:end_angle_out], lambda x: x)
		norm_out = Neuron(weights[end_angle_out:], lambda x: x)

		out_layer = [angle_out, norm_out]

		self.brain = [deep_layer, out_layer]

	# Find bounded number of fish within perception
	def seeable_prey(self):
		prey = list(self.model.get_neighbors_w_distance(self, self.perception, False))
		prey.sort(key=lambda x: x[1]) # sort them by who is closer

		prey = prey[:self.nb_seeable_fish]

		return prey

	# Move according to neural net
	def move(self, prey):
		prey_positions = reduce(lambda acc, elm: acc + [elm[0].pos[0]] + [elm[0].pos[1]], prey, [])
		prey_positions += [0 for _ in range(2 * self.nb_seeable_fish - len(prey_positions))]

		intermediary_outputs = [prey_positions]
		for layer in self.brain:
			intermediary = [neuron(intermediary_outputs[-1]) for neuron in layer]
			intermediary_outputs.append(intermediary)

		angle, norm = intermediary_outputs[-1][0], intermediary_outputs[-1][1]
		new_x = self.pos[0] + norm * cos(angle)
		new_y = self.pos[1] + norm * sin(angle)
		self.pos = (new_x, new_y)

	# Eat potential prey within eating radius
	def eat(self, prey):
		for fish,dist in prey:
			if dist <= self.eat_radius:
				self.energy += 1
				self.model.remove_entity(fish)

	# Do metabolism and possibly die
	def metabolize(self):
		self.energy -= self.metabolism

		if self.energy < 0:
			self.model.remove_entity(self)

	def step(self):
		prey = self.seeable_prey()

		self.move(prey)
		self.eat(prey)
		self.metabolize()

		
