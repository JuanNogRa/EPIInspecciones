from django import template
import re
from django.utils.safestring import mark_safe
from django import template
from django.contrib.auth.models import Group 

register = template.Library()


@register.filter(name ='add')

def add(html_input, properties):
    """
    Inserta propiedades en un campo html.

    Uso: {{ form.field_name|add:'class="form-control" placeholder="Placeholder here"' }}
    """
    pattern = r'(\s\/>|>)'
    regex = re.compile(pattern, re.IGNORECASE)
    replace = ' {0}>'.format(properties)
    html = regex.sub(replace, str(html_input))
    
    return mark_safe(html)



@register.filter(name='is_group') 
def is_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name) 
        
        return group in user.groups.all() 
    
    except Group.DoesNotExist:
        
        return False

@register.filter(name='update_variable')
def update_variable(html_input, value):
    data = value
    return data

# @register.filter(name='addclass')

# def addclass(value, arg):

#     return value.as_widget(attrs={'class': arg})

# @register.filter(name='addplaceholder')

# def addplaceholder(value, arg):

#     return value.as_widget(attrs={'placeholder': arg})



# @register.filter(name='addautofocus')

# def addautofocus(value, arg):

#     return value.as_widget(attrs={'autofocus': arg})