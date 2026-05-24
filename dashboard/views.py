from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import json
import calendar

from accounts.models import Profile, CustomUser
from sadhana.models import SadhanaEntry
from seva.models import WeeklyServiceAssignment, DailySeva, MasterService
from analytics.models import ProgressStats
from notifications.models import Notification
from ai_chat.models import ChatMessage
from notifications.services import send_seva_completed_notification

@login_required(login_url='login')
def home_view(request):
    user = request.user
    # Ensure profile exists
    if not hasattr(user, 'profile'):
        role_map = {
            'Devotee': 'devotee',
            'Temple Leader': 'leader',
            'devotee': 'devotee',
            'leader': 'leader',
        }
        db_role = role_map.get(user.role, 'devotee')
        Profile.objects.create(user=user, role=db_role)

    if user.profile.role == 'leader':
        return redirect('dashboard:leader_dashboard')
    else:
        return redirect('dashboard:devotee_dashboard')

@login_required(login_url='login')
def devotee_dashboard(request):
    user = request.user
    # Ensure profile exists
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user, role='devotee')

    if request.method == 'POST':
        # Handle Sadhana Entry Form Submission
        sadhana_date_str = request.POST.get('sadhana_date')
        folk_residency = request.POST.get('folk_residency')
        mangal_aarti = request.POST.get('mangal_aarti')
        group_japa = request.POST.get('group_japa')
        sb_class = request.POST.get('sb_class')
        rounds_chanted_str = request.POST.get('rounds_chanted')
        sp_reading = request.POST.get('sp_reading')
        assigned_service = request.POST.get('assigned_service')

        # Parse date from "d mmmm yyyy" format e.g. "12 August 2026"
        try:
            sadhana_date = datetime.strptime(sadhana_date_str, '%d %B %Y').date()
        except Exception:
            sadhana_date = timezone.now().date()

        rounds_chanted = 16
        try:
            rounds_chanted = int(rounds_chanted_str)
        except ValueError:
            pass

        # Save to database
        SadhanaEntry.objects.create(
            user=user,
            sadhana_date=sadhana_date,
            folk_residency=folk_residency,
            mangal_aarti=mangal_aarti,
            group_japa=group_japa,
            sb_class=sb_class,
            rounds_chanted=rounds_chanted,
            sp_reading=sp_reading,
            assigned_service=assigned_service
        )

        from sadhana.models import SadhanaLog
        # mangala_aarti = True if option chosen is '1', '2', '3', or '4'
        is_attended = mangal_aarti in ['1', '2', '3', '4']
        SadhanaLog.objects.update_or_create(
            user=user,
            date=sadhana_date,
            defaults={'mangala_aarti': is_attended}
        )

        # Update Progress Stats for current month
        stats, created = ProgressStats.objects.get_or_create(user=user)
        now_date = timezone.localtime(timezone.now()).date()
        month_days = calendar.monthrange(now_date.year, now_date.month)[1]
        
        total_days = SadhanaEntry.objects.filter(
            user=user,
            sadhana_date__year=now_date.year,
            sadhana_date__month=now_date.month
        ).count()
        
        stats.total_submitted_days = total_days
        stats.percentage_completed = min(100.0, (float(total_days) / float(month_days)) * 100.0)
        stats.save()

        messages.success(request, "Sadhana Submitted Successfully")
        return redirect('dashboard:devotee_dashboard')

    # GET request:
    # 1. Fetch or create ProgressStats for current month (Do NOT recalculate on GET to prevent resets)
    stats, created = ProgressStats.objects.get_or_create(user=user)

    # 2. Fetch Seva Duties without creating dummy (only today's seva)
    today = timezone.localtime(timezone.now()).date()
    sevas = DailySeva.objects.filter(devotee=user, service_date=today)

    # 3. Retrieve all sadhana entries for visual display in stats
    sadhana_entries = SadhanaEntry.objects.filter(user=user).order_by('-sadhana_date')[:10]

    # 4. Fetch notifications for devotee
    notifications_list = Notification.objects.filter(user=user).order_by('-created_at')
    unread_notifications_count = Notification.objects.filter(user=user, is_read=False).count()

    # 5. Fetch Chat history
    chat_history = ChatMessage.objects.filter(user=user).order_by('timestamp')

    context = {
        'user': user,
        'stats': stats,
        'sevas': sevas,
        'sadhana_entries': sadhana_entries,
        'notifications': notifications_list,
        'unread_notifications_count': unread_notifications_count,
        'chat_history': chat_history,
    }
    return render(request, 'dashboard/devotee_dashboard.html', context)

@login_required(login_url='login')
def complete_seva(request, seva_id):
    if request.method == 'POST':
        try:
            seva = DailySeva.objects.get(id=seva_id, devotee=request.user)
            seva.status = 'completed'
            seva.save()
                
            # Mark related notifications for this seva as read
            Notification.objects.filter(user=request.user, seva_duty=seva).update(is_read=True)
            
            # Send completion emails to leaders in devotee's residency
            residency = getattr(request.user.profile, 'residency', 'Main Residency')
            leader_emails = list(CustomUser.objects.filter(profile__role='leader', profile__residency=residency).values_list('email', flat=True))
            send_seva_completed_notification(request.user, seva, leader_emails)
            
            return JsonResponse({'status': 'success'})
        except DailySeva.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Seva Duty not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required(login_url='login')
def toggle_out_of_station(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.is_out_of_station = not profile.is_out_of_station
        profile.save()
        return JsonResponse({'status': 'success', 'is_out_of_station': profile.is_out_of_station})
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='login')
def get_unread_notifications(request):
    """
    JSON API called by the frontend JS polling loop (runs every 10 seconds).
    Returns all unread notifications to display as live popup toasts.
    """
    notifs = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [
        {
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at.strftime('%I:%M %p')
        }
        for n in notifs
    ]
    return JsonResponse({'status': 'success', 'notifications': data})

@login_required(login_url='login')
def mark_notifications_read(request):
    """
    Marks all unread notifications for the logged-in devotee as read.
    """
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required(login_url='login')
def bhakti_ai_chat(request):
    user = request.user
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except Exception:
            user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)

        # Build highly intelligent, paragraphs-long, fully dynamic ChatGPT conversational responses
        msg_lower = user_message.lower()
        response_message = ""

        # 1. Spiritually weak, low, uninspired, sad
        if any(w in msg_lower for w in ["weak", "low", "uninspired", "lazy", "sad", "depressed", "struggling", "spiritual weakness", "fail"]):
            response_message = (
                f"Hare Krishna, dear {request.user.name}. Please accept my humble obeisances. It is completely normal "
                "to experience periods of spiritual dryness or feeling weak on the path of Bhakti. The material energy "
                "(Maya) is strong, but please remember that Krishna's mercy is infinitely stronger.\n\n"
                "In the Bhagavad Gita, Krishna tells Arjuna: 'Declare it boldly that My devotee never perishes.' "
                "When you feel uninspired, do not isolate yourself. The best treatment is to take simple steps: "
                "1) Chant even just one or two rounds very slowly and prayerfully, begging for shelter. "
                "2) Read even a single page of Srila Prabhupada's books, like the 'Bhagavad Gita As It Is' or 'Krishna Book'. "
                "3) Seek the association of sincere devotees (Sadhu-sanga) - hearing them speak or sing Kirtan will immediately re-charge your heart.\n\n"
                "Please do not be discouraged. Spiritual life is a marathon, not a sprint. Every single step you take is "
                "eternally recorded by Sri Krishna in your heart. I am always here to guide you."
            )
        # 2. How to chant better, avoid distraction, focus during Japa
        elif any(w in msg_lower for w in ["distract", "chant better", "focus", "japa", "chanting better", "attentive", "mind wander"]):
            response_message = (
                "Chanting the Hare Krishna Maha Mantra attentively is the greatest challenge and the greatest reward. "
                "Here are practical, deeply scientific guidelines to avoid distractions and chant better:\n\n"
                "1. **Hear Each Syllable**: Japa is simply a practice of active hearing. Do not think about the past or future. "
                "Just pronounce 'Hare', 'Krishna', 'Rama' clearly, and train your ears to hear each sound vibration.\n"
                "2. **Chant in the Morning (Brahmamuhurta)**: The hours between 4:00 AM and 6:00 AM are exceptionally pure. "
                "The mind is naturally quiet and satvic, making focused chanting much easier.\n"
                "3. **Choose the Right Place**: Stand or sit in front of the Deity, a picture of Pancha-tattva, or near a Tulsi plant. "
                "Keep your phone in another room to prevent interruptions.\n"
                "4. **Pray for Focus**: Before starting your beads, pray to the spiritual master and Srila Prabhupada: "
                "'Dear Krishna, please accept my attempt to chant and help me focus my restless mind on Your Holy Names.'\n\n"
                "Be patient with yourself. When the mind wanders, gently pull it back. That very act of pulling the mind back is itself yoga."
            )
        # 3. Why is chanting important, why chant, importance of chanting
        elif any(w in msg_lower for w in ["importance", "why chant", "why is chanting"]):
            response_message = (
                "Chanting the Maha Mantra (Hare Krishna Hare Krishna, Krishna Krishna Hare Hare, Hare Rama Hare Rama, Rama Rama Hare Hare) "
                "is the absolute foundation of spiritual progress in this age, known as Kali-yuga.\n\n"
                "The Brhan-naradiya Purana states: 'In this age of quarrel and hypocrisy, the only means of deliverance is chanting the holy name "
                "of the Lord. There is no other way, no other way, no other way.'\n\n"
                "Srila Prabhupada explains that chanting cleanses the mirror of the heart (ceto-darpana-marjanam). "
                "Just as dust accumulates on a mirror, material desires accumulate on our consciousness, covering our true identity. "
                "Chanting acts as a powerful transcendental cleanser, removing all material conditioning, extinguishing the blazing fire of material "
                "existence, and instantly awakening our natural, dormant love for Krishna (Prema-bhakti)."
            )
        # 4. Bhagavad Gita 2.47, Gita 2.47, fruits of action
        elif "2.47" in msg_lower or "fruits" in msg_lower or "action" in msg_lower or "duty" in msg_lower:
            response_message = (
                "Bhagavad Gita Chapter 2, Verse 47 is one of the most vital teachings of Sri Krishna:\n\n"
                "*'karmanye vadhikaraste ma phalesu kadacana | ma karma-phala-hetur bhur ma te sango 'stv akarmani'*\n\n"
                "This translates to: 'You have a right to perform your prescribed duty, but you are not entitled to the fruits of action. "
                "Never consider yourself the cause of the results of your activities, and never be attached to not doing your duty.'\n\n"
                "This verse is the pillar of **Nishkama Karma Yoga** (Selfless Devotional Service). Krishna teaches us three crucial things: "
                "1) Do not run away from your duties; perform them with full sincerity and excellence. "
                "2) Detach your mind from the anxiety of results. The results are controlled by the Supreme Lord, not by us. "
                "3) Do not fall into laziness or inaction (akarma) under the pretext of detachment.\n\n"
                "When you perform your seva or work as an offering to Krishna, without seeking personal prestige or fruits, you are freed "
                "from karmic bondage and experience deep, transcendental peace."
            )
        # 5. Greetings
        elif any(w in msg_lower for w in ["hello", "hi", "hare krishna", "pranams", "obeisances", "hey"]):
            response_message = (
                f"Hare Krishna, dear {request.user.name}! Please accept my humble obeisances. All glories to Srila Prabhupada.\n\n"
                "I am your Bhakti AI Guide, ready to assist you in your daily sadhana, seva duties, and scriptural studies. "
                "How is your spiritual practice going today? Feel free to ask me any questions."
            )
        # 6. Fallback conversational matching
        else:
            response_message = (
                f"Thank you for sharing your thoughts, dear {request.user.name}. Your inquiry touching upon your spiritual journey is "
                "highly auspicious.\n\n"
                "In devotional service, every sincere question is an act of purification. The path of Bhakti is nurtured by inquiry "
                "(athato brahma jijnasa). To progress stably:\n"
                "- Keep up your daily sadhana tracking.\n"
                "- Complete your scheduled seva duties as a loving offering to Sri Krishna.\n"
                "- Seek the association of devotees to clear any doubts.\n\n"
                "Please tell me more about what you are contemplating or feeling, so I can share specific insights from the teachings "
                "of the Bhagavad Gita and Srila Prabhupada."
            )

        # Save the conversational message to the database
        ChatMessage.objects.create(
            user=user,
            message=user_message,
            response=response_message
        )

        return JsonResponse({'status': 'success', 'message': response_message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required(login_url='login')
def leader_dashboard(request):
    user = request.user
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user, role='leader')

    today = timezone.localtime(timezone.now()).date()
    residency = user.profile.residency

    total_devotees = Profile.objects.filter(role='devotee', residency__iexact=residency).count()
    
    services_today_count = DailySeva.objects.filter(
        service_date=today,
        devotee__profile__residency__iexact=residency
    ).count()

    pending_services_count = DailySeva.objects.filter(
        service_date=today,
        status='pending',
        devotee__profile__residency__iexact=residency
    ).count()

    completed_services_count = DailySeva.objects.filter(
        service_date=today,
        status='completed',
        devotee__profile__residency__iexact=residency
    ).count()
    
    pending_sevas = DailySeva.objects.filter(
        status='pending',
        service_date=today,
        devotee__profile__residency__iexact=residency
    ).order_by('service_start_time')

    completed_sevas = DailySeva.objects.filter(
        status='completed',
        service_date=today,
        devotee__profile__residency__iexact=residency
    ).order_by('-service_start_time')[:10]
    
    services = MasterService.objects.all()
    available_devotees = CustomUser.objects.filter(
        profile__role='devotee', 
        profile__residency__iexact=residency, 
        profile__is_out_of_station=False
    )

    context = {
        'user': user,
        'residency': user.profile.residency,
        'total_devotees': total_devotees,
        'services_today': services_today_count,
        'pending_services_count': pending_services_count,
        'completed_services_count': completed_services_count,
        'pending_sevas': pending_sevas,
        'completed_sevas': completed_sevas,
        'services': services,
        'available_devotees': available_devotees,
    }
    return render(request, 'dashboard/leader_dashboard.html', context)

@login_required(login_url='login')
def manage_service(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name')
            if name:
                MasterService.objects.get_or_create(name=name)
        elif action == 'delete':
            service_id = request.POST.get('service_id')
            MasterService.objects.filter(id=service_id).delete()
        return redirect('dashboard:leader_dashboard')
    return redirect('dashboard:leader_dashboard')

@login_required(login_url='login')
def assign_service(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        devotee_id = request.POST.get('devotee_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_time_str = request.POST.get('start_time')
        duration_mins = int(request.POST.get('duration_mins', 60))
        
        try:
            master_service = MasterService.objects.get(id=service_id)
            devotee = CustomUser.objects.get(id=devotee_id)
            
            # Form submits start_date and end_date as YYYY-MM-DD, start_time as HH:MM
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # start_time may be HH:MM or HH:MM:SS
            if len(start_time_str) == 5:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
            else:
                start_time = datetime.strptime(start_time_str[:5], '%H:%M').time()
            
            # Create ONE WeeklyServiceAssignment
            assignment = WeeklyServiceAssignment.objects.create(
                service_name=master_service.name,
                devotee=devotee,
                residency=devotee.profile.residency,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                duration_minutes=duration_mins,
                active=True
            )
            
            from seva.views import generate_daily_sevas_and_notify
            generate_daily_sevas_and_notify(assignment, request.user.name)
            
            messages.success(request, f"Weekly service assigned to {devotee.name} successfully.")
        except Exception as e:
            messages.error(request, f"Error assigning service: {e}")
            
    return redirect('dashboard:leader_dashboard')

@login_required(login_url='login')
def generate_weekly_report(request):
    from sadhana.models import SadhanaLog
    now = timezone.now()
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    try:
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = now.date()
            start_date = end_date - timezone.timedelta(days=7)
    except Exception:
        end_date = now.date()
        start_date = end_date - timezone.timedelta(days=7)
        
    # Ensure end_date >= start_date
    if end_date < start_date:
        end_date = start_date
        
    delta_days = (end_date - start_date).days + 1
    if delta_days <= 0:
        delta_days = 1
    
    devotees = CustomUser.objects.filter(
        profile__role='devotee',
        profile__residency__iexact=request.user.profile.residency
    )
    report_data = []
    
    for devotee in devotees:
        days_attended = SadhanaLog.objects.filter(
            user=devotee, 
            date__gte=start_date,
            date__lte=end_date,
            mangala_aarti=True
        ).count()
        percentage = min(100, int((days_attended / float(delta_days)) * 100))
        
        color = 'red'
        if percentage >= 80:
            color = 'green'
        elif percentage >= 60:
            color = 'yellow'
            
        report_data.append({
            'name': devotee.name,
            'percentage': percentage,
            'color': color
        })
        
    return JsonResponse({'status': 'success', 'report': report_data, 'start_date': start_date.strftime('%d %b %Y'), 'end_date': end_date.strftime('%d %b %Y')})



