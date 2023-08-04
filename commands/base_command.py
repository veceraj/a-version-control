"""Command module"""
from abc import ABCMeta, abstractmethod


class IRunnable(metaclass=ABCMeta):
    """Runnable interface"""

    @abstractmethod
    def run(self, args):
        """Run method of interface"""
