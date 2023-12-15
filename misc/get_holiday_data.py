from datetime import date, timedelta
import holidays
import csv

# set up dates observed
start_date = date(2022, 1, 1)
end_date = date(2023, 12, 31)
delta = timedelta(days=1)
us_holidays = holidays.US()

daysUntilNext = 0

holiday_dataset = dict()

# find all holiays in between these dates
while(start_date <= end_date):
    
    row_data=["", 0]
    if start_date in us_holidays:
        row_data=[us_holidays.get(start_date), 1]

    holiday_dataset["{}".format(start_date)]=row_data
    start_date+=delta

start_date = date(2022, 1, 1)

# find how many days until next holiday
while(start_date <= end_date):
    daysUntilNext+=1
    if(end_date in us_holidays):
       daysUntilNext = 0;
    
    holiday_dataset["{}".format(end_date)].append(daysUntilNext);
    end_date-=delta

# print to csv
with open('holidays.csv', 'w') as csv_file:  
    fields = ["date", "holiday", 'hasHoliday', "daysUntilNext"]
    writer = csv.writer(csv_file)
    writer.writerow(fields)
    
    for key, value in holiday_dataset.items():
       writer.writerow([key, value[0],value[1], value[2]])
