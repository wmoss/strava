import csv
import sys
import datetime
import pylab
from matplotlib import pyplot

MILES_PER_KM = 0.621371

# Add a line to the plot
def add_year(year, x_axis, y_axis):
    pylab.plot(x_axis + [365], y_axis + [y_axis[-1]], label=year)

reader = csv.reader(open(sys.argv[1]))
distances = []
for row in reader:
    # skip everything but rides
    if row[3] == 'Ride':
        parsed = datetime.datetime.strptime(row[1], "%b %d, %Y, %I:%M:%S %p")
        distances.append([parsed, float(row[6]) * MILES_PER_KM])

# sort by date
distances = sorted(distances, key=lambda x: x[0])

# create daily sum using default dict
current_year = None
current_miles = 0

x_axis = [0]
y_axis = [0]

max_miles = 0

for date, miles in distances:
    year = date.year
    if current_year != year:
        add_year(current_year, x_axis, y_axis)

        current_miles = 0
        x_axis = [0]
        y_axis = [0]

    current_miles += miles
    day_of_year = date.timetuple().tm_yday

    max_miles = max(max_miles, current_miles)

    x_axis.append(day_of_year)
    y_axis.append(current_miles)

    current_year = year

add_year(current_year, x_axis, y_axis)

# generate months
days = []
months = []
for month in xrange(1, 13):
    date = datetime.date(1900, month, 1)
    days.append(date.timetuple().tm_yday)
    months.append(date.strftime('%B'))
pyplot.xticks(days, months, rotation=30)

pyplot.subplots_adjust(top=0.95, bottom=0.15)
pylab.legend(loc='upper left')
pyplot.xlim(right=365)
pyplot.ylim(top=max_miles)
pyplot.margins(0.4)
pyplot.savefig('miles_per_year.png')
