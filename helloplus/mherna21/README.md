# Malware Classifier using a Multilayer Perceptron

## What does the program do? 

The program classifies APK files as malware or benign using a Multilayer Perceptron neural network.
The features and labels are obtained from the 'asm_feature.csv' file.
The dataset is divided into a training set for model training and a testing set for accuracy measurement.

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

In our project, we can apply similar data preprocessing techniques used in this malware classifier, such as removing irrelevant columns from the CSV file. Additionally, we may incorporate a multilayer perceptron, similar to the one utilized in this malware classifier, after the transformer layer in our Machine Learning model. This approach allows the transformer to handle input sequences, capturing 
long-range dependencies, while the multilayer perceptron processes extracted features or embeddings from the transformer layers.
