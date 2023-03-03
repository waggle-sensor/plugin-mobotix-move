# Mobotix Preset Mover Plugin

This plugin is designed to move a Mobotix camera to a specified preset location. 
The plugin takes the IP or URL of the camera, the user ID, and the password as command-line arguments. 
It also takes the preset location ID as an optional argument.
The 32 preset locations are available for use by calling preset 1-32 or scan with 1-32 by calling 99. 
In scanning mode, plugin currently scans all the points 1-32, 
but it should be able to perform a loop-scan only over a user given set of points.


## Usage

To execute the plugin use the following (from within the built `Docker` container):

`python3 /app/app.py --ip <ip_address> -i <interval> -l <loops> -u <user_id> -p <password> --pt <preset_location>`


    `<ip_address>`: The IP address or URL of the camera. This argument is required.
    `<interval>`: Interval between the move in seconds (optional, defaults to 120 Seconds).
    `<loops>`: Scanning loops to perform (optional, defaults to -1=infinite).
    `<user_id>`: The user ID of the camera. Defaults to `admin`.
    `<password>`: The password of the camera. This argument is required.
    `<preset_location>`: The preset location ID (currently between 1 and 32) (optional, defaults to 99=scanning mode will perform a loop-scan over all preset positions). 


Example:

```
python3 /app/app.py --ip 10.11.12.13 -u admin -p password --pt 5
```

This moves camera with ip 10.11.12.13 to preset point 5.

### Development

The `Docker` container can be built by executing the following:

```
./build.sh
```

Note: The camera always send the OK signal even if the location string is not properly sent.
