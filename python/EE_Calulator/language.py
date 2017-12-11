import csv


def language():

    maxID = 33005

    with open('../../data/Language.txt','r') as lang_file:
        lang_stream = csv.reader(lang_file, delimiter=',')

        j = 0

        lang = []

        lang = [0] * (maxID + 1)

        for row in lang_stream:

            lang_id = int(row[0])
            lang_name = row[1].replace('"','')

            lang[lang_id] = lang_name
            j = j + 1


    return lang