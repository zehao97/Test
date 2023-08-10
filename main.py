from Building import Building
from Coordinator import EnergySupplier
from filip.models.base import FiwareHeader
from filip.utils.cleanup import clear_context_broker, clear_iot_agent
import os

from filip.clients.ngsi_v2 import ContextBrokerClient # TODO TEST

# Create the fiware header
fiware_header = FiwareHeader(service=os.getenv('Service'),
                             service_path=os.getenv('Service_path'))
CB_URL = os.getenv('CB_URL')
IOTA_URL = os.getenv('IOTA_URL')
MQTT_Broker_URL = os.getenv('MQTT_Broker_URL')


if __name__ == '__main__':
    clear_context_broker(url=CB_URL, fiware_header=fiware_header)
    clear_iot_agent(url=IOTA_URL, fiware_header=fiware_header)
    cbc = ContextBrokerClient(url=CB_URL, fiware_header=fiware_header) # TODO TEST

    # define energy supplier to handle the energy data
    supplier = EnergySupplier()
    #call Class Buidling
    buildings = [Building(id=i) for i in range(6)]  # TODO set the id properly
    time_index = list(range(3))

    # It happens before the i o'clock. It's the process that building communicate with energy supplier.
    for i in time_index:
        # Step 1
        for building in buildings:
            building.publish_data(time_index=i)
            temp = building.data_demand[i]
            # building_000_entity = cbc.get_entity(f"urn:ngsi-ld:Building:{buildings.index(building)}") # TODO TEST
            # print('\nPublish Entity:') #TODO TEST
            # print(building_000_entity) #TODO TEST
            #Get corresponding entities and send datas to energy supplier
            supplier.get_entity(id=buildings.index(building))
            supplier.read_data()

        # supplier knows how much electricity should be traded between i and i+1 h
        supplier.balancing()
        supplier.announcing(time_index=i)

        # send the data between i and i+1h
        for building in buildings:
            building.publish_data(time_index=i)

            #Get corresponding entities and send datas to energy supplier
            supplier.get_entity(id=buildings.index(building))
            supplier.read_data()

        # supplier knows how much electricity have been traded between i and i+1 h
        supplier.balancing()
        supplier.accounting(time_index=i)

    # Shut down
    for building in buildings:
        building.shutdown()

    #Step 2
    #call Class Coordinator
    #coordinator = Coordinator()
    # TODO market algorithm
    #coordinator.read_data()
    #coordinator.balancing()
    #coordinator.feed_back()

    # Step 3
    # TODO not necessarily required
    #for building in buildings:
    #    building.do_something_after_the_balancing_if_necessary()

    #TODO
    #plot()
