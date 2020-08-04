from signalrcore.hub_connection_builder import HubConnectionBuilder
import board
import busio
import adafruit_pca9685
import time
import simplejson as json

server_url = 'ws://192.168.1.49/api/ws/machine'

i2c =busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685

mapping = [9, 8, 7, 5, 4, 2, 14, 13]

pca.frequency = 60

hub_connection = HubConnectionBuilder()\
    .with_url(server_url)\
    .with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()


def turn_machine(json_data):
    json_data = json.dumps(json_data)
    data = json.loads(json_data)
    dispenser = data[0]['dispenser']
    count = data[0]['count']
    print('Turning dispenser ' + str(dispenser) + " for " + str(count) + ' times!')

    for x in range (0, count):
        channel = pca.channel[mapping[dispenser-1]]
        channel.duty_cycle = 0xFFFF
        time.sleep(0.5)
        channel.duty_cycle = 0x00
        time.sleep(3)


hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))
hub_connection.on('turndispenser', turn_machine)

hub_connection.start()
message= None
while True:
    time.sleep(0.5)
    #do nothing

hub_connection.stop();

