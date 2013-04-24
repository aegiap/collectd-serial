collectd-serial
===============

Python plugin to graph data from a serial connection to a arduino into colletcd.

This plugin is still work in progress.

more details
------------

Push the Arduino sketch in arduino/dht11_sketch.ino to your board.

configuration
-------------

This should be added to your collectd configuration :: 

    <LoadPlugin python>
            Globals true
    </LoadPlugin>
    
    <Plugin python>
            ModulePath "/your/path/to/python"
            LogTraces true
            Interactive true
            Import "arduino_serial"
    
            <Module arduino_serial>
                    SerialDevice "/dev/ttyACM0"
                    SerialSpeed 9600
                    Debug true
            </Module>
    </Plugin>
