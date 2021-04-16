#!/usr/bin/env python

import csv
import json
import re
from fractions import Fraction

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

def standard_mass_to_grams(measurement_text):
    measurement_text = measurement_text.strip()
    broken_text = measurement_text.split(' ')
    if broken_text[-1] == "pound" or broken_text[-1] == "pounds":
        # 1 pound is 453.592 grams
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(453.592)
    elif broken_text[-1] == "ounce" or broken_text[-1] == "ounces":
        # 1 tablespoon = 14.7868 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(28.3495)
    else:
        return "Not a Mass Measurement"

def standard_volume_to_ml(measurement_text):
    measurement_text = measurement_text.strip()
    broken_text = measurement_text.split(' ')
    if broken_text[-1] == "cup" or broken_text[-1] == "cups":
        # 1 cup = 236.588 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(236.588)
    elif broken_text[-1] == "tablespoon" or broken_text[-1] == "tablespoons":
        # 1 tablespoon = 14.7868 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(14.7868)
    elif broken_text[-1] == "teaspoon" or broken_text[-1] == "teaspoons":
        # 1 teaspoon = 4.92892 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(4.92892)
    elif broken_text[-1] == "ounce" or broken_text[-1] == "ounces":
        # 1 ounce = 29.5735 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(29.5735)
    elif broken_text[-1] == "pint" or broken_text[-1] == "pints":
        # 1 pint = 473.176 mL
        value = " ".join(broken_text[:-1])
        value = convert_to_float(value)
        return value * float(473.176)
    else:
        return "Not a Volume Measurement"
    
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def convertML_to_standard_volume(amount):
    # conversion : full cups, tablespoons, teaspoons, quarter teaspoons
    # since cooking instructions are by in large improper in terms of volume
    # the volumes outputted are rounded to approximate fractional amounts
    conversion = [0, 0, 0, 0]
    fractional = ""
    while amount >= 236.588: #pound
        amount = amount - 236.588
        conversion[0] += 1
    while amount >= 28.3495: #ounce
        amount = amount - 28.3495
        conversion[1] += 1
    while amount >= 3.54368: #eigth of an ounce
        amount = amount - 3.54368
        conversion[2] += 1
    combined_measurement = ""
    if conversion[0] == 1:
        combined_measurement = combined_measurement + str(conversion[0]) + " pound, "
    elif conversion[0] > 1:
        combined_measurement = combined_measurement + str(conversion[0]) + " pound, "
    if conversion[1] == 1:
        if conversion[2] >= 1:
            fractional_amount = Fraction(conversion[2], 4)
            return combined_measurement + str(conversion[1]) + " " + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " ounces "
        return combined_measurement + str(conversion[1]) + " ounce "
    elif conversion[1] > 1:
        if conversion[2] >= 1:
            fractional_amount = Fraction(conversion[2], 8)
            return combined_measurement + str(conversion[1]) + " " + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " ounces "
        return combined_measurement + str(conversion[1]) + " ounces "
    return combined_measurement.strip(',')

def convert_grams_to_standard_mass(amount):
    # conversion : full cups, tablespoons, teaspoons, quarter teaspoons
    # since cooking instructions are by in large improper in terms of volume
    # the volumes outputted are rounded to approximate fractional amounts
    conversion = [0, 0, 0]
    fractional = ""
    while amount >= 453.592:
        amount = amount - 453.592
        conversion[0] += 1
    while amount >= 14.7868:
        amount = amount - 14.7868
        conversion[1] += 1
    while amount >= 4.92892:
        amount = amount - 4.92892
        conversion[2] += 1
    while amount >= 1.23:
        amount = amount - 1.23
        conversion[3] += 1
    if conversion[0] >= 1 and conversion[1] >= 2:
        if conversion[1] % 2 == 1:
            conversion[1] += 1
        fractional_amount = Fraction(conversion[1], 16)
        return str(conversion[0]) + " " + str(fractional_amount.numerator)+ "/" + str(fractional_amount.denominator) + " cups"
    combined_measurement = ""
    if conversion[0] == 1:
        combined_measurement = combined_measurement + str(conversion[0]) + " cup, "
    elif conversion[0] > 1:
        combined_measurement = combined_measurement + str(conversion[0]) + " cups, "
    if conversion[1] == 1:
        combined_measurement = combined_measurement + str(conversion[1]) + " tablespoon, "
    elif conversion[1] > 1:
        combined_measurement = combined_measurement + str(conversion[1]) + " tablespoons, "
    if conversion[2] == 1:
        if conversion[3] >= 1:
            fractional_amount = Fraction(conversion[3], 4)
            return combined_measurement + str(conversion[2]) + " " + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " teaspoons "
        return combined_measurement + str(conversion[2]) + " teaspoon "
    elif conversion[2] > 1:
        if conversion[3] >= 1:
            fractional_amount = Fraction(conversion[3], 4)
            return combined_measurement + str(conversion[2]) + " " + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " teaspoons "
        return combined_measurement + str(conversion[2]) + " teaspoons "
    return combined_measurement.strip(",")


class Substitution:

    def __init__(self, substitute):
        self.original_text = substitute
        substitute = substitute.strip()
        self.components = self.find_all_components(substitute)
    
    def find_all_components(self, substitute):
        # all substitutions stored in mL
        broken_text = substitute.split(' ')
        current_string = ""
        current_component = [0.0, '']
        i = 0
        setting_number = True
        componentals = []
        while i < len(broken_text):
            if setting_number:
                if hasNumbers(broken_text[i]):
                    current_string = current_string + " " + broken_text[i]
                else:
                    setting_number = False
                    current_string = current_string + " " + broken_text[i]
                    ml_value = standard_volume_to_ml(current_string)
                    current_component[0] = ml_value
                    current_string = ""
            else:
                if hasNumbers(broken_text[i]):
                    setting_number = True
                    current_component[1] = current_string
                    componentals.append(current_component)
                    current_string = broken_text[i]
                    current_component = [0.0,'']
                else:
                    if not broken_text[i] == "plus" and not broken_text[i] == "and":
                        current_string = current_string + " " + broken_text[i]
            i = i + 1
        current_component[1] = current_string
        componentals.append(current_component)
        return componentals

    def print_self(self):
        print(self.original_text)

class Ingredient:
    def __init__(self, ingredient):
        # ingredient is a triple of the form measurement type (volume or mass), measurement, ingredient text
        self.ingredient = format_ingredient_listing(ingredient)

    def format_ingredient_listing(self, ingredient):
        volumes = ['teaspoon', 'tablespoon','cup', 'pint', 'teaspoons', 'tablespoons','cups', 'pints']
        weights = ['ounce', 'pound', 'ounces', 'pounds']
        ingredient = ingredient.strip()
        broken_text = ingredient.split()
        i = 0
        ingredient_tuple = ["", 0.0, ""]
        current_string = ""
        setting_number = True
        while i < len(broken_text):
            if setting_number:
                if hasNumbers(broken_text[i]):
                    current_string = current_string + " " + broken_text[i]
                else:
                    setting_number = False
                    if broken_text[i] in volumes:
                        current_string = current_string + " " + broken_text[i]
                        ml_value = standard_volume_to_ml(current_string)
                        ingredient_tuple[0] = ml_value
                        ingredient_tuple[1] = "milliliters"
                        current_string = ""
                    elif broken_text[i] in weights:
                        current_string = current_string + " " + broken_text[i]
                        grams_value = standard_weight_to_grams(current_string)
                        ingredient_tuple[0] = grams_value
                        ingredient_tuple[1] = "grams"
                        current_string = ""
                    else:
                        value = convert_to_float(current_string)
                        ingredient_tuple[0] = value
                        ingredient_tuple[1] = "N/A"
                        current_string = broken_text[i]
            else:
                current_string = current_string + " " + broken_text[i]
            i = i + 1
        ingredient_tuple[2] = current_string
        return ingredient_tuple

class Recipe:
    def __init__(self,title, ingredients, instructions):
        self.title = title
        self.ingredients = ingredients
        self.instructions = self.format_instructions(instructions)
        #approximate to show how the recipe adjustment works
        self.servings = 4

    def print_me(self):
        print("Ingredients:")
        for i in range(len(self.ingredients)):
            print(str(i) + ". " + self.ingredients[i])
        print('\n')
        print("Instructions:")
        for i in range(len(self.instructions)):
            print(str(i) + ". " + self.instructions[i])
        print('\n')

    def format_instructions(self, instructions):
        return instructions.split('\n')


class Substitution_Set:
    def __init__(self, original_amount, substitutes):
        self.original_amount = original_amount
        self.substitutes = [Substitution(item) for item in substitutes]
    
    def print_potential_substitutes(self):
        for item in self.substitutes:
            item.print_self()

def open_and_parse_recipe_database(master_list):
    recipes = {}
    with open(master_list, 'r') as file:
        reader = json.load(file)
        for key in reader.keys():
            recipes[key] = Recipe(reader[key]['title'], reader[key]['ingredients'], reader[key]['instructions'])
    return recipes

def open_and_parse_substitution_list(master_list):
    substitutions = {}
    with open(master_list, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            substitutions[row[0]] = Substitution_Set(row[1], row[2].split(','))
    return substitutions

substitution_dict = open_and_parse_substitution_list('test_files_substitution/substitution_master_list.csv')
print("Finished populating substitution list!")
recipe_dict = open_and_parse_recipe_database('test_files_substitution/recipes_raw_nosource_epi.json')
for key in recipe_dict.keys():
    print(recipe_dict[key].print_me())
print("Finished populating recipe database!")
#All recipes originally from Epicurious, a popular food recipe forum. 