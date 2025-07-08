Feature: UI Tests

  Scenario: Place Order - Login before Checkout
    Given I open the home page
    And I login with valid credentials
    And I add a product to the cart
    And I proceed to checkout
    And I fill payment details
    When I place the order
    Then the order should be confirmed
