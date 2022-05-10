Feature: The API runs as is, immediately after cloning the repository.
  As a developer/user with limited time,
  I want to start a new service with zero Incidental Complexity,
  So I can immediately make progress on the Essential Complexity of my particular use-case.


  Scenario Outline: The database connection is established using data loaded from a config file
  Given a "<config_file>" exists
  And it has database credentials
  And they are complete
  When the app is running
  Then the app uses a database connection with those credentials

  Examples: Amounts
      | config_file |
      | config.ini  |


  Scenario: Objects can be saved to and loaded from the database
  Given an object is created in memory
  And it has data that must persist
  When it is saved
  And it is loaded by id
  And nothing is loaded by a bad id
  And it is loaded by an arbitrary attribute
  Then the data loaded by id matches the saved data
  Then the data loaded by an arbitrary attribute contains that attribute



  Scenario: The API has a status endpoint for verifying that it is operational
  Given the API is running
  When a get request is sent to /status
  Then a status code of 200 is returned
