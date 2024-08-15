# Ensure necessary libraries are loaded
library(dplyr)
library(tidyr)
library(readxl)
library(greybox)

Check <- read_excel("Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Check.xlsx")
# Assuming 'Check' is your data frame
Check <- Check %>%
  select(Cp, Number of Childrens, Desired Expansion Policy, Ratio Expansion, Desired Simulation Policy, Time to find the solution, Total Cost)
spread(Check)
