from django.urls import path
from .views import *
app_name = 'home'
urlpatterns = [
    path('', homeview,name='home'),
    path('login/', loginview.as_view(),name='login'),
    path('register-admin/', RegisterAdmin.as_view(),name='register_admin'),
    path('register-student/', RegisterStudent.as_view(),name='register_student'),
    path('logout/', logout,name='logout'),
    path('student-details/<int:id>/', StudentDetails,name='student-details'),
    path('marks/', MarksView,name='marks'),
    path('add-marks/', AddMarks,name='add-marks'),
    path('edit-marks/<int:id>/', EditMarks,name='edit-marks'),
    path('search-customers', SearchCustomers,name='search-customers'),
]