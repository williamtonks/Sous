import csv

substitutions = []

with open('substitution_master_list.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        substitutions.append(row)

for row in substitutions:
    potential_subs = row[2]
    potential_subs = potential_subs.replace('\xa0', ' ')
    row[2] = potential_subs
    print(row)
        

with open('output.csv', 'w') as file:
    writer = csv.writer(file)
    for row in substitutions:
       writer.writerow(row)
