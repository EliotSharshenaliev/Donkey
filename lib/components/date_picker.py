from kivy.uix.widget import Widget
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from lib.utills.time_conventer import time_converter

class CustomizedDateTimePicker:
    def on_save_date(self, instance, value, date_range):
        pass

    def show_date_picker(self, *args):
        import datetime
        data_picker = MDDatePicker(min_year=datetime.date.today().year,
                                   max_year=datetime.date.today().year + 1)
        data_picker.bind(on_save=self.on_save_date)
        data_picker.open()

    def on_save_time(self, time):
        pass

    def show_time_picker(self, *args):
        data_picker = MDTimePicker()
        data_picker.bind(time=self.on_save_time)
        data_picker.open()
