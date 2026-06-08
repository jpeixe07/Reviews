"""Trending Filter feature tests."""

from pytest_bdd import given, scenario, then, when
from datetime import datetime, timedelta
import logging

# ==========================================
# SCENARIOS
# ==========================================

@scenario('../features/TrendingFilter.feature', 'Audience Filtering in the Service Layer')
def test_audience_filtering_in_the_service_layer():
    pass

@scenario('../features/TrendingFilter.feature', 'Temporal calculation for the "Trending" ranking')
def test_temporal_calculation_for_the_trending_ranking():
    pass

@scenario('../features/TrendingFilter.feature', 'Category segmentation in the Popularity ranking')
def test_category_segmentation_in_the_popularity_ranking():
    pass

@scenario('../features/TrendingFilter.feature', 'Quorum failure due to insufficient volume')
def test_quorum_failure_due_to_insufficient_volume():
    pass

@scenario('../features/TrendingFilter.feature', 'Relevance failure due to expired time window')
def test_relevance_failure_due_to_expired_time_window():
    pass

# ==========================================
# STEPS (GIVEN)
# ==========================================

@given('that in the database the work "Short Film" has average 5.0 based on 5 ratings')
def setup_short_film(run, db):
    run(db.media.insert_one({"title": "Short Film", "avg_score": 5.0, "review_count": 5, "created_at": datetime.utcnow()}))

@given('the work "The Godfather" has average 4.9 based on 1,200 ratings')
def setup_godfather(run, db):
    run(db.media.insert_one({"title": "The Godfather", "avg_score": 4.9, "review_count": 1200, "created_at": datetime.utcnow()}))

@given('the service rule requires a minimum quorum of 50 ratings for the ranking')
def step_quorum_rule():
    pass # Passo puramente semântico do BDD

@given('the work "Old Classic" has 100,000 total views, with only 10 recorded in the last 30 days')
def setup_old_classic(run, db):
    # Simulate a record from 5 years ago
    past_date = datetime.utcnow() - timedelta(days=365 * 5)
    run(db.media.insert_one({"title": "Old Classic", "view_count": 100000, "created_at": past_date}))

@given('the work "Recent Release" has 500 total views, with 450 recorded in the last 30 days')
def setup_recent_release(run, db):
    now = datetime.utcnow()
    run(db.media.insert_one({"title": "Recent Release", "view_count": 500, "created_at": now}))

@given('the work "Global Blockbuster" is a "movie" with high traction')
def setup_global_blockbuster(run, db):
    run(db.media.insert_one({"title": "Global Blockbuster", "type": "movie", "view_count": 50000, "created_at": datetime.utcnow()}))

@given('the work "National Series" is a "series" with high traction')
def setup_national_series(run, db):
    run(db.media.insert_one({"title": "National Series", "type": "series", "view_count": 45000, "created_at": datetime.utcnow()}))

@given('the database only contains works with fewer than 50 ratings each')
def setup_low_quorum_db(run, db):
    run(db.media.delete_many({}))
    run(db.media.insert_one({"title": "Obscure Indie", "avg_score": 5.0, "review_count": 10, "created_at": datetime.utcnow()}))

@given('the work "1990 Box Office Hit" has 1,000,000 total ratings and 0 ratings in the last 30 days')
def setup_1990_hit(run, db):
    past = datetime.utcnow() - timedelta(days=365 * 10)
    run(db.media.insert_one({"title": "1990 Box Office Hit", "view_count": 1000000, "created_at": past}))

@given('the work "Viral Indie" has 1,000 ratings, all recorded in the last 24 hours')
def setup_viral_indie(run, db):
    run(db.media.insert_one({"title": "Viral Indie", "view_count": 1000, "created_at": datetime.utcnow()}))


# ==========================================
# STEPS (WHEN)
# ==========================================

@when('the service receives a request to generate the "Top Rated" list')
def request_top_rated(client, context):
    context["response"] = client.get("/home")

@when('the service receives a request to process the "Trending" ranking with period set to "month"')
def request_trending_month(client, context):
    context["response"] = client.get("/home?period=month")

@when('the service receives a ranking request with filter set to "series"')
def request_series_filter(client, context):
    context["response"] = client.get("/home?media_type=series")

@when('the service processes the "Trending" ranking incorrectly ignoring the date filter')
def request_ignore_date_filter(client, context):
    # Simulate an 'all time' call bypassing the temporal filter
    context["response"] = client.get("/home?period=all")


# ==========================================
# STEPS (THEN)
# ==========================================

@then('the service processes the aggregation of ratings validating the quorum')
def validate_quorum_processing():
    pass

@then('returns a dataset that includes the work "The Godfather"')
def check_godfather_included(context):
    data = context["response"].json()
    titles = [item["title"] for item in data.get("top_rated", [])]
    assert "The Godfather" in titles

@then('completely omits the work "Short Film" from the generated response.')
def check_short_film_omitted(context):
    data = context["response"].json()
    titles = [item["title"] for item in data.get("top_rated", [])]
    assert "Short Film" not in titles

@then('the service performs the query filtering interactions only by the recent 30-day period')
def validate_temporal_filtering():
    pass

@then('returns the result list ranking "Recent Release" higher than "Old Classic".')
def validate_temporal_ranking(context):
    data = context["response"].json()
    titles = [item["title"] for item in data.get("trending", [])]
    
    assert "Recent Release" in titles
    # "Old Classic" was created years ago and the router with "?period=month" filters via 'created_at >= 30 days', so it's ignored
    assert "Old Classic" not in titles 

@then('the service applies the category filter')
def validate_category_filter():
    pass

@then('returns the dataset with the work "National Series"')
def validate_national_series(context):
    data = context["response"].json()
    titles = [item["title"] for item in data.get("trending", [])]
    assert "National Series" in titles

@then('omits the work "Global Blockbuster" from the generated response.')
def validate_blockbuster_omitted(context):
    data = context["response"].json()
    titles = [item["title"] for item in data.get("trending", [])]
    assert "Global Blockbuster" not in titles

@then('the service processes the validation and identifies that no work reached the threshold')
def validate_threshold_failure():
    pass

@then('returns an empty dataset instead of listing works with low quorum')
def validate_empty_quorum_dataset(context):
    data = context["response"].json()
    assert len(data.get("top_rated", [])) == 0

@then('the system writes a "WARN: top_rated aggregation returned 0 items. Quorum threshold not met for current period." record for monitoring.')
def validate_quorum_warn_log(caplog):
    # This test will intentionally fail until you add "import logging" in the home router
    # and emit logger.warning("WARN: top_rated aggregation...") when top_rated is empty.
    assert "WARN: top_rated aggregation returned 0 items." in caplog.text

@then('the system should identify the inconsistency between total volume and time-based volume')
def validate_relevance_inconsistency():
    pass

@then('the work "1990 Box Office Hit" should not appear at the top of the "Trending" ranking')
def check_1990_hit_not_top(context):
    data = context["response"].json()
    trending = data.get("trending", [])
    if trending:
        assert trending[0]["title"] != "1990 Box Office Hit"

@then('an "ERROR: trending aggregation bypassed temporal date_filter." alert should be recorded in the logs.')
def check_error_log(caplog):
    # Again, this will fail in TDD until the developer logs this specific case in the backend logger.
    assert "ERROR: trending aggregation bypassed temporal date_filter." in caplog.text