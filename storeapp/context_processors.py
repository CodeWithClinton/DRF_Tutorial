from .models import Cart
import uuid

def cart_renderer(request):
      try:
         cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
      except:
         request.session['nonuser'] = str(uuid.uuid4())
         cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
         
      return {
         'cart': cart
      }