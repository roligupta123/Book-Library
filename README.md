# 📚 Book Library
A Django-based web application to manage a library system where users can browse, request, and get assigned books.


## 🚀 Features
- User authentication (Admin and normal users)
- Browse books with details (title, author, ISBN, price, etc.)
- Request books (with max limit per user)
- Admin approval/rejection of book requests
- Track assigned books
- Book availability status


## 🛠️ Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default, can be changed to PostgreSQL/MySQL)
- **Version Control:** Git + GitHub


## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/roligupta123/Book-Library.git
   cd Book-Library

2.  Create a virtual environment:
  python -m venv venv
  source venv/bin/activate   
  venv\Scripts\activate

3. Install dependencies:
   ```bash
     pip install -r requirements.txt

5. Apply Migration:
   ```bash
     python manage.py migrate,
     python manage.py makemigrations

6. Run the development server:
   ```bash
   python manage.py runserver

8. Open the app in your browser:
   ```bash
   http://127.0.0.1:8000/



---

This way:
- On GitHub, your name will appear nicely at the bottom.
- You can link to your GitHub profile or email.
- You can even add a profile picture using Markdown if you want.

If you’d like, I can **rewrite your whole README** from start to finish with:
- Project title
- Description
- Setup steps (these commands)
- Author section with your name and GitHub link  
and make it look professional.  

Do you want me to create that polished full README now?
