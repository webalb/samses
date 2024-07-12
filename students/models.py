# from django.db import models
# from django.contrib.auth.models import User
# from users.models import CustomUser
# # Create your models here.

# class Student(models.Model):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     other_name = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     passport_photograph = models.ImageField(upload_to='students_passport_photograph/%Y/%m/%d/')
#     admission_number = models.CharField(max_length=10,unique=True)
#     date_of_admission = models.DateField()

#     guardian_email = models.EmailField(blank=True)
#     guardian_phone_number = models.CharField(max_length=15)

#     country_of_birth = models.CharField()
#     state_of_origin = models.CharField()
#     place_of_birth = models.CharField() # LGA of birth

#     created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['admission_number'])
#         ]
        
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class TermPerformance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     term_name = models.CharField(max_length=100)
#     grade = models.CharField(max_length=2)
#     comments = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.student} - {self.term_name}"

# class Graduation(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     graduation_date = models.DateField()
#     graduation_status = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.student} - {'Graduated' if self.graduation_status else 'Not Graduated'}"
