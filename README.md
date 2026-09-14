# MOTH SPECIES DIVERSITY SIMULATOR

## Description:
This project was created with the intention of being used as a tool to investigate how moth species diversity may vary across different habitats. I was inspired to create this after a field trip to Kent. Here, we were tasked with designing hypothetic preliminary experiments which we would investigate in the site, with my group deciding on the exact research question this project aims to investigate:

> How does moth species diversty vary across woodlands and grassland habitats.

Due to time constraints and available resources, we were unable to actually test this research question on site. However, it was around this same time that I had been introduced to the world of computational biology and the use of computer programming to model ecosystems and different populations. While this is in no way a replacement for real-life field work, I have become very interested in the role computational biology and predictive modelling may play in the future of conservational research, especially in a rising age of artificial intelligence. So, I decided this would be an excellent opportunity for me to test these uses myself whilst learning to code using Python!

## Disclaimer:
To model the growth of different populations this programme applies a logistical model, calculating an intrinsic growth rate (*r*) based on the compatability of the diet and environemt for each moth in an environment. This is different to the standard scientific approach, which considers the death and birthrates of a population across generations, however was required due to the lack of available data. To standardise the intrinsic growth rates to a more reasonable value, the `compatability score` calculated for a moth in a habitat was decreased by 0.3. This was becase 0.3 was found to be the median intrinsic growth rate across all of the pre-set moths and habitats I created for this project, which were each created based on data collected during my field study. While the simulation can support the creation of new moth species and habitats, be conscious of this standardisation. This was done so that the success of a moth in a habitat can be compared relative to other species or different habtiats but means no values found are accurate to numbers which may be found in the real world. Moreover, for simplicity sake at the scale of this project, intraspecific competition and predator-prey interactions were disregarded, but would be interesting future developments of this simulation.

## limitations:
- assumes that every plant species in a given habitat are equally abundant
- data, e.g. available flora, moth species, are taken from basic surveying of Badgell's Woods which lacked strong scientific method
- does not account for intraspecific competition
- does not consider predation
- some values, e.g. coverage, are somewhat arbitrary
- seasonal fluctuations are not considered
- used offspring production counts are estimates based on limited data

## How to run it
pip install -r requirements.txt
streamlit run app.py

Use `pytest` to test

## How it works:
Firstly, object oriented programming was used to create the different habitats and moths. This includes a Class `Species` to create a moth spcecies. This Class takes the paramters: species_name, diet, moth_colors, larval_colors, and offspring. Thus, this class creates objects representing a species of moth. Each object/species of moth created using this class is appended into a class attribute called species_lst, which contains every moth species created. Similarly, the Class `Habitat` is used to create a habitat, taking the parameters: habitat_name, colors, flora, and carrying_capacity, as well as a similar list habitat_lst.

To calculate a compatability score for each species in a habitat, compatability was broken down into camoflage and diet. For camoflage, the number of colors in the habitat environment and the colors in the moth_colors and larval_colors. These are the two primary life-stages for a moth and appear wildly different. This score is the proportion of colors in the environment that matches the patterning of the moth, where larval and moth colours are weighted equally. This was calculated using the equation: (moth_matches + larval_matches) / (2 * len(habitat.colors)) in the function `camoflage_compatability_calc()`. The same philosophy was used to calculate a diet compatability score, using the formula: diet_matches / len(habitat.flora) in the function `diet_compatability_calc()`. These two values were averaged in the function `compatability_score_calc()`. As described before, this value was used to calculated an intrinsic growth rate in the function `r_calculator()`.

This value was used to model the population growth of the species in this habitat using the function `pop_growth()`. This used a logistical growth model that follows the equation: P(n+1) = P(n) + rP(n) * (1 - P(n)/K), where P(n) is the population size in generation n and P(n+1) is the population size the next generation. r is the intrinsic growth rate of the population and K is the carrying capacity of the habitat. For this simulation, the offspring count of the moth species was P(n) as to simulate a moth migrating to the habitat and having one successful reproductive cycle. This function creates an array containing the different population sizes each generation.

Streamlit was used to present this data in an accessible way and facilitate the use of the simulation with a user-friendly interface. This website can also be used to create new habitats and moth species, however these are only stored locally to that instance of the webpage. Using this streamlit webpage is demonstrated in the video.