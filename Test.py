#import from filip
import time

from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient
from filip.clients.mqtt import IoTAMQTTClient
from filip.models.base import FiwareHeader
from filip.utils.cleanup import clear_context_broker, clear_iot_agent
from filip.models.ngsi_v2.context import ContextEntity, NamedContextAttribute

#import form packages
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import pandas as pd
import json
import matplotlib.pyplot as plt

#verschiedene URL
CB_URL= "http://134.130.166.184:1026"
IOTA_URL= "http://134.130.166.184:4041"
QL_URL="http://134.130.166.184:8668"
MQTT_URL="http://134.130.166.184:1883"

#database
Service='lem_test'
Servcice_path='/'
Topic_Energy_Building='jdu_zwu'
APIKEY= 'huhuhu'

#simulation time
t_start=0
t_end=23
t_step=1

if __name__ == '__main__':
    #create a fiware header
    fiware_header=FiwareHeader(service=Service,
                               service_path=Servcice_path)

    #clear the state of context broker and iot agent
    clear_context_broker(url=CB_URL,fiware_header=fiware_header)
    clear_iot_agent(url=IOTA_URL,fiware_header=fiware_header)

    #create the clients
    cbc=ContextBrokerClient(url=CB_URL, fiware_header=fiware_header)
    iotac=IoTAClient(url=IOTA_URL,fiware_header=fiware_header)
    mqttc=mqtt.Client(protocol=mqtt.MQTTv5)

    #create context entities for 6 Buildings and add the attributes
    building_00 = ContextEntity(id="urn:ngsi-ld:building:00", type="Building")
    building_01 = ContextEntity(id="urn:ngsi-ld:building:01", type="Building")
    building_02 = ContextEntity(id="urn:ngsi-ld:building:02", type="Building")
    building_03 = ContextEntity(id="urn:ngsi-ld:building:03", type="Building")
    building_04 = ContextEntity(id="urn:ngsi-ld:building:04", type="Building")
    building_05 = ContextEntity(id="urn:ngsi-ld:building:05", type="Building")

    building_description=NamedContextAttribute(name="Description", type="Text", value="The Building involved in the Energymarkt")
    building_00.add_attributes(attrs=[building_description])

    #provision the building entity
    cbc.post_entity(entity=building_00, update=True)

    #check in the context broker if the entities corresponding to the buildings
    cbc.get_entity(entity_id="urn:ngsi-ld:building:00", entity_type="Building")

    #get the energy data of the buildings
    b0_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building0.csv")
    demand_00=list(b0_df["res_load"])
    production_00=list(b0_df["res_inj"])

    b1_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building1.csv")
    b2_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building2.csv")
    b3_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building3.csv")
    b4_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building4.csv")
    b5_df = pd.read_csv("T:\jdu-zwu\Test\operations_1h/building5.csv")

    #define a vocabulary to store the energydata
    building_energy_data= []

    def on_message(client, userdata, msg):
       payload = msg.payload.decode('utf-8')
       building_energy_data.append(json.loads(payload))

    #add call back function to the client
    mqttc.on_message=on_message

    #mqtt connect and subscribe the topic
    mqtt_url=urlparse(MQTT_URL)
    mqttc.connect(host=mqtt_url.hostname,
                 port=mqtt_url.port,
                 keepalive=60,
                 bind_address="",
                 bind_port=0,
                 clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                 properties=None)
    mqttc.subscribe(topic=Topic_Energy_Building)

    # create a non-blocking thread for mqtt communication
    mqttc.loop_start()

    #create a loop that publishes the energydata every hour to the context broker
    for t_sim in (int(t_start),int(t_end),int(t_step)):
        mqttc.publish(topic=Topic_Energy_Building,
                      payload=json.dumps({"demand": demand_00[t_sim],
                                          "t_sim": t_sim}))
        #simulation for next loop
        time.sleep(1)

    #close the mqtt listening thread
    mqttc.loop_stop()

    #disconnect the mqtt device
    mqttc.disconnect()

    #plot results
    fig, ax = plt.subplots()
    t_simulation = [item["t_sim"] for item in building_energy_data]
    demand=[item["demand"] for item in building_energy_data]
    ax.plot(t_simulation, demand)
    ax.set_xlabel('time in hour')
    ax.set_ylabel('demand for next hour')