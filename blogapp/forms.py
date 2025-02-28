from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Email'})
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a message (optional)', 'rows': 3})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        to = cleaned_data.get("to")

        if email and to and email == to:
            raise forms.ValidationError("Sender and recipient emails cannot be the same.")

        return cleaned_data
