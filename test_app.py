import pytest

from moths import Species
from habitats import Habitat
import sim

## sim.py

def test_camoflage_compatability_calc():

    h = Habitat(
    habitat_name="woodland",
    colors=["green", "gray", "dark_brown", "white"],
    flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
    carrying_capacity=250000)
        
    s = Species (
    species_name="pale tussock",
    diet=["birch", "hawthorn", "oak"],
    moth_colors=["gray", "white"],
    larval_colors=["yellow", "green"],
    offspring=200)

    result = sim.camoflage_compatability_calc(habitat=h, moth=s)

    if not isinstance(result, float):
        raise TypeError(f"Camoflage compatability score is not an integer, got {type(result)}")

    
    assert result == pytest.approx(0.375)
    

def test_diet_compatability_calc():

    h = Habitat(
        habitat_name="woodland",
        colors=["green", "gray", "dark_brown", "white"],
        flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
        carrying_capacity=250000)
        
    s = Species (
        species_name="pale tussock",
        diet=["birch", "hawthorn", "oak"],
        moth_colors=["gray", "white"],
        larval_colors=["yellow", "green"],
        offspring=200)

    result = sim.diet_compatability_calc(habitat=h, moth=s)

    if not isinstance(result, float):
        raise TypeError(f"Diet compatability score is not an integer, got {type(result)}")
    
    assert result == pytest.approx(0.4)
    

def test_compatability_score_calc():

    h = Habitat(
        habitat_name="woodland",
        colors=["green", "gray", "dark_brown", "white"],
        flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
        carrying_capacity=250000)
        
    s = Species (
        species_name="pale tussock",
        diet=["birch", "hawthorn", "oak"],
        moth_colors=["gray", "white"],
        larval_colors=["yellow", "green"],
        offspring=200)

    result = sim.compatability_score_calc(habitat=h, moth=s)

    if not isinstance(result, float):
        raise TypeError(f"Compatability score is not an integer, got {type(result)}")

    assert result == pytest.approx(0.3875)


def test_r_calculator():
    h = Habitat(
    habitat_name="woodland",
    colors=["green", "gray", "dark_brown", "white"],
    flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
    carrying_capacity=250000)
        
    s = Species (
        species_name="pale tussock",
        diet=["birch", "hawthorn", "oak"],
        moth_colors=["gray", "white"],
        larval_colors=["yellow", "green"],
        offspring=200)

    result = sim.r_calculator(moth=s, habitat=h)

    if not isinstance(result, float):
        raise TypeError(f"r value is not an integer, got {type(result)}")

    assert result == pytest.approx(0.0875)

    
def test_pop_growth():
    h = Habitat(
    habitat_name="woodland",
    colors=["green", "gray", "dark_brown", "white"],
    flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
    carrying_capacity=250000)
        
    s = Species (
    species_name="pale tussock",
    diet=["birch", "hawthorn", "oak"],
    moth_colors=["gray", "white"],
    larval_colors=["yellow", "green"],
    offspring=200)

    populations = sim.pop_growth(species=s, habitat=h, n=10)

    assert populations == [200, 217.486, 236.4994699439314, 257.1735973642761, 279.6531387429368, 304.0954163256407, 330.67139934635367, 359.5668765381386, 390.98372731667956, 425.14129956062976, 462.27790247857763]


## moths.py

def test_species_init():
    Species.species_lst = []

    lime_hawk = Species(
    species_name="lime hawk-moth",
    diet=["birch", "leaves"],
    moth_colors=["green", "dark_brown", "light_brown"],
    larval_colors=["green", "yellow"],
    offspring=150)

    assert lime_hawk.species_name == "lime hawk-moth"
    assert lime_hawk.diet == ["birch", "leaves"]
    assert lime_hawk.moth_colors == ["green", "dark_brown", "light_brown"]
    assert lime_hawk.larval_colors == ["green", "yellow"]
    assert lime_hawk.offspring == 150

    if len(lime_hawk.diet) == 0:
        raise ValueError("No diet given for moth")

    if len(lime_hawk.moth_colors) == 0:
        raise ValueError("No colors given for moth patterning")

    if len(lime_hawk.larval_colors) == 0:
        raise ValueError("No colors given for moth larvae")

    if not isinstance(lime_hawk.offspring, int):
        raise TypeError("Offspring count is not an integer")


def test_species_lst():
    Species.species_lst = []

    lime_hawk = Species(
    species_name="lime hawk-moth",
    diet=["birch", "leaves"],
    moth_colors=["green", "dark_brown", "light_brown"],
    larval_colors=["green", "yellow"],
    offspring=150)

    brimstone = Species(
    species_name="brimstone moth",
    diet=["bluebell", "buckthorn", "thistles"],
    moth_colors=["yellow", "brown"],
    larval_colors=["green"],
    offspring=100)

    assert Species.species_lst == [lime_hawk, brimstone]

## habitats.py

def test_habitat_init():
    Habitat.habitat_lst = []

    grassland = Habitat(
    habitat_name="grassland",
    colors=["green", "light_brown", "yellow", "dark_brown"],
    flora=["hawthorn", "oak", "grass", "nettle"],
    carrying_capacity=250000
    )

    assert grassland.habitat_name == "grassland"
    assert grassland.colors == ["green", "light_brown", "yellow", "dark_brown"]
    assert grassland.flora == ["hawthorn", "oak", "grass", "nettle"]
    assert grassland.carrying_capacity == 250000

    if len(grassland.colors) == 0:
        raise ValueError("There are no colors given to this habitat")

    if len(grassland.flora) == 0:
        raise ValueError("There are no plants given to this habitat")

    if not isinstance(grassland.carrying_capacity, int):
        raise TypeError("Carrying Capacity is not an integer")


def test_habitat_lst():
    Habitat.habitat_lst = []

    grassland = Habitat(
    habitat_name="grassland",
    colors=["green", "light_brown", "yellow", "dark_brown"],
    flora=["hawthorn", "oak", "grass", "nettle"],
    carrying_capacity=250000
    )

    woodland = Habitat(
    habitat_name="woodland",
    colors=["green", "gray", "dark_brown", "white"],
    flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
    carrying_capacity=250000
    )

    assert  Habitat.habitat_lst == [grassland, woodland]