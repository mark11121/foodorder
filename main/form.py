from django import forms

SEARCH_CHOICES = [
    ('', ''),
    ('NOT', '排除'),
    ('%', '任意搜尋'),
    ('=" "', '=空白'),
    ('<>" "', '!=空白'),
]



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
            # 將每個欄位前面的下拉選單設置為不需要驗證
            self.fields[f'select_{field_name}'] = forms.ChoiceField(required=False)

        if initial_data:
            self.data = initial_data

    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.fields:
            if field_name.startswith('select_'):
                continue  # 跳過下拉選單欄位
            if field_name in cleaned_data:
                cleaned_data[field_name] = cleaned_data[field_name].strip()
        return cleaned_data

    def search(self):
        query = {}
        for field_name in self.fields_to_search:
            value = self.cleaned_data.get(field_name, '').strip()
            select_value = self.cleaned_data.get(f'select_{field_name}')
            if value and select_value:
                if field_name in self.category_fields:
                    query[f'{field_name}__name__icontains'] = value
                    query[f'{field_name}__category__exact'] = select_value
                else:
                    query[f'{field_name}__icontains'] = value

        return self.model.objects.filter(**query)