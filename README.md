# Estimating undisclosed data in QCEW
This code estimates undisclosed values for employment in the BLS' Quarterly Census of Employment and Wages (QCEW).

## Installation
If you are a Mac user, run the following on the command line:
```
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If you are a Windows user, run:
```
python -m venv env
env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the code
Once all the dependencies are installed in the virtual environment, run:
```
python -m main
```
which will run estimations in a loop of all 51 states across the variable `years` defined in config.py. The list of states is ordered by the population size in an accending order.

## States schedule
Different states have different number of counties, and therefore different memory requirements during the estimation process. Based on the first round of estimation performed in January 2023:

* small-size states (56000 - 53000) need up to 64 GiB of memory
* medium-size states (51000 - 06000 excluding 48000) need up to 128 GiB of memory
* mammut-size states (48000) need up to 256 GiB of memory

## Data 
The data used in the estimation are Q4 QCEW data obtained by consuming BLS' API. Given a state code, the function `load_state_data` loads the data into a Python dictionary that has a following tree-like structure:

```
{"year": 
    {
        "state_code": ..., 
        {"ind": "...", 
         "est": ..., 
         "emp": ..., 
         "wages": ..., 
         "children": [
                {"ind": "...", 
                 "est": ..., 
                 "emp": ..., 
                 "wages": ..., 
                 "children": [...]
                } ...
            ]
        }
    }, ...
}
```
For each year, the function first extracts all the county (`area_fips`) codes for a state, and then fills the dictionary with all the county data. Each year starts with the state data tree and ends with the last county tree in an accending order.

## Defining constraints
Once the data is loaded, the code extracts all the constraints based on the parent-child relationships of the nodes in the trees. The code first loops through the county codes to obtain all the county-level constraints, and then loops through the industries in the state-tree to obtain the state-level constraints.

## Estimation
Finally, the code vectorizes the constraints by placing them in a convenient matrix form and solves the following linear programming problem:

```
min c*x
subject to:
A*x + s = b
x >=0
```

where x is a vector of unknown employment levels, c is a vector of ones, and the A matrix and the b vector reflect all the constraints, and s is a vector of slack variables.

The solver used in the estimation is ECOS solver from the library `cvxpy`.

## Results
For each state in the loop, the undisclosed values are saved in the appropriate nodes with the `_lp` suffix (for example `emp_lp`) and the dictionary is saved as a JSON file in the project folder.

## Extensions and refinements
The code can be easily adapted to estimate undisclosed total wages. The estimation might need more memory, though, given that wage numbers are significantly higher in absolute terms relative to employment numbers. Moreover, the state-level estimates do not add up to the national-level data. To achieve that, we would need to collect all the county-, state- and national-level constraints and solve a linear programming problem on the national level. Such computational costs would be significantly higher than the highest memory configuration used on the state level. Luckily, AWS has supercomputers available for such a costly task.

Finally, one could add a time-series aspect to refine the estimates. Employment in an industry would follow an autoregressive process and depend on its past realizations. In such a setting, one could use a version of Kalman filter to estimate the undisclosed values. Nevertheless, further analysis of the current results should determine whether adding the time-series aspect to the estimation brings enough benefits relative to additional costs in terms of estimation.