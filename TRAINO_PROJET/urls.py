from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from front.views import Bienvenu_onatra

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Bienvenu_onatra.as_view(), name = 'bienvenu_onatra'),
    path('utilisateur/', include('utilisateur.urls')),
    path('front/', include('front.urls')),
    path('traino_materiel/', include('traino_materiel.urls')),
    path('train/', include('train.urls')),
    path('voiture/', include('voiture.urls')),
    path('gare/', include('gare.urls')),
    path('voyage/', include('voyage.urls')),
    path('tarification/', include('tarification.urls')),
    path('details_voyage/', include('details_voyage.urls')),
    path('publication_avis/', include('publication_avis.urls')),
    path('reservation_paiement/', include('reservation_paiement.urls')),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



