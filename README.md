# UniSpend.io  

### 🎥 Video Demo  
[Watch here](https://youtu.be/NBsGP7CfqhM)  

---

## 📌 Description  
**UniSpend** is a budgeting web application designed for university students around the world to track their weekly expenses and save money during their studies.  

Students set a **weekly budget**, and every time they log an expense, it gets deducted from that budget. This motivates students to spend wisely and manage their finances better.  

The project was inspired by the **CS50 Flask lecture**, and it uses Flask, SQLite, Jinja, and Bootstrap for implementation.  

---

## ⚙️ Features  
- 👤 **User Authentication** – Register and log in securely with hashed passwords.  
- 💸 **Weekly Budgeting** – Set and update a weekly budget goal.  
- 📝 **Expense Tracking** – Add, remove, and categorize expenses.  
- 📊 **Weekly Summaries** – View detailed summaries of spending and savings for each week.  
- 🌍 **Global Support** – Choose your country at registration; the app automatically assigns the correct **currency code**.  
- 🎨 **UI/UX** – Styled with **Bootstrap** and a custom `main.css` file.  

---

## 🗂️ Project Structure  
- **`app.py`** → Main Flask application (routes and logic).  
- **`templates/`** → 10 HTML templates:  
  - `add.html`, `apology.html`, `change.html`, `index.html`, `layout.html`, `login.html`, `register.html`, `remove.html`, `summary.html`, `weeklysummary.html`  
- **`static/`** → Contains `main.css` for styling.  
- **`userData.db`** → SQLite database storing user and expense data.  
- **`countries.csv`** → List of countries and their currency codes (for global support).  
- **`helpers.py`** → Utility functions (`login_required`, `apology`) adapted from CS50 Finance.  

---

## 🔑 Key Implementation Details  
- The **homepage (`index.html`)** displays the user’s current week expenses, remaining budget, and total days since registration.  
- The app calculates the **current week number** using Python’s `datetime` module.  
- Expenses are stored with:  
  - Type (Education, Food, etc.)  
  - Amount spent  
  - Timestamp  
  - Week number  
- Weekly summaries are auto-generated at the end of each week, letting users review their spending and savings.  
- The **apology template** is adapted from CS50 Finance but customized with a new meme template.  

---

## 🛠️ Technologies Used  
- **Python (Flask)**  
- **SQLite (CS50 SQL)**  
- **HTML, CSS, Bootstrap**  
- **Jinja Templating**  

---

## 🚀 How to Run Locally  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/unispend.git
   cd unispend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app
   ```bash
   flask run
   ```
4. Open in your browser
   ```bash
   http://127.0.0.1:5000
   ```

