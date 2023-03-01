# Mobotix Preset Mover Plugin

This plugin is designed to move a Mobotix camera to a specified preset location. The plugin takes the IP or URL of the camera, the user ID, and the password as command-line arguments. It also takes the preset location ID as an optional argument.
The 32 preset locations are available for use by calling preset 1-32.

   

## Usage

To execute the plugin use the following (from within the built `Docker` container):

```
python3 /app/app.py --ip <ip_address> -u <user_id> -p <password> --pt <preset_location>
```
    `<ip_address>`: The IP address or URL of the camera.
    `<user_id>`: The user ID of the camera.
    `<password>`: The password of the camera.
    `<preset_location>`: The preset location ID of the camera (optional, defaults to 1).


Example:

```
python3 /app/app.py --ip 10.11.12.13 -u admin -p password --pt 5
```

### Development

The `Docker` container can be built by executing the following:

```
./build.sh
```
