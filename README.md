Copyright (c) 2023 by UCL BA Student XGGZ9. All rights reserved.

## Aluminium Pricing and Purchase Decisioning Engine

Code Repo For UCL BA Student Number XGGZ9 Final Thesis

### Section 1 - Overview

The thesis evolves around building an engine consisting of the following two sections:

1. Aluminium Pricing (What this repo mainly contains)
2. Purchase Decisioning (This is included in notebooks/Procurment_Decision.ipynb where comparison betwen raw material cost with/without the purchase decision guided by aluminium pricing engine)

The main aim is to predict Aluminium pricing and utilise the decision engine to save raw material costs for a Aluminum door factory based in China. Refer to the submitted paper for more detailed discussion.

### Section 2 - Installation Quick-Start

> in project root folder

```
pip install -r requirements.txt
```

### Section 3 - Getting the raw data
The raw data is provided as a zip file with passcode specified in the thesis in the following folder (as the repo will be open to public and to avoid the data being used outside of the purpose of this thesis):

> data/raw/raw_data.zip



### Section 4 - Running the Code
The project had been set-up in a way that CLI tool is provided to access different modules, an example is shown below

> syntax: python -m src.run {orchestrator name}
>
> make sure required raw data is already in place

```
python -m src.run preprocess
```

The list of available orchestrators are:
- `scrape`: scrape the metals futures prices
- `preprocess`: read in raw data (in csv format) and conduct data pre-processing/cleaning
- `analysis`: conduct statistical analysis and produce EDA plots
- `model`: build all models discussed in the thesis, including linear ones and LSTM. make sure `preprocess` is run before running this step.

### Section 5 - Results:

Results are stored automatically within the project folders:
- data folder consists of all csv outputs from the pipeline run
- each run will have its own run id where one would be able to locate the log files and all plots generated
