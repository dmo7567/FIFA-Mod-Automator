# Import the 'date' class from the 'datetime' module
from datetime import date
import random

# Define a start date as July 2, 2014
f_date = date(1753, 1, 1)

# Define an end date as July 11, 2014
l_date = date(2023, 12, 31)

# Calculate the difference between the end date and start date
delta = l_date - f_date

id = 62171 + int(delta.days)

# Print the number of days in the time difference
print(id)



playerHeight = 168

playerWeight = int(((playerHeight/100)*22*2.205)-random.randint(7, 14))

print(playerWeight)