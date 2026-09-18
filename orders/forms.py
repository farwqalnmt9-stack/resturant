from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    location_method = forms.ChoiceField(
        choices=(('map', 'تحديد من الخريطة'), ('manual', 'إدخال العنوان يدويًا')),
        initial='map',
        widget=forms.RadioSelect,
        label='طريقة تحديد الموقع',
    )

    class Meta:
        model = Order
        fields = ['phone', 'delivery_address', 'delivery_latitude', 'delivery_longitude']
        labels = {'phone': 'رقم الهاتف', 'delivery_address': 'العنوان'}
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'مثال: 09XX XXX XXX', 'inputmode': 'tel', 'autocomplete': 'tel'}),
            'delivery_address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'اكتب الحي والشارع وأي وصف يساعد السائق على الوصول إليك', 'autocomplete': 'street-address'}),
            'delivery_latitude': forms.HiddenInput(), 'delivery_longitude': forms.HiddenInput(),
        }

    def clean(self):
        data = super().clean()
        if data.get('location_method') == 'map':
            if data.get('delivery_latitude') is None or data.get('delivery_longitude') is None:
                self.add_error('delivery_latitude', 'يرجى تحديد موقع التوصيل على الخريطة.')
        elif not data.get('delivery_address', '').strip():
            self.add_error('delivery_address', 'يرجى كتابة عنوان التوصيل.')
        return data
