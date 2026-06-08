"""Content Search feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/ContentSearch.feature', 'search content by exact match')
def test_search_content_by_exact_match():
    """search content by exact match."""


@scenario('features/ContentSearch.feature', 'search content by title')
def test_search_content_by_title():
    """search content by title."""


@scenario('features/ContentSearch.feature', 'search content with a non-existent term')
def test_search_content_with_a_nonexistent_term():
    """search content with a non-existent term."""


@scenario('features/ContentSearch.feature', 'search content with a spelling mistake')
def test_search_content_with_a_spelling_mistake():
    """search content with a spelling mistake."""


@given('the system has some content stored')
def _():
    """the system has some content stored."""
    raise NotImplementedError


@when('I search for the term "Avengers: Endgame"')
def _():
    """I search for the term "Avengers: Endgame"."""
    raise NotImplementedError


@when('I search for the term "Titanic"')
def _():
    """I search for the term "Titanic"."""
    raise NotImplementedError


@when('I search for the term "UnknownTitle123"')
def _():
    """I search for the term "UnknownTitle123"."""
    raise NotImplementedError


@when('I search for the term "Vingadoes"')
def _():
    """I search for the term "Vingadoes"."""
    raise NotImplementedError


@then('I can see a "No results found" screen')
def _():
    """I can see a "No results found" screen."""
    raise NotImplementedError


@then('I can see the list of works that exactly match the searched term')
def _():
    """I can see the list of works that exactly match the searched term."""
    raise NotImplementedError


@then('I can see works that match the searched term')
def _():
    """I can see works that match the searched term."""
    raise NotImplementedError


@then('I can still see the searched term "Vingadoes" in the search bar')
def _():
    """I can still see the searched term "Vingadoes" in the search bar."""
    raise NotImplementedError


@then('no works are returned for the searched term')
def _():
    """no works are returned for the searched term."""
    raise NotImplementedError


@then('the returned results contain works with the term in the title, synopsis or description')
def _():
    """the returned results contain works with the term in the title, synopsis or description."""
    raise NotImplementedError

