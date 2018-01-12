# 2017Fall-IntelligentSecurityGuard
## Quick link
* [Webpage](https://ntuee-eslab.github.io/2017Fall-IntelligentSecurityGuard/index.html)
* [Requirements](https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard#requierments)
* [Installation & Usage](https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard#installation--usage)
* [Build Instructions](https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard#build-instructions)
* [Recognize Usage](https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard#recognize-usage)
* [C Library in Python](https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard#c-library-in-python)

## Requirements
### Software
- python 3
- pexpect(python module)
- darknet-nnpack(already built)

### Hardware
- Rpi3 model B
- Arduino uno
- Rpi自走車套件
- 行動電源(5V 2.1A)
- 9V電池
- 高亮白LED
- Rpi camera module
- 人體紅外線感應器
- 單路relay
- 蜂鳴器

## Installation & Usage
Log in to Raspberry Pi using SSH.
```
git clone https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard.git
cd 2017Fall-IntelligentSecurityGuard
python main.py
```
For the first time, use `navigation` to set up the route. Press `start` then the car will move along the route.
## Build Instructions
If there is any problem, you can try to build the darknet yourself. But do check the directory path of `dartnet-nnpack` and that in `recognize.py`. Or the recognition might crash.

Log in to Raspberry Pi using SSH.<br/>
Install [PeachPy](https://github.com/Maratyszcza/PeachPy) and [confu](https://github.com/Maratyszcza/confu)
```
sudo apt-get install python-pip
sudo pip install --upgrade git+https://github.com/Maratyszcza/PeachPy
sudo pip install --upgrade git+https://github.com/Maratyszcza/confu
```
Install [Ninja](https://ninja-build.org/)
```
cd 2017Fall-IntelligentSecurityGuard
mkdir alter
cd alter
git clone https://github.com/ninja-build/ninja.git
cd ninja
git checkout release
./configure.py --bootstrap
export NINJA_PATH=$PWD
```
Install clang
```
sudo apt-get install clang
```
Install modified [NNPACK](https://github.com/shizukachan/NNPACK)
```
git clone https://github.com/shizukachan/NNPACK
cd NNPACK
confu setup
```
If you are using Rpi3, use the following commands. Replace `NNPACK/src/init.c` with `replace/init.c`

Otherwise, modify `NNPACK/src/init.c` to fit your CPU arch.

Also, add `-fPIC` to `cflags` and `cxxflags` in `NNPACK/build.ninja`.
```
$NINJA_PATH/ninja
bin/convolution-inference-smoketest
sudo cp -a lib/* /usr/lib/
sudo cp include/nnpack.h /usr/include/
sudo cp deps/pthreadpool/include/pthreadpool.h /usr/include/
cd ../
```
Install [qasm2](https://github.com/Terminus-IMRC/qpu-assembler2)
```
sudo apt-get install flex
git clone https://github.com/Terminus-IMRC/qpu-assembler2
cd qpu-assembler2
make
sudo make install
cd ../
```
Install [qbin2hex](https://github.com/Terminus-IMRC/qpu-bin-to-hex)
```
git clone https://github.com/Terminus-IMRC/qpu-bin-to-hex
cd qpu-bin-to-hex
make
sudo make install
cd ../
```
Install [qmkl](https://github.com/Idein/qmkl)
```
sudo apt-get install cmake
git clone https://github.com/Idein/qmkl.git
cd qmkl
cmake .
make
sudo make install
cd ../
```
Install [darknet-nnpack](https://github.com/shizukachan/darknet-nnpack)
```
git clone https://github.com/shizukachan/darknet-nnpack.git
cd darknet-nnpack
```
Replace `darknet-nnpack/Makefile` with `replace/Makefile` then `make` it.

(Note that this `Makefile` is only for Rpi3. If you want to run on other platform, modify `-mcpu=cortex-a53` part in the `Makefile` to fit the CPU arch you are using.)

Ref: [shizukachan/darknet-nnpack](https://github.com/shizukachan/darknet-nnpack)

## Recognize Usage
If you just want to test the human detection, use the following commands.
```python
# initialize
from recognize import *
p = init()
# take a photo
shot()
# recognize(return true if detected)
recognize(p)
# move the prediction image
move()
```
The final image will be `data/predictions.png`.

## C Library in Python
The origin version of [darknet](https://github.com/pjreddie/darknet) provides `darknet.py` for python user. Since now we build it with `NNPACK`, the script is no longer usable. After some studies, I make a new version. You can put `replace/darknet.py` under your `darknet-nnpack` directory and simply run it.
