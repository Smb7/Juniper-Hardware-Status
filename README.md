# Get Juniper Hardware Status

The goal of this project was to decrease the time it takes to remote into each switch, run the commands, and then cipher through the output to see if the alarms are false or true. By creating this repo, I am able to check all switch statuses in a minute, whereas manually doing it takes between 10-15 minutes.

## Table of Contents

- [Prerequisite](#prerequisite)
- [How to Install, Configure, and Run](#how-to-install-configure-and-run)
- [How to Setup an RSA Key](#how-to-setup-an-rsa-key)

## Prerequisite

1. Must have Juniper devices that use Junos CLI.
   
2. Must have SSH enabled on the devices.

3. Must configure RSA keys for remoting into the switches.

## How to Install, Configure, and Run

1. Clone the GitHub repo:
    ```bash
    git clone https://github.com/Smb7/Juniper-Hardware-Status.git
    ```

2. Save and open in VSCode or your preferred IDE.

3. Install the requirements from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

4. Edit the `app.py` file:
    ```python
    switch_names = {
        "<IP address>": "<Switch name>",  # replace with IP address and switch name 
        "<IP address>": "<Switch name>"
    }

    filePath = [
        r"<filepath for RSA key>",  # replace with file path for secret RSA key
        r"<filepath for RSA key>"
    ]
    ```

5. Run `app.py`.

6. Run `data.py`.

7. Done!

## How to Setup an RSA Key
1. On local windows machine create RSA Key
```bash
ssh-keygen -b 2048 -t rsa -C <You
```

2. Add RSA key to the switch
```bash
pscp C:\Users\shaneb\.ssh\name.pub <Username>@ipaddr:/var/tmp
```

3. Start shell in Junos
```bash
start shell
```

4. Find public key in Junos
```bash
cd /var/home/username/.ssh/

ls 

chmod 600 authorized_keys #this is not required only if you have issues
```

5. Add key to User Account in Junos
```bash
set system login user sbrennan authentication load-key-file /var/tmp/NameHere.pub
```
6. Done















