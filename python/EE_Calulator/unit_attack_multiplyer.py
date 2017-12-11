
import csv

import dbobject as db_obj
import dbfamily as db_fam

# import EE databases
obj = db_obj.object_import()
fam = db_fam.family_import()

# enter indices of needed object fields
name_index = 0
attack_index = 24
attackMode_index = 32
family_index = 2

names = ['']

M = []  # attack multiplier matrix

k_flag = False   # flag for first element



# Calculate attack multipliers for each object
for k in range(len(obj)):   # loop over attacking units

    M_row = []      # next row of multiplier matrix
    l_flag = False    # flag for first element

    # Only calculate for units with non-zero attack
    attack_k = obj[k][attack_index]
    if attack_k <= 0:
        continue

    # name of attacker
    name_k = obj[k][name_index]

    for l in range(len(obj)):   # loop over defending units

        # Only calculate for units with non-zero attack
        attack_l = obj[l][attack_index]
        if attack_l <= 0:
            continue

        # name of defender
        name_l = obj[l][name_index]

        # save names
        print(k)
        if k_flag == False:
            names.append(name_l)
        if l_flag == False:
            M_row.append(name_k)
            l_flag = True

        # Determine coordinates in attack multiplier matrix
        attackMode_k = obj[k][attackMode_index] + 3
        family_l = obj[l][family_index]

        # load attack multiplyer for this unit pair
        multiplier = fam[family_l][attackMode_k]

        M_row.append(multiplier)

    if k_flag == False:
        M.append(names)
        k_flag = True

    M.append(M_row)


with open('../../excel/attack_mult_export.csv', 'w') as export_file:
    export_writer = csv.writer(export_file, delimiter=',')

    for i in range(len(M)):
        export_writer.writerow(M[i])