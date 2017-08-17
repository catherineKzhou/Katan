import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class KatanServer(PodSixNet.Server.Server):
    channelCLass = ClientChannel
    def Connected(self, channel, addr):
        print 'new connection: ', channel

katanServe = KatanServer()
while True:
    katanServe.Pump()
    sleep(0.01)
