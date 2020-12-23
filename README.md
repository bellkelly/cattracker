# cattracker

This program is configured to track cat litter behaviour using a Raspberry Pi and a external device such as a usb gaming controller. The configuration is set up for a Retrolink SNES controller.

## Notes

- Make sure python is intalled
- Make sure timezone is correct.

## Install

### Python Dependecies

First install dependencies:
```
pip install -r requirements.txt
```

### Google Sheet API

Get an API key for Google sheets [see docs](https://developers.google.com/maps/documentation/javascript/get-api-key).

Save the credentials file as `credentials.json` in the root directory of this project.

### Boot at startup

Create a log file in the project root:

```
mkdir logs
```

Copy the service file to systemd:

```
sudo cp cattracker.service /etc/systemd/system/cattracker.service
```

Start the service with:

```
sudo systemctl start cattracker.service
```

To enable at startup:

```
sudo systemctl enable cattracker.service
```

## Troubleshooting

### Error: `FileNotFoundError: [Errno 2] No such file or directory: '/dev/input/eventX'`

Either the pi user cannot see the input device or the device has been assigned to a different `eventX`. Run `ls -l /dev/input/` as root to see available input devices and the groups that can see them. Change the `GAMEPAD` variable in `cattracker.py` if necessary
