Feature: API Tests

  Scenario: Login with invalid credentials
    When I try to login with email 'invalid@example.com' and password 'wrongpassword'
    Then the login response code should be 400 or 404

  Scenario: Search for a valid product
    When I search for product 'tshirt'
    Then the search response code should be 200

  Scenario: Place Order - Login before Checkout
    Given I open the home page
    And I login with valid credentials
    And I add a product to the cart
    And I proceed to checkout
    And I fill payment details
    When I place the order
    Then the order should be confirmed