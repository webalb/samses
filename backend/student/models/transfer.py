from django.db import models
from .student import Student
from .school import School

class Transfer(models.Model):
    """
    Logs transfers with details like reason for transfer, approval status, and the destination school.
    """
    TRANSFER_TYPE_CHOICES = [
        ('intra_state', 'Intra-State Transfer'),
        ('inter_state', 'Inter-State Transfer'),
        ('external', 'External Transfer'),
    ]
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="transfer_records")
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE_CHOICES, help_text="Type of transfer.")
    current_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="outgoing_transfers")
    destination_school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="incoming_transfers")
    reason = models.TextField(help_text="Reason for the transfer.")
    transfer_date = models.DateField(help_text="Date of the transfer.")
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        help_text="Approval status of the transfer."
    )
    notes = models.TextField(blank=True, help_text="Additional notes or comments.")

    def __str__(self):
        return f"{self.student.full_name} - {self.transfer_type} to {self.destination_school.name if self.destination_school else 'External'} ({self.approval_status.capitalize()})"


class ExternalTransferVerification(models.Model):
    """
    Handles validation of student data for transfers from schools outside SAMSES.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="external_verifications")
    originating_school = models.CharField(max_length=255, help_text="Name of the school the student is transferring from.")
    documents_submitted = models.TextField(help_text="Details of the documents submitted for verification.")
    verification_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')],
        default='pending',
        help_text="Status of the verification process."
    )
    verification_date = models.DateField(blank=True, null=True, help_text="Date when verification was completed.")
    notes = models.TextField(blank=True, help_text="Additional notes or comments.")

    def __str__(self):
        return f"{self.student.full_name} - {self.originating_school} ({self.verification_status.capitalize()})"
