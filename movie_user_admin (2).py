import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import io
from tkinter import Tk, filedialog
import cv2
import tempfile
import os
from moviepy.editor import VideoFileClip

global newid, mydb, mycursor, username, font, username_entry, password_entry, bg
font = ('Helvetica', 12)
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhakti$04",
        database="miniproject"
    )

mycursor = mydb.cursor()

def admin_login_window():
    global newid, username, username_entry, password_entry
    root = tk.Toplevel(main_root)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d"%(width, height))
    root.title("Admin Login")

    # Show image using label 
    label1 = tk.Label(root, image = bg) 
    label1.place(x = 0, y = 0)

    # Create labels and entry fields
    username_label = tk.Label(root, text="Username:", font=font)
    username_label.place(x=width/2-60, y=height/2 -60)
    username_entry = tk.Entry(root,  font=font)
    username_entry.place(x=width/2-60, y=height/2 -30)

    password_label = tk.Label(root, text="Password:", font=font)
    password_label.place(x=width/2-60, y=height/2)
    password_entry = tk.Entry(root, show="*", font=font)
    password_entry.place(x=width/2-60, y=height/2 +30)

    login_button = tk.Button(root, text="Login", font=font, command=lambda: login("admin"))
    login_button.place(x=width/2-40, y=height/2 +80)
    # main_root.withdraw()

def login(tablename):
    global newid, username
    username = username_entry.get()
    password = password_entry.get()

    # Create a table if not exists
    query="CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))".format(tablename)
    mycursor.execute(query)
    query = "SELECT username FROM {} where username=(%s)".format(tablename)
    mycursor.execute(query, [username])
    use = mycursor.fetchall()
    q = "SELECT password FROM {} where username=(%s)".format(tablename)
    mycursor.execute(q, [username])
    p = mycursor.fetchall()
    query = "select id from {} where username=(%s)".format(tablename)
    mycursor.execute(query, [username])
    newid = mycursor.fetchall()
    # print(type(use), "  ", p)
    if len(use)==0:
        messagebox.showinfo("Login Error", f"{tablename} does not exist.")
        return
    else:
        # print(type(p), "  ", p)
        if p[0][0]!=password:
            messagebox.showinfo("Login Error", f"Incorrect Password!!!")
            return

    # Clear the entry fields
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    # main_root.withdraw()
    if tablename=="admin":
        start_admin_main_window()
    else:
        start_user_main_window()

def start_admin_main_window():
    admin_window = tk.Toplevel(main_root)
    admin_window.title("Admin Window")
    
    # Create a frame to contain the buttons with a background color
    button_frame = ttk.Frame(admin_window, padding=20)
    button_frame.pack(padx=20, pady=20)

    # Create four buttons in a box layout
    button1 = ttk.Button(button_frame, text="Add Movie", command=add_movie)
    button1.grid(row=0, column=0, padx=5, pady=5)

    # button2 = ttk.Button(button_frame, text="Delete Movie")
    # button2.grid(row=0, column=1, padx=5, pady=5)

    button3 = ttk.Button(button_frame, text="View History", command=view_history)
    button3.grid(row=1, column=0, padx=5, pady=5)

    # button4 = ttk.Button(button_frame, text="View History of a User", command=view_specific_history)
    # button4.grid(row=1, column=1, padx=5, pady=5)

def user_login_window():
    global newid, username, username_entry, password_entry
    print("in user")
    root = tk.Toplevel(main_root)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d"%(width, height))
    root.title("User Login/Registration")

    # Show image using label 
    label1 = tk.Label(root, image = bg) 
    label1.place(x = 0, y = 0)
    
    # Create labels and entry fields
    username_label = tk.Label(root, text="Username:", font=font)
    username_label.place(x=width/2-60, y=height/2 -60)
    username_entry = tk.Entry(root,  font=font)
    username_entry.place(x=width/2-60, y=height/2 -30)

    password_label = tk.Label(root, text="Password:", font=font)
    password_label.place(x=width/2-60, y=height/2)
    password_entry = tk.Entry(root, show="*", font=font)
    password_entry.place(x=width/2-60, y=height/2 +30)

    login_button = tk.Button(root, text="Login", font=font, command=lambda: login("users"))
    login_button.place(x=width/2-40, y=height/2 +80)
    register_button = tk.Button(root, text="Register", font=font, command=user_register)
    register_button.place(x=width/2+40, y=height/2 +80)
    # main_root.withdraw()

def user_register():
    global newid, mydb, mycursor, username
    username = username_entry.get()
    password = password_entry.get()

    # Create a table if not exists
    mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
    query = "SELECT username FROM users where username=(%s)"
    mycursor.execute(query, [username])
    use = mycursor.fetchall()
    q = "SELECT password FROM users where username=(%s)"
    mycursor.execute(q, [username])
    p = mycursor.fetchall()
    query = "select id from users where username=(%s)"
    mycursor.execute(query, [username])
    newid = mycursor.fetchall()
    # print(type(use), "  ", p)
    if len(use)==0:
        # Insert username and password into the table
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("User registered successfully!")
    else:
        # print(type(p), "  ", p)
        messagebox.showinfo("Registration Error", f"User Already exists. Please login!!!")
        return

    # Clear the entry fields
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    # main_root.withdraw()
    start_user_main_window()

def add_movie():
    add_movie_window = tk.Toplevel(main_root)
    width = add_movie_window.winfo_screenwidth()
    height = add_movie_window.winfo_screenheight()
    add_movie_window.geometry("%dx%d"%(width, height))
    add_movie_window.title("Add Movie")

    # Create a frame to contain the buttons with a transparent background
    details_frame = ttk.Frame(add_movie_window, style='Transparent.TFrame')
    details_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create a custom style for the frame to make it transparent
    style = ttk.Style()
    style.configure('Transparent.TFrame', background='')

    # Movie Name
    movie_name_label = tk.Label(details_frame, text="Movie Name: ", font=font)
    movie_name_label.grid(row=0, column=0, padx=5, pady=5)
    movie_name_entry = tk.Entry(details_frame, font=font)
    movie_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Rating
    movie_rating_label = tk.Label(details_frame, text="Rating: ", font=font)
    movie_rating_label.grid(row=1, column=0, padx=5, pady=5)
    movie_rating_entry = tk.Entry(details_frame, font=font)
    movie_rating_entry.grid(row=1, column=1, padx=5, pady=5)

    # Genre
    movie_genre_label = tk.Label(details_frame, text="Genre: ", font=font)
    movie_genre_label.grid(row=2, column=0, padx=5, pady=5)
    movie_genre_entry = tk.Entry(details_frame, font=font)
    movie_genre_entry.grid(row=2, column=1, padx=5, pady=5)

    # Year Released
    movie_year_label = tk.Label(details_frame, text="Year Released: ", font=font)
    movie_year_label.grid(row=3, column=0, padx=5, pady=5)
    movie_year_entry = tk.Entry(details_frame, font=font)
    movie_year_entry.grid(row=3, column=1, padx=5, pady=5)

    # Released
    movie_year_label = tk.Label(details_frame, text="Released: ", font=font)
    movie_year_label.grid(row=4, column=0, padx=5, pady=5)
    movie_year_entry = tk.Entry(details_frame, font=font)
    movie_year_entry.grid(row=4, column=1, padx=5, pady=5)

    # Score
    movie_score_label = tk.Label(details_frame, text="Score: ", font=font)
    movie_score_label.grid(row=5, column=0, padx=5, pady=5)
    movie_score_entry = tk.Entry(details_frame, font=font)
    movie_score_entry.grid(row=5, column=1, padx=5, pady=5)

    # Votes
    movie_votes_label = tk.Label(details_frame, text="Votes: ", font=font)
    movie_votes_label.grid(row=6, column=0, padx=5, pady=5)
    movie_votes_entry = tk.Entry(details_frame, font=font)
    movie_votes_entry.grid(row=6, column=1, padx=5, pady=5)

    # Director
    movie_director_label = tk.Label(details_frame, text="Director: ", font=font)
    movie_director_label.grid(row=7, column=0, padx=5, pady=5)
    movie_director_entry = tk.Entry(details_frame, font=font)
    movie_director_entry.grid(row=7, column=1, padx=5, pady=5)

    # Writer
    movie_writer_label = tk.Label(details_frame, text="Writer: ", font=font)
    movie_writer_label.grid(row=8, column=0, padx=5, pady=5)
    movie_writer_entry = tk.Entry(details_frame, font=font)
    movie_writer_entry.grid(row=8, column=1, padx=5, pady=5)

    # Star
    movie_star_label = tk.Label(details_frame, text="Star: ", font=font)
    movie_star_label.grid(row=9, column=0, padx=5, pady=5)
    movie_star_entry = tk.Entry(details_frame, font=font)
    movie_star_entry.grid(row=9, column=1, padx=5, pady=5)

    # Country
    movie_country_label = tk.Label(details_frame, text="Country: ", font=font)
    movie_country_label.grid(row=10, column=0, padx=5, pady=5)
    movie_country_entry = tk.Entry(details_frame, font=font)
    movie_country_entry.grid(row=10, column=1, padx=5, pady=5)

    # Budget
    movie_budget_label = tk.Label(details_frame, text="Budget: ", font=font)
    movie_budget_label.grid(row=11, column=0, padx=5, pady=5)
    movie_budget_entry = tk.Entry(details_frame, font=font)
    movie_budget_entry.grid(row=11, column=1, padx=5, pady=5)

    # Gross
    movie_gross_label = tk.Label(details_frame, text="Gross: ", font=font)
    movie_gross_label.grid(row=12, column=0, padx=5, pady=5)
    movie_gross_entry = tk.Entry(details_frame, font=font)
    movie_gross_entry.grid(row=12, column=1, padx=5, pady=5)

    # Company
    movie_company_label = tk.Label(details_frame, text="Company: ", font=font)
    movie_company_label.grid(row=13, column=0, padx=5, pady=5)
    movie_company_entry = tk.Entry(details_frame, font=font)
    movie_company_entry.grid(row=13, column=1, padx=5, pady=5)

    # Runtime
    movie_runtime_label = tk.Label(details_frame, text="Runtime: ", font=font)
    movie_runtime_label.grid(row=14, column=0, padx=5, pady=5)
    movie_runtime_entry = tk.Entry(details_frame, font=font)
    movie_runtime_entry.grid(row=14, column=1, padx=5, pady=5)

    def add_image_to_database():

        # Function to prompt user to select an image file
        def select_image_file():
            root = Tk()
            root.withdraw()  # Hide the main window

            # Open a file dialog for selecting an image
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            root.destroy()  # Destroy the Tkinter window

            return file_path

        # Select image file using file dialog
        image_path = select_image_file()

        # Insert image into the table
        with open(image_path, "rb") as file:
            image_data = file.read()
            mycursor.execute("select count(movie_id) from images")
            count = mycursor.fetchall()[0][0] + 1
            query = "INSERT INTO images (movie_id, image) VALUES (%s, %s)"
            mycursor.execute(query, (count, image_data))
            mydb.commit()

        print("Image added")

    # Image
    add_image_label = tk.Label(details_frame, text="Image: ", font=font)
    add_image_label.grid(row=15, column=0, padx=5, pady=5)
    add_image_button = tk.Button(details_frame, text="Choose Image", font=font, command=add_image_to_database)
    add_image_button.grid(row=15, column=1, columnspan=2, padx=5, pady=5)

    def add_movie_to_database():
        # Retrieve values from entry widgets
        movie_name = movie_name_entry.get()
        rating = movie_rating_entry.get()
        genre = movie_genre_entry.get()
        year = movie_year_entry.get()
        released = movie_year_entry.get()
        score = movie_score_entry.get()
        votes = movie_votes_entry.get()
        director = movie_director_entry.get()
        writer = movie_writer_entry.get()
        star = movie_star_entry.get()
        country = movie_country_entry.get()
        budget = movie_budget_entry.get()
        gross = movie_gross_entry.get()
        company = movie_company_entry.get()
        runtime = movie_runtime_entry.get()
        
        mycursor.execute("select count(movie_id) from short_movies")
        count = mycursor.fetchall()[0][0] + 1  # Increment count by 1
        
        # Insert values into the database
        query = "INSERT INTO short_movies (movie_id, name, rating, genre, year, released, score, votes, director, writer, star, country, budget, gross, company, runtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (count, movie_name, rating, genre, year, released, score, votes, director, writer, star, country, budget, gross, company, runtime)
        mycursor.execute(query, values)
        mydb.commit()
        messagebox.showinfo("Movie Added", f"Movie '{movie_name}' added successfully!!!")

    # Create "add" button
    add_button = tk.Button(details_frame, text="Add", font=font, command=add_movie_to_database)
    add_button.grid(row=16, column=0, columnspan=2, padx=5, pady=5)

def view_history():
    # Placeholder function for opening the history
    history_info_window = tk.Toplevel(main_root)
    history_info_window.geometry("600x400")
    history_info_window.title("History of all users")
    
    my_scrolling_list(history_info_window, "SELECT * FROM history", False , [] , "history")

def view_specific_history():
    # Placeholder function for opening the history
    history_info_window = tk.Toplevel(main_root)
    history_info_window.geometry("600x400")
    history_info_window.title("History of users")

    # Create a frame to contain the buttons with a transparent background
    details_frame = ttk.Frame(history_info_window, style='Transparent.TFrame')
    details_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create a custom style for the frame to make it transparent
    style = ttk.Style()
    style.configure('Transparent.TFrame', background='')
    print("in viewing history")
    username_label = tk.Label(details_frame, text="Enter username: ", font=font)
    username_label.grid(row=0, column=0, padx=5, pady=5)
    username_label_entry = tk.Entry(details_frame, font=font)
    username_label_entry.grid(row=0, column=1, padx=5, pady=5)
    user = username_label_entry.get()
    mycursor.execute("select id from users where username=(%s)", [user])
    id = mycursor.fetchall()

    my_scrolling_list(history_info_window, "SELECT * FROM history where id=(%s)", True , [id[0][0]] , "history")

def my_scrolling_list(window, forquery, iswhere, where_find, tablename):
    # Create a frame to hold movie names with scrollbar
    movie_frame = tk.Frame(window, bg="black")
    movie_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(movie_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas within the movie frame
    canvas = tk.Canvas(movie_frame, yscrollcommand=scrollbar.set, bg="black")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame to contain the movie labels
    movie_container = tk.Frame(canvas, bg="black")
    # movie_container.configure(bg="black")
    canvas.create_window((0, 0), window=movie_container, anchor=tk.NW)

    scrollbar.config(command=canvas.yview)

    if iswhere:
        mycursor.execute(forquery, where_find)
    else:
        # Fetch movie names from the database
        mycursor.execute(forquery)
    
    movies = mycursor.fetchall()

    # Display movie names in frames with "More" button
    for movie in movies:
        if tablename!="short_movies":
            movie_name = movie[2]
        else:
            movie_name = movie[1]

        # Create a frame for each movie name
        movie_frame_item = tk.Frame(movie_container, bg="black")
        movie_frame_item.pack(fill=tk.X, padx=5, pady=2)

        movie_image_item = tk.Frame(movie_frame_item, width=10, height=10, bg="black")
        movie_image_item.pack(side=tk.LEFT)

        if tablename=="short_movies":
            myid=movie[0]
        else:
            myid=movie[1]
        # print(myid)
        mycursor.execute("SELECT image FROM images WHERE movie_id = (%s)", [myid])
        image_data = mycursor.fetchone()[0]
        
        # Convert image data to ImageTk format
        image = Image.open(io.BytesIO(image_data))
        newsize = (50, 60)
        image = image.resize(newsize)
        photo = ImageTk.PhotoImage(image)
            
        # Display movie poster image
        image_label = tk.Label(movie_image_item, image=photo)
        image_label.image = photo  # To prevent garbage collection
        image_label.pack(side=tk.LEFT)

        # Label to display the movie name
        movie_name_label = tk.Label(movie_frame_item, text=movie_name, font=font, bg="black", fg="white")
        movie_name_label.pack(side=tk.LEFT)

        if tablename!="short_movies":
            remove_button = tk.Button(movie_frame_item, text="Remove", bg="red", fg="white", command=lambda m=movie: remove_history(m, movie_frame_item, tablename))
            remove_button.pack(side=tk.RIGHT)
        else:
            # Button for "More" action
            more_button = tk.Button(movie_frame_item, text="More", bg="blue", fg="white", command=lambda m=movie: more_info(m, username))
            more_button.pack(side=tk.RIGHT)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    movie_container.bind("<Configure>", on_configure)

def start_user_main_window():
    # Open a new window displaying user info and options
    user_info_window = tk.Toplevel(main_root)
    width = main_root.winfo_screenwidth()
    height = main_root.winfo_screenheight()
    user_info_window.geometry("%dx%d"%(width-40, height-100))
    user_info_window.configure(bg="black")
    user_info_window.title("User Information")

    search_frame = tk.Frame(user_info_window)
    search_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

    search_entry = tk.Entry(search_frame, font=font, text="Enter movie name to search...")
    search_entry.pack(side=tk.LEFT)

    search_button = tk.Button(search_frame, text="Search", font=font, command=lambda:getmovie(search_entry))
    search_button.pack(side=tk.LEFT, padx=5)
    # search_entry.bind("<Return>", getmovie(findmovie)) 

    # Create a frame to hold the labels
    label_frame = tk.Frame(user_info_window, bg="black")
    label_frame.pack(side=tk.TOP, fill=tk.X)

    # Display movie names
    movie_label = tk.Label(label_frame, text="Movie Names:", font=font)
    movie_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Display the registered username
    username_label = tk.Label(label_frame, text="Welcome "+str(username), font=font)
    username_label.pack(side=tk.RIGHT, padx=10, pady=10)

    # Pack the labels frame
    label_frame.pack(side=tk.TOP, fill=tk.X)

    my_scrolling_list(user_info_window, "SELECT * FROM short_movies", False, [], "short_movies")

    # Add Watchlist button
    watchlist_button = tk.Button(user_info_window, text="Watchlist", command=lambda: open_watchlist(username))
    watchlist_button.pack(pady=5)

    # Add History button
    history_button = tk.Button(user_info_window, text="History", command=lambda: open_history(username))
    history_button.pack(pady=5)

def getmovie(search_entry):
    # Create a frame to hold movie names with scrollbar
    findmovie = search_entry.get()
    print(findmovie)

    mycursor.execute("SELECT * FROM short_movies where name=(%s)", [findmovie])
    movies = mycursor.fetchall()
    if(len(movies)==0):
        messagebox.showinfo("Movie not found", f"Movie '{findmovie}' not present!")
        return
    else:
        search_info_window = tk.Toplevel(main_root)
        search_info_window.geometry("600x400")
        search_info_window.title("Your Searched Movie")
        my_scrolling_list(search_info_window, "SELECT * FROM short_movies where name=(%s)", True, [findmovie], "short_movies")

def more_info(movie, username):
    print(movie)
    movie_info_window = tk.Toplevel(main_root)
    movie_info_window.geometry("600x400")
    movie_info_window.title("Movie Information")

    movie_image_item = tk.Frame(movie_info_window, width=100, height=100)
    movie_image_item.pack(side=tk.LEFT)

    mycursor.execute("SELECT image FROM images WHERE movie_id = (%s)", [movie[0]])
    image_data = mycursor.fetchone()[0]
        
    # Convert image data to ImageTk format
    image = Image.open(io.BytesIO(image_data))
    newsize = (300, 400)
    image = image.resize(newsize)
    photo = ImageTk.PhotoImage(image)
            
    # Display movie poster image
    image_label = tk.Label(movie_image_item, image=photo)
    image_label.image = photo  # To prevent garbage collection
    image_label.pack(side=tk.LEFT)

    movie_name_label = tk.Label(movie_info_window, text="Movie Name: "+movie[1])
    movie_name_label.pack()
    movie_rating_label = tk.Label(movie_info_window, text="Rating: "+movie[2])
    movie_rating_label.pack()
    movie_Genre_label = tk.Label(movie_info_window, text="Genre: "+movie[3])
    movie_Genre_label.pack()
    movie_Year_label = tk.Label(movie_info_window, text="Year: "+str(movie[4]))
    movie_Year_label.pack()
    movie_release_label = tk.Label(movie_info_window, text="Date Of release: "+str(movie[5]))
    movie_release_label.pack()
    movie_Score_label = tk.Label(movie_info_window, text="Score: "+str(movie[6]))
    movie_Score_label.pack()
    movie_Votes_label = tk.Label(movie_info_window, text="Votes: "+str(movie[7]))
    movie_Votes_label.pack()
    movie_director_label = tk.Label(movie_info_window, text="Director: "+str(movie[8]))
    movie_director_label.pack()
    movie_Writer_label = tk.Label(movie_info_window, text="Writer: "+str(movie[9]))
    movie_Writer_label.pack()
    movie_Star_label = tk.Label(movie_info_window, text="Star: "+str(movie[10]))
    movie_Star_label.pack()
    movie_Country_label = tk.Label(movie_info_window, text="Country: "+str(movie[11]))
    movie_Country_label.pack()
    movie_Budget_label = tk.Label(movie_info_window, text="Budget: "+str(movie[12]))
    movie_Budget_label.pack()
    # Placeholder function for displaying more information about a movie
    # messagebox.showinfo("More Information", f"More information about the movie '{movie[1]}' \nRating: '{movie[2]}' \nGenre: '{movie[3]}'")

    play_button = tk.Button(movie_info_window, text="Play", command=lambda: play_movie(movie, username))
    play_button.pack()

    watchlist_button = tk.Button(movie_info_window, text="Add to Watchlist", command=lambda: add_to_watchlist(movie, username))
    watchlist_button.pack()
    # Placeholder function for displaying more information about a movie
    # messagebox.showinfo("More Information", f"More information about the movie '{movie[1]}' \nRating: '{movie[2]}' \nGenre: '{movie[3]}'")

def play_movie(movie, username):
    # Placeholder function for playing the selected movie
    mycursor.execute("CREATE TABLE IF NOT EXISTS history(id INT, movie_id INT, name text, foreign key(id) references users(id), foreign key(movie_id) references short_movies(movie_id))")
    query = "insert into history values(%s, %s, %s)"
    val = (newid[0][0], movie[0], movie[1])
    print(val)
    mycursor.execute(query, val)
    mydb.commit()
    # messagebox.showinfo("Add to History", f"Added '{movie[1]}' to the history")
    play_video()

# Function to retrieve and play video
# Function to retrieve and play video
def play_video():
    global video_id
    # Retrieve video data from the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT video FROM videos WHERE movie_id = 3")
    video_data = mycursor.fetchone()[0]
    
    # Create a temporary file to store video data
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_data)
        temp_filename = temp_file.name
    
    # Create a new Tkinter window to display the video
    video_window = tk.Toplevel(main_root)
    video_window.title("Video Player")
    
    # Load video using moviepy
    video_clip = VideoFileClip(temp_filename)

    # Function to update video frames
    def update_frame(t):
        frame = video_clip.get_frame(t)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (600, 400))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.image = photo
        video_window.after(10, update_frame, t + 0.01)  # Update every 10 milliseconds

    # Create a label to display video frames
    video_label = tk.Label(video_window)
    video_label.pack()

    # Start updating video frames
    update_frame(0)

    # Play audio using system default player
    os.system(f'start {temp_filename}')
  
def open_history(username):
    # Placeholder function for opening the history
    history_info_window = tk.Toplevel(main_root)
    history_info_window.geometry("600x400")
    history_info_window.title("My History")
    
    my_scrolling_list(history_info_window, "SELECT * FROM history where id=(%s)", True, [newid[0][0]], "history")
    
def remove_history(movie, movie_frame_item, tablename):
    print(movie)
    print([newid[0][0], movie[1]])
    query = "delete from {} where id=(%s) and movie_id=(%s)".format(tablename)
    mycursor.execute(query, [newid[0][0], movie[1]])
    mydb.commit()
    movie_frame_item.pack_forget()
    movie_frame_item.destroy()
    messagebox.showinfo("Removed", f"Removed '{movie[2]}' from {tablename}")

def add_to_watchlist(movie, username):
    mycursor.execute("SELECT * FROM watchlist where id=(%s) and movie_id=(%s)", [newid[0][0], movie[0]])
    movies = mycursor.fetchall()
    if(len(movies)==0):
        # Placeholder function for adding the selected movie to the watchlist
        mycursor.execute("CREATE TABLE IF NOT EXISTS watchlist(id INT, movie_id INT, name text, foreign key(id) references users(id), foreign key(movie_id) references short_movies(movie_id))")
        query = "insert into watchlist values(%s, %s, %s)"
        val = (newid[0][0], movie[0], movie[1])
        print(val)
        mycursor.execute(query, val)
        mydb.commit()
        messagebox.showinfo("Add to Watchlist", f"Added '{movie[1]}' to the watchlist")
    else:
        messagebox.showinfo("Already in Watchlist", f"Movie '{movie[1]}' is already in your watchlist!!!")
    main_root.withdraw()

def open_watchlist(username):
    # Placeholder function for opening the watchlist
    # Create a frame to hold movie names with scrollbar
    watchlist_info_window = tk.Toplevel(main_root)
    watchlist_info_window.geometry("600x400")
    watchlist_info_window.title("My Watchlist")
    
    my_scrolling_list(watchlist_info_window, "SELECT * FROM watchlist where id=(%s)", True, [newid[0][0]], "watchlist")

# Create Tkinter window
main_root = tk.Tk()
width = main_root.winfo_screenwidth()
height = main_root.winfo_screenheight()
main_root.geometry("%dx%d"%(width, height))
main_root.title("Movie Library Management")

# Open the image file
image_path = "C:\DBMS mini project\login.png"
image = Image.open(image_path)

# Resize the image to the desired dimensions
desired_width = 1250  # Replace with your desired width
desired_height = 700  # Replace with your desired height
resized_image = image.resize((width, height))

# Convert the resized image to a Tkinter PhotoImage object
bg = ImageTk.PhotoImage(resized_image)
# Show image using label 
label1 = tk.Label(main_root, image = bg) 
label1.place(x = 0, y = 0)

# Create a frame to contain the buttons with a transparent background
button_frame = ttk.Frame(main_root, style='Transparent.TFrame')
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a custom style for the frame to make it transparent
style = ttk.Style()
style.configure('Transparent.TFrame', background='')

admin_login_button = ttk.Button(button_frame, text="Admin", command=admin_login_window)
admin_login_button.grid(row=0, column=0, padx=5, pady=5)

user_login_button = ttk.Button(button_frame, text="User", command=user_login_window)
user_login_button.grid(row=0, column=1, padx=5, pady=5)

main_root.mainloop()