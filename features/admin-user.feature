Feature: Admin user

  As an administrator of the Reviews platform
  I want to create, remove and edit users, delete common user accounts,
  register artists, authors, voice actors, and publish news
  So that the content, catalog and community of the platform stay organised

  Scenario: non-admin user cannot access admin endpoints
    Given the common user "Maria321" is authenticated
    When the user requests the admin users list
    Then the system returns a forbidden access error
    And no admin user data is returned

  Scenario: admin creates a common user successfully
    Given the admin "GabrielAdmin" is authenticated
    And no account exists with username "AnaReviews"
    When the admin creates a user with username "AnaReviews", email "ana@example.com" and role "common"
    Then the system persists the user "AnaReviews" with role "common"
    And the audit log records "create_user" by "GabrielAdmin"

  Scenario: common admin tries to remove another admin and is blocked
    Given the admin "OpsAdmin" is authenticated with role "admin"
    And the user "DevAdmin" exists with role "admin" and status "active"
    When "OpsAdmin" requests permanent deletion of "DevAdmin"
    Then the system returns a forbidden access error
    And "DevAdmin" remains active with role "admin"
    And no related records for "DevAdmin" are deleted

  Scenario: admin edits an existing user email successfully
    Given the admin "GabrielAdmin" is authenticated
    And the active user "Maria321" has email "old@example.com"
    When the admin updates "Maria321" email to "new@example.com"
    Then "Maria321" has email "new@example.com"
    And an email verification token is created for "new@example.com"
    And the audit log records "update_user" by "GabrielAdmin"
    And the audit log entry stores old email "old@example.com" and new email "new@example.com"

  Scenario: admin bans a common user successfully
    Given the admin "GabrielAdmin" is authenticated
    And the common user "Pedro123" has a public post "Review Ratatouille"
    When the admin bans "Pedro123" with reason "rule violation"
    Then "Pedro123" has status "banned"
    And the post "Review Ratatouille" is hidden from public listings
    And the post "Review Ratatouille" remains stored for moderation history

  Scenario: admin deletes a common user account permanently
    Given the admin "GabrielAdmin" is authenticated
    And the common user "Pedro123" owns the post "Review Ratatouille"
    And the post "Review Ratatouille" has the comment "Legal!"
    When the admin permanently deletes "Pedro123"
    Then the user "Pedro123" is removed
    And the post "Review Ratatouille" is removed
    And the comment "Legal!" is removed
    And the audit log records "delete_user" by "GabrielAdmin"

  Scenario: admin registers a new voice actor successfully
    Given the admin "GabrielAdmin" is authenticated
    And no catalog contributor exists with name "Wendel Bezerra"
    When the admin registers the contributor "Wendel Bezerra" with role "voice-actor"
    Then the catalog stores "Wendel Bezerra" with role "voice-actor"
    And the audit log records "create_artist" by "GabrielAdmin"

  Scenario: admin tries to register an artist without a name and is rejected
    Given the admin "GabrielAdmin" is authenticated
    And the catalog has no contributor with an empty name
    When the admin registers a contributor with name "" and role "artist"
    Then the system returns the validation error "name is required"
    And no contributor with an empty name is stored in the catalog

  Scenario: admin searches for an artist by partial name
    Given the admin "GabrielAdmin" is authenticated
    And the catalog contains the contributor "Fernanda Montenegro" with role "artist"
    And the catalog contains the contributor "Wendel Bezerra" with role "voice-actor"
    When the admin searches catalog contributors by the term "Fern"
    Then the search results include "Fernanda Montenegro"
    And the search results do not include "Wendel Bezerra"

  Scenario: admin creates a news post with tags
    Given the admin "GabrielAdmin" is authenticated
    And no news post exists with title "New season announced"
    When the admin creates a news post titled "New season announced" with body "The new season starts in June"
    And the admin sets the news tags to "series,release"
    Then the news post "New season announced" is stored with tags "series,release"
    And common users can see the news post "New season announced" on the feed
    And the audit log records "create_news" by "GabrielAdmin"

  Scenario: audit log records the registration of a new artist
    Given the admin "GabrielAdmin" is authenticated
    When the admin registers the contributor "Neil Gaiman" with role "author"
    And the admin requests the audit log filtered by actor "GabrielAdmin" and action "create_artist"
    Then the audit log contains an entry for "Neil Gaiman"
    And the entry stores the actor "GabrielAdmin", action "create_artist" and target type "artist"
