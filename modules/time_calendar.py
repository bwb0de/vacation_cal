import time
import datetime
from matrix_creator import PickleDataType, Extended_UniqueItem_List, ExtendedDict
from cli_tools import amarelo, verde

class DateHandlers:
   def convert_brt_timestamp(self, date):
      return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, "%d/%m/%Y")))
   
   def create_period_pair(self, start_date, end_date):
      start_dt = self.convert_brt_timestamp(start_date)
      end_dt = self.convert_brt_timestamp(end_date)
      return (start_dt, end_dt)

   def time_delta(self, start_date, end_date):
      if start_date == str and end_date == str:
         period = self.create_period_pair(start_date, end_date)
      else:
         period = (start_date, end_date)
      return period[1] - period[0]

   def extanded_period_pair(self, pair):
      delta = self.time_delta(pair[0], pair[1])
      delta = delta.days
      start_date = pair[0]
      output = []
      for day in range(0, delta+1):
         output.append(start_date + datetime.timedelta(days=day))
      return output

     


class Calendar(DateHandlers, PickleDataType):
   def __init__(self):
      super(Calendar).__init__()
      self.people = Extended_UniqueItem_List()
      self.absence_dates = ExtendedDict()

   def add(self, name, init_date, end_date=False):
      if not end_date:
         period_tuple = self.create_period_pair(init_date, init_date)
      else:
         period_tuple = self.create_period_pair(init_date, end_date)

      self.people.append(name)
      self.absence_dates.append(name, period_tuple)
   
   def check(self, start_date, end_date=False, list_people=False, sort_by_amout_of_people=False):
      if not end_date:
         self.check_period([self.convert_brt_timestamp(start_date)])
      else:
         period_pair = self.create_period_pair(start_date, end_date)
         extended_period = self.extanded_period_pair(period_pair)
         self.check_period(extended_period, list_people=list_people, sort_by_amout_of_people=sort_by_amout_of_people)

   def print_day_info(self, response_tuple, list_people=False):
      print(amarelo(response_tuple[0]))
      print(amarelo('Pessoas disponíveis:'), response_tuple[1])
      if list_people:
         print(response_tuple[2])


   def check_period(self, list_of_dates, list_people=False, sort_by_amout_of_people=False):
      output = []
      for day in list_of_dates:
         people_not_avaliable = Extended_UniqueItem_List()
         for person in self.absence_dates.keys():
            for interval in self.absence_dates[person]:
               if day >= interval[0] and day <= interval[1]:
                  people_not_avaliable.append(person)
         
         people_avaliable = Extended_UniqueItem_List(self.people.copy()) - people_not_avaliable

         tp = (day, len(people_avaliable), people_avaliable)
         output.append(tp)
         
         if not sort_by_amout_of_people:
            self.print_day_info(tp, list_people=list_people)

      sort_by_num_of_people = lambda x: x[1]
      output.sort(key=sort_by_num_of_people, reverse=True)

      if sort_by_amout_of_people:
         for tp in output:
            self.print_day_info(tp, list_people=list_people)




            

