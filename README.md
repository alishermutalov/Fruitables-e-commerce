# E-commerce Django Application

This is a fully functional e-commerce website built with Django. It provides users with the ability to browse products, add them to their cart, checkout with a payment system, and manage their orders. The site also includes user authentication, profile management, and multi-language support.

## Features

- **Product Catalog**: Users can browse a wide range of products, filter by categories, and search for items.
- **Cart System**: Users can add products to their cart, update quantities, and proceed to checkout.
- **Order Management**: Users can view their order history and track the status of their current orders.
- **User Profiles**: Each user has a profile with address, phone number, and date of birth. Users can update their profile information.
- **Multi-language Support**: The website supports multiple languages.
- **Payment Integration**: The site uses the Stripe provider to handle payments.
- **Responsive Design**: The website is fully responsive and works on all devices.
- **Authentication**: Users can register, log in, and log out, with options for social login (Google).
- **Admin Panel**: Admins can manage products, categories, users, and orders through the Django admin interface.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ecommerce-django.git
   cd ecommerce-django
   
2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install dependencies:**:
   ```bash
   pip install -r requirements.txt

4. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   
6. **Run the development server:**
   ```bash
   python manage.py runserver
   
### Notes:
- Customize this template to match the specific details of your project.
- Add any additional features or functionalities your project may include.
