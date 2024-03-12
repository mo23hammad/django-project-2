from django import forms

class AddCartForm(forms.Form):
    quantity = forms.IntegerField(max_value=9,min_value=1)

class CouponForm(forms.Form):
    code = forms.CharField(label='discount code',max_length=100)