# Mobotix Preset Mover Plugin

This plugin is designed to move a Mobotix camera to a specified preset location. The plugin takes the IP or URL of the camera, the user ID, and the password as command-line arguments. It also takes the preset location ID as an optional argument.
The 32 preset locations are available for use by calling preset 1-32 or scan with 1-32 by calling 99.


## Usage

To execute the plugin use the following (from within the built `Docker` container):

```
python3 /app/app.py --ip <ip_address> -i <interval> -u <user_id> -p <password> --pt <preset_location>
```
    `<ip_address>`: The IP address or URL of the camera.
    `<user_id>`: The user ID of the camera.
    `<interval>`: Interval between the move in seconds.
    `<password>`: The password of the camera.
    `<preset_location>`: The preset location ID of the camera (optional, defaults to 1).


Example:

```
python3 /app/app.py --ip 10.11.12.13 -u admin -p password --pt 5
```

Running on the Node using `pluginctl`:
```
sudo pluginctl run -n test-move 10.31.81.1:5000/local/plugin-mobotix-move -- --ip 10.31.81.13 -pt 99 -i 120 -u admin -p wagglesage
```

This will move it to all 32 points in a single loop with 120 seconds interval between the move.

This moves camera with ip 10.11.12.13 to preset point 5.

### Development

The `Docker` container can be built by executing the following:

```
./build.sh
```

Note: The camera always send the OK signal even if the location string is not properly sent.
