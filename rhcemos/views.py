from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from functools import wraps
from datetime import datetime
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum


def is_authenticated(f):  # le meme principe de login_required
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_matricule'):
            return redirect('signin')
        return f(request, *args, **kwargs)
    return wrapper


# Create your views here.


def index(request):
    return render(request, "rhcemos/index.html")


def signin(request):
    error = None
    if request.method == "POST":
        matricule = request.POST['matricule']
        password = request.POST['mot_de_passe']
        try:
            user = Personnelles.objects.get(Matricule=matricule)
        except Personnelles.DoesNotExist:
            user = None

        if user is not None and user.MotDePasse == password:
            request.session['user_matricule'] = user.Matricule
            return redirect('dashboard')
        else:
            error = "Matricule ou mot de passe invalide."
    return render(request, 'rhcemos/index.html', {'error': error})


def signout(request):
    if 'user_matricule' in request.session:
        del request.session['user_matricule']
    logout(request)
    return redirect('index')


def demande_absence(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    if request.method == 'POST':
        date_debut = request.POST.get('DateDebut')
        date_fin = request.POST.get('DateFin')
        motif_absence = request.POST.get('MotifAbsence')
        tel_absence = request.POST.get('TelAbsence')
        mail_absence = request.POST.get('MailAbsence')
        pj_demande_absence = request.FILES.get('PJDemandeAbsence')

        # Convert the strings to date objects
        date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()

        # Calculate DureAbsence
        dure_absence = (date_fin_obj - date_debut_obj).days + 1

        # Use IdTypeAbsence instead of DescriptionAbsence for fetching the type
        id_type_absence = request.POST.get('DescriptionAbsence')

        try:
            personnel = Personnelles.objects.get(Matricule=user_matricule)
            type_absence = TypeAbsence.objects.get(pk=id_type_absence)
        except (Personnelles.DoesNotExist, TypeAbsence.DoesNotExist):
            messages.error(
                request, 'Erreur lors de la récupération des informations.')
            return redirect('absence')

        # Create a new DemandeAbsence instance
        demande = DemandeAbsence(
            DateDebut=date_debut,
            DateFin=date_fin,
            DureAbsence=dure_absence,
            MotifAbsence=motif_absence,
            TelAbsence=tel_absence,
            MailAbsence=mail_absence,
            PJDemandeAbsence=pj_demande_absence,
            DateSaisi=datetime.now(),
            IdTypeAbsence=type_absence,
            IdPersonnel=personnel,
        )
        demande.save()

        messages.success(
            request, 'Votre Demande a été enregistrée avec succès.')
        return redirect('absence')

    all_types = TypeAbsence.objects.all()
    return render(request, "rhcemos/absence.html", {'user': user, 'all_types': all_types})


def approve_chef(request, pk):
    absence = get_object_or_404(DemandeAbsence, pk=pk)
    absence.ValidationChef1 = "approuvé"
    absence.save()
    return redirect('dashboard')


def reject_chef(request, pk):
    absence = get_object_or_404(DemandeAbsence, pk=pk)
    absence.ValidationChef1 = "Rejetée"
    absence.ValidationRH = "Rejetée"
    absence.save()
    return redirect('dashboard')


def approve_rh(request, pk):
    absence = get_object_or_404(DemandeAbsence, pk=pk)
    absence.ValidationRH = "approuvé"
    absence.save()
    return redirect('dashboard')


def reject_rh(request, pk):
    absence = get_object_or_404(DemandeAbsence, pk=pk)
    absence.ValidationRH = "Rejetée"
    absence.save()
    return redirect('dashboard')


def demande_hs(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)

    # Filter agents to get all personnel who belong to the same service and society as the chef
    agents = Personnelles.objects.filter(
        Q(IdPoste__IdService=user.IdPoste.IdService) &
        Q(IdSociete=user.IdSociete) &
        ~Q(IdPersonnel=user.IdPersonnel)
    )

    if request.method == "POST":
        # Get form data
        IdPersonnelCreePour = request.POST.get('IdPersonnelCreePour')
        DateDebutHS = request.POST.get('DateDebut')
        HDebut = request.POST.get('HDebut')
        DateFin = request.POST.get('DateFin')
        HFin = request.POST.get('HFin')
        TauxHoraire = request.POST.get('TauxHoraire')
        Commentaire = request.POST.get('Commentaire')

        # Creating a new DemandeHS object
        new_demande_hs = DemandeHS(
            IdPersonnelCreePar=user,
            IdPersonnelCreePour=Personnelles.objects.get(
                IdPersonnel=IdPersonnelCreePour),
            DateDebutHS=DateDebutHS,
            HDebut=HDebut,
            DateFin=DateFin,
            HFin=HFin,
            TauxHoraire=TauxHoraire,
            DateSaisi=datetime.now(),
            Commentaire=Commentaire,
            ValidationChef1="approuvé"
        )

        # Saving the object to the database
        new_demande_hs.save()

        messages.success(
            request, 'Demande Heure Supplementaire créée avec succès')
        return redirect('heuresupplementaire')

    return render(request, "rhcemos/heuresupplementaire.html", {'user': user, 'agents': agents})


def approve_hs(request, demande_id):
    demande_hs = get_object_or_404(DemandeHS, pk=demande_id)
    demande_hs.ValidationRH = "approuvé"
    demande_hs.DateDernierModification = datetime.now()
    demande_hs.save()
    return redirect('dashboard')


def reject_hs(request, demande_id):
    demande_hs = get_object_or_404(DemandeHS, pk=demande_id)
    demande_hs.ValidationRH = "rejetée"
    demande_hs.DateDernierModification = datetime.now()
    demande_hs.save()
    return redirect('dashboard')


def demande_attestation(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    if request.method == 'POST':
        # Use IdTypeAbsence instead of DescriptionAttestation for fetching the type
        id_type_attestation = request.POST.get('DescriptionAttestation')

        try:
            personnel = Personnelles.objects.get(Matricule=user_matricule)
            type_attestation = TypeAttestation.objects.get(
                pk=id_type_attestation)
        except (Personnelles.DoesNotExist, TypeAttestation.DoesNotExist):
            messages.error(
                request, 'Erreur lors de la récupération des informations.')
            return redirect('attestation')

        # Create a new DemandeAbsence instance
        demande = DemandeAttestation(
            DateCreation=datetime.now(),
            IdTypeAttestation=type_attestation,
            IdPersonnel=personnel,
        )
        demande.save()

        messages.success(
            request, 'Votre Demande a été enregistrée avec succès.')
        return redirect('attestation')

    all_types = TypeAttestation.objects.all()
    return render(request, "rhcemos/attestation.html", {'user': user, 'all_types': all_types})


def approve_attestation(request, demande_id):
    demande_attestation = get_object_or_404(DemandeAttestation, pk=demande_id)
    demande_attestation.ValidationRH = "approuvé"
    demande_attestation.save()
    return redirect('dashboard')


def reject_attestation(request, demande_id):
    demande_attestation = get_object_or_404(DemandeAttestation, pk=demande_id)
    demande_attestation.ValidationRH = "rejetée"
    demande_attestation.save()
    return redirect('dashboard')


@is_authenticated
def dashboard(request):
    user_matricule = request.session['user_matricule']
    
    
    
    current_user = Personnelles.objects.get(Matricule=user_matricule)
    
    
    
    
    permitted_roles = ["rh", "admin", "chef"]

    mes_absences = DemandeAbsence.objects.filter(IdPersonnel=current_user)
    mes_hs = DemandeHS.objects.filter(
        IdPersonnelCreePour=current_user,
        ValidationRH="approuvé"
    )
    mes_attestations = DemandeAttestation.objects.filter(
        IdPersonnel=current_user
    )

    if current_user.IdRole.NameRole == "chef":
        equipe_absences = DemandeAbsence.objects.filter(
            IdPersonnel__IdPoste__IdService=current_user.IdPoste.IdService,
            IdPersonnel__IdSociete=current_user.IdSociete
        ).exclude(
            Q(IdPersonnel=current_user) |
            Q(ValidationChef1="approuvé") |
            Q(ValidationChef1="rejetée")
        )
    elif current_user.IdRole.NameRole in ["admin", "rh"]:
        equipe_absences = DemandeAbsence.objects.filter(
            ValidationChef1="approuvé"
        ).exclude(
            Q(IdPersonnel=current_user) |
            Q(ValidationRH="approuvé") |
            Q(ValidationRH="rejetée")
        )

    else:
        equipe_absences = DemandeAbsence.objects.none()  # Or some other default case

    if current_user.IdRole.NameRole in ["admin", "rh"]:
        equipe_hs = DemandeHS.objects.filter(
            ValidationChef1="approuvé"
        ).exclude(
            Q(ValidationRH="approuvé") |
            Q(ValidationRH="rejetée")
        )
    else:
        equipe_hs = DemandeHS.objects.none()

    if current_user.IdRole.NameRole in ["admin", "rh"]:
        equipe_attestations = DemandeAttestation.objects.all().exclude(
            Q(ValidationRH="approuvé") |
            Q(ValidationRH="rejetée")
        )
    else:
        equipe_attestations = DemandeAttestation.objects.none()  # Or some other default case

    return render(request, "rhcemos/dashboard.html", {'user': current_user, 'mes_absences': mes_absences, 'mes_hs': mes_hs, 'mes_attestations': mes_attestations, 'equipe_absences': equipe_absences, 'equipe_hs': equipe_hs, 'equipe_attestations': equipe_attestations, 'permitted_roles': permitted_roles})


def contact(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    if request.method == 'POST':
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Composez un message formaté avec les informations de l'utilisateur
        formatted_message = f"""
        <p><strong>Matricule :</strong> {user.Matricule}</p>
        <p><strong>Téléphone :</strong> {user.TelephonePersonnel}</p>
        <p><strong>Société :</strong> {user.IdSociete.DescriptionSociete}</p>
        <p><strong>Service :</strong> {user.IdPoste.IdService.DescriptionService}</p>
        <br />
        <p><strong>Objet :</strong>{sujet}</p>
        <br />
        Monsieur : <strong> {user.Prenom.upper()} {user.Nom.upper()} </strong>
        <br />
        <p><strong>Message :</strong></p>
        <p>{message}</p>
        <br />
        Cordialement,
        <br /><br />
        
        <div style="font-family: Arial, sans-serif; color: #535353; font-size: 10pt;">
            <p style="color: #2d4e77; font-weight: bold;">
                PORTAIL RH
            </p>

            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="width: 225px; padding: 0 5.4pt;" valign="top">
                        <img width="154" height="43" src="https://cemosciment.ma/img/resources/logo.png" style="display: block;">
                    </td>
                    <td style="width: 413px; padding: 0 5.4pt;" valign="top">
                        <p style="font-weight: bold; color: #092800; line-height: 12.75pt;">
                            CEMOS CIMENT S. A.
                        </p>
                        <p style="font-size: 8pt; font-weight: bold; color: #092800; line-height: 12.75pt;">
                            Filiale de Cemos Group PLC
                        </p>
                        <p style="font-size: 8.5pt; line-height: 12.75pt;">
                            Hay Jedid | Rue Principale RN | 70050 Tarfaya 
                        </p>
                        <p style="font-size: 8.5pt; line-height: 12.75pt;">
                            Mob 212 (0) xxx xxx xxx
                        </p>
                    </td>
                </tr>
            </table>

            <p style="color: #1f497d; text-align: justify; line-height: 1.5;">
                Cette communication et les pièces jointes sont destinées à la personne ou l'entité nommée ci-dessus et peuvent contenir des éléments confidentiels et / ou privilégiés. Toute révision, divulgation, diffusion, retransmission, publication ou toute autre utilisation ou prise de toute action sur la base de ces informations par des personnes ou entités autres que le destinataire est interdite. Si vous l'avez reçu par erreur, veuillez en informer 
                l'expéditeur en répondant à cet e-mail ou par téléphone au +212 (0) 662 110 412 et enlevez le matériel de votre système. Les actions de Cemos Ciment S.A. et de ses employés sont régies par son code de conduite de manière éthique et en conformité avec toutes les lois anti-corruption et autres lois de chaque endroit où il est présent et en situation irrégulière doit être signalée sur le 
                <a href="http://www.cemosciment.ma/conformité" target="_blank" style="color: #0056d6;">site web de la société</a> en toute confidentialité. Cemos Ciment S.A. est filiale de Cemos Group Plc. Cemos-Ciment SA. au capital de 50 000 000 DH, RC Laayoune N°18909, ICE N° 000333383000065 Patente N° 77612500, IF N° 18773131, Site aÌ Hay Jedid, Rue Principale SN - Tarfaya.
            </p>

            <p>
                <a href="http://www.cemosciment.ma/" target="_blank" style="color: #1f497d;">www.cemosciment.ma</a>
            </p>
            <p style="color: #00b050;">
                Pensez à l'environnement avant d'imprimer cet e-mail.
            </p>
        </div>

        """

        # Envoyer le mail
        send_mail(
            sujet,
            '',  # Le corps du message est vide parce que nous utilisons html_message pour le contenu formaté en HTML
            user.Email,  # Ici, utilisez l'adresse e-mail de l'utilisateur comme expéditeur
            ['Houss.benhassoun.1999@gmail.com'],  # Liste des destinataires
            # Utilisez l'argument html_message pour spécifier le contenu formaté en HTML
            html_message=formatted_message,
        )

        return redirect('dashboard')

    return render(request, "rhcemos/contact.html", {'user': user})


def profile(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/profile.html", {'user': user})


def update_status(request):
    if request.method == "POST":
        new_status = request.POST.get('status')
        user_matricule = request.session['user_matricule']
        user = Personnelles.objects.get(Matricule=user_matricule)
        user.statut = new_status
        user.save()
    return redirect('profile')


def users(request):
    user_matricule = request.session['user_matricule']
    current_user = Personnelles.objects.get(Matricule=user_matricule)
    all_users = Personnelles.objects.all()
    return render(request, "rhcemos/users.html", {'user': current_user, 'personnelles': all_users})


def attestation(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/attestation.html", {'user': user})


def stagiaire(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/stagiaire.html", {'user': user})


def absence(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/absence.html", {'user': user})


def mouvement(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/mouvement.html", {'user': user})


def heuresupplementaire(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/heuresupplementaire.html", {'user': user})


def evenement(request):
    user_matricule = request.session['user_matricule']
    user = Personnelles.objects.get(Matricule=user_matricule)
    return render(request, "rhcemos/evenement.html", {'user': user})
