

---

# 🎬💰🐍 Multi-Project Repository

This repository contains **three standalone projects** I built using different technologies:

1. **Expense Tracker (Java)** – A Java-based desktop application for managing personal finances.
2. **Movie Library Management System (Python + MySQL + Tkinter)** – A GUI-based movie library with authentication, watchlist, and video playback.
3. **Snake Game (Python + Pygame)** – A fun snake game with obstacles, scoring, and sounds.

---

## 📂 Project Structure

```
├── ExpenseTracker.java         # Java Expense Tracker Application
├── movie_library.py            # Movie Library Management System (Tkinter + MySQL)
├── game.py                     # Snake Game (Pygame)
└── README.md                   # Project Documentation
```

---

## 💰 1. Expense Tracker (Java)

### 📌 Overview

A simple **Java desktop application** to track personal expenses. It helps users log daily expenses, categorize them, and generate summaries.

### ✨ Features

* Add, view, and delete expenses.
* Categorization of expenses (e.g., Food, Travel, Shopping).
* Summary of total expenses.
* Lightweight and easy-to-use.

### ⚙️ Tech Stack

* **Java** (Core Java, Swing/JavaFX if GUI present).

### 🚀 How to Run

1. Compile the Java file:

   ```bash
   javac ExpenseTracker.java
   ```
2. Run the program:

   ```bash
   java ExpenseTracker
   ```

---

## 🎬 2. Movie Library Management System (Python + MySQL + Tkinter)

### 📌 Overview

A **GUI-based movie library** where admins can add movies and users can register/login, search movies, view details, maintain watchlists, and play videos.

### ✨ Features

* **Admin Panel**

  * Add movies with details (rating, genre, director, etc.).
  * Upload and store movie posters & videos in MySQL.
  * View user history.

* **User Panel**

  * Register & login with credentials.
  * Search movies and view details.
  * Add to watchlist and view history.
  * Play videos directly inside the app.

### ⚙️ Tech Stack

* **Python** (Tkinter, MoviePy, PIL, OpenCV)
* **MySQL** (Backend database for movies, users, watchlist, history)

### 📂 Database Schema

* `users(id, username, password)`
* `admin(id, username, password)`
* `short_movies(movie_id, name, rating, genre, year, released, score, votes, director, writer, star, country, budget, gross, company, runtime)`
* `images(movie_id, image)`
* `videos(movie_id, video)`
* `history(id, movie_id, name)`
* `watchlist(id, movie_id, name)`

### 🚀 How to Run

1. Install dependencies:

   ```bash
   pip install mysql-connector-python pillow opencv-python moviepy
   ```
2. Ensure you have a **MySQL database** running and update your connection in the script:

   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="your_password",
       database="miniproject"
   )
   ```
3. Run the script:

   ```bash
   python movie_library.py
   ```

---

## 🐍 3. Snake Game (Python + Pygame)

### 📌 Overview

A classic **Snake Game** with added difficulty from randomly generated obstacles. Built using Pygame with smooth graphics and sound effects.

### ✨ Features

* Start screen with a **“Start Game”** button.
* Food collection increases score & snake length.
* Randomly generated obstacles.
* High score tracking (`hiscore.txt`).
* Game over screen with restart option.
* Background music and sound effects.

### ⚙️ Tech Stack

* **Python**
* **Pygame**

### 🚀 How to Run

1. Install dependencies:

   ```bash
   pip install pygame
   ```
2. Run the game:

   ```bash
   python game.py
   ```

---

## 🔮 Future Improvements

* **Expense Tracker**: Add database support, graphs for expense visualization.
* **Movie Library**: Add user ratings, recommendations, better video playback integration.
* **Snake Game**: Add levels, power-ups, and multiplayer mode.

---


