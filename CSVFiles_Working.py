import csv

#with open('names.csv', 'r') as csv_file:
#    csv_reader = csv.reader(csv_file)
#    next(csv_reader)

#    with open('new_names.csv', 'w') as new_file:
#        csv_writer = csv.writer(new_file, delimiter='\t')

#        for line in csv_reader:
#            csv_writer.writerow(line)

with open('names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('new_names1.csv', 'w') as new_file:
        fieldnames = ['firstname', 'lastname', 'emailaddress']

        csv_writer = csv.DictWriter(new_file, fieldnames, delimiter='\t')
        csv_writer.writeheader()

        for line in csv_reader:
            csv_writer.writerow(line)
