import os.path
import tkinter as tk
import sqlite3

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("SQLite3 Database Viewer")

        # Create labels for the textboxes
        label1 = tk.Label(master, text="Enter database name:")
        label1.pack()
        # Create textboxes for user input
        self.textbox1 = tk.Entry(master)
        self.textbox1.pack()
        self.textbox1.insert(0, "db.sqlite3")

        # Create labels for the textboxes
        label2 = tk.Label(master, text="Enter table name to view:")
        label2.pack()
        # Create textboxes for user input
        self.textbox2 = tk.Entry(master)
        self.textbox2.pack()
        self.textbox2.insert(0, "myapp_user")

        # Create a button to retrieve data
        self.button = tk.Button(master, text="Retrieve Data", command=self.retrieve_data)
        self.button.pack(pady=10)

        # Create a frame for the label
        label_frame = tk.Frame(master, bd=2, relief="solid")  # bd= kolik pixelu ma border mit
        label_frame.pack(pady=10)

        # Create a label to display the data and add it to the frame
        self.label = tk.Label(label_frame, text="")
        self.label.pack()

    def retrieve_data(self):
        # Get user input from textboxes
        input1 = self.textbox1.get() #db.sqlite3
        input2 = self.textbox2.get() #myapp_user
        # Create a connection to the database
        if os.path.exists(input1):
            self.conn = sqlite3.connect(input1)

            # Create a cursor to execute SQL queries
            self.cursor = self.conn.cursor()
            try:
                # Execute a SELECT query
                self.cursor.execute(f"SELECT * FROM {input2}")

                # Fetch all the results
                results = self.cursor.fetchall()

                # Display the results in the label
                self.label.config(text=f"** Found database and table **\n\n{results}")
            except:
                self.label.config(text=f"Database loaded, but table NOT found!\nEntered TABLE: {input2}")
        else:
            self.label.config(text=f"Database NOT found!\nEntered DATABASE: {input1}")

# Create the Tkinter window and start the event loop
root = tk.Tk()

# Set the size of the window to half of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width / 2)
window_height = int(screen_height / 2)
window_x = int((screen_width - window_width) / 2)
window_y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

app = App(root)
root.mainloop()

# Close the database connection
app.conn.close()
