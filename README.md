# cattracker

This program is configured to track cat litter behaviour using a Raspberry Pi and a external device such as a usb gaming controller. The configuration is set up for a Retrolink SNES controller.

## Install

First install dependencies:
```
pip install -r requirements.txt
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
sudo systemctl enable myscript.service
```
