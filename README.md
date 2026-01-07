# 🛒 ShopMart – E-Commerce Web Application

ShopMart is a full-stack e-commerce web application built using Django that allows users to browse products, add items to cart, make secure payments, and manage orders. It provides a complete online shopping experience with an admin panel for managing products and users.

---

## 🚀 Features

### 👤 User Features
- User registration & login
- Browse products by category
- Add products to cart
- Place orders and checkout
- Secure online payment using PayPal

### 🛠 Admin Features
- Add, update, and delete products
- Manage users and orders
- View complete sales and order details

---

## 🛠 Tech Stack

| Layer        | Technology            |
|-------------|------------------------|
| Frontend    | HTML, CSS, Bootstrap   |
| Backend     | Python, Django         |
| Database    | SQLite / MySQL         |
| Payments    | PayPal Payment Gateway |
| Architecture| Django MVT             |

---

## 🔄 Application Flow

1. User registers or logs in  
2. Browses products and adds to cart  
3. Proceeds to checkout  
4. Completes payment via PayPal  
5. Order is placed and stored in database  
6. Admin can manage orders and products  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yashgithub2003/ShopMart.git
cd ShopMart
2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser (Admin)
python manage.py createsuperuser

6️⃣ Run the Server
python manage.py runserver

7️⃣ Open in Browser
http://127.0.0.1:8000/
