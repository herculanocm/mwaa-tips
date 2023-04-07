# AWS MWAA - Airflow Tips
Methods Utils

## Ubuntu nested
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
sudo apt install python3.7-distutils
```


## Create VirtualEnv
```
virtualenv --python="/usr/bin/python3.7" "./venv"
```

## Enable virtual
```
source venv/bin/activate
```

## Install deps
```
pip install -r requirements.txt
```

## Generate Wheel
```
python setup.py bdist_wheel
```

## Tests

```
pytest -v -s
```