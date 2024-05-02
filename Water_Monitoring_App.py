import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QFormLayout, QTextEdit, QComboBox, QMessageBox, QFrame, QDialog
import sqlite3
from PyQt6.QtCore import *
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from moderator_panel import ModeratorPanel
from role_selection import RoleSelectionDialog


class Water_Monitoring_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Water Monitoring System")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget=QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout=QVBoxLayout()
        self.central_widget.setLayout(self.layout)



        self.logo_label=QLabel()
        pixmap=QPixmap("Icon/ictu-logo.png")
        scaled_pixmap=pixmap.scaled(600, 400)
        self.logo_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.logo_label)

        self.developer_label=QLabel("Developed by: Brian")
        self.layout.addWidget(self.developer_label)


        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter the name of user")
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter the corresponding password to the user")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Connect to the SQLite database
        self.conn = sqlite3.connect("water_monitoring.db")
        self.cursor = self.conn.cursor()

    def login(self):
        username=self.username_input.text()
        password=self.password_input.text()

        # Check if the username and password match in the database
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user=self.cursor.fetchone()

        if user[1]== username and user[2] == password:
            self.show_role_selection_dialog()
        else:
            QMessageBox.warning(self, "Invalid Credentials", "Invalid username or password")


    def show_role_selection_dialog(self):
        dialog=RoleSelectionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            role=dialog.selected_role()
            if role == "Administrator":
                self.open_admin_panel()
            elif role == "Moderator":
                self.open_moderator_panel()
            elif role == "Customer":
                self.open_customer_panel()

    def open_admin_panel(self):
        # Implement the admin panel GUI and functionalities here, remeber that admin has access to moderator and customer too
        admin_panel=QWidget()
        admin_layout=QVBoxLayout()

        # Title label
        title_label=QLabel("<h2>Administrator Panel</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        admin_layout.addWidget(title_label)

        # User registration form
        user_form_layout=QFormLayout()
        self.username_reg_input=QLineEdit()
        self.password_reg_input=QLineEdit()
        self.role_reg_input=QLineEdit()
        user_form_layout.addRow("Username:", self.username_reg_input)
        user_form_layout.addRow("Password:", self.password_reg_input)
        user_form_layout.addRow("Role:", self.role_reg_input)

        register_user_button=QPushButton("Register User")
        register_user_button.clicked.connect(self.register_user)
        admin_layout.addLayout(user_form_layout)
        admin_layout.addWidget(register_user_button)

        # Water source registration form
        water_source_form_layout=QFormLayout()
        self.name_input=QLineEdit()
        self.type_input=QComboBox()
        self.type_input.addItems(["River", "Lake", "Well", "Pond", "Reservoir"])
        self.location_input=QLineEdit()
        self.condition_input=QTextEdit()
        water_source_form_layout.addRow("Name:", self.name_input)
        water_source_form_layout.addRow("Type:", self.type_input)
        water_source_form_layout.addRow("Location:", self.location_input)
        water_source_form_layout.addRow("Condition:", self.condition_input)

        register_water_source_button=QPushButton("Register Water Source")
        register_water_source_button.clicked.connect(self.register_water_source)
        admin_layout.addLayout(water_source_form_layout)
        admin_layout.addWidget(register_water_source_button)



        # Receive complaint form
        complaint_form_layout=QFormLayout()
        self.complaint_user_id_input=QLineEdit()
        self.complaint_water_source_id_input=QLineEdit()
        self.complaint_description_input=QTextEdit()
        complaint_form_layout.addRow("User ID:", self.complaint_user_id_input)
        complaint_form_layout.addRow("Water Source ID:", self.complaint_water_source_id_input)
        complaint_form_layout.addRow("Description:", self.complaint_description_input)

        # receive_complaint_button=QPushButton("Receive Complaint")
        # receive_complaint_button.clicked.connect(self.receive_complaint)
        # admin_layout.addLayout(complaint_form_layout)
        # admin_layout.addWidget(receive_complaint_button)

        # # Export water source information button
        export_button=QPushButton("Export Water Source Information")
        export_button.clicked.connect(self.export_water_sources_to_excel)
        admin_layout.addWidget(export_button)
        #
        # Send warning email button
        send_email_button=QPushButton("Send Warning Email")
        send_email_button.clicked.connect(self.send_warning_email)
        admin_layout.addWidget(send_email_button)

        admin_panel.setLayout(admin_layout)
        self.setCentralWidget(admin_panel)

    def open_moderator_panel(self):
        # Implement the moderator panel GUI and functionalities here
        self.moderator_panel=ModeratorPanel()
        self.moderator_layout=QVBoxLayout()
        self.moderator_layout.addWidget(QLabel("<h2>Moderator Panel</h2>"))
        self.moderator_panel.setLayout(self.moderator_layout)


        #Store condition button
        store_condition_button=QPushButton("Store Condition")
        store_condition_button.clicked.connect(self.store_condition)
        # we can update the water condition in the water sources table
        self.moderator_layout.addWidget(store_condition_button)



        # Fetch complaints from the database
        complaints_data=self.fetch_complaints_data()  # Implement this method to fetch complaints

        # Set complaints model in the moderator panel

        self.moderator_panel.set_complaints_data(complaints_data)



        # Show moderator panel
        self.setCentralWidget(self.moderator_panel)

    def fetch_complaints_data(self):
        self.cursor.execute("SELECT * FROM complaints")
        complaints_data=self.cursor.fetchall()
        return complaints_data




    def register_user(self):
        username=self.username_reg_input.text()
        password=self.password_reg_input.text()
        role=self.role_reg_input.text()

        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                (username, password, role))
            self.conn.commit()
            QMessageBox.information(self, "Success", "User registered successfully.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists. Please choose a different username.")

    def register_water_source(self):
        name=self.name_input.text()
        Type=self.type_input.currentText()
        location=self.location_input.text()
        condition=self.condition_input.toPlainText()

        self.cursor.execute("INSERT INTO water_sources (name, type, location, condition) VALUES (?, ?, ?, ?)",
                            (name, Type, location, condition))
        self.conn.commit()
        QMessageBox.information(self, "Success", "Water source registered successfully.")

    # def receive_complaint(self):
    #     user_id=self.complaint_user_id_input.text()
    #     water_source_id=self.complaint_water_source_id_input.text()
    #     description=self.complaint_description_input.toPlainText()
    #     self.receive_complaint_from_user(user_id, water_source_id, description)
    #
    # def receive_complaint_from_user(self, user_id, water_source_id, description):
    #     try:
    #         self.cursor.execute(
    #             "INSERT INTO complaints (user_id, water_souce_id, description, status) VALUES (?, ?, ?, 'Pending')",
    #             (user_id, water_source_id, description))
    #         self.conn.commit()
    #         QMessageBox.information(self, "Success", "Complaint received successfully.")
    #
    #     except Exception as e:
    #         QMessageBox.warning(self, "Error", f"Failed to receive complaint: {str(e)} ")

    def store_condition(self):
       # Assume you have a method to get the selected water source ID
        condition_report = self.condition_input.toPlainText()
        water_source_id=1
        self.store_water_condition(condition_report, water_source_id)



    def store_water_condition(self, water_source_id, condition_report):
        self.cursor.execute("UPDATE water_sources SET condition=? WHERE id=?", (condition_report, water_source_id))
        self.conn.commit()
        QMessageBox.information(self, "Success", "Water condition updated successfully.")

    def send_warning_email(self):
        # Fetch water source details
        self.cursor.execute("SELECT * FROM water_sources ")
        water_source_info =self.cursor.fetchone()

        if water_source_info:
            if water_source_info[4] == "Poor":  # Assuming the condition is stored in the fifth column
                # Email configuration
                sender_email="ymarcbrian@gmail.com"
                password="xtls ctif hgyy cmkl"
                receiver_email="marccoder697@gmail.com"
                subject="Warning: Poor Water Condition"
                body=f"There is a danger alert for the water source {water_source_info[1]} located at {water_source_info[3]}. Please take necessary action."

                # Create message
                message=MIMEMultipart()
                message["From"]=sender_email
                message["To"]=receiver_email
                message["Subject"]=subject
                message.attach(MIMEText(body, "plain"))

                # Send email
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())

                QMessageBox.information(self, "Email Sent", "Warning email sent to users in danger area.")
            else:
                QMessageBox.information(self, "No Warning", "Water condition is not poor. No warning email sent.")

        else:
            QMessageBox.warning(self, "Error", f"No water source found with ID: ")

    def export_water_sources_to_excel(self):
        try:
            self.cursor.execute("SELECT * FROM water_sources")
            water_sources_info=self.cursor.fetchall()

            # Create a new Excel workbook
            workbook=openpyxl.Workbook()
            sheet=workbook.active
            sheet.title="Water Sources"

            # Write header row
            sheet.append(["ID", "Name", "Type", "Location", "Condition"])

            # Write data rows
            for water_source in water_sources_info:
                sheet.append(water_source)

            # Save the workbook
            workbook.save("water_sources.xlsx")

            QMessageBox.information(self, "Success", "Water source information exported to Excel file.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export water source information: {str(e)}")


    def open_customer_panel(self):
        # Implement the customer panel GUI and functionalities here
        customer_panel=QWidget()
        customer_layout=QVBoxLayout()
        customer_layout.addWidget(QLabel("<h2>Customer Panel</h2>"))
        customer_panel.setLayout(customer_layout)
        self.setCentralWidget(customer_panel)

        complaint_form_layout=QFormLayout()
        self.complaint_user_id_input=QLineEdit()
        self.complaint_water_source_id_input=QLineEdit()
        self.complaint_description_input=QTextEdit()
        complaint_form_layout.addRow("User ID:", self.complaint_user_id_input)
        complaint_form_layout.addRow("Water Source ID:", self.complaint_water_source_id_input)
        complaint_form_layout.addRow("Description:", self.complaint_description_input)

        send_complaint_button=QPushButton("send complaint")
        send_complaint_button.clicked.connect(self.send_complaint)
        customer_layout.addLayout(complaint_form_layout)
        customer_layout.addWidget(send_complaint_button)

    # the customer sends a complaint and moderator receives and displays it in table view
    def send_complaint(self):
        user_id=self.complaint_user_id_input.text()
        water_source_id=self.complaint_water_source_id_input.text()
        description=self.complaint_description_input.toPlainText()
        self.send_complaint_from_user(user_id, water_source_id, description)

    def send_complaint_from_user(self, user_id, water_source_id, description):
        try:
            self.cursor.execute(
                "INSERT INTO complaints (user_id, water_souce_id, description, status) VALUES (?, ?, ?, 'Pending')",
                (user_id, water_source_id, description))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Complaint sent successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send complaint: {str(e)} ")



    def closeEvent(self, event):
        # Close the database connection when the application is closed
        self.conn.close()

def main():
    app=QApplication(sys.argv)
    window=Water_Monitoring_App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()