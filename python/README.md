# Azure Mqtt Broker Sample Python Instructions

## Make sure you have python 3.6+ installed

Make sure you have python 3.6, or higher installed. Run `python3 --version` to verify. If it's not installed, run the following command to install it:
```bash
sudo apt install python3 python3-pip
```
## Update PIP

For extra safety, upgrade the Python package manager (PIP) by running the following command.

```
python3 -m pip install virtualenv
```

* In case of `/usr/bin/python3: No module named pip` error, install as follows
  ```
  sudo apt-get update
  sudo apt install python3-pip
  ```
  
* You can ignore the below warning.  When you create your virtual environment, it will enable the correct version of pip.
```
The scripts pip.exe, pip3.9.exe and pip3.exe are installed in 'C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

## Create your virtual environment

A virtual environment gives us a safe space to install Python libraries without changing your "global" python configuration.

1. Create a virtual environment through the following command. The last directory segment defines the name of the environment. Let's use `env/mqtt-broker`:

  ```
  python3 -m venv ~/env/mqtt-broker
  ```

  If you encountered the following error: `The virtual environment was not created successfully because ensurepip is not available.`, install the python3-venv package using the following command:

  ```
  sudo apt install python3.8-venv
  ```

2. Activate your virtual environment.  You need to run this everytime you use the provided python scripts in each scenario. 

  ```
  source ~/env/mqtt-broker/bin/activate
  ```

  After you do this, your prompt will change to include the `mqtt-broker` name.

  ```
 user@contoso:~$ source ~/env/mqtt-broker/bin/activate
  (mqtt-broker) user@contoso:~$
  ```

4. Now you are using the python and pip executables from inside the `env/mqtt-broker` directory, and all libraries that you install will also be stored in this directory.

  Also, now that we're in the virtual environment, you can use `python3` or `python` commands since they both point to the same thing.

## Install helper modules

The following instructions will help you install the modules that you will need to run tests.

You need to change the directory to run the following commands from this python folder of your cloned repo. Change the following command to point to the correct path.

```
cd ./MQTTBrokerPrivatePreview/python

```
To install the modules that you will need to run these tests, run pip to install the code in this directory in 'editable' mode.

```
pip install -e .
```

If you see `ERROR: Failed building wheel for paho.mqtt`, run `pip install wheel`, then run `pip install -e .` again. 

This should install Paho as well as a few other libraries that we need.  You can verify this with `pip list`:
```
(mqtt-broker) user@contoso:~/MQTTBrokerPrivatePreview/python$ pip list
Package                  Version Location
------------------------ ------- --------------------------------------------
MQTTBrokerPreviewSamples 0.0.0   /home/user/MQTTBrokerPrivatePreview/python
paho-mqtt                1.6.1
pip                      20.0.2
pkg-resources            0.0.0
setuptools               44.0.0
six                      1.16.0
wheel                    0.37.1
```

## Verifying your install

To verify that you have the libraries successfully installed, you can:

1. Type `cd ..` to move into the root of the repo.
2. Type `python` to launch the python interpreter
3. Inside python, type `import paho_client`.
4. If no error is displayed, then the library was successfully installed.
5. type `exit()` to exit the Python interpreter.

For example:
```
(mqtt-broker) user@contoso:~/projects/broker/MQTTBrokerPrivatePreview/python$ cd ..
(mqtt-broker) user@contoso:~/projects/broker/MQTTBrokerPrivatePreview$ python
Python 3.10.7 (default, Jul  7 2020, 14:58:11)
[GCC 7.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import paho_client
>>> dir(paho_client)
['Any', 'ConnectionStatus', 'IncomingAckList', 'IncomingMessageList', 'List', 'PahoClient', 'SymmetricKeyAuth', 'Tuple', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'logger', 'logging', 'mqtt']
>>> exit()

```
