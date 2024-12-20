Feature: API Testing for User Management
  Test API endpoints for user retrieval, user creation, and login functionality.

  Scenario Outline: Verify user retrieval by ID
    Given the API endpoint for user retrieval "<user_id>"
    When I send a GET request to the endpoint
    Then I should receive a status code "<expected_status>"
    And the response should match the expected structure
      | expected_status | response_structure |
      | 200             | contains "data"    |
      | 404             | equals "{}"        |

    Examples:
      | user_id | expected_status |
      | 2       | 200             |
      | 9999    | 404             |

  Scenario: Create a new user
    Given the API endpoint for user creation
    And the user payload is
      | key   | value      |
      | name  | morpheus   |
      | job   | leader     |
    When I send a POST request with the payload
    Then I should receive a status code 201
    And the response should contain the user's name "morpheus"
    And the response should contain the user's job "leader"

  Scenario Outline: Login with different payloads
    Given the API endpoint for login
    And the payload is
      | key        | value         |
      | email      | eve.holt@reqres.in |
      | <password> | <value>       |
    When I send a POST request with the payload
    Then I should receive a status code "<expected_status>"
    And the response should
      | expected_status | response_field | check |
      | 200             | token          | exist |
      | 400             | error          | equals "Missing password" |

    Examples:
      | password   | value        | expected_status |
      | password   | cityslicka   | 200             |
      | <missing>  |              | 400             |
