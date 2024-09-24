from django import template # Importing the template module

register = template.Library() # Creating a template library

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)  # Returning the value for the specified key

@register.filter
def get_category_transactions(categorised_transactions, category_name):
    if not isinstance(categorised_transactions, dict):
        raise ValueError("categorised_transactions should be a dictionary")
 
    return categorised_transactions.get(category_name, []) # Returning transactions for the category
