Feature: The API runs as is, immediately after cloning the repository.
  As a developer/user with limited time,
  I want to start a new service with zero Incidental Complexity,
  So I can immediately make progress on the Essential Complexity of my particular use-case.


  Scenario Outline: The API uses database credentials from a config file
  Given a "<config_file>" exists
  And it has database credentials
  And they are complete
  When the app is running
  Then the app uses a database connection with those credentials

  Examples: Amounts
      | config_file |
      | config.ini  |


  Scenario: The API can save and load objects to the database
  Given an object is created in memory
  And it has data that must persist
  When it is saved
  And it is loaded by id
  Then the loaded data matches the saved data