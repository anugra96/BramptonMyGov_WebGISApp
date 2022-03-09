# BramptonMyGov_WebGISApp
 
## How To Run App On Localhost


### 1. Install miniconda on local machine
Go to [Miniconda — Conda documentation](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links) to download the appropriate installer for your local machine.

### 2. Open Anaconda Prompt (Miniconda3)
Search "Anaconda Prompt (Miniconda3)" in start menu and open. 
Navigate to cloned repo on your local machine. 

    cd <PATH_TO_CLONED_REPO>

### 3. Set up Conda Virtual Environment from environment.yml
In the Anaconda Prompt, run the following command:

    conda env create -f environment.yml --prefix ./venv
This will construct a conda virtual environment in the cloned repo folder called "venv", with all dependencies required to run the app. 

### 4. Activate Conda Virtual Environment
The conda virtual environment needs to be activated using the following command in Anaconda prompt:

    conda activate ./venv

### 5. Run app.py To Open Web App on Localhost
Run the following command:

    python app.py

The app will then open in your local host. Click the localhost link in the Anaconda Prompt.

### 6. ENJOY!