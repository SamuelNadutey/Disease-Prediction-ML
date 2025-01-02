# Disease Prediction with Machine Learning

This project uses machine learning to predict diseases (diabetes, heart disease, and Parkinson's) based on user-input health data. The app is built using Python and Streamlit, providing an interactive interface for users to visualize results and receive health insights.

**Note:** This project is in beta and is continually being worked on to improve accuracy and add more features.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Training](#model-training)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Contributing](#contributing)

## Overview
The goal of this project is to create a simple, user-friendly application that can predict multiple diseases using health data. By entering relevant medical metrics, users receive predictions and recommended actions. The app leverages trained machine learning models saved as `.sav` files for fast inference.

## Features
- **Predicts three diseases:** Diabetes, Heart Disease, Parkinson's
- **Interactive UI** – Built with Streamlit
- **Real-time Visualizations** – Displays health metrics with radar/spider charts (Plotly)
- **Model Persistence** – Pre-trained models are stored and loaded using `joblib`
- **Health Insights** – Provides recommended actions if risk is detected

## Installation
### Requirements
- Python 3.7+
- pip
- Git

### Clone the Repository
```bash
 git clone https://github.com/yourusername/disease-prediction-app.git
 cd disease-prediction-app
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app/app.py
```

## Usage
1. Launch the app by running the Streamlit command above.
2. Upload health data (CSV format) or manually input the values.
3. Select the type of disease prediction (Diabetes, Heart Disease, Parkinson's).
4. View predictions and visualizations.
5. Follow the recommended actions if the prediction detects a risk.

## Model Training
The models used in this project were trained using Google Colab notebooks. Each notebook contains data preprocessing, feature selection, model training, and evaluation. 

### Notebooks
- [Diabetes Model Training (Colab)](https://colab.research.google.com/drive/1YEVfewJHdT7MitTQ4fnynvja9hKbWBCE?usp=drive_link)
- [Heart Disease Model Training (Colab)](https://colab.research.google.com/drive/19DmV2PuA2ogaPxeq_b-aIFajFLF8nprj?usp=drive_link)
- [Parkinson's Model Training (Colab)](https://colab.research.google.com/drive/1xx5xVpR0TB--29U72spzXCdl4YxCUqhg?usp=drive_link)

### Accuracy and Metrics
- **Diabetes Model:**
  - Accuracy: 92%
- **Heart Disease Model:**
  - Accuracy: 88%
- **Parkinson's Model:**
  - Accuracy: 87%

The models were evaluated using standard machine learning techniques, including train-test splitting, cross-validation, and hyperparameter tuning.

## Demo
A live demo will be available soon. In the meantime, follow the installation and usage instructions to try it locally.

For a quick preview, here is a **GIF walkthrough** of the app in action (coming soon).

## Technologies Used
- **Machine Learning** – scikit-learn (model training)
- **Web Framework** – Streamlit
- **Visualization** – Plotly
- **Data Handling** – Pandas
- **Model Saving/Loading** – joblib

## File Structure
```
project-folder/
│
├── app/
│   ├── app.py                 # Main Streamlit app file
│   ├── diabetes_model.sav     # Diabetes prediction model
│   ├── heart_disease_model.sav # Heart disease prediction model
│   ├── parkinsons_model.sav   # Parkinson's prediction model
│
├── data/
│   ├── diabetes.csv           # Sample diabetes dataset
│   ├── heart_disease.csv      # Sample heart disease dataset
│   ├── parkinsons.csv         # Sample Parkinson's dataset
│
├── notebooks/                 # Google Colab Notebooks for model training
│   ├── diabetes_training.ipynb
│   ├── heart_disease_training.ipynb
│   ├── parkinsons_training.ipynb
│
├── images/
│   └── health_banner.jpg      # App banner image
│
├── saved_models/              # Folder containing pre-trained models
│
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── streamlit_run.sh           # Shell script to launch the app
├── .gitignore                 # Ignore unnecessary files
```

## Contributing
Contributions are welcome! If you'd like to contribute to the project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature/your-feature`).
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

**Ongoing Development:** 
- Additional disease models will be integrated in future updates.
- UI improvements and expanded visualizations are in progress.
- More datasets and performance enhancements will be added.

