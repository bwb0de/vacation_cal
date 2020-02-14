import time
import datetime

from modules.py_obj_data_tools import PickleDataType, Extended_UniqueItem_List, ExtendedDict
from modules.time_calendar_config import pasta_dados
from modules.cli_tools import amarelo, verde


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
   def __init__(self, fname):
      super(Calendar).__init__()
      self.pessoas = Extended_UniqueItem_List()
      self.datas_de_ausencias = ExtendedDict()
      self.target_folder = pasta_dados
      self.persist(file_ext=".cal", fname=fname)

   def add(self, name, init_date, end_date=False):
      if not end_date:
         period_tuple = self.create_period_pair(init_date, init_date)
      else:
         period_tuple = self.create_period_pair(init_date, end_date)

      self.pessoas.append(name)
      self.datas_de_ausencias.append(name, period_tuple)
      self.persist()
   
   def check(self, start_date, end_date=False, list_pessoas=False, sort_by_amout_of_pessoas=False):
      if not end_date:
         self.check_period([self.convert_brt_timestamp(start_date)])
      else:
         period_pair = self.create_period_pair(start_date, end_date)
         extended_period = self.extanded_period_pair(period_pair)
         self.check_period(extended_period, list_pessoas=list_pessoas, sort_by_amout_of_pessoas=sort_by_amout_of_pessoas)


   def print_day_info(self, response_tuple, list_pessoas=False):
      print(amarelo(str(response_tuple[0]).split(' ')[0]))
      print(amarelo('Número de pessoas disponíveis:'), response_tuple[1])
      if list_pessoas:
         print(response_tuple[2])


   def check_period(self, list_of_dates, list_pessoas=False, sort_by_amout_of_pessoas=False):
      output = []
      for day in list_of_dates:
         pessoas_not_avaliable = Extended_UniqueItem_List()
         for person in self.datas_de_ausencias.keys():
            for interval in self.datas_de_ausencias[person]:
               if day >= interval[0] and day <= interval[1]:
                  pessoas_not_avaliable.append(person)
         
         pessoas_avaliable = Extended_UniqueItem_List(self.pessoas.copy()) - pessoas_not_avaliable

         tp = (day, len(pessoas_avaliable), pessoas_avaliable)
         output.append(tp)
         
         if not sort_by_amout_of_pessoas:
            self.print_day_info(tp, list_pessoas=list_pessoas)

      sort_by_num_of_pessoas = lambda x: x[1]
      output.sort(key=sort_by_num_of_pessoas, reverse=True)

      if sort_by_amout_of_pessoas:
         for tp in output:
            self.print_day_info(tp, list_pessoas=list_pessoas)




            

