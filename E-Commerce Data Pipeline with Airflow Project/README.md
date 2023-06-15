# E-Commerce Data Pipeline With Airflow
## Project Overview

This project is designed to demonstrate the implementation of a data pipeline using Apache Airflow. The dataset used for this project is sourced from Kaggle, specifically the "E-commerce Sales Data" dataset, which can be accessed [here](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data).

## Objective
The main objective of this project is to showcase how Apache Airflow can be utilized to build and orchestrate a data pipeline for processing and analyzing e-commerce sales data (specifically Amazon Sale Report.csv data). By leveraging Apache Airflow's capabilities, the project aims to highlight the ease and efficiency of managing complex data workflows, including data extraction, transformation, loading, and analysis.

## Technologies Used
The project utilizes the following technologies:

- **Apache Airflow**: A platform used to programmatically author, schedule, and monitor workflows, making it ideal for constructing data pipelines.
- **Python**: The primary programming language used for scripting and executing tasks within the Apache Airflow environment.
- **Pandas**: A powerful data manipulation and analysis library used for handling and transforming the e-commerce sales data.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) library employed for connecting to and querying the project's database.
- **PostgreSQL**: An open-source relational database management system utilized for storing and managing the transformed data.

## Project Structure
The project's structure consists of the following components:

1. **DAGs (Directed Acyclic Graphs) Folder**: This folder contains the definition of the DAGs, which represent the workflows created using Apache Airflow. These DAGs define the tasks, their dependencies, and the schedule for executing the tasks.
2. **Scripts Folder**: This folder comprises the Python scripts used for extracting, transforming, and loading the e-commerce sales data. These scripts are executed as tasks within the DAGs.
3. **Data Folder**: This folder stores the e-commerce sales data downloaded from Kaggle. It contains the necessary CSV files required for the project.
4. **Notebooks Folder**: This folder includes Jupyter notebooks that provide step-by-step explanations of the data pipeline implementation using Apache Airflow. These notebooks can serve as a guide for understanding and reproducing the project.

## Getting Started
To run this project locally, follow these steps:

1. Clone the project repository from GitHub.
2. Set up a local Apache Airflow environment and configure it accordingly.
3. Download the e-commerce sales data from the Kaggle link provided above and place it in the "Data" folder.
4. Install the required dependencies by running `pip install -r requirements.txt` in your project's virtual environment.
5. Adjust the necessary configurations within the DAGs and scripts to match your local setup (e.g., file paths, database credentials, etc.).
6. Start Apache Airflow's web server and scheduler.
7. Trigger the DAGs manually or based on the specified schedule, and monitor the progress and results through the Apache Airflow UI.

## Conclusion
By showcasing the implementation of a data pipeline using Apache Airflow, this project demonstrates the power and flexibility of Apache Airflow in managing and automating complex data workflows. Through the use of the provided e-commerce sales dataset, users can gain insights into the various stages of data processing and analysis, including extraction, transformation, loading, and querying of data. Feel free to explore the project and adapt it to your specific requirements or datasets. Happy coding!
