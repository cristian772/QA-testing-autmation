Feature: Login Functionality
  Background: Login on saucedemon site
    Given I sign in as standard_user

  Scenario: I add a backpack to cart
    When I add a backpack to cart
    Then the backpack shoud be on cart


  Scenario: I add all the products to card and i check out
    When I add all the products to the cart
    And I click on cart
    And I proceed to Check out
    And I put my delivery inforamtion
    And I finish the check out
    Then I should be see Thank you for your order!
