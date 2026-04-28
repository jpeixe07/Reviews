Feature: Feed page
    As a platform user
    I want to access the feed page
    So that I can see trending works, top-rated content, and access specific rankings

Scenario: Viewing trending works of the last week (Em Alta)
    Given I am on the platform's feed page
    Then the system displays the trending works
    And these works are ordered by the volume of views during the last week

Scenario: Viewing top-rated works of the current week (Mais Bem Avaliados da Semana)
    Given I am on the platform's feed page
    Then the system displays the highest-rated works of the week
    And these works are ordered by their average evaluation score for the current week

Scenario: Browsing more items in a category
    Given I am on the platform's feed page
    When I request to see more items from a specific category
    Then additional works associated with that category are presented to me

Scenario: Accessing the most viewed works by period
    Given I am on the platform's feed page
    When I request the ranking of most viewed works for a specific timeframe
    Then I am presented with the "Most Viewed" list filtered by that period

Scenario: Accessing the most evaluated works of all time
    Given I am on the platform's feed page
    When I request the historical ranking of most evaluated works
    Then I am presented with the "Most Evaluated" list reflecting all-time data