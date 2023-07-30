@Code Repo For UCL BA Student Number XGZZ9 Final Thesis

## Aluminium Pricing and Purchase Decisioning Engine

### Installation Quick-Start

```
# in project root folder
pip install -r requirements.txt
```

### Running the Code
The project had been set-up in a way that CLI tool is provided to access different modules, an example is shown below
```
# syntax: python -m src.run {orchestrator name}
python -m src.run preprocess
```

The list of available orchestrators are:
- scrape: scrape the metals futures prices
- preprocess: read in raw data (in csv format) and conduct data pre-processing/cleaning