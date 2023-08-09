from Building import Building
from Coordinator import Coordinator, EnergySupplier
from filip.models.base import FiwareHeader
from filip.utils.cleanup import clear_context_broker, clear_iot_agent
import os

# Create the fiware header
fiware_header = FiwareHeader(service=os.getenv('Service'),
                             service_path=os.getenv('Service_path'))
CB_URL = os.getenv('CB_URL')
IOTA_URL = os.getenv('IOTA_URL')
MQTT_Broker_URL = os.getenv('MQTT_Broker_URL')


if __name__ == '__main__':
    clear_context_broker(url=CB_URL, fiware_header=fiware_header)
    clear_iot_agent(url=IOTA_URL, fiware_header=fiware_header)

    # define energy supplier to handle the energy data
    supplier = EnergySupplier()
    #call Class Buidling
    buildings = [Building(id=i) for i in range(5)]  # TODO set the id properly
    time_index = list(range(3))
    for i in time_index:
        # Step 1
        for building in buildings:
            building.publish_data(time_index=i)

            #Get corresponding entities and send datas to energy supplier
            supplier.get_entity(id=buildings.index(building))
            supplier.read_data()

            # close the mqtt listening thread
            building.mqttc.loop_stop()

            # disconnect the mqtt device
            building.mqttc.disconnect()
        supplier.accounting(time_index=i)


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
