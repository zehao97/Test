from Building import Building
from Coordinator import Coordinator


if __name__ == '__main__':
    buildings = [Building(id=i) for i in range(5)]  # TODO set the id properly
    coordinator = Coordinator()
    time_index = [...]
    for i in time_index:
        # Step 1
        for building in buildings:
            building.publish_data(time_index=i)

        # Step 2
        # TODO market algorithm
        coordinator.read_data()
        coordinator.balancing()
        coordinator.feed_back()

        # Step 3
        # TODO not necessarily required
        for building in buildings:
            building.do_something_after_the_balancing_if_necessary()

    #TODO
    plot()
