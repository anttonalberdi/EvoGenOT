#### LIBRARIES ####
from opentrons import labware, instruments, modules, robot
import pandas as pd

tag.data = pd.read_csv("ANML.csv")
tag.comb = pd.read_csv("ANML.comb.v1.csv")

#Get number of combinations
tag.comb = len(tag.data)
