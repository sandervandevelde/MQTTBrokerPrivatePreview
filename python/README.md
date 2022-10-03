# Azure IoT Hub Broker Sample Python Instructions

## Make sure you have python 3.6+ installed

Make sure you have python 3.6, 3.7, 3.8, or 3.9 installed.   Run `python3 --version` to verify:
```
(Python-3.6.10) bertk@bertk-hp:~/temp/broker$ python3 --version
Python 3.6.10
```

On Linux, you can install python3 with `sudo apt install python3 python3-pip`

## Update PIP

For extra safety, upgrade the Python package manager (PIP) by running the following command.

```
python3 -m pip install virtualenv
```

* In case of `/usr/bin/python3: No module named pip` error, install as follows
  ```
  sudo apt install python3-pip
  ```
  
* You can ignore the below warning.  When you create your virtual environment, it will enable the correct version of pip.
```
The scripts pip.exe, pip3.9.exe and pip3.exe are installed in 'C:\Users\bertk\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

## Set up your virtual environment

Next, we set up a virtual environment.  This gives us a safe space to install Python libraries without changing your "global" python configuration.

1. Install the `virtualenv` library

  ```
  python3 -m pip install virtualenv
  ```

2. Create your virtual environment in some directory.  This can go anywhere. The last directory segment defines the name of the environment. Let's use `env/iothub-broker`:

  ```
  python3 -m venv env/iothub-broker
  ```

  In case of `The virtual environment was not created successfully because ensurepip is not available. On Debian/Ubuntu systems, you need to install the python3-venv package using the following command.` error, install virtual environment as follows.

  ```
  sudo apt install python3.8-venv
  ```

3. Activate your virtual environment.  You need to do this any time you want to work with this code.

  In Linux:
  ```
  source env/iothub-broker/bin/activate
  ```

  In Windows command prompt:
  ```
  env\iothub-broker\Scripts\activate.bat
  ```

  In powershell:
  ```
  .\env\iothub-broker\Scripts\Activate.ps1
  ```

  After you do this, your prompt will change to include the `iothub-broker` name.

  ```
  bertk@bertk-hp:~$ source ~/env/iothub-broker/bin/activate
  (iothub-broker) bertk@bertk-hp:~$
  ```

4. Now you are using the python and pip executables from inside the `env/iothub-broker` directory, and all libraries that you install will also be stored in this directory.

  Also, now that we're in the virtual environment, you can use `python3` or `python` commands since they both point to the same thing.

## Install helper modules

To install the modules that you will need to run these tests, run pip to install the code in this directory in 'editable' mode.

```
pip install -e .
```

If you see `ERROR: Failed building wheel for paho.mqtt`, run `pip install wheel`, then run `pip install -e .` again. 

This should install Paho as well as a few other libraries that we need.  You can verify this with `pip list`:
```
(iothub-broker) bertk@bertk-hp:~/projects/broker/IoTHubMQTTBrokerPreviewSamples/python$ pip list
Package                        Version Location
------------------------------ ------- -----------------------------------------------------------------
IoTHubMQTTBrokerPreviewSamples 0.0.0   /home/bertk/projects/broker/IoTHubMQTTBrokerPreviewSamples/python
paho-mqtt                      1.5.1
pip                            21.2.4
setuptools                     56.1.0
six                            1.16.0
wheel                          0.36.2
(iothub-broker) bertk@bertk-hp:~/projects/broker/IoTHubMQTTBrokerPreviewSamples/python$
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
(iothub-broker) bertk@bertk-hp:~/projects/broker/IoTHubMQTTBrokerPreviewSamples/python$ cd ..
(iothub-broker) bertk@bertk-hp:~/projects/broker/IoTHubMQTTBrokerPreviewSamples$ python
Python 3.6.10 (default, Jul  7 2020, 14:58:11)
[GCC 7.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import paho_client
>>> dir(paho_client)
['Any', 'ConnectionStatus', 'IncomingAckList', 'IncomingMessageList', 'List', 'PahoClient', 'SymmetricKeyAuth', 'Tuple', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'logger', 'logging', 'mqtt']
>>> exit()

```
