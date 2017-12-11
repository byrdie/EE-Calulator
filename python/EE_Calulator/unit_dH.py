
import csv

import dbobject as db_obj
import dbfamily as db_fam
import dbweapontohit as db_w2h
import language as l
import epoch_span


# import EE databases
obj = db_obj.object_import()
fam = db_fam.family_import()
w2h = db_w2h.weapontohit_import()
lang = l.language()

# enter indices of needed object fields
name_index = 0
attack_index = 24
attack_speed_index = 11
hitpoints_index = 6
shock_armor_index = 25
arrow_armor_index = 26
pierce_armor_index = 27
gun_armor_index = 28
laser_armor_index = 29
missile_armor_index = 30
attackMode_index = 32
family_index = 2
epoch_index = 4
unitTypeID_index = 36
weapontohitID_index = 23
LanguageId_index = 84


A = []  # Attack matrix
D = []  # Armor tensor
M = []  # Multiplier matrix
W = []  # weapontohit matrix
H = []  # hitpoints matrix
dH = []  # change in hitpoints matrix
dT = []     # dwell time matrix
dHdT = []   # change in hitpoints per unit time
dGdT = []   # percent change in hitpoints per unit time
V = []      # ratio of dGdT for two objects

obj2 = []

names = ['']

for unitTypeID in range(35):
    for epoch in range(1,16):
        for k in range(len(obj)):
            # Sort Unit Type ID
            if obj[k][unitTypeID_index] != unitTypeID:
                continue

            # sort epoch
            if obj[k][epoch_index] != epoch:
                continue

            # name of attacker
            name_k = obj[k][name_index]

            # Only calculate for units with non-zero attack
            attack_k = obj[k][attack_index]
            if attack_k <= 0:
                continue

            # exclude special units
            if name_k[0] == 'x':
                continue

            if obj[k][attack_speed_index] == 0:
                continue

            obj2.append(obj[k])


obj = obj2


k_flag = False  # flag for first element

# Calculate attack multipliers for each object
for k in range(len(obj)):   # loop over attacking units

    A_l = []  # Attack matrix
    D_l = []    # Armor tensor
    M_l = []  # Multiplier matrix
    W_l = []  # weapontohit matrix
    H_l = []  # hitpoints matrix
    dH_l = []  # change in hitpoints matrix
    dT_l = []  # dwell time matrix
    dHdT_l = []  # change in hitpoints per unit time
    dGdT_l = []  # percent change in hitpoints per unit time
    V_l = []  # ratio of dGdT for two objects

    l_flag = False    # flag for first element

    # name of attacker
    langID_k = obj[k][LanguageId_index]
    name_k = lang[langID_k]

    for l in range(len(obj)):   # loop over defending units

        # name of defender
        langID_l = obj[l][LanguageId_index]
        name_l = lang[langID_l]

        # save names
        if k_flag == False:
            names.append(name_l)
        if l_flag == False:
            A_l.append(name_k)
            D_l.append(name_k)
            M_l.append(name_k)
            W_l.append(name_k)
            H_l.append(name_k)
            dH_l.append(name_k)
            dT_l.append(name_k)
            dHdT_l.append(name_k)
            dGdT_l.append(name_k)
            V_l.append(name_k)

            l_flag = True

        # load attack
        a_k = obj[k][attack_index]
        a_l = obj[l][attack_index]


        # load health
        h_k = obj[k][hitpoints_index]
        h_l = obj[l][hitpoints_index]


        # load armor
        d_k = []
        d_l = []
        d_k.append(obj[k][shock_armor_index])
        d_k.append(obj[k][arrow_armor_index])
        d_k.append(obj[k][pierce_armor_index])
        d_k.append(obj[k][gun_armor_index])
        d_k.append(obj[k][laser_armor_index])
        d_k.append(obj[k][missile_armor_index])
        d_l.append(obj[l][shock_armor_index])
        d_l.append(obj[l][arrow_armor_index])
        d_l.append(obj[l][pierce_armor_index])
        d_l.append(obj[l][gun_armor_index])
        d_l.append(obj[l][laser_armor_index])
        d_l.append(obj[l][missile_armor_index])

        # Load attack multiplier
        attackMode_k = obj[k][attackMode_index] + 3     # offset data cells
        attackMode_l = obj[l][attackMode_index] + 3  # offset data cells
        family_k = obj[k][family_index]
        family_l = obj[l][family_index]
        m_kl = fam[family_l][attackMode_k]
        m_lk = fam[family_k][attackMode_l]


        # load weapontohit multiplier
        w2h_k = obj[k][weapontohitID_index]
        w2h_l = obj[l][weapontohitID_index]
        w_kl = w2h[w2h_l][w2h_k + 3]
        w_lk = w2h[w2h_k][w2h_l + 3]


        # load attack speed
        dt_k = obj[k][attack_speed_index]
        dt_l = obj[l][attack_speed_index]


        # calculate change in hitpoints for attacker
        if (m_kl != 0):
            dh_kl = max(a_k * m_kl * w_kl - d_l[w2h_k],1)
        else:
            dh_kl = 0

        # calculate change in hitpoints for defender
        if m_lk != 0:
            dh_lk = max(a_l * m_lk * w_lk - d_k[w2h_l],1)
        else:
            dh_lk = 0


        # calculate change in hitpoints per unit time
        dhdt_kl = dh_kl / dt_k
        dhdt_lk = dh_lk / dt_l


        # calculate percent change in hitpoints per unit time
        dgdt_kl = dhdt_kl / h_l
        dgdt_lk = dhdt_lk / h_k


        # calculate unit fitness score
        if dgdt_kl == 0:
            v_kl = ''
        elif dgdt_lk == 0:
            v_kl = ''
        else:
            v_kl = dgdt_kl / dgdt_lk
        # try:
        #     v_kl = dgdt_kl / dgdt_lk
        # except ZeroDivisionError:
        #     v_kl = ''

        A_l.append(a_k)
        H_l.append(h_l)
        M_l.append(m_kl)
        W_l.append(w_kl)
        dT_l.append(dt_l)
        dH_l.append(dh_kl)
        dHdT_l.append(dhdt_kl)
        dGdT_l.append(dgdt_kl)
        V_l.append(v_kl)


    if k_flag == False:
        A.append(names)
        D.append(names)
        M.append(names)
        W.append(names)
        H.append(names)
        dH.append(names)
        dT.append(names)
        dHdT.append(names)
        dGdT.append(names)
        V.append(names)

        k_flag = True

    A.append(A_l)
    D.append(D_l)
    M.append(M_l)
    W.append(W_l)
    H.append(H_l)
    dH.append(dH_l)
    dT.append(dT_l)
    dHdT.append(dHdT_l)
    dGdT.append(dGdT_l)
    V.append(V_l)

    # A
    # D
    # M
    # W
    # H
    # dH
    # dT
    # dHdT
    # dGdT
    # V

epc = epoch_span.epoch_span()

F = []

# sort into different epoch pages
for epoch in range(1,16):

    F_e = []

    i_flag = False

    F_e.append([ V[0][0] ])

    for i in range(1, len(V)):

        if epc[i - 1][0] == 0: continue

        if epc[i - 1][0] <= epoch and epoch <= epc[i - 1][1]:

            F_i = []

            j_flag = False

            F_i.append(V[i][0])
            F_e[0].append(V[i][0])

            for j in range(1, len(V[0])):

                if epc[j - 1][0] == 0: continue

                if epc[j - 1][0] <= epoch and epoch <= epc[j - 1][1]:

                    F_i.append(V[i][j])


            F_e.append(F_i)

        # else:
        #
        #     F_i = []
        #
        #     for j in range(len(V[0])):
        #
        #         F_i.append(V[i][j])
        #
        #     F_e.append(F_i)





    F.append(F_e)


with open('../../excel/unit_relationships/0_A.csv', 'w') as A_file, \
        open('../../excel/unit_relationships/1_M.csv', 'w') as M_file, \
        open('../../excel/unit_relationships/2_W.csv', 'w') as W_file, \
        open('../../excel/unit_relationships/3_H.csv', 'w') as H_file, \
        open('../../excel/unit_relationships/4_dH.csv', 'w') as dH_file, \
        open('../../excel/unit_relationships/5_dT.csv', 'w') as dT_file, \
        open('../../excel/unit_relationships/6_dHdT.csv', 'w') as dHdT_file, \
        open('../../excel/unit_relationships/7_dGdT.csv', 'w') as dGdT_file, \
        open('../../excel/unit_relationships/8_V.csv', 'w') as V_file:

    A_writer = csv.writer(A_file, delimiter=',')
    M_writer = csv.writer(M_file, delimiter=',')
    W_writer = csv.writer(W_file, delimiter=',')
    H_writer = csv.writer(H_file, delimiter=',')
    dH_writer = csv.writer(dH_file, delimiter=',')
    dT_writer = csv.writer(dT_file, delimiter=',')
    dHdT_writer = csv.writer(dHdT_file, delimiter=',')
    dGdT_writer = csv.writer(dGdT_file, delimiter=',')
    V_writer = csv.writer(V_file, delimiter=',')

    for i in range(len(A)):
        A_writer.writerow(A[i])
        M_writer.writerow(M[i])
        W_writer.writerow(W[i])
        H_writer.writerow(H[i])
        dH_writer.writerow(dH[i])
        dT_writer.writerow(dT[i])
        dHdT_writer.writerow(dHdT[i])
        dGdT_writer.writerow(dGdT[i])
        V_writer.writerow(V[i])



for i in range(1,16):

    with open('../../excel/unit_relationships/epoch/' + str(i) + '.csv', 'w') as F_file:

        F_writer = csv.writer(F_file, delimiter=',')

        for j in range(len(F[i - 1])):

            F_writer.writerow(F[i - 1][j])