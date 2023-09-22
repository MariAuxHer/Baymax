# Malware Classifier using a Multilayer Perceptron

## What the program does? 

This program classifies apk files as malware or benign using a simple Multi-Layer Perceptron neural network. The features fed to the model as well as their respective labels are in the asm_feature.csv file. The program divides the dataset into a training set to train the model and the testing set to measure the accuracy of the model/s predictions. 

## How to run the program? 

- Install anaconda in your machine - make sure it is installed by running the command: conda --version

- Create a new conda environment and activate it: 

    - Run the following commands (replacing myenv with name of your environment):

        - conda create --name myenv
        - conda activate myenv

- Install Jupyter notebook and IPykernel by running the following command: 

    conda install jupyter ipykernel 

- Create a ipynb file (Jupyter notebook) and select the kernel for that notebook by either clicking "Select kernel" in the IDE or running the following command: 

    python -m ipykernel install --user--name=myenv --display-name="My Environment" 

- Install all the necessary dependencies to run the notebook (torch, pandas, and tqdm):

    conda install -c pytorch torch 
    conda install pandas 
    conda install tqdm

- Run all the code cells until the very last one (which tries the model). To run each of the code cells press: ctrl + return 

## How that technology might be used in the group project? 

In our project, we need to do the same data preprocessing I did for this malware classifier - for instance, dropping columns from the csv file that contain irrelevant information. In addition, for the Machine Learning model we will use in our project, we may need to add a multilayer perceptron - similar to the one used in this malware classifier - following the transformer layer. The transformer can handle the input sequences and capture long-range dependencies, while the multilayer perceptron can process extracted features or embeddings from the transformr layers. 
