from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)


@register.filter(name='lookup')
def lookup(dict,key):
	return dict[key]
	
@register.filter(name='list_val')
def list_val(lis,pos):
	return lis[pos]