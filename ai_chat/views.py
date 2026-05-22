from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ChatMessage
import json
import openai

@login_required(login_url='login')
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except Exception:
            user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)

        user = request.user
        
        # Build chat context from database history
        past_messages = ChatMessage.objects.filter(user=user).order_by('timestamp')[:10]
        
        messages = [
            {"role": "system", "content": f"You are the Bhakti AI Guide, a deeply compassionate, wise, and spiritual chatbot for the BhaktiVerse devotee dashboard. You help devotees with their daily sadhana (spiritual practice), philosophical questions based on Bhagavad Gita and Srila Prabhupada's teachings, and emotional support. The user's name is {user.name}. Keep responses highly empathetic, profound, and formatted with clear paragraphs."}
        ]

        for msg in past_messages:
            messages.append({"role": "user", "content": msg.message})
            messages.append({"role": "assistant", "content": msg.response})

        # Append current message
        messages.append({"role": "user", "content": user_message})

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            ai_response = response.choices[0].message.content.strip()
            
            # Save the new message to history
            ChatMessage.objects.create(
                user=user,
                message=user_message,
                response=ai_response
            )

            return JsonResponse({'status': 'success', 'message': ai_response})

        except Exception as e:
            print(f"OpenAI API Error: {e}")
            fallback_msg = "Hare Krishna! My connection to the spiritual ether (OpenAI API) is currently down or misconfigured. Please ask your Temple Leader to configure the OPENAI_API_KEY in settings.py."
            return JsonResponse({'status': 'error', 'message': fallback_msg})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
