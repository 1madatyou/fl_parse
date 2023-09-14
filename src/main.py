import unittest
from typing import List, Type

from freelance_services.weblancer.service import WeblancerService
from base import BaseFreelanceService


class FreelanceServiceManager:
    ''' Class for executing several or one parsing services '''

    def __init__(self, services:List[Type[BaseFreelanceService]]):
        self.services = services

    def start(self):
        for service in self.services:
            service_instance = service()
            service_instance.exec()


if __name__ == '__main__':
    service_list = [
        WeblancerService
    ]
    manager = FreelanceServiceManager(service_list)
    manager.start()