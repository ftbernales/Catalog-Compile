CASE="bolinao-cat"

# Merging catalogues
ARG1="./settings/merge_$CASE.toml"
oqm cat merge $ARG1

# Creating the homogenised catalogue
ARG1="./settings/homogenise_$CASE.toml"
ARG2="./h5/$CASE_otab.h5"
ARG3="./h5/$CASE_mtab.h5"

oqm cat homogenise $ARG1 $ARG2 $ARG3

# Checking the homogenised catalogue
ARG1="./settings/check_$CASE.toml"
ARG2="./h5/$CASE_homogenised.h5"

oqm cat check_duplicates $ARG1 $ARG2

# Create .csv
ARG3="./csv/catalogue_$CASE.csv"
oqm cat create_csv $ARG2 $ARG3