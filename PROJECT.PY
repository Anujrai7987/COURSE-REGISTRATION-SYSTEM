import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class CourseRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Registration System")
        self.root.geometry("900x700")
        self.root.config(bg="#f5f5f5")
        
        # Data storage
        self.available_courses = {
            "CS101": {"name": "Introduction to Programming", "credits": 3, "seats": 30, "enrolled": 0},
            "CS201": {"name": "Data Structures", "credits": 4, "seats": 25, "enrolled": 0},
            "CS301": {"name": "Database Systems", "credits": 3, "seats": 20, "enrolled": 0},
            "MA101": {"name": "Calculus I", "credits": 4, "seats": 35, "enrolled": 0},
            "MA201": {"name": "Linear Algebra", "credits": 3, "seats": 30, "enrolled": 0},
            "PH101": {"name": "Physics I", "credits": 4, "seats": 25, "enrolled": 0},
            "EN101": {"name": "English Composition", "credits": 3, "seats": 40, "enrolled": 0},
            "HI101": {"name": "World History", "credits": 3, "seats": 35, "enrolled": 0}
        }
        
        self.registered_courses = []
        self.student_name = ""
        self.student_id = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="🎓 Course Registration System", 
                        font=("Arial", 24, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Student Info
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), expand=True)
        
        # Student Information
        info_label = tk.Label(left_panel, text="Student Information", 
                             font=("Arial", 14, "bold"), bg="white")
        info_label.pack(pady=10)
        
        info_frame = tk.Frame(left_panel, bg="white")
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(info_frame, text="Student Name:", font=("Arial", 10), 
                bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(info_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(info_frame, text="Student ID:", font=("Arial", 10), 
                bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.id_entry = tk.Entry(info_frame, font=("Arial", 10), width=25)
        self.id_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Available Courses
        courses_label = tk.Label(left_panel, text="Available Courses", 
                                font=("Arial", 14, "bold"), bg="white")
        courses_label.pack(pady=(20, 10))
        
        # Treeview for courses
        tree_frame = tk.Frame(left_panel, bg="white")
        tree_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.course_tree = ttk.Treeview(tree_frame, columns=("Name", "Credits", "Seats"), 
                                       show="tree headings", yscrollcommand=scrollbar.set)
        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)
        
        # Configure columns
        self.course_tree.column("#0", width=80)
        self.course_tree.column("Name", width=200)
        self.course_tree.column("Credits", width=60)
        self.course_tree.column("Seats", width=80)
        
        self.course_tree.heading("#0", text="Code")
        self.course_tree.heading("Name", text="Course Name")
        self.course_tree.heading("Credits", text="Credits")
        self.course_tree.heading("Seats", text="Available")
        
        self.populate_course_tree()
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg="white")
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Register Course", command=self.register_course,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                 width=15, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Drop Course", command=self.drop_course,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                 width=15, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Right panel - Registered Courses
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        reg_label = tk.Label(right_panel, text="My Registered Courses", 
                            font=("Arial", 14, "bold"), bg="white")
        reg_label.pack(pady=10)
        
        # Registered courses listbox
        list_frame = tk.Frame(right_panel, bg="white")
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        reg_scrollbar = tk.Scrollbar(list_frame)
        reg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.registered_listbox = tk.Listbox(list_frame, font=("Arial", 10),
                                            yscrollcommand=reg_scrollbar.set,
                                            height=15, bg="#ecf0f1")
        self.registered_listbox.pack(fill=tk.BOTH, expand=True)
        reg_scrollbar.config(command=self.registered_listbox.yview)
        
        # Summary
        summary_frame = tk.Frame(right_panel, bg="white")
        summary_frame.pack(pady=15, padx=20, fill=tk.X)
        
        self.total_credits_label = tk.Label(summary_frame, text="Total Credits: 0", 
                                           font=("Arial", 11, "bold"), bg="white")
        self.total_credits_label.pack(anchor=tk.W, pady=3)
        
        self.total_courses_label = tk.Label(summary_frame, text="Total Courses: 0", 
                                           font=("Arial", 11, "bold"), bg="white")
        self.total_courses_label.pack(anchor=tk.W, pady=3)
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg="white")
        action_frame.pack(pady=15)
        
        tk.Button(action_frame, text="Submit Registration", command=self.submit_registration,
                 bg="#3498db", fg="white", font=("Arial", 11, "bold"), 
                 width=18, cursor="hand2").pack(pady=5)
        
        tk.Button(action_frame, text="Clear All", command=self.clear_all,
                 bg="#95a5a6", fg="white", font=("Arial", 11, "bold"), 
                 width=18, cursor="hand2").pack(pady=5)
        
    def populate_course_tree(self):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
            
        for code, info in self.available_courses.items():
            available = info['seats'] - info['enrolled']
            self.course_tree.insert("", tk.END, text=code, 
                                   values=(info['name'], info['credits'], 
                                          f"{available}/{info['seats']}"))
    
    def register_course(self):
        if not self.name_entry.get() or not self.id_entry.get():
            messagebox.showwarning("Warning", "Please enter student name and ID!")
            return
            
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to register!")
            return
        
        course_code = self.course_tree.item(selected[0])['text']
        
        if course_code in self.registered_courses:
            messagebox.showinfo("Info", "You are already registered for this course!")
            return
        
        course = self.available_courses[course_code]
        if course['enrolled'] >= course['seats']:
            messagebox.showerror("Error", "This course is full!")
            return
        
        # Check credit limit (max 18 credits)
        total_credits = sum(self.available_courses[c]['credits'] for c in self.registered_courses)
        if total_credits + course['credits'] > 18:
            messagebox.showwarning("Warning", "Cannot exceed 18 credits per semester!")
            return
        
        self.registered_courses.append(course_code)
        course['enrolled'] += 1
        
        course_info = f"{course_code} - {course['name']} ({course['credits']} credits)"
        self.registered_listbox.insert(tk.END, course_info)
        
        self.populate_course_tree()
        self.update_summary()
        
        messagebox.showinfo("Success", f"Successfully registered for {course['name']}!")
    
    def drop_course(self):
        selected = self.registered_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to drop!")
            return
        
        course_info = self.registered_listbox.get(selected[0])
        course_code = course_info.split(" - ")[0]
        
        self.registered_courses.remove(course_code)
        self.available_courses[course_code]['enrolled'] -= 1
        self.registered_listbox.delete(selected[0])
        
        self.populate_course_tree()
        self.update_summary()
        
        messagebox.showinfo("Success", f"Successfully dropped {course_code}!")
    
    def update_summary(self):
        total_credits = sum(self.available_courses[c]['credits'] for c in self.registered_courses)
        total_courses = len(self.registered_courses)
        
        self.total_credits_label.config(text=f"Total Credits: {total_credits}")
        self.total_courses_label.config(text=f"Total Courses: {total_courses}")
    
    def submit_registration(self):
        if not self.registered_courses:
            messagebox.showwarning("Warning", "No courses registered!")
            return
        
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        
        if not name or not student_id:
            messagebox.showwarning("Warning", "Please enter student name and ID!")
            return
        
        total_credits = sum(self.available_courses[c]['credits'] for c in self.registered_courses)
        
        confirmation = f"Student: {name}\nID: {student_id}\n\n"
        confirmation += "Registered Courses:\n"
        for code in self.registered_courses:
            course = self.available_courses[code]
            confirmation += f"- {code}: {course['name']} ({course['credits']} credits)\n"
        confirmation += f"\nTotal: {len(self.registered_courses)} courses, {total_credits} credits"
        confirmation += f"\n\nSubmit registration?"
        
        if messagebox.askyesno("Confirm Registration", confirmation):
            messagebox.showinfo("Success", "Registration submitted successfully!\n\nCheck your email for confirmation.")
    
    def clear_all(self):
        if not self.registered_courses:
            return
            
        if messagebox.askyesno("Confirm", "Clear all registered courses?"):
            for code in self.registered_courses:
                self.available_courses[code]['enrolled'] -= 1
            
            self.registered_courses.clear()
            self.registered_listbox.delete(0, tk.END)
            self.populate_course_tree()
            self.update_summary()

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseRegistrationSystem(root)
    root.mainloop()