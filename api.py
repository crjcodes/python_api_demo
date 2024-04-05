import api_startup

try:
  api_startup.perform_startup_steps(None, "bogus")
  print("hello")
except Exception as err:
  print(f"Startup failure due to unexpected {err=}, {type(err)=}")
  raise    