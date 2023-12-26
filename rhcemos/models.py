from django.db import models
import uuid
# Create your models here.


class PRole(models.Model):
    IdRole = models.AutoField(primary_key=True)
    NameRole = models.CharField(max_length=100, null=True)
    DescriptionRole = models.CharField(max_length=300, null=True)
    Statut = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.NameRole} ({self.IdRole})"

    class Meta:
        db_table = 'P_Role'


class PService(models.Model):
    IdService = models.AutoField(primary_key=True)
    DescriptionService = models.CharField(max_length=300, null=True)
    CodeService = models.IntegerField(null=True)
    Statut = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.DescriptionService} ({self.IdService})"

    class Meta:
        db_table = 'P_Service'


class PPoste(models.Model):
    IdPoste = models.AutoField(primary_key=True)
    DescriptionPoste = models.CharField(max_length=300, null=True)
    CodePoste = models.IntegerField(null=True)
    Statut = models.CharField(max_length=10, null=True)
    IdService = models.ForeignKey(
        PService, null=True,
        on_delete=models.SET_NULL,
        db_column='IdService')

    def __str__(self):
        return f"{self.DescriptionPoste} ({self.IdPoste})"

    class Meta:
        db_table = 'P_Poste'


class PSociete(models.Model):
    IdSociete = models.AutoField(primary_key=True)
    DescriptionSociete = models.CharField(max_length=300, null=True)
    Localisation = models.CharField(max_length=300, null=True)
    Telephone = models.CharField(max_length=50, null=True)
    Email = models.EmailField(max_length=50, null=True)
    RC = models.CharField(max_length=300, null=True)
    CodeSociete = models.IntegerField(null=True)
    Statut = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.DescriptionSociete} ({self.IdSociete})"

    class Meta:
        db_table = 'P_Societe'


class Personnelles(models.Model):
    IdPersonnel = models.AutoField(primary_key=True)
    Matricule = models.CharField(max_length=25, null=True)
    Cin = models.CharField(max_length=25, null=True)
    Nom = models.CharField(max_length=25, null=True)
    Prenom = models.CharField(max_length=25, null=True)
    TelephonePersonnel = models.CharField(
        max_length=25,
        null=True)
    TelephoneProfessionel = models.CharField(
        max_length=25,
        null=True)
    EmailPersonnel = models.EmailField(max_length=100, null=True)
    Genre = models.CharField(max_length=25, null=True)
    DateNaissance = models.DateField(null=True)
    LieuNaissance = models.CharField(max_length=50, null=True)
    NbrEnfant = models.IntegerField(null=True)
    Photo = models.CharField(max_length=255, null=True)
    Email = models.EmailField(max_length=100, null=True)
    MotDePasse = models.CharField(max_length=255, null=True)
    DateAffiliation = models.DateField(null=True)
    DateDepart = models.DateField(null=True)
    SoldeConge = models.FloatField(null=True)
    SoldeRecuperation = models.FloatField(null=True)
    RestAnneeDerniere = models.FloatField(null=True)
    SalaireMensuel = models.FloatField(null=True)
    SalaireHoraire = models.FloatField(null=True)
    IdFromPointeurse = models.IntegerField(null=True)
    CardNumber = models.IntegerField(null=True)
    Statut = models.CharField(max_length=55, null=True)
    IdSociete = models.ForeignKey(
        PSociete, null=True,
        on_delete=models.SET_NULL,
        db_column='IdSociete')
    IdPoste = models.ForeignKey(
        PPoste, null=True,
        on_delete=models.SET_NULL,
        db_column='IdPoste')
    IdRole = models.ForeignKey(
        PRole, null=True,
        on_delete=models.SET_NULL,
        db_column='IdRole')

    def __str__(self):
        return f"{self.Matricule} ({self.IdPersonnel})"

    class Meta:
        db_table = 'Personnelles'


class TypeAbsence(models.Model):
    IdTypeAbsence = models.AutoField(primary_key=True)
    DescriptionAbsence = models.CharField(max_length=300, null=True)
    Commentaire = models.TextField(null=True)
    Statut = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'TypeAbsence'


class DemandeAbsence(models.Model):
    IdDemandeAbsence = models.AutoField(primary_key=True)
    DateDebut = models.DateField(null=True)
    DateFin = models.DateField(null=True)
    DureAbsence = models.FloatField(null=True)
    MotifAbsence = models.TextField(null=True)
    TelAbsence = models.CharField(max_length=30, null=True)
    MailAbsence = models.CharField(max_length=250, null=True)
    ValidationChef1 = models.CharField(max_length=30, null=True)
    ValidationChef2 = models.CharField(max_length=30, null=True)
    ValidationRH = models.CharField(max_length=30, null=True)
    DateSaisi = models.DateField(null=True)
    DateDernierModification = models.DateField(null=True)
    PJDemandeAbsence = models.TextField(null=True)
    IdPersonnel = models.ForeignKey(
        Personnelles, null=True,
        on_delete=models.SET_NULL,
        db_column='IdPersonnel')
    IdTypeAbsence = models.ForeignKey(
        TypeAbsence, null=True,
        on_delete=models.SET_NULL,
        db_column='IdTypeAbsence')

    class Meta:
        db_table = 'DemandeAbsence'


class TypeAttestation(models.Model):
    IdTypeAttestation = models.AutoField(primary_key=True)
    DescriptionAttestation = models.CharField(max_length=300, null=True)
    Commentaire = models.TextField(null=True)
    Statut = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'TypeAttestation'


class DemandeAttestation(models.Model):
    IdDemandeAttestation = models.AutoField(primary_key=True)
    DateCreation = models.DateField(null=True)
    ValidationRH = models.CharField(max_length=30, null=True)
    IdTypeAttestation = models.ForeignKey(
        TypeAttestation, null=True,
        on_delete=models.SET_NULL,
        db_column='IdTypeAttestation')
    IdPersonnel = models.ForeignKey(
        Personnelles, null=True,
        on_delete=models.SET_NULL,
        db_column='IdPersonnel')

    class Meta:
        db_table = 'DemandeAttestation'


class DemandeHS(models.Model):
    IdDemandeHS = models.AutoField(primary_key=True)
    DateDebutHS = models.DateField(null=True)
    HDebut = models.TimeField(null=True)
    DateFin = models.DateField(null=True)
    HFin = models.TimeField(null=True)
    TauxHoraire = models.FloatField(null=True)
    ValidationChef1 = models.CharField(max_length=30, null=True)
    ValidationChef2 = models.CharField(max_length=30, null=True)
    ValidationRH = models.CharField(max_length=30, null=True)
    DateSaisi = models.DateField(null=True)
    DateDernierModification = models.DateField(null=True)
    Commentaire = models.TextField(null=True)
    IdPersonnelCreePar = models.ForeignKey(
        Personnelles,
        related_name="created_by",
        null=True, on_delete=models.SET_NULL,
        db_column='IdPersonnelCreePar')
    IdPersonnelCreePour = models.ForeignKey(
        Personnelles,
        related_name="created_for",
        null=True, on_delete=models.SET_NULL,
        db_column='IdPersonnelCreePour')

    class Meta:
        db_table = 'DemandeHS'


class Pointage(models.Model):
    IdPointage = models.AutoField(primary_key=True)
    DateEntre = models.DateField(null=True)
    HE = models.BigIntegerField(null=True)
    DateSoti = models.DateField(null=True)
    HS = models.BigIntegerField(null=True)
    DateExtraction = models.DateField(null=True)
    OutilPointageE = models.CharField(max_length=50, null=True)
    OutilPointageS = models.CharField(max_length=50, null=True)
    Commentaire = models.TextField(null=True)
    IdPersonnel = models.ForeignKey(
        Personnelles, null=True,
        on_delete=models.SET_NULL,
        db_column='IdPersonnel')

    class Meta:
        db_table = 'Pointage'


class ErreurPointage(models.Model):
    IdErreurPointage = models.AutoField(primary_key=True)
    DateInsertion = models.DateField(null=True)
    Commentaire = models.TextField(null=True)
    IdPointage = models.ForeignKey(
        Pointage, null=True,
        on_delete=models.SET_NULL,
        db_column='IdPointage')

    class Meta:
        db_table = 'ErreurPointage'


class Horaire(models.Model):
    IdHoraire = models.AutoField(primary_key=True)
    DateDebut = models.DateField(null=True)
    HDebut = models.TimeField(null=True)
    DateFin = models.DateField(null=True)
    HFin = models.TimeField(null=True)
    Commentaire = models.TextField(null=True)

    class Meta:
        db_table = 'Horaire'


class PlanDeRoulement(models.Model):
    IdPlanDeRoulement = models.AutoField(primary_key=True)
    DateDebut = models.DateField(null=True)
    DateFin = models.DateField(null=True)
    DateCreation = models.DateField(null=True)
    Commentaire = models.TextField(null=True)
    JTravail = models.CharField(max_length=30, null=True)
    JRepos = models.CharField(max_length=30, null=True)
    JReposTravaile = models.CharField(max_length=30, null=True)
    JFerieTravaille = models.CharField(max_length=30, null=True)
    Modification = models.CharField(max_length=30, null=True)
    DateModification = models.DateField(null=True)
    IdPersonneModifier = models.ForeignKey(
        Personnelles,
        related_name="modifier_by", null=True,
        on_delete=models.SET_NULL,
        db_column='IdPersonneModifier')
    IdHoraire = models.ForeignKey(
        Horaire, null=True,
        on_delete=models.SET_NULL,
        db_column='IdHoraire')
    IdPersonnelCreePar = models.ForeignKey(
        Personnelles,
        related_name="plan_created_by",
        null=True, on_delete=models.SET_NULL,
        db_column='IdPersonnelCreePar')
    IdPersonnelCreePour = models.ForeignKey(
        Personnelles,
        related_name="plan_created_for",
        null=True, on_delete=models.SET_NULL,
        db_column='IdPersonnelCreePour')

    class Meta:
        db_table = 'PlanDeRoulement'


class CalendrierGenerale(models.Model):
    Idcalendrier = models.AutoField(primary_key=True)
    DateDebut = models.DateField(null=True)
    DateFin = models.DateField(null=True)
    DateCreation = models.DateField(null=True)
    Commentaire = models.TextField(null=True)

    class Meta:
        db_table = 'calendrierGenerale'
