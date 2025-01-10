# views.py
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest

from backend.schools.models import AcademicSession

def complete_current_sessions(request):
    if request.method == "POST":
        # Mark all ongoing sessions as completed
        AcademicSession.complete_all_ongoing_sessions()
        messages.success(request, "All ongoing academic sessions have been marked as completed.")
        
        # Redirect back to the referring page
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        return redirect("schools:academic_session_list")  # Fallback redirection if no referer is found
    return HttpResponseBadRequest("Invalid request method.")

def complete_session(request, session_id):
    session = get_object_or_404(AcademicSession, id=session_id)
    if session.status == "ongoing":
        session.complete_session()
        messages.success(request, f"Academic session '{session.session_name}' has been completed.")
    else:
        messages.warning(request, "Only ongoing sessions can be completed.")
    
    # Redirect back to the referring page
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("schools:academic_session_list")  