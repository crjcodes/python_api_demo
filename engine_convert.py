import string
import datetime
import re
import json
from model_operating_hours import OperatingHours

def ConvertFrom(filename):
  """
  Takes the name of a csv file matching the business specification, then
  maps to a list of our internal data model
  DESIGN: mapping to a data model may be overkill. Can just map to a json structure
  and treat it like a database of sorts
  """
  if not filename or not filename.strip():
    # TODO: FUTURE: configurable logging
    raise ValueError()

  file = open(filename, "r")
  # Assuming always a header
  next(file)

  internal_data = []
  for line in file:
    internal_data.append(map_line_to_model(line))

  return json.dumps(internal_data)

def map_line_to_model(line):
  """
  Will return the sub-json to add to our data "store"
  """
  if not line or not isinstance(line, str) or line == "":
    raise ValueError() 

  line = line.strip()
  field_values = line.split(',')

  if not validate_incoming_data(field_values):
    raise ValueError()     
  
  restaurant_name = field_values[0]
  opHours = parse_op_hours(field_values[1])

  return ""

def validate_incoming_data(field_values):
  if field_values == None:
    print("No data found in this line")
    return False
  
  if isinstance(field_values, list) == False:
    print("Data not recognized")
    return False
  
  length = len(field_values)
  if not field_values or length != 2:
    print("Not all fields were found in this row of data")
    return False
 
  return True


def parse_op_hours(human_readable_op_hours):
  """
  TODO: 
    Future: if performance concerns, compile the regex
      beforehand (plus other options)
    Future: the find/replace can be replaced by one operation
  """
  sections = human_readable_op_hours.split(r'\s*/\s*')

  op_hours_list = []

  for section in sections:

    # Parse from input data

    section, close_time_text = parse_last_time_text(section) 
    section, open_time_text = parse_last_time_text(section)
    
    dow_list = parse_dow_text(section)

    # Convert to non-primitive types    
    start_time = datetime.datetime.strptime(open_time_text, '%H:%M').time()
    end_time = datetime.datetime.strptime(close_time_text, '%H:%M').time()

    for dow in dow_list:
      op_hours = OperatingHours(dow, start_time, end_time)
      op_hours_list.append(op_hours)

  return op_hours_list

def parse_last_time_text(section):

  if (section is None or section == ""):
    return section, None

  # non-overlapping
  # look for the last occurrence first
  # TODO: FUTURE: possible performance improvements with a different search, if needed
  match = re.search(r"(?s:.*)\s([0-9][0-9:]*\s*[ap]m)\s*", section)

  if match == None:
    return section, None

  timeText = match.group(1)
  section = section.replace(timeText, "")
  # TODO: as regex, in case spaces aren't there
  section = section.replace(" - ", "")
  print(f"section = {section}")

  # TODO: error check on the match results
  return section, re.sub(r'\s', "", timeText)

def parse_dow_text(section):
    # TODO; right now, relying on exceptions for the error handling

    # TODO: move to common location
    dow_full = "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    dow_list = []

    # disconnected days
    firstBreak = section.split(",")
    for f in firstBreak:
      second_break = f.split("-")      
      start_dow = second_break[0].strip()
      
      if start_dow not in dow_full:
        continue

      df_start_index = dow_full.index(start_dow)

      if len(second_break) == 1:
        dow_list.append(f.strip())
      else:
        end_dow = second_break[1].strip()

        if end_dow not in dow_full:
          continue

        df_end_index = dow_full.index(end_dow)
        for df in dow_full[df_start_index:df_end_index+1]:
          dow_list.append(df)             
    
    return dow_list

def findFirst(pattern, text):
  find = re.findall(pattern, text)
  if not find or len(find) == 0:
    return None
  
  return find[0]

