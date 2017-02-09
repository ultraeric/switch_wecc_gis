import csv
import os

filename = 'PollutantsSum.csv'

pollutant = 'CO2'

outputfile = 'PollutantPercentile' + pollutant + '.csv'

if os.path.isfile(outputfile):
    # Remove old file since we are appending to a file later
    os.remove(outputfile)

with open(filename, 'rb') as csvfile, open(outputfile, 'a') as csvout:
    reader = csv.DictReader(csvfile)
    fieldnames = ['Region'] + [pollutant + '_RUNEX'] + [pollutant + '_Perc']  # add new columns
    writer = csv.DictWriter(csvout, fieldnames)
    writer.writeheader()
    tuples = []

    for row in reader:
        region = row['Region']
        pol = float(row[pollutant + '_RUNEX'])
        tuples.append((region, pol))

    sort_pol = sorted(tuples, key=lambda pollutant: pollutant[1])

    length = len(sort_pol)
    for i in range(0, length):
        pr = (i/float(length))*100
        writer.writerow({'Region': sort_pol[i][0], pollutant + '_RUNEX': sort_pol[i][1], pollutant + '_Perc': pr})
