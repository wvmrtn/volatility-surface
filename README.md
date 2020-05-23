# volatility-surface
Web-based application to compute the implied volatility and visualize the volatility surface. 

## Installation
`git clone` the master repository https://github.com/wvmrtn/volatility-surface.git to retrieve a copy on your local machine.

Create a virtual environment (with e.g. virtualenv, conda). 

`cd` to cloned repository and run the command `pip install .` To install as developper, run the command `pip install -e .`.

### Requirements
dash>=1.0.0

pandas>=1.0.0

scipy>=1.0.0

jupyter-dash

requests>=2.0.0

## Running
In the cloned directory, and after creating a virtual environment and installing, run `python main_app.py`. After waiting a moment, a webpage will open in a web browser with the interface ready to be used.
