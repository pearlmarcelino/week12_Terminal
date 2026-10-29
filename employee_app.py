# Part 1: Django setup and imports 
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import tkinter as tk
from tkinter import messagebox
from employees.models import Employee 
employee_ids = []


# Part 2: callback functions 
def refresh_list():
    """Reload all employees from the database into the listbox."""
    listbox.delete(0, tk.END)
    employee_ids.clear()
    for emp in Employee.objects.all():
        listbox.insert(
            tk.END, f"{emp.name} | {emp.position} | {emp.date_hired:%Y-%m-%d}"
        )
        employee_ids.append(emp.id)


def clear_fields():
    """Empty both entry boxes and put the cursor back on Name."""
    name_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)
    name_entry.focus()


def add_employee():
    """Validate the input, save a new Employee, then refresh the list."""
    name = name_entry.get().strip()
    position = position_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Name cannot be blank.")
    elif not position:
        messagebox.showerror("Error", "Position cannot be blank.")
    elif len(name) > 100:
        messagebox.showerror("Error", "Name is too long (max 100 characters).")
    elif len(position) > 100:
        messagebox.showerror("Error", "Position is too long (max 100 characters).")
    else:
        Employee.objects.create(name=name, position=position)
        clear_fields()
        refresh_list()
        messagebox.showinfo("Success", f"Employee '{name}' was added successfully.")


def delete_employee():
    """Delete the employee selected in the listbox (after confirming)."""
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select an employee to delete.")
    else:
        emp_id = employee_ids[selection[0]]
        if messagebox.askyesno("Confirm delete", "Delete the selected employee?"):
            emp = Employee.objects.get(id=emp_id)
            emp_name = emp.name
            emp.delete()
            refresh_list()
            messagebox.showinfo("Success", f"Employee '{emp_name}' was deleted successfully.")


# Part 3: the window and widgets 
PINK = "#ffc0da"       
DARK_PINK = "#ff69b4"  

root = tk.Tk()
root.title("Employee Management System")
root.geometry("650x500")
root.minsize(450, 350)
root.configure(bg=PINK)

root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

tk.Label(root, text="Name:", bg=PINK, font=("Arial", 12)).grid(
    row=0, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Position:", bg=PINK, font=("Arial", 12)).grid(
    row=1, column=0, padx=10, pady=10, sticky="e")
position_entry = tk.Entry(root, font=("Arial", 12))
position_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Row of buttons; each button column shares the width equally
button_frame = tk.Frame(root, bg=PINK)
button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
for col in range(4):
    button_frame.columnconfigure(col, weight=1)

button_style = {"bg": DARK_PINK, "fg": "white", "font": ("Arial", 11, "bold")}
tk.Button(button_frame, text="Add Employee", command=add_employee, **button_style).grid(
    row=0, column=0, padx=3, sticky="ew")
tk.Button(button_frame, text="Refresh List", command=refresh_list, **button_style).grid(
    row=0, column=1, padx=3, sticky="ew")
tk.Button(button_frame, text="Clear Fields", command=clear_fields, **button_style).grid(
    row=0, column=2, padx=3, sticky="ew")
tk.Button(button_frame, text="Delete Employee", command=delete_employee, **button_style).grid(
    row=0, column=3, padx=3, sticky="ew")

tk.Label(root, text="Employees (select one to delete):", bg=PINK,
         font=("Arial", 11)).grid(row=3, column=0, columnspan=2, padx=10, sticky="w")

list_frame = tk.Frame(root, bg=PINK)
list_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
list_frame.columnconfigure(0, weight=1)
list_frame.rowconfigure(0, weight=1)

listbox = tk.Listbox(list_frame, font=("Arial", 12))
listbox.grid(row=0, column=0, sticky="nsew")

scrollbar = tk.Scrollbar(list_frame, command=listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)


# Part 4: start
refresh_list()    
root.mainloop()    