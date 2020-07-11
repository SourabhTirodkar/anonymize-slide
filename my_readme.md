# Anonymize the whole slide image

## The code does run on python version 2.6 and 2.7

### * 1. Setting up Anaconda Environment

Commands:
a. conda create --name py2 python=2.7
b. activate py2
c. conda install nb_conda

For more information refer [Anaconda page](https://docs.anaconda.com/anaconda/user-guide/tasks/switch-environment/).

If the environment was activated successfully, you should see (py2- name used here) at the beggining of the command prompt. This will set the kernel as your default kernel when running the code.


### * 2. Installing Openslide library and also Openslide binaries files for Windows

OpenSlide is C libraries; as a result, they have to be installed separately from the conda environment, which contains all of the python dependencies.

The Windows Binaries for OpenSlide can be found at 'openslide.org/download/'. Download the appropriate binaries for your system (either 32-bit or 64-bit) and unzip the file.

**Steps:**
a. Copy the .dll files in ../bin/ to .../Anaconda/envs/py2/Library/bin/.
b. Copy the .h files to .../Anaconda/envs/py2/include/.
c. Finally, copy the .lib file to .../Anaconda/envs/py2/libs/.

Note- py2 is the name of the environment.
OpenSlide has now been installed.

Installing Openslide Python library
conda install -c cdeepakroy openslide-python
For more information refer [Anaconda page of openslide](https://anaconda.org/cdeepakroy/openslide-python).

### * 3. Running the code

If you are on the environment created which was just created, go the the path to that environment and then:
***python anonymize-slide.py 'path for the whole slide image'***
Example: python anonymize-slide.py abc.svs
where abc.svs is the filename for the whole slide image and is present in the same path. If not on the same path, we need to mention the path along with the name.

If the whole folder has to be anonymize with a specific format, then:
***anonymize-slide.py *.svs***
This will delete all the labels from the whole slide image

