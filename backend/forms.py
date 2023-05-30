from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from backend.models import *

from django.urls import reverse_lazy


class GenerateTradeModelForm(ModelForm):
    class Meta:
        model = GenerateTradeModel
        # fields = "__all__"
        exclude = ('Attach_file','Trade_id','Status')


class TestBlotterForm(ModelForm):
    class Meta:
        model = TestBlotter
        fields = "__all__"

        widgets = {
            'Book': forms.Select(attrs={'class': 'form-control', 'id': 'Book'}),
            'Contract_name': forms.Select(attrs={'class': 'form-control', 'id': 'Contract_name'}),

        }

class FutureLTDForm(ModelForm):
    class Meta:
        model = FutureLTD
        fields = "__all__"

        widgets = {
            'Contract_symbol': forms.DateInput(attrs={'class': 'form-control', 'id': 'Contract_symbol', 'type': 'date'}),
            'Ls_gas_oil': forms.DateInput(attrs={'class': 'form-control', 'id': 'Ls_gas_oil', 'type': 'date'}),
            'Brent_crude_futures': forms.DateInput(attrs={'class': 'form-control', 'id': 'Brent_crude_futures', 'type': 'date'}),
            'RBOB_Gasoline_futures': forms.DateInput(attrs={'class': 'form-control', 'id': 'RBOB_Gasoline_futures', 'type': 'date'}),
            'Heating_oil_futures': forms.DateInput(attrs={'class': 'form-control', 'id': 'Heating_oil_futures', 'type': 'date'}),
            'WTI_crude_futures': forms.DateInput(attrs={'class': 'form-control', 'id': 'WTI_crude_futures', 'type': 'date'}),
        }




# class CustomerCompanyForm(ModelForm):
#     class Meta:
#         model = CustomerCompanyModel
#         # fields = "__all__"
#         exclude = ('Attach_file',)


# class CustomerAccountsForm(ModelForm):
#     class Meta:
#         model = CustomerAccountsModel
#         fields = "__all__"
#
#         widgets = {
#             'Customer_Company': forms.Select(attrs={'class': 'form-control', 'id': 'Customer_Company'}),
#             'Account': forms.TextInput(attrs={'class': 'form-control', 'id': 'Account'}),
#             'Cash_Factor': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Cash_Factor'}),
#
#         }


class CompanyInvestmentForm(ModelForm):
    class Meta:
        model = CompanyInvestmentModel
        fields = "__all__"

        widgets = {
            'Customer_Company_name':forms.TextInput(attrs={'class': 'form-control', 'id': 'Customer_Company_name'}),
            'Customer_Account': forms.TextInput(attrs={'class': 'form-control', 'id': 'Customer_Account'}),
            'Transfer_Amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Transfer_Amount'}),
            'Cash_Factor': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Cash_Factor'}),
            'Customer_Transfer_Type': forms.Select(attrs={'class': 'form-control', 'id': 'Customer_Transfer_Type'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'Email','placeholder':"enter email"}),
            'Remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'Remarks'}),
        }

#
# class FuturesBlottersForm(ModelForm):
#     class Meta:
#         model = FuturesBlottersModel
#         # fields = "__all__"
#         exclude = ('Unit','Clearer_rate','Exchange_rate','Brokerage','Total_Fee','Holiday', "bbl_mt_conversion",'kbbl_mt_conversion')
#
#         widgets = {
#             # 'Date':forms.DateField(widget=forms.DateInput(attrs={'type':'date'})),
#             'Date': forms.DateInput(attrs={'class': 'form-control', 'id': 'Date', 'type': 'date'}),
#             'Trade_Type': forms.Select(attrs={'class': 'form-control', 'id': 'Trade_Type', 'label': 'Select'}),
#             'Clearer': forms.Select(attrs={'class': 'form-control', 'id': 'Clearer','placeholder':'Clearer'}),
#             'Trader': forms.Select(attrs={'class': 'form-control', 'id': 'Trader'}),
#             'Book': forms.Select(attrs={'class': 'form-control', 'id': 'Book'}),
#             'Customer_Company': forms.Select(attrs={'class': 'form-control', 'id': 'Customer_Company'}),
#             'Account': forms.Select(attrs={'class': 'form-control', 'id': 'Account'}),
#             'Strategy': forms.Select(attrs={'class': 'form-control', 'id': 'Strategy'}),
#             'Buy_Sell': forms.TextInput(attrs={'class': 'form-control', 'id': 'Buy_Sell'}),
#             'Volume': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Volume'}),
#             'Contract_Name': forms.Select(attrs={'class': 'form-control', 'id': 'Contract_Name'}),
#
#
#             'Contract_Month': forms.DateInput(attrs={'class': 'form-control', 'id': 'Contract_Month', 'type': 'date'}),
#             'Price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Price'}),
#             'Type': forms.Select(attrs={'class': 'form-control', 'id': 'Type'}),
#             'Approximate_EP': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Approximate_EP'}),
#
#             'EFS_Code': forms.NumberInput(attrs={'class': 'form-control', 'id': 'EFS_Code'}),
#             'Broker': forms.Select(attrs={'class': 'form-control', 'id': 'Broker'}),
#             'Notes': forms.TextInput(attrs={'class': 'form-control', 'id': 'Notes', 'row': 2}),
#
#         }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['Account'].queryset = CustomerAccountsModel.objects.none()

