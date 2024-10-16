# Environment Setup

## Conda

First things first you need to install conda if you haven't already. Check [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and install miniconda. Once you have installed conda, create a new environment for this project.


## Rust

For some reason, one of the dependencies for this project has a dependency itself that was requiring me to have a rust compiler in order to install it via pip. So you might need to install Rust, your mileage may vary. [Here's the link](https://www.rust-lang.org/tools/install), and remember to add it to the path.

## Python

This is the easy part, after a quick `conda install python` and a following `pip install --upgrade pip`, run `pip install -r requirements.txt` from within the assets directory, and you should be all good to run the project.

## Running The Project

Once all of the prerequisites are in place, create a file `API_creds.json` and add the BAM URL and your BAM key:

```
{
    "BAM_Key": PUT YOUR BAM KEY HERE,
    "BAM_URL": PUT BAM URL HERE,
}
```


In the future the plan is to support watsonx projects, but while this is still in development BAM is far more practical.

Run the project by running `streamlit run Bank_Exec.py` (newsletter demo) or `streamlit run Articles.py` (sentiment demo).