from typing import List, Type

from base import BaseFreelanceService
from utils import measure_time
from freelance_services.weblancer.service import WeblancerService


class FreelanceServiceManager:
    ''' Class for executing several or one parsing services '''

    def __init__(self, services:List[Type[BaseFreelanceService]]):
        self.services = services

    def start(self):
        for service in self.services:
            service_instance = service()
            service_instance.exec()

@measure_time
def main():
    service_list = [
        WeblancerService
    ]
    manager = FreelanceServiceManager(service_list)
    manager.start()

if __name__ == '__main__':
    main()