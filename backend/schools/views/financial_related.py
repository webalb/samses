from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy


from backend.schools.models import FeeStructure, School
from backend.schools.forms import FeeStructureForm
from backend.schools.utils import generic_create, generic_delete


# ==============================
# ||| SCHOOL FINANCE DETAILS |||
# ==============================
def school_finance(request, school_id):
    school = get_object_or_404(School, pk=school_id)

    context = {
        'school': school,
    }
    return render(request, 'sections/finance.html', context)
# Create Fee Structure
def fee_structure_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    return generic_create(
        request=request,
        form_class=FeeStructureForm,
        obj_name="Fee Structure",
        related_obj=school,
        redirect_url=reverse_lazy('schools:school_finance', kwargs={'school_id': school_id})
    )

# Update Fee Structure
def fee_structure_update(request, pk):
    fee_structure = get_object_or_404(FeeStructure, pk=pk)
    return generic_create(
        request=request,
        form_class=FeeStructureForm,
        obj_name="Fee Structure",
        obj=fee_structure,
        related_obj=fee_structure.school,
        redirect_url=reverse_lazy('schools:school_finance', kwargs={'school_id': fee_structure.school.id})
    )

# Delete Fee Structure
def fee_structure_delete(request, pk):
    return generic_delete(
        request=request,
        model=FeeStructure,
        pk=pk,
        redirect_url=reverse_lazy('schools:school_finance', kwargs={'school_id': FeeStructure.objects.get(pk=pk).school.id}),
        obj_name="Fee Structure"
    )
