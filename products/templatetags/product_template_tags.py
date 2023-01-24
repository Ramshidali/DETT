from django import template

register = template.Library()


@register.simple_tag
def get_age_group(age_group):
    """
    for converting age groups code to readable one
    :param age_group:
    :return:
    """
    if '10' in age_group:
        return "0-9"
    elif '20' in age_group:
        return "10-19"
    elif '30' in age_group:
        return "20-29"
    elif '40' in age_group:
        return "30-39"
    elif '50' in age_group:
        return "40-49"
    elif '60' in age_group:
        return "50-59"
    elif '70' in age_group:
        return "60-69"
    elif '80' in age_group:
        return "70-79"
    elif '90' in age_group:
        return "80 and above"
