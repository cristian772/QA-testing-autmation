Feature: Login Functionality
  Background: Login on saucedemon site
    Given I sign in as standard_user

  Scenario: I add a backpack to cart
    When I add a backpack to cart
    Then the backpack shoud be on cart


  Scenario: I add all the products to cart and i check out
    When I add all the products to the cart
    And I click on cart and proceed check out
    And I put my delivery information
    Then I should see Thank you for your order!
