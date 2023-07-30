## Aluminium Pricing and Purchase Decisioning Engine

Code Repo For UCL BA Student Number XGZZ9 Final Thesis

### Section 1 - Overview

The thesis evolves around building an engine consisting of the following two sections:

1. Aluminium Pricing
2. Purchase Decisioning

The main aim is to predict Aluminium pricing and utilise the decision engine to save raw material costs for a Aluminum door factory based in China. Refer to the submitted paper for more detailed discussion.

### Section 2 - Installation Quick-Start

> in project root folder

```
pip install -r requirements.txt
```


### Section 3 - Running the Code
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
