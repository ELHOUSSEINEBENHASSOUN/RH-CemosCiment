from django.contrib import admin
from .models import PRole, PService, PPoste, PSociete, Personnelles, Pointage, ErreurPointage, TypeAbsence, DemandeAbsence, DemandeHS, TypeAttestation, DemandeAttestation, Horaire, PlanDeRoulement, CalendrierGenerale
from django.db.models import Model


# Register your models here.

def get_model_fields(model):
    fields = []
    for field in model._meta.fields:
        if isinstance(field, Model):
            continue
        fields.append(field.name)
    return fields


@admin.register(PRole)
class PRole(admin.ModelAdmin):
    list_display = get_model_fields(PRole)


@admin.register(PService)
class PService(admin.ModelAdmin):
    list_display = get_model_fields(PService)


@admin.register(PPoste)
class PPoste(admin.ModelAdmin):
    list_display = get_model_fields(PPoste)


@admin.register(PSociete)
class PPoste(admin.ModelAdmin):
    list_display = get_model_fields(PSociete)


@admin.register(Personnelles)
class Personnelles(admin.ModelAdmin):
    list_display = get_model_fields(Personnelles)


@admin.register(TypeAbsence)
class TypeAbsence(admin.ModelAdmin):
    list_display = get_model_fields(TypeAbsence)


@admin.register(DemandeAbsence)
class DemandeAbsence(admin.ModelAdmin):
    list_display = get_model_fields(DemandeAbsence)


@admin.register(DemandeHS)
class DemandeHS(admin.ModelAdmin):
    list_display = get_model_fields(DemandeHS)


@admin.register(TypeAttestation)
class TypeAttestation(admin.ModelAdmin):
    list_display = get_model_fields(TypeAttestation)


@admin.register(DemandeAttestation)
class DemandeAttestation(admin.ModelAdmin):
    list_display = get_model_fields(DemandeAttestation)


@admin.register(Horaire)
class Horaire(admin.ModelAdmin):
    pass


@admin.register(PlanDeRoulement)
class PlanDeRoulement(admin.ModelAdmin):
    pass


@admin.register(CalendrierGenerale)
class CalendrierGenerale(admin.ModelAdmin):
    pass


@admin.register(Pointage)
class Pointage(admin.ModelAdmin):
    pass


@admin.register(ErreurPointage)
class ErreurPointage(admin.ModelAdmin):
    pass


"""

@admin.register(PService)
class PService(admin.ModelAdmin):
    list_display = (
        "titre",
        "slug",
        "price",
        "price_mad",
        "published",
        "instructor",
        "created_at",
    )

    # Metter l'attribut modifiable
    list_editable = ("titre", "price", "published", "instructor")
    # Metter l'attribut cliquable
    list_display_links = ("slug", "created_at")
    # Ajouter la barre de recherche
    search_fields = ("titre", "slug")
    # Ajouter la barre de filtre à droite
    list_filter = ("published", "instructor")
    # Ajouter la table de filtre pour choisir plusieurs choix
    filter_horizontal = ("tags", )
    # Ajouter la text de filtre dans instructor et category
    autocomplete_fields = ("instructor", "category")
    # Ajouter Pagination Per Page dans la table de course
    list_per_page = 2
    # désactiver le champs slug
    readonly_fields = ("slug", )
    # le meme modifcation dans le titre = slug en meme temps
    # prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Pour eviter l'erreur dans autocomplete_fields de CourseAdmin
    search_fields = ("label", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass """
