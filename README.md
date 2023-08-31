# E-BIKE (E-Commerce App)

Welcome to the E-BIKE E-Commerce App repository. This app is a feature-rich, multi-vendor e-commerce platform for buying and selling bikes. It includes various e-commerce functionalities, and is built using Django, PostgreSQL,Html,css ,django template engine for generating dynamic html content 

## Overview

E-BIKE  is a comprehensive e-commerce solution tailored for bike enthusiasts. It provides a user-friendly platform for buying and selling bikes from various vendors. The app includes a wide range of features, including product listing, shopping cart, order management, discounts, reviews, user profiles, and more.

## Features

- Multi-vendor support for bike sellers.
- Product listing with detailed descriptions and image zooming.
- Shopping cart and order management.
- Offers and coupon management.
- User and vendor profiles.
- Review and rating system for Bikes.
- Category management for easy navigation.
- Admin panel for coupon and sales report management.
- OTP verification for secure registration .
- Export data to Excel and PDF formats
- Auto suggestion for product searching
- session and cookie authentication
- sales report using chart js
- reset passwords
- online payment

## Technology Stack
 - Framework: Django
 - Database: PostgreSQL
 - Twilio for otp verification
 - smtp for sending mails
 - Payment Gateway: Razorpay
 - chart js

## Getting Started

Follow these steps to set up and run the app locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ashwin275/E_BIKE.git

2. **Create a virtual environment and activate it:**
      ```bash
      python -m venv djvenv
      source djvenv/bin/activate   # On Windows: djvenv\Scripts\activate
      cd project

3. **pip install -r requirements.txt**
     ```bash
     pip install -r requirements.txt
4. **Set up the PostgreSQL Database:**

    . Create a PostgreSQL database and update the database configuration in the settings.
      
    . Run migrations:

    ```bash
    python manage.py migrate
5. **Configure Twilio for OTP Verification:**
   
     . Update Twilio credentials in the settings.py file.
   
     . Update the email settings in the settings.py file.

7. **Start the backend server:**
      ```bash
      python manage.py runserver
8. **Access the app at** http://127.0.0.1:8000/
    

    
   
