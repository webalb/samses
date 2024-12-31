from django.db import models

from .school import School
from .levels_and_classes import ProgramLevelTemplate
from .stakeholder import Staff
from student.models import Student

class FinanceRelatedModel(models.Model):
    """
    Description: Model Description
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class FeeStructure(FinanceRelatedModel):
    class_level = models.ForeignKey(
        'ProgramLevelTemplate',
        on_delete=models.CASCADE,
        help_text="The class level this fee applies to."
    )
    fee_type = models.CharField(
        max_length=50,
        choices=[
            ('tuition', 'Tuition Fee'),
            ('registration', 'Registration Fee'),
            ('exam', 'Examination Fee'),
            ('data_management', 'Data Management Fee'),
            ('sports', 'Sports Fee'),
            ('laboratory', 'Laboratory Fee'),
            ('extra_lesson', 'Extra Lesson Fee'),
            ('execution', 'Execution Fee'),
            ('field_trip', 'Field Trip Fee'),
            ('graduation', 'Graduation Fee'),
            ('other', 'Other Fee'),
        ],
        help_text="Type of fee being charged."
    )
    is_optional = models.BooleanField(
        default=False,
        help_text="Indicates if this fee is optional (e.g., Extra Lesson classes)."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in Naira."
    )
    description = models.TextField(blank=True, help_text="Additional details about the fee.")

    class Meta:
        unique_together = (('class_level', 'fee_type'),)
    def __str__(self):
        return f"{self.school.name} - {self.get_fee_type_display()} for {self.class_level.level}"

import uuid
from django.utils.timezone import now

class Invoice(FinanceRelatedModel):
    """
    Model for generating school payment invoices with a unique and professional invoice ID.
    """
    invoice_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False,
        primary_key=True, 
        help_text="Unique invoice identifier (e.g., INV-YYYYMMDD-XXXXX)."
    )
    invoice_date = models.DateField(auto_now_add=True, help_text="The date when the invoice was created.")
    due_date = models.DateField(help_text="The date by which the payment is due.")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Total amount to be paid.")
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Partial', 'Partialy Paid'),('Paid', 'Paid'), ('Overdue', 'Overdue')],
        default='Pending',
        help_text="Current status of the invoice."
    )
    optional_fees_selected = models.ManyToManyField(
        'FeeStructure',
        blank=True,
        help_text="Optional fees selected by the parent or guardian."
    )

    def __str__(self):
        return f"Invoice {self.invoice_id} for {self.student.full_name()}"

    def save(self, *args, **kwargs):
        """
        Override save method to generate a unique invoice ID.
        """
        if not self.invoice_id:
            date_prefix = now().strftime('%Y%m%d')  # e.g., 20240101 for January 1, 2024
            unique_suffix = str(uuid.uuid4().int)[:6]  # Generate a unique 6-digit suffix
            self.invoice_id = f"INV-{date_prefix}-{unique_suffix}"

        super().save(*args, **kwargs)

    def calculate_total(self):
        """
        Calculate the total amount based on applicable non-optional and selected optional fees.
        """
        total = 0.0
        non_optional_fees = FeeStructure.objects.filter(
            school=self.school,
            class_level=self.student.class_level,
            is_optional=False
        )
        for fee in non_optional_fees:
            total += fee.amount

        for fee in self.optional_fees_selected.all():
            total += fee.amount

        self.total_amount = total
        self.save()
        return total

class Payment(FinanceRelatedModel):
    """
    Model for tracking payments made against invoices.
    """
    invoice = models.ForeignKey(
        'Invoice',
        on_delete=models.CASCADE,
        related_name='payments',
        help_text="The invoice this payment is associated with."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount paid in Naira."
    )
    payment_date = models.DateField(
        auto_now_add=True,
        help_text="The date when the payment was made."
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('Check', 'Check'),
            ('Online', 'Online'),
            ('Bank Transfer', 'Bank Transfer'),
            ('POS', 'POS'),
        ],
        help_text="Method used for the payment."
    )
    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        blank=True,
        help_text="Unique receipt number for the payment. if its cash, leave it the system will generate"
    )

    def __str__(self):
        return f"Payment for Invoice {self.invoice.invoice_id} - {self.amount} Naira"

    def save(self, *args, **kwargs):
        """
        Override save method to:
        - Generate a unique receipt number.
        - Update the invoice status if total payments cover the invoice amount.
        """
        if not self.receipt_number:
            from uuid import uuid4
            self.receipt_number = f"REC-{uuid4().hex[:16].upper()}"

        super().save(*args, **kwargs)

        # Update invoice status based on total payments
        total_paid = sum(payment.amount for payment in self.invoice.payments.all())
        if total_paid >= self.invoice.total_amount:
            self.invoice.status = 'Paid'
        elif total_paid > 0 and total_paid < self.invoice.total_amount:
            self.invoice.status = 'Partially Paid'
        else:
            self.invoice.status = 'Pending'
        self.invoice.save()

class ExpenseCategory(FinanceRelatedModel):
    """
    Model for categorizing school expenses.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the expense category (e.g., Salaries, Utilities).")
    description = models.TextField(blank=True, help_text="Description of the expense category.")

    def __str__(self):
        return self.name

class SchoolExpense(FinanceRelatedModel):
    """
    Model for recording school expenses.
    """
    category = models.ForeignKey(
        'ExpenseCategory',
        on_delete=models.CASCADE,
        related_name='school_expenses',
        help_text="Category of the expense."
    )
    description = models.TextField(help_text="Details of the expense.")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Amount spent.")
    date_incurred = models.DateField(help_text="Date when the expense was incurred.")
    receipt_number = models.CharField(max_length=50, unique=True, blank=True, help_text="Unique receipt or reference number for this expense.")

    def __str__(self):
        return f"{self.category.name} - {self.amount} for {self.school.name}"

    def save(self, *args, **kwargs):
        """
        Auto-generate receipt_number if not provided.
        """
        if not self.receipt_number:
            from uuid import uuid4
            self.receipt_number = f"EXP-{uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

class Budget(FinanceRelatedModel):
    fiscal_year = models.CharField(max_length=10, help_text="Fiscal year (e.g., 2024).")
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total annual budget.")
    salaries = models.DecimalField(max_digits=15, decimal_places=2, help_text="Budget allocated for salaries.")
    infrastructure = models.DecimalField(max_digits=15, decimal_places=2, help_text="Budget for infrastructure development.")
    learning_materials = models.DecimalField(max_digits=15, decimal_places=2, help_text="Budget for learning materials.")
    miscellaneous = models.DecimalField(max_digits=15, decimal_places=2, help_text="Miscellaneous expenditures.")
    description = models.TextField(blank=True, help_text="Additional budget details.")

    def __str__(self):
        return f"Budget for {self.school.name} - Fiscal Year {self.fiscal_year}"

class Salary(FinanceRelatedModel):
    school=None
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.employee.full_name()} - {self.pay_date}"

class FundingSource(FinanceRelatedModel):
    source_name = models.CharField(max_length=100, help_text="Name of the funding source (e.g., Government Grant).")
    funding_type = models.CharField(
        max_length=50,
        choices=[
            ('government', 'Government'),
            ('donation', 'Donation'),
            ('loan', 'Loan'),
            ('other', 'Other'),
        ],
        help_text="Type of funding source.",
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Amount received in local currency.")
    date_received = models.DateField()
    description = models.TextField(blank=True, help_text="Additional details about the funding.")

    def __str__(self):
        return f"{self.source_name} - {self.amount} ({self.school.name})"

class ScholarshipAndAid(FinanceRelatedModel):
    name = models.CharField(max_length=100, help_text="Name of the scholarship or aid program.")
    description = models.TextField(blank=True, help_text="Details about the program.")
    eligibility_criteria = models.TextField(help_text="Criteria for students to qualify.")
    total_funding = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total amount allocated.")
    application_deadline = models.DateField(blank=True, null=True, help_text="Deadline for applications (if any).")
    number_of_recipients = models.PositiveIntegerField(help_text="Number of students benefiting from this program.")

    def __str__(self):
        return f"{self.name} ({self.school.name})"
