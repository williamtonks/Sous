#!/usr/bin/env python

import unicodedata
import csv
import json
import re
from fractions import Fraction

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasAlpha(inputString):
    return any(char.isalpha() for char in inputString)

def remove_non_digits(inputString):
    acceptable_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '/']
    chars_to_remove = []
    parsed_string = inputString
    for char in inputString:
        if not char in acceptable_chars:
            chars_to_remove.append(char)
    for char in chars_to_remove:
        parsed_string = parsed_string.replace(char, "")
    return parsed_string

def remove_non_alphabet_characters(inputString):
    parsed_string = ""
    for char in inputString:
        if char.isalpha():
            parsed_string = parsed_string + char
        else:
            parsed_string = parsed_string + " "
    return parsed_string
        
def convert_to_float(frac_str):
    frac_str = frac_str.strip()
    if '(' in frac_str:
        index = frac_str.find('(')
        frac_str = frac_str[:index]
    frac_str = remove_non_digits(frac_str)
    #print(frac_str)
    if not hasNumbers(frac_str):
        return 0
    try:
        return float(frac_str)
    except ValueError:
        if not '/' in frac_str and ' ' in frac_str:
            broken_num = frac_str.split(' ')
            return float(broken_num[0])
        multiplier = 1.0
        str_to_consider = ""
        broken_text = frac_str.split()
        not_done = True
        for item in broken_text:
            if not_done:
                str_to_consider = str_to_consider + " " + item
            if '/' in item:
                not_done = False
        frac_str = str_to_consider.strip()
        #print("2." + frac_str)
        if frac_str.count('/') > 1:
            return float(1.0)
        if len(frac_str.split(" ")) > 2:
            broken_num = frac_str.split(' ')
            multiplier = convert_to_float(broken_num[0])
            if '/' in broken_num[-2]:
                frac_str = broken_num[-2]
            else:
                frac_str = broken_num[-2] + " " + broken_num[-1]
        frac_str = frac_str.strip()
        #print("3." + frac_str)
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        if num == "":
            num = "1"
        if denom == "":
            denom = "1"
        frac = float(num) / float(denom)
        return (whole - frac) * multiplier if whole < 0 else (whole + frac) * multiplier

def standard_weight_to_grams(measurement_text):
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

def convert_grams_to_standard_weight(amount):
    # conversion : pound, ounce, eigth of an ounce
    # since cooking instructions are by in large improper in terms of volume
    # the volumes outputted are rounded to approximate fractional amounts
    conversion = [0, 0, 0]
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
        combined_measurement = combined_measurement + str(conversion[0]) + " pounds, "
    if conversion[1] >= 1:
        combined_measurement = combined_measurement + str(conversion[1]) + " "
    if conversion[2] >= 1:
        fractional_amount = Fraction(conversion[2], 8)
        return combined_measurement + " " + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " ounces "
    elif conversion[1] >= 1:
        return combined_measurement + " ounces "
    return combined_measurement.strip(',')

def convert_ml_to_standard_volume(amount):
    # conversion : full cups, tablespoons, teaspoons, sixtheenth teaspoons
    # since cooking instructions are by in large improper in terms of volume
    # the volumes outputted are rounded to approximate fractional amounts
    conversion = [0, 0, 0, 0]
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
    while amount >= .305:
        amount = amount - .305
        conversion[3] += 1
    if conversion[0] >= 1 and conversion[1] >= 2:
        if conversion[1] % 2 == 1:
            conversion[1] += 1
        fractional_amount = Fraction(conversion[1], 16)
        if fractional_amount.numerator > fractional_amount.denominator:
            conversion[0] += 1
            conversion[1] -= 16
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
    if conversion[3] >= 16:
        conversion[2] += 1
        conversion[3] -= 16
    if conversion[2] >= 1:
        combined_measurement = combined_measurement + str(conversion[2]) + " "
    if conversion[3] >= 1:
        fractional_amount = Fraction(conversion[3], 16)
        return combined_measurement + str(fractional_amount.numerator) + "/" + str(fractional_amount.denominator) + " teaspoons "
    elif conversion[2] >= 0:
        return combined_measurement + " teaspoon "
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
    def __init__(self, ingredient_text):
        # ingredient is a triple of the form measurement type (volume or mass), measurement, ingredient text
        self.ingredient_text = unicodedata.normalize('NFKD', ingredient_text).encode('ascii', 'ignore')
        self.ingredient = self.format_ingredient_listing(self.ingredient_text)

    def format_ingredient_listing(self, ingredient):
        volumes = ['teaspoon', 'tablespoon','cup', 'pint', 'teaspoons', 'tablespoons','cups', 'pints']
        weights = ['ounce', 'pound', 'ounces', 'pounds', 'oz']
        ingredient = ingredient.strip()
        broken_text = ingredient.split()
        i = 0
        ingredient_tuple = [0.0, "", ""]
        current_string = ""
        setting_number = True
        while i < len(broken_text):
            if setting_number:
                if hasNumbers(broken_text[i]):
                    current_string = current_string + " " + broken_text[i]
                else:
                    setting_number = False
                    if hasNumbers(current_string):
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
                            if value == 0.0:
                                ingredient_tuple[0] = "To Taste"
                            else:
                                ingredient_tuple[0] = value
                            ingredient_tuple[1] = "N/A"
                            current_string = broken_text[i]
                    else:
                        ingredient_tuple[0] = "To Taste"
                        ingredient_tuple[1] = "N/A"
                        current_string = broken_text[i]
            else:
                current_string = current_string + " " + broken_text[i]
            i = i + 1
        ingredient_tuple[2] = current_string
        #for debugging ingredient parsing
        #print(ingredient)
        #print(ingredient_tuple)
        #print()
        return ingredient_tuple

class Recipe:
    def __init__(self,title, ingredients, instructions):
        self.title = title
        self.ingredients = []
        for item in ingredients:
            self.ingredients.append(Ingredient(item))
        self.instructions = self.format_instructions(instructions)
        #approximate to show how the recipe adjustment works
        self.servings = 4

    def print_me(self):
        print("Ingredients:")
        for i in range(len(self.ingredients)):
            print(str(i + 1) + ". " + self.ingredients[i].ingredient_text)
        print('\n')
        print("Instructions:")
        for i in range(len(self.instructions)):
            print(str(i) + ". " + self.instructions[i])
        print('\n')

    def print_ingredients(self):
        print("Ingredients:")
        for i in range(len(self.ingredients)):
            print(str(i + 1) + ". " + self.ingredients[i].ingredient_text)
            #print(self.ingredients[i].ingredient)
        print('\n')

    def update_recipe_substitution(self, position_of_old, new_ingredients):
        self.ingredients.pop(position_of_old)
        for item in new_ingredients:
            self.ingredients.append(Ingredient(item))

    def format_instructions(self, instructions):
        return instructions.split('\n')

    def adjust_servings(self, new_servings):
        old_servings = self.servings
        ratio = float(new_servings) / float(old_servings)
        new_ingredient_lines = []
        for item in self.ingredients:
            if item.ingredient[1] == "milliliters" :
                sub_amount_in_ml = item.ingredient[0] * ratio
                printable = convert_ml_to_standard_volume(sub_amount_in_ml)
                #print(printable.strip() + " of " + item.ingredient[2].strip())
                new_ingredient_lines.append(unicode(printable.strip() + " " + item.ingredient[2].strip()))
            elif item.ingredient[1] == "grams":
                sub_amount_in_grams = item.ingredient[0] * ratio
                printable = convert_grams_to_standard_weight(sub_amount_in_grams)
                #print(printable.strip() + " of " + item.ingredient[2].strip())
                new_ingredient_lines.append(unicode(printable.strip() + " " + item.ingredient[2].strip()))
            elif item.ingredient[0] == "To Taste":
                new_ingredient_lines.append(unicode(item.ingredient_text))
            else:
                sub_amount = ratio * item.ingredient[0]
                new_ingredient_lines.append(unicode(str(sub_amount) + " " + item.ingredient[2].strip()))
        self.ingredients = []
        for item in new_ingredient_lines:
            self.ingredients.append(Ingredient(item))
        self.servings = new_servings




class Substitution_Set:
    def __init__(self, original_amount, substitutes):
        self.original_amount = standard_volume_to_ml(original_amount)
        self.substitutes = [Substitution(item) for item in substitutes]
    
    def print_potential_substitutes(self):
        for item in self.substitutes:
            item.print_self()

def open_and_parse_recipe_database(master_list):
    recipes = {}
    with open(master_list, 'r') as file:
        reader = json.load(file)
        for key in reader.keys():
            title = str(unicodedata.normalize('NFKD', reader[key]['title']).encode('ascii', 'ignore'))
            new_title = ""
            for char in title:
                new_title = new_title + char
            new_title = new_title.strip()
            #print(title)
            recipes[new_title] = Recipe(reader[key]['title'], reader[key]['ingredients'], reader[key]['instructions'])
    return recipes

def open_and_parse_substitution_list(master_list):
    substitutions = {}
    with open(master_list, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            substitutions[row[0]] = Substitution_Set(row[1], row[2].split(','))
    return substitutions

def print_a_recipe(key):
    print('\n')
    print(recipe_dict[key].title)
    print("Serves: " + str(recipe_dict[key].servings))
    recipe_dict[key].print_ingredients()

def substitution_quantities(recipe_amount, ingredient_amount, substitution_amount):
    #print("Recipe Amount " + str(recipe_amount))
    #print("Ingredient Amount " + str(ingredient_amount))
    #print("Substitution Amount " + str(substitution_amount))
    return recipe_amount * (float(substitution_amount) / float(ingredient_amount))

def recipe_chosen(original_key):
    recipe = recipe_dict[original_key]
    print_a_recipe(original_key)
    needs_substitution = str(raw_input("Do you need to make a substitution?"))
    keep_going = False
    if 'y' in needs_substitution.lower():
        keep_going = True
    while(keep_going):
        substitute = int(raw_input(" Enter it's number: "))
        ingredient_line = recipe.ingredients[substitute - 1]
        print("You have selected: " + recipe.ingredients[substitute - 1].ingredient_text)
        raw_ingredient = (recipe.ingredients[substitute - 1].ingredient[2]).strip()
        print(raw_ingredient)
        substitute_list = substitution_dict.keys()
        ingredient_key = ""
        for key in substitute_list:
            if raw_ingredient in key:
                answer = str(raw_input("Does this seem like the ingredient you picked? '" + str(key) + "' ... "))
                if 'y' in answer.lower():
                    ingredient_key = key
                    break
        if ingredient_key == "":
            print("Sorry we didn't find a suitable substitute! Maybe try a different recipe. ")
            break
        print("Here are some potential substitutes:")
        substitution = []
        for item in substitution_dict[ingredient_key].substitutes:
            for component in item.components:
                print(component[1])
            answer = str(raw_input("Do you have the above?... "))
            if 'y' in answer.lower():
                substitution = item
                break
        new_ingredient_lines = []
        print("Here are your proportional substitutes for: " + ingredient_line.ingredient_text)
        for item in substitution.components:
            sub_amount_in_ml = substitution_quantities(ingredient_line.ingredient[0], substitution_dict[ingredient_key].original_amount, item[0]) #each of these in mL
            printable = convert_ml_to_standard_volume(sub_amount_in_ml)
            print(printable.strip() + " of " + item[1].strip())
            new_ingredient_lines.append(unicode(printable.strip() + " " + item[1].strip()))
        
        recipe.update_recipe_substitution(substitute - 1, new_ingredient_lines)
        print_a_recipe(original_key)

        needs_substitution = str(raw_input("Do you need to make another substitution?"))
        keep_going = False
        if 'y' in needs_substitution.lower():
            keep_going = True

def change_recipe_serving_size(recipe_key, new_servings):
    recipe = recipe_dict[recipe_key]
    print_a_recipe(recipe_key)
    recipe.adjust_servings(new_servings)
    print_a_recipe(recipe_key)

substitution_dict = open_and_parse_substitution_list('test_files_substitution/substitution_master_list.csv')
print("Finished populating substitution list!")
recipe_dict = open_and_parse_recipe_database('test_files_substitution/recipes_raw_nosource_epi.json')
print("Finished populating recipe database!")
change_recipe_serving_size('Chocolate Roll-Out Cookies', 6)

print("Welcome to the Sous Substitution Service. Here's a recipe for Chocolate Roll-Out Cookies")
recipe_chosen('Chocolate Roll-Out Cookies')
#All recipes originally from Epicurious, a popular food recipe forum. 