from django.urls import path
from tf_idf import views

# from tf_idf.views import LoadFileView, TFIDFView

urlpatterns = [
    path('', views.load_file, name='load_file'),
    path('show_words/<str:name>', views.show_words, name='show_words'),
]
