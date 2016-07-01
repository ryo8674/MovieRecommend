import csv

f = open('in_data.csv', 'rU')

reader = csv.reader(f)
header = next(reader)

#target =[]
target = header[1:]
print target

for row in reader:
   print (row[1:])

f.close()
