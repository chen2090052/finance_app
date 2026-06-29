from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["type", "category", "amount", "date", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "type": "类型",
            "category": "分类",
            "amount": "金额",
            "date": "日期",
            "note": "备注",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        transaction_type = self.data.get("type") or self.initial.get("type")
        if not transaction_type and self.instance.pk:
            transaction_type = self.instance.type
        if transaction_type:
            self.fields["category"].queryset = Category.objects.filter(
                type=transaction_type, is_deleted=False
            )
        else:
            self.fields["category"].queryset = Category.objects.filter(
                is_deleted=False
            )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("金额必须大于0")
        return amount


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type", "icon", "sort_order"]
        labels = {
            "name": "分类名称",
            "type": "类型",
            "icon": "图标",
            "sort_order": "排序",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
