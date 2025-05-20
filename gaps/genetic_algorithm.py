from __future__ import print_function
from operator import attrgetter

from gaps import utils
from gaps.crossover import Crossover
from gaps.image_analysis import ImageAnalysis
from gaps.individual import Individual
from gaps.progress_bar import print_progress
from gaps.selection import roulette_selection
from gaps.progress_plot import ProgressPlot
from gaps.mutate import mutate  # ✅ Mutation module


class GeneticAlgorithm(object):
    TERMINATION_THRESHOLD = 10

    def __init__(self, image, piece_size, population_size, generations, elite_size=2, mutation_rate=0.01):
        self._image = image
        self._piece_size = piece_size
        self._generations = generations
        self._elite_size = elite_size
        self._mutation_rate = mutation_rate  # ✅ Store mutation rate
        pieces, rows, columns = utils.flatten_image(image, piece_size, indexed=True)
        self._population = [
            Individual(pieces, rows, columns) for _ in range(population_size)
        ]
        self._pieces = pieces

    def start_evolution(self, verbose):
        print(f">>> start_evolution() called with verbose = {verbose}")
        if verbose:
            plot = ProgressPlot()

        print("=== Pieces:      {}\n".format(len(self._pieces)))

        ImageAnalysis.analyze_image(self._pieces)

        fittest = None
        best_fitness_score = float("-inf")
        termination_counter = 0

        for generation in range(self._generations):
            print_progress(
                generation, self._generations - 1, prefix="=== Solving puzzle: "
            )

            new_population = []

            # Elitism
            elite = self._get_elite_individuals(elites=self._elite_size)
            new_population.extend(elite)

            selected_parents = roulette_selection(
                self._population, elites=self._elite_size
            )

            for first_parent, second_parent in selected_parents:
                crossover = Crossover(first_parent, second_parent)
                crossover.run()
                child = crossover.child()

                # ✅ Apply mutation here
                child = mutate(child, self._mutation_rate)

                new_population.append(child)

            fittest = self._best_individual()

            if fittest.fitness <= best_fitness_score:
                termination_counter += 1
            else:
                best_fitness_score = fittest.fitness
                termination_counter = 0

            if termination_counter == self.TERMINATION_THRESHOLD:
                print("\n\n=== GA terminated")
                print(
                    "=== There was no improvement for {} generations".format(
                        self.TERMINATION_THRESHOLD
                    )
                )
                if verbose:
                    plot.finish()
                return fittest

            self._population = new_population

            if verbose:
                plot.show(fittest.to_image(), f"Generation {generation + 1}")

        if verbose:
            plot.finish()
        return fittest

    def _get_elite_individuals(self, elites):
        return sorted(self._population, key=attrgetter("fitness"))[-elites:]

    def _best_individual(self):
        return max(self._population, key=attrgetter("fitness"))
