# Specifications of RaspberryPi 4 model B :strawberry:
<li>Processor: Broadcom BCM2711, quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz<br>
<li>Memory: 8GB LPDDR4 with on-die ECC<br>
<li>OS: Debian 11.5(Bullseye)<br>
<li>Python version: 3.9.2<br>


# Installation of pytorch :pie::flashlight:
The instruction 
```
pip install torch torchvision torchaudio
```
gave me error 
```
Traceback (most recent call last):
  File "/usr/bin/pip", line 33, in <module>
    sys.exit(load_entry_point('pip==20.3.4', 'console_scripts', 'pip')())
  File "/usr/bin/pip", line 25, in importlib_load_entry_point
    return next(matches).load()
  File "/usr/lib/python3.9/importlib/metadata.py", line 77, in load
    module = import_module(match.group('module'))
  File "/usr/lib/python3.9/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1030, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
  File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 680, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 790, in exec_module
  File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
  File "/usr/lib/python3/dist-packages/pip/_internal/cli/main.py", line 10, in <module>
    from pip._internal.cli.autocompletion import autocomplete
  File "/usr/lib/python3/dist-packages/pip/_internal/cli/autocompletion.py", line 9, in <module>
    from pip._internal.cli.main_parser import create_main_parser
  File "/usr/lib/python3/dist-packages/pip/_internal/cli/main_parser.py", line 7, in <module>
    from pip._internal.cli import cmdoptions
  File "/usr/lib/python3/dist-packages/pip/_internal/cli/cmdoptions.py", line 23, in <module>
    from pip._vendor.packaging.utils import canonicalize_name
  File "/usr/lib/python3/dist-packages/pip/_vendor/__init__.py", line 94, in <module>
    vendored("requests.packages.urllib3.contrib.pyopenssl")
  File "/usr/lib/python3/dist-packages/pip/_vendor/__init__.py", line 36, in vendored
    __import__(modulename, globals(), locals(), level=0)
  File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
  File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 664, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 627, in _load_backward_compatible
  File "<frozen zipimport>", line 259, in load_module
  File "/usr/share/python-wheels/urllib3-1.26.5-py2.py3-none-any.whl/urllib3/contrib/pyopenssl.py", line 50, in <module>
  File "/usr/lib/python3/dist-packages/OpenSSL/__init__.py", line 8, in <module>
    from OpenSSL import crypto, SSL
  File "/usr/lib/python3/dist-packages/OpenSSL/crypto.py", line 1556, in <module>
    class X509StoreFlags(object):
  File "/usr/lib/python3/dist-packages/OpenSSL/crypto.py", line 1577, in X509StoreFlags
    CB_ISSUER_CHECK = _lib.X509_V_FLAG_CB_ISSUER_CHECK
AttributeError: module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'
```
> Hence for installation of pytorch, different approach had to be implemented. This tutorial was referred from [Q-engineering](https://qengineering.eu/install-pytorch-on-raspberry-pi-4.html).
```
# get a fresh start
$ sudo apt-get update
$ sudo apt-get upgrade

# install the dependencies (if not already onboard)
$ sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev

# above 58.3.0 you get version issues
$ sudo -H pip3 install setuptools==58.3.0
$ sudo -H pip3 install Cython

# install gdown to download from Google drive
$ sudo -H pip3 install gdown
```
```
Bullseye OS
# download the wheel
$ gdown https://drive.google.com/uc?id=1A2Lc-7y3-ATauRa4FntiYGH90b1GjAzx

# install PyTorch 1.12.0
$ sudo -H pip3 install torch-1.12.0a0+git67ece03-cp39-cp39-linux_aarch64.whl

# clean up
$ rm torch-1.12.0a0+git67ece03-cp39-cp39-linux_aarch64.whl
```

## Torchvision :flashlight::eyes:
```
Used with PyTorch 1.12.0
# the dependencies
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev

# install gdown to download from Google drive, if not done yet
$ sudo -H pip3 install gdown
```
```
Bullseye OS
# download TorchVision 0.12.0
$ gdown https://drive.google.com/uc?id=1VBegXwqS-A4MVNlHt8Y_0cu697NrAtf7

# install TorchVision 0.13.0
$ sudo -H pip3 install torchvision-0.13.0a0+da3794e-cp39-cp39-linux_aarch64.whl

# clean up
$ rm torchvision-0.13.0a0+da3794e-cp39-cp39-linux_aarch64.whl
```
After the required library installation, you are good to go for inplementation
