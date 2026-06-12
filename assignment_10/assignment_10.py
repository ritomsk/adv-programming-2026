class Address:
    def __init__(self, street, city, zip_code):
        self.street = street
        self.city = city
        self.zip_code = zip_code

    def __str__(self):
        return f"{self.street}, {self.city} {self.zip_code}"

class Student:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address
        self.courses = []

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0 or value > 120:
            raise ValueError("Age must be a valid positive integer between 0 and 120.")
        self._age = value

    def add_course(self, course):
        self.courses.append(course)

    def display(self):
        course_list = ", ".join(self.courses) if self.courses else "None"
        return f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}\nCourses: {course_list}"

class ScholarshipStudent(Student):
    def __init__(self, name, age, address, scholarship_amount):
        super().__init__(name, age, address)
        self.scholarship_amount = scholarship_amount

    def display(self):
        base_display = super().display()
        return f"{base_display}\nScholarship Amount: ${self.scholarship_amount}"

if __name__ == "__main__":
    student_address = Address("123 Maple St", "Springfield", "12345")
    
    student1 = Student("Alice", 20, student_address)
    student1.add_course("Mathematics")
    student1.add_course("Physics")
    
    scholar_address = Address("456 Oak Ave", "Metropolis", "67890")
    
    scholar1 = ScholarshipStudent("Bob", 22, scholar_address, 5000)
    scholar1.add_course("Computer Science")
    scholar1.add_course("Data Structures")
    
    print("--- Standard Student ---")
    print(student1.display())
    
    print("\n--- Scholarship Student ---")
    print(scholar1.display())