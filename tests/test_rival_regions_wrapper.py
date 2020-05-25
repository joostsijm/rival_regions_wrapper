"""Wrapper test"""

from datetime import datetime

import pytest

from rival_regions_wrapper.api_wrapper import Profile, Storage, Market, ResourceState, Perks, \
    Craft, Overview, War


@pytest.fixture
def profile_keys():
    """Standard key from profile"""
    return ['profile_id', 'name', 'level', 'level_percentage', 'strenght', 'education', 'endurance']

@pytest.mark.vcr()
def test_profile_info(profile_keys):
    """Test an API call to get client info"""
    profile_instance = Profile(192852686)
    response = profile_instance.info()

    assert isinstance(response, dict), "The response should be a dict"
    assert response['profile_id'] == 192852686, "The ID should be in the response"
    assert set(profile_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['name'], str), "Name should be a string"
    assert isinstance(response['level'], int), "level should be a int"
    assert isinstance(response['level_percentage'], int), "level_percentage should be a int"
    assert isinstance(response['strenght'], int), "strenght should be a int"
    assert isinstance(response['education'], int), "education should be a int"
    assert isinstance(response['endurance'], int), "endurance should be a int"

@pytest.fixture
def storage_keys():
    """Standard keys for storage"""
    return [
        'oil', 'ore', 'uranium', 'diamonds', 'liquid_oxygen',
        'helium-3', 'rivalium', 'antirad', 'energy_drink', 
        'spacerockets', 'lss', 'tanks', 'aircrafts', 'missiles', 
        'bombers', 'battleships', 'laser_drones', 'moon_tanks', 'space_stations',
        'oil_max', 'ore_max', 'uranium_max', 'diamonds_max', 'liquid_oxygen_max',
        'helium-3_max', 'rivalium_max', 'antirad_max', 'energy_drink_max', 
        'spacerockets_max', 'lss_max', 'tanks_max', 'aircrafts_max', 'missiles_max', 
        'bombers_max', 'battleships_max', 'laser_drones_max', 'moon_tanks_max', 'space_stations'
    ]

@pytest.mark.vcr()
def test_storage_info(storage_keys):
    """Test an API call to get storage info"""
    response = Storage.info()

    assert isinstance(response, dict), "The response should be a dict"
    assert set(storage_keys).issubset(response.keys()), "All keys should be in the response"

@pytest.fixture
def market_keys():
    """Standard keys for storage"""
    return ['player_id', 'player_name', 'price', 'amount']

@pytest.mark.vcr()
def test_market_info(market_keys):
    """Test an API call to get market info"""
    resource = 'oil'
    response = Market.info(resource)

    assert isinstance(response, list), "The response should be a list"
    if response:
        assert isinstance(response[0], dict), "The first element should be a dict"
        assert set(market_keys).issubset(response[0].keys()), "All keys should be in the response"
        assert isinstance(response[0]['player_id'], int), "The player_id should be a int"
        assert isinstance(response[0]['player_name'], str), "The player_name should be a int"
        assert isinstance(response[0]['price'], int), "The price should be a int"
        assert isinstance(response[0]['amount'], int), "The price should be a int"

@pytest.fixture
def resource_keys():
    """Standard keys for resource"""
    return ['region_id', 'region_name', 'explored', 'maximum', 'deep_exploration', 'limit_left']

@pytest.mark.vcr()
def test_resource_state_info(resource_keys):
    """Test an API call to get market info"""
    state = 3382
    resource = 'oil'
    response = ResourceState.info(state, resource)

    assert isinstance(response, list), "The response should be a list"
    if response:
        assert isinstance(response[0], dict), "The first element should be a dict"
        assert set(resource_keys).issubset(response[0].keys()), "All keys should be in the response"
        assert isinstance(response[0]['region_id'], int), "The region_id should be a int"
        assert isinstance(response[0]['region_name'], str), "The region_name should be a str"
        assert isinstance(response[0]['explored'], float), "The explored should be a float"
        assert isinstance(response[0]['maximum'], int), "The maximum should be a int"
        assert isinstance(response[0]['deep_exploration'], int), "deep_exploration should be int"
        assert isinstance(response[0]['limit_left'], int), "The limit_left should be a int"

@pytest.fixture
def perks_keys():
    """Standard keys for perks"""
    return ['strenght', 'education', 'endurance', 'upgrade_date', 'upgrade_perk']

@pytest.mark.vcr()
def test_perks_info(perks_keys):
    """Test an API call to get perks info"""
    response = Perks.info()

    assert isinstance(response, dict), "The response should be a dict"
    assert set(perks_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['strenght'], int), "strengt should be an int"
    assert isinstance(response['education'], int), "educatino should be an int"
    assert isinstance(response['endurance'], int), "endurance should be an int"
    assert isinstance(response['upgrade_date'], datetime), "upgrade_date should be a date"
    assert isinstance(response['upgrade_perk'], int), "upgrade_perk should be an int"

@pytest.fixture
def craft_keys():
    """Standard keys for craft"""
    return ['market_price', 'resources']

@pytest.mark.vcr()
def test_craft_produce():
    """Test an API call to produce new item"""
    item = 'energy_drink'
    Craft.produce(item, 10)

    assert True

@pytest.fixture
def overview_info_keys():
    """Standard keys for overview info"""
    return ['perks', 'war']

@pytest.mark.vcr()
def test_overview_info(overview_info_keys):
    """Test an API call for overview"""
    response = Overview.info()

    assert isinstance(response, dict), "The response hould be a dict"
    assert set(overview_info_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['war'], dict), "The war key should be a dict"

@pytest.fixture
def overview_status_keys():
    """Standard kenys for overview status"""
    return ['profile_id', 'party_id', 'gold', 'money', 'level', 'exp']

@pytest.mark.vcr()
def test_overview_status(overview_status_keys):
    """Test an API cal for status"""
    response = Overview.status()

    assert isinstance(response, dict), "The response hould be a dict"
    assert set(overview_status_keys).issubset(response.keys()), "All keys should be in the response"

@pytest.mark.vcr()
def test_war_page():
    """Test getting training war"""
    response = War.page()

    assert isinstance(response, dict), "The response should be a dict"
    assert isinstance(response['training_war'], int), "The training_war should be an int"

@pytest.mark.vcr()
def test_war_info():
    """Test war info"""
    war_page = War.page()
    print(war_page['training_war'])
    war_id = war_page['training_war']
    response = War.info(war_id)

    print(response)
