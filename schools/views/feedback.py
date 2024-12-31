from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from schools.models import School, SchoolFeedback
from schools.forms import SchoolFeedbackForm


def feedback_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = SchoolFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect(reverse_lazy('schools:details', kwargs={'pk': school.id}))
    else:
        form = SchoolFeedbackForm(initial={'school': school})

    return render(request, 'schools/create.html', {'form': form, 'object': school, 'obj_name': 'Feedback'})

def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(SchoolFeedback, pk=feedback_id)

    return render(request, 'schools/feedback_detail.html', {'feedback': feedback})

def feedback_delete(request, feedback_id):
    feedback = get_object_or_404(SchoolFeedback, pk=feedback_id)
    school = feedback.school
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully.')
        return redirect(reverse_lazy('schools:details', kwargs={'pk': school.id}))
    return render(request, 'schools/confirm_delete.html', {'object': feedback, 'obj_name': 'Feedback'})
