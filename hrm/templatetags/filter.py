from django import template
register = template.Library()


@register.filter(name='image_value')
def image_value(value):
	return str(value).endswith(('.png','.jpg','.jpeg','.gif','JPG','JPEG','jfif'))


@register.filter(name='is_list')
def is_list(value):
	return isinstance(value, list)