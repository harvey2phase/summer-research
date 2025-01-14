import numpy as np

from transforms import transform

#-------------------------------------------------------------------------------
# Run
#-------------------------------------------------------------------------------

def main():

    get_one_data_set(
        "../cnn_data/e4_age80/cohort1/",
        "4",
        "5"
    )

def get_one_data_set(folder, x, y):
    xy = x + "x" + y + "y"

    kind = "train"
    transform(
        folder + y + "y_unbiased_" + kind + "_ind",
        x_years_before_80_dead_in_y_years,
        [
            folder + "unbiased_" + xy + "_" + kind + "_set.txt",
            folder + "unbiased_" + xy + "_" + kind + "_labels.txt",
            x,
            y
        ]
    )
    kind = "eval"
    transform(
        folder + y + "y_unbiased_" + kind + "_ind",
        x_years_before_80_dead_in_y_years,
        [
            folder + "unbiased_" + xy + "_" + kind + "_set.txt",
            folder + "unbiased_" + xy + "_" + kind + "_labels.txt",
            x,
            y
        ]
    )

#-------------------------------------------------------------------------------
# Transformations
#-------------------------------------------------------------------------------

# This function truncates line matrices of 80+ year-olds to matrices that
#   include the health states between 80 and 80-x years, and assigns labels
#   based whether the individual is dead y years after age 80.
# The function appends the truncated matrices in a training file and the labels
#   in a label file. Inidividuals are labeled 1 if they die within y years after
#   age 80, and labeled 0 otherwise
# Parameters:
#   input_folder: folder that contains line matrices
#   filenmae: filename
#   params: string array that contains the following
#     matrix_file: the path to the matrix data file to be written
#     label_file: the path to the label file to be written
#     x: the number of years before 80 to record
#     y: if the individual is dead at/before age 80+y, it is given a label 1
def x_years_before_80_dead_in_y_years(input_folder, filename, params):
    matrix_filename = params[0]
    label_filename = params[1]
    x = int(params[2])
    y = int(params[3])

    matrix = np.loadtxt(input_folder + filename)

    truncated = matrix[:, 80 - x : 80]
    if filename[2].isdigit():
        death_age = int(filename[0] + filename[1] + filename[2], 10)
    else:
        death_age = int(filename[0] + filename[1], 10)

    matrix_file = open(matrix_filename, "a+")
    for row in truncated:
        for state in row:
            matrix_file.write(str(state) + " ")
    matrix_file.write("\n")
    matrix_file.close()

    label_file = open(label_filename, "a+")
    if (death_age <= 80 + y):
        label_file.write("1\n")
    else:
        label_file.write("0\n")
    label_file.close()

#-------------------------------------------------------------------------------
# Call main
#-------------------------------------------------------------------------------

main()
