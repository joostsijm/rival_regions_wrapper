"""Wrapper test"""

import pytest

from rival_regions_wrapper.api_wrapper import Profile


@pytest.fixture
def profile_keys():
    """Standard key from profile"""
    return ['profile_id', 'name', 'level', 'level_percentage', 'strenght', 'education', 'endurance']

@pytest.mark.vcr()
def test_profile_info(profile_keys):
    """Test an API call to get client info"""

    profile_instance = Profile(192852686)
    response = profile_instance.info()
    print(response)

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
        'profile_id', 'oil', 'ore', 'uranium', 'diamonds', 'liquid_oxygen', 'rivalium',
        'antirad', 'energy_drink', 'spacerockets', 'lss', 'tanks', 'aircrafts',
        'missiles', 'bombers', 'battleships', 'laser_drones', 'moon_tanks', 'space_stations'
    ]
