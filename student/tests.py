from django.test import TestCase

# Create your tests here.
"""
Here are 50 different document types used in primary and secondary schools:

1. **Student Records:**
    * Admission Form
    * Student Registration Form
    * Transfer Certificate
    * Birth Certificate 
    * Immunization Records
    * Progress Reports
    * Report Cards
    * Grade Sheets
    * Attendance Registers
    * Graduation Certificates
    * Leaving Certificates
    * Student Profiles
    * Medical Records 
    * Disciplinary Records
    * Extracurricular Activity Records
    * Student ID Cards

2. **Teacher Records:**
    * Teacher Contracts
    * Lesson Plans
    * Scheme of Work
    * Staff Attendance Register
    * Performance Appraisal Forms
    * Professional Development Certificates
    * Leave Applications
    * Teaching Certificates
    * Qualifications 

3. **School Administration:**
    * School Calendar
    * Timetable
    * Curriculum Guide
    * School Rules and Regulations
    * Parent-Teacher Association (PTA) Minutes
    * School Budget
    * Financial Reports
    * Inventory Lists
    * Maintenance Records
    * School Prospectus
    * Enrollment Records
    * Graduation Lists
    * School Handbook
    * Emergency Contact Information
    * Safety Procedures
    * School Policies

4. **Library Records:**
    * Library Catalog
    * Book Issue Records
    * Library Fines Records
    * Book Orders
    * Library Inventory 

5. **Examination Records:**
    * Examination Timetables
    * Question Papers 
    * Answer Scripts
    * Marking Schemes
    * Grade Distribution
    * Examination Results 
    * Moderation Reports
    * Cheating Reports

6. **Other:**
    * School Newsletter
    * Parent-Teacher Communication Logs
    * School Correspondence
    * Meeting Minutes
    * Safety Audits
    * Insurance Documents
    * Legal Documents 

This list provides a comprehensive overview of the diverse range of documents used in primary and secondary schools. The specific documents used may vary depending on the school's size, type, and location. 

Here’s a categorized list of models for extending the **Student Data Management Component (SDMC)** with a brief explanation of each:

---

### **1. Parent/Guardian Information**
1. **Guardian**  
   - Stores guardian details like name, relationship to the student, contact information, occupation, and emergency contact priority.

2. **GuardianStudentMapping**  
   - Links guardians to students, defining roles (e.g., primary guardian, financial sponsor).

---

### **2. Student Attendance**
3. **AttendanceRecord**  
   - Tracks student attendance by date, including reasons for absence and partial attendance.

4. **ExamAttendance**  
   - Tracks attendance during exams and ties it to exam metadata.

---

### **3. Behavior and Discipline Records**
5. **BehaviorRecord**  
   - Logs student behavior incidents, including offense type, date, and resolution.

6. **DisciplinaryAction**  
   - Stores details of actions taken for discipline (e.g., warnings, suspensions, or counseling sessions).

7. **RecognitionRecord**  
   - Records awards, achievements, and commendations for behavior and performance.

---

### **4. Health Records**
8. **HealthRecord**  
   - Stores health-related details such as chronic illnesses, allergies, and emergency instructions.

9. **VaccinationRecord**  
   - Tracks vaccinations, dates administered, and compliance with school health policies.

10. **HealthScreening**  
    - Logs results of periodic health check-ups.

---

### **5. Extracurricular Activities**
11. **ClubMembership**  
    - Tracks students’ involvement in clubs, societies, and extracurricular groups.

12. **SportsParticipation**  
    - Logs participation in sports, including positions held and awards won.

13. **ActivityRecognition**  
    - Tracks recognitions received for extracurricular activities.

---

### **6. Student Transfers**
14. **TransferRecord**  
    - Logs transfers with details like reason for transfer, approval status, and the destination school.

15. **ExternalTransferVerification**  
    - Handles validation of student data for transfers from schools outside SAMSES.

---

### **7. Historical Data**
16. **ArchivedStudentData**  
    - Stores historical data for students who have graduated or transferred.

17. **DataRetentionPolicy**  
    - Defines rules for how long data is retained for inactive students.

---

### **8. Academic Counseling**
18. **ProgressReport**  
    - Summarizes academic strengths, weaknesses, and advice for improvement.

19. **CounselingSession**  
    - Logs details of career or academic counseling sessions.

---

### **9. Digital Resources and Integration**
20. **DigitalResourceAccess**  
    - Tracks e-learning resources or online courses accessed by students.

21. **ExternalSystemIntegration**  
    - Stores data exchanged with external systems like admission portals or government registries.

---

### **Next Steps**
Which category would you like to begin with? We can implement **Attendance** models first, as they are foundational to student records and are often integrated with academic and disciplinary records.
"""