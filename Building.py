
class Building:
    def __init__(self, id):
        self.data = self.load_csv_data()
        self.initialization()

    def publish_data(self, time_index):
        pass

    def initialization(self):
        """
        initialization on fiware platform
        :return:
        """
        pass

    def load_csv_data(self):
        csv_data = read_from_csv() # TODO
        return csv_data


