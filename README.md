# 2017Fall-IntelligentSecurityGuard
## Requierments
- python 3
- pexpect
- darknet-nnpack
## Installation
```
git clone https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard.git
```
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
cp 
'''
