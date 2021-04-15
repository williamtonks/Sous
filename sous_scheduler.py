import csv

class Substitution:
    def __init__(self, original_amount, substitutes):
        self.original_amount = original_amount
        self.substitutes = substitutes

def open_and_parse_substitution_list(master_list):
    substitutions = {}
    with open(master_list, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            substitutions[row[0]] = Substitution(row[1], row[2].split(','))
    return substitutions


substitution_dict = open_and_parse_substitution_list('test_files_substitution/substitution_master_list.csv')