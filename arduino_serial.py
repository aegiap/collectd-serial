import collectd 
import serial
from os import sep

class ArduinoSerial:

    def __init__(self):
        self.plugin_name = 'ArduinoSerial'
        self.speed = 9600
        self.device = '/dev/ttyACM1'
        self.ser = None
        self.debug = False
        self.timeout = 1
        self.plugin_instance = None 

        self.set_plugin()


    def open(self):
        try:
            if self.debug:
                collectd.warning('ArduinoSerial: ' +
                    'trying to connect to %s with speed %s' %
                    (self.device, self.speed))
            self.ser = serial.Serial(self.device, self.speed, timeout=self.timeout)
        except:
            collectd.warning('ArduinoSerial: ' + 
                'error on the serial device %s with the speed %d' %
                (self.device, self.speed))

        if not self.ser.isOpen():
            self.ser.open()

        self.ser.nonblocking()
        collectd.info('ArduinoSerial: serial connection is ok')


    def set_plugin(self):
        path_elements = self.device.split(sep)
        self.plugin_instance = path_elements[-1]


    def submit(self, datatype, instance, value):
        """
        Push the data back to collectd.
        """
        cvalue = collectd.Values(plugin='arduinoserial')
        cvalue.plugin = self.plugin_name
        cvalue.plugin_instance = self.plugin_instance
        cvalue.type = datatype
        cvalue.type_instance = instance
        cvalue.values = [value, ]
        cvalue.dispatch()
 
        if self.debug:
            collectd.warning('ArduinoSerial: data dispatched: %s %.1f' %
                (datatype, value))
 

    def get_value(self):
        """
        Open the serial port, get the value and treat it.
        Then close the serial port.
        """
        humidity = 0.0
        temperature = 0.0

        self.open()

        while 1:
            reading = self.ser.readline().strip().split(' ')

            #if self.debug: 
            #     collectd.warning('ArduinoSerial: ' +
            #         'debug) received line with %d elements' %
            #         len(reading))

            if len(reading) > 7:
                temperature = float(reading[8])
                humidity = float(reading[4])
                self.submit('temperature', 'gauge', temperature)
                self.submit('humidity', 'gauge', humidity)
                break

        if self.ser.isOpen():
            self.ser.close()
    
    def config(self, obj):
        """
        Get the configuration from collectd
        """
        for child in obj.children:
            if child.key == 'Debug':
                self.debug = True
            elif child.key == 'SerialDevice':
                self.device = child.values[0]
                self.set_plugin()
            elif child.key == 'SerialSpeed':
                self.speed = int(child.values[0])

        collectd.info('ArduinoSerial: configuration')


arduino = ArduinoSerial()
collectd.register_config(arduino.config)
collectd.register_read(arduino.get_value)
