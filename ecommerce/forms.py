from django import forms

class Contact_Form(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Enter Your Name...."
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Enter Your Email Address...."
            }
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "placeholder":"Enter Your Message...."
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError(" Email Address must be G mail. ")
        return email

    # def clean_message(self):
    #     raise forms.ValidationError("Try Error")
