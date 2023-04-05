###################################
# Author: Ondrej Tomasek
# Programmed by: Ondrej Tomasek
# LinkedIn: linkedin.com/in/ondrat
# Date(DD.MM.YYYY): 04.04.2023
###################################
# Please read README.txt before use
###################################

####################################### IMPORTS #######################################

import os.path
import tkinter as tk
import sqlite3

####################################### APP ###########################################
class App:
    def __init__(self, master):
        # setup window and fonts
        self.master = master
        self.master.title("SQLite3 Database Viewer by linkedin.com/in/ondrat")
        #self.master.configure(bg="grey")
        # Set up fonts
        font_label = ("Arial", 12)
        font_textbox = ("Arial", 10)

        # Create labels for the textboxes
        label1 = tk.Label(master, text="Enter database name:", font=font_label, fg="#333333")
        label1.pack(pady=10)

        # Create textboxes for user input
        self.textbox1 = tk.Entry(master, font=font_textbox, bd=0, bg="#F2F2F2", highlightthickness=2,
                                 highlightbackground="#CCCCCC", highlightcolor="#CCCCCC", relief="solid", justify="center")
        self.textbox1.pack(ipady=5, padx=20, pady=10)
        self.textbox1.insert(0, "db.sqlite3")
        self.textbox1.config(width=int(window_width / 20))

        # Create label and entry widgets
        label2 = tk.Label(master, text="Enter table name to view:", font=font_label, fg="#333333")
        self.textbox2 = tk.Entry(master, font=font_textbox, bd=0, bg="#F2F2F2", highlightthickness=2,
                                 highlightbackground="#CCCCCC", highlightcolor="#CCCCCC", relief="solid", justify="center")
        self.textbox2.insert(0, "myapp_user")
        self.textbox2.config(width=int(window_width / 20))

        # Place label and entry widgets side by side
        label2.pack(pady=10)
        self.textbox2.pack(ipady=5, padx=20, pady=10)

        # Create the "Or lookup available TABLES" label and checkbox
        label4 = tk.Label(master, text="Or lookup available TABLES:", font=font_label, fg="#333333")
        # create an IntVar to represent the state of the checkbox
        global checkbox_state
        checkbox_state = tk.IntVar()

        def checkbox_status():
            # check the state of the checkbox
            if checkbox_state.get() == 1:
                self.textbox2.config(state="disabled")
                #self.textbox3.config(state="disabled")
            else:
                self.textbox2.config(state="normal")
                #self.textbox3.config(state="normal")

        self.checkbox = tk.Checkbutton(master, variable=checkbox_state, command=checkbox_status, selectcolor="#FFFFFF")

        # Place the label and checkbox below the first row
        label4.pack(pady=10)
        self.checkbox.pack()

        ## Create labels for the textboxes
        #label3 = tk.Label(master, text="Enter command to execute:", font=font_label, fg="#333333")
        #label3.pack()
        ## Create textboxes for user input
        #self.textbox3 = tk.Entry(master, font=font_textbox, bd=0, bg="#F2F2F2", highlightthickness=2,
        #                         highlightbackground="#CCCCCC", highlightcolor="#CCCCCC", relief="solid", justify="center")
        #self.textbox3.pack(ipady=5, padx=20, pady=10)
        #self.textbox3.insert(0, f"SELECT * FROM {self.textbox2.get()}")
        #self.textbox3.config(width=int(window_width / 20))

        # Create a button to retrieve data
        self.button = tk.Button(master, text="Retrieve Data", command=self.retrieve_data, bg="#4CAF50", fg="white", borderwidth=0, relief="solid", padx=10, pady=5, activebackground="#00661b")
        self.button.pack(pady=10)

        # Create a frame for the label
        label_frame = tk.Frame(master, bd=2, relief="solid")  # bd= kolik pixelu ma border mit
        label_frame.pack(pady=10)

        # Create a Text widget to display the data and add it to the frame
        self.text = tk.Text(label_frame, wrap="word", font=font_label, fg="#333333")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.config(state="disabled")  # Disable editing of the Text widget

        # Create a scrollbar and attach it to the Text widget
        scrollbar = tk.Scrollbar(label_frame, orient="vertical", command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

    def retrieve_data(self):
        # Get user input from textboxes
        input1 = self.textbox1.get()  # db.sqlite3
        input2 = self.textbox2.get()  # myapp_user
        # Create a connection to the database
        if os.path.exists(input1):
            self.conn = sqlite3.connect(input1)
            # Create a cursor to execute SQL queries
            self.cursor = self.conn.cursor()
            try:
                # try to gain access to the database
                if checkbox_state.get() == 1:
                    try:
                        # try to get tables
                        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = self.cursor.fetchall()
                        table_names = [table[0] for table in tables]
                        self.text.config(state="normal")  # Enable editing of the Text widget
                        self.text.delete("1.0", "end")
                        self.text.insert("end", f"** All tables in database **\n\n{' || '.join(table_names)}")
                        self.text.config(state="disabled")

                    except:
                        self.text.config(state="normal")  # Enable editing of the Text widget
                        self.text.delete("1.0", "end")
                        self.text.insert("end", f"No tables found!")
                        self.text.config(state="disabled")
                else:
                    # Execute a SELECT query
                    self.cursor.execute(f"SELECT * FROM {self.textbox2.get()}")

                    # Fetch all the results
                    results = self.cursor.fetchall()
                    # Format the results string with newline separator
                    results_str = "\n".join([str(t) for t in results])

                    # Display the results in the Text widget
                    self.text.config(state="normal")  # Enable editing of the Text widget
                    self.text.delete("1.0", "end")
                    self.text.insert("end", f"** Found database and table **\n\n{results_str}")
                    self.text.config(state="disabled")
            except:
                self.text.config(state="normal")  # Enable editing of the Text widget
                self.text.delete("1.0", "end")
                self.text.insert("end", f"Database loaded, but table NOT found!\n\n+ Entered TABLE: {input2}")
                self.text.config(state="disabled")
        else:
            self.text.config(state="normal")  # Enable editing of the Text widget
            self.text.delete("1.0", "end")
            self.text.insert("end", f"Database NOT found!\n\n+ Entered DATABASE: {input1}")
            self.text.config(state="disabled")

####################################### TKINTER MAIN WINDOW ##################################
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
