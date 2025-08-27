Feature: Place Order - Login before Checkout
  As a signed-in user
  I want to add a product and place an order
  So that I can complete a purchase

  Background:
    Given I open the home page
    And I login with valid credentials

  Scenario: Place order successfully
    Given I add a product to the cart
    And I proceed to checkout
    And I fill order message
    When I place the order
    Then the order should be confirmed
