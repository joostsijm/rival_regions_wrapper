"""
Abstract wrapper module
"""

from abc import ABC


class AbstractWrapper(ABC):
    """abstract base class for wrappers"""

    def __init__(self, middleware):
        self.middleware = middleware
