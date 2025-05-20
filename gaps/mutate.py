import random

def mutate(individual, mutation_rate):
    """Randomly swaps two pieces in the individual with given mutation rate."""
    if random.random() < mutation_rate:
        pieces = individual.pieces[:]
        idx1, idx2 = random.sample(range(len(pieces)), 2)
        pieces[idx1], pieces[idx2] = pieces[idx2], pieces[idx1]
        
        # Recreate the individual without shuffling
        mutated = individual.__class__(
            pieces=pieces,
            rows=individual.rows,
            columns=individual.columns,
            shuffle=False
        )
        return mutated
    return individual
