# Smartphone sensor data

## About this app

This app queries a SQL database every second.


## How to run this app

(The following instructions apply to Posix/bash. Windows users should check
[here](https://docs.python.org/3/library/venv.html).)

First, clone this repository and open a terminal inside the root folder.

Create and activate a new virtual environment (recommended) by running
the following:

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```
Run the app:

```bash
python main.py
```
Open a browser at http://127.0.0.1:8050


## Resources

- To learn more about Dash, check out our [documentation](https://plot.ly/dash).
