import unittest
import api_startup
import manager_operating_hours

class StartupTests(unittest.TestCase):
  def test_should_throw_exception_when_no_manager(self):
    testManager = manager_operating_hours.Manager()
    self.assertRaises(ValueError, api_startup.perform_startup_steps, None, "")

  def test_should_throw_exception_when_no_input_data_file(self):
    testManager = manager_operating_hours.Manager()
    self.assertRaises(ValueError, api_startup.perform_startup_steps, testManager, "")

  def test_should_have_converted_data_when_nominal_input_data(self):
    testManager = manager_operating_hours.Manager()
    api_startup.perform_startup_steps(testManager, "test_input_data.csv")

    # result = testManager.Accessor.dataSourceAsJson
    # deserializedResult = json.loads(result)

    self.assertNotEqual("", testManager.Converted)


if __name__ == '__main__':
    unittest.main()
