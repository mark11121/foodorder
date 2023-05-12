from django import forms

class SearchForm(forms.Form):
    def __init__(self, model, fields, label_suffixes=None, initial_data=None, category_fields=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.fields_to_search = fields
        self.category_fields = category_fields

        for field_name in self.fields_to_search:
            label = label_suffixes.get(field_name, field_name)
            self.fields[field_name] = forms.CharField(
                required=False, label=label
            )

        if initial_data:
            self.data = initial_data

    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.fields:
            if field_name in cleaned_data:
                cleaned_data[field_name] = cleaned_data[field_name].strip()
        return cleaned_data

    def search(self):
        query = {}
        for field_name in self.fields_to_search:
            value = self.cleaned_data.get(field_name, '').strip()
            if value:
                if field_name in self.category_fields:
                    query[f'{field_name}__name__icontains'] = value
                else:
                    query[f'{field_name}__icontains'] = value

        return self.model.objects.filter(**query)