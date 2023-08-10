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
        self.data_sum = 0

    def get_entity(self, id):  # TODO Get corresponding entities
        self.building_entity = self.cbc.get_entity(f"urn:ngsi-ld:Building:{id}")
        print('\nBuilding Entity:') # TODO TEST
        print(
            {
                "simtime": self.building_entity.simtime.value,
                "demand": self.building_entity.demand.value,
                "production": self.building_entity.production.value
            }
        ) # TODO TEST

    def read_data(self):  # TODO Get corresponding datas from entities and send to energy supplier
        self.data.append({"time_index": self.building_entity.simtime.value,
                          "demand": self.building_entity.demand.value,
                          "production": self.building_entity.production.value})
        # print('\n Data:') # TODO TEST
        # print(self.data) # TODO TEST

    def balancing(self):  # TODO Calculate the amount of traded electricity with grid
        total_production = sum(pro["production"] for pro in self.data)
        total_demand = sum(dem["demand"] for dem in self.data)
        self.data_sum = total_production - total_demand
        print('\n Sum of Data:') # TODO TEST
        print(self.data_sum) # TODO TEST

    def announcing(self, time_index):
        if self.data_sum == 0:
            print(f"Between {time_index}h and {time_index + 1}h there's no exchange with grid.")
        elif self.data_sum > 0:
            print(f"Between {time_index}h and {time_index + 1}h {self.data_sum}kwh electricity can be sold to grid.")
        else:
            print(f"Between {time_index}h and {time_index + 1}h {abs(self.data_sum)}kwh electricity should be bought from grid.")
        #clear the list after been used
        self.data.clear()
        self.data_sum = 0

    def accounting(self, time_index):
        if self.data_sum == 0:
            print(f"Between {time_index}h and {time_index + 1}h no exchange with grid.")
        elif self.data_sum > 0:
            print(f"Between {time_index}h and {time_index + 1}h {self.data_sum}kwh electricity were sold to grid.")
        else:
            print(f"Between {time_index}h and {time_index + 1}h {abs(self.data_sum)}kwh electricity were bought from grid.")
        self.data.clear()
        self.data_sum = 0

