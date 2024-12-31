from django.db import models

from schools.models import School

class SchoolFeedback(models.Model):
    """
    Model for handling feedback or complaints about a school.
    """
    ROLE_CHOICES = [
        ('Staff', 'Staff'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
        ('Public Individual', 'Public Individual'),
        ('Organization', 'Organization'),
        ('Anonymous', 'Anonymous'),
    ]

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        help_text="The school this feedback is associated with."
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Role of the person providing feedback."
    )
    feedback_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Name of the person providing feedback (optional for anonymous)."
    )
    subject = models.CharField(
        max_length=100,
        help_text="Subject or title of the feedback."
    )
    feedback_text = models.TextField(
        help_text="Detailed feedback or complaint."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the feedback was submitted."
    )

    def __str__(self):
        return f"{self.subject} ({self.get_role_display()})"

    class Meta:
        verbose_name = "School Feedback"
        verbose_name_plural = "School Feedbacks"
        ordering = ['-created_at']

