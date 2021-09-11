from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # call the default init method to set the form up as it would be by default
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # create a dictionary of placeholders which will show up in the form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }
        # setting the autofocus attribute on the full name field to True so the cursor will-
        # start in the full name field when the page loads
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # iterating through the form felds
        for field in self.fields:
            if self.fields[field].required:
                # adding a * to the placeholder if it is a required field
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # setting the placeholders to their values in the dictionary
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Stripe
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # removing the form field labels
            self.fields[field].label = False
