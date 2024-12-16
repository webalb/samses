from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages

from schools.models import School, Classrooms, Library, Laboratory, ComputerLab, SportsFacility, SchoolImages
from schools.forms import ClassroomsForm, LibraryForm, LaboratoryForm, ComputerLabForm, SportsFacilityForm, SchoolImagesForm

# Classrooms Create View
def classroom_create(request, school_id):
    """
    View to handle the creation of classroom infrastructure and associated images.
    """
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        # Initialize forms with POST data
        classroom_form = ClassroomsForm(request.POST)
        image_form = SchoolImagesForm(request.POST, request.FILES)

        if classroom_form.is_valid() and image_form.is_valid():
            # Save classroom details
            classroom = classroom_form.save(commit=False)
            classroom.school_id = school_id
            classroom.save()

            # Handle multiple image uploads
            images = request.FILES.getlist('image')  # Get the list of uploaded images
            for image in images:
                SchoolImages.objects.create(
                    school_id=school_id,
                    image=image,
                    image_type='classroom',  # Assign the type as 'classroom'
                )
            messages.success(request, 'Class rooms infrastructure details uploaded successfully')

            # Redirect to the same page or another page after saving
            return redirect('schools:details', pk=school_id)

    else:
        # Initialize empty forms
        classroom_form = ClassroomsForm()
        image_form = SchoolImagesForm()

    return render(request, 'schools/classroom_create.html', {
        'classroom_form': classroom_form,
        'image_form': image_form,
        'school': school,
    })
# Similarly for Library
def library_create(request, school_id):
    ImageFormSet = modelformset_factory(SchoolImages, form=SchoolImagesForm, extra=3, max_num=3)
    if request.method == 'POST':
        library_form = LibraryForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)

        if library_form.is_valid() and image_formset.is_valid():
            library = library_form.save(commit=False)
            library.school_id = school_id
            library.save()

            for form in image_formset:
                image = form.save(commit=False)
                image.school_id = school_id
                image.image_type = 'library'
                image.save()

            return redirect('school:library_create', school_id=school_id)

    else:
        library_form = LibraryForm()
        image_formset = ImageFormSet(queryset=SchoolImages.objects.none())

    return render(request, 'school/library_create.html', {
        'library_form': library_form,
        'image_formset': image_formset,
    })

# Repeat similar logic for Laboratory, ComputerLab, and SportsFacility
