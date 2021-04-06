"""
Abstract wrapper module
"""

from abc import ABC


class AbstractWrapper(ABC):
    """abstract base class for wrappers"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper
