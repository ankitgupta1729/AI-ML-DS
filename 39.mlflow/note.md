1. Mlflow tool makes experiment tracking efficient. It also has other benefits like reproducibility and deployment as well as model management(you can export models to model registry like this is V1 model, this is V2 model).

It makes ML development easier. Mlflow is an important part of MLOps. you can install it by `pip install mlflow` and then run `mlflow ui` to launch local version of mlflow.

2. Go to terminal and go to "/AI-ML-DS/39.mlflow/demo" location and then run `conda activate base` and then run `mlflow ui`. Once you launch the mlflow UI in browser then open docs after clicking it on the page. 

3. Run the `experiment1.ipynb` and `experiment2.ipynb` notebooks with base environment and then check the experiments in the mlflow UI in browser. You can compare models and download artifacts and can use these downloaded artifacts in docker.

4. For model registry or model registration, check `experiment3.ipynb`. Now, suppose, I have to register XGB model with SMOTE for deployment then we have to change in the experiment3.ipynb notebook at the end. For run_id, you have to go to the mlflow ui and go to a particular model and copy the run id and then paste it in the notebook.

After running the code, you can check the model in the mlflow UI in browser in `model` tab for registered model and there you can put the description and alias as `challenger` for experimentation models and `champion` for deployment models in production.

5. Check the modification in code for loading the model and testing few predictions for test dataset after downloading the model.

You can also copy the model to production and put alias as `champion` in mlflow UI.

There are various cloud providers which support it and so we can download the model from mlflow ui and package it and put into docker and run it in production.

We can also make Jenkins (CI/CD tool) to create pipeline to automate all ml workflows.

You can see the mlflow docs for databricks and other platforms deployments.

6. Currently we are doing things locally but what if there are 2 or more data scientists in the same team and they want to publish their experiment results to some centralized cloud based servers. 

DagsHub(https://dagshub.com/) is a tool or platform that will help us do that. 

First create a github repo for this with name as `mlflow_dagshub_demo` (https://github.com/ankitgupta1729/mlflow_dagshub_demo) and put the experiment3.ipynb notebook in it.

Now, go to dagshub and login and create a new account. Dagshub is like github with version control and data control and many other features. 

Now, click on the `Create` button and click on `Connect with a Repository`. Connect with github and add the mlflow_dagshub_demo repo and connect that repo. 

Now, go to `Experiments` tab and copy the code of first 2 lines for dagshub setup and put it in experiment3.ipynb notebook below the header dagshub setup.

Now, change the below 2 lines as:

#mlflow.set_tracking_uri(uri="http://127.0.0.1:5000/")
mlflow.set_tracking_uri(uri="https://dagshub.com/ankitgupta1729/mlflow_dagshub_demo.mlflow")

Now, run the cell and check the results at `https://dagshub.com/ankitgupta1729/mlflow_dagshub_demo.mlflow` in browser. You can also register the model on dagshub or through code as well.

7. 

