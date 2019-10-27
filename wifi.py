
#---network.cfg---
#config webinterface 
    #bekannte netzwerke und passw 
    #server wie lange nach boot aktiv lassen
    #ap wenn kein bekanntes netzwerk verfügbar?

from microWebSrv import MicroWebSrv
import network
from machine import Timer
import ujson

t2_counter = 0

class connect :
    # ============================================================================
    # ===( Constants )============================================================
    # ============================================================================
    
    #connect Modes

    _tryST_AP = 0
    _tryST    = 1
    _AP       = 2
    #self._AP

    # ============================================================================
    # ===( Class globals  )=======================================================
    # ============================================================================

    
 
    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================
    @staticmethod
    def find_known_wifi(knownNetworks):
        """search in config for networks and her pass"""

        wlan = network.WLAN(network.STA_IF);
        wlan.active(True)
        wifis = wlan.scan();
        wlan.active(False)

        show_wifi_List = []
        connecable_wifis = []

        for i in wifis:
            show_wifi_List.append(i[0].decode("utf-8"))

        for x in knownNetworks:
            if x["ssid"] in show_wifi_List:
                connecable_wifis.append(x)

        #todo: gehe nach priorität
        if len(connecable_wifis)>0:
            return connecable_wifis[0]
        else:
            return False


    def do_connect(wifi):
        """ set host and connect to a network """
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(dhcp_hostname='Bewaesserung')
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(wifi["ssid"], wifi["pass"])
            while not wlan.isconnected():
                pass
        #wlan.ifconfig(('192.168.178.68', '255.255.255.0', '192.168.178.1', '8.8.8.8'))
        print('network config:', wlan.ifconfig())
        
        return True


    def open_AP(ssid,passw):
    """if no network to connect and the config allow it. open a AP"""

        wlan = network.WLAN(network.AP_IF) # create access-point interface
        wlan.active(True)
        wlan.config(essid=ssid) # set the ESSID of the access point
        #wlan.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=passw) # set the ESSID of the access point
     

    def close_Connection():

        print('close wifi')
        wlan = network.WLAN(network.STA_IF);
        wlan.active(False)




    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, configFile = "network.cfg", mode = 0 ):

        
        self._connectMode   = mode
        self._configFile    = configFile
        self._connectionReady = False

        f = open(self._configFile)

        self.netconfigobj = ujson.loads(f.read())

        f.close()

        self.timer = Timer(-1)
        #self.timerCounter = 
        global t2_counter 
        t2_counter = self.netconfigobj["networkActiveTime"]
        wifi_to_connect = False

        if self._connectMode == self._tryST_AP or self._connectMode == self._tryST:

            wifi_to_connect = connect.find_known_wifi(self.netconfigobj["knownNetworks"])

            if wifi_to_connect != False:

                self._connectionReady = connect.do_connect(wifi_to_connect)
           

        if (self._connectMode == self._tryST_AP or self._connectMode == self._AP) and not self._connectionReady: 

            connect.open_AP(self.netconfigobj["APName"],self.netconfigobj["APPass"])

        if self.netconfigobj["networkActiveTime"]>0:
            self.timer.init(period=60000, mode=Timer.PERIODIC, callback=self._t2_callback_function)



    def _t2_callback_function(self,t):
        global t2_counter
        t2_counter -= 1
        print(self._configFile)
        print('networkshutdown in ')
        print(t2_counter)
        if t2_counter == 0:
        #t2_counter = 45
            t.deinit()
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)

            print('shutdown wifi')
"""
    def _t2_callback_function(t):
        
        globals timer_counter
        timer_counter -= 1
        if timer_counter == 0:
            #self.timer.
            close_Connection()
"""


#--------------------------------------------------------------------

#t2_counter = netconfigobj["networkActiveTime"]  #schaktet nach x min das wlan ab (wenn nicht zurückgesetzt ) 
#t2 = Timer(-1)
#t2.init(period=60000, mode=Timer.PERIODIC, callback=t2_callback_function)









