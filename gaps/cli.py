import click
import cv2 as cv
import numpy as np

from gaps import utils
from gaps.genetic_algorithm import GeneticAlgorithm
from gaps.size_detector import SizeDetector

DEFAULT_GENERATIONS = 20
DEFAULT_POPULATION = 200

MIN_PIECE_SIZE = 32
MAX_PIECE_SIZE = 128


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "ignore_unknown_options": True,
    }
)
def cli():
    """Solve or create puzzles with square pieces."""


def _validate_piece_size(_context, _param, value):
    if value < MIN_PIECE_SIZE:
        raise click.BadParameter(f"Minimum piece size is {MIN_PIECE_SIZE} pixels")
    if value > MAX_PIECE_SIZE:
        raise click.BadParameter(f"Maximum piece size is {MAX_PIECE_SIZE} pixels")
    return value


def _validate_positive_integer(_context, _param, value):
    if value <= 0:
        raise click.BadParameter("Should be a positive integer.")
    return value


@click.command()
@click.argument("puzzle", type=click.Path(exists=True, readable=True))
@click.argument("solution", type=click.Path(dir_okay=False, writable=True))
@click.option("-s", "--size", type=int, help="Size of single square puzzle piece in pixels. Autodetected if not specified.")
@click.option("-g", "--generations", type=int, show_default=True, default=DEFAULT_GENERATIONS, callback=_validate_positive_integer, help="The number of generations for genetic algorithm.")
@click.option("-p", "--population", type=int, show_default=True, default=DEFAULT_POPULATION, callback=_validate_positive_integer, help="The size of the initial population for genetic algorithm.")
@click.option("-d", "--debug", is_flag=True, default=False, help="If enabled, shows the best individual after each generation.")
def run(puzzle, solution, size, generations, population, debug):
    """Run puzzle solver."""
    input_puzzle = cv.imread(puzzle)

    if size is None:
        detector = SizeDetector(input_puzzle)
        size = detector.detect()

    click.echo(f"Population: {population}")
    click.echo(f"Generations: {generations}")
    click.echo(f"Piece size: {size}")

    ga = GeneticAlgorithm(
        image=input_puzzle,
        piece_size=size,
        population_size=population,
        generations=generations,
    )
    result = ga.start_evolution(debug)  # ✅ Pass debug here
    output_image = result.to_image()

    cv.imwrite(solution, output_image)
    click.echo("Puzzle solved")


@click.command()
@click.argument("image", type=click.Path(exists=True, readable=True))
@click.argument("puzzle", type=click.Path(writable=True))
@click.option("-s", "--size", type=int, show_default=True, default=MAX_PIECE_SIZE, callback=_validate_piece_size, help="Size of single square puzzle piece in pixels.")
def create(image, puzzle, size):
    """Create jigsaw puzzle with square pieces."""
    input_image = cv.imread(image)
    pieces, rows, columns = utils.flatten_image(input_image, size)
    np.random.shuffle(pieces)
    output_image = utils.assemble_image(pieces, rows, columns)
    cv.imwrite(puzzle, output_image)
    click.echo(f"\nCreated puzzle with {len(pieces)} pieces")


cli.add_command(run, name="run")
cli.add_command(create, name="create")

if __name__ == "__main__":
    cli()
