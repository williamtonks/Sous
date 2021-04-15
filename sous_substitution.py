#!/usr/bin/env python

import csv
import re

def fraction_as_float(fraction):
    

def standard_to_ml(measurement_text):
    broken_text = measurement_text.split(' ')
    if broken_text[-1] == "cup" or broken_text[-1] == "cups":
        return milli
    elif broken_text[-1] == "tablespoon" or broken_text[-1] == "tablespoons":
        return milli
    elif broken_text[-1] == "teaspoon" or broken_text[-1] == "teaspoon":
        return milli
    elif broken_text[-1] == "ounce" or broken_text[-1] == "ounces":
        return milli
    else:
        return "Not a Volume Measurement"
    

class Substitution:

    def __init__(self, substitute):
        self.original_text = substitute
        substitute = substitute.strip()
        self.components = self.find_all_components(substitute)
    
    def find_all_components(self, substitute):
        # all substitutions stored in mL
        broken_text = substitute.split(' ')
        current_string = ""
        current_component = [' ', ' ']
        i = 0
        setting_number = True
        while i < range(len(broken_text)):
            if setting_number:
                
            else:


    def print_self(self):
        print(self.original_text)
            

class Substitution_Set:
    def __init__(self, original_amount, substitutes):
        self.original_amount = original_amount
        self.substitutes = [Substitution(item) for item in substitutes]
    
    def print_potential_substitutes(self):
        for item in self.substitutes:
            item.print_self()

def open_and_parse_substitution_list(master_list):
    substitutions = {}
    with open(master_list, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            substitutions[row[0]] = Substitution_Set(row[1], row[2].split(','))
    return substitutions

substitution_dict = open_and_parse_substitution_list('test_files_substitution/substitution_master_list.csv')
