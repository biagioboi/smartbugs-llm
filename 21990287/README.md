# Artifact Description
Vulnerable Verified Smart Contracts is a dataset of real vulnerable Ethereum smart contracts. Based on the manually labeled [Benchmark dataset of Solidity smart contracts](https://doi.org/10.5281/zenodo.7744053). A total of 609 vulnerable contracts are provided, containing 1,117 vulnerabilities.

The dataset is split into: "train", "validation" and "test". Each file is in the [Apache Parquet](https://parquet.apache.org/) data file format.

# Environment Setup
The [Pandas](https://pandas.pydata.org) library for Python is required to load the dataset. Both Unix-based and Windows systems are supported.

# Getting Started
The following code snippet demonstrates how to load the dataset into a Pandas DataFrame.

``` python
import pandas as pd
df = pd.read_parquet("path/to/data")
```

# License
All Smart Contracts in the dataset are subject to their own original licenses.