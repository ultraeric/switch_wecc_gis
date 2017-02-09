import csv
import os

directory = '../Florin/EMFAC2014_County/'

newfile = 'PollutantsSum.csv'

if os.path.isfile(newfile):
    # Remove old file since we are appending to a file later
    os.remove(newfile)

# Open result file
with open(newfile, 'a') as csvfile:
    fieldnames = ['Region', 'PM2_5_RUNEX', 'PM10_RUNEX', 'CO2_RUNEX', 'NOx_RUNEX', 'NUM_CARS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through EMFACE Counties
    for filename in os.listdir(directory):
        with open(directory + filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            # Start sum of column
            sum_of_PM2_5 = 0.0
            sum_of_PM10 = 0.0
            sum_of_CO2 = 0.0
            sum_of_NOx = 0.0
            num_cars = 0
            for row in reader:
                region = row['Region']
                break

            for row in reader:
                sum_of_PM2_5 += float(row['PM2_5_RUNEX'])
                sum_of_PM10 += float(row['PM10_RUNEX'])
                sum_of_CO2 += float(row['CO2_RUNEX'])
                sum_of_NOx += float(row['NOx_RUNEX'])

                num_cars += 1
            # Add row to NEWFILE with the current region and sum of each column
            writer.writerow({'Region': region, 'PM2_5_RUNEX': sum_of_PM2_5, 'PM10_RUNEX': sum_of_PM10, 'CO2_RUNEX': sum_of_CO2, 'NOx_RUNEX': sum_of_NOx, 'NUM_CARS': num_cars})
