import streamlit as st
import time
from PIL import Image
import matplotlib.pyplot as plt


# Creating moth class ====================================================================================
class Species:
    species_lst = []

    # used to create a species of moth
    def __init__(self, species_name: str, diet: list[str], moth_colors: list[str], larval_colors: list[str], offspring: int) -> None:
        self.species_name = species_name # species name
        self.diet = diet # preferred larval foods (plants)
        self.moth_colors = moth_colors # colors of moth's patterning
        self.larval_colors = larval_colors # colors of the larvae
        self.offspring = offspring # number of offspring produced each generation

        Species.species_lst.append(self)
    

pale_tussock = Species (
    species_name="pale tussock",
    diet=["birch", "hawthorn", "oak"],
    moth_colors=["gray", "white"],
    larval_colors=["yellow", "green"],
    offspring=200)

angle_shades = Species (
    species_name="angle shades",
    diet=["grass", "nettle", "birch", "oak"],
    moth_colors=["light_brown", "dark_brown", "gray"],
    larval_colors=["green"],
    offspring=300)

lime_hawk = Species(
    species_name="lime hawk-moth",
    diet=["birch", "leaves"],
    moth_colors=["green", "dark_brown", "light_brown"],
    larval_colors=["green", "yellow"],
    offspring=150)

brimstone = Species(
    species_name="brimstone moth",
    diet=["bluebell", "buckthorn", "thistles"],
    moth_colors=["yellow", "green"],
    larval_colors=["dark_brown"],
    offspring=100)


# Creating habitat class ==========================================================================================
class Habitat:
    habitat_lst = []

    def __init__(self, habitat_name: str, colors: list[str], flora: list[str], carrying_capacity: int):
        self.habitat_name = habitat_name # habitat name
        self.colors = colors # common colors in the environment
        self.flora = flora # available flora
        self.carrying_capacity = carrying_capacity # carrying capacity of the habitat

        Habitat.habitat_lst.append(self)


grassland = Habitat(
    habitat_name="grassland",
    colors=["green", "light_brown", "yellow", "dark_brown"],
    flora=["hawthorn", "oak", "grass", "nettle"],
    carrying_capacity=2500
)

woodland = Habitat(
    habitat_name="woodland",
    colors=["green", "gray", "dark_brown", "white"],
    flora=["hawthorn", "birch", "bluebell", "buckthorn", "leaves"],
    carrying_capacity=2500
)

# potential colors = green, dark_brown, light_brown, yellow, gray, white
# potential flora = hawthorn, oak, birch, buckthorn, bluebell, grass, nettle, leaves


# running the simulation ==========================================================================================
def camoflage_compatability_calc(moth: Species, habitat: Habitat):
    '''
    Computes a compatability score for the camouflage of a moth species in a habitat.
    This score is the proportion of colors in the environment that matches the patterning of the moth, where larval and moth
    colours are weighted equally.

    Args:
        moth.colors: list of the colours in the moth's patterning
        moth.larval_colors: list of the colours of the larvae
        habitatcolors: list of the colors in the environment of the habitat
        matches: the number of colors in the environment that matches the moth's patterning
    '''
    moth_matches = 0
    larval_matches = 0
    for color in habitat.colors:
        if color in moth.moth_colors:
            moth_matches += 1
        if color in moth.larval_colors:
            larval_matches += 1
    return (moth_matches + larval_matches) / (2 * len(habitat.colors))


def diet_compatability_calc(moth: Species, habitat: Habitat):
    '''
    Computes a compatability score for the diet of a moth species in a habitat. 
    This score is the proportion of available flora that are within the moth's diet

    Args:
        moth.diet: list of the plants in the diet of the given moth
        habitat.flora: list of the available plant species in the area
        matches: the number of plant species' which are in the moth's diet
    '''
    matches = 0
    for plant in habitat.flora:
        if plant in moth.diet:
            matches += 1
    return matches / len(habitat.flora)


def compatability_score_calc(moth: Species, habitat: Habitat):
    '''
    computes a survival score by finding the average of each survival compatibility metric
    '''
    compatability_score = (camoflage_compatability_calc(moth, habitat) + diet_compatability_calc(moth, habitat)) / 2
    return compatability_score


def r_calculator(moth: Species, habitat: Habitat):
    '''
    calculator used to compute the intrinsic growth rate of the each species population
    in a given habitat.  
    '''
    compatability_score = compatability_score_calc(moth, habitat)
    r = compatability_score - 0.3
    return r


def pop_growth(species: Species, habitat: Habitat, n):
    '''
    models population growth according to a Logistic Model
    Args:
        populations: an array storing the population density after each generation
        p_0: the initial population size
        n: the number of generations
        r: intrinsic growth rate
        p_n: the population size in a given genereation
    '''
    p_0 = species.offspring
    populations = [p_0]
    
    r = r_calculator(moth=species, habitat=habitat)

    for i in range(n):
        p_n = populations[i]
        p_n1 = p_n + r * p_n * (1 - p_n / habitat.carrying_capacity)
        populations.append(p_n1)

    return populations

def standard_pop_growth(species: Species, habitat: Habitat, n):
    p_0 = species.offspring
    populations = [p_0]
        
    r = 0.1
    
    for i in range(n):
        p_n = populations[i]
        p_n1 = p_n + r * p_n * (1 - p_n / habitat.carrying_capacity)
        populations.append(p_n1)
    
    return populations


def plot_populations(moth, habitat, n):
    '''
    plots the population growth of each species in a given habitat based on the logistic 
    growth model
    '''
    x = list(range(n + 1))
    y1 = pop_growth(moth, habitat, n)
    y2 = standard_pop_growth(moth, habitat, n)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y1)
    ax.plot(x, y2, color="gray", linestyle = ':')

    ax.set(xlabel='Generation', ylabel='Population size',
           title = f"Logistic growth of {moth.species_name} in the {habitat.habitat_name} against a standard curve (r=0)")
    ax.grid()

    fig.savefig("plot.png")    



# Creating the app / running main() ==========================================================================================


def main():
    st.set_page_config(
        page_title="Simulation"
    )

    st.title("Moth Diversity Simulation")
    st.write("This app is used to simulate the growth of moth populations in different habitats. " \
    "You may use any of the pre-created habitat and moth species, or create new ones using the relevant buttons. " \
    "This tool is in development and is not suitable for scientific use." \
    "\n")

    st.divider(width="stretch")

    # creating and selecting moths 
    st.header("Moths:")

    st.write("Please select the moth species you wish to simulate with. " \
    "Information about all of the moth species can be found in the Moths tab.")

    moth_option = st.selectbox("Select a moth species", options = Species.species_lst,
                            format_func=lambda s: s.species_name.title())

    st.write(f"You have chosen the {moth_option.species_name.title()}")
    st.write("")


    st.write("If you wish to create a new moth species press the button below.")


    if "creating_new_moth" not in st.session_state:
        st.session_state.creating_new_moth = False

    if st.button("Create new moth species"):
        st.session_state.creating_new_moth = True

    if st.session_state.creating_new_moth:
        st.subheader("Create a new moth:")  

        moth_name = st.text_input("Moth Name")

        moth_colors = st.multiselect("Pattern Colors", 
            options=["green", "dark_brown", "light_brown", "yellow", "white", "gray"])

        larval_colors = st.multiselect("Larval Colors",
            options = ["green", "yellow", "brown"])
        
        diet = st.multiselect("Diet",
            options = ["hawthorn", "oak", "birch", "buckthorn", "buckthorn", "grass", "leaves"])

        offspring = st.number_input("Offspring Production", step = 50, min_value=0)

        if st.button("Create moth"):
            if not moth_name or not moth_colors or not larval_colors or not diet or not offspring:
                st.error("Please fill out every field before creating a moth.")
            else:
                new_moth = Species(
                    species_name=moth_name,
                    diet=diet,
                    moth_colors=moth_colors,
                    larval_colors=larval_colors,
                    offspring=offspring
                )

                st.success(f"Created {moth_name.title()}!")
                time.sleep(2)
                st.write(new_moth)
                st.write(type(new_moth))
                st.session_state.creating_new_moth = False
                st.rerun()

        st.divider(width="stretch")



    st.divider(width="stretch")

    # creating and selecting a habitat
    st.header("Habitats:")

    st.write("Please select the habitat you wish to simulate with. " \
    "Information about all of the habitats can be found in the Habitats tab.")

    habitat_option = st.selectbox("Select habitat", options= Habitat.habitat_lst,
                                format_func=lambda s: s.habitat_name.title())
    st.write(f"You have chosen the {habitat_option.habitat_name.title()}")
    st.write("")

    st.write("If you wish to create a new habitat press the button below.")

    if "creating_new_habitat" not in st.session_state:
        st.session_state.creating_new_habitat = False

    if st.button("Create a new habitat"):
        st.session_state.creating_new_habitat = True

    if st.session_state.creating_new_habitat:
        st.subheader("Create a new habitat:")

        habitat_name = st.text_input("Habitat Name")

        habitat_colors = st.multiselect("Habitat colors",
            options = ["green", "dark_brown", "light_brown", "yellow", "gray", "white"])

        habitat_flora = st.multiselect("Habitat flora",
            options = ["hawthorn", "oak", "birch", "buckthorn", "buckthorn", "grass", "leaves"])

        carrying_capacity = st.number_input("Carrying Capacity", step = 1000, min_value=0)

        if st.button("Create habitat"):
            if not habitat_name or not habitat_colors or not habitat_flora or not carrying_capacity:
                st.error("Please fill out every field before creating a habitat")
            else:
                woodland = Habitat(
                    habitat_name=habitat_name,
                    colors=habitat_colors,
                    flora=habitat_flora,
                    carrying_capacity=carrying_capacity)

                st.success(f"Created {habitat_name}!")
                time.sleep(2)
                st.session_state.creating_new_moth = False
                st.rerun()

    st.divider(width="stretch")

    # running the simulation
    st.header("Simulation:")
    st.write("")
    st.write(f"Moth: {moth_option.species_name.title()}")
    st.write(f"Habitat: {habitat_option.habitat_name.title()}")
    st.write("")
    generations = st.number_input("How many generations would you like to simulate",
                    min_value=0, step=10)
    st.write("")
    st.write("")

    def run_simulation():
        plot = plot_populations(moth=moth_option, habitat=habitat_option, n=generations)

        image = Image.open('plot.png')
        st.image(image, width=680)

    if "running_simulation" not in st.session_state:
        st.session_state.running_simulation = False

    if st.button("Run simulation"):
        st.session_state.running_simulation = True

    if st.session_state.running_simulation:
        st.subheader("Running simulation:")
        run_simulation()
        st.write(f"This graph shows the logistic growth of {moth_option.species_name.title()} in {habitat_option.habitat_name.title()} in the blue line. "\
            "The gray dotted line represents the growth model for a slightly growing populations \(r=0.1\). "\
                "Thank you for using this simulation!")

        if st.button("Finish Simulation"):
            st.session_state.running_simulation = False

    st.divider(width="stretch")

if __name__ == "__main__":
    main()
