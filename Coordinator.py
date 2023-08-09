import os
from filip.models.base import FiwareHeader
from filip.clients.ngsi_v2 import ContextBrokerClient

#Get the same context broker client
CB_URL = os.getenv('CB_URL')
fiware_header = FiwareHeader(service=os.getenv('Service'),
                             service_path=os.getenv('Service_path'))

class EnergySupplier:
    def __init__(self):
        self.cbc = ContextBrokerClient(url=CB_URL, fiware_header=fiware_header)
        self.data = []
        self.data_sum = self.balancing()

    def get_entity(self, id):  # TODO Get corresponding entities
        self.building_entity = self.cbc.get_entity(f"urn:ngsi-ld:Building:{id}")
        return self.building_entity

    def read_data(self):  # TODO Get corresponding datas from entities and send to energy supplier
        self.data.append({"time_index": self.building_entity.simtime.value,
                          "demand": self.building_entity.demand.value,
                          "production": self.building_entity.production.value})
        self.data_sum = self.balancing()
        return self.data

    def balancing(self):  # TODO Calculate the amount of traded electricity with grid
        total_production = sum(pro["production"] for pro in self.data)
        total_demand = sum(dem["demand"] for dem in self.data)
        return total_production - total_demand

    def accounting(self, time_index):
        if self.data_sum == 0:
            print(f"Between {time_index}h and {time_index + 1}h there's no exchange with grid.")
        elif self.data_sum > 0:
            print(f"Between {time_index}h and {time_index + 1}h {self.data_sum}kwh electricity can be sold to grid.")
        else:
            print(f"Between {time_index}h and {time_index + 1}h {abs(self.data_sum)}kwh electricity should be bought from grid.")


class Coordinator:
    pass