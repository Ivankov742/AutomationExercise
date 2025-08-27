Feature: AutomationExercise API
  The API should handle login and product search properly

  Scenario: Verify login with invalid credentials
    When I POST "verifyLogin" with form data:
      """
      {"email": "invalid@example.com", "password": "wrongpassword"}
      """
    Then the API response status should be 200
    And the JSON field "responseCode" should equal 404
    And the JSON field "message" should contain "user not found"

  Scenario: Search product with keyword
    When I POST "searchProduct" with form data:
      """
      {"search_product": "tshirt"}
      """
    Then the API response status should be 200
    And the JSON field "responseCode" should equal 200
    And the JSON should have key "products"

  Scenario: GET method is not allowed for searchProduct
    When I GET "searchProduct"
    Then the API response status should be 200
    And the JSON field "responseCode" should be one of 400,405
