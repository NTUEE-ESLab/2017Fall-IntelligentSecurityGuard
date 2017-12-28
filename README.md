# 2017Fall-IntelligentSecurityGuard
## Requierments
- python 3
- pexpect
- darknet-nnpack
## Installation & Usage
```
git clone https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard.git
cd 2017Fall-IntelligentSecurityGuard
python main.py
```
For the first time, use `navigation` to set up the route. Press `start` then the car will move along the route.
## Build Instructions
If there is any problem, you can try to build the darknet yourself.
Install pexpect
```
sudo pip install pexpect
```
Log in to Raspberry Pi using SSH.<br/>
Install [PeachPy](https://github.com/Maratyszcza/PeachPy) and [confu](https://github.com/Maratyszcza/confu)
```
sudo apt-get install python-pip
sudo pip install --upgrade git+https://github.com/Maratyszcza/PeachPy
sudo pip install --upgrade git+https://github.com/Maratyszcza/confu
```
Install [Ninja](https://ninja-build.org/)
```
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
If you are using Rpi3, use the following commands.
```
cp 
```
Otherwise, 
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
make
```
##Recognize Usage
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
