import tkinter as tk
from tkinter import filedialog, messagebox
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

engine = create_engine('sqlite:///patient_records.db')
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    date = Column(Date)
    gender = Column(String)
    diagnosis = Column(String)
    treatment_plan = Column(String)
    relevant_doctor = Column(String)
    diagnostic_report = Column(LargeBinary)
    medical_history = Column(LargeBinary)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class PatientRecordManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Patient Record Management System")
        self.master.geometry("800x500")

        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        self.age_label = tk.Label(master, text="Age:")
        self.age_label.grid(row=0, column=2)
        self.age_entry = tk.Entry(master)
        self.age_entry.grid(row=0, column=3)

        self.date_label = tk.Label(master, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=1, column=0)
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=1, column=1)

        self.gender_label = tk.Label(master, text="Gender:")
        self.gender_label.grid(row=1, column=2)
        self.gender_entry = tk.Entry(master)
        self.gender_entry.grid(row=1, column=3)

        self.diagnosis_label = tk.Label(master, text="Diagnosis:")
        self.diagnosis_label.grid(row=2, column=0)
        self.diagnosis_entry = tk.Entry(master)
        self.diagnosis_entry.grid(row=2, column=1)

        self.treatment_plan_label = tk.Label(master, text="Treatment Plan:")
        self.treatment_plan_label.grid(row=2, column=2)
        self.treatment_plan_entry = tk.Entry(master)
        self.treatment_plan_entry.grid(row=2, column=3)

        self.relevant_doctor_label = tk.Label(master, text="Relevant Doctor:")
        self.relevant_doctor_label.grid(row=3, column=0)
        self.relevant_doctor_entry = tk.Entry(master)
        self.relevant_doctor_entry.grid(row=3, column=1)

        self.search_label = tk.Label(master, text="Search by Name:")
        self.search_label.grid(row=3, column=2)
        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=3, column=3)

        self.entry_fields = [
            self.name_entry,
            self.age_entry,
            self.date_entry,
            self.gender_entry,
            self.diagnosis_entry,
            self.treatment_plan_entry,
            self.relevant_doctor_entry,
            self.search_entry
        ]

        for i, entry_field in enumerate(self.entry_fields):
            entry_field.bind('<Return>', lambda event, index=i+1: self.focus_next_entry(event, index))

        self.search_button = tk.Button(master, text="Search", command=self.search_record)
        self.search_button.grid(row=4, column=0, columnspan=4)

        self.diagnostic_report_button = tk.Button(master, text="Upload Diagnostic Report", command=self.upload_diagnostic_report)
        self.diagnostic_report_button.grid(row=5, column=0)

        self.medical_history_button = tk.Button(master, text="Upload Medical History", command=self.upload_medical_history)
        self.medical_history_button.grid(row=5, column=1)

        self.add_button = tk.Button(master, text="Add Record", command=self.add_record)
        self.add_button.grid(row=6, column=0)

        self.update_button = tk.Button(master, text="Update Record", command=self.update_record)
        self.update_button.grid(row=6, column=1)

        self.delete_button = tk.Button(master, text="Delete Record", command=self.delete_record)
        self.delete_button.grid(row=6, column=2)

        self.export_button = tk.Button(master, text="Export Records", command=self.export_records)
        self.export_button.grid(row=6, column=3)

    def upload_diagnostic_report(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "rb") as file:
                file_content = file.read()
            messagebox.showinfo("Success", "Diagnostic Report uploaded successfully!")
            return file_content
        else:
            messagebox.showerror("Error", "No file selected.")
            return None

    def upload_medical_history(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "rb") as file:
                file_content = file.read()
            messagebox.showinfo("Success", "Medical History uploaded successfully!")
            return file_content
        else:
            messagebox.showerror("Error", "No file selected.")
            return None

    def add_record(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        date = self.date_entry.get()
        gender = self.gender_entry.get()
        diagnosis = self.diagnosis_entry.get()
        treatment_plan = self.treatment_plan_entry.get()
        relevant_doctor = self.relevant_doctor_entry.get()

        new_patient = Patient(name=name, age=age, date=date, gender=gender, diagnosis=diagnosis, treatment_plan=treatment_plan, relevant_doctor=relevant_doctor)
        session.add(new_patient)
        session.commit()

        with open('patient_records.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, age, date, gender, diagnosis, treatment_plan, relevant_doctor])

        messagebox.showinfo("Success", "Patient record added successfully!")
        self.clear_entries()

    def update_record(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        date = self.date_entry.get()
        gender = self.gender_entry.get()
        diagnosis = self.diagnosis_entry.get()
        treatment_plan = self.treatment_plan_entry.get()
        relevant_doctor = self.relevant_doctor_entry.get()

        patient_id = selected_patient_id  # You need to define selected_patient_id or pass it as an argument
        patient = session.query(Patient).filter_by(id=patient_id).first()
        patient.name = name
        patient.age = age
        patient.date = date
        patient.gender = gender
        patient.diagnosis = diagnosis
        patient.treatment_plan = treatment_plan
        patient.relevant_doctor = relevant_doctor

        session.commit()
        messagebox.showinfo("Success", "Patient record updated successfully!")
        self.clear_entries()

    def delete_record(self):
        name = self.search_entry.get()
        patient = session.query(Patient).filter_by(name=name).first()
        if patient:
            session.delete(patient)
            session.commit()
            messagebox.showinfo("Success", "Patient record deleted successfully!")
            self.clear_entries()
        else:
            messagebox.showinfo("Delete Record", "No patient found with that name.")

    def export_records(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Age", "Date", "Gender", "Diagnosis", "Treatment Plan", "Relevant Doctor"])
                patients = session.query(Patient).all()
                for patient in patients:
                    writer.writerow([patient.name, patient.age, patient.date, patient.gender, patient.diagnosis, patient.treatment_plan, patient.relevant_doctor])
            messagebox.showinfo("Success", "Records exported to CSV successfully!")
        else:
            messagebox.showerror("Error", "No file selected.")

    def search_record(self):
        search_name = self.search_entry.get()
        patient = session.query(Patient).filter_by(name=search_name).first()
        if patient:
            info_message = f"Name: {patient.name}\nAge: {patient.age}\nDate: {patient.date}\nGender: {patient.gender}\nDiagnosis: {patient.diagnosis}\nTreatment Plan: {patient.treatment_plan}\nRelevant Doctor: {patient.relevant_doctor}"
            messagebox.showinfo("Search Result", info_message)
        else:
            messagebox.showinfo("Search Result", "Patient not found")
            
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)
        self.treatment_plan_entry.delete(0, tk.END)
        self.relevant_doctor_entry.delete(0, tk.END)

    def focus_next_entry(self, event, index):
        if index < len(self.entry_fields):
            value = self.entry_fields[index - 1].get()
            if value:
                session.add(Patient(name=value))  # Assuming the entered value is the name of the patient
                session.commit()

                with open('patient_records.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([value])

            self.entry_fields[index].focus_set()
        else:
            self.add_record()

root = tk.Tk()
my_gui = PatientRecordManagementSystem(root)
root.mainloop()