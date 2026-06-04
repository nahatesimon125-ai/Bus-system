from .models import CustomerUser

def current_user(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = CustomerUser.objects.get(id=user_id)
        except CustomerUser.DoesNotExist:
            pass
    return {'current_user': user}
