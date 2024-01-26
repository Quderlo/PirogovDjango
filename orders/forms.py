from django import forms
from .models import Directory, Client, Order, Progress


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'type']
        labels = {
            'name': 'Название',
            'type': 'Тип',
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'second_name', 'address', 'telephone']
        labels = {
            'first_name': 'Имя',
            'second_name': 'Фамилия',
            'address': 'Адрес',
            'telephone': 'Телефон',
        }


class OrderForm(forms.ModelForm):
    directory = forms.ModelChoiceField(
        queryset=Directory.objects.all(),
        widget=forms.Select(attrs={'onchange': 'check_selection(this);'}),
        required=False,
    )
    create_new_directory = forms.BooleanField(
        label='Создать новую технику',
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'toggle_new_directory();'}),
    )
    new_directory_name = forms.CharField(label='Новая техника (название)', required=False)
    new_directory_type = forms.CharField(label='Тип новой техники', required=False)
    new_total_cost = forms.DecimalField(label='Новая стоимость', required=False)

    class Meta:
        model = Order
        fields = ['description', 'total_cost', 'serial_number', 'directory', 'client']
        labels = {
            'description': 'Описание',
            'total_cost': 'Примерная начальная стоимость',
            'serial_number': 'Серийный номер',
            'directory': 'Техника',
            'client': 'Клиент',
        }

    def clean(self):
        cleaned_data = super().clean()
        directory = cleaned_data.get('directory')
        create_new_directory = cleaned_data.get('create_new_directory')
        new_directory_name = cleaned_data.get('new_directory_name')
        new_directory_type = cleaned_data.get('new_directory_type')

        if not directory and create_new_directory and not (new_directory_name and new_directory_type):
            raise forms.ValidationError('Если создаете новую технику, укажите название и тип')

        return cleaned_data


class SearchOrderForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Поиск по клиенту или работнику')


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(choices=Progress.ORDER_STATUS_CHOICES),
        }
        labels = {
            'status': 'Статус',
            'notes': 'Заметки',
        }

class UpdateOrderCostForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_cost']