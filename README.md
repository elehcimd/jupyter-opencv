# Jupyter-OpenCV Docker image

This Docker image provides a cross-platform environment that includes Jupyter Notebooks, Python3 and OpenCV 3.4 to experiment with computer-vision. Tested on Windows, MacOS, and Linux. Friends in environmental engineering use it on Windows as alternative to MATLAB.

## Image details

Based on **Ubuntu 16.4** and includes:

* **Python3.5** as default Python interpreter
* **OpenCV 3.4** with extra modules, highgui and Python support
* **Jupyter notebook** web server
* **X Window libraries** compatible with MacOS (XQuartz), Windows (Xming) and Linux (X.Org) 
* Includes demo of Jupyter notebook with embedded web video player and OpenCV processing
* Includes Demo of container-host X Window interaction with `xeyes`

## Quick start

* Install Docker: https://docs.docker.com/install/
* Start container: `docker run -p 127.0.0.1:8889:8888 micheda/jupyter-opencv:3.4.0`
* Open Jupyter notebook demo at http://127.0.0.1:8889/notebooks/notebooks/demo.ipynb

Any modification will be lost at container termination. Next section provides instructions to persist changes.

## Persisting your notebooks

To persist modifications to notebooks, you must *mount* a directory on the host inside the container using the `-v` option, documented at https://docs.docker.com/engine/reference/run/#volume-shared-filesystems . In the following example, the host directory  `/your/notebooks` is mounted on the container directory `/playground/shared`:

```
docker run -p 127.0.0.1:8889:8888 -v/your/notebooks:/playground/shared micheda/jupyter-opencv:3.4.0
```

Modifications inside `/playground/shared` are persisted in the corresponding host directory, `/your/notebooks`.
You can mount the host directory at mountpoint `/playground` to hide the examples.
The root Jupyter directory can be accessed at http://spark-driver:8888/tree.

## Demo of X Window application

This demo shows you how to use the X Window System Server running on the host
to visualize and interact with visual applications running in the container.
E.g., you can interact with `xeyes`, visualize a video with `ffmpeg` and use the OpenCV highgui module.


### X Window demo For MacOS users:

Follow these steps on the host:

1. Install XQuartz (MacOS): https://www.xquartz.org/
2. Launch XQuartz. Under the XQuartz menu, select Preferences
3. Go to the security tab and ensure `Allow connections from network clients` is checked
4. Restart XQartz
5. Run `xhost +` to allow connections from any host to the macOS host
6. Open a web shell in the container: http://127.0.0.1:8889/terminals/1 and execute the following commands:
   1. Run `export DISPLAY=docker.for.mac.host.internal:0`
   2. Run `xeyes` 


### X Window demo For Windows users:

Follow these steps on the host:

1. Install Xming (Windows): http://www.straightrunning.com/XmingNotes/
2. Launch Xming: `Xming -multiwindow -clipboard`
3. Run `xhost +`to allow connections from any host to the Windows host
4. Open a web shell in the container: http://127.0.0.1:8889/terminals/1 and execute the following commands:
   1. Run `export DISPLAY=docker.for.win.localhost:0`
   2. Run `xeyes` 

Recommendation: use the Windows PowerShell to execute commands.


### X Window demo For Linux users:

Follow these steps on the host:

1. Install Xorg following the instructions for your distribution. Most likely it's alraedy installed if you are accessing this document from its web browser.
2. Run `xhost +` to allow connections from any host to the Linux host
3. Open a web shell in the container: http://127.0.0.1:8889/terminals/1 and execute the following commands:
   1. Run `export DISPLAY=docker.for.linux.localhost:0`
   2. Run `xeyes` 

## Credits

* OpenCV integration based on https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/ - Thank You, Adrian!
 
## Docker image development

Builds, tests and releases are managed with `Fabric`.
Install Docker and Fabric in your host system. To install Fabric:

```
pip install Fabric3
```


### Building and publishing a new release

Update the build, and start:

```
fab docker_build
fab docker_start
```

Verify that the tests are all green:

```
fab test
```

Generate the demo Jupyter notebook from the Python notebook source:

```
fab docker_exec:'pynb notebooks_src/demo.py \
    --export-ipynb notebooks/demo.ipynb \
    --no-exec \
    --disable-footer'
```

Authenticate your user, tag and push the image:

```
docker login --username micheda
docker tag jupyter-opencv micheda/jupyter-opencv:3.4.0
docker push micheda/jupyter-opencv:3.4.0
```


### Docker container

To build the Docker image:

```
fab docker_build
```

To force a complete rebuild of the Docker image without using the cache:

```
fab docker_build:--no-cache
```

To start the daemonized Docker container:

```
fab docker_start
```

The repository directory on the host is mounted in the container at `/playground`.
Any changes on the host are immediately visible inside the container.
To run the container without external mount points:

```
fab docker_start:false
```

To stop the Docker container:

```
fab docker_stop
``` 

To open a shell in the Docker container:

```
fab docker_sh
```


### Running the tests

Before running the tests, start the container.

To run the py.test tests:

```
fab test
```

To run a single test:

```
fab test:tests/test_pep8.py::test_pep8
```

To run tests printing output and stopping at first error:

```
fab test_sx
```

To run the pep8 test:

```
fab test_pep8
```

To fix some common pep8 errors in the code:

```
fab fix_pep8
```


## Contributing

1. Fork it
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Create a new Pull Request
