from .forms import ( 
		SchoolForm, 
		SubjectForm, 
		TermForm, 
		AcademicSessionForm, 
		StakeholderForm, 
		SchoolMetadataForm, 
		AccreditationForm, 
		SuspensionForm, InspectionReportForm, ParentEngagementForm
	)
from .infrastructure_forms import ( 
	ClassroomsForm, 
	SchoolImagesUpdateForm, 
	LibraryForm, 
	LaboratoryForm, 
	ComputerLabForm, 
	SportsFacilityForm, 
	SchoolImagesForm, LibraryUpdateForm, LaboratoryUpdateForm, 
	ComputerLabUpdateForm, SportsFacilityUpdateForm,
	SpecialNeedsResourceForm,
	SpecialNeedsResourceUpdateForm,
 )
from .vocational_related import DepartmentRepositoryForm, VocationalPartnershipForm, SchoolDepartmentForm
from .levels_classes_and_subject import (
			LevelClassesForm, 
			ClassWithoutProgramLevelFieldForm, 
			NoStreamForm, 
			SubjectRepositoryForm,
			SchoolSubjectForm,
		)

from .feedback import SchoolFeedbackForm
from .grading_system import GradingScaleForm, GradeBoundaryForm, SubjectGradingConfigurationForm
from .stakeholders import StaffForm
from .financial_related import FeeStructureForm