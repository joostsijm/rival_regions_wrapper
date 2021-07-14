"""Wrapper test"""

# pylint: disable=redefined-outer-name

from datetime import datetime, timedelta

import pytest

from rival_regions_wrapper.wrapper import Profile, Storage, Market, \
        ResourceState, Perks, Craft, Overview, War, Work, Article, \
        Conference, LanguageChat


@pytest.fixture
def profile_keys():
    """Standard key from profile"""
    return [
            'profile_id', 'name', 'level', 'level_percentage', 'strenght',
            'education', 'endurance'
        ]


@pytest.mark.vcr()
def test_profile_info(middleware, profile_keys):
    """Test an API call to get client info"""
    profile_instance = Profile(middleware, 192852686)
    response = profile_instance.info()

    assert isinstance(response, dict), "The response should be a dict"
    assert response['profile_id'] == 192852686, \
        "The ID should be in the response"
    assert set(profile_keys).issubset(response.keys()), \
        "All keys should be in the response"
    assert isinstance(response['name'], str), "Name should be a string"
    assert isinstance(response['level'], int), "level should be a int"
    assert isinstance(response['level_percentage'], int), \
        "level_percentage should be a int"
    assert isinstance(response['strenght'], int), "strenght should be a int"
    assert isinstance(response['education'], int), "education should be a int"
    assert isinstance(response['endurance'], int), "endurance should be a int"


@pytest.mark.skip(reason="message request")
def test_profile_message(middleware, profile_id, message):
    """Test an API to send message to profile"""
    Profile(middleware, profile_id).message(message)


@pytest.fixture
def storage_keys():
    """Standard keys for storage"""
    return [
            'oil', 'ore', 'uranium', 'diamonds', 'liquid_oxygen',
            'helium-3', 'rivalium', 'antirad', 'energy_drink',
            'spacerockets', 'lss', 'tanks', 'aircrafts', 'missiles',
            'bombers', 'battleships', 'laser_drones', 'moon_tanks',
            'space_stations', 'oil_max', 'ore_max', 'uranium_max',
            'diamonds_max', 'liquid_oxygen_max', 'helium-3_max',
            'rivalium_max', 'antirad_max', 'energy_drink_max',
            'spacerockets_max', 'lss_max', 'tanks_max', 'aircrafts_max',
            'missiles_max', 'bombers_max', 'battleships_max',
            'laser_drones_max', 'moon_tanks_max', 'space_stations'
        ]


@pytest.mark.vcr()
def test_storage_info(middleware, storage_keys):
    """Test an API call to get storage info"""
    response = Storage(middleware).info()

    assert isinstance(response, dict), "The response should be a dict"
    assert set(storage_keys).issubset(response.keys()), \
        "All keys should be in the response"


@pytest.fixture
def market_keys():
    """Standard keys for storage"""
    return ['player_id', 'player_name', 'price', 'amount']


@pytest.mark.vcr()
def test_market_info(middleware, market_keys):
    """Test an API call to get market info"""
    resource = 'oil'
    response = Market(middleware).info(resource)

    assert isinstance(response, list), "The response should be a list"
    if response:
        assert isinstance(response[0], dict), \
            "The first element should be a dict"
        assert set(market_keys).issubset(response[0].keys()), \
            "All keys should be in the response"
        assert isinstance(response[0]['player_id'], int), \
            "The player_id should be a int"
        assert isinstance(response[0]['player_name'], str), \
            "The player_name should be a int"
        assert isinstance(response[0]['price'], int), \
            "The price should be a int"
        assert isinstance(response[0]['amount'], int), \
            "The price should be a int"


@pytest.fixture
def resource_keys():
    """Standard keys for resource"""
    return [
            'region_id', 'region_name', 'explored', 'maximum',
            'deep_exploration', 'limit_left'
        ]


@pytest.mark.vcr()
def test_resource_state_info(middleware, resource_keys):
    """Test an API call to get market info"""
    state = 3382
    resource = 'oil'
    response = ResourceState(middleware, state).info(resource)

    assert isinstance(response, list), "The response should be a list"
    if response:
        assert isinstance(response[0], dict), \
            "The first element should be a dict"
        assert set(resource_keys).issubset(response[0].keys()), \
            "All keys should be in the response"
        assert isinstance(response[0]['region_id'], int), \
            "The region_id should be a int"
        assert isinstance(response[0]['region_name'], str), \
            "The region_name should be a str"
        assert isinstance(response[0]['explored'], float), \
            "The explored should be a float"
        assert isinstance(response[0]['maximum'], int), \
            "The maximum should be a int"
        assert isinstance(response[0]['deep_exploration'], int), \
            "deep_exploration should be int"
        assert isinstance(response[0]['limit_left'], int), \
            "The limit_left should be a int"


@pytest.fixture
def perks_keys():
    """Standard keys for perks"""
    return [
            'strenght', 'education', 'endurance', 'upgrade_date',
            'upgrade_perk'
        ]


@pytest.mark.vcr()
def test_perks_info(middleware, perks_keys):
    """Test an API call to get perks info"""
    response = Perks(middleware).info()

    assert isinstance(response, dict), \
        "The response should be a dict"
    assert set(perks_keys).issubset(response.keys()), \
        "All keys should be in the response"
    assert isinstance(response['strenght'], int), "strengt should be an int"
    assert isinstance(response['education'], int), "educatino should be an int"
    assert isinstance(response['endurance'], int), "endurance should be an int"

    try:
        assert isinstance(response['upgrade_date'], datetime), \
            "upgrade_date should be a date"
        assert isinstance(response['upgrade_perk'], int), \
            "upgrade_perk should be an int"
    except AssertionError:
        assert isinstance(response['upgrade_date'], type(None)), \
            "upgrade_date should be None if not upgrading"
        assert isinstance(response['upgrade_perk'], type(None)), \
            "upgrade_perk should be an int"


@pytest.mark.skip(reason="Update request")
def test_perks_upgrade(middleware, perk, perk_upgrade_type):
    """Test an API call to upgrade perk"""
    Perks(middleware).upgrade(perk, perk_upgrade_type)


@pytest.fixture
def craft_keys():
    """Standard keys for craft"""
    return ['market_price', 'resources']


@pytest.mark.skip(reason="Update request")
def test_craft_produce(middleware, craft_item, craft_amount):
    """Test an API call to craft a new item"""
    Craft(middleware).produce(craft_item, craft_amount)
    assert True


@pytest.fixture
def overview_info_keys():
    """Standard keys for overview info"""
    return ['perks', 'war']


@pytest.mark.vcr()
def test_overview_info(middleware, overview_info_keys):
    """Test an API call for overview"""
    response = Overview(middleware).info()

    assert isinstance(response, dict), "The response hould be a dict"
    assert set(overview_info_keys).issubset(response.keys()), \
        "All keys should be in the response"
    assert isinstance(response['war'], dict), "The war key should be a dict"


@pytest.fixture
def overview_status_keys():
    """Standard kenys for overview status"""
    return [
            'profile_id', 'party_id', 'gold', 'money', 'level', 'exp'
        ]


@pytest.mark.vcr()
def test_overview_status(middleware, overview_status_keys):
    """Test an API cal for status"""
    response = Overview(middleware).status()

    assert isinstance(response, dict), "The response hould be a dict"
    assert set(overview_status_keys).issubset(response.keys()), \
        "All keys should be in the response"


@pytest.mark.vcr()
def test_war_page(middleware):
    """Test getting training war"""
    response = War(middleware).page()

    assert isinstance(response, dict), "The response should be a dict"
    if response['training_war']:
        assert isinstance(response['training_war'], int), \
            "The training_war should be an int"


@pytest.mark.vcr()
def test_war_info(middleware):
    """Test war info"""
    war = War(middleware)
    war_page = war.page()
    war_id = war_page['training_war']
    response = war.info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert isinstance(response['damage'], int), \
        "Damage should be an int"
    assert isinstance(response['attack_hourly_available'], bool), \
        "Attack hourly should be a bool"
    assert isinstance(response['energ_drinks'], int), \
        "Energy drinks should be an int"
    if 'max_hero_name' in response:
        assert isinstance(response['max_hero_name'], str), \
            "max hero name should be a str"
    if 'max_hero_damage' in response:
        assert isinstance(response['max_hero_damage'], int), \
            "max hero damage should be an int"
    if 'time_left' in response:
        assert isinstance(response['time_left'], timedelta), \
            "time left should be a time delta"
    assert isinstance(response['finish_date'], datetime), \
        "Finish date should be a date"
    assert isinstance(response['war_units'], dict), \
        "war units should be a dict"


@pytest.mark.vcr()
def test_war_info_ground_war(middleware):
    """Test war info"""
    war_id = 329541
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'war', "Type should be a ground war"
    assert isinstance(response['attack'], dict), "Attack should be a dict"
    assert isinstance(response['attack']['state_id'], int), \
        "State id should be an integer"
    assert isinstance(response['attack']['state_name'], str), \
        "State nameshould be a string"
    assert isinstance(response['attack']['region_id'], int), \
        "Region id should be an integer"
    assert isinstance(response['attack']['region_name'], str), \
        "Region name should be a string"
    assert isinstance(response['attack']['damage'], int), \
        "Damage should be an intger"
    assert isinstance(response['defend']['state_id'], int), \
        "State id should be an integer"
    assert isinstance(response['defend']['state_name'], str), \
        "State name should be a string"
    assert isinstance(response['defend']['region_id'], int), \
        "Region id should be an integer"
    assert isinstance(response['defend']['region_name'], str), \
        "Region name should be a string"
    assert isinstance(response['defend']['damage'], int), \
        "Damage should be an integer"


@pytest.mark.vcr()
def test_war_info_coup(middleware):
    """Test war info"""
    war_id = 329518
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'coup', "Type should be a coup"


@pytest.mark.vcr()
def test_war_info_revolution(middleware):
    """Test war info"""
    war_id = 329461
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'revolution', "Type should be a revolution"


@pytest.mark.vcr()
def test_war_info_trooper_war(middleware):
    """Test war info"""
    war_id = 329458
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'troopers war', "Type should be a trooper war"


@pytest.mark.vcr()
def test_war_info_sea_war(middleware):
    """Test war info"""
    war_id = 329618
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'sea war', "Type should be a sea war"


@pytest.mark.vcr()
def test_war_info_space_war(middleware):
    """Test war info"""
    war_id = 329531
    response = War(middleware).info(war_id)

    assert isinstance(response, dict), "The response should be a dict"
    assert response['type'] == 'space war', "Type should be a space war"


@pytest.mark.vcr()
def test_work_info(middleware):
    """Test work info"""
    response = Work(middleware).page()

    assert isinstance(response, dict), "The response should be a dict"
    assert isinstance(response['factory'], dict), "Factory should be a dict"
    assert isinstance(response['resources_left'], dict), \
        "Resources left should be a dict"
    assert isinstance(response['work_exp'], dict), "Work exp should be a dict"


@pytest.fixture
def article_keys():
    """Standard key fro article"""
    return [
            'article_id', 'article_title', 'newspaper_id', 'newspaper_name',
            'author_name', 'author_id', 'region_name', 'region_id',
            'content_text', 'content_html', 'language', 'rating', 'comments',
            'post_date'
        ]


@pytest.mark.vcr()
def test_article_info_one(middleware, article_keys):
    """Test article info"""
    article_id = 2708696
    response = Article(middleware).info(article_id)

    assert isinstance(response, dict), "The resonse should be a dict"
    assert set(article_keys).issubset(response.keys()), \
        "All keys should be in the response"
    assert isinstance(response['article_id'], int), \
        "Article id should be an integer"
    assert isinstance(response['article_title'], str), \
        "Article title should be a str"
    assert isinstance(response['newspaper_id'], int), \
        "Newspaper id should be an integer"
    assert isinstance(response['newspaper_name'], str), \
        "Newspaper name should be a string"
    assert isinstance(response['author_name'], str), \
        "Author name should be a string"
    assert isinstance(response['author_id'], int), \
        "Author id should be an integer"
    assert isinstance(response['region_name'], str), \
        "Region name should be a string"
    assert isinstance(response['region_id'], int), \
        "Region id should be an integer"
    assert isinstance(response['content_text'], str), \
        "Content text should be a string"
    assert isinstance(response['content_html'], str), \
        "Content html should be a string"
    assert isinstance(response['language'], str), \
        "Language should be a string"
    assert isinstance(response['rating'], int), \
        "Rating should be an integer"
    assert isinstance(response['comments'], int), \
        "Comments should be an integer"
    assert isinstance(response['post_date'], datetime), \
        "Post date should be a datetime"


@pytest.mark.vcr()
def test_article_info_two(middleware, article_keys):
    """Test article info"""
    article_id = 2862982
    response = Article(middleware).info(article_id)

    assert isinstance(response, dict), "The resonse should be a dict"
    assert set(article_keys).issubset(response.keys()), \
        "All keys should be in the response"
    assert isinstance(response['article_id'], int), \
        "Article id should be an integer"
    assert isinstance(response['article_title'], str), \
        "Article title should be a str"
    assert response['newspaper_id'] is None, "Newspaper id should be none"
    assert response['newspaper_name'] is None, "Newspaper name should be none"
    assert isinstance(response['author_name'], str), \
        "Author name should be a string"
    assert isinstance(response['author_id'], int), \
        "Author id should be an integer"
    assert isinstance(response['region_name'], str), \
        "Region name should be a string"
    assert isinstance(response['region_id'], int), \
        "Region id should be an integer"
    assert isinstance(response['content_text'], str), \
        "Content text should be a string"
    assert isinstance(response['content_html'], str), \
        "Content html should be a string"
    assert isinstance(response['language'], str), "Language should be a string"
    assert isinstance(response['rating'], int), "Rating should be an integer"
    assert isinstance(response['comments'], int), \
        "Comments should be an integer"
    assert isinstance(response['post_date'], datetime), \
        "Post date should be a datetime"


@pytest.mark.skip(reason="conference message request")
def test_conference_message(middleware, conference_id, message):
    """Test conference message"""
    Conference(middleware, conference_id).message(message)


@pytest.mark.skip(reason="conference notification request")
def test_conference_notification(middleware, conference_id, message):
    """Test conference notification"""
    Conference(middleware, conference_id).notification(message, True)


@pytest.mark.skip(reason="conference title change request")
def test_conference_change_title(middleware, conference_id, conference_title):
    """Test conference change title"""
    Conference(middleware, conference_id).change_title(conference_title)


@pytest.mark.skip(reason="language chat message request")
def test_language_chat_message(middleware, language_chat, message):
    """Test sending message to language chat"""
    LanguageChat(middleware, language_chat).message(message)
