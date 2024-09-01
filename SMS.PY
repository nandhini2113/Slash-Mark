import sys
import mysql.connector
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, QDialog, QWidget, \
    QPushButton, QApplication, QMainWindow, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import QCoreApplication

class DBHelper():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='sdms'
        )
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS student(
                sid INTEGER,
                Sname TEXT,
                dept INTEGER,
                year INTEGER,
                course_a INTEGER,
                course_b INTEGER,
                course_c INTEGER
            )
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS faculty(
                fid INTEGER,
                f_name TEXT,
                course INTEGER,
                dept INTEGER,
                class_room INTEGER
            )
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Course(
                cid INTEGER,
                c_name TEXT,
                faculty TEXT,
                credit INTEGER,
                type INTEGER,
                slot INTEGER,
                No_enrolled INTEGER
            )
        """)

    def addStudent(self, sid, Sname, dept, year, course_a, course_b, course_c):
        try:
            self.c.execute(
                "INSERT INTO student (sid, Sname, dept, year, course_a, course_b, course_c) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (sid, Sname, dept, year, course_a, course_b, course_c)
            )
            self.conn.commit()
            QMessageBox.information(None, 'Successful', 'Student is added successfully to the database.')
        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Could not add student to the database. Error: {e}')
        finally:
            self.c.close()
            self.conn.close()

    def searchStudent(self, sid):
        try:
            self.c.execute("SELECT * from student WHERE sid=%s", (sid,))
            self.data = self.c.fetchone()

            if not self.data:
                QMessageBox.warning(None, 'Error', 'Could not find any student with roll no ' + str(sid))
                return None
            self.list = []
            for i in range(0, 7):
                self.list.append(self.data[i])
            showStudent(self.list)
        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Error searching student: {e}')
        finally:
            self.c.close()
            self.conn.close()

    def deleteRecord(self, sid):
        try:
            self.c.execute("DELETE FROM student WHERE sid=%s", (sid,))
            self.conn.commit()
            if self.c.rowcount == 0:
                QMessageBox.warning(None, 'Error', 'No student found with roll no ' + str(sid))
            else:
                QMessageBox.information(None, 'Successful', 'Student is deleted from the database.')
        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Could not delete student from the database. Error: {e}')
        finally:
            self.c.close()
            self.conn.close()



class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.userNameLabel = QLabel("Username")
        self.userPassLabel = QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName, 1, 2)
        layout.addWidget(self.textPass, 2, 2)
        layout.addWidget(self.buttonLogin, 3, 1, 1, 2)

        self.setWindowTitle("Login")

    def handleLogin(self):
        if (self.textName.text() == '' and self.textPass.text() == ''):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')

def showStudent(list):
    sid = list[0]
    sname = list[1]
    dept = ["Mechanical Engineering", "Chemical Engineering", "Software Engineering", "Biotech Engineering", "Computer Science and Engineering", "Information Technology"][list[2]]
    year = ["1st", "2nd", "3rd", "4th"][list[3]]
    courses = ["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE", "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS", "MOBILE APP"]
    course_a = courses[list[4]]
    course_b = courses[list[5]]
    course_c = courses[list[6]]

    table = QTableWidget()
    tableItem = QTableWidgetItem()
    table.setWindowTitle("Student Details")
    table.setRowCount(7)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Roll"))
    table.setItem(0, 1, QTableWidgetItem(str(sid)))
    table.setItem(1, 0, QTableWidgetItem("Name"))
    table.setItem(1, 1, QTableWidgetItem(str(sname)))
    table.setItem(2, 0, QTableWidgetItem("Department"))
    table.setItem(2, 1, QTableWidgetItem(str(dept)))
    table.setItem(3, 0, QTableWidgetItem("Year"))
    table.setItem(3, 1, QTableWidgetItem(str(year)))
    table.setItem(4, 0, QTableWidgetItem("Slot A"))
    table.setItem(4, 1, QTableWidgetItem(str(course_a)))
    table.setItem(5, 0, QTableWidgetItem("Slot B"))
    table.setItem(5, 1, QTableWidgetItem(str(course_b)))
    table.setItem(6, 0, QTableWidgetItem("Slot C"))
    table.setItem(6, 1, QTableWidgetItem(str(course_c)))
    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog = QDialog()
    dialog.setWindowTitle("Student Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

class AddStudent(QDialog):
    def __init__(self):
        super().__init__()

        self.dept = -1
        self.year = -1
        self.sid = -1
        self.sname = ""
        self.course_a = -1
        self.course_b = -1
        self.course_c = -1

        self.btnCancel = QPushButton("Cancel", self)
        self.btnReset = QPushButton("Reset", self)
        self.btnAdd = QPushButton("Add", self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.yearCombo = QComboBox(self)
        self.yearCombo.addItems(["1st", "2nd", "3rd", "4th"])      

        self.branchCombo = QComboBox(self)
        self.branchCombo.addItems(["Mechanical", "Chemical", "Software", "Biotech", "Computer Science", "Information Technology"])

        self.cACombo = QComboBox(self)
        self.cACombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE", "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS"])

        self.cBCombo = QComboBox(self)
        self.cBCombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE", "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS"])

        self.cCCombo = QComboBox(self)
        self.cCCombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE", "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS", "MOBILE APP"])

        self.rollLabel = QLabel("Roll No")
        self.nameLabel = QLabel("Name")
        self.cALabel = QLabel("Slot A")
        self.yearLabel = QLabel("Current Year")
        self.cBLabel = QLabel("Slot B")
        self.branchLabel = QLabel("Branch")
        self.cCLabel = QLabel("Slot C")
   
        self.rollText = QLineEdit(self)
        self.nameText = QLineEdit(self)

        self.setGeometry(300, 100, 500, 400)
        self.setWindowTitle("Student Registration")

        layout = QGridLayout()
        layout.addWidget(self.rollLabel, 1, 0)
        layout.addWidget(self.rollText, 1, 1, 1, 2)
        layout.addWidget(self.nameLabel, 2, 0)
        layout.addWidget(self.nameText, 2, 1, 1, 2)
        layout.addWidget(self.branchLabel, 3, 0)
        layout.addWidget(self.branchCombo, 3, 1, 1, 2)
        layout.addWidget(self.yearLabel, 4, 0)
        layout.addWidget(self.yearCombo, 4, 1, 1, 2)
        layout.addWidget(self.cALabel, 5, 0)
        layout.addWidget(self.cACombo, 5, 1, 1, 2)
        layout.addWidget(self.cBLabel, 6, 0)
        layout.addWidget(self.cBCombo, 6, 1, 1, 2)
        layout.addWidget(self.cCLabel, 7, 0)
        layout.addWidget(self.cCCombo, 7, 1, 1, 2)

        layout.addWidget(self.btnCancel, 8, 2)
        layout.addWidget(self.btnReset, 8, 1)
        layout.addWidget(self.btnAdd, 8, 0)

        self.setLayout(layout)

        self.btnAdd.clicked.connect(self.addStudent)
        self.btnReset.clicked.connect(self.reset_fields)

    def reset_fields(self):
        self.rollText.clear()
        self.nameText.clear()
        self.yearCombo.setCurrentIndex(0)
        self.branchCombo.setCurrentIndex(0)
        self.cACombo.setCurrentIndex(0)
        self.cBCombo.setCurrentIndex(0)
        self.cCCombo.setCurrentIndex(0)

    def addStudent(self):
        self.sid = self.rollText.text()
        self.sname = self.nameText.text()
        self.dept = self.branchCombo.currentIndex()
        self.year = self.yearCombo.currentIndex()
        self.course_a = self.cACombo.currentIndex()
        self.course_b = self.cBCombo.currentIndex()
        self.course_c = self.cCCombo.currentIndex()
        db = DBHelper()
        db.addStudent(self.sid, self.sname, self.dept, self.year, self.course_a, self.course_b, self.course_c)

class SearchStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.sid = ""
        self.lbl = QLabel("Enter the roll no of the student to be searched")
        self.btnSearch = QPushButton("Search")
        self.editField = QLineEdit(self)
        self.btnSearch.clicked.connect(self.searchStudent)
        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl)
        layout.addWidget(self.editField)
        layout.addWidget(self.btnSearch)
        self.setWindowTitle("Student Registration")

    def searchStudent(self):
        self.sid = self.editField.text()
        if self.editField.text() == "":
            QMessageBox.warning(self, 'Error', 'Please enter the roll number')
            return None
        db = DBHelper()
        db.searchStudent(self.sid)

class DeleteStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.sid = ""
        self.lbl = QLabel("Enter the roll no of the student to be deleted")
        self.btnDelete = QPushButton("Delete")
        self.editField = QLineEdit(self)
        self.btnDelete.clicked.connect(self.deleteRecord)
        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl)
        layout.addWidget(self.editField)
        layout.addWidget(self.btnDelete)
        self.setWindowTitle("Student Registration")

    def deleteRecord(self):
        self.sid = self.editField.text()
        if self.editField.text() == "":
            QMessageBox.warning(self, 'Error', 'Please enter the roll number')
            return None
        db = DBHelper()
        db.deleteRecord(self.sid)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 100, 500, 400)
        self.form_widget = Main(self)
        self.setCentralWidget(self.form_widget)
        self.setWindowTitle("Student Database Management System")
        self.show()

class Main(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.lbl = QLabel("Student Database Management System", self)
        self.lbl.setFont(QtGui.QFont("Sanserif", 20))

        self.btnAdd = QPushButton("Add Student", self)
        self.btnSearch = QPushButton("Search Student", self)
        self.btnDelete = QPushButton("Delete Student", self)
        self.btnAdd.setFixedHeight(50)
        self.btnSearch.setFixedHeight(50)
        self.btnDelete.setFixedHeight(50)

        layout.addWidget(self.lbl)
        layout.addWidget(self.btnAdd)
        layout.addWidget(self.btnSearch)
        layout.addWidget(self.btnDelete)
        layout.addStretch()

        self.setLayout(layout)
        self.btnAdd.clicked.connect(self.addStudent)
        self.btnSearch.clicked.connect(self.searchStudent)
        self.btnDelete.clicked.connect(self.deleteStudent)

    def addStudent(self):
        addStudent = AddStudent()
        addStudent.exec()

    def searchStudent(self):
        searchStudent = SearchStudent()
        searchStudent.exec()

    def deleteStudent(self):
        deleteStudent = DeleteStudent()
        deleteStudent.exec()

def main():
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
