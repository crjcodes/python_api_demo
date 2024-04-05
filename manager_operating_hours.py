import string
import engine_convert
#import operating_hours_accessor

class Manager:
#  Accessor = operating_hours_accessor.Accessor()
  Converted = ""

  """
  Manages the use cases for requesting what establishments are open
  """
  def list_operating_restaurants(self, date_time=None):
    return "TODO"

  def ingest_new_data_source(self, filename):
    """
    This approach will NOT work for larger input
    One alternative approach is to have a background or separate
    process ingest the csv in chunks at a time and store in a database
    Then, here, the accessor could access the database instead of 
    an internal json structure held in memory
    """
    Converted = engine_convert.ConvertFrom(filename)
    # self.Accessor.store(Converted)
    return
  
  def parse_dow_start_end(self, line):
    return