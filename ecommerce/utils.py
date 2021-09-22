from django.utils.text import slugify
import random, string

def rand_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = instance.title
    
    Klass = instance.__class__  
    qs_exist = Klass.objects.filter(slug=slug).exists()
    if qs_exist:
        new_slug = f"{slug}-{rand_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug 
    

def unique_order_id_generator(instance,): 
    order_id = rand_string_generator().upper()
    Klass = instance.__class__  
    qs_exist = Klass.objects.filter(order_id=order_id).exists()
    if qs_exist:
        return unique_slug_generator(instance)
    return order_id 