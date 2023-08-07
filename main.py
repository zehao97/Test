from Building import Building
from Coordinator import Coordinator


if __name__ == '__main__':
    #call Class Buidling
    buildings = [Building(id=i) for i in range(5)]  # TODO set the id properly
    #define lists to store historical data
    buildings_demand = []
    buildings_production = []

    time_index = list(range(24))
    for i in time_index:
        # Step 1
        for building in buildings:
            building.publish_data(time_index=i)
            #Get corresponding entities and add values to history
            building_entity = building.cbc.get_entity(entity_id=building.building_device().entity_name,
                                                      entity_type=building.building_device().entity_type)
            buildings_demand.append({"time_index": building_entity.simtime.value,
                                     "demand": building_entity.demand.value})
            buildings_production.append({"time_index": building_entity.simtime.value,
                                         "production": building_entity.production.value})
    # close the mqtt listening thread
    building.mqttc.loop_stop()

    # disconnect the mqtt device
    building.mqttc.disconnect()

    #Step 2
    #call Class Coordinator
    coordinator = Coordinator()
    # TODO market algorithm
    coordinator.read_data()
    coordinator.balancing()
    coordinator.feed_back()

    # Step 3
    # TODO not necessarily required
    for building in buildings:
        building.do_something_after_the_balancing_if_necessary()

    #TODO
    #plot()
