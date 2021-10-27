# Conda
There are two commonly accepted means for running and creating conda environments.
<ol>
<li>Install the whole suite from Anaconda</li>
<ul>
<li>IDE</li>
<ul>
    <li>VS Code</li>
    <li>Spyder</li>
    <li>Jupyter</li>
    <li>RStudio</li>
</ul>
<li>Package Manager</li>
<li>Languages</li>
<ul>
<li>Julia</li>
<li>Python</li>
<li>R</li>
</ul>
</ul>
<li>Install the package management from miniconda</li>
</ol>

## Setting up Conda

You can find the installation packages for [Anaconda](https://www.anaconda.com/products/individual)

You can find the installation packages for [miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Setting up miniconda on Ubuntu

From you terminal enter the following commands
```
$ sudo wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Next you need to make the shell script executable by running the `chmod` command
```
$ sudo chmod +x Miniconda3-latest-Linux-x86_64.sh
```

Next, run the script to install miniconda. Answer "Yes" to the installation questions
```
./Miniconda3-latest-Linux-x86_64.sh
```
Lastly, you can activate conda by simply typing the following command on the prompt
```
conda activate
```

## Conda Virtual Environments
Using virtual environments is the best way to manage development of any python solution. Whether you are doing application development or machine learning, setting up a virtual environment to handle all your packages is absolutely essential for building python solutions. It helps in preventing cross-contamination of python versions, it reduces the number of packages that need to be used for a solution and overall organizes your requirements into easily deployable, updateable lists or Yaml files.

|Function|Command|
|---|---|
|Create a new environment ENV_NAME with Python version 3.X|	conda create --name ENV_NAME python=3.X|
|Create a new environment ENV_NAME with some initial packages|	conda create --name ENV_NAME python=3.X pandas ipykernel|
|Create a new environment from a yaml file|	conda env create --file environment.yaml|
|Activate the environment ENV_NAME (OSX, Linux)|	conda activate ENV_NAME|
|Activate the environment ENV_NAME (Windows)|	source activate ENV_NAME|
|Deactivate the current environment (*)	|source deactivate|
|Delete the environment ENV_NAME	|conda env remove --name ENV_NAME|
|List all installed environments	|conda env list|
|Create a YAML file for active environment(*)	|conda env export > environment.yaml|
