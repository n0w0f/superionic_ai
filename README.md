superionic_ai
==============================




A heirarchical screening workflow to discover superionic conductors


## Local Installation

The following steps assume that you use MacOS or some Linux flavor. If you use Windows, we recommend that you first install the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10).


We recommend that you create a virtual conda environment on your computer in which you install the dependencies for this exercise. To do so head over to [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and follow the installation instructions there.

Then, use

```bash
conda env create -f environment.yml -n superionic_ai
```

You can activate this environment using

```bash
conda activate superionic_ai
```


Create a new folder and clone this repository (you need `git` for this, if you get a `missing command` error for `git` you can install it with `sudo apt-get install git`)

```bash
git clone https://github.com/n0w0f/superionic_ai.git
cd superionic_ai
pip install -e .
```


## 💪 Getting Started

```bash
cd src
python3 main.py
```

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`  #TODO
    ├── README.md          <- The top-level README for developers using this project.
    |
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details  #TODO
    │
    ├── models             <- Trained and serialized model checkpoints will be loaded while running src 
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.  #TODO
    │
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported   #TODO
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data            <- all data prepared or developed using the app will reside here
    |   |   |──          
    │   │   └── start_mat.yaml  
    │   │
    │   ├── data_prep                     <- Scripts to turn raw data into features , query structures, build structures , anything related to data !!
    |   |   |──  mp_query.py              <- anything relater to materials project api, query
    |   |   |──  structure_builder.py     <- anythin related to playing with strucututres
    │   │   └──  pymatgen_action.py       <- anything related to pymatgen 
    │   │
    |   ├── utils                <-  All helper function
    |   |   |──  read_yaml.py    <-  reading yamls
    │   │   └── manage_files.py  <-  create folders save files 
    │   │
    │   ├── models         <- Scripts to use models in workflows
    │   │   │                 
    │   │   ├── dynamics.py   <- anything realted to md
    │   │   ├── dynamics.py   <- anything realted to screening
    │   │   └── m3gnet.py     <- property prediction, relax
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io  #TODO


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
