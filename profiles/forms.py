from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    # call the default init method to set the form up as it would be by default
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # create a dictionary of placeholders which will show up in the form fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }
        # setting the autofocus attribute on the full name field to True so the cursor will-
        # start in the full name field when the page loads
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # iterating through the form felds
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    # adding a * to the placeholder if it is a required field
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # setting the placeholders to their values in the dictionary
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Stripe
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # removing the form field labels
            self.fields[field].label = False
