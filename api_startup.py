import manager_operating_hours

def perform_startup_steps(manager, filename="data_restaurants.csv"):
  try:
    if manager == None:
      raise ValueError("No manager")
    
    # TODO: FUTURE: name of file input through command-line and configuration
    # TODO: figure out how to reference the file in a data directory, not just source
    manager.ingest_new_data_source(filename)
    print("manager ingestion")
  except Exception as err:
    print(f"Startup failure due to unexpected {err=}, {type(err)=}")
    raise  