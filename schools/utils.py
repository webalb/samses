from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db import transaction  # Import transaction
from schools.models import School, SchoolImages
from schools.forms import SchoolImagesForm, SchoolImagesUpdateForm
from django.core.exceptions import ValidationError

import os
import logging

logger = logging.getLogger(__name__)

def remove_old_file(file_path):
    """
    Removes the file at the given path if it exists. 
    Also checks if parent directories are empty and removes them recursively.

    Args:
        file_path (str): The path to the file to be removed.

    Returns:
        bool: True if the file and potentially empty directories were removed 
             successfully, False otherwise.
    """
    try:
        if file_path and os.path.isfile(file_path):
            os.remove(file_path)

            file_dir = os.path.dirname(file_path)

            while True:
                try:
                    if not os.listdir(file_dir):
                        os.rmdir(file_dir)
                        file_dir = os.path.dirname(file_dir)
                    else:
                        break
                except OSError as e:
                    # Log the error but don't stop the process
                    logger.error(f"Error removing directory: {file_dir}. Error: {e}")
                    break

            return True

    except OSError as e:
        logger.error(f"Error removing file: {file_path}. Error: {e}")
        return False


# Image type mapping to clean up strings
IMAGE_TYPE_MAPPING = {
    'computer_lab': 'computerlab',
    'science_lab': 'sciencelab',
    'classrooms': 'classrooms',
    # Add other mappings as needed
}


def infrastructure_create(request, school_id, form_class, image_type):
    """
    Generic view to handle the creation of infrastructure (e.g., Computer Lab, Science Lab)
    and associated images.
    """
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = form_class(request.POST)
        image_form = SchoolImagesForm(request.POST, request.FILES)

        try:
            with transaction.atomic():  # Ensure atomicity
                if form.is_valid() and image_form.is_valid():
                    # Save form data
                    instance = form.save(commit=False)
                    instance.school_id = school_id
                    images_description = request.POST.get('description')
                    if images_description:
                        instance.images_description = images_description
                    instance.save()

                    # Handle image uploads
                    images = request.FILES.getlist('image')
                    MAX_IMAGES = 3
                    if images:
                        existing_count = SchoolImages.objects.filter(school_id=school_id, image_type=image_type).count()
                        if existing_count + len(images) > MAX_IMAGES:
                            raise ValidationError(f"Maximum {MAX_IMAGES} images allowed.")

                        for image in images:
                            SchoolImages.objects.create(
                                school_id=school_id,
                                image=image,
                                image_type=IMAGE_TYPE_MAPPING.get(image_type, image_type),
                            )

                    messages.success(request, f"{image_type.replace('_', ' ').capitalize()} infrastructure uploaded successfully.")
                    redirect_url = f"{reverse('schools:details', kwargs={'pk': school_id})}#{image_type}"
                    return redirect(redirect_url)

        except ValidationError as e:
            # Add validation errors to the image form
            image_form.add_error('image', e.message)
        except Exception as e:
            # Handle unexpected errors gracefully
            print(e)
            messages.error(request, "An error occurred while saving the data. Please try again.")

    else:
        form = form_class()
        image_form = SchoolImagesForm()

    return render(request, 'schools/infrastructure_create.html', {
        'form': form,
        'form_type': f"{image_type.replace('_', ' ').capitalize()}",
        'image_form': image_form,
        'school': school,
    })

def infrastructure_update(request, school_id, model_class, form_class, image_type):
    """
    Generic view to handle the update of infrastructure (e.g., Classroom, Computer Lab, etc.)
    and associated images.
    """
    school = get_object_or_404(School, pk=school_id)
    instance = get_object_or_404(model_class, pk=school_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        image_form = SchoolImagesForm(request.POST, request.FILES)

        try:
            with transaction.atomic():  # Ensure atomicity
                if form.is_valid() and image_form.is_valid():
                    # Save the updated infrastructure details
                    form.save()

                    # Handle image deletions
                    delete_all_images = request.POST.get('delete_all_images')  # Checkbox for deleting all images
                    delete_image_ids = request.POST.getlist('delete_images')  # List of individual images to delete

                    if delete_all_images:
                        SchoolImages.objects.filter(school_id=school_id, image_type=image_type).delete()
                    elif delete_image_ids:
                        SchoolImages.objects.filter(id__in=delete_image_ids).delete()

                    # Handle new image uploads
                    new_images = request.FILES.getlist('image')
                    existing_image_count = SchoolImages.objects.filter(school_id=school_id, image_type=image_type).count()

                    if new_images:
                        total_images_count = existing_image_count + len(new_images)
                        MAX_IMAGES = 3

                        if total_images_count > MAX_IMAGES:
                            image_form.add_error('image', f"A {image_type.replace('_', ' ')} can have a maximum of {MAX_IMAGES} images.")
                            raise ValidationError("Exceeded the allowed number of images.")

                        # Save new images
                        for image in new_images:
                            SchoolImages.objects.create(
                                school_id=school_id,
                                image=image,
                                image_type=IMAGE_TYPE_MAPPING.get(image_type, image_type),
                            )

                    # Only redirect if no image form errors
                    if not image_form.errors:
                        messages.success(request, f"{image_type.replace('_', ' ').capitalize()} details updated successfully.")
                        return redirect(reverse('schools:details', kwargs={'pk': school_id}) + f"#{image_type}")
        
        except ValidationError:
            # Handle form errors gracefully (image form errors are already added)
            pass
        except Exception as e:
            messages.error(request, "An unexpected error occurred.a Please try again.")

    else:
        # Prepopulate forms with existing data
        form = form_class(instance=instance)
        image_form = SchoolImagesUpdateForm()

    # Retrieve existing images
    images = SchoolImages.objects.filter(school_id=school_id, image_type=image_type.replace('_', ''))

    return render(request, 'schools/infrastructure_update.html', {
        'form': form,
        'image_form': image_form,
        'school': school,
        'images': images,
        'form_type': image_type.replace('_', ' ').capitalize(),
    })

def infrastructure_delete(request, school_id, model_class, image_type):
    """
    Generic view to handle the deletion of infrastructure (e.g., Classroom, Computer Lab, etc.)
    and associated images.
    """
    school = get_object_or_404(School, pk=school_id)
    instance = get_object_or_404(model_class, school=school)  # Retrieve the specific infrastructure instance

    if request.method == 'POST':
        # Delete associated images
        SchoolImages.objects.filter(school_id=school_id, image_type=image_type).delete()

        # Delete the infrastructure record
        instance.delete()

        messages.success(request, f"{image_type.replace('_', ' ').capitalize()} details deleted successfully.")
        return redirect(reverse('schools:details', kwargs={'pk': school_id}) + f"#{image_type}")

    return render(request, 'schools/infrastructure_confirm_delete.html', {
        'school': school,
        'instance': instance,
        'form_type': image_type.replace('_', ' ').capitalize(),
    })


def generic_create(request, form_class, obj_name, obj=None, related_obj=None, redirect_url=None):
    """
    Generic view for creating and updating objects.
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            if related_obj:
                instance.school = related_obj  # Attach the related school object if applicable
            instance.save()
            messages.success(request, f"{obj_name} saved successfully!")
            return redirect(redirect_url)
    else:
        form = form_class(instance=obj)

    return render(request, 'schools/create.html', {
        'form': form,
        'object': related_obj or obj,
        'obj_name': obj_name,
    })


def generic_delete(request, model, pk, redirect_url, obj_name):
    """
    Generic view for deleting objects.
    """
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{obj_name} deleted successfully!")
        return redirect(redirect_url)

    return render(request, 'schools/confirm_delete.html', {
        'object': obj,
        'obj_name': obj_name,
    })
