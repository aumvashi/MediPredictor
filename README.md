# MediPredictor

**MediPredictor** is a comprehensive health assistant application designed to predict medical conditions such as diabetes, heart disease, and Parkinson's disease using machine learning models. It provides a user-friendly interface for patients to input their health data and receive predictions, and an admin interface to manage and view user details securely.

## Table of Contents
1. [Unique Idea Brief (Solution)](#unique-idea-brief-solution)
2. [Features Offered](#features-offered)
3. [Process Flow](#process-flow)
4. [Architecture Diagram](#architecture-diagram)
5. [Technologies Used](#technologies-used)
6. [Prerequisites](#prereguisites)

## Unique Idea Brief (Solution)
MediPredictor aims to provide an accessible and reliable way for individuals to get preliminary assessments for serious health conditions using advanced machine learning models. This solution bridges the gap between patients and medical professionals by providing initial screening results that can prompt further medical consultation.

## Features Offered
- **User Registration and Login**: Secure registration and login for users and admins.
- **Health Predictions**: Predicts the likelihood of diabetes, heart disease, and Parkinson's disease.
- **Admin Dashboard**: Admins can view all user details except for passwords, which are securely hashed.
- **Interactive Interface**: User-friendly interface designed using Streamlit.
- **Data Security**: Secure handling of user data with encryption for sensitive information.

## Process Flow
1. **User Registration**: Users sign up with their details.
2. **Login**: Users log in to access health prediction services.
3. **Data Input**: Users input their health metrics.
4. **Prediction**: Machine learning models process the input data and provide predictions.
5. **Result Display**: The prediction results are displayed to the user.
6. **Admin Access**: Admins log in to view user details and manage the system.

## Architecture Diagram
<img width="520" alt="System Architecture" src="https://github.com/aumvashi/MediPredictor/assets/165994662/f97da9ad-2b34-477f-a879-b2d73cfb2bc0">


## Technologies Used
- **Streamlit**: Front-end framework for creating the web interface.
- **SQLite**: Database for storing user data.
- **Bcrypt**: Library for password hashing.
- **Machine Learning Models**: Pre-trained models for predicting diabetes, heart disease, and Parkinson's disease.
- **Python**: Main programming language used for development.


### Prerequisites
- Python 3.x installed on your system.
- Virtual environment setup (optional but recommended).


