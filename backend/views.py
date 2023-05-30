from django.shortcuts import render, redirect
from .urls import *
from .forms import *
from django.views import View
from .email import Email
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from .models import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
import pandas as pd
from django.http import JsonResponse
import json
from .models import Type as TYPEMODEL
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
from .forms import *
import random
import numpy as np
import calendar
from datetime import datetime
from datetime import date
from datetime import timedelta
from functools import reduce

from .filters import HistoryFilter
import json
import csv
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission
from django.utils.decorators import method_decorator
import sys
import asyncio


class Login(View):
    def get(self,request):
        print('0qqqq00000000qqqq000')
        return render(request,"auth-signin-basic.html")
    
    def post(self,request):
        user = Email.authenticate(self,username=request.POST['email'], password=request.POST['password'])
        print(request.POST['email'])
        print(request.POST['password'])
        if user is not None:
            login(request, user)
            if user.user_type == '0':
                return HttpResponseRedirect('customer-dashboard')
            elif user.user_type == '1':
                return HttpResponseRedirect('customer-dashboard')
        else:
            return render(request,"auth-signin-basic.html")


class AdminLogin(View):
    def get(self, request):
        print('0qqqq00000000qqqq000')
        return render(request, "admin-auth-signin-basic.html")

    def post(self, request):
        user = Email.authenticate(self, username=request.POST['email'], password=request.POST['password'])
        print(request.POST['email'])
        print(request.POST['password'])
        if user is not None:
            login(request, user)
            if user.user_type == '0':
                return HttpResponseRedirect('index')
            elif user.user_type != '0':
                messages.error(request, "Invalid admin")
                return HttpResponseRedirect('/')
        else:
            return render(request, "auth-signin-basic.html")




class CustomerDashboard(View):
    def get(self, request):
        return render(request,"customer/customer_dashboard.html")

        
class Index(View):
    def get(self, request):
        return render(request,"index.html")


class CustomLogoutView(LogoutView):
    def get(self, request):
        return render(request, "logout.html")
    # next_page = reverse_lazy('backendapp:login')


    
#_________________________________Check if the users is authenticated _____________________________________________________

class CheckUserMixins(LoginRequiredMixin):
        login_url = '/'
        permission_denied_message = "Unusual Activity Detected. Please Login to continue!"
        raise_exception = False

#_________________________________Traders-->(CRUD)_____________________________________________________

class TraderModdal(View):
    model=Traders
    feilds="__all__"
    success_url=reverse_lazy('backendapp:addtraders')
    
class AddTraders(CheckUserMixins,TraderModdal, ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Trader Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file:
            # Creating objects with file upload
            try:
                print("helo file")
                print("file", file)
                df = pd.read_csv(file, usecols=['Trader' or 'trader'])
                print("read csv", df)
                if len(df) > 0:
                    for i, name in df.iterrows():
                        print("i", i)
                        print("name", name)
                        obj = self.model.objects.create(name=name['Trader'])
                        obj.save()
                    messages.info(request, f"Added {len(df)} Trader")
                else:
                    messages.error(request, "There are no values in file")
            except:

                messages.info(request, "Error ❌ Column Traders not Found")
        return HttpResponseRedirect('/add-trader')
    
class TradersDetail(CheckUserMixins, TraderModdal, DetailView):
    """ Traders Detail View"""
    
#_______________________________________Book--->(CRUD)_______________________________________________________________


class AddBookModal(View):
        model=Book
        feilds="__all__"
        success_url=reverse_lazy('backendapp:addbook')
        
class AddBook(CheckUserMixins,AddBookModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Trader Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Book'or'book' ])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Book'or'book'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Book")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Book not Found")
        return HttpResponseRedirect('/add-book')
    

class BooksDetail(CheckUserMixins, AddBookModal, DetailView):
    """        """
    
    
#_______________________________________Product--->(CRUD)_______________________________________________________________


class ProductModal(View):
        model=Product
        feilds="__all__"
        success_url=reverse_lazy('backendapp:addproduct')
        
class AddProduct(CheckUserMixins,ProductModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Trader Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Product'or'product'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Product'or'product'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Product")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Product not Found")
        return HttpResponseRedirect('/add-product')
    

class ProductDetails(CheckUserMixins, ProductModal, DetailView):
    """        """
    
    

#_______________________________________Strategy--->(CRUD)_______________________________________________________________


class StrategyModal(View):
        model=Strategy
        feilds="__all__"
        success_url=reverse_lazy('backendapp:addstrategy')
        
class AddStrategy(CheckUserMixins,StrategyModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Strategy' or 'strategy' ])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Strategy' or 'strategy'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Strategy")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Strategy not Found")
        return HttpResponseRedirect('/add-strategy')
    

class StrategyDetails(CheckUserMixins, StrategyModal, DetailView):
    """  """
    
    
#_______________________________________Derivative--->(CRUD)_______________________________________________________________


class DerivativeModal(View):
        model=DerivativeM
        feilds="__all__"
        success_url=reverse_lazy('backendapp:derivative')
        
class Derivative(CheckUserMixins,DerivativeModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
           try:
                df = pd.read_csv(file,usecols=['Derivative'or'derivative'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Derivative'or'derivative'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Derivative")
                else:
                    messages.error(request, "There are no values in file")
           except:
                messages.info(request, "Error ❌ Column Derivative not Found")
        return HttpResponseRedirect('/add-derivative')
    

class DerivativeDetails(CheckUserMixins, DerivativeModal, DetailView):
    """  """
    
    
    
#_______________________________________Type--->(CRUD)_______________________________________________________________


class TypeModal(View):
        model=Type
        feilds="__all__"
        success_url=reverse_lazy('backendapp:type')
        
class Type(CheckUserMixins,TypeModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Type'or'type'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Type'or'type'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Type")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Type not Found")
        return HttpResponseRedirect('/add-type')
    

class TypeDetails(CheckUserMixins, TypeModal, DetailView):
    """  """
    
    
#_______________________________________Unit--->(CRUD)_______________________________________________________________


class unitModal(View):
        model=Unit1
        feilds="__all__"
        success_url=reverse_lazy('backendapp:type')
        
class Unit(CheckUserMixins,unitModal,ListView):
    template_name="backend/unit_list.html"
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Unit'or'unit'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Unit'or'unit'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Unit")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Unit not Found")
        return HttpResponseRedirect('/add-unit')
    

class UnitDetails(CheckUserMixins, unitModal, DetailView):
    template_name="backend/unit_detail.html"
    """ """


#_______________________________________Broker--->(CRUD)_______________________________________________________________


class BrokerModal(View):
        model=BrokerM
        feilds="__all__"
        success_url=reverse_lazy('backendapp:broker')
        
class Broker(CheckUserMixins,BrokerModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Broker'or'broker'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Broker'or 'broker'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Broker")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Broker not Found")
        return HttpResponseRedirect('/add-broker')
    

class BrokerDetails(CheckUserMixins, BrokerModal, DetailView):
    """ """
    



#_______________________________________Clearer--->(CRUD)_______________________________________________________________


class ClearerModal(View):
        model=ClearearM
        feilds="__all__"
        success_url=reverse_lazy('backendapp:clearer')
        
class Clearer(CheckUserMixins,ClearerModal,ListView):
    paginate_by=10
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
 # create Traders
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: # editng a object
            trader = self.model.objects.get(id=edit_name_id)
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['Clearer'or'clearer'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Clearer'or 'clearer'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Clearer")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column Clearer not Found")
        return HttpResponseRedirect('/add-clearer')
    

class ClearerDetails(CheckUserMixins, ClearerModal, DetailView):
    """ """
    
#___________________________________Contract CRUD________________________________________________________________

class Contract(CheckUserMixins,View):
    
    def get(self, request):

        datelist=[]
        date = HolidayM.objects.all().values('name')
        print("date:",type(date))

        for i in HolidayM.objects.all().values('name'):

            if i not in datelist:
                datelist.append(i)

        print("datelist:",datelist)

        print("datett:",date)
        data = json.dumps(list(datelist))
        contract_name = ContractM.objects.all().values('contract_name')
        unit = Unit1.objects.all()
        print(data,'-------------json')
        # all = ContractM.objects.all()

        search_query = request.GET.get('search_query')
        print("search_query", search_query)
        if search_query =='Futures':
            search_query ='features'

        if search_query:
            all = ContractM.objects.filter(
                Q(contract_name__istartswith=search_query)|Q(gmifc_code__istartswith=search_query)|
                Q(contract1__istartswith=search_query)|Q(contract2__istartswith=search_query)|
                Q(derivative__istartswith=search_query) | Q(single_dif__istartswith=search_query) |
                Q(major_mini__istartswith=search_query) | Q(major_mini_conn__istartswith=search_query) |
                Q(unit__istartswith=search_query) | Q(tick__istartswith=search_query) |
                Q(holiday__istartswith=search_query) | Q(bbi_mt_conversion__istartswith=search_query) |
                Q(f_w_months__istartswith=search_query) | Q(exchange_fee__istartswith=search_query) |
                Q(exchanging_clearing_fee__istartswith=search_query) | Q(block_fee__istartswith=search_query) |
                Q(screen_fee__istartswith=search_query) | Q(physical_code__istartswith=search_query) |
                Q(logical_code__istartswith=search_query) | Q(symbol_code__istartswith=search_query)

            )
        else:
            all = ContractM.objects.all()

        print("all:",all)
        paginator = Paginator(all,20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"backend/contractm_list.html",{'date':data,'contract_name':contract_name, 'object_list':all,'page_obj': page_obj,'unit':unit})
    
    def post(self, request):
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj=ContractM.objects.get(id=delet_id)
            obj.delete()
            messages.info(request,"Deleted")
            return HttpResponseRedirect('/add-contract')
        else:
            contract_name = request.POST.get('contract_name')
            swaps_features = request.POST.get('swaps_features')
            single_diff = request.POST.get('single_diff')
            major_mini_option = request.POST.get('major_mini_option')
            option1contract = request.POST.get('option1contract')
            option2contract = request.POST.get('option2')
            major_mini = request.POST.get('major_mini')
            print(major_mini)
            print('**********************************')
            unit = request.POST.get('unit')
            tick = request.POST.get('tick')
            holiday = request.POST.get('holiday')
            bbimit_converter = request.POST.get('bbimit_converter')
            f_w_months = request.POST.get('f_w_months')
            exchangeFee = request.POST.get('exchangeFee')
            exchangeClearanceFee = request.POST.get('exchangeClearanceFee')
            blockFee = request.POST.get('blockFee')
            screenFee = request.POST.get('screenFee')
            gmifc_code  =request.POST.get('gmifc_code')
            physical_code  =request.POST.get('physical_code')
            logical_code  =request.POST.get('logical_code')
            symbol_code  =request.POST.get('symbol_code')
            obj = ContractM(derivative=swaps_features,single_dif=single_diff,major_mini=major_mini_option,contract_name=contract_name,
                            contract1=option1contract, contract2=option2contract,major_mini_conn=major_mini, unit=unit, tick=tick,
                            holiday=holiday,bbi_mt_conversion=bbimit_converter, f_w_months=f_w_months,exchange_fee=exchangeFee,
                            exchanging_clearing_fee=exchangeClearanceFee, block_fee=blockFee, screen_fee=screenFee,
                            gmifc_code=gmifc_code, physical_code=physical_code, logical_code=logical_code, symbol_code=symbol_code)
            obj.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect('/add-contract')

class EditContract(CheckUserMixins,View):
    def get(self,request,**kwargs):
        object = ContractM.objects.get(id=kwargs['id'])
        date = HolidayM.objects.all().values('name')
        print(type(date))
        data = json.dumps(list(date))
        contract_name = ContractM.objects.all().values('contract_name')
        print(data,'-------------json')
        all = ContractM.objects.all()
        return render(request,"backend/edit_contract.html",{"object":object,'date':data,'contract_name':contract_name, 'object_list':all})
    
    def post(self, request, **kwargs):
        object = ContractM.objects.get(id=kwargs['id'])
        # contract_name = request.POST.get('contract_name')
        # derivative = request.POST.get('swaps_features')
        # print("derivative:",derivative)
        # single_diff = request.POST.get('single_diff')
        # major_mini_option = request.POST.get('major_mini_option')
        # option1contract = request.POST.get('option1contract')
        # option2contract =  request.POST.get('option2')
        # major_mini = request.POST.get('major_mini_conn')
        # unit = request.POST.get('unit')
        # tick = request.POST.get('tick')
        # holiday = request.POST.get('holiday')
        # bbimit_converter = request.POST.get('bbimit_converter')
        #
        # f_w_months = request.POST.get('f_w_months')
        # exchangeFee = request.POST.get('exchangeFee')
        # exchangeClearanceFee = request.POST.get('exchangeClearanceFee')
        # blockFee = request.POST.get('blockFee')
        # screenFee = request.POST.get('screenFee')
        # gmifc_code = request.POST.get('gmifc_code')
        #
        #
        # physical_code = request.POST.get('physical_code')
        # logical_code = request.POST.get('logical_code')
        # symbol_code = request.POST.get('symbol_code')

        object.contract_name = request.POST.get('contract_name')
        object.derivative = request.POST.get('swaps_features')
        object.single_dif = request.POST.get('single_diff')
        object.major_mini = request.POST.get('major_mini_option')
        object.contract1 = request.POST.get('option1contract')
        object.contract2 = request.POST.get('option2')
        object.major_mini_conn = request.POST.get('major_mini_conn')
        object.unit = request.POST.get('unit')
        object.tick = request.POST.get('tick')
        object.holiday = request.POST.get('holiday')
        object.bbi_mt_conversion = request.POST.get('bbimit_converter')
        object.f_w_months = request.POST.get('f_w_months')
        object.exchange_fee = request.POST.get('exchangeFee')
        object.exchanging_clearing_fee = request.POST.get('exchangeClearanceFee')
        object.block_fee = request.POST.get('blockFee')
        object.screen_fee = request.POST.get('screenFee')
        object.gmifc_code  =request.POST.get('gmifc_code')
        object.physical_code  =request.POST.get('physical_code')
        object.logical_code  =request.POST.get('logical_code')
        object.symbol_code  =request.POST.get('symbol_code')
        object.save()


        # ContractM.objects.filter(id=object).update(derivative=derivative,
        #                                                              contract_name=contract_name,
        #                                                              single_dif=single_diff,major_mini=major_mini_option,
        #                                                              contract1=option1contract,
        #                                                              Premium_discount=premium_discount,
        #                                                              Pricing_term=pricing_term,
        #                                                              bl_date=bl_date,
        #                                                              start_date=start_date, end_date=end_date,
        #                                                              Holiday=holiday,Delivery_mode=deliverymode,
        #                                                              Port=port, Terminal=terminal,
        #                                                              Vessal_name=vessal_name, Tank=tank,
        #                                                              Remarks=Remarks,External_Terminal=external_terminal,Headging=hedging,
        #                                                              # calculated and_ get_values
        #                                                              price_days=priced_days, unprice_days=unpriced_days,
        #                                                              Total_no_days=total_working_days,
        #                                                              total_volume=total_volume,
        #                                                              price_volume=priced_volume,
        #                                                              unprice_volume=unpriced_volume,m3=m3,
        #                                                              )





        messages.success(request,"Edited Successfully")
        return HttpResponseRedirect('/add-contract')


class Holiday(CheckUserMixins, ListView):
    model = HolidayM
    paginate_by=25
    # view all Traders
    def get_queryset(self):
        search_query=self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()
    def post(self,request, *args, **kwargs):
        name = request.POST.get('name')
        date = request.POST.get('date')
        edit_date = request.POST.get('edit_date')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name: # Creating a object
            obj=self.model.objects.create(name=name,date=date)
            obj.save()
            messages.success(request,'Successfully Created')
        elif edit_name: 
            trader = self.model.objects.get(id=edit_name_id)
            if edit_date:
                trader.date=edit_date # editng a object           
            trader.name=edit_name
            trader.save()
            messages.success(request,'Edited Successfully')
        elif delet_id: # deleting a object
            trader = self.model.objects.get(id=delet_id)
            trader.delete()
            messages.success(request,'Deleted Successfully')
        elif file: # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['name','holiday'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['name','holiday'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Holiday")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Column name and holiday not Found")
        return HttpResponseRedirect('/add-holiday')
    

class AllHoliday(View):
    def post(self, request):
        print('reached')
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        option1 = data_dict.get('option1contract')
        option2 = data_dict.get('option2')
        print(option1)
        print(option2)
        data = ContractM.objects.filter(Q(contract_name=option1)|Q(contract_name=option2))
        a = list()
        for data in data :
            c =dict(holiday = data.holiday)
            a.append(c)
        print(a)
        serializer_data = {'options':a}
        print(serializer_data)
        print('#########################################')
        return JsonResponse(serializer_data, safe=False)
    

class ClearerRateModel(View):
    model=ClearerRateM
    feilds="__all__"
    success_url=reverse_lazy('backendapp:clearer')
    
class ClearerRate(CheckUserMixins,ClearerRateModel,ListView):
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_query=self.request.GET.get('search_query')
        if search_query:
           context['object_list']= ClearerRateM.objects.filter(Q(contract__contract_name__istartswith=search_query)|Q(clearer__name__istartswith=search_query))
           context['clearer']= ClearearM.objects.all()

        else:
            context['clearer']= ClearearM.objects.all()
            print(context['clearer'])
        return context
    
    def post(self,request):
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj = ClearerRateM.objects.get(id=delet_id)
            obj.delete()
            messages.success(request,"Deleted Successfully")
            return HttpResponseRedirect('/add-clearer-rate')
        clearer_house_feee = request.POST.get('clearer_house_feee')
        derivatives = request.POST.get('derivatives')
        contract_name = request.POST.get('contract_name')
        clearer = request.POST.get('clearer')
        obj = ClearerRateM.objects.create(clearer_house_fee=clearer_house_feee, derivative=derivatives, contract_id=contract_name,clearer_id=clearer)
        messages.info(request, "created Clearer")
        return HttpResponseRedirect('add-clearer-rate')
            

def clearer_rate_filter(request):
    if request.method=="POST":
        print('request reached')
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        option_selected = data_dict.get('option_selected')
        print(option_selected)
        data = ContractM.objects.filter(derivative=option_selected)
        l = [{'data':data.contract_name, 'data_id':data.id}for data in data]
        print(l)
        return JsonResponse({'a':l}, safe=False)


class EditClearer(CheckUserMixins, View):
    model=ClearerRateM
    
    def get(self,request,**kwargs):
        print('dddddddddddd')
        obj = self.model.objects.get(id=kwargs['id'])
        clearer = ClearearM.objects.all()
        return render(request,"backend/editclearer.html",{'obj':obj,'clearer':clearer})
    
    def post(self, request, **kwargs):
        obj1 = ClearerRateM.objects.get(id=1)
        obj1.clearer_house_fee=request.POST.get('clearer_house_feee')
        obj1.derivative =  request.POST.get('derivatives')
        obj1.contract_id=request.POST.get('contract_name')
        obj1.clearer_id=request.POST.get('clearer')
        obj1.save()
        messages.success(request,"Edited Successfully")
        return HttpResponseRedirect('/add-clearer-rate')
        
    
    
def clearear_api_swaps(request):
    dict_1 = {}
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        print(request_data)
        data_dict = json.loads(request_data)
        print(data_dict)
        derivative = data_dict.get('derivatives')
        
        data = ContractM.objects.filter(derivative=derivative)
        
        dict_1 = {'derivatives': [{'contract': data.contract_name, 'id':data.id} for data in data]}
        print(dict_1)
        
    return JsonResponse(dict_1)




class BrockerageModal(View):
    model = BrockerageM
    feilds = "__all__"
    success_url=reverse_lazy('backendapp:clearer')
    

    
class BrockerageView(CheckUserMixins, BrockerageModal, ListView):
    paginate_by=50
    def get_context_data(self, *args, **kwargs):
        search_query = self.request.GET.get('search_query')
        context = super().get_context_data(*args, **kwargs)
        if search_query:
            context['object_list']= self.model.objects.filter(Q(contract_name__contract_name__istartswith=search_query)|Q(brocker__name=search_query)|Q(brockerage=search_query))
            return context
        context['contract_name']= ContractM.objects.all()
        context['brocker']= BrokerM.objects.all()
        return context
    
    def post(self, request):
        contract_name = request.POST.get('contract_name')
        apply_mode = request.POST.get('apply_mode')
        broker = request.POST.get('broker')
        brockerage = request.POST.get('brockerage')
        derivatives = request.POST.get('derivatives')
        delet_id = request.POST.get('delet_id')
        print(delet_id)
        print('dddddddddddd')
        if delet_id:
            obj = self.model.objects.get(id=delet_id)
            obj.delete()
            messages.success(request,'Deleted Successfully')  
            return HttpResponseRedirect('/add-brockerage')       
        if apply_mode == "1":
            try:
                brockerage_model = BrockerageM.objects.all()
                for obj in brockerage_model:
                    obj.brockerage=brockerage
                    obj.apply_mode = "Standard"
                    obj.derivatives=derivatives
                    obj.save()          
                messages.success(request,'Standard Brokerage Fees Applied')  
                return HttpResponseRedirect('/add-brockerage')       
            except:
                pass
            messages.success(request,'Error') 
            return HttpResponseRedirect('/add-brockerage')       
        elif apply_mode == "2":
            try:
                obj = BrockerageM(contract_name_id=contract_name, brocker_id=broker, apply_mode="only For",brockerage=brockerage,derivatives=derivatives)
                obj.save()
                messages.success('Brockerage Saved')
                return HttpResponseRedirect('/add-brockerage')
            except:
                pass
            messages.success(request,'Error') 
            return HttpResponseRedirect('/add-brockerage')
        
        
def brockerage_contract_change(request,contract_name):
    print(contract_name)
    if contract_name:
        if contract_name == 'futures':
            obj = ContractM.objects.filter(Q(derivative__icontains='features')|Q(derivative__icontains='futures'))
        else:
            obj = ContractM.objects.filter(Q(derivative__icontains=contract_name)|Q(derivative__icontains=contract_name))
         
        return JsonResponse({'data':[{'contract_name':i.contract_name,'contract_id':i.id} for i in obj]},safe=False)
    else:
        return JsonResponse({'a':'a'})
    
        
    
class EditBrockerage(View):
    
    def get(self,request, *args, **kwargs):
        context={}
        context['contract_name']= ContractM.objects.all()
        context['brocker']= BrokerM.objects.all()
        context['data'] = BrockerageM.objects.get(id=kwargs['id'])
        return render(request, "backend/edit_brocker.html", context)
    
    def post(self, request, *args, **kwargs):
            
            obj = BrockerageM.objects.get(id=kwargs['id'])
            obj.contract_name_id= request.POST.get('contract_name')
            obj.brocker_id=request.POST.get('broker')
            obj.brockerage=request.POST.get('brockerage')
            obj.save()
            messages.info(request, "Successfully Edited")
            return HttpResponseRedirect('/add-brockerage')
        
        

class CargoModel(View):
    model = CargoM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:cargo')


class Cargo(CheckUserMixins, CargoModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name:  # Creating a object
            obj = self.model.objects.create(name=name)
            obj.save()
            messages.success(request, 'Successfully Created')
            return HttpResponseRedirect('/add-cargo')
        elif edit_name:  # editng a object
            cargo = self.model.objects.get(id=edit_name_id)
            cargo.name = edit_name
            cargo.save()
            messages.success(request, 'Edited Successfully')
            return HttpResponseRedirect('/add-cargo')
        elif delet_id:  # deleting a object
            cargo = self.model.objects.get(id=delet_id)
            cargo.delete()
            messages.success(request, 'Deleted Successfully')
            return HttpResponseRedirect('/add-cargo')
        elif file:  # Creating objects with file upload
             try:
                df = pd.read_csv(file,usecols=['cargo'or'Cargo'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['cargo'or'Cargo'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Cargo")
                else:
                    messages.error(request, "There are no values in file")
             except:
                messages.info(request, "Error ❌ Column Cargo not Found")
                return HttpResponseRedirect('/add-cargo')


class CargoDetails(CheckUserMixins, CargoModel, DetailView):
    """ """

########################################### counter party ##################################



class CounterpartyModel(View):
    model = CounterpartyM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:cargo')


class Counterparty(CheckUserMixins, CounterpartyModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(Q(trader_license_number__istartswith=search_query)|Q(email__istartswith=search_query)|Q(company_name__istartswith=search_query))
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        company_name = request.POST.get('company_name')
        licesence_number = request.POST.get('licesence_number')
        email = request.POST.get('email')
        edit_company_name = request.POST.get('edit_company_name')
        edit_id = request.POST.get('edit_id')
        edit_licesence_number = request.POST.get('edit_licesence_number')
        edit_email = request.POST.get('edit_email')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if company_name:  # Creating a object
            obj = self.model.objects.create(company_name=company_name,trader_license_number=licesence_number,email=email)
            obj.save()
            messages.success(request, 'Successfully Created')
        elif edit_company_name:  # editng a object
            counterparty = self.model.objects.get(id=edit_id)
            counterparty.company_name = edit_company_name
            counterparty.trader_license_number = edit_licesence_number
            print("counterparty.email:",counterparty.email)
            counterparty.email = edit_email
            counterparty.save()
            messages.success(request, 'Edited Successfully')
        elif delet_id:  # deleting a object
            counterparty = self.model.objects.get(id=delet_id)
            counterparty.delete()
            messages.success(request, 'Deleted Successfully')
        elif file:  # Creating objects with file upload
             try:
                df = pd.read_csv(file,usecols=['cargo'or'Cargo'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['cargo'or'Cargo'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Cargo")
                else:
                    messages.error(request, "There are no values in file")
             except:
                messages.info(request, "Error ❌ Column Cargo not Found")
        return HttpResponseRedirect('/add-counterparty')


class CounterPartyDetails(CheckUserMixins, CounterpartyModel, DetailView):
    """ """


###########################################  PORTS ##################################

class PortModel(View):
    model = PortM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:port')


class Port(CheckUserMixins, PortModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name:  # Creating a object
            obj = self.model.objects.create(name=name)
            obj.save()
            messages.success(request, 'Successfully Created')
        elif edit_name:  # editng a object
            port = self.model.objects.get(id=edit_name_id)
            port.name = edit_name
            port.save()
            messages.success(request, 'Edited Successfully')
        elif delet_id:  # deleting a object
            port = self.model.objects.get(id=delet_id)
            port.delete()
            messages.success(request, 'Deleted Successfully')
        elif file:  # Creating objects with file upload
             try:
                df = pd.read_csv(file,usecols=['port'or'Port'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['port'or'Port'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Port")
                else:
                    messages.error(request, "There are no values in file")
             except:
                messages.info(request, "Error ❌ Column Port not Found")
        return HttpResponseRedirect('/add-port')


class PortDetails(CheckUserMixins, PortModel, DetailView):
    """ """


###########################################  TERMINAL ##################################

class TerminalModel(View):
    model = TerminalM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:terminal')


class Terminal(CheckUserMixins, TerminalModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name:  # Creating a object
            obj = self.model.objects.create(name=name)
            obj.save()
            messages.success(request, 'Successfully Created')
        elif edit_name:  # editng a object
            terminal = self.model.objects.get(id=edit_name_id)
            terminal.name = edit_name
            terminal.save()
            messages.success(request, 'Edited Successfully')
        elif delet_id:  # deleting a object
            terminal = self.model.objects.get(id=delet_id)
            terminal.delete()
            messages.success(request, 'Deleted Successfully')
        elif file:  # Creating objects with file upload
             try:
                df = pd.read_csv(file,usecols=['terminal'or'Terminal'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['terminal'or'Terminal'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Terminal")
                else:
                    messages.error(request, "There are no values in file")
             except:
                messages.info(request, "Error ❌ Terminal Port not Found")
        return HttpResponseRedirect('/add-terminal')


class TerminalDetails(CheckUserMixins, TerminalModel, DetailView):
    """ """




###########################################  TankNumberM ##################################

class TankNumberModel(View):
    model = TankNumberM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:tankno')


class TankNumber(CheckUserMixins, TankNumberModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name:  # Creating a object
            obj = self.model.objects.create(name=name)
            obj.save()
            messages.success(request, 'Successfully Created')
        elif edit_name:  # editng a object
            tankno = self.model.objects.get(id=edit_name_id)
            tankno.name = edit_name
            tankno.save()
            messages.success(request, 'Edited Successfully')
        elif delet_id:  # deleting a object
            tankno = self.model.objects.get(id=delet_id)
            tankno.delete()
            messages.success(request, 'Deleted Successfully')
        elif file:  # Creating objects with file upload
            try:
                df = pd.read_csv(file,usecols=['tank number'or'Tank Number'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['tank number'or'Tank Number'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Tank Numbers")
                else:
                    messages.error(request, "There are no values in file")
            except:
                messages.info(request, "Error ❌ Tank Number not Found")
        return HttpResponseRedirect('/add-tankno')


class TankNumberDetails(CheckUserMixins, TankNumberModel, DetailView):
    """ """

###########################################  Tank Type ##################################

class TankTypeModel(View):
    model = TankTypeM
    feilds = "__all__"
    success_url = reverse_lazy('backendapp:tanktype')


class TankType(CheckUserMixins, TankTypeModel, ListView):
    paginate_by = 10
    # view all Traders
    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return self.model.objects.filter(name__istartswith=search_query)
        return self.model.objects.all()

    # create Traders
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        edit_name = request.POST.get('edit_name')
        edit_name_id = request.POST.get('edit_name_id')
        delet_id = request.POST.get('delet_id')
        file = request.FILES.get('file')
        if name:  # Creating a object
            obj = self.model.objects.create(name=name)
            obj.save()
            messages.success(request, 'Successfully Created')
        elif edit_name:  # editng a object
            tanktype = self.model.objects.get(id=edit_name_id)
            tanktype.name = edit_name
            tanktype.save()
            messages.success(request, 'Edited Successfully')
        elif delet_id:  # deleting a object
            tanktype = self.model.objects.get(id=delet_id)
            tanktype.delete()
            messages.success(request, 'Deleted Successfully')
        elif file:  # Creating objects with file upload
          try:
                df = pd.read_csv(file,usecols=['Tank Type'or'tank type'])
                print(df)
                if len(df)>0:
                    for i,name in df.iterrows():
                        obj = self.model.objects.create(name=name['Tank Type'or'tank type'])
                        obj.save()
                    messages.info(request,f"Added {len(df)} Tank Type")
                else:
                    messages.error(request, "There are no values in file")
          except:
                messages.info(request, "Error ❌ Tank Type not Found")
        return HttpResponseRedirect('/add-tanktype')


class TankTypeDetails(CheckUserMixins, TankTypeModel, DetailView):
    """ """

########################################### Generate Trade ID ##################################


class AddGenerateTradeView(CreateView):
    form_class = GenerateTradeModelForm
    template_name = "backend/Generate_trade.html"
    model = GenerateTradeModel
    success_url = reverse_lazy("add-generate-trade")

    def form_valid(self, form):
        form.instance.author = self.request.user
        Company_name = form.cleaned_data.get("Company_name")
        print("type:",type(str(Company_name)))
        print("counter_party",Company_name)
        product = form.cleaned_data.get("Cargo")
        print("product", product)
        book = form.cleaned_data.get("Book")
        print("book", book)
        quantity = form.cleaned_data.get("Quantity")
        print("quantity", quantity)
        print("Type of :",type(product))

        strategy = form.cleaned_data.get("Strategy")
        print("strategy", strategy)
        print("Type of :", type(strategy))

        # leave_data = CounterPartyModel.objects.filter(Trade_licence=Company_name)
        # print("leave_data",leave_data.Trade_licence)

        CounterParty = CounterpartyM.objects.all()

        for i in CounterParty:
            if Company_name in CounterParty:
                print("Licence",Company_name.Trade_licence)
                licence= Company_name.Trade_licence
                print("licence 2:",licence)
            # print("printj:", i.Trade_licence)

        print("Type of licence before converting:",type(licence))
        compstr= str(Company_name)
        licencestr= str(licence)
        productstr= str(product)
        bookstar= str(book)
        qtystr = str(quantity)
        strategy = str(strategy)

        print("type of compstr:",type(compstr))
        comp3 = compstr[0:3]
        licence3 = licencestr[0:3]
        book3 = bookstar[0:3]
        qty3 = qtystr[0:3]
        print("first3:",comp3)

        edited = comp3 + "-" + licence3 + "-" + book3  + "-" + productstr + "-" + qty3 + "-" + strategy

        randint_ = str(random.randint(1000, 99999))
        trade_id = edited + "-"+ randint_
        print("final rand:", trade_id)
        instance = form.save(commit=False)
        instance.Trade_id = trade_id
        instance.save()

        status_value = "New"
        print("Status value:",status_value)
        print("type of status:",type(status_value))

        instance = form.save(commit=False)
        instance.Status = status_value
        instance.save()


        self.object = form.save()
        messages.success(self.request,"Trade has been saved")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generate_trade = GenerateTradeModel.objects.all()
        context["generate_trades"] = generate_trade
        return context



# class CreateUsers(CheckUserMixins,ListView):
#     model = CustomUser
#     def get_queryset(self, *args, **kwargs):
#         return self.model.objects.filter(user_type=1)
#
#     def post(self,request):
#         name = self.request.POST.get('name')
#         password = self.request.POST.get('passsword11')
#         print(password)
#         print('---------------------------')
#         email = self.request.POST.get('email')
#         obj = CustomUser.objects.create_user(username=email, email=email, first_name=name, password=password, user_type=1)
#         return HttpResponse('created')


class CreateUsers(CheckUserMixins, PermissionRequiredMixin, ListView):
    permission_required = 'backend.view_customuser'
    model = CustomUser

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(user_type=1)

    def post(self, request):
        name = self.request.POST.get('name')
        password = self.request.POST.get('passsword11')
        print(password)
        print('---------------------------')
        email = self.request.POST.get('email')
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj = CustomUser.objects.get(id=delet_id)
            obj.delete()
            messages.info(request, "Deleted")
            return HttpResponseRedirect('/create-users')
        obj = CustomUser.objects.create_user(username=email, email=email, first_name=name, password=password,
                                             user_type=1)
        return HttpResponseRedirect('/create-users')


class CreateAdminUser(CheckUserMixins,PermissionRequiredMixin, View):
    permission_required='backend.view_customuser'
    def get(self,request):
        user = CustomUser.objects.filter(user_type='0')
        return render(request, "backend/create_admin.html",{'object_list':user})

    def post(self, request):
        name = request.POST.get('name')
        password = self.request.POST.get('passsword11')
        email = self.request.POST.get('email')
        user_exist = CustomUser.objects.filter(email=email)
        permision = request.POST.getlist('permision')
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj = CustomUser.objects.get(id=delet_id)
            obj.delete()
            messages.info(request, "Deleted")
            return HttpResponseRedirect('/create-admin-user')
        if user_exist:
            messages.info(request, "Email Already Exists")
            return HttpResponseRedirect('/create-admin-user')
        else:
            user = CustomUser.objects.create_user(username=email, email=email, first_name=name, password=password,
                                                  user_type=0)
            user.save()
            for i in permision:
                permission = Permission.objects.get(codename=i)
                user.user_permissions.add(permission)
            messages.info(request, "Created Users with permission")
            return HttpResponseRedirect('/create-admin-user')


class UniqueTrader(CheckUserMixins, ListView):
    model = GenerateTradeModel
    paginate_by=20
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_query = self.request.POST.get('search_query')
        if search_query:
            context['object_list'] = self.model.objects.filter(Q(Trade_id__istartswith=search_query)|Q(Company_name__company_name=search_query)|Q(Status=search_query))
            context['company_name'] = CounterpartyM.objects.all()
            context['cargo']=CargoM.objects.all()
            context['strategy']=Strategy.objects.all()
            context['book'] = Book.objects.all()
            context['unit'] = Unit1.objects.all()
            return context
        else:
            context['object_list'] = self.model.objects.all()
            context['company_name'] = CounterpartyM.objects.all()
            context['cargo']=CargoM.objects.all()
            context['strategy']=Strategy.objects.all()
            context['book'] = Book.objects.all()
            context['unit'] = Unit1.objects.all()
            return context
    
    def post(self, request):
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj = GenerateTradeModel.objects.get(id=delet_id)
            obj.delete()
            messages.info(request,"Succefully Deleted")
            return HttpResponseRedirect('unique-trader')
        company_name = request.POST['company_name']
        strategy = request.POST['strategy']
        cargo = request.POST['cargo']
        book = request.POST['book']
        quantity = request.POST['quantity']
        unit = request.POST['unit']
        obj = GenerateTradeModel(Company_name_id=company_name, Book_id=book, Quantity=quantity, Cargo_id=cargo,
                                 Strategy_id=strategy, Unit_id=unit,deal_current_qty=quantity)
        obj.save()
        messages.success(request,' Successfully Added')
        return HttpResponseRedirect('unique-trader')
    

class EditUniqueTrader(View):
    
    def get(self, request, *args, **kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        context={}
        context['object_list'] =GenerateTradeModel.objects.all()
        context['company_name'] = CounterpartyM.objects.all()
        context['cargo']=CargoM.objects.all()
        context['strategy']=Strategy.objects.all()
        context['book'] = Book.objects.all()
        context['data']=data
        return render(request,"backend/edit_unique_trader.html", context)
    
    def post(self,request, *args, **kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        data.Company_name_id=request.POST['company_name']
        data.Book_id=request.POST['book']
        data.Quantity=request.POST['quantity']
        data.Cargo_id=request.POST['cargo']
        data.Strategy_id= request.POST['strategy']
        data.save()
        return HttpResponseRedirect('/unique-trader')



def Closerequest(request,*args, **kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        data.Status= "Closed"
        trade_id = data.Trade_id
        print("trade id",trade_id)
        # data.save()
        print("after save")

        pb = PhysicalBlotterModel.objects.all()

        for i in pb:
            if trade_id in i.Trade_id:
                update_status_in_pb = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
                print("update_status_in_admin:", update_status_in_pb)
                print("b4")

                for i in update_status_in_pb:
                    print("new")
                    print(i.status)
                    i.status = "Closed"
                    updated_status = i.status
                    print("updated status:",updated_status)
                    print(i.status)
                    print(updated_status)

                PhysicalBlotterModel.objects.filter(Trade_id=trade_id).update(
                    status=updated_status)
                # print(update_status_in_pb.status)
                # print("after")
                # update_status_in_pb.status = "Closed"
                # print("status changed")
                # update_status_in_pb.save()
            else:
                print("Trade id not in physical blotter")
                pass

        # update_status_in_pb = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
        # print("update_status_in_admin:", update_status_in_pb)
        # print("b4")
        # print(update_status_in_pb.status)
        # print("after")
        # update_status_in_pb.status = "Closed"
        # print("status changed")
        # update_status_in_pb.save()

        data.save()
        return HttpResponseRedirect("/unique-trader")



class CloseRequestView(View):
    def get(self,request,*args,**kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        trade_id = data.Trade_id
        print("trade id", trade_id)
        print("after save")
        qs = PhysicalBlotterModel.objects.order_by('-Date')
        print("physicalblotters:",qs)

        sb_tradeid_filter = SwapBlotterModel.objects.filter(physica_blotter_connect=trade_id)
        fb_tradeid_filter = FutureBlotterModel.objects.filter(physica_blotter_connect=trade_id)
        inv_tradeid_filter = InventoryModel.objects.filter(Trade_id=trade_id)
        pb_tradeid_filter = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)

        print("sb_tradeid_filter", sb_tradeid_filter)
        print("fb_tradeid_filter", fb_tradeid_filter)
        print("inv_tradeid_filter", inv_tradeid_filter)
        print("pb_tradeid_filter", pb_tradeid_filter)

        context ={
            # "sb_trade_df":sb_trade_df,
            "trade_id":trade_id,
            "fb_tradeid_filter":fb_tradeid_filter,
            "inv_tradeid_filter":inv_tradeid_filter,
            "pb_tradeid_filter":pb_tradeid_filter,
            # "tank_summ_trade_id":tank_summ_trade_id,
        }

        return render(request,"customer/close-deal-tempate.html",context)

    def post(self, request,*args,**kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        data.Status = "Closed"
        trade_id = data.Trade_id
        print("trade id", trade_id)
        # data.save()
        print("after save")

        pb = PhysicalBlotterModel.objects.all()

        for i in pb:
            print("helloi")
            if trade_id in i.Trade_id:
                update_status_in_pb = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
                print("update_status_in_admin:", update_status_in_pb)
                print("b4")

                for i in update_status_in_pb:
                    print("new")
                    print(i.status)
                    i.status = "Closed"
                    updated_status = i.status
                    print("updated status:", updated_status)
                    print(i.status)
                    print(updated_status)

                PhysicalBlotterModel.objects.filter(Trade_id=trade_id).update(
                    status=updated_status)
                # print(update_status_in_pb.status)
                # print("after")
                # update_status_in_pb.status = "Closed"
                # print("status changed")
                # update_status_in_pb.save()
            else:
                print("Trade id not in physical blotter")
                pass

        data.save()
        return HttpResponseRedirect("/unique-trader")
        # return HttpResponse('deleted')






##### CANCEL REQUEST


def Cancelrequest(request, *args, **kwargs):
    data = GenerateTradeModel.objects.get(id=kwargs['id'])
    data.Status = "Cancelled"
    trade_id = data.Trade_id
    print("trade id", trade_id)
    # data.save()
    print("after save")

    pb = PhysicalBlotterModel.objects.all()

    for i in pb:
        if trade_id in i.Trade_id:
            update_status_in_pb = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
            print("update_status_in_admin:", update_status_in_pb)
            print("b4")

            for i in update_status_in_pb:
                print("new")
                print(i.status)
                i.status = "Cancelled"
                updated_status = i.status
                print("updated status:", updated_status)
                print(i.status)
                print(updated_status)

            PhysicalBlotterModel.objects.filter(Trade_id=trade_id).update(
                status=updated_status)
            # print(update_status_in_pb.status)
            # print("after")
            # update_status_in_pb.status = "Closed"
            # print("status changed")
            # update_status_in_pb.save()
        else:
            print("Trade id not in physical blotter")
            pass

    # update_status_in_pb = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
    # print("update_status_in_admin:", update_status_in_pb)
    # print("b4")
    # print(update_status_in_pb.status)
    # print("after")
    # update_status_in_pb.status = "Closed"
    # print("status changed")
    # update_status_in_pb.save()

    data.save()
    return HttpResponseRedirect("/unique-trader")


# FUTURE BLOTTER SAME AS SWAP BLOTTER

class FutureBlotter(CheckUserMixins, View):
    def get(self, request):
        book = Book.objects.all()
        clearer = ClearearM.objects.values_list('name', flat=True).distinct()
        trader = Traders.objects.all()
        book = Book.objects.all()
        customer_company = CompanyInvestmentModel.objects.all()
        strategy = Strategy.objects.all()
        derivatives = DerivativeM.objects.all()
        type = TYPEMODEL.objects.all()
        search_query = request.GET.get('search_query')
        print("search_query", search_query)
        today = date.today()
        print("first today:",today)
        change_date_today = today.strftime("%d-%b-%y")
        print("change_date_today",change_date_today)



        if search_query:
            data1 = FutureBlotterModel.objects.filter(
                Q(customer_company__istartswith=search_query) | Q(trader__name__istartswith=search_query)
                | Q(customer_account__istartswith=search_query) | Q(broker__istartswith=search_query) | Q(
                    efs_code__istartswith=search_query) | Q(contract__istartswith=search_query)

                | Q(clearer__istartswith=search_query) | Q(strategy__name__istartswith=search_query) | Q(
                    volume__istartswith=search_query) | Q(holiday__istartswith=search_query)

                | Q(type__istartswith=search_query) | Q(notes__istartswith=search_query) |
                Q(Trade_id__istartswith=search_query) | Q(tick__istartswith=search_query) |

                Q(trader_type__istartswith=search_query) | Q(price__istartswith=search_query)|
                Q(date__istartswith=search_query)
            )


        else:
            # data1 = FutureBlotterModel.objects.all()
            data1 = FutureBlotterModel.objects.filter(date__icontains=today)
        paginator = Paginator(data1, 25)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)

        context = {'book': book, 'clearer': clearer, 'trader': trader,
                   'customer_company': customer_company, 'strategy': strategy, 'derivatives': derivatives,
                   'type': type, 'page_obj': data}
        return render(request, "customer/futureblotter.html", context)

    def post(self, request,*args,**kwargs):
        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        clearer = request.POST.get('clearer', '')  # id
        print("Cleaerr:",clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        customer_company = request.POST.get('customer_company', '')
        print("customer_company:", customer_company)
        company_account = request.POST.get('company_account', '')
        print("company_account:",company_account)
        buy_sell = request.POST.get('buy_sell', '')
        volume = request.POST.get('volume', '')
        pb_id = request.POST.get('pb_id', '')
        contract_name = request.POST.get('contract_name')
        strategy = request.POST.get('strategy', '')  # id
        # derivatives = request.POST.get('derivatives', '')
        contract_month = request.POST.get('contract_month', '')
        # end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        print("price:",price)
        # price = float(price)
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        type = request.POST.get('type', '')
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        notes = request.POST.get('notes', '')

        unit_gett = request.POST.get('unit_c', '')
        tick_gett = request.POST.get('tick_c', '')
        delete_feild = request.POST.get('delete_feild')
        print("delete_feild",delete_feild)
        if delete_feild:
            dlid = self.request.POST.get('delete_feild')
            print("dlid:", dlid)
            obj = FutureBlotterModel.objects.get(id=dlid)
            if obj.duplicate_id == 'none':
                obj.delete()
                messages.info(request, 'Deleted')
                return HttpResponseRedirect("/future-blotter")
            else:
                print("dlid:",dlid)
                # print(kwargs['id'])
                obj = FutureBlotterModel.objects.get(id=dlid)
                print(obj)
                print('dddddddddddddddddddd')
                obj2 = FutureBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
                print("obj2:",obj2)
                for i in obj2:
                    obj1 = FutureBlotterModel.objects.get(id=i.id)
                    obj1.delete()
                    obj2.delete()
                # obj = FutureBlotterModel.objects.get(id=dlid)
                # obj2 = FutureBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
                # for i in obj2:
                #     obj1 = FutureBlotterModel.objects.get(id=i.id)
                #     obj1.delete()
                    messages.info(request, 'Deleted')
                    return HttpResponseRedirect("/future-blotter")

        print("************* Coversion from string to particular type")
        date = datetime.strptime(date, '%Y-%m-%d').date()
        print("converted start_date:", date)

        c = ContractM.objects.filter(contract_name=contract_name)[0]
        print(c)
        print('get all future values form future blotter form')
        # print("Type of contract month:", type(contract_month)
        # # print("contract name type:",type(contract_name))
        list1 = list(clearer)
        print("list:", list1)

        # # codes from forms django
        today = datetime.today()
        print("today:", today)
        #
        contract_month = datetime.strptime(contract_month, '%Y-%m-%d').date()

        datem = datetime(contract_month.year, contract_month.month, 1)
        date_to_first = datem.date()
        print("current date today1:", date_to_first)
        #
        print("get contract_name ", contract_name)
        # Contract_Name = contract_name
        # print("str contract_name_str:", Contract_Name)
        randint_ = str(random.randint(10, 99999))
        Contract = ContractM.objects.filter(derivative="features")
        print("Contract -", Contract)

        contract = ContractM.objects.filter(contract_name__icontains=contract_name)[0]
        print("cont unit:", contract.unit)
        unit = contract.unit
        tick = contract.tick
        bbl_unit_convert = contract.bbi_mt_conversion
        holiday = contract.holiday
        fwrd_contrct_mnths = contract.f_w_months
        exchange_fee = contract.exchange_fee
        physical_code = contract.physical_code
        print("exchange_fee get from contract:", exchange_fee)
        exhange_clearing_fee = contract.exchanging_clearing_fee
        print("exhange_clearing_fee get from contract:", exhange_clearing_fee)

        try:
            second_fw_month = fwrd_contrct_mnths + 1
        except:
            fwrd_contrct_mnths = 0
            second_fw_month = 0

        volume_value = float(volume)
        print("volume_value:", volume_value)
        holiday = str(holiday)
        unit = str(unit)
        exchange_fee_value = round(-abs(float(exchange_fee) * volume_value), 3)
        print("exchange_fee_value:", exchange_fee_value)
        exhange_clearing_fee_value = round(-abs(float(exhange_clearing_fee) * volume_value), 3)
        print("exhange_clearing_fee_value:", exhange_clearing_fee_value)
        brokerage = 0.0
        total_fee = exchange_fee_value + exhange_clearing_fee_value
        print("total_fee", total_fee)

        bbl_mt_conversion = float(bbl_unit_convert) * float(volume_value) * float(tick)
        kbbl_mt_conversion = (float(bbl_unit_convert) * float(volume_value) * float(tick)) / 1000

        print("bbl_mt_conversion:", bbl_mt_conversion)
        print("kbbl_mt_conversion:", kbbl_mt_conversion)

        if bileteral_external == 'Bilateral':
            trade_id = "BLT" + "-" + "F" + "-" + randint_
            print("tradeid BLT:", trade_id)

            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep,
                                     type=type, efs_code=efs_code, broker=brocker,
                                     notes=notes, Trade_id=trade_id,
                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion, tick=tick,
                                     bileteral_external=bileteral_external,physical_code=physical_code,
                                     physica_blotter_connect=pb_id,
                                     )
            obj.save()
            obj.duplicate_id = obj.id
            obj.save()
            if float(volume) < 0:
                volume1 = abs(float(volume))
                print("volume<0 inside biletral:", volume1)
            else:
                volume1 = '-' + str(volume)
                print("string in -ve ", volume1)
                volume1 = float(volume1)
                print("string convert into int -ve ", volume1)

                # recalculation for negative value
                print("exchange_fee:", exchange_fee)
                print("exhange_clearing_fee:", exhange_clearing_fee)
                exchange_fee_value_neg = round(-abs(float(exchange_fee) * volume1), 3)
                print("exchange_fee_value for negative volume:", exchange_fee_value)
                exhange_clearing_fee_value_neg = round(-abs(float(exhange_clearing_fee) * volume1), 3)
                print("exhange_clearing_fee_value for negative volume::", exhange_clearing_fee_value)
                brokerage = 0.0
                total_fee_neg = exchange_fee_value_neg + exhange_clearing_fee_value_neg
                print("total_fee", total_fee)

                bbl_mt_conversion_neg = float(bbl_unit_convert) * float(volume1) * float(tick)
                kbbl_mt_conversion_neg = (float(bbl_unit_convert) * float(volume1) * float(tick)) / 1000

                print("bbl_mt_conversion for negative:", bbl_mt_conversion_neg)
                print("kbbl_mt_conversion for negative:", kbbl_mt_conversion_neg)

            obj1 = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                      book=customer_company, customer_account=company_account,
                                      strategy_id=strategy, volume=volume1, customer_company=book,
                                      contract=contract_name, Contract_Month=contract_month,
                                      price=price, approx_ep=approximate_ep,
                                      type=type, efs_code=efs_code, broker=brocker, Trade_id=trade_id,
                                      notes=notes, duplicate_id=obj.id,
                                      # # calculated and_ get_values for negative volume
                                      unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value_neg,
                                      Exchange_rate=exhange_clearing_fee_value_neg, brockerage=brokerage,
                                      total_fee=total_fee_neg, bbl_mt_conversion=bbl_mt_conversion_neg,
                                      kbbl_mt_conversion=kbbl_mt_conversion_neg, tick=tick,
                                      bileteral_external=bileteral_external,physical_code=physical_code,
                                      physica_blotter_connect=pb_id,

                                      )
            obj1.save()
            messages.info(request, 'Future-blotter Trade Saved')
            return HttpResponseRedirect('/future-blotter')
        else:

            trade_id = "EXT" + "-" + "F" + "-" + randint_
            print("tradeid EXT:", trade_id)
            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep, type=type, efs_code=efs_code,
                                     broker=brocker, Trade_id=trade_id, notes=notes, tick=tick,

                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion,bileteral_external=bileteral_external,
                                     physical_code = physical_code,physica_blotter_connect=pb_id,
                                     )
            obj.save()
            messages.info(request, 'Future-blotter Trade Saved')
        return HttpResponseRedirect('/future-blotter')
# future blotter edit


class EditFutureBlotter(View):
    def get(self, request, **kwargs):
        obj = FutureBlotterModel.objects.get(id=kwargs['id'])
        clearer = ClearearM.objects.values_list('name', flat=True).distinct()
        trader = Traders.objects.all()
        book = Book.objects.all()
        customer_company = CompanyInvestmentModel.objects.all()
        strategy = Strategy.objects.all()
        type = TYPEMODEL.objects.all()

        print("date checking:",obj.Contract_Month)

        data = FutureBlotterModel.objects.all()
        context = {'book': book, 'clearer': clearer, 'trader': trader,
                   'customer_company': customer_company, 'strategy': strategy,
                   'type': type, 'object_list': data, 'd': obj}
        return render(request, 'customer/edit-future-blotter.html', context)

    def post(self, request, **kwargs):
        obj = FutureBlotterModel.objects.get(id=kwargs['id'])
        print("traded id:",obj.Trade_id)
        tradeid = obj.Trade_id

        if obj.duplicate_id == 'none':
            obj.delete()
        else:
            print(kwargs['id'])
            obj = FutureBlotterModel.objects.get(id=kwargs['id'])
            print(obj)
            print('dddddddddddddddddddd')
            obj2 = FutureBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = FutureBlotterModel.objects.get(id=i.id)
                obj1.delete()

        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        clearer = request.POST.get('clearer', '')  # id
        print("Cleaerr:", clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        customer_company = request.POST.get('customer_company', '')
        print("customer_company:", customer_company)
        company_account = request.POST.get('company_account', '')
        print("company_account:", company_account)
        buy_sell = request.POST.get('buy_sell', '')
        volume = request.POST.get('volume', '')
        pb_id = request.POST.get('pb_id', '')
        contract_name = request.POST.get('contract_name')
        print("contract_name:",contract_name)
        strategy = request.POST.get('strategy', '')  # id
        # derivatives = request.POST.get('derivatives', '')
        contract_month = request.POST.get('contract_month', '')
        # end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        print("price:", price)
        # price = float(price)
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        print("holiday:",holiday)
        type = request.POST.get('type', '')
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        print("brokergetting from form",brocker)
        notes = request.POST.get('notes', '')

        unit_gett = request.POST.get('unit_c', '')
        tick_gett = request.POST.get('tick_c', '')
        delete_feild = request.POST.get('delete_feild')
        print("delete_feild", delete_feild)

        c = ContractM.objects.filter(contract_name=contract_name)[0]
        print("Ccontract filter:",c)

        brocker = str(brocker)


        # obj_delete_id = FutureBlotterModel.objects.get(id=self.kwargs['id'])
        # print("obj_delete_id:",obj_delete_id)
        # obj_delete = FutureBlotterModel.objects.filter(duplicate_id=obj_delete_id.duplicate_id)
        # obj_delete.delete()

        print('RECALCULATION For edit ')
        # print("Type of contract month:", type(contract_month)
        # # print("contract name type:",type(contract_name))
        list1 = list(clearer)
        print("list:", list1)

        # # codes from forms django
        today = datetime.today()
        print("today:", today)
        #
        contract_month = datetime.strptime(contract_month, '%Y-%m-%d').date()

        datem = datetime(contract_month.year, contract_month.month, 1)
        date_to_first = datem.date()
        print("current date today1:", date_to_first)
        #
        print("get contract_name ", contract_name)
        # Contract_Name = contract_name
        # print("str contract_name_str:", Contract_Name)
        randint_ = str(random.randint(10, 99999))
        Contract = ContractM.objects.filter(derivative="features")
        print("Contract -", Contract)

        contract = ContractM.objects.filter(contract_name__icontains=contract_name)[0]
        print("cont unit:", contract.unit)
        unit = contract.unit
        tick = contract.tick
        bbl_unit_convert = contract.bbi_mt_conversion
        holiday = contract.holiday
        print("original holiday:",holiday)

        fwrd_contrct_mnths = contract.f_w_months
        exchange_fee = contract.exchange_fee
        physical_code = contract.physical_code
        print("exchange_fee get from contract:", exchange_fee)
        exhange_clearing_fee = contract.exchanging_clearing_fee
        print("exhange_clearing_fee get from contract:", exhange_clearing_fee)

        try:
            second_fw_month = fwrd_contrct_mnths + 1
        except:
            fwrd_contrct_mnths = 0
            second_fw_month = 0

        volume_value = float(volume)
        print("volume_value:", volume_value)
        holiday = str(holiday)
        unit = str(unit)
        exchange_fee_value = round(-abs(float(exchange_fee) * volume_value), 3)
        print("exchange_fee_value:", exchange_fee_value)
        exhange_clearing_fee_value = round(-abs(float(exhange_clearing_fee) * volume_value), 3)
        print("exhange_clearing_fee_value:", exhange_clearing_fee_value)
        brokerage = 0.0
        total_fee = exchange_fee_value + exhange_clearing_fee_value
        print("total_fee", total_fee)

        bbl_mt_conversion = float(bbl_unit_convert) * float(volume_value) * float(tick)
        kbbl_mt_conversion = (float(bbl_unit_convert) * float(volume_value) * float(tick)) / 1000

        print("bbl_mt_conversion:", bbl_mt_conversion)
        print("kbbl_mt_conversion:", kbbl_mt_conversion)

        print("brocker:",brocker)

        if bileteral_external == 'Bilateral':
            trade_id = "BLT" + "-" + "F" + "-" + randint_
            print("tradeid BLT:", trade_id)

            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep,
                                     type=type, efs_code=efs_code, broker=brocker,
                                     notes=notes, Trade_id=trade_id,
                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion, tick=tick,
                                     bileteral_external=bileteral_external,
                                     physical_code=physical_code,

                                     )
            obj.save()
            obj.duplicate_id = obj.id
            obj.save()

            print("volume:",volume)

            print("new negative volume check")
            if float(volume) < 0:
                volume1 = abs(float(volume))
                print("volume<0 inside biletral:", volume1)
            else:
                volume1 = '-' + str(volume)
                print("string in -ve ", volume1)
                volume1 = float(volume1)
                print("string convert into int -ve ", volume1)

            # recalculation for negative value
            print("exchange_fee:", exchange_fee)
            print("exhange_clearing_fee:", exhange_clearing_fee)
            exchange_fee_value_neg = round(-abs(float(exchange_fee) * volume1), 3)
            print("exchange_fee_value for negative volume:", exchange_fee_value)
            exhange_clearing_fee_value_neg = round(-abs(float(exhange_clearing_fee) * volume1), 3)
            print("exhange_clearing_fee_value for negative volume::", exhange_clearing_fee_value)
            brokerage = 0.0
            total_fee_neg = exchange_fee_value_neg + exhange_clearing_fee_value_neg
            print("total_fee", total_fee)

            bbl_mt_conversion_neg = float(bbl_unit_convert) * float(volume1) * float(tick)
            kbbl_mt_conversion_neg = (float(bbl_unit_convert) * float(volume1) * float(tick)) / 1000

            print("bbl_mt_conversion for negative:", bbl_mt_conversion_neg)
            print("kbbl_mt_conversion for negative:", kbbl_mt_conversion_neg)

            obj1 = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                      book=customer_company, customer_account=company_account,
                                      strategy_id=strategy, volume=volume1, customer_company=book,
                                      contract=contract_name, Contract_Month=contract_month,
                                      price=price, approx_ep=approximate_ep,
                                      type=type, efs_code=efs_code, broker=brocker, Trade_id=trade_id,
                                      notes=notes, duplicate_id=obj.id,
                                      # # calculated and_ get_values for negative volume
                                      unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value_neg,
                                      Exchange_rate=exhange_clearing_fee_value_neg, brockerage=brokerage,
                                      total_fee=total_fee_neg, bbl_mt_conversion=bbl_mt_conversion_neg,
                                      kbbl_mt_conversion=kbbl_mt_conversion_neg, tick=tick,
                                      bileteral_external=bileteral_external,
                                      physical_code=physical_code,


                                      )
            obj1.save()
            messages.info(request, 'Future-blotter Trade Saved')
            return HttpResponseRedirect('/future-blotter')
        else:

            trade_id = "EXT" + "-" + "F" + "-" + randint_
            print("tradeid EXT:", trade_id)

            print("brocker:",brocker)

            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep, type=type, efs_code=efs_code,
                                     broker=brocker, Trade_id=trade_id, notes=notes, tick=tick,

                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion, bileteral_external=bileteral_external,
                                     physical_code=physical_code,
                                     )
            obj.save()
            messages.info(request, 'Future-blotter Trade Saved')
            return HttpResponseRedirect('/future-blotter')


class DeleteFutureBlotter(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/delete-future-blotter.html')

    def post(self, request, *args, **kwargs):
        obj = FutureBlotterModel.objects.get(id=kwargs['id'])
        if obj.duplicate_id == 'none':
            obj.delete()
        else:
            print(kwargs['id'])
            obj = FutureBlotterModel.objects.get(id=kwargs['id'])
            print(obj)
            print('dddddddddddddddddddd')
            obj2 = FutureBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = FutureBlotterModel.objects.get(id=i.id)
                obj1.delete()

        messages.info(request, 'Deleted')
        return HttpResponseRedirect('/fb-trade-hist/')


## Future blotter details view

class FutureBlotterDetailsView(View):
    def get(self,request,*args,**kwargs):
        # print(kwargs)
        qs = FutureBlotterModel.objects.get(id=kwargs['id'])
        return render(request,"customer/fb-details.html",{"fb":qs})




def export_fb_csv_today(request):
    today = date.today()
    print("first today:", today)
    fb= FutureBlotterModel.objects.filter(date__icontains=today)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Futureblotter.csv'
    writer = csv.writer(response)
    writer.writerow(['No','date','trader_type','bileteral_external','clearer',
                    'trader','book','customer_company','customer_account','volume',
                    'contract','strategy','Contract_Month','price','approx_ep','type','broker','efs_code','notes','unit','Clearer_rate',
                    'Exchange_rate', 'brockerage', 'total_fee', 'holiday', 'tick', 'bbl_mt_conversion','kbbl_mt_conversion','Trade_id','physical_code',
                  ] )

    fb_fields = fb.values_list(

        'id', 'date','trader_type','bileteral_external','clearer',
        'trader', 'book', 'customer_company', 'customer_account', 'volume',
        'contract', 'strategy', 'Contract_Month', 'price', 'approx_ep', 'type', 'broker', 'efs_code', 'notes', 'unit', 'Clearer_rate',
        'Exchange_rate', 'brockerage', 'total_fee', 'holiday', 'tick', 'bbl_mt_conversion','kbbl_mt_conversion','Trade_id','physical_code',
         )

    for item in fb_fields:
        writer.writerow(item)
    return response










def search_customer_company(request, company_name):
    obj = CompanyInvestmentModel.objects.filter(Customer_Company_name__icontains=company_name)
    lis = [{'data': data.Customer_Account} for data in obj]
    print(lis)
    return JsonResponse({'company_name': lis}, safe=False)


def future_bloters_clearer_derivative(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        clearer_name = data_dict.get('clearer')
        obj = ClearerRateM.objects.filter(Q(clearer__name=clearer_name), Q(derivative='features'))
        data = [{'data': data.contract.contract_name} for data in obj]
        return JsonResponse({'data': data}, safe=False)


### new for customer company and broker same as cleaerer
def future_bloters_company_broker_derivative(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract_name')
        print("contract_name",contract_name)
        obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith= contract_name)
        data= [{'data': i.brocker.name} for i in obj2]
        print(data)
        print('ddd')
        return JsonResponse({'data': data}, safe=False)


#### holiday seperate

def future_bloters_company_holiday_relation(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract_name')
        print("contract_name",contract_name)

        obj = ContractM.objects.filter(contract_name__icontains=contract_name)
        print(contract_name)

        data = [{'date': data.holiday} for data in obj]
        print(data)
        print('ddd')
        return JsonResponse({'data': data}, safe=False)


def future_bloters_holiday_relation(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract_name')
        obj = ContractM.objects.filter(contract_name__icontains=contract_name)
        print(contract_name)
        obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith=contract_name)
        data = [{'date': data.holiday} for data in obj]
        data1 = [{'data': i.brocker.name} for i in obj2]
        print(data1)
        print('ddd')
        return JsonResponse({'data': data, 'data1': data1}, safe=False)


#
def contract_name_holiday_relation_fb(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract')

        print("contract_name",contract_name)
        print("hello contu")
        obj = ContractM.objects.filter(contract_name__icontains=contract_name)
        print(contract_name)
        obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith=contract_name)
        data = [{'date': data.holiday} for data in obj]
        data1 = [{'data': i.brocker.name} for i in obj2]
        print(data1,"data1")
        print('ddd')
        print(data,"data")
    return JsonResponse({'data': data, 'data1': data1}, safe=False)


def filter_futureblotter_table(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        trade_type_filter = data_dict.get('trade_type')
        clearer_filter = data_dict.get('clearer')
        trader_filter = data_dict.get('trader')

        print("trade_type_filter:",trade_type_filter)
        print("clearer_filter:", clearer_filter)
        print("trader_filter:", trader_filter)


        obj = FutureBlotterModel.objects.filter(Q(trader_type=trade_type_filter) | Q(clearer=clearer_filter) | Q(trader__name=trader_filter))
        print("filter fututreblotter",obj)

        k = "test"

    return JsonResponse({'data':k}, safe=False)






# export futurblotter to CSV
def export_fb_csv(request):
    fb= FutureBlotterModel.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Futureblotter.csv'
    writer = csv.writer(response)
    writer.writerow(['No','date','trader_type','bileteral_external','clearer',
                    'trader','book','customer_company','customer_account','volume',
                    'contract','strategy','Contract_Month','price','approx_ep','type','broker','efs_code','notes','unit','Clearer_rate',
                    'Exchange_rate', 'brockerage', 'total_fee', 'holiday', 'tick', 'bbl_mt_conversion','kbbl_mt_conversion','Trade_id','physical_code',
                  ] )

    fb_fields = fb.values_list(

        'id', 'date','trader_type','bileteral_external','clearer',
        'trader', 'book', 'customer_company', 'customer_account', 'volume',
        'contract', 'strategy', 'Contract_Month', 'price', 'approx_ep', 'type', 'broker', 'efs_code', 'notes', 'unit', 'Clearer_rate',
        'Exchange_rate', 'brockerage', 'total_fee', 'holiday', 'tick', 'bbl_mt_conversion','kbbl_mt_conversion','Trade_id','physical_code',
         )

    for item in fb_fields:
        writer.writerow(item)
    return response


#### copy futureblotter


class CopyFutureBlotter(CheckUserMixins, View):
    def get(self, request,*args,**kwargs):
        obj = FutureBlotterModel.objects.get(id=kwargs['id'])
        book = Book.objects.all()
        clearer = ClearearM.objects.values_list('name', flat=True).distinct()
        trader = Traders.objects.all()
        book = Book.objects.all()
        customer_company = CompanyInvestmentModel.objects.all()
        strategy = Strategy.objects.all()
        type = TYPEMODEL.objects.all()
        data = FutureBlotterModel.objects.all()
        context = {'book': book, 'clearer': clearer, 'trader': trader,
                   'customer_company': customer_company, 'strategy': strategy,
                   'type': type, 'object_list': data, 'd': obj}
        return render(request, "customer/futureblotter-copy.html", context)

    def post(self, request,*args,**kwargs):
        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        clearer = request.POST.get('clearer', '')  # id
        print("Cleaerr:",clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        customer_company = request.POST.get('customer_company', '')
        print("customer_company:", customer_company)
        company_account = request.POST.get('company_account', '')
        print("company_account:",company_account)
        buy_sell = request.POST.get('buy_sell', '')
        volume = request.POST.get('volume', '')
        pb_id = request.POST.get('pb_id', '')
        contract_name = request.POST.get('contract_name')
        strategy = request.POST.get('strategy', '')  # id
        # derivatives = request.POST.get('derivatives', '')
        contract_month = request.POST.get('contract_month', '')
        # end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        type = request.POST.get('type', '')
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        notes = request.POST.get('notes', '')
        delete_feild = request.POST.get('delete_feild')
        c = ContractM.objects.filter(contract_name=contract_name)[0]
        print(c)
        print('get all future values form future blotter form')
        # print("Type of contract month:", type(contract_month)
        # # print("contract name type:",type(contract_name))
        list1 = list(clearer)
        print("list:", list1)

        # # codes from forms django
        today = datetime.today()
        print("today:", today)
        #
        contract_month = datetime.strptime(contract_month, '%Y-%m-%d').date()

        datem = datetime(contract_month.year, contract_month.month, 1)
        date_to_first = datem.date()
        print("current date today1:", date_to_first)
        #
        print("get contract_name ", contract_name)
        # Contract_Name = contract_name
        # print("str contract_name_str:", Contract_Name)
        randint_ = str(random.randint(10, 99999))
        Contract = ContractM.objects.filter(derivative="features")
        print("Contract -", Contract)

        contract = ContractM.objects.filter(contract_name__icontains=contract_name)[0]
        print("cont unit:", contract.unit)
        unit = contract.unit
        tick = contract.tick
        bbl_unit_convert = contract.bbi_mt_conversion
        holiday = contract.holiday
        fwrd_contrct_mnths = contract.f_w_months
        exchange_fee = contract.exchange_fee
        physical_code = contract.physical_code
        print("exchange_fee get from contract:", exchange_fee)
        exhange_clearing_fee = contract.exchanging_clearing_fee
        print("exhange_clearing_fee get from contract:", exhange_clearing_fee)

        try:
            second_fw_month = fwrd_contrct_mnths + 1
        except:
            fwrd_contrct_mnths = 0
            second_fw_month = 0

        volume_value = float(volume)
        print("volume_value:", volume_value)
        holiday = str(holiday)
        unit = str(unit)
        exchange_fee_value = round(-abs(float(exchange_fee) * volume_value), 3)
        print("exchange_fee_value:", exchange_fee_value)
        exhange_clearing_fee_value = round(-abs(float(exhange_clearing_fee) * volume_value), 3)
        print("exhange_clearing_fee_value:", exhange_clearing_fee_value)
        brokerage = 0.0
        total_fee = exchange_fee_value + exhange_clearing_fee_value
        print("total_fee", total_fee)

        bbl_mt_conversion = float(bbl_unit_convert) * float(volume_value) * float(tick)
        kbbl_mt_conversion = (float(bbl_unit_convert) * float(volume_value) * float(tick)) / 1000

        print("bbl_mt_conversion:", bbl_mt_conversion)
        print("kbbl_mt_conversion:", kbbl_mt_conversion)

        if bileteral_external == 'Bilateral':
            trade_id = "BLT" + "-" + "F" + "-" + randint_
            print("tradeid BLT:", trade_id)

            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep,
                                     type=type, efs_code=efs_code, broker=brocker,
                                     notes=notes, Trade_id=trade_id,
                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion, tick=tick,
                                     bileteral_external=bileteral_external,physical_code=physical_code,
                                     physica_blotter_connect=pb_id,
                                     )
            obj.save()
            obj.duplicate_id = obj.id
            obj.save()
            if float(volume) < 0:
                volume1 = abs(float(volume))
                print("volume<0 inside biletral:", volume1)
            else:
                volume1 = '-' + str(volume)
                print("string in -ve ", volume1)
                volume1 = float(volume1)
                print("string convert into int -ve ", volume1)

            # recalculation for negative value
            print("exchange_fee:", exchange_fee)
            print("exhange_clearing_fee:", exhange_clearing_fee)
            exchange_fee_value_neg = round(-abs(float(exchange_fee) * volume1), 3)
            print("exchange_fee_value for negative volume:", exchange_fee_value)
            exhange_clearing_fee_value_neg = round(-abs(float(exhange_clearing_fee) * volume1), 3)
            print("exhange_clearing_fee_value for negative volume::", exhange_clearing_fee_value)
            brokerage = 0.0
            total_fee_neg = exchange_fee_value_neg + exhange_clearing_fee_value_neg
            print("total_fee", total_fee)

            bbl_mt_conversion_neg = float(bbl_unit_convert) * float(volume1) * float(tick)
            kbbl_mt_conversion_neg = (float(bbl_unit_convert) * float(volume1) * float(tick)) / 1000

            print("bbl_mt_conversion for negative:", bbl_mt_conversion_neg)
            print("kbbl_mt_conversion for negative:", kbbl_mt_conversion_neg)

            obj1 = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                      book=customer_company, customer_account=company_account,
                                      strategy_id=strategy, volume=volume1, customer_company=book,
                                      contract=contract_name, Contract_Month=contract_month,
                                      price=price, approx_ep=approximate_ep,
                                      type=type, efs_code=efs_code, broker=brocker, Trade_id=trade_id,
                                      notes=notes, duplicate_id=obj.id,
                                      # # calculated and_ get_values for negative volume
                                      unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value_neg,
                                      Exchange_rate=exhange_clearing_fee_value_neg, brockerage=brokerage,
                                      total_fee=total_fee_neg, bbl_mt_conversion=bbl_mt_conversion_neg,
                                      kbbl_mt_conversion=kbbl_mt_conversion_neg, tick=tick,
                                      bileteral_external=bileteral_external,physical_code=physical_code,
                                      physica_blotter_connect=pb_id,

                                      )
            obj1.save()
            messages.info(request, 'Future-blotter Trade Saved')
            return HttpResponseRedirect('/future-blotter')
        else:

            trade_id = "EXT" + "-" + "F" + "-" + randint_
            print("tradeid EXT:", trade_id)
            obj = FutureBlotterModel(date=date, trader_type=bileteral_external, clearer=clearer, trader_id=trader,
                                     book=book, customer_account=company_account,
                                     strategy_id=strategy, volume=volume,
                                     customer_company=customer_company,
                                     contract=contract_name, Contract_Month=contract_month,
                                     price=price, approx_ep=approximate_ep, type=type, efs_code=efs_code,
                                     broker=brocker, Trade_id=trade_id, notes=notes, tick=tick,

                                     # calculated and_ get_values
                                     unit=unit, holiday=holiday, Clearer_rate=exchange_fee_value,
                                     Exchange_rate=exhange_clearing_fee_value, brockerage=brokerage,
                                     total_fee=total_fee, bbl_mt_conversion=bbl_mt_conversion,
                                     kbbl_mt_conversion=kbbl_mt_conversion,bileteral_external=bileteral_external,
                                     physical_code = physical_code,physica_blotter_connect=pb_id,
                                     )
            obj.save()
            messages.info(request, 'Future-blotter Trade Saved')
        return HttpResponseRedirect('/future-blotter')










# END FUTURE BLOTTER SAME AS SWAP

    
# class SwapsBlotter(CheckUserMixins, View):
#     def get (self,request):
#         book = Book.objects.all()
#         clearer = ClearearM.objects.values_list('name',flat=True).distinct()
#         trader = Traders.objects.all()
#         book = Book.objects.all()
#         customer_company = CompanyInvestmentModel.objects.all()
#         strategy = Strategy.objects.all()
#         derivatives = DerivativeM.objects.all()
#         type = TYPEMODEL.objects.all()
#         data1 = SwapBlotterModel.objects.all()
#         paginator = Paginator(data1,25)
#         page_number = request.GET.get('page')
#         data = paginator.get_page(page_number)
#         context = {'book':book,'clearer':clearer, 'trader':trader,
#                   'customer_company':customer_company, 'strategy':strategy,'derivatives':derivatives,
#                   'type':type,'page_obj':data}
#         return render (request, "backend/swaps_bloter.html",context)
#
#     def post(self,request):
#         date = request.POST.get('date','')
#         bileteral_external = request.POST.get('bileteral_external','')
#         clearer = request.POST.get('clearer','')#id
#         trader = request.POST.get('trader','') #id
#         book = request.POST.get('book','')
#         company_account = request.POST.get('company_account','')
#         strategy = request.POST.get('strategy','') #id
#         derivatives = request.POST.get('derivatives','')
#         volume = request.POST.get('volume','')
#         customer_company = request.POST.get('customer_company','')
#         buy_sell = request.POST.get('buy_sell','')
#         contract_name = request.POST.get('contract_name','')
#         start_date = request.POST.get('start_date','')
#         end_date = request.POST.get('end_date','')
#         price = request.POST.get('price','')
#         approximate_ep = request.POST.get('approximate_ep','')
#         holiday = request.POST.get('holiday','')
#         type = request.POST.get('type','')
#         efs_code = request.POST.get('efs_code','')
#         brocker = request.POST.get('brocker','')
#         notes = request.POST.get('notes','')
#         # book = request.POST.get('book','')
#         delete_feild = request.POST.get('delete_feild')
#         c = ContractM.objects.filter(contract_name=contract_name)[0]
#         print("Print c :",c)
#
#         # conversion of all dates
#         print("************* Coversion from string to particular type")
#
#         start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#         print("converted start_date:",start_date)
#
#         end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#         print("converted end_date:", end_date)
#
#         date_ = datetime.strptime(date, '%Y-%m-%d').date()
#         print("converted date:", date_)
#         print('****************************************')
#
#         # conversion of values
#
#         volume = int(volume)
#
#
#
#         #   the working holiday list dates  using data frame
#         print("Finding holiday:")
#         print("Holioday selected",holiday)
#         holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
#         # workingdays
#         holi_list_selcted = []
#         for i in holiday_list_of_selected_holi:
#             holi_list_selcted.append(i)
#         print("new list of selected holi:",holi_list_selcted)
#
#         holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
#         holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
#         holiday_list = holiday_date_df['Dates'].to_list()
#         print(holi_list_selcted, 'first++++++++total_swap_days')
#
#         holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
#         holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
#         holi_list_selcted = holiday_date_df['Dates'].to_list()
#         print(holiday_list, 'first++++++++total_swap_days')
#
#         total_working_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holi_list_selcted))
#         print(total_working_days, '++++++++total_swap_days')
#         # end mycode
#
#         # holiday_list = []
#         # holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
#         # for i in holiday_check:
#         #     holiday_list.append(i)
#         #
#         # print(holiday_list, 'holiday_list+++++')
#         #
#         # holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
#         # holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
#         # holiday_list = holiday_date_df['Dates'].to_list()
#         # print(holiday_list, 'first++++++++total_swap_days')
#         #
#         # total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
#         # print(total_swap_days, '++++++++total_swap_days')
#
#         randint_ = str(random.randint(1000, 99999))
#
#         # <!----- priced and unpriced days start ----!>
#         if date_ <= start_date:
#             print("first condition priced days")
#             priced_days = 0
#             # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
#             unprice_calcu = pd.bdate_range(start=start_date, end=end_date, freq="C",
#                                            holidays=holi_list_selcted)
#             unpriced_days = len(unprice_calcu)
#             print("priced days: step 1",priced_days)
#             print("unpriced_days : step 1", unpriced_days)
#             print("first Priced/unpriced days ")
#             print('+++++++++++++++++++++++++++++++++++++++++')
#         # ---------------------------------------------------------------------------
#         elif (date_ > start_date) and (date_ <= end_date):
#             print("2nd pricing days condition")
#             unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=holi_list_selcted))
#             workday = len(pd.bdate_range(start=start_date, end=end_date,
#                                          freq="C", holidays=holi_list_selcted))
#             priced_days = workday - unpriced_days
#
#             print("priced days: step 2", priced_days)
#             print("unpriced_days : step 2", unpriced_days)
#             print("second Priced/unpriced days ")
#             print('+++++++++++++++++++++++++++++++++++++++++')
#         elif (date_ > end_date):
#             print("Hi 3rd priced days CONDITION")
#             unpriced_days = 0
#             # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
#             priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
#             print(priced_days)
#             priced_days = len(priced_days)
#
#             print("priced days:", priced_days)
#             print("Unpriced days:", unpriced_days)
#
#             print("Third Priced/unpriced days ")
#             print('+++++++++++++++++++++++++++++++++++++++++')
#
#         else:
#             pass
#             # <!----- priced unpriced end ---!>
#
#             # <!-----priced volume ----!>
#         priced_volume = (priced_days / total_working_days) * volume
#         unpriced_volume = (volume / total_working_days) * unpriced_days
#         priced_volume = round(priced_volume, 2)
#         unpriced_volume = round(unpriced_volume, 2)
#         # total volume
#         total_volume = priced_volume + unpriced_volume
#
#         # priced volume for  negative volume
#         priced_volume_negative = -abs(priced_volume)
#         print("priced_volume_negative:", priced_volume_negative)
#         unpriced_volume_negative = -abs(unpriced_volume)
#         print("unpriced_volume_negative:", unpriced_volume_negative)
#         # total volume negative
#         total_volume_neg = priced_volume_negative + unpriced_volume_negative
#         forwards_months = c.f_w_months
#         print("forwards_months:",forwards_months)
#         try:
#
#             second_fw_month = int(forwards_months) + 1
#             print("second_fw_month:", second_fw_month)
#         except:
#             fwrd_contrct_mnths = 0
#             second_fw_month = 0
#             print("fwrd_contrct_mnths 0:", fwrd_contrct_mnths)
#             print("second_fw_month 0:", second_fw_month)
#
#         # first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(fwrd_contrct_mnths))
#         # second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_fw_month))
#         # print("first_month before unit:", first_month)
#         # print("second_month before unit:", second_month)
#
#         if bileteral_external=='Bilateral':
#             trade_id = "BLT" + "-" + "F" + "-" + randint_
#             print("tradeid BLT:", trade_id)
#
#             if c.single_dif=='diff':
#                         contract1 = ContractM.objects.filter(contract_name=c.contract1)[0]
#                         print("contract 1:",contract1)
#                         print("contract1.bbi_mt_conversion:",contract1.bbi_mt_conversion)
#
#                         contract2 = ContractM.objects.filter(contract_name=c.contract2)[0]
#                         print("contract 2:", contract2)
#
#                         try:
#                             second_fw_month_c1 = contract1.f_w_months + 1
#                             second_fw_month_c2 = contract2.f_w_months + 1
#                             print("second_fw_month_c1:", second_fw_month_c1)
#                         except:
#                             fwrd_contrct_mnths_c1 = 0
#                             second_fw_month_c1 = 0
#
#                             fwrd_contrct_mnths_c2 = 0
#                             second_fw_month_c2 = 0
#
#                         first_month_c1 = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_fw_month_c1))
#                         first_month_c2 = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_fw_month_c2))
#                         second_month_c1 = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_fw_month_c1))
#                         second_month_c2 = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_fw_month_c2))
#                         print("first_month before unit:", first_month_c1)
#                         print("second_month before unit:", second_month_c1)
#
#
#
#
#                         obj = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                                 tick=c.tick,fw_months=c.f_w_months,
#                                            unit=c.unit,
#                                            singl_dif=c.single_dif,
#                                            mini_major=c.major_mini,
#                                            mini_major_connection=c.major_mini_conn,
#                                            bbi_mt_conversion =c.bbi_mt_conversion,
#                                            block_fee=c.block_fee,
#                                            screen_fee =c.screen_fee,
#                                            bbi_mt=c.bbi_mt_conversion,
#                                            book=book,customer_account=company_account,
#                                            strategy_id=strategy,derivatives=derivatives,
#                                            volume=volume,customer_company=customer_company,
#                                            contract=contract_name,start_date=start_date,
#                                            end_date=end_date,price=price,approx_ep=approximate_ep,
#                                            holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                            notes=notes,trader_type=bileteral_external,buy_sell=buy_sell,
#                                            Trade_id = trade_id,
#                                            # calculated values
#                                            total_days=total_working_days, priced_days=priced_days,unpriced_days=unpriced_days,
#                                            priced_volume=priced_volume,unpriced_volume=unpriced_volume,total_volume=total_volume
#
#                                                )
#                         obj.save()
#                         obj.duplicate_id=obj.id
#                         obj.save()
#                         # if int(volume)<0:
#                         #     volume1=  abs(int(volume))
#                         # else:
#                         #     volume1=  '-'+str(volume)
#                         # obj1 = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                         #                          tick=c.tick,
#                         #                    unit=c.unit,
#                         #                    singl_dif=c.single_dif,
#                         #                    mini_major=c.major_mini,
#                         #                    mini_major_connection=c.major_mini_conn,
#                         #                    bbi_mt_conversion =c.bbi_mt_conversion,
#                         #                    block_fee=c.block_fee,
#                         #                    screen_fee =c.screen_fee,
#                         #                    bbi_mt=c.bbi_mt_conversion,
#                         #                    book=customer_company,customer_account=company_account,
#                         #                    strategy_id=strategy,derivatives=derivatives,
#                         #                    volume=volume1,customer_company=book,
#                         #                    contract=contract_name,start_date=start_date,
#                         #                    end_date=end_date,price=price,approx_ep=approximate_ep,
#                         #                    holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                         #                    notes=notes,duplicate_id=obj.id,bileteral_external=bileteral_external,buy_sell=buy_sell)
#                         # obj1.save()
#                         print("ROW 1")
#                         row1 = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                        tick=contract1.tick,fw_months=contract1.f_w_months,
#                                        unit=contract1.unit,
#                                        singl_dif=contract1.single_dif,
#                                        mini_major=contract1.major_mini,
#                                        mini_major_connection=contract1.major_mini_conn,
#                                        bbi_mt_conversion =contract1.bbi_mt_conversion,
#                                        block_fee=contract1.block_fee,
#                                        screen_fee =contract1.screen_fee,
#                                        bbi_mt=contract1.bbi_mt_conversion,
#                                        book=book,customer_account=company_account,
#                                        strategy_id=strategy,derivatives=derivatives,
#                                        volume=volume,customer_company=customer_company,
#                                        contract=contract1.contract_name,start_date=start_date,
#                                        end_date=end_date,price=price,approx_ep=approximate_ep,
#                                        holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                        notes=notes,duplicate_id=obj.id,trader_type=bileteral_external,buy_sell=buy_sell,
#                                        Trade_id=trade_id,
#                                         # calculated values
#                                        total_days=total_working_days, priced_days=priced_days, unpriced_days=unpriced_days,
#                                        priced_volume=priced_volume, unpriced_volume=unpriced_volume,total_volume=total_volume
#
#                                        )
#                         row1.save()
#                         print("ROW 2")
#                         if int(volume)<0:
#                             volume1=  abs(int(volume))
#                         else:
#                             volume1=  '-'+str(volume)
#                         row2 = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                                  tick=contract2.tick,fw_months=contract2.f_w_months,
#                                            unit=contract2.unit,
#                                            singl_dif=contract2.single_dif,
#                                            mini_major=contract2.major_mini,
#                                            mini_major_connection=contract2.major_mini_conn,
#                                            bbi_mt_conversion =contract2.bbi_mt_conversion,
#                                            block_fee=contract2.block_fee,
#                                            screen_fee =contract2.screen_fee,
#                                            bbi_mt=contract2.bbi_mt_conversion,
#                                            book=book,customer_account=company_account,
#                                            strategy_id=strategy,derivatives=derivatives,
#                                            volume=volume1,customer_company=customer_company,
#                                            contract=contract2.contract_name,start_date=start_date,
#                                            end_date=end_date,price=price,approx_ep=approximate_ep,
#                                            holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                            notes=notes,duplicate_id=obj.id,trader_type=bileteral_external,
#                                            buy_sell=buy_sell, Trade_id = trade_id,
#                                             # calculated values
#                                             total_days=total_working_days, priced_days=priced_days,
#                                             unpriced_days=unpriced_days, total_volume=total_volume_neg,
#                                             priced_volume=priced_volume_negative, unpriced_volume=unpriced_volume_negative,
#
#                                                 )
#                         row2.save()
#                       # first negative
#                         print("Duplicate of Object 1")
#                         if int(volume) < 0:
#                             volume1 = abs(int(volume))
#                         else:
#                             volume1 = '-' + str(volume)
#                         obj1 = SwapBlotterModel(date=date, clearer=clearer, trader_id=trader,
#                                                 tick=c.tick,fw_months=c.f_w_months,
#                                                 unit=c.unit,
#                                                 singl_dif=c.single_dif,
#                                                 mini_major=c.major_mini,
#                                                 mini_major_connection=c.major_mini_conn,
#                                                 bbi_mt_conversion=c.bbi_mt_conversion,
#                                                 block_fee=c.block_fee,
#                                                 screen_fee=c.screen_fee,
#                                                 bbi_mt=c.bbi_mt_conversion,
#                                                 book=customer_company, customer_account=company_account,
#                                                 strategy_id=strategy, derivatives=derivatives,
#                                                 volume=volume1, customer_company=book,
#                                                 contract=contract_name, start_date=start_date,
#                                                 end_date=end_date, price=price, approx_ep=approximate_ep,
#                                                 holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
#                                                 notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
#                                                 buy_sell=buy_sell, Trade_id = trade_id,
#                                                 # calculated values
#                                                 total_days=total_working_days, priced_days=priced_days,
#                                                 unpriced_days=unpriced_days,total_volume=total_volume_neg,
#                                                 priced_volume=priced_volume_negative,unpriced_volume=unpriced_volume_negative,
#
#
#                                                 )
#                         obj1.save()
#
#                         # end first negative
#
#                         print("Row 3")
#
#                         if int(volume)<0:
#                             volume1=  abs(int(volume))
#                         else:
#                             volume1=  '-'+str(volume)
#                         row3 = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                                  tick=contract1.tick,fw_months=contract1.f_w_months,
#                                            unit=contract1.unit,
#                                            singl_dif=contract1.single_dif,
#                                            mini_major=contract1.major_mini,
#                                            mini_major_connection=contract1.major_mini_conn,
#                                            bbi_mt_conversion =contract1.bbi_mt_conversion,
#                                            block_fee=contract1.block_fee,
#                                            screen_fee =contract1.screen_fee,
#                                            bbi_mt=contract1.bbi_mt_conversion,
#                                            book=customer_company,customer_account=company_account,
#                                            strategy_id=strategy,derivatives=derivatives,
#                                            volume=volume1,customer_company=book,
#                                            contract=contract1.contract_name,start_date=start_date,
#                                            end_date=end_date,price=price,approx_ep=approximate_ep,
#                                            holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                            notes=notes,duplicate_id=obj.id,trader_type=bileteral_external,
#                                            buy_sell=buy_sell,Trade_id = trade_id,
#                                             # calculated values
#                                             total_days=total_working_days, priced_days=priced_days,
#                                             unpriced_days=unpriced_days, priced_volume=priced_volume_negative,
#                                             unpriced_volume=unpriced_volume_negative,total_volume=total_volume_neg,
#
#
#                                                 )
#                         row3.save()
#
#                         print("Row 4")
#
#                         row4 = SwapBlotterModel(date=date, clearer=clearer, trader_id=trader,
#                                                 tick=contract2.tick,fw_months=contract2.f_w_months,
#                                                 unit=contract2.unit,
#                                                 singl_dif=contract2.single_dif,
#                                                 mini_major=contract2.major_mini,
#                                                 mini_major_connection=contract2.major_mini_conn,
#                                                 bbi_mt_conversion=contract2.bbi_mt_conversion,
#                                                 block_fee=contract2.block_fee,
#                                                 screen_fee=contract2.screen_fee,
#                                                 bbi_mt=contract2.bbi_mt_conversion,
#                                                 book=customer_company, customer_account=company_account,
#                                                 strategy_id=strategy, derivatives=derivatives,
#                                                 volume=volume, customer_company=book,
#                                                 contract=contract2.contract_name, start_date=start_date,
#                                                 end_date=end_date, price=price, approx_ep=approximate_ep,
#                                                 holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
#                                                 notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
#                                                 buy_sell=buy_sell, Trade_id = trade_id,
#                                                 # calculated values
#                                                 total_days=total_working_days, priced_days=priced_days,total_volume=total_volume,
#                                                 unpriced_days=unpriced_days,priced_volume=priced_volume,unpriced_volume=unpriced_volume,
#
#                                                 )
#                         row4.save()
#                         messages.info(request,'Saved')
#                         return HttpResponseRedirect('/swaps-blotter')
#
#             elif c.single_dif=='single':
#                 print("bilateral single")
#                 obj = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                            tick=c.tick,fw_months=c.f_w_months,
#                                            unit=c.unit,
#                                            singl_dif=c.single_dif,
#                                            mini_major=c.major_mini,
#                                            mini_major_connection=c.major_mini_conn,
#                                            bbi_mt_conversion =c.bbi_mt_conversion,
#                                            block_fee=c.block_fee,
#                                            screen_fee =c.screen_fee,
#                                            bbi_mt=c.bbi_mt_conversion,
#                                            book=book,customer_account=company_account,
#                                            strategy_id=strategy,derivatives=derivatives,
#                                            volume=volume,customer_company=customer_company,
#                                            contract=contract_name,start_date=start_date,
#                                            end_date=end_date,price=price,approx_ep=approximate_ep,
#                                            holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                            notes=notes,trader_type=bileteral_external,
#                                            buy_sell=buy_sell, Trade_id = trade_id,
#
#                                            # calculated values
#                                            total_days=total_working_days, priced_days=priced_days,
#                                            unpriced_days=unpriced_days,priced_volume=priced_volume,unpriced_volume=unpriced_volume,
#                                            total_volume= total_volume
#
#                                        )
#                 obj.save()
#                 obj.duplicate_id=obj.id
#                 obj.save()
#                 print("bilateral single copy")
#                 if int(volume)<0:
#                     volume1=  abs(int(volume))
#                 else:
#                     volume1=  '-'+str(volume)
#                     obj1 = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                             tick=c.tick,fw_months=c.f_w_months,
#                                            unit=c.unit,
#                                            singl_dif=c.single_dif,
#                                            mini_major=c.major_mini,
#                                            mini_major_connection=c.major_mini_conn,
#                                            bbi_mt_conversion =c.bbi_mt_conversion,
#                                            block_fee=c.block_fee,
#                                            screen_fee =c.screen_fee,
#                                            bbi_mt=c.bbi_mt_conversion,
#                                            book=customer_company,customer_account=company_account,
#                                            strategy_id=strategy,derivatives=derivatives,
#                                            volume=volume1,customer_company=book,
#                                            contract=contract_name,start_date=start_date,
#                                            end_date=end_date,price=price,approx_ep=approximate_ep,
#                                            holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                            notes=notes,duplicate_id=obj.id,trader_type=bileteral_external,
#                                            buy_sell=buy_sell,Trade_id = trade_id,
#
#                                            # calculated values
#                                            total_days=total_working_days, priced_days=priced_days,
#                                            unpriced_days=unpriced_days,priced_volume=priced_volume_negative,
#                                             unpriced_volume=unpriced_volume_negative, total_volume=total_volume_neg,
#
#                                             )
#                     obj1.save()
#                 messages.info(request,'Saved')
#                 return HttpResponseRedirect('/swaps-blotter')
#
#         elif bileteral_external=='External':
#             print("external diff")
#             trade_id = "EXT" + "-" + "F" + "-" + randint_
#             print("tradeid EXT:", trade_id)
#
#             if c.single_dif == 'diff':
#
#                 contract1 = ContractM.objects.filter(contract_name=c.contract1)[0]
#                 print("contract 1:", contract1)
#                 print("contract1.bbi_mt_conversion:", contract1.bbi_mt_conversion)
#                 contract2 = ContractM.objects.filter(contract_name=c.contract2)[0]
#                 print("contract 2:", contract2)
#
#                 obj = SwapBlotterModel(date=date,clearer=clearer,trader_id=trader,
#                                         tick=c.tick,
#                                    unit=c.unit,fw_months=c.f_w_months,
#                                    singl_dif=c.single_dif,
#                                    mini_major=c.major_mini,
#                                    mini_major_connection=c.major_mini_conn,
#                                    bbi_mt_conversion =c.bbi_mt_conversion,
#                                    block_fee=c.block_fee,
#                                    screen_fee =c.screen_fee,
#                                    bbi_mt=c.bbi_mt_conversion,
#                                    book=book,customer_account=company_account,
#                                    strategy_id=strategy,derivatives=derivatives,
#                                    volume=volume,customer_company=customer_company,
#                                    contract=contract_name,start_date=start_date,
#                                    end_date=end_date,price=price,approx_ep=approximate_ep,
#                                    holiday=holiday,type=type,efs_code=efs_code,broker=brocker,
#                                    notes=notes,trader_type=bileteral_external,
#                                    buy_sell=buy_sell,Trade_id = trade_id,
#                                    # calculated values
#                                     total_days=total_working_days, priced_days=priced_days,total_volume=total_volume,
#                                     unpriced_days=unpriced_days,priced_volume=priced_volume,unpriced_volume=unpriced_volume,
#
#                                        )
#                 obj.save()
#                 obj.duplicate_id=obj.id
#                 obj.save()
#
#                 print("row 1: positive")
#                 row1 = SwapBlotterModel(date=date, clearer=clearer, trader_id=trader,
#                                         tick=contract1.tick,fw_months=contract1.f_w_months,
#                                         unit=contract1.unit,
#                                         singl_dif=contract1.single_dif,
#                                         mini_major=contract1.major_mini,
#                                         mini_major_connection=contract1.major_mini_conn,
#                                         bbi_mt_conversion=contract1.bbi_mt_conversion,
#                                         block_fee=contract1.block_fee,
#                                         screen_fee=contract1.screen_fee,
#                                         bbi_mt=contract1.bbi_mt_conversion,
#                                         book=book, customer_account=company_account,
#                                         strategy_id=strategy, derivatives=derivatives,
#                                         volume=volume, customer_company=customer_company,
#                                         contract=contract1.contract_name, start_date=start_date,
#                                         end_date=end_date, price=price, approx_ep=approximate_ep,
#                                         holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
#                                         notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
#                                         buy_sell=buy_sell,Trade_id = trade_id,
#                                         # calculated values
#                                         total_days=total_working_days, priced_days=priced_days,total_volume=total_volume,
#                                         unpriced_days=unpriced_days,priced_volume=priced_volume,unpriced_volume=unpriced_volume,
#
#                                         )
#                 row1.save()
#
#                 print("row 2: Neagative")
#                 if int(volume) < 0:
#                     volume1 = abs(int(volume))
#                 else:
#                     volume1 = '-' + str(volume)
#                     row2 = SwapBlotterModel(date=date, clearer=clearer, trader_id=trader,
#                                         tick=contract2.tick,fw_months=contract2.f_w_months,
#                                         unit=contract2.unit,
#                                         singl_dif=contract2.single_dif,
#                                         mini_major=contract2.major_mini,
#                                         mini_major_connection=contract2.major_mini_conn,
#                                         bbi_mt_conversion=contract2.bbi_mt_conversion,
#                                         block_fee=contract2.block_fee,
#                                         screen_fee=contract2.screen_fee,
#                                         bbi_mt=contract2.bbi_mt_conversion,
#                                         book=customer_company, customer_account=company_account,
#                                         strategy_id=strategy, derivatives=derivatives,
#                                         volume=volume1, customer_company=book,
#                                         contract=contract2.contract_name, start_date=start_date,
#                                         end_date=end_date, price=price, approx_ep=approximate_ep,
#                                         holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
#                                         notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
#                                         buy_sell=buy_sell,Trade_id = trade_id,
#                                         # calculated values
#                                         total_days=total_working_days, priced_days=priced_days,
#                                         unpriced_days=unpriced_days,priced_volume=priced_volume_negative,
#                                         unpriced_volume=unpriced_volume_negative,total_volume=total_volume_neg,
#                                             )
#                     row2.save()
#                     messages.info(request,'Saved')
#                     return HttpResponseRedirect('/swaps-blotter')
#             else:
#                 print("ORIGINAL EXTERNAL")
#                 print("priced days:",priced_days)
#                 print("unpriced days:", unpriced_days)
#                 obj = SwapBlotterModel(date=date, clearer=clearer, trader_id=trader,
#                                        tick=c.tick,fw_months=c.f_w_months,
#                                        unit=c.unit,
#                                        singl_dif=c.single_dif,
#                                        mini_major=c.major_mini,
#                                        mini_major_connection=c.major_mini_conn,
#                                        bbi_mt_conversion=c.bbi_mt_conversion,
#                                        block_fee=c.block_fee,
#                                        screen_fee=c.screen_fee,
#                                        bbi_mt=c.bbi_mt_conversion,
#
#                                        book=book, customer_account=company_account,
#                                        strategy_id=strategy, derivatives=derivatives,
#                                        volume=volume, customer_company=customer_company,
#                                        contract=contract_name, start_date=start_date,
#                                        end_date=end_date, price=price, approx_ep=approximate_ep,
#                                        holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
#                                        notes=notes, trader_type=bileteral_external,
#                                        buy_sell=buy_sell,Trade_id=trade_id,
#                                        # calculated values
#                                        total_days=total_working_days, priced_days=priced_days,total_volume=total_volume_neg,
#                                        unpriced_days=unpriced_days,priced_volume=priced_volume,unpriced_volume=unpriced_volume,
#                                        )
#                 obj.save()
#                 print("done")
#                 messages.info(request, 'Saved')
#                 return HttpResponseRedirect('/swaps-blotter')





class SwapsBlotter(CheckUserMixins, View):

    def diff_contract(self, request, *data):

        date_value = data[0]
        bileteral_external = data[1]
        clearer = data[2]
        trader = data[3]
        book = data[4]
        customer_company = data[5]
        company_account = data[6]
        strategy = data[7]
        derivatives = data[8]
        volume = data[9]
        volume = float(volume)
        contract_name = data[10]
        start_date = data[11]
        end_date = data[12]
        price = data[13]
        price = float(price)
        approximate_ep = data[14]
        holiday = data[15]
        type = data[16]
        efs_code = data[17]
        brocker = data[18]
        diff_id = data[19]
        diff_unit_value = data[20]
        tick = data[21]
        notes = data[22]
        trade_id=data[23]

        # delete_feild =data[22]

        contract_list = []
        count = 0
        c = ContractM.objects.filter(contract_name=contract_name)[0]
        diff_contract_tick = tick

        contract1 = ContractM.objects.filter(contract_name=c.contract1)[0]
        sub_contract1_tick = contract1.tick
        sub_contract1_unit = contract1.unit
        sub_contract1_conversion = contract1.bbi_mt_conversion
        contract_list.append(contract1)

        contract2 = ContractM.objects.filter(contract_name=c.contract2)[0]
        sub_contract2_tick = contract2.tick
        sub_contract2_unit = contract2.unit
        sub_contract2_conversion = contract2.bbi_mt_conversion
        contract_list.append(contract2)

        sub_conv_bbl_mt = {sub_contract1_unit: sub_contract1_conversion, sub_contract2_unit: sub_contract2_conversion}
        contract_tick = {sub_contract1_unit: sub_contract1_tick, sub_contract2_unit: sub_contract2_tick}

        print(sub_conv_bbl_mt, contract_tick, '++++++++Tick,Conversion')



        print("contract_list", contract_list)






        for diff_contracts in contract_list:

            print("diff_contracts:", diff_contracts)

            count = count + 1
            swaps_contract_value = diff_contracts.contract_name
            swaps_contract_unit = diff_contracts.unit
            swaps_ticks_val = diff_contracts.tick

            swaps_screen_fee_val = diff_contracts.screen_fee
            swaps_block_fee_val = diff_contracts.block_fee
            conversion_value = diff_contracts.bbi_mt_conversion
            conversion_value_bbl_mt = diff_contracts.bbi_mt_conversion
            FW_Month = diff_contracts.f_w_months
            diff_single_value = diff_contracts.single_dif
            Major_Mini_value = diff_contracts.major_mini
            Mini_Conn_Contract_value = diff_contracts.major_mini_conn
            physical_code = diff_contracts.physical_code
            logical_code = diff_contracts.logical_code
            symbol_code = diff_contracts.symbol_code


            swaps_ticks_val = float(swaps_ticks_val)
            swaps_screen_fee_val = float(swaps_screen_fee_val)
            swaps_block_fee_val = float(swaps_block_fee_val)
            conversion_value = float(conversion_value)
            conversion_value_bbl_mt = float(conversion_value_bbl_mt)

            print("fw",FW_Month)

            if FW_Month == '':
                FW_Month = 0
            else:
                FW_Month = int(FW_Month)


            print(swaps_contract_value, 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            if diff_unit_value == 'MT':

                if sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                    conversion_value = float(conversion_value)
                    swaps_ticks_val = float(diff_contract_tick)

                    print('mt mt mt', conversion_value, swaps_ticks_val)

                elif sub_contract1_unit != sub_contract2_unit:

                    if swaps_contract_unit == 'bbl':

                        conversion_value = sub_conv_bbl_mt['MT']
                        conversion_value = float(conversion_value)
                        swaps_ticks_val = contract_tick['MT']
                    else:

                        conversion_value = conversion_value

                elif sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':
                    conversion_value = float(conversion_value)

            else:

                if diff_unit_value == 'bbl':

                    if sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

                    elif sub_contract1_unit != sub_contract2_unit:

                        if swaps_contract_unit == 'MT':

                            conversion_value = float(1)
                            swaps_ticks_val = contract_tick['bbl']

                        else:

                            conversion_value = float(1)

                    elif sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

            if (data[15] == 'non-common'):

                holiday = diff_contracts.holiday
            else:
                holiday = data[15]
            print(holiday, 'Working Till Here')

            try:
                second_FW_Month = int(FW_Month) + 1
            except:
                FW_Month = 0
                second_FW_Month = 0

            try:

                if brocker == 'Ice Block':

                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = 0.0
                    brokerage = 0.0

                elif brocker == 'Ice Screen':
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = round((float(swaps_screen_fee_val) * float(volume)), 3)
                    brokerage = 0.0

                else:

                    swaps_screen_fee_value = 0.0
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    brokerage = 0.0

            except:
                print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                raise

            print(swaps_block_fee_value, 'swaps_block_fee_value', 'swaps_block_fee_value', swaps_block_fee_value,
                  'brokerage', brokerage)

            from datetime import date
            todays_date = date.today()
            start_date_value = start_date
            end_date_value = end_date
            # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
            # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

            holiday_list = []
            holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
            for i in holiday_check:
                holiday_list.append(i)

            print(holiday_list, 'holiday_list')

            holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
            holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
            holiday_list = holiday_date_df['Dates'].to_list()
            total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
            print(total_swap_days, 'total_swap_days')

            today = todays_date.strftime("%d-%b-%y")
            todays_date = datetime.strptime(today, "%d-%b-%y")
            end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
            start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
            print(todays_date)
            print(start_date_value, 'start_date_value')
            print(end_date_value, 'end_date_value')

            # *******************Priced ,Unpriced Days*************************************************************************************************
            if todays_date <= start_date_value:

                unpriced_days = total_swap_days
                priced_days = 0

            elif (todays_date > start_date_value) and (todays_date <= end_date_value):

                unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
                priced_days = int(total_swap_days) - unpriced_days


            elif todays_date > end_date_value:
                unpriced_days = 0
                priced_days = int(total_swap_days)


            priced_volume = round(((priced_days / total_swap_days) * volume), 3)
            un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
            total_volume = round((priced_volume + un_priced_volume), 3)

            bbl_mt_conversion = round(float(conversion_value) * float(volume) * float(swaps_ticks_val), 3)
            kbbl_mt_conversion = round(
                ((float(conversion_value) * float(volume) * float(swaps_ticks_val)) / 1000), 3)
            unpriced_kbbl_mt = round(
                ((float(conversion_value) * float(un_priced_volume) * float(swaps_ticks_val)) / 1000),
                3)

            Ticks_value = swaps_ticks_val
            print(bbl_mt_conversion, 'bbl_mt_conversion', kbbl_mt_conversion, 'kbbl_mt_conversion', 'unpriced_kbbl_mt',
                  unpriced_kbbl_mt, Ticks_value, 'Ticks_value')

            print(FW_Month, 'FW_Month')
            print(second_FW_Month, 'second_FW_Month')

            first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
            first_month = first_month.strftime('01-%m-%Y')
            first_month = datetime.strptime(first_month, '%d-%m-%Y')
            first_month = first_month.date()
            print(first_month, 'first_month')

            second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
            second_month = second_month.strftime('01-%m-%Y')
            second_month = datetime.strptime(second_month, '%d-%m-%Y')
            second_month = second_month.date()
            print(second_month, 'second_month')

            print('swaps_contract_value', swaps_contract_value, first_month, 'first_monthworks', second_month,
                  'second_month', 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            # Last Traded Date Starting***************************************#
            if swaps_contract_value == 'RBOB 1st Line':
                print("contract_name_str,", swaps_contract_value)
                print("hello loop")
                filter_column = 'RBOB_Gasoline_futures'
            elif (swaps_contract_value == 'LS GO 1st Line') or (swaps_contract_value == 'LS GO 1st Line Mini'):
                filter_column = 'Ls_gas_oil'
            elif (swaps_contract_value == 'Brent 1st Line') or (swaps_contract_value == 'Brent 1st Line Mini') :
                filter_column = 'Brent_crude_futures'

            elif swaps_contract_value == 'WTI Crude Futures':
                filter_column = 'WTI_crude_futures'

            else:
                filter_column = swaps_contract_value
                print("Not matching company NAMEE")

            future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                           'Heating_oil_futures', 'WTI_crude_futures']

            if filter_column in future_ltd_column_name_list:

                try:
                    contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

                except:
                    print('Error,LTD Not present in Admin side')

                for sub in contract_date_value:
                    LTD = sub[filter_column]
                    # LTD = datetime.strptime(LTD,'%d-%m-%Y')

                print('Last Traded Day:', LTD)

                yesterday = todays_date - timedelta(days=1)
                yesterday = yesterday.date()
                print("yesterday_date", yesterday)

                first_month_value = first_month.strftime('01-%m-%Y')
                second_month_value = second_month.strftime('01-%m-%Y')

                first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
                second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

                First_Month_value = first_month.strftime("01-%b-%y")
                Second_Month_value = second_month.strftime("01-%b-%y")

                ## Last Trading Month

                Start_date_LTD = LTD.strftime("%Y-%m-01")
                Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
                Start_date_LTD = Start_date_LTD.date()

                month = LTD.month
                year = LTD.year
                first_date, num_days = calendar.monthrange(year, month)

                # End Date Trading Month
                End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
                End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

                # Last Business day before LTD

                offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                                n=1)  # change holiday list from singapore to real holiday list
                Day_before_LTD = LTD - offset_x

                from datetime import date
                today_format = date.today()

                start_date_value = start_date_value.date()
                Day_before_LTD = Day_before_LTD.date()
                End_Date_LTD = End_Date_LTD.date()

                print("LTD", LTD)
                print("Start_date_LTD:", Start_date_LTD)
                print("Day_before_LTD:", Day_before_LTD)
                print("End_Date_LTD:", End_Date_LTD)
                print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
                #
                #    # Total Days in Trading month
                Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                    holidays=holiday_list))  # change holiday list from singapore to real holiday list
                # Number of trading Days before LTD
                No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
                # Number of trading Days after LTD
                No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

                First_Month_Days_value = No_days_BF_LTD
                Second_Month_Days_value = No_days_AF_LTD

                print("Total_days_LTD NEW", Total_days_LTD)
                print("No_days_BF_LTD", No_days_BF_LTD)
                print("No_days_AF_LTD", No_days_AF_LTD)
                print("First_Month_Days_value:", First_Month_Days_value)
                print("Second_Month_Days_value:", Second_Month_Days_value)

                # try:
                #
                #     first_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
                #     second_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
                #
                #     First_Month_Settle_Price_value = first_month_price_value
                #     Second_Month_Price_value = second_month_price_value
                #
                # except:
                #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
                #     raise

                if (today_format <= start_date_value):
                    print('first')

                    # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                    #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                    # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                    priced_days_BF_LTD = 0
                    unpriced_days_BF_LTD = No_days_BF_LTD
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD


                elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                    print('second')
                    priced_days_BF_LTD = len(
                        pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                    #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                    #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                    #
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


                elif (today_format == LTD):

                    print('3rd')
                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

                elif today_format > LTD and today_format <= End_Date_LTD:
                    print('4rth')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_AF_LTD = len(
                        pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[
                    #     settlement_prices_df["Date"].isin(
                    #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                    #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round(
                    #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                    #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


                elif today_format > End_Date_LTD:
                    print('5th')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = No_days_AF_LTD
                    unpriced_days_AF_LTD = 0

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)

                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                    #                                  3)

                First_Month_value = first_month.strftime("%d-%b-%y")
                Second_Month_value = second_month.strftime("%d-%b-%y")

                print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                      priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

                futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                       3)
                futures_equivalent_second_Month = round(
                    ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

                Futures_equivalent_First_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
                Futures_equivalent_Second_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

                print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                      'futures_equivalent_second_Month')
                print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                      'Futures_equivalent_Second_kbbl')


            else:

                futures_equivalent_first_Month = 0.0
                futures_equivalent_second_Month = 0.0
                Futures_equivalent_First_kbbl = 0.0
                Futures_equivalent_Second_kbbl = 0.0
                first_month = start_date
                second_month = end_date
                First_Month_value = ''
                Second_Month_value = ''
                First_Month_Days_value = 0
                Second_Month_Days_value = 0
            print('if contract2', contract2)

            if diff_contracts == (contract2):

                print('its Contract2', contract2, volume, 'volume')
                volume = -(volume) if float(volume) > 0 else abs(volume)
                priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
                un_priced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
                total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)

                bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
                kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                    kbbl_mt_conversion)

                unpriced_kbbl_mt = round(-(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt),
                                         3)

                futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                    futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)

                futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                    futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)

                Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                    Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

                Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                    Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            print('Second_Contract', volume, 'volume', priced_volume, 'priced_volume', 'un_priced_volume',
                  un_priced_volume, 'total_volume', total_volume)
            print('bbl_mt_conversion', bbl_mt_conversion, 'kbbl_mt_conversion', kbbl_mt_conversion, 'unpriced_kbbl_mt',
                  'unpriced_kbbl_mt',
                  futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', 'Futures_equivalent_Second_kbbl',
                  Futures_equivalent_Second_kbbl)

            diff_single_value = str('Diff') + '-' + 'Sub'

            print(date_value, 'date_value')

            print("total_days:",total_swap_days)

            new_total_days= int(total_swap_days)

            print("new_total_days:",new_total_days)



            diff_obj = SwapBlotterModel(date=date_value,Trade_id=trade_id, trader_id=trader, clearer=clearer,
                                        tick=Ticks_value,
                                        unit=swaps_contract_unit,
                                        singl_dif=diff_single_value,
                                        mini_major=Major_Mini_value,
                                        mini_major_connection=Mini_Conn_Contract_value,
                                        bbi_mt_conversion=conversion_value,
                                        block_fee=swaps_block_fee_value,
                                        screen_fee=swaps_screen_fee_value,
                                        bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                                        book=book, customer_account=company_account,
                                        strategy_id=strategy, derivatives=derivatives,
                                        volume=volume, customer_company=customer_company,
                                        contract=swaps_contract_value, start_date=start_date,
                                        end_date=end_date, price=price, approx_ep=approximate_ep,
                                        holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                        notes=notes, trader_type=bileteral_external, buy_sell='test',
                                        fw_months=FW_Month,physical_code=physical_code,
                                        priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                                        priced_volume=priced_volume, unpriced_volume=un_priced_volume, unpriced_kbbl_mt=unpriced_kbbl_mt,
                                        First_month=first_month,Second_month=second_month,
                                        first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                                        futures_equiv_first=futures_equivalent_first_Month,futures_equiv_second=futures_equivalent_second_Month,
                                        futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl,total_days=total_swap_days,total_n_days=new_total_days)
            diff_obj.save()
            print('++dd++')
            print("total_days:", total_swap_days)
            diff_obj.duplicate_id = diff_id
            diff_obj.save()
            messages.info(request, 'Saved')
            print('diff save')
        # print("Executuion stopped")
        # sys.exit("error message")
        # print("total_days:", total_swap_days)

    def get(self, request):
        book = Book.objects.all()
        clearer = ClearearM.objects.values_list('name', flat=True).distinct()
        trader = Traders.objects.all()
        book = Book.objects.all()
        customer_company = CompanyInvestmentModel.objects.all()
        strategy = Strategy.objects.all()
        derivatives = DerivativeM.objects.all()
        type = TYPEMODEL.objects.all()
        today = date.today()
        print("first today:", today)

        search_query = request.GET.get('search_query')
        print("search_query",search_query)

        if search_query:
            data1 = SwapBlotterModel.objects.filter(Q(customer_company__istartswith=search_query)|Q(trader__name__istartswith=search_query)
                                                    |Q(customer_account__istartswith=search_query)|Q(broker__istartswith=search_query)|Q(efs_code__istartswith=search_query)|Q(contract__istartswith=search_query)

                                                    | Q(clearer__istartswith=search_query) | Q(strategy__name__istartswith=search_query) | Q(volume__istartswith=search_query) | Q(holiday__istartswith=search_query)

                                                    | Q(type__istartswith=search_query) | Q(notes__istartswith=search_query) | Q(Trade_id__istartswith=search_query) | Q(   tick__istartswith=search_query)


                                                    )
        else:

            data1 = SwapBlotterModel.objects.filter(date__icontains=today)

        paginator = Paginator(data1,25)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        context = {'book': book, 'clearer': clearer, 'trader': trader,
                   'customer_company': customer_company, 'strategy': strategy, 'derivatives': derivatives,
                   'type': type, 'page_obj': data}
        return render(request, "backend/swaps_bloter.html", context)

    def post(self, request):

        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        print(bileteral_external,'bileteral_external')
        clearer = request.POST.get('clearer', '')  # id
        print(clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        company_account = request.POST.get('company_account', '')
        strategy = request.POST.get('strategy', '')  # id
        derivatives = request.POST.get('derivatives', '')
        volume = request.POST.get('volume', '')
        volume = float(volume)
        customer_company = request.POST.get('customer_company', '')
        buy_sell = request.POST.get('buy_sell', '')
        contract_name = request.POST.get('contract_name', '')
        print("contract_name:",contract_name)
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        type = request.POST.get('type', '')
        pb_id = request.POST.get('pb_id', '')
        print("pb_id",pb_id)
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        notes = request.POST.get('notes', '')
        book = request.POST.get('book', '')

        unit_c = request.POST.get('unit_c', '')
        tick_c = request.POST.get('tick_c', '')


        delete_feild = request.POST.get('delete_feild')

        randint_ = str(random.randint(1000, 99999))

        if bileteral_external == "External":
            trade_id = "EXT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)
        elif bileteral_external == "Bilateral":
            trade_id = "BLT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)

        c = ContractM.objects.filter(contract_name=contract_name)[0]
        tick = c.tick
        print(tick, 'tick')
        tick = float(tick)
        unit = c.unit
        print("unit:",unit)


        singl_dif = c.single_dif
        print("singl_dif:",singl_dif)
        mini_major = c.major_mini
        print("mini_major:", mini_major)
        mini_major_connection = c.major_mini_conn
        print("mini_major_connection:", mini_major_connection)
        physical_code = c.physical_code
        print("physical_code:", physical_code)
        logical_code = c.logical_code
        print("logical_code:", logical_code)
        symbol_code = c.symbol_code
        print("symbol_code:", symbol_code)

        block_fee = c.block_fee
        print("block_fee:", block_fee)

        screen_fee = c.screen_fee
        print("screen_fee:", screen_fee)

        screen_fee = float(str(screen_fee))
        print("screen_fee2:", screen_fee)


        bbl_mt = c.bbi_mt_conversion
        print("bbl_mt:", bbl_mt)


        bbl_mt = float(str(bbl_mt))
        print("bbl_mt:", bbl_mt)


        FW_Month = c.f_w_months
        print("FW_Month:", FW_Month)

        if FW_Month == '':
            FW_Month = 0
        else:
            FW_Month = int(FW_Month)
            print("FW_Month:", FW_Month)


        print(block_fee, 'block_fee', screen_fee, 'screen_fee', FW_Month)

        try:
            second_FW_Month = FW_Month + 1
        except:
            FW_Month = 0
            second_FW_Month = 0

        try:

            if brocker == 'Ice Block':

                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = 0.0
                brokerage = 0.0

            elif brocker == 'Ice Screen':
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = round((float(screen_fee) * float(volume)), 3)
                brokerage = 0.0

            else:

                swaps_screen_fee_value = 0.0
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                brokerage = 0.0

        except:
            print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            raise

        swaps_screen_fee_value = round(-(abs(swaps_screen_fee_value)), 3)
        swaps_block_fee_value = round(-(abs(swaps_block_fee_value)), 3)
        # total_fees = float(clearer_rate_calc) + float(brokerage) + float(swaps_screen_fee_value) + float(
        #     swaps_block_fee_value)

        total_fees = float(brokerage) + float(swaps_screen_fee_value) + float(
            swaps_block_fee_value)
        total_fees = round(total_fees, 3)

        print("testingbileteral_external:",bileteral_external)

        if bileteral_external == 'Bilateral':
            # clearer_rate_calc = 0.0
            swaps_block_fee_value = 0.0
            swaps_screen_fee_value = 0.0
            brokerage = 0.0

        from datetime import date
        todays_date = date.today()
        start_date_value = start_date
        end_date_value = end_date
        # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
        # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

        holiday_list = []
        holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        for i in holiday_check:
            holiday_list.append(i)

        print(holiday_list, 'holiday_list')

        holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
        print(total_swap_days, 'total_swap_days')

        today = todays_date.strftime("%d-%b-%y")
        todays_date = datetime.strptime(today, "%d-%b-%y")
        end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
        start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
        print(todays_date)
        print(start_date_value, 'start_date_value')
        print(end_date_value, 'end_date_value')

        # *******************Priced ,Unpriced Days*************************************************************************************************
        if todays_date <= start_date_value:

            unpriced_days = total_swap_days
            priced_days = 0

        elif (todays_date > start_date_value) and (todays_date <= end_date_value):

            unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
            priced_days = int(total_swap_days) - unpriced_days


        elif todays_date > end_date_value:
            unpriced_days = 0
            priced_days = int(total_swap_days)


        priced_volume = round(((priced_days / total_swap_days) * volume), 3)
        un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
        total_volume = round((priced_volume + un_priced_volume), 3)

        bbl_mt_conversion = round(float(bbl_mt) * float(volume) * float(tick), 3)
        kbbl_mt_conversion = round(
            ((float(bbl_mt) * float(volume) * float(tick)) / 1000), 3)
        unpriced_kbbl_mt = round(
            ((float(bbl_mt) * float(un_priced_volume) * float(tick)) / 1000),
            3)

        first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
        first_month = first_month.strftime('01-%m-%Y')
        first_month = datetime.strptime(first_month, '%d-%m-%Y')
        first_month = first_month.date()
        print(first_month, 'first_month')

        second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
        second_month = second_month.strftime('01-%m-%Y')
        second_month = datetime.strptime(second_month, '%d-%m-%Y')
        second_month = second_month.date()
        print(second_month, 'second_month')

        # Last Traded Date Starting***************************************#
        if contract_name == 'RBOB 1st Line':
            print("contract_name_str,", contract_name)
            print("hello loop")
            filter_column = 'RBOB_Gasoline_futures'
        elif (contract_name == 'LS GO 1st Line') or (contract_name == 'LS GO 1st Line Mini'):
            filter_column = 'Ls_gas_oil'
        elif (contract_name == 'Brent 1st Line') or (contract_name == 'Brent 1st Line Mini'):
            filter_column = 'Brent_crude_futures'

        elif contract_name == 'WTI Crude Futures':
            filter_column = 'WTI_crude_futures'

        else:
            filter_column = contract_name
            print("Not matching company NAMEE")

        future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                       'Heating_oil_futures', 'WTI_crude_futures']

        if filter_column in future_ltd_column_name_list:

            try:
                contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

            except:
                print('Error,LTD Not present in Admin side')

            for sub in contract_date_value:
                LTD = sub[filter_column]
                # LTD = datetime.strptime(LTD,'%d-%m-%Y')

            print('Last MAin Traded Day:', LTD)

            yesterday = todays_date - timedelta(days=1)
            yesterday = yesterday.date()
            print("yesterday_date", yesterday)

            first_month_value = first_month.strftime('01-%m-%Y')
            second_month_value = second_month.strftime('01-%m-%Y')

            first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
            second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

            First_Month_value = first_month.strftime("01-%b-%y")
            Second_Month_value = second_month.strftime("01-%b-%y")

            ## Last Trading Month

            Start_date_LTD = LTD.strftime("%Y-%m-01")
            Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
            Start_date_LTD = Start_date_LTD.date()

            month = LTD.month
            year = LTD.year
            first_date, num_days = calendar.monthrange(year, month)

            # End Date Trading Month
            End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
            End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

            # Last Business day before LTD

            offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                            n=1)  # change holiday list from singapore to real holiday list
            Day_before_LTD = LTD - offset_x

            from datetime import date
            today_format = date.today()

            start_date_value = start_date_value.date()
            Day_before_LTD = Day_before_LTD.date()
            End_Date_LTD = End_Date_LTD.date()

            print("LTD", LTD)
            print("Start_date_LTD:", Start_date_LTD)
            print("Day_before_LTD:", Day_before_LTD)
            print("End_Date_LTD:", End_Date_LTD)
            print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
            #
            #    # Total Days in Trading month
            Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                holidays=holiday_list))  # change holiday list from singapore to real holiday list
            # Number of trading Days before LTD
            No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
            # Number of trading Days after LTD
            No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

            First_Month_Days_value = No_days_BF_LTD
            Second_Month_Days_value = No_days_AF_LTD

            print("Total_days_LTD NEW", Total_days_LTD)
            print("No_days_BF_LTD", No_days_BF_LTD)
            print("No_days_AF_LTD", No_days_AF_LTD)
            print("First_Month_Days_value:", First_Month_Days_value)
            print("Second_Month_Days_value:", Second_Month_Days_value)

            # try:
            #
            #     first_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
            #     second_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
            #
            #     First_Month_Settle_Price_value = first_month_price_value
            #     Second_Month_Price_value = second_month_price_value
            #
            # except:
            #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
            #     raise

            if (today_format <= start_date_value):
                print('first')

                # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                priced_days_BF_LTD = 0
                unpriced_days_BF_LTD = No_days_BF_LTD
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD


            elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                print('second')
                priced_days_BF_LTD = len(
                    pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                #
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


            elif (today_format == LTD):

                print('3rd')
                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

            elif today_format > LTD and today_format <= End_Date_LTD:
                print('4rth')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_AF_LTD = len(pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[
                #     settlement_prices_df["Date"].isin(
                #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round(
                #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


            elif today_format > End_Date_LTD:
                print('5th')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = No_days_AF_LTD
                unpriced_days_AF_LTD = 0

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)

                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                #                                  3)

            First_Month_value = first_month.strftime("%d-%b-%y")
            Second_Month_value = second_month.strftime("%d-%b-%y")

            print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                  priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

            futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                   3)
            futures_equivalent_second_Month = round(
                ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

            Futures_equivalent_First_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
            Futures_equivalent_Second_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

            print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                  'Futures_equivalent_Second_kbbl')


        else:

            futures_equivalent_first_Month = 0.0
            futures_equivalent_second_Month = 0.0
            Futures_equivalent_First_kbbl = 0.0
            Futures_equivalent_Second_kbbl = 0.0
            first_month = start_date
            second_month = end_date
            First_Month_Days_value = 0
            Second_Month_Days_value = 0.0
            First_Month_value = ''
            Second_Month_value = ''

        print('ManinTrade')
        print("Physical code:",physical_code)
        date = request.POST.get('date', '')


        print("datasave")

        obj = SwapBlotterModel(date=date, Trade_id=trade_id, trader_type=bileteral_external,clearer=clearer, trader_id=trader,
                               book=book, customer_account=company_account,
                               strategy_id=strategy, derivatives=derivatives,
                               volume=volume, customer_company=customer_company,
                               contract=contract_name, start_date=start_date,
                               end_date=end_date, price=price, approx_ep=approximate_ep,
                               holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                               tick=tick,unit=unit,singl_dif=singl_dif,mini_major=c.major_mini,
                               mini_major_connection=c.major_mini_conn,
                               bbi_mt_conversion=bbl_mt,
                               block_fee=block_fee,physica_blotter_connect=pb_id,
                               screen_fee=screen_fee,fw_months=FW_Month,physical_code=physical_code,
                               bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                               notes=notes, buy_sell=buy_sell,
                               total_days=total_swap_days,
                               priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                               priced_volume=priced_volume,unpriced_volume=un_priced_volume, unpriced_kbbl_mt=unpriced_kbbl_mt,
                               First_month=first_month,Second_month=second_month,
                               first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                               futures_equiv_first=futures_equivalent_first_Month,futures_equiv_second=futures_equivalent_second_Month,
                               futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl)
        obj.save()
        obj.duplicate_id = obj.id
        obj.save()
        messages.info(request, 'Saved')


        diff_id = obj.id
        print(
            '++++++++++++++++++++first save from form++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        if  (bileteral_external == 'External') and singl_dif != 'diff':
            return HttpResponseRedirect('/swaps-blotter')


        print("secondif")

        if singl_dif == 'diff':
            diff_result = self.diff_contract(request, date, bileteral_external, clearer, trader, book, customer_company,
                                             company_account, strategy, derivatives, volume, contract_name,
                                             start_date, end_date, price, approximate_ep, holiday, type, efs_code,
                                             brocker, diff_id, unit, tick, notes,trade_id)
            print(diff_result, '++++++++dIff Call')

            print("3rd if")

        if bileteral_external == 'Bilateral':
            print('bilateral')

            print("4th if")

            volume = -(volume) if float(volume) > 0 else abs(volume)
            int_priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
            int_unpriced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
            int_total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)
            int_bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
            int_kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                kbbl_mt_conversion)
            int_unpriced_kbbl_mt = -(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt)
            int_unpriced_kbbl_mt = round(int_unpriced_kbbl_mt, 3)

            int_futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)
            int_futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)
            int_Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

            int_Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            int_clearing_rate = 0.0

            int_brokerage = 0.0
            int_screen_fee = 0.0
            int_block_fee = 0.0
            int_total_fee = 0.0


            print("save copy")

            obj1 = SwapBlotterModel(date=date, Trade_id=trade_id,clearer=clearer, trader_id=trader,
                                    tick=c.tick,
                                    unit=c.unit,
                                    singl_dif=c.single_dif,
                                    mini_major=c.major_mini,
                                    mini_major_connection=c.major_mini_conn,
                                    bbi_mt_conversion=c.bbi_mt_conversion,
                                    block_fee=c.block_fee,
                                    screen_fee=c.screen_fee,fw_months=FW_Month,
                                    bbi_mt=int_bbl_mt_conversion, kbbl_mt_conversion=int_kbbl_mt_conversion,
                                    book=customer_company, customer_account=company_account,
                                    strategy_id=strategy, derivatives=derivatives,physica_blotter_connect=pb_id,
                                    volume=volume, customer_company=book,physical_code=physical_code,
                                    contract=contract_name, start_date=start_date,
                                    end_date=end_date, price=price, approx_ep=approximate_ep,
                                    holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                    notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
                                    buy_sell=buy_sell, total_days=total_swap_days,
                                    priced_days=priced_days, unpriced_days=unpriced_days, total_volume=int_total_volume,
                                    priced_volume=int_priced_volume, unpriced_volume=int_unpriced_volume, unpriced_kbbl_mt=int_unpriced_kbbl_mt,
                                    First_month=first_month,Second_month=second_month,
                                    first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                                    futures_equiv_first=int_futures_equivalent_first_Month,futures_equiv_second=int_futures_equivalent_second_Month,
                                    futures_equiv_first_kbbl=int_Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=int_Futures_equivalent_Second_kbbl)
            obj1.save()
            obj.duplicate_id = diff_id
            obj.save()

            if (c.single_dif == 'diff') and (bileteral_external == 'Bilateral'):
                diff_result_bilat = self.diff_contract(request, date, bileteral_external, clearer, trader,
                                                       customer_company,
                                                       book, company_account, strategy, derivatives, volume,
                                                       contract_name,
                                                       start_date, end_date, price, approximate_ep, holiday, type,
                                                       efs_code,
                                                       brocker, diff_id, unit, tick, notes,trade_id)

                print(diff_result_bilat)

        print('first return')

        # update_database(request)

        messages.info(request, 'Saved')
        return HttpResponseRedirect('/swaps-blotter')



#######################################################################             Copy swap Blotter     #########################################################################################


class CopySwapsBlotter(CheckUserMixins, View):

    def diff_contract(self, request, *data):

        date_value = data[0]
        bileteral_external = data[1]
        clearer = data[2]
        trader = data[3]
        book = data[4]
        customer_company = data[5]
        company_account = data[6]
        strategy = data[7]
        derivatives = data[8]
        volume = data[9]
        volume = float(volume)
        contract_name = data[10]
        start_date = data[11]
        end_date = data[12]
        price = data[13]
        price = float(price)
        approximate_ep = data[14]
        holiday = data[15]
        type = data[16]
        efs_code = data[17]
        brocker = data[18]
        diff_id = data[19]
        diff_unit_value = data[20]
        tick = data[21]
        notes = data[22]
        trade_id=data[23]

        # delete_feild =data[22]

        contract_list = []
        count = 0
        c = ContractM.objects.filter(contract_name=contract_name)[0]
        diff_contract_tick = tick

        contract1 = ContractM.objects.filter(contract_name=c.contract1)[0]
        sub_contract1_tick = contract1.tick
        sub_contract1_unit = contract1.unit
        sub_contract1_conversion = contract1.bbi_mt_conversion
        contract_list.append(contract1)

        contract2 = ContractM.objects.filter(contract_name=c.contract2)[0]
        sub_contract2_tick = contract2.tick
        sub_contract2_unit = contract2.unit
        sub_contract2_conversion = contract2.bbi_mt_conversion
        contract_list.append(contract2)

        sub_conv_bbl_mt = {sub_contract1_unit: sub_contract1_conversion, sub_contract2_unit: sub_contract2_conversion}
        contract_tick = {sub_contract1_unit: sub_contract1_tick, sub_contract2_unit: sub_contract2_tick}

        print(sub_conv_bbl_mt, contract_tick, '++++++++Tick,Conversion')



        print("contract_list", contract_list)






        for diff_contracts in contract_list:

            print("diff_contracts:", diff_contracts)

            count = count + 1
            swaps_contract_value = diff_contracts.contract_name
            swaps_contract_unit = diff_contracts.unit
            swaps_ticks_val = diff_contracts.tick

            swaps_screen_fee_val = diff_contracts.screen_fee
            swaps_block_fee_val = diff_contracts.block_fee
            conversion_value = diff_contracts.bbi_mt_conversion
            conversion_value_bbl_mt = diff_contracts.bbi_mt_conversion
            FW_Month = diff_contracts.f_w_months
            diff_single_value = diff_contracts.single_dif
            Major_Mini_value = diff_contracts.major_mini
            Mini_Conn_Contract_value = diff_contracts.major_mini_conn
            physical_code = diff_contracts.physical_code
            logical_code = diff_contracts.logical_code
            symbol_code = diff_contracts.symbol_code


            swaps_ticks_val = float(swaps_ticks_val)
            swaps_screen_fee_val = float(swaps_screen_fee_val)
            swaps_block_fee_val = float(swaps_block_fee_val)
            conversion_value = float(conversion_value)
            conversion_value_bbl_mt = float(conversion_value_bbl_mt)

            print("fw",FW_Month)

            if FW_Month == '':
                FW_Month = 0
            else:
                FW_Month = int(FW_Month)


            print(swaps_contract_value, 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            if diff_unit_value == 'MT':

                if sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                    conversion_value = float(conversion_value)
                    swaps_ticks_val = float(diff_contract_tick)

                    print('mt mt mt', conversion_value, swaps_ticks_val)

                elif sub_contract1_unit != sub_contract2_unit:

                    if swaps_contract_unit == 'bbl':

                        conversion_value = sub_conv_bbl_mt['MT']
                        conversion_value = float(conversion_value)
                        swaps_ticks_val = contract_tick['MT']
                    else:

                        conversion_value = conversion_value

                elif sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':
                    conversion_value = float(conversion_value)

            else:

                if diff_unit_value == 'bbl':

                    if sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

                    elif sub_contract1_unit != sub_contract2_unit:

                        if swaps_contract_unit == 'MT':

                            conversion_value = float(1)
                            swaps_ticks_val = contract_tick['bbl']

                        else:

                            conversion_value = float(1)

                    elif sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

            if (data[15] == 'non-common'):

                holiday = diff_contracts.holiday
            else:
                holiday = data[15]
            print(holiday, 'Working Till Here')

            try:
                second_FW_Month = int(FW_Month) + 1
            except:
                FW_Month = 0
                second_FW_Month = 0

            try:

                if brocker == 'Ice Block':

                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = 0.0
                    brokerage = 0.0

                elif brocker == 'Ice Screen':
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = round((float(swaps_screen_fee_val) * float(volume)), 3)
                    brokerage = 0.0

                else:

                    swaps_screen_fee_value = 0.0
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    brokerage = 0.0

            except:
                print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                raise

            print(swaps_block_fee_value, 'swaps_block_fee_value', 'swaps_block_fee_value', swaps_block_fee_value,
                  'brokerage', brokerage)

            from datetime import date
            todays_date = date.today()
            start_date_value = start_date
            end_date_value = end_date
            # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
            # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

            holiday_list = []
            holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
            for i in holiday_check:
                holiday_list.append(i)

            print(holiday_list, 'holiday_list')

            holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
            holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
            holiday_list = holiday_date_df['Dates'].to_list()
            total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
            print(total_swap_days, 'total_swap_days')

            today = todays_date.strftime("%d-%b-%y")
            todays_date = datetime.strptime(today, "%d-%b-%y")
            end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
            start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
            print(todays_date)
            print(start_date_value, 'start_date_value')
            print(end_date_value, 'end_date_value')

            # *******************Priced ,Unpriced Days*************************************************************************************************
            if todays_date <= start_date_value:

                unpriced_days = total_swap_days
                priced_days = 0

            elif (todays_date > start_date_value) and (todays_date <= end_date_value):

                unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
                priced_days = int(total_swap_days) - unpriced_days


            elif todays_date > end_date_value:
                unpriced_days = 0
                priced_days = int(total_swap_days)


            priced_volume = round(((priced_days / total_swap_days) * volume), 3)
            un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
            total_volume = round((priced_volume + un_priced_volume), 3)

            bbl_mt_conversion = round(float(conversion_value) * float(volume) * float(swaps_ticks_val), 3)
            kbbl_mt_conversion = round(
                ((float(conversion_value) * float(volume) * float(swaps_ticks_val)) / 1000), 3)
            unpriced_kbbl_mt = round(
                ((float(conversion_value) * float(un_priced_volume) * float(swaps_ticks_val)) / 1000),
                3)

            Ticks_value = swaps_ticks_val
            print(bbl_mt_conversion, 'bbl_mt_conversion', kbbl_mt_conversion, 'kbbl_mt_conversion', 'unpriced_kbbl_mt',
                  unpriced_kbbl_mt, Ticks_value, 'Ticks_value')

            print(FW_Month, 'FW_Month')
            print(second_FW_Month, 'second_FW_Month')

            first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
            first_month = first_month.strftime('01-%m-%Y')
            first_month = datetime.strptime(first_month, '%d-%m-%Y')
            first_month = first_month.date()
            print(first_month, 'first_month')

            second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
            second_month = second_month.strftime('01-%m-%Y')
            second_month = datetime.strptime(second_month, '%d-%m-%Y')
            second_month = second_month.date()
            print(second_month, 'second_month')

            print('swaps_contract_value', swaps_contract_value, first_month, 'first_monthworks', second_month,
                  'second_month', 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            # Last Traded Date Starting***************************************#
            if swaps_contract_value == 'RBOB 1st Line':
                print("contract_name_str,", swaps_contract_value)
                print("hello loop")
                filter_column = 'RBOB_Gasoline_futures'
            elif (swaps_contract_value == 'LS GO 1st Line') or (swaps_contract_value == 'LS GO 1st Line Mini'):
                filter_column = 'Ls_gas_oil'
            elif (swaps_contract_value == 'Brent 1st Line') or (swaps_contract_value == 'Brent 1st Line Mini') :
                filter_column = 'Brent_crude_futures'

            elif swaps_contract_value == 'WTI Crude Futures':
                filter_column = 'WTI_crude_futures'

            else:
                filter_column = swaps_contract_value
                print("Not matching company NAMEE")

            future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                           'Heating_oil_futures', 'WTI_crude_futures']

            if filter_column in future_ltd_column_name_list:

                try:
                    contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

                except:
                    print('Error,LTD Not present in Admin side')

                for sub in contract_date_value:
                    LTD = sub[filter_column]
                    # LTD = datetime.strptime(LTD,'%d-%m-%Y')

                print('Last Traded Day:', LTD)

                yesterday = todays_date - timedelta(days=1)
                yesterday = yesterday.date()
                print("yesterday_date", yesterday)

                first_month_value = first_month.strftime('01-%m-%Y')
                second_month_value = second_month.strftime('01-%m-%Y')

                first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
                second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

                First_Month_value = first_month.strftime("01-%b-%y")
                Second_Month_value = second_month.strftime("01-%b-%y")

                ## Last Trading Month

                Start_date_LTD = LTD.strftime("%Y-%m-01")
                Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
                Start_date_LTD = Start_date_LTD.date()

                month = LTD.month
                year = LTD.year
                first_date, num_days = calendar.monthrange(year, month)

                # End Date Trading Month
                End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
                End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

                # Last Business day before LTD

                offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                                n=1)  # change holiday list from singapore to real holiday list
                Day_before_LTD = LTD - offset_x

                from datetime import date
                today_format = date.today()

                start_date_value = start_date_value.date()
                Day_before_LTD = Day_before_LTD.date()
                End_Date_LTD = End_Date_LTD.date()

                print("LTD", LTD)
                print("Start_date_LTD:", Start_date_LTD)
                print("Day_before_LTD:", Day_before_LTD)
                print("End_Date_LTD:", End_Date_LTD)
                print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
                #
                #    # Total Days in Trading month
                Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                    holidays=holiday_list))  # change holiday list from singapore to real holiday list
                # Number of trading Days before LTD
                No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
                # Number of trading Days after LTD
                No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

                First_Month_Days_value = No_days_BF_LTD
                Second_Month_Days_value = No_days_AF_LTD

                print("Total_days_LTD NEW", Total_days_LTD)
                print("No_days_BF_LTD", No_days_BF_LTD)
                print("No_days_AF_LTD", No_days_AF_LTD)
                print("First_Month_Days_value:", First_Month_Days_value)
                print("Second_Month_Days_value:", Second_Month_Days_value)

                # try:
                #
                #     first_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
                #     second_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
                #
                #     First_Month_Settle_Price_value = first_month_price_value
                #     Second_Month_Price_value = second_month_price_value
                #
                # except:
                #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
                #     raise

                if (today_format <= start_date_value):
                    print('first')

                    # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                    #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                    # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                    priced_days_BF_LTD = 0
                    unpriced_days_BF_LTD = No_days_BF_LTD
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD


                elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                    print('second')
                    priced_days_BF_LTD = len(
                        pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                    #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                    #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                    #
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


                elif (today_format == LTD):

                    print('3rd')
                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

                elif today_format > LTD and today_format <= End_Date_LTD:
                    print('4rth')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_AF_LTD = len(
                        pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[
                    #     settlement_prices_df["Date"].isin(
                    #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                    #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round(
                    #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                    #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


                elif today_format > End_Date_LTD:
                    print('5th')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = No_days_AF_LTD
                    unpriced_days_AF_LTD = 0

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)

                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                    #                                  3)

                First_Month_value = first_month.strftime("%d-%b-%y")
                Second_Month_value = second_month.strftime("%d-%b-%y")

                print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                      priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

                futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                       3)
                futures_equivalent_second_Month = round(
                    ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

                Futures_equivalent_First_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
                Futures_equivalent_Second_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

                print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                      'futures_equivalent_second_Month')
                print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                      'Futures_equivalent_Second_kbbl')


            else:

                futures_equivalent_first_Month = 0.0
                futures_equivalent_second_Month = 0.0
                Futures_equivalent_First_kbbl = 0.0
                Futures_equivalent_Second_kbbl = 0.0
                first_month = start_date
                second_month = end_date
                First_Month_value = ''
                Second_Month_value = ''
                First_Month_Days_value = 0
                Second_Month_Days_value = 0
            print('if contract2', contract2)

            if diff_contracts == (contract2):

                print('its Contract2', contract2, volume, 'volume')
                volume = -(volume) if float(volume) > 0 else abs(volume)
                priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
                un_priced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
                total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)

                bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
                kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                    kbbl_mt_conversion)

                unpriced_kbbl_mt = round(-(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt),
                                         3)

                futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                    futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)

                futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                    futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)

                Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                    Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

                Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                    Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            print('Second_Contract', volume, 'volume', priced_volume, 'priced_volume', 'un_priced_volume',
                  un_priced_volume, 'total_volume', total_volume)
            print('bbl_mt_conversion', bbl_mt_conversion, 'kbbl_mt_conversion', kbbl_mt_conversion, 'unpriced_kbbl_mt',
                  'unpriced_kbbl_mt',
                  futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', 'Futures_equivalent_Second_kbbl',
                  Futures_equivalent_Second_kbbl)

            diff_single_value = str('Diff') + '-' + 'Sub'

            print(date_value, 'date_value')

            print("total_days:",total_swap_days)

            new_total_days= int(total_swap_days)

            print("new_total_days:",new_total_days)



            diff_obj = SwapBlotterModel(date=date_value,Trade_id=trade_id, trader_id=trader, clearer=clearer,
                                        tick=Ticks_value,
                                        unit=swaps_contract_unit,
                                        singl_dif=diff_single_value,
                                        mini_major=Major_Mini_value,
                                        mini_major_connection=Mini_Conn_Contract_value,
                                        bbi_mt_conversion=conversion_value,
                                        block_fee=swaps_block_fee_value,
                                        screen_fee=swaps_screen_fee_value,
                                        bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                                        book=book, customer_account=company_account,
                                        strategy_id=strategy, derivatives=derivatives,
                                        volume=volume, customer_company=customer_company,
                                        contract=swaps_contract_value, start_date=start_date,
                                        end_date=end_date, price=price, approx_ep=approximate_ep,
                                        holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                        notes=notes, trader_type=bileteral_external, buy_sell='test',
                                        fw_months=FW_Month,physical_code=physical_code,
                                        priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                                        priced_volume=priced_volume, unpriced_volume=un_priced_volume, unpriced_kbbl_mt=unpriced_kbbl_mt,
                                        First_month=first_month,Second_month=second_month,
                                        first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                                        futures_equiv_first=futures_equivalent_first_Month,futures_equiv_second=futures_equivalent_second_Month,
                                        futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl,total_days=total_swap_days,total_n_days=new_total_days)
            diff_obj.save()
            print('++dd++')
            print("total_days:", total_swap_days)
            diff_obj.duplicate_id = diff_id
            diff_obj.save()
            messages.info(request, 'Saved')
            print('diff save')
        # print("Executuion stopped")
        # sys.exit("error message")
        # print("total_days:", total_swap_days)

    def get(self, request,*args,**kwargs):

        obj = SwapBlotterModel.objects.get(id=kwargs['id'])
        book = Book.objects.all()
        clearer = ClearearM.objects.values_list('name', flat=True).distinct()
        trader = Traders.objects.all()
        book = Book.objects.all()
        customer_company = CompanyInvestmentModel.objects.all()
        strategy = Strategy.objects.all()
        derivatives = DerivativeM.objects.all()
        type = TYPEMODEL.objects.all()

        today = date.today()
        print("first today:", today)
        search_query = request.GET.get('search_query')
        print("search_query",search_query)

        if search_query:
            data1 = SwapBlotterModel.objects.filter(Q(customer_company__istartswith=search_query)|Q(trader__name__istartswith=search_query)
                                                    |Q(customer_account__istartswith=search_query)|Q(broker__istartswith=search_query)|Q(efs_code__istartswith=search_query)|Q(contract__istartswith=search_query)

                                                    | Q(clearer__istartswith=search_query) | Q(strategy__name__istartswith=search_query) | Q(volume__istartswith=search_query) | Q(holiday__istartswith=search_query)

                                                    | Q(type__istartswith=search_query) | Q(notes__istartswith=search_query) | Q(Trade_id__istartswith=search_query) | Q(   tick__istartswith=search_query)


                                                    )
        else:

            data1 = SwapBlotterModel.objects.all()

        paginator = Paginator(data1,25)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        context = {'book': book, 'clearer': clearer, 'trader': trader,
                   'customer_company': customer_company, 'strategy': strategy, 'derivatives': derivatives,
                   'type': type, 'page_obj': data,"d":obj}
        return render(request, "customer/swapsblotter_copy.html", context)

    def post(self, request,*args,**kwargs):

        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        print(bileteral_external,'bileteral_external')
        clearer = request.POST.get('clearer', '')  # id
        print(clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        company_account = request.POST.get('company_account', '')
        strategy = request.POST.get('strategy', '')  # id
        derivatives = request.POST.get('derivatives', '')
        volume = request.POST.get('volume', '')
        volume = float(volume)
        customer_company = request.POST.get('customer_company', '')
        buy_sell = request.POST.get('buy_sell', '')
        contract_name = request.POST.get('contract_name', '')
        print("contract_name:",contract_name)
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        type = request.POST.get('type', '')
        pb_id = request.POST.get('pb_id', '')
        print("pb_id",pb_id)
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        print(" get brocker",brocker)

        notes = request.POST.get('notes', '')
        book = request.POST.get('book', '')

        unit_c = request.POST.get('unit_c', '')
        tick_c = request.POST.get('tick_c', '')


        delete_feild = request.POST.get('delete_feild')

        randint_ = str(random.randint(1000, 99999))

        if bileteral_external == "External":
            trade_id = "EXT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)
        elif bileteral_external == "Bilateral":
            trade_id = "BLT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)

        c = ContractM.objects.filter(contract_name=contract_name)[0]
        tick = c.tick
        print(tick, 'tick')
        tick = float(tick)
        unit = c.unit
        print("unit:",unit)


        singl_dif = c.single_dif
        print("singl_dif:",singl_dif)
        mini_major = c.major_mini
        print("mini_major:", mini_major)
        mini_major_connection = c.major_mini_conn
        print("mini_major_connection:", mini_major_connection)
        physical_code = c.physical_code
        print("physical_code:", physical_code)
        logical_code = c.logical_code
        print("logical_code:", logical_code)
        symbol_code = c.symbol_code
        print("symbol_code:", symbol_code)

        block_fee = c.block_fee
        print("block_fee:", block_fee)

        screen_fee = c.screen_fee
        print("screen_fee:", screen_fee)

        screen_fee = float(str(screen_fee))
        print("screen_fee2:", screen_fee)


        bbl_mt = c.bbi_mt_conversion
        print("bbl_mt:", bbl_mt)


        bbl_mt = float(str(bbl_mt))
        print("bbl_mt:", bbl_mt)


        FW_Month = c.f_w_months
        print("FW_Month:", FW_Month)

        if FW_Month == '':
            FW_Month = 0
        else:
            FW_Month = int(FW_Month)
            print("FW_Month:", FW_Month)


        print(block_fee, 'block_fee', screen_fee, 'screen_fee', FW_Month)

        try:
            second_FW_Month = FW_Month + 1
        except:
            FW_Month = 0
            second_FW_Month = 0

        try:

            if brocker == 'Ice Block':

                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = 0.0
                brokerage = 0.0

            elif brocker == 'Ice Screen':
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = round((float(screen_fee) * float(volume)), 3)
                brokerage = 0.0

            else:

                swaps_screen_fee_value = 0.0
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                brokerage = 0.0

        except:
            print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            raise

        swaps_screen_fee_value = round(-(abs(swaps_screen_fee_value)), 3)
        swaps_block_fee_value = round(-(abs(swaps_block_fee_value)), 3)
        # total_fees = float(clearer_rate_calc) + float(brokerage) + float(swaps_screen_fee_value) + float(
        #     swaps_block_fee_value)

        total_fees = float(brokerage) + float(swaps_screen_fee_value) + float(
            swaps_block_fee_value)
        total_fees = round(total_fees, 3)

        print("testingbileteral_external:",bileteral_external)

        if bileteral_external == 'Bilateral':
            # clearer_rate_calc = 0.0
            swaps_block_fee_value = 0.0
            swaps_screen_fee_value = 0.0
            brokerage = 0.0

        from datetime import date
        todays_date = date.today()
        start_date_value = start_date
        end_date_value = end_date
        # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
        # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

        holiday_list = []
        holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        for i in holiday_check:
            holiday_list.append(i)

        print(holiday_list, 'holiday_list')

        holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
        print(total_swap_days, 'total_swap_days')

        today = todays_date.strftime("%d-%b-%y")
        todays_date = datetime.strptime(today, "%d-%b-%y")
        end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
        start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
        print(todays_date)
        print(start_date_value, 'start_date_value')
        print(end_date_value, 'end_date_value')

        # *******************Priced ,Unpriced Days*************************************************************************************************
        if todays_date <= start_date_value:

            unpriced_days = total_swap_days
            priced_days = 0

        elif (todays_date > start_date_value) and (todays_date <= end_date_value):

            unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
            priced_days = int(total_swap_days) - unpriced_days


        elif todays_date > end_date_value:
            unpriced_days = 0
            priced_days = int(total_swap_days)


        priced_volume = round(((priced_days / total_swap_days) * volume), 3)
        un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
        total_volume = round((priced_volume + un_priced_volume), 3)

        bbl_mt_conversion = round(float(bbl_mt) * float(volume) * float(tick), 3)
        kbbl_mt_conversion = round(
            ((float(bbl_mt) * float(volume) * float(tick)) / 1000), 3)
        unpriced_kbbl_mt = round(
            ((float(bbl_mt) * float(un_priced_volume) * float(tick)) / 1000),
            3)

        first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
        first_month = first_month.strftime('01-%m-%Y')
        first_month = datetime.strptime(first_month, '%d-%m-%Y')
        first_month = first_month.date()
        print(first_month, 'first_month')

        second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
        second_month = second_month.strftime('01-%m-%Y')
        second_month = datetime.strptime(second_month, '%d-%m-%Y')
        second_month = second_month.date()
        print(second_month, 'second_month')

        # Last Traded Date Starting***************************************#
        if contract_name == 'RBOB 1st Line':
            print("contract_name_str,", contract_name)
            print("hello loop")
            filter_column = 'RBOB_Gasoline_futures'
        elif (contract_name == 'LS GO 1st Line') or (contract_name == 'LS GO 1st Line Mini'):
            filter_column = 'Ls_gas_oil'
        elif (contract_name == 'Brent 1st Line') or (contract_name == 'Brent 1st Line Mini'):
            filter_column = 'Brent_crude_futures'

        elif contract_name == 'WTI Crude Futures':
            filter_column = 'WTI_crude_futures'

        else:
            filter_column = contract_name
            print("Not matching company NAMEE")

        future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                       'Heating_oil_futures', 'WTI_crude_futures']

        if filter_column in future_ltd_column_name_list:

            try:
                contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

            except:
                print('Error,LTD Not present in Admin side')

            for sub in contract_date_value:
                LTD = sub[filter_column]
                # LTD = datetime.strptime(LTD,'%d-%m-%Y')

            print('Last MAin Traded Day:', LTD)

            yesterday = todays_date - timedelta(days=1)
            yesterday = yesterday.date()
            print("yesterday_date", yesterday)

            first_month_value = first_month.strftime('01-%m-%Y')
            second_month_value = second_month.strftime('01-%m-%Y')

            first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
            second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

            First_Month_value = first_month.strftime("01-%b-%y")
            Second_Month_value = second_month.strftime("01-%b-%y")

            ## Last Trading Month

            Start_date_LTD = LTD.strftime("%Y-%m-01")
            Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
            Start_date_LTD = Start_date_LTD.date()

            month = LTD.month
            year = LTD.year
            first_date, num_days = calendar.monthrange(year, month)

            # End Date Trading Month
            End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
            End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

            # Last Business day before LTD

            offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                            n=1)  # change holiday list from singapore to real holiday list
            Day_before_LTD = LTD - offset_x

            from datetime import date
            today_format = date.today()

            start_date_value = start_date_value.date()
            Day_before_LTD = Day_before_LTD.date()
            End_Date_LTD = End_Date_LTD.date()

            print("LTD", LTD)
            print("Start_date_LTD:", Start_date_LTD)
            print("Day_before_LTD:", Day_before_LTD)
            print("End_Date_LTD:", End_Date_LTD)
            print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
            #
            #    # Total Days in Trading month
            Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                holidays=holiday_list))  # change holiday list from singapore to real holiday list
            # Number of trading Days before LTD
            No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
            # Number of trading Days after LTD
            No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

            First_Month_Days_value = No_days_BF_LTD
            Second_Month_Days_value = No_days_AF_LTD

            print("Total_days_LTD NEW", Total_days_LTD)
            print("No_days_BF_LTD", No_days_BF_LTD)
            print("No_days_AF_LTD", No_days_AF_LTD)
            print("First_Month_Days_value:", First_Month_Days_value)
            print("Second_Month_Days_value:", Second_Month_Days_value)

            # try:
            #
            #     first_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
            #     second_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
            #
            #     First_Month_Settle_Price_value = first_month_price_value
            #     Second_Month_Price_value = second_month_price_value
            #
            # except:
            #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
            #     raise

            if (today_format <= start_date_value):
                print('first')

                # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                priced_days_BF_LTD = 0
                unpriced_days_BF_LTD = No_days_BF_LTD
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD


            elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                print('second')
                priced_days_BF_LTD = len(
                    pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                #
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


            elif (today_format == LTD):

                print('3rd')
                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

            elif today_format > LTD and today_format <= End_Date_LTD:
                print('4rth')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_AF_LTD = len(pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[
                #     settlement_prices_df["Date"].isin(
                #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round(
                #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


            elif today_format > End_Date_LTD:
                print('5th')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = No_days_AF_LTD
                unpriced_days_AF_LTD = 0

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)

                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                #                                  3)

            First_Month_value = first_month.strftime("%d-%b-%y")
            Second_Month_value = second_month.strftime("%d-%b-%y")

            print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                  priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

            futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                   3)
            futures_equivalent_second_Month = round(
                ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

            Futures_equivalent_First_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
            Futures_equivalent_Second_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

            print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                  'Futures_equivalent_Second_kbbl')


        else:

            futures_equivalent_first_Month = 0.0
            futures_equivalent_second_Month = 0.0
            Futures_equivalent_First_kbbl = 0.0
            Futures_equivalent_Second_kbbl = 0.0
            first_month = start_date
            second_month = end_date
            First_Month_Days_value = 0
            Second_Month_Days_value = 0.0
            First_Month_value = ''
            Second_Month_value = ''

        print('ManinTrade')
        print("Physical code:",physical_code)
        date = request.POST.get('date', '')



        print("datasave")

        print("brocker to save:",brocker)


        obj = SwapBlotterModel(date=date, Trade_id=trade_id, trader_type=bileteral_external,clearer=clearer, trader_id=trader,
                               book=book, customer_account=company_account,
                               strategy_id=strategy, derivatives=derivatives,
                               volume=volume, customer_company=customer_company,
                               contract=contract_name, start_date=start_date,
                               end_date=end_date, price=price, approx_ep=approximate_ep,
                               holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                               tick=tick,unit=unit,singl_dif=singl_dif,mini_major=c.major_mini,
                               mini_major_connection=c.major_mini_conn,
                               bbi_mt_conversion=bbl_mt,
                               block_fee=block_fee,physica_blotter_connect=pb_id,
                               screen_fee=screen_fee,fw_months=FW_Month,physical_code=physical_code,
                               bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                               notes=notes, buy_sell=buy_sell,
                               total_days=total_swap_days,
                               priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                               priced_volume=priced_volume,unpriced_volume=un_priced_volume, unpriced_kbbl_mt=unpriced_kbbl_mt,
                               First_month=first_month,Second_month=second_month,
                               first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                               futures_equiv_first=futures_equivalent_first_Month,futures_equiv_second=futures_equivalent_second_Month,
                               futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl)
        obj.save()
        obj.duplicate_id = obj.id
        obj.save()
        messages.info(request, 'Saved')


        diff_id = obj.id
        print(
            '++++++++++++++++++++first save from form++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        if  (bileteral_external == 'External') and singl_dif != 'diff':
            return HttpResponseRedirect('/swaps-blotter')


        print("secondif")

        if singl_dif == 'diff':
            diff_result = self.diff_contract(request, date, bileteral_external, clearer, trader, book, customer_company,
                                             company_account, strategy, derivatives, volume, contract_name,
                                             start_date, end_date, price, approximate_ep, holiday, type, efs_code,
                                             brocker, diff_id, unit, tick, notes,trade_id)
            print(diff_result, '++++++++dIff Call')

            print("3rd if")

        if bileteral_external == 'Bilateral':
            print('bilateral')

            print("4th if")

            volume = -(volume) if float(volume) > 0 else abs(volume)
            int_priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
            int_unpriced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
            int_total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)
            int_bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
            int_kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                kbbl_mt_conversion)
            int_unpriced_kbbl_mt = -(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt)
            int_unpriced_kbbl_mt = round(int_unpriced_kbbl_mt, 3)

            int_futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)
            int_futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)
            int_Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

            int_Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            int_clearing_rate = 0.0

            int_brokerage = 0.0
            int_screen_fee = 0.0
            int_block_fee = 0.0
            int_total_fee = 0.0


            print("save copy")

            obj1 = SwapBlotterModel(date=date, Trade_id=trade_id,clearer=clearer, trader_id=trader,
                                    tick=c.tick,
                                    unit=c.unit,
                                    singl_dif=c.single_dif,
                                    mini_major=c.major_mini,
                                    mini_major_connection=c.major_mini_conn,
                                    bbi_mt_conversion=c.bbi_mt_conversion,
                                    block_fee=c.block_fee,
                                    screen_fee=c.screen_fee,fw_months=FW_Month,
                                    bbi_mt=int_bbl_mt_conversion, kbbl_mt_conversion=int_kbbl_mt_conversion,
                                    book=customer_company, customer_account=company_account,
                                    strategy_id=strategy, derivatives=derivatives,physica_blotter_connect=pb_id,
                                    volume=volume, customer_company=book,physical_code=physical_code,
                                    contract=contract_name, start_date=start_date,
                                    end_date=end_date, price=price, approx_ep=approximate_ep,
                                    holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                    notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
                                    buy_sell=buy_sell, total_days=total_swap_days,
                                    priced_days=priced_days, unpriced_days=unpriced_days, total_volume=int_total_volume,
                                    priced_volume=int_priced_volume, unpriced_volume=int_unpriced_volume, unpriced_kbbl_mt=int_unpriced_kbbl_mt,
                                    First_month=first_month,Second_month=second_month,
                                    first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                                    futures_equiv_first=int_futures_equivalent_first_Month,futures_equiv_second=int_futures_equivalent_second_Month,
                                    futures_equiv_first_kbbl=int_Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=int_Futures_equivalent_Second_kbbl)
            obj1.save()
            obj.duplicate_id = diff_id
            obj.save()

            if (c.single_dif == 'diff') and (bileteral_external == 'Bilateral'):
                diff_result_bilat = self.diff_contract(request, date, bileteral_external, clearer, trader,
                                                       customer_company,
                                                       book, company_account, strategy, derivatives, volume,
                                                       contract_name,
                                                       start_date, end_date, price, approximate_ep, holiday, type,
                                                       efs_code,
                                                       brocker, diff_id, unit, tick, notes,trade_id)

                print(diff_result_bilat)

        print('first return')

        # update_database(request)

        messages.info(request, 'Saved')
        return HttpResponseRedirect('/swaps-blotter')


###########################################################                       swaps details view                      #####################################################################################

class SwapsBlotterDetailsView(View):
    def get(self,request,*args,**kwargs):
        # print(kwargs)
        qs = SwapBlotterModel.objects.get(id=kwargs['id'])
        return render(request,"customer/sb-details.html",{"fb":qs})



################################################################     end of copy swap blotter   ####################################################################################################


class EditSwapsBlotter(View):

    def diff_contract(self, request, *data):

        date_value = data[0]
        bileteral_external = data[1]
        clearer = data[2]
        trader = data[3]
        book = data[4]
        customer_company = data[5]
        company_account = data[6]
        strategy = data[7]
        derivatives = data[8]
        volume = data[9]
        volume = float(volume)
        contract_name = data[10]
        start_date = data[11]
        end_date = data[12]
        price = data[13]
        price = float(price)
        approximate_ep = data[14]
        holiday = data[15]
        type = data[16]
        efs_code = data[17]
        brocker = data[18]
        diff_id = data[19]
        diff_unit_value = data[20]
        tick = data[21]
        notes = data[22]
        trade_id = data[23]

        # delete_feild =data[22]

        contract_list = []
        count = 0
        c = ContractM.objects.filter(contract_name=contract_name)[0]
        diff_contract_tick = tick

        contract1 = ContractM.objects.filter(contract_name=c.contract1)[0]
        sub_contract1_tick = contract1.tick
        sub_contract1_unit = contract1.unit
        sub_contract1_conversion = contract1.bbi_mt_conversion
        contract_list.append(contract1)

        contract2 = ContractM.objects.filter(contract_name=c.contract2)[0]
        sub_contract2_tick = contract2.tick
        sub_contract2_unit = contract2.unit
        sub_contract2_conversion = contract2.bbi_mt_conversion
        contract_list.append(contract2)

        sub_conv_bbl_mt = {sub_contract1_unit: sub_contract1_conversion, sub_contract2_unit: sub_contract2_conversion}
        contract_tick = {sub_contract1_unit: sub_contract1_tick, sub_contract2_unit: sub_contract2_tick}

        print(sub_conv_bbl_mt, contract_tick, '++++++++Tick,Conversion')

        print("contract_list", contract_list)

        for diff_contracts in contract_list:

            print("diff_contracts:", diff_contracts)

            count = count + 1
            swaps_contract_value = diff_contracts.contract_name
            swaps_contract_unit = diff_contracts.unit
            swaps_ticks_val = diff_contracts.tick

            swaps_screen_fee_val = diff_contracts.screen_fee
            swaps_block_fee_val = diff_contracts.block_fee
            conversion_value = diff_contracts.bbi_mt_conversion
            conversion_value_bbl_mt = diff_contracts.bbi_mt_conversion
            FW_Month = diff_contracts.f_w_months
            diff_single_value = diff_contracts.single_dif
            Major_Mini_value = diff_contracts.major_mini
            Mini_Conn_Contract_value = diff_contracts.major_mini_conn
            physical_code = diff_contracts.physical_code
            logical_code = diff_contracts.logical_code
            symbol_code = diff_contracts.symbol_code

            swaps_ticks_val = float(swaps_ticks_val)
            swaps_screen_fee_val = float(swaps_screen_fee_val)
            swaps_block_fee_val = float(swaps_block_fee_val)
            conversion_value = float(conversion_value)
            conversion_value_bbl_mt = float(conversion_value_bbl_mt)

            print("fw", FW_Month)

            if FW_Month == '':
                FW_Month = 0
            else:
                FW_Month = int(FW_Month)

            print(swaps_contract_value, 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            if diff_unit_value == 'MT':

                if sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                    conversion_value = float(conversion_value)
                    swaps_ticks_val = float(diff_contract_tick)

                    print('mt mt mt', conversion_value, swaps_ticks_val)

                elif sub_contract1_unit != sub_contract2_unit:

                    if swaps_contract_unit == 'bbl':

                        conversion_value = sub_conv_bbl_mt['MT']
                        conversion_value = float(conversion_value)
                        swaps_ticks_val = contract_tick['MT']
                    else:

                        conversion_value = conversion_value

                elif sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':
                    conversion_value = float(conversion_value)

            else:

                if diff_unit_value == 'bbl':

                    if sub_contract1_unit == 'bbl' and sub_contract2_unit == 'bbl':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

                    elif sub_contract1_unit != sub_contract2_unit:

                        if swaps_contract_unit == 'MT':

                            conversion_value = float(1)
                            swaps_ticks_val = contract_tick['bbl']

                        else:

                            conversion_value = float(1)

                    elif sub_contract1_unit == 'MT' and sub_contract2_unit == 'MT':

                        conversion_value = float(1)
                        swaps_ticks_val = float(diff_contract_tick)

            if (data[15] == 'non-common'):

                holiday = diff_contracts.holiday
            else:
                holiday = data[15]
            print(holiday, 'Working Till Here')

            try:
                second_FW_Month = int(FW_Month) + 1
            except:
                FW_Month = 0
                second_FW_Month = 0

            try:

                if brocker == 'Ice Block':

                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = 0.0
                    brokerage = 0.0

                elif brocker == 'Ice Screen':
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    swaps_screen_fee_value = round((float(swaps_screen_fee_val) * float(volume)), 3)
                    brokerage = 0.0

                else:

                    swaps_screen_fee_value = 0.0
                    swaps_block_fee_value = round((float(swaps_block_fee_val) * float(volume)), 3)
                    brokerage = 0.0

            except:
                print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
                raise

            print(swaps_block_fee_value, 'swaps_block_fee_value', 'swaps_block_fee_value', swaps_block_fee_value,
                  'brokerage', brokerage)

            from datetime import date
            todays_date = date.today()
            start_date_value = start_date
            end_date_value = end_date
            # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
            # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

            holiday_list = []
            holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
            for i in holiday_check:
                holiday_list.append(i)

            print(holiday_list, 'holiday_list')

            holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
            holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
            holiday_list = holiday_date_df['Dates'].to_list()
            total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
            print(total_swap_days, 'total_swap_days')

            today = todays_date.strftime("%d-%b-%y")
            todays_date = datetime.strptime(today, "%d-%b-%y")
            end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
            start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
            print(todays_date)
            print(start_date_value, 'start_date_value')
            print(end_date_value, 'end_date_value')

            # *******************Priced ,Unpriced Days*************************************************************************************************
            if todays_date <= start_date_value:

                unpriced_days = total_swap_days
                priced_days = 0

            elif (todays_date > start_date_value) and (todays_date <= end_date_value):

                unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
                priced_days = int(total_swap_days) - unpriced_days


            elif todays_date > end_date_value:
                unpriced_days = 0
                priced_days = int(total_swap_days)

            priced_volume = round(((priced_days / total_swap_days) * volume), 3)
            un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
            total_volume = round((priced_volume + un_priced_volume), 3)

            bbl_mt_conversion = round(float(conversion_value) * float(volume) * float(swaps_ticks_val), 3)
            kbbl_mt_conversion = round(
                ((float(conversion_value) * float(volume) * float(swaps_ticks_val)) / 1000), 3)
            unpriced_kbbl_mt = round(
                ((float(conversion_value) * float(un_priced_volume) * float(swaps_ticks_val)) / 1000),
                3)

            Ticks_value = swaps_ticks_val
            print(bbl_mt_conversion, 'bbl_mt_conversion', kbbl_mt_conversion, 'kbbl_mt_conversion', 'unpriced_kbbl_mt',
                  unpriced_kbbl_mt, Ticks_value, 'Ticks_value')

            print(FW_Month, 'FW_Month')
            print(second_FW_Month, 'second_FW_Month')

            first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
            first_month = first_month.strftime('01-%m-%Y')
            first_month = datetime.strptime(first_month, '%d-%m-%Y')
            first_month = first_month.date()
            print(first_month, 'first_month')

            second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
            second_month = second_month.strftime('01-%m-%Y')
            second_month = datetime.strptime(second_month, '%d-%m-%Y')
            second_month = second_month.date()
            print(second_month, 'second_month')

            print('swaps_contract_value', swaps_contract_value, first_month, 'first_monthworks', second_month,
                  'second_month', 'swaps_contract_value+++++++++++++++', FW_Month, 'FW_Month++++++')

            # Last Traded Date Starting***************************************#
            if swaps_contract_value == 'RBOB 1st Line':
                print("contract_name_str,", swaps_contract_value)
                print("hello loop")
                filter_column = 'RBOB_Gasoline_futures'
            elif (swaps_contract_value == 'LS GO 1st Line') or (swaps_contract_value == 'LS GO 1st Line Mini'):
                filter_column = 'Ls_gas_oil'
            elif (swaps_contract_value == 'Brent 1st Line') or (swaps_contract_value == 'Brent 1st Line Mini'):
                filter_column = 'Brent_crude_futures'

            elif swaps_contract_value == 'WTI Crude Futures':
                filter_column = 'WTI_crude_futures'

            else:
                filter_column = swaps_contract_value
                print("Not matching company NAMEE")

            future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                           'Heating_oil_futures', 'WTI_crude_futures']

            if filter_column in future_ltd_column_name_list:

                try:
                    contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

                except:
                    print('Error,LTD Not present in Admin side')

                for sub in contract_date_value:
                    LTD = sub[filter_column]
                    # LTD = datetime.strptime(LTD,'%d-%m-%Y')

                print('Last Traded Day:', LTD)

                yesterday = todays_date - timedelta(days=1)
                yesterday = yesterday.date()
                print("yesterday_date", yesterday)

                first_month_value = first_month.strftime('01-%m-%Y')
                second_month_value = second_month.strftime('01-%m-%Y')

                first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
                second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

                First_Month_value = first_month.strftime("01-%b-%y")
                Second_Month_value = second_month.strftime("01-%b-%y")

                ## Last Trading Month

                Start_date_LTD = LTD.strftime("%Y-%m-01")
                Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
                Start_date_LTD = Start_date_LTD.date()

                month = LTD.month
                year = LTD.year
                first_date, num_days = calendar.monthrange(year, month)

                # End Date Trading Month
                End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
                End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

                # Last Business day before LTD

                offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                                n=1)  # change holiday list from singapore to real holiday list
                Day_before_LTD = LTD - offset_x

                from datetime import date
                today_format = date.today()

                start_date_value = start_date_value.date()
                Day_before_LTD = Day_before_LTD.date()
                End_Date_LTD = End_Date_LTD.date()

                print("LTD", LTD)
                print("Start_date_LTD:", Start_date_LTD)
                print("Day_before_LTD:", Day_before_LTD)
                print("End_Date_LTD:", End_Date_LTD)
                print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
                #
                #    # Total Days in Trading month
                Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                    holidays=holiday_list))  # change holiday list from singapore to real holiday list
                # Number of trading Days before LTD
                No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
                # Number of trading Days after LTD
                No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

                First_Month_Days_value = No_days_BF_LTD
                Second_Month_Days_value = No_days_AF_LTD

                print("Total_days_LTD NEW", Total_days_LTD)
                print("No_days_BF_LTD", No_days_BF_LTD)
                print("No_days_AF_LTD", No_days_AF_LTD)
                print("First_Month_Days_value:", First_Month_Days_value)
                print("Second_Month_Days_value:", Second_Month_Days_value)

                # try:
                #
                #     first_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
                #     second_month_price_value = \
                #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
                #
                #     First_Month_Settle_Price_value = first_month_price_value
                #     Second_Month_Price_value = second_month_price_value
                #
                # except:
                #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
                #     raise

                if (today_format <= start_date_value):
                    print('first')

                    # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                    #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                    # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                    priced_days_BF_LTD = 0
                    unpriced_days_BF_LTD = No_days_BF_LTD
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD


                elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                    print('second')
                    priced_days_BF_LTD = len(
                        pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                    #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                    #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                    #
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


                elif (today_format == LTD):

                    print('3rd')
                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = 0
                    unpriced_days_AF_LTD = No_days_AF_LTD

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

                elif today_format > LTD and today_format <= End_Date_LTD:
                    print('4rth')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                    unpriced_days_AF_LTD = len(
                        pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[
                    #     settlement_prices_df["Date"].isin(
                    #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                    #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)
                    #
                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round(
                    #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                    #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


                elif today_format > End_Date_LTD:
                    print('5th')

                    priced_days_BF_LTD = No_days_BF_LTD
                    unpriced_days_BF_LTD = 0
                    priced_days_AF_LTD = No_days_AF_LTD
                    unpriced_days_AF_LTD = 0

                    # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                    # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                    #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                    # AF_LTD_priced_avg_settlement_price = round(
                    #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                    #
                    # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                    #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                    # MTM_value = round(MTM_Price, 3)

                    # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                    # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                    #                                  3)

                First_Month_value = first_month.strftime("%d-%b-%y")
                Second_Month_value = second_month.strftime("%d-%b-%y")

                print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                      priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

                futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                       3)
                futures_equivalent_second_Month = round(
                    ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

                Futures_equivalent_First_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
                Futures_equivalent_Second_kbbl = round(
                    ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

                print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                      'futures_equivalent_second_Month')
                print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                      'Futures_equivalent_Second_kbbl')


            else:

                futures_equivalent_first_Month = 0.0
                futures_equivalent_second_Month = 0.0
                Futures_equivalent_First_kbbl = 0.0
                Futures_equivalent_Second_kbbl = 0.0
                first_month = start_date
                second_month = end_date
                First_Month_value = ''
                Second_Month_value = ''
                First_Month_Days_value = 0
                Second_Month_Days_value = 0
            print('if contract2', contract2)

            if diff_contracts == (contract2):
                print('its Contract2', contract2, volume, 'volume')
                volume = -(volume) if float(volume) > 0 else abs(volume)
                priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
                un_priced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
                total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)

                bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
                kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                    kbbl_mt_conversion)

                unpriced_kbbl_mt = round(-(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt),
                                         3)

                futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                    futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)

                futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                    futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)

                Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                    Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

                Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                    Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            print('Second_Contract', volume, 'volume', priced_volume, 'priced_volume', 'un_priced_volume',
                  un_priced_volume, 'total_volume', total_volume)
            print('bbl_mt_conversion', bbl_mt_conversion, 'kbbl_mt_conversion', kbbl_mt_conversion, 'unpriced_kbbl_mt',
                  'unpriced_kbbl_mt',
                  futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', 'Futures_equivalent_Second_kbbl',
                  Futures_equivalent_Second_kbbl)

            diff_single_value = str('Diff') + '-' + 'Sub'

            print(date_value, 'date_value')

            print("total_days:", total_swap_days)

            new_total_days = int(total_swap_days)

            print("new_total_days:", new_total_days)

            diff_obj = SwapBlotterModel(date=date_value, Trade_id=trade_id, trader_id=trader, clearer=clearer,
                                        tick=Ticks_value,
                                        unit=swaps_contract_unit,
                                        singl_dif=diff_single_value,
                                        mini_major=Major_Mini_value,
                                        mini_major_connection=Mini_Conn_Contract_value,
                                        bbi_mt_conversion=conversion_value,
                                        block_fee=swaps_block_fee_value,
                                        screen_fee=swaps_screen_fee_value,
                                        bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                                        book=book, customer_account=company_account,
                                        strategy_id=strategy, derivatives=derivatives,
                                        volume=volume, customer_company=customer_company,
                                        contract=swaps_contract_value, start_date=start_date,
                                        end_date=end_date, price=price, approx_ep=approximate_ep,
                                        holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                        notes=notes, trader_type=bileteral_external, buy_sell='test',
                                        fw_months=FW_Month, physical_code=physical_code,
                                        priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                                        priced_volume=priced_volume, unpriced_volume=un_priced_volume,
                                        unpriced_kbbl_mt=unpriced_kbbl_mt,
                                        First_month=first_month, Second_month=second_month,
                                        first_month_days=First_Month_Days_value,
                                        second_month_days=Second_Month_Days_value,
                                        futures_equiv_first=futures_equivalent_first_Month,
                                        futures_equiv_second=futures_equivalent_second_Month,
                                        futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,
                                        futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl,
                                        total_days=total_swap_days, total_n_days=new_total_days)
            diff_obj.save()
            print('++dd++')
            print("total_days:", total_swap_days)
            diff_obj.duplicate_id = diff_id
            diff_obj.save()
            messages.info(request, 'Saved')
            print('diff save')
        # print("Executuion stopped")
        # sys.exit("error message")
        # print("total_days:", total_swap_days)

    def get(self,request,**kwargs):
            obj = SwapBlotterModel.objects.get(id=kwargs['id'])
            book = Book.objects.all()
            print("b4:",obj.bileteral_external)
            clearer = ClearearM.objects.values_list('name',flat=True).distinct()
            trader = Traders.objects.all()
            book = Book.objects.all()
            customer_company = CompanyInvestmentModel.objects.all()
            strategy = Strategy.objects.all()
            derivatives = DerivativeM.objects.all()
            type = TYPEMODEL.objects.all()
            data = SwapBlotterModel.objects.all()
            context = {'book':book,'clearer':clearer, 'trader':trader,
                      'customer_company':customer_company, 'strategy':strategy,'derivatives':derivatives,
                      'type':type,'object_list':data,'d':obj}
            return render(request,'backend/edit-swaps-blotter.html',context)

            # return render(request, 'customer/swap-edit2.html', context)

    def post(self, request,*args,**kwargs):

        obj = SwapBlotterModel.objects.get(id=kwargs['id'])

        if obj.duplicate_id == 'none':
            obj.delete()
        else:

            obj = SwapBlotterModel.objects.get(id=kwargs['id'])
            print(obj)
            print('dddddddddddddddddddd')
            obj2 = SwapBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = SwapBlotterModel.objects.get(id=i.id)
                obj1.delete()

        date = request.POST.get('date', '')
        bileteral_external = request.POST.get('bileteral_external', '')
        print(bileteral_external,'bileteral_external')
        clearer = request.POST.get('clearer', '')  # id
        print(clearer)
        trader = request.POST.get('trader', '')  # id
        book = request.POST.get('book', '')
        company_account = request.POST.get('company_account', '')
        strategy = request.POST.get('strategy', '')  # id
        derivatives = request.POST.get('derivatives', '')
        volume = request.POST.get('volume', '')
        volume = float(volume)
        customer_company = request.POST.get('customer_company', '')
        buy_sell = request.POST.get('buy_sell', '')
        contract_name = request.POST.get('contract_name', '')
        print("contract_name:",contract_name)
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        price = request.POST.get('price', '')
        approximate_ep = request.POST.get('approximate_ep', '')
        holiday = request.POST.get('holiday', '')
        type = request.POST.get('type', '')
        pb_id = request.POST.get('pb_id', '')
        print("pb_id",pb_id)
        efs_code = request.POST.get('efs_code', '')
        brocker = request.POST.get('brocker', '')
        notes = request.POST.get('notes', '')
        book = request.POST.get('book', '')

        unit_c = request.POST.get('unit_c', '')
        tick_c = request.POST.get('tick_c', '')


        delete_feild = request.POST.get('delete_feild')

        randint_ = str(random.randint(1000, 99999))

        if bileteral_external == "External":
            trade_id = "EXT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)
        elif bileteral_external == "Bilateral":
            trade_id = "BLT" + "-" + "S" + "-" + randint_
            print("trade_id swap ex:", trade_id)


        print("trade idddddd:",trade_id)

        c = ContractM.objects.filter(contract_name=contract_name)[0]
        tick = c.tick
        print(tick, 'tick')
        tick = float(tick)
        unit = c.unit
        print("unit:",unit)


        singl_dif = c.single_dif
        print("singl_dif:",singl_dif)
        mini_major = c.major_mini
        print("mini_major:", mini_major)
        mini_major_connection = c.major_mini_conn
        print("mini_major_connection:", mini_major_connection)
        physical_code = c.physical_code
        print("physical_code:", physical_code)
        logical_code = c.logical_code
        print("logical_code:", logical_code)
        symbol_code = c.symbol_code
        print("symbol_code:", symbol_code)

        block_fee = c.block_fee
        print("block_fee:", block_fee)

        screen_fee = c.screen_fee
        print("screen_fee:", screen_fee)

        screen_fee = float(str(screen_fee))
        print("screen_fee2:", screen_fee)


        bbl_mt = c.bbi_mt_conversion
        print("bbl_mt:", bbl_mt)


        bbl_mt = float(str(bbl_mt))
        print("bbl_mt:", bbl_mt)


        FW_Month = c.f_w_months
        print("FW_Month:", FW_Month)

        if FW_Month == '':
            FW_Month = 0
        else:
            FW_Month = int(FW_Month)
            print("FW_Month:", FW_Month)


        print(block_fee, 'block_fee', screen_fee, 'screen_fee', FW_Month)

        try:
            second_FW_Month = FW_Month + 1
        except:
            FW_Month = 0
            second_FW_Month = 0

        try:

            if brocker == 'Ice Block':

                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = 0.0
                brokerage = 0.0

            elif brocker == 'Ice Screen':
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                swaps_screen_fee_value = round((float(screen_fee) * float(volume)), 3)
                brokerage = 0.0

            else:

                swaps_screen_fee_value = 0.0
                swaps_block_fee_value = round((float(block_fee) * float(volume)), 3)
                brokerage = 0.0

        except:
            print("error", 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            messages.error(request, 'Screen Fee/ Block Fee/Brokerage given in admin side invalid/Non-Numeric')
            raise

        swaps_screen_fee_value = round(-(abs(swaps_screen_fee_value)), 3)
        swaps_block_fee_value = round(-(abs(swaps_block_fee_value)), 3)
        # total_fees = float(clearer_rate_calc) + float(brokerage) + float(swaps_screen_fee_value) + float(
        #     swaps_block_fee_value)

        total_fees = float(brokerage) + float(swaps_screen_fee_value) + float(
            swaps_block_fee_value)
        total_fees = round(total_fees, 3)

        print("testingbileteral_external:",bileteral_external)

        if bileteral_external == 'Bilateral':
            # clearer_rate_calc = 0.0
            swaps_block_fee_value = 0.0
            swaps_screen_fee_value = 0.0
            brokerage = 0.0

        from datetime import date
        todays_date = date.today()
        start_date_value = start_date
        end_date_value = end_date
        # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # print('date_type',type(todays_date),type(start_date_value),type(end_date_value))
        # todays_date = datetime.strptime(today, "%Y-%m-%d").date()

        holiday_list = []
        holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        for i in holiday_check:
            holiday_list.append(i)

        print(holiday_list, 'holiday_list')

        holiday_date_df = pd.DataFrame(holiday_list, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
        print(total_swap_days, 'total_swap_days')

        today = todays_date.strftime("%d-%b-%y")
        todays_date = datetime.strptime(today, "%d-%b-%y")
        end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d')
        start_date_value = datetime.strptime(start_date_value, '%Y-%m-%d')
        print(todays_date)
        print(start_date_value, 'start_date_value')
        print(end_date_value, 'end_date_value')

        # *******************Priced ,Unpriced Days*************************************************************************************************
        if todays_date <= start_date_value:

            unpriced_days = total_swap_days
            priced_days = 0

        elif (todays_date > start_date_value) and (todays_date <= end_date_value):

            unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
            priced_days = int(total_swap_days) - unpriced_days


        elif todays_date > end_date_value:
            unpriced_days = 0
            priced_days = int(total_swap_days)


        priced_volume = round(((priced_days / total_swap_days) * volume), 3)
        un_priced_volume = round(((volume / total_swap_days) * unpriced_days), 3)
        total_volume = round((priced_volume + un_priced_volume), 3)

        bbl_mt_conversion = round(float(bbl_mt) * float(volume) * float(tick), 3)
        kbbl_mt_conversion = round(
            ((float(bbl_mt) * float(volume) * float(tick)) / 1000), 3)
        unpriced_kbbl_mt = round(
            ((float(bbl_mt) * float(un_priced_volume) * float(tick)) / 1000),
            3)

        first_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(FW_Month))
        first_month = first_month.strftime('01-%m-%Y')
        first_month = datetime.strptime(first_month, '%d-%m-%Y')
        first_month = first_month.date()
        print(first_month, 'first_month')

        second_month = pd.to_datetime(start_date) + pd.DateOffset(months=int(second_FW_Month))
        second_month = second_month.strftime('01-%m-%Y')
        second_month = datetime.strptime(second_month, '%d-%m-%Y')
        second_month = second_month.date()
        print(second_month, 'second_month')

        # Last Traded Date Starting***************************************#
        if contract_name == 'RBOB 1st Line':
            print("contract_name_str,", contract_name)
            print("hello loop")
            filter_column = 'RBOB_Gasoline_futures'
        elif (contract_name == 'LS GO 1st Line') or (contract_name == 'LS GO 1st Line Mini'):
            filter_column = 'Ls_gas_oil'
        elif (contract_name == 'Brent 1st Line') or (contract_name == 'Brent 1st Line Mini'):
            filter_column = 'Brent_crude_futures'

        elif contract_name == 'WTI Crude Futures':
            filter_column = 'WTI_crude_futures'

        else:
            filter_column = contract_name
            print("Not matching company NAMEE")

        future_ltd_column_name_list = ['Ls_gas_oil', 'Brent_crude_futures', 'RBOB_Gasoline_futures',
                                       'Heating_oil_futures', 'WTI_crude_futures']

        if filter_column in future_ltd_column_name_list:

            try:
                contract_date_value = FutureLTD.objects.filter(Q(Contract_symbol=first_month)).values(filter_column)

            except:
                print('Error,LTD Not present in Admin side')

            for sub in contract_date_value:
                LTD = sub[filter_column]
                # LTD = datetime.strptime(LTD,'%d-%m-%Y')

            print('Last MAin Traded Day:', LTD)

            yesterday = todays_date - timedelta(days=1)
            yesterday = yesterday.date()
            print("yesterday_date", yesterday)

            first_month_value = first_month.strftime('01-%m-%Y')
            second_month_value = second_month.strftime('01-%m-%Y')

            first_month = datetime.strptime(first_month_value, '%d-%m-%Y')
            second_month = datetime.strptime(second_month_value, '%d-%m-%Y')

            First_Month_value = first_month.strftime("01-%b-%y")
            Second_Month_value = second_month.strftime("01-%b-%y")

            ## Last Trading Month

            Start_date_LTD = LTD.strftime("%Y-%m-01")
            Start_date_LTD = datetime.strptime(Start_date_LTD, "%Y-%m-%d")
            Start_date_LTD = Start_date_LTD.date()

            month = LTD.month
            year = LTD.year
            first_date, num_days = calendar.monthrange(year, month)

            # End Date Trading Month
            End_Date_LTD = str(num_days) + "-" + str(month) + "-" + str(year)
            End_Date_LTD = datetime.strptime(End_Date_LTD, '%d-%m-%Y')

            # Last Business day before LTD

            offset_x = pd.tseries.offsets.CustomBusinessDay(holidays=holiday_list,
                                                            n=1)  # change holiday list from singapore to real holiday list
            Day_before_LTD = LTD - offset_x

            from datetime import date
            today_format = date.today()

            start_date_value = start_date_value.date()
            Day_before_LTD = Day_before_LTD.date()
            End_Date_LTD = End_Date_LTD.date()

            print("LTD", LTD)
            print("Start_date_LTD:", Start_date_LTD)
            print("Day_before_LTD:", Day_before_LTD)
            print("End_Date_LTD:", End_Date_LTD)
            print(start_date_value, 'start_date_value', today_format, 'today_format', 'yesterday', yesterday)
            #
            #    # Total Days in Trading month
            Total_days_LTD = len(pd.bdate_range(start_date_value, End_Date_LTD, freq="C",
                                                holidays=holiday_list))  # change holiday list from singapore to real holiday list
            # Number of trading Days before LTD
            No_days_BF_LTD = len(pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))
            # Number of trading Days after LTD
            No_days_AF_LTD = len(pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))

            First_Month_Days_value = No_days_BF_LTD
            Second_Month_Days_value = No_days_AF_LTD

            print("Total_days_LTD NEW", Total_days_LTD)
            print("No_days_BF_LTD", No_days_BF_LTD)
            print("No_days_AF_LTD", No_days_AF_LTD)
            print("First_Month_Days_value:", First_Month_Days_value)
            print("Second_Month_Days_value:", Second_Month_Days_value)

            # try:
            #
            #     first_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == first_month, swaps_contract_value].iloc[0]
            #     second_month_price_value = \
            #         ICE_Pricing.loc[ICE_Pricing['Contract Month'] == second_month, swaps_contract_value].iloc[0]
            #
            #     First_Month_Settle_Price_value = first_month_price_value
            #     Second_Month_Price_value = second_month_price_value
            #
            # except:
            #     messagebox.showerror("error", 'Prices Unavailable for given Contract Date.Please add Pricing')
            #     raise

            if (today_format <= start_date_value):
                print('first')

                # MTM_Price = ((float(First_Month_Settle_Price_value) * No_days_BF_LTD) + (
                #         float(Second_Month_Price_value) * No_days_AF_LTD)) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                # first_month_price_value = round((float(First_Month_Settle_Price_value) * No_days_BF_LTD), 3)
                # second_month_price_value = round((float(Second_Month_Price_value) * No_days_AF_LTD), 3)

                priced_days_BF_LTD = 0
                unpriced_days_BF_LTD = No_days_BF_LTD
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD


            elif (today_format > start_date_value) and (today_format <= Day_before_LTD):

                print('second')
                priced_days_BF_LTD = len(
                    pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_BF_LTD = len(pd.bdate_range(today, Day_before_LTD, freq="C", holidays=holiday_list))
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, yesterday, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD) + (
                #                      unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD) +
                #                                 (float(First_Month_Settle_Price_value) * unpriced_days_BF_LTD), 3)
                #
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)


            elif (today_format == LTD):

                print('3rd')
                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = 0
                unpriced_days_AF_LTD = No_days_AF_LTD

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((unpriced_days_AF_LTD * float(Second_Month_Price_value)), 3)

            elif today_format > LTD and today_format <= End_Date_LTD:
                print('4rth')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = len(pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))
                unpriced_days_AF_LTD = len(pd.bdate_range(today_format, End_Date_LTD, freq="C", holidays=holiday_list))

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[
                #     settlement_prices_df["Date"].isin(
                #         pd.bdate_range(LTD, yesterday, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) +
                #              (unpriced_days_AF_LTD * float(Second_Month_Price_value))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)
                #
                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round(
                #     ((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)) + (
                #             unpriced_days_AF_LTD * float(Second_Month_Price_value))), 3)


            elif today_format > End_Date_LTD:
                print('5th')

                priced_days_BF_LTD = No_days_BF_LTD
                unpriced_days_BF_LTD = 0
                priced_days_AF_LTD = No_days_AF_LTD
                unpriced_days_AF_LTD = 0

                # priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(start_date_value, Day_before_LTD, freq="C", holidays=holiday_list))]
                # priced_avg_settlement_price = round((priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # AF_LTD_priced_settlement_price = settlement_prices_df[settlement_prices_df["Date"].isin(
                #     pd.bdate_range(LTD, End_Date_LTD, freq="C", holidays=holiday_list))]
                # AF_LTD_priced_avg_settlement_price = round(
                #     (AF_LTD_priced_settlement_price[swaps_contract_value].mean()), 3)
                #
                # MTM_Price = ((float(priced_avg_settlement_price) * priced_days_BF_LTD) + (
                #         priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price))) / (Total_days_LTD)
                # MTM_value = round(MTM_Price, 3)

                # first_month_price_value = round((float(priced_avg_settlement_price) * priced_days_BF_LTD), 3)
                # second_month_price_value = round((priced_days_AF_LTD * float(AF_LTD_priced_avg_settlement_price)),
                #                                  3)

            First_Month_value = first_month.strftime("%d-%b-%y")
            Second_Month_value = second_month.strftime("%d-%b-%y")

            print(priced_days_BF_LTD, 'priced_days_BF_LTD', 'unpriced_days_BF_LTD', unpriced_days_BF_LTD,
                  priced_days_AF_LTD, 'priced_days_AF_LTD', unpriced_days_AF_LTD, 'unpriced_days_AF_LTD')

            futures_equivalent_first_Month = round(((float(volume) / total_swap_days) * unpriced_days_BF_LTD),
                                                   3)
            futures_equivalent_second_Month = round(
                ((float(volume) / total_swap_days) * unpriced_days_AF_LTD), 3)

            Futures_equivalent_First_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_BF_LTD), 3)
            Futures_equivalent_Second_kbbl = round(
                ((float(kbbl_mt_conversion) / total_swap_days) * unpriced_days_AF_LTD), 3)

            print(futures_equivalent_first_Month, 'futures_equivalent_first_Month', futures_equivalent_second_Month,
                  'futures_equivalent_second_Month')
            print(Futures_equivalent_First_kbbl, 'Futures_equivalent_First_kbbl', Futures_equivalent_Second_kbbl,
                  'Futures_equivalent_Second_kbbl')


        else:

            futures_equivalent_first_Month = 0.0
            futures_equivalent_second_Month = 0.0
            Futures_equivalent_First_kbbl = 0.0
            Futures_equivalent_Second_kbbl = 0.0
            first_month = start_date
            second_month = end_date
            First_Month_Days_value = 0
            Second_Month_Days_value = 0.0
            First_Month_value = ''
            Second_Month_value = ''

        print('ManinTrade')
        print("Physical code:",physical_code)
        date = request.POST.get('date', '')



        print("datasave")

        print("trade id:",trade_id)


        obj = SwapBlotterModel(date=date, Trade_id=trade_id, trader_type=bileteral_external,clearer=clearer, trader_id=trader,
                               book=book, customer_account=company_account,
                               strategy_id=strategy, derivatives=derivatives,
                               volume=volume, customer_company=customer_company,
                               contract=contract_name, start_date=start_date,
                               end_date=end_date, price=price, approx_ep=approximate_ep,
                               holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                               tick=tick,unit=unit,singl_dif=singl_dif,mini_major=c.major_mini,
                               mini_major_connection=c.major_mini_conn,
                               bbi_mt_conversion=bbl_mt,
                               block_fee=block_fee,physica_blotter_connect=pb_id,
                               screen_fee=screen_fee,fw_months=FW_Month,physical_code=physical_code,
                               bbi_mt=bbl_mt_conversion, kbbl_mt_conversion=kbbl_mt_conversion,
                               notes=notes, buy_sell=buy_sell,
                               total_days=total_swap_days,
                               priced_days=priced_days, unpriced_days=unpriced_days, total_volume=total_volume,
                               priced_volume=priced_volume,unpriced_volume=un_priced_volume, unpriced_kbbl_mt=unpriced_kbbl_mt,
                               First_month=first_month,Second_month=second_month,
                               first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                               futures_equiv_first=futures_equivalent_first_Month,futures_equiv_second=futures_equivalent_second_Month,
                               futures_equiv_first_kbbl=Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=Futures_equivalent_Second_kbbl)
        obj.save()
        obj.duplicate_id = obj.id
        obj.save()
        messages.info(request, 'Saved')


        diff_id = obj.id
        print(
            '++++++++++++++++++++first save from form++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        if  (bileteral_external == 'External') and singl_dif != 'diff':
            return HttpResponseRedirect('/swaps-blotter')


        print("secondif")

        if singl_dif == 'diff':
            diff_result = self.diff_contract(request, date, bileteral_external, clearer, trader, book, customer_company,
                                             company_account, strategy, derivatives, volume, contract_name,
                                             start_date, end_date, price, approximate_ep, holiday, type, efs_code,
                                             brocker, diff_id, unit, tick, notes,trade_id)
            print(diff_result, '++++++++dIff Call')

            print("3rd if")

        if bileteral_external == 'Bilateral':
            print('bilateral')

            print("4th if")

            volume = -(volume) if float(volume) > 0 else abs(volume)
            int_priced_volume = -(priced_volume) if float(priced_volume) > 0 else abs(priced_volume)
            int_unpriced_volume = -(un_priced_volume) if float(un_priced_volume) > 0 else abs(un_priced_volume)
            int_total_volume = -(total_volume) if float(total_volume) > 0 else abs(total_volume)
            int_bbl_mt_conversion = -(bbl_mt_conversion) if float(bbl_mt_conversion) > 0 else abs(bbl_mt_conversion)
            int_kbbl_mt_conversion = -(kbbl_mt_conversion) if float(kbbl_mt_conversion) > 0 else abs(
                kbbl_mt_conversion)
            int_unpriced_kbbl_mt = -(unpriced_kbbl_mt) if float(unpriced_kbbl_mt) > 0 else abs(unpriced_kbbl_mt)
            int_unpriced_kbbl_mt = round(int_unpriced_kbbl_mt, 3)

            int_futures_equivalent_first_Month = -(futures_equivalent_first_Month) if float(
                futures_equivalent_first_Month) > 0 else abs(futures_equivalent_first_Month)
            int_futures_equivalent_second_Month = -(futures_equivalent_second_Month) if float(
                futures_equivalent_second_Month) > 0 else abs(futures_equivalent_second_Month)
            int_Futures_equivalent_First_kbbl = -(Futures_equivalent_First_kbbl) if float(
                Futures_equivalent_First_kbbl) > 0 else abs(Futures_equivalent_First_kbbl)

            int_Futures_equivalent_Second_kbbl = -(Futures_equivalent_Second_kbbl) if float(
                Futures_equivalent_Second_kbbl) > 0 else abs(Futures_equivalent_Second_kbbl)

            int_clearing_rate = 0.0

            int_brokerage = 0.0
            int_screen_fee = 0.0
            int_block_fee = 0.0
            int_total_fee = 0.0


            print("save copy")

            obj1 = SwapBlotterModel(date=date, Trade_id=trade_id,clearer=clearer, trader_id=trader,
                                    tick=c.tick,
                                    unit=c.unit,
                                    singl_dif=c.single_dif,
                                    mini_major=c.major_mini,
                                    mini_major_connection=c.major_mini_conn,
                                    bbi_mt_conversion=c.bbi_mt_conversion,
                                    block_fee=c.block_fee,
                                    screen_fee=c.screen_fee,fw_months=FW_Month,
                                    bbi_mt=int_bbl_mt_conversion, kbbl_mt_conversion=int_kbbl_mt_conversion,
                                    book=customer_company, customer_account=company_account,
                                    strategy_id=strategy, derivatives=derivatives,physica_blotter_connect=pb_id,
                                    volume=volume, customer_company=book,physical_code=physical_code,
                                    contract=contract_name, start_date=start_date,
                                    end_date=end_date, price=price, approx_ep=approximate_ep,
                                    holiday=holiday, type=type, efs_code=efs_code, broker=brocker,
                                    notes=notes, duplicate_id=obj.id, trader_type=bileteral_external,
                                    buy_sell=buy_sell, total_days=total_swap_days,
                                    priced_days=priced_days, unpriced_days=unpriced_days, total_volume=int_total_volume,
                                    priced_volume=int_priced_volume, unpriced_volume=int_unpriced_volume, unpriced_kbbl_mt=int_unpriced_kbbl_mt,
                                    First_month=first_month,Second_month=second_month,
                                    first_month_days=First_Month_Days_value ,second_month_days=Second_Month_Days_value,
                                    futures_equiv_first=int_futures_equivalent_first_Month,futures_equiv_second=int_futures_equivalent_second_Month,
                                    futures_equiv_first_kbbl=int_Futures_equivalent_First_kbbl,futures_equiv_second_kbbl=int_Futures_equivalent_Second_kbbl)
            obj1.save()
            obj.duplicate_id = diff_id
            obj.save()

            if (c.single_dif == 'diff') and (bileteral_external == 'Bilateral'):
                diff_result_bilat = self.diff_contract(request, date, bileteral_external, clearer, trader,
                                                       customer_company,
                                                       book, company_account, strategy, derivatives, volume,
                                                       contract_name,
                                                       start_date, end_date, price, approximate_ep, holiday, type,
                                                       efs_code,
                                                       brocker, diff_id, unit, tick, notes,trade_id)

                print(diff_result_bilat)

        print('first return')

        # update_database(request)

        messages.info(request, 'Saved')
        return HttpResponseRedirect('/swaps-blotter')

class DeleteSwapsBlotter(View):
    
    def get(self,request,*args, **kwargs):
        return render(request,'backend/delete-swaps-blotter.html')
    
    def post(self,request,*args, **kwargs):
        obj = SwapBlotterModel.objects.get(id=kwargs['id'])
        if obj.duplicate_id == 'none':
            obj.delete()
        else:
            print(kwargs['id'])
            obj = SwapBlotterModel.objects.get(id=kwargs['id'])
            print(obj)
            print('dddddddddddddddddddd')
            obj2 = SwapBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = SwapBlotterModel.objects.get(id=i.id)
                obj1.delete()

        messages.info(request,'Deleted')
        return HttpResponseRedirect('/swaps-blotter')


#########  delete swaps tradehistory

class DeleteSwapsTradeHistory(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'backend/delete-swaps-blotter.html')

    def post(self, request, *args, **kwargs):
        obj = SwapBlotterModel.objects.get(id=kwargs['id'])
        if obj.duplicate_id == 'none':
            obj.delete()
        else:
            print(kwargs['id'])
            obj = SwapBlotterModel.objects.get(id=kwargs['id'])
            print(obj)
            print('dddddddddddddddddddd')
            obj2 = SwapBlotterModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = SwapBlotterModel.objects.get(id=i.id)
                obj1.delete()

        messages.info(request, 'Deleted')
        return HttpResponseRedirect('/swap-trade-history')


def search_customer_company(request, company_name):
    print("hello serch compnay")

    print("conpnay name:",company_name)
    obj = CompanyInvestmentModel.objects.filter(Customer_Company_name__icontains=company_name)
    lis = [{'data':data.Customer_Account} for data in obj]
    print(lis)
    print("hell",lis)
    return JsonResponse({'company_name':lis}, safe=False)




def swaps_bloters_clearer_derivative(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        clearer_name = data_dict.get('clearer')

        obj = ClearerRateM.objects.filter(Q(clearer__name=clearer_name), Q(derivative='swaps')) 
        data =[{'data':data.contract.contract_name} for data in obj]
        print("data:",data)
        return JsonResponse({'data':data}, safe=False)


def contract_name_holiday_relation(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract_name')
        print("contractname:",contract_name)
        obj = ContractM.objects.filter(contract_name=contract_name)

        print("obj new:",obj)

        print(contract_name)
        obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith=contract_name)
        data = [{'date':data.holiday}for data in obj]
        data1 = [{'data':i.brocker.name}for i in obj2]

        data3 = [{'data':data.unit}for data in obj]
        data4 = [{'data': data.tick} for data in obj]

        print(data1)

        uniq_data1 =[]
        for x in data1:
            if x not in uniq_data1:
                uniq_data1.append(x)

        print("uniq_data1 22",uniq_data1)

        print("Holiday 22:",data)
        print('ddd')

        print("22 unit ",data3)
        print("22 tick ", data4)

    return JsonResponse({'data':data, 'data1':uniq_data1,'data3':data3,'data4':data4}, safe=False)





from django.utils import timezone
from datetime import datetime, timedelta
def enddate_of_month(request):

    request_data = request.body.decode('utf-8')
    data_dict = json.loads(request_data)
    date_string = data_dict.get('start_date')
    # date_string = request.POST.get('date')
    print("date_string",date_string)
    # try:
        # Convert the user input to a datetime object
    date = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Calculate the last day of the month
    year = date.year
    month = date.month
    _, last_day = calendar.monthrange(year, month)
    last_date = datetime(year, month, last_day).date()

    print("last:date",last_date)

    # except ValueError:
    #     error_message = 'Invalid date format. Please enter a date in the format YYYY-MM-DD.'
    #     return render(request, 'error.html', {'error_message': error_message})
    return JsonResponse({'data':last_date}, safe=False)


# export swapsblotter to CSV
def export_sb_csv_today(request):
    today = date.today()
    print("first today:", today)
    sb= SwapBlotterModel.objects.filter(date__icontains=today)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Swapblotter.csv'
    writer = csv.writer(response)
    writer.writerow(['No','date','trader_type','trader','book',
                    'customer_company','customer_account','strategy','derivatives','clearer',
                    'contract','volume','start_date','end_date','price','approx_ep','holiday','type','broker','efs_code','notes',
                    'Trade_id', 'tick', 'unit', 'singl_dif', 'mini_major', 'mini_major_connection','bbi_mt_conversion','kbbl_mt_conversion','total_days',

                     'priced_days', 'unpriced_days', 'total_volume', 'priced_volume', 'unpriced_volume', 'block_fee','screen_fee', 'brockerage', 'total_fee',

                     'bbi_mt', 'kbbi_mt', 'unpriced_kbbl_mt', 'fw_months', 'LTD', 'First_month','Second_month','MTM','first_month_days','second_month_days',
                     'first_month_settle_price', 'second_month_settle_price', 'PNL','total_PNL','futures_equiv_first','futures_equiv_second','futures_equiv_first_kbbl',
                     'futures_equiv_second_kbbl','bileteral_external','buy_sell','physical_code',
                  ] )

    sb_fields = sb.values_list(

        'id', 'date','trader_type','trader','book',
        'customer_company','customer_account','strategy','derivatives','clearer',
        'contract', 'volume', 'start_date', 'end_date', 'price', 'approx_ep', 'holiday', 'type', 'broker', 'efs_code','notes',

        'Trade_id', 'tick', 'unit', 'singl_dif', 'mini_major', 'mini_major_connection','bbi_mt_conversion','kbbl_mt_conversion','total_days',
        'priced_days', 'unpriced_days', 'total_volume', 'priced_volume', 'unpriced_volume', 'block_fee','screen_fee', 'brockerage', 'total_fee',
        'bbi_mt', 'kbbi_mt', 'unpriced_kbbl_mt', 'fw_months', 'LTD', 'First_month', 'Second_month', 'MTM',
        'first_month_days', 'second_month_days',
        'first_month_settle_price', 'second_month_settle_price', 'PNL', 'total_PNL', 'futures_equiv_first',
        'futures_equiv_second', 'futures_equiv_first_kbbl',
        'futures_equiv_second_kbbl', 'bileteral_external', 'buy_sell', 'physical_code',

         )

    for item in sb_fields:
        writer.writerow(item)
    return response













# export swapsblotter to CSV
def export_sb_csv(request):
    sb= SwapBlotterModel.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Swapblotter.csv'
    writer = csv.writer(response)
    writer.writerow(['No','date','trader_type','trader','book',
                    'customer_company','customer_account','strategy','derivatives','clearer',
                    'contract','volume','start_date','end_date','price','approx_ep','holiday','type','broker','efs_code','notes',
                    'Trade_id', 'tick', 'unit', 'singl_dif', 'mini_major', 'mini_major_connection','bbi_mt_conversion','kbbl_mt_conversion','total_days',

                     'priced_days', 'unpriced_days', 'total_volume', 'priced_volume', 'unpriced_volume', 'block_fee','screen_fee', 'brockerage', 'total_fee',

                     'bbi_mt', 'kbbi_mt', 'unpriced_kbbl_mt', 'fw_months', 'LTD', 'First_month','Second_month','MTM','first_month_days','second_month_days',
                     'first_month_settle_price', 'second_month_settle_price', 'PNL','total_PNL','futures_equiv_first','futures_equiv_second','futures_equiv_first_kbbl',
                     'futures_equiv_second_kbbl','bileteral_external','buy_sell','physical_code',
                  ] )

    sb_fields = sb.values_list(

        'id', 'date','trader_type','trader','book',
        'customer_company','customer_account','strategy','derivatives','clearer',
        'contract', 'volume', 'start_date', 'end_date', 'price', 'approx_ep', 'holiday', 'type', 'broker', 'efs_code','notes',

        'Trade_id', 'tick', 'unit', 'singl_dif', 'mini_major', 'mini_major_connection','bbi_mt_conversion','kbbl_mt_conversion','total_days',
        'priced_days', 'unpriced_days', 'total_volume', 'priced_volume', 'unpriced_volume', 'block_fee','screen_fee', 'brockerage', 'total_fee',
        'bbi_mt', 'kbbi_mt', 'unpriced_kbbl_mt', 'fw_months', 'LTD', 'First_month', 'Second_month', 'MTM',
        'first_month_days', 'second_month_days',
        'first_month_settle_price', 'second_month_settle_price', 'PNL', 'total_PNL', 'futures_equiv_first',
        'futures_equiv_second', 'futures_equiv_first_kbbl',
        'futures_equiv_second_kbbl', 'bileteral_external', 'buy_sell', 'physical_code',

         )

    for item in sb_fields:
        writer.writerow(item)
    return response



### new for customer company and broker same as cleaerer
def swaps_blotters_company_broker_derivative(request):
    if request.method == "POST":
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        contract_name = data_dict.get('contract_name')
        print("contract_name",contract_name)

        obj = ContractM.objects.filter(contract_name=contract_name)
        print("obj new:", obj)
        data2 = [{'date': data.holiday} for data in obj]

        obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith=contract_name)
        data = [{'data': i.brocker.name} for i in obj2]
        print(data)

        data3 = [{'data': data.unit} for data in obj]
        data4 = [{'data': data.tick} for data in obj]

        uniq_data1 = []
        for x in data:
            if x not in uniq_data1:
                uniq_data1.append(x)

        print("Holiday 22:", data2)
        

        print(data)
        print('ddd')
        return JsonResponse({'data': uniq_data1,'holiday':data2,'unit':data3,'tick':data4}, safe=False)




# contract_name = data_dict.get('contract_name')
#         print("contractname:",contract_name)
#         obj = ContractM.objects.filter(contract_name=contract_name)
#
#         print("obj new:",obj)
#
#         print(contract_name)
#         obj2 = BrockerageM.objects.filter(contract_name__contract_name__istartswith=contract_name)
#         data = [{'date':data.holiday}for data in obj]
#         data1 = [{'data':i.brocker.name}for i in obj2]
#
#         data3 = [{'data':data.unit}for data in obj]
#         data4 = [{'data': data.tick} for data in obj]
#
#         print(data1)
#
#         uniq_data1 =[]
#         for x in data1:
#             if x not in uniq_data1:
#                 uniq_data1.append(x)
#
#         print("uniq_data1 22",uniq_data1)
#
#         print("Holiday 22:",data)
#         print('ddd')
#
#         print("22 unit ",data3)
#         print("22 tick ", data4)
#
#     return JsonResponse({'data':data, 'data1':uniq_data1,'data3':data3,'data4':data4}, safe=False)



# update database swap blotter
def update_database(request,*args,**kwargs):
    id = kwargs.get("id")
    print("ID OF MINE:",id)
    sb_values = SwapBlotterModel.objects.all()
    print("sb_values",sb_values)
    today_up = date.today()
    print("today_date in update:",today_up)

    for i in sb_values:
        print('iiiii',i)
        print("i.startdate",i.start_date)
        startdate_up = i.start_date
        print("startdate_up:",startdate_up)
        enddate_up = i.end_date
        print("enddate_up:", enddate_up)

        print("i.end_date", i.end_date)
        print("i.Holiday", i.holiday)
        holiday_up = i.holiday
        print("holiday_up:",holiday_up)
        volume = i.volume
        edit_trade_id=i.Trade_id
        print("Volume:",volume)

        print("************* Coversion from string to particular type")

        startdate_up = datetime.strptime(startdate_up, '%Y-%m-%d').date()
        print("converted start_date:", startdate_up)
        enddate_up = datetime.strptime(enddate_up, '%Y-%m-%d').date()
        print("converted end_date:", enddate_up)

        # date_ = datetime.strptime(date, '%Y-%m-%d').date()
        # print("converted date_:", date_)
        #
        # bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        # print("converted bl_date:", bl_date)
        print('****************************************')

        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday_up).values_list("date")
        print("holiday_list_of_selected_holi:",holiday_list_of_selected_holi)
        holiday_date_df = pd.DataFrame(holiday_list_of_selected_holi,columns=['Dates'])
        holiday_date_df['Dates']= pd.to_datetime(holiday_date_df["Dates"])
        holiday_list_of_selected_holi=holiday_date_df['Dates'].to_list()

        print("new holiday list with only dates:",holiday_list_of_selected_holi,type(holiday_list_of_selected_holi))


        # holiday_list_of_selected_holi = str(holiday_list_of_selected_holi)
        # print("after string:, listt",holiday_list_of_selected_holi,type(holiday_list_of_selected_holi))
        # singapore_holiday = ['2023-01-30', '2023-01-09', '2023-01-29', '2023-02-01']

    #     print(":CALCULATING PRICED AND UNPRICED DAYS FOR UPDATING DATABASE1:")


        # workingdays
        workingdays = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
        workingdays = len(workingdays)
        print("working b4 overwrite 5:", workingdays)

        # <!----- priced and unpriced days start ----!>
        if today_up <= startdate_up:
            print("first condition priced days")
            priced_days= 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
            unpriced_days = len(unprice_calcu)
            print("unpriced in uodate:",unpriced_days)
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (today_up > startdate_up) and (today_up <= enddate_up):

            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=today_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi))

            workday = len(pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi))
            priced_days = workday - unpriced_days
            print("workday update:",workday)
            print("priced_days_up:",priced_days)
            print("unpriced_days update:", unpriced_days)
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        # elif (today > start_date_value) and (today<=end_date_value):

        elif (today_up > enddate_up):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()

        else:
            pass
            # <!----- priced unpriced end ---!>
        print(":CALCULATING PRICED AND UNPRICED VOLUME FOR UPDATING DATABASE1:")
        # <!-----priced volume ----!>
        #    priced_volume_update = (priced_days_update / total_swaps_days_update) * volume_update
        #    priced_volume_update = round(priced_volume_update, 2)
        print("priced_days up:",priced_days, type(priced_days))
        print("working_days up:",workingdays,type(workingdays))
        print("Volume UP:",volume)

        priced_days = float(priced_days)
        print("float priced_days",priced_days)

        workingdays = float(workingdays)
        print("float priced_days", workingdays)

        priced_volume = (float(priced_days) / float(workingdays)) * float(volume)

        print("errror")

        print("priced volume up:", priced_volume)

        print("unpriced days",unpriced_days)

        unpriced_volume = (float(volume) / float(workingdays)) * float(unpriced_days)
        print("hellllo")
        priced_volume = round(priced_volume, 2)
        unpriced_volume = round(unpriced_volume, 2)
        print("priced volume up:", priced_volume)
        print("Unpriced volume up:", unpriced_volume)
        unpriced_volume = round(unpriced_volume, 2)
        print("Unpriced volume round up:", unpriced_volume)

        total_volume = priced_volume + unpriced_volume
        print("TOTAL VOLUME: ", total_volume)
        total_volume = round(total_volume, 2)
        print("TOTAL VOLUME round: ", total_volume)
        # <!------priced volume end ---!>

        print("## ADDING PRICED/UNPRICED DAYS PRICED UNPRICED VOLUME TO DB AUTOMATICALLY ##")


        print("hello")

        all_swap_up = SwapBlotterModel.objects.all()
        # for i in all_swap_up:
        trade_id=i.Trade_id
        edit_start_date=i.start_date

        print(trade_id,'tarde_id')
        print("hello update swap")
        print("i.price_days",i.priced_days)
        i.priced_days = priced_days

        update_priced_days=i.priced_days
        print("new priced up :", update_priced_days)
        print("i.unpriced:",i.unpriced_days)
        i.unpriced_days = unpriced_days
        update_unpriced_days=i.unpriced_days
        print("new unprice up:", update_unpriced_days)
        #
        print("i.price_volume:", i.priced_volume)
        i.priced_volume = priced_volume
        update_priced_volume=i.priced_volume
        print("new priced volume up", i.priced_volume)
        print("i.unprice_volume:", i.unpriced_volume)
        i.unpriced_volume = unpriced_volume
        update_unpriced_volume=i.unpriced_volume
        print("new unpriced volume up")
        print("end update swap")
    #         # i.save()
        SwapBlotterModel.objects.filter(Trade_id=edit_trade_id,start_date=startdate_up,end_date=enddate_up,volume=volume).update(priced_days=update_priced_days,unpriced_days=update_unpriced_days,priced_volume=update_priced_volume,unpriced_volume=update_unpriced_volume,total_days=workingdays)

        print("OUTSIDE LOOP SWAP")

    return HttpResponseRedirect("swaps-blotter")

    # update_status_in_admin.Status = "Discharged"
    # update_status_in_admin.save()

    # return render(request,"customer/sb.html")


##################################   AddCompanyInvestment Blotter

class AddCompanyInvestment(CreateView):
    form_class = CompanyInvestmentForm
    template_name = "customer/Customer-Investment-add.html"
    model = CompanyInvestmentModel
    success_url = reverse_lazy("backendapp:add-company-investment")

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        messages.success(self.request," Company Investment  has been saved")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companyinvestment = CompanyInvestmentModel.objects.all()
        context["companyinvestments"] =companyinvestment
        return context

#
class CompanyInvestmentEditView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        companyinvestment = CompanyInvestmentModel.objects.get(id=id)
        form = CompanyInvestmentForm(instance=companyinvestment)
        return render(request, "customer/edit-company-investment.html", {"form": form})
    def post(self,request,*args,**kwargs):
        id= kwargs.get("id")
        companyinvestment = CompanyInvestmentModel.objects.get(id=id)
        form =CompanyInvestmentForm(request.POST,instance=companyinvestment,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Company Investment has been updated")
            # return render(request,"super_admin/Trader-add.html",{"form":form})
            return HttpResponseRedirect('/add-company-investment')

        else:
            messages.info(request,"Company Investment updation failed")
            return render(request,"customer/edit-company-investment.html",{"form":form})

def RemoveCompanyInvestment(request,*args,**kwargs):
    id=kwargs.get("id")
    companyinvestment=CompanyInvestmentModel.objects.get(id=id)
    companyinvestment.delete()
    messages.info(request,"Company Investment has been removed")
    return HttpResponseRedirect('/add-company-investment')



## Tank Capacity

class TankCapacityView(CheckUserMixins, ListView):
    model = TankCapacityM

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_query = self.request.POST.get('search_query')
        if search_query:
            context['object_list'] = self.model.objects.filter(
                Q(Port_name__istartswith=search_query) | Q(Terminal__name=search_query) | Q(
                    Cargo=search_query))
            context['port'] = PortM.objects.all()
            context['terminal'] = TerminalM.objects.all()
            context['tank_type'] = TankTypeM.objects.all()
            context['tank_no'] = TankNumberM.objects.all()
            # context['unit'] = Unit.objects.all()
            return context
        else:
            context['object_list'] = self.model.objects.all()
            context['port'] = PortM.objects.all()
            context['terminal'] = TerminalM.objects.all()
            context['tank_type'] = TankTypeM.objects.all()
            context['tank_no'] = TankNumberM.objects.all()
            # context['unit'] = Unit.objects.all()
            return context

    def post(self, request):
        delet_id = request.POST.get('delet_id')
        if delet_id:
            obj = TankCapacityM.objects.get(id=delet_id)
            obj.delete()
            messages.info(request, "Succefully Deleted")
            return HttpResponseRedirect('tank-capacity')
        port = request.POST['port']
        terminal = request.POST['terminal']
        tank_type = request.POST['tank_type']
        tank_no = request.POST['tank_no']
        product_status = "Empty"
        density = 0
        density = int(density)
        current_qty = 0
        qty_add_discharge = 0
        nominal_capacity = request.POST['nominal_capacity']
        safe_fill_capacity = request.POST['safe_fill_capacity']
        prevailing_GOV = request.POST['prevailing_GOV']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        # today = request.POST['today']
        today = datetime.today()

        cost = request.POST['cost']
        remarks = request.POST['remarks']
        # calculations
        # workingdays
        workingdays = pd.date_range(start=start_date, end=end_date, freq="C")
        duration = len(workingdays)
        remaining_days = pd.date_range(start=today, end=end_date, freq="C")
        remaining_days= len(remaining_days)
        cargo = "EMPTY"






        obj = TankCapacityM(Port_id=port, Terminal_id=terminal, Tank_type_id=tank_type,
                                 Tank_no_id=tank_no, product_status=product_status,
                                 Density=density,Nominal_capacity=nominal_capacity,
                                 Safe_fill_capacity=safe_fill_capacity, Prevailing_GOV=prevailing_GOV, start_date=start_date,
                                 end_date=end_date,Today=today,Cost=cost,Remarks=remarks,
                                 #calculation behind
                                 duration=duration,Remaining_space=safe_fill_capacity,current_quantity=current_qty,
                                 Qty_add_discharge=qty_add_discharge, Remaining_days=remaining_days,Cargo=cargo,


                                 # Cargo=cargo,


                                 )
        obj.save()
        return HttpResponseRedirect('tank-capacity')


class EditTankCapacity(View):

    def get(self, request, *args, **kwargs):
        data = TankCapacityM.objects.get(id=kwargs['id'])
        context = {}
        context['object_list'] = TankCapacityM.objects.all()
        context['port'] = PortM.objects.all()
        context['cargo'] = CargoM.objects.all()
        context['strategy'] = Strategy.objects.all()
        context['book'] = Book.objects.all()
        # context['unit'] = Unit.objects.all()
        context['data'] = data
        return render(request, "backend/edit_unique_trader.html", context)

    def post(self, request, *args, **kwargs):
        data = GenerateTradeModel.objects.get(id=kwargs['id'])
        data.Company_name_id = request.POST['company_name']
        data.Book_id = request.POST['book']
        data.Quantity = request.POST['quantity']
        data.Cargo_id = request.POST['cargo']
        data.Status = request.POST['status']
        # data.Unit_id = request.POST['unit']
        data.Strategy_id = request.POST['strategy']
        data.save()
        return HttpResponseRedirect('/tank-capacity')


# Physical Blotter model same as swap
class PhysicalBlotterView(CheckUserMixins, View):
    def get(self, request, **kwargs):
        obj = GenerateTradeModel.objects.get(id=kwargs['id'])
        book = Book.objects.all()


        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:",holiday_distict)

        uniq_holiday_list=[]
        for x in holiday_distict:
            if x not in uniq_holiday_list:
                uniq_holiday_list.append(x)
        print("uniq_holiday_list:",uniq_holiday_list)

        working_distinct_holiday = HolidayM.objects.order_by().values_list('name').distinct()
        print("working_distinct_holiday",working_distinct_holiday)



        unit = Unit1.objects.all()
        holiday = HolidayM.objects.all()
        print("holiday :",holiday)
        port = PortM.objects.all()
        terminal = TerminalM.objects.all()
        tank = TankCapacityM.objects.all()
        print("tank:",tank)
        # ntank = tank.name
        # print("new tank:",ntank)
        type = TYPEMODEL.objects.all()
        pricing_contract = ContractM.objects.all()
        data = FutureBlotterModel.objects.all()
        context = {'book': book, 'holiday': uniq_holiday_list, 'port': port,
                   'terminal': terminal,'pricing_contract':pricing_contract,
                   'tank': tank, 'unit':unit,
                   'type': type, 'object_list': data, 'd': obj}
        print("context end:")
        return render(request, "customer/physicalblotter.html", context)
    def post(self, request, *args, **kwargs):
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:",date)
        tradeid = request.POST.get('tradeid', '')
        trader = request.POST.get('trader', '')  # id
        print("trader:",trader)
        book = request.POST.get('book', '')  # id
        company_name = request.POST.get('company_name', '')
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        derivatives = request.POST.get('derivatives', '')
        print("derivatives:",derivatives)
        # buysell = request.POST.get('buysell', '')
        cargo = request.POST.get('cargo', '')
        pricing_contract = request.POST.get('pricing_contract','')
        pricing_methode = request.POST.get('pricing_methode', '')  # id
        volume = request.POST.get('quantity', '')
        print("volume_qty",volume)

        unit = request.POST.get('unit', '')
        print("Unit",unit)
        density = request.POST.get('density', '')
        nominated_quantity = request.POST.get('nominated_quantity', '')
        premium_discount = request.POST.get('premium_discount', '')
        print("premium_discount:",premium_discount)
        pricing_term = request.POST.get('pricing_term', '')
        bl_date = request.POST.get('bl_date', '')
        print("BL date:",bl_date)
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        holiday = request.POST.get('holiday', '')
        print("holiday get:",holiday)
        deliverymode = request.POST.get('deliverymode', '')
        port = request.POST.get('port', '')
        print("port:",port)
        terminal = request.POST.get('terminal', '')
        vessal_name = request.POST.get('vessal_name', '')
        tank = request.POST.get('tank', '')
        print("Tank",tank)
        external_terminal = request.POST.get('external_terminal', '')
        hedging = request.POST.get('hedging', '')
        Remarks = request.POST.get('Remarks', '')

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = PhysicalBlotterModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/pb-list/")

        # #update status in admin side :
        # admin_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        # current_admin_status = admin_status.Status
        # print("current status:",current_admin_status)
        #
        # #copied code
        # admin_volume = GenerateTradeModel.objects.get(Trade_id=tradeid)
        # print("tettesrt")
        # deal_volume = admin_volume.Quantity
        # print("current volume:", deal_volume)
        #
        # update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
        # update_status_in_admin.Status = "Process"
        # update_status_in_admin.save()
        #
        # print("after updating status:",update_status_in_admin.Status)
        #
        # Purchase/salesID
        volume = float(volume)

        if volume >= 0:
            print("Buying")
            print("cargo buying:", cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "P" + "-" + cargo + "-" + randint_
            print("purchase_id buying:",purchase_id)
            buysell = "Buy"
        elif volume <= 0:
            print("selling")
            print("cargo selling:", cargo)
            cargo = str(cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "S" + "-" + cargo + "-" + randint_
            print("purchase_id selling:", purchase_id)
            buysell= "Sell"
        else:
            pass
        #
        print("************* Coversion from string to particular type")

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        print("converted start_date:", start_date)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        print("converted end_date:", end_date)

        date_ = datetime.strptime(date, '%Y-%m-%d').date()
        print("converted date_:", date_)

        bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        print("converted bl_date:", bl_date)
        print('****************************************')


        # HOLIDAY DATE LIST OF SELECTED HOLIDAY in DATAFRAME

        #   the working holiday list dates  using data frame
        print("Finding holiday:")
        print("Holioday selected", holiday)
        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        # workingdays
        holi_list_selcted = []
        for i in holiday_list_of_selected_holi:
            holi_list_selcted.append(i)
        print("new list of selected holi:", holi_list_selcted)


        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holi_list_selcted, 'first++++++++total_swap_days')

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holi_list_selcted = holiday_date_df['Dates'].to_list()
        print(holiday_list, 'first++++++++total_swap_days')

        total_working_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holi_list_selcted))
        print(total_working_days, '++++++++total_swap_days')

        # <!----- priced and unpriced days start ----!>

        print("Priced unpriced starting")

        if date_ <= start_date:
            print("first condition priced days")
            priced_days = 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            unpriced_days = len(unprice_calcu)
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (date_ > start_date) and (date_ <= end_date):
            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=holi_list_selcted))

            workday = len(pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted))
            priced_days = workday - unpriced_days
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
        #
        elif (date_ > end_date):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        else:
            pass

        print("Priced unpriced end")
            # <!----- priced unpriced end ---!>

        # # <!-----priced volume ----!>

        print("Priced volume begining")

        pricing_methode = str(pricing_methode)

        print("pricing_methode b4 volume",pricing_methode)
        unit = str(unit)

        if pricing_methode == "Fixed":
            print('hi Fixed')
            print("startdate:", start_date)
            print("enddate:", end_date)

            if start_date == end_date:

                total_volume = volume
                total_volume = round(volume, 3)
                print("totalk volume:",total_volume)
                priced_volume = total_volume
                unpriced_volume = 0
                # instance = form.save(commit=False)
                # instance.total_volume = total_volume
                # # instance.position = total_volume
                # instance.price_volume = priced_volume
                # instance.unprice_volume = unpriced_volume
                # instance.save()
                print('+++++++++++++++++++++++++++++++++++++++++')
            else:
                pass
        elif pricing_methode == "Float":
            print('hi float')
            total_volume = volume
            priced_volume = (total_volume / total_working_days) * priced_days
            priced_volume = round(priced_volume, 3)
            print("priced volume:", priced_volume)
            unpriced_volume = (total_volume / total_working_days) * unpriced_days
            unpriced_volume = round(unpriced_volume, 3)
            print("unpriced_volume", unpriced_volume)
            # instance = form.save(commit=False)
            # instance.total_volume = total_volume
            # # instance.position = total_volume
            # instance.price_volume = priced_volume
            # instance.unprice_volume = unpriced_volume
            # instance.save()
            print('+++++++++++++++++++++++++++++++++++++++++')

        # ######## status change ###############
        status = "Open"
        status = str(status)
        print("status converted to open:", status)

        shore_recieved = 0

        generate_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        print("hai", generate_status.Status)
        print("testing")

        ### newly added from dileena to conver to cubic meter
        if unit == 'MT':
            if float(density) < 1:
                m3 = round(float(volume) / float(density), 3)
            else:
                m3 = round((float(volume) / float(density)) / 1000, 3)
        elif unit == 'm³':
            m3 = round(float(volume) * 1, 3)

        elif unit == 'bbl':

            m3 = round(float((volume) / 6.289) / float(density), 3) if float(
                density) < 1 else round(float((volume) / 6.289) / (float(density) / 1000), 3)

        print("total volume b4:",total_volume)

        print("priced_volume:",priced_volume)
        print("unpriced_volume:", unpriced_volume)
        #
        print("object creation for pb")
        obj = PhysicalBlotterModel(Date=date, Trader=trader, Book=book, Company_name=company_name,
                                 Strategy=strategy, Derivative=derivatives,
                                 Trade_id=tradeid, Buy_sell=buysell,
                                 Cargo=cargo,
                                 Pricing_contract_id=pricing_contract, Pricing_method=pricing_methode,
                                 Quantity=volume, Unit=unit,
                                 Density=density, Nominated_quantity=nominated_quantity,
                                 Premium_discount=premium_discount, Pricing_term=premium_discount,

                                 bl_date=bl_date,start_date=start_date, end_date=end_date,
                                   Holiday=holiday,
                                 Total_no_days=total_working_days, Delivery_mode=deliverymode,
                                 Port=port, Terminal=terminal,
                                 Vessal_name=vessal_name, Tank=tank,Remarks=Remarks,
                                 External_Terminal=external_terminal,Headging=hedging,
        #                            # calculated and_ get_values
                                 Purchase_sales_ID= purchase_id,status = status,
                                 price_days=priced_days,unprice_days = unpriced_days,
                                 total_volume = total_volume,price_volume = priced_volume,
                                 unprice_volume = unpriced_volume,Shore_recieved=shore_recieved,m3=m3,
                                 )
        obj.save()

        # update status in admin side :
        admin_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        current_admin_status = admin_status.Status
        print("current status:", current_admin_status)

        # copied code
        pb_volume_list=[]
        admin_volume = GenerateTradeModel.objects.get(Trade_id=tradeid)
        print("tettesrt")
        deal_volume = admin_volume.Quantity
        print("deal volume:", deal_volume)

        pb_volume = PhysicalBlotterModel.objects.filter(Trade_id=tradeid)
        if pb_volume:
            print("work")
            # pb_volume_list.append(pb_volume.Quantity)
            for i in pb_volume:
                quantity = i.Quantity
                pb_volume_list.append(float(quantity))

            print("testt volumepb")

            print("current volume:", pb_volume)
            pb_volume_sum = sum(pb_volume_list)
            print("pb_volume_sum:",pb_volume_sum)
            print("end")

            deal_current_volume_update = float(deal_volume) - float(pb_volume_sum)
            print("deal_current_volume_update", deal_current_volume_update)

            if float(deal_volume) == float(pb_volume_sum):
                print("inside if ")
                update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
                update_status_in_admin.Status = "Process"
                update_status_in_admin.deal_current_qty = deal_current_volume_update
                update_status_in_admin.save()
                print("after updating status:", update_status_in_admin.Status)
            else:
                update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
                update_status_in_admin.deal_current_qty = deal_current_volume_update
                update_status_in_admin.save()

        else:
            pass

        print(" saved Physical Blotter")
        messages.info(request, 'physical-blotter Trade Saved')
        return HttpResponseRedirect('/pb-list/')


def tank_port_terminal_relation(request):
    print("Hi Port")
    if request.method == "POST":
        print("Hello Post methode")
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        port_name = data_dict.get('port_name')
        print("Port name:",port_name)
        obj = TankCapacityM.objects.filter(Port__name=port_name)
        print("obj:",obj)
        for data in obj:
            print("checking:",data.product_status)
            print("checking:", data.Terminal.name)
            print("checking:", data.Tank_no.name)

        data = [{'date': data.Terminal.name} for data in obj]
        data1 = [{'data': i.Tank_no.name} for i in obj]

        print("data:",data)
        uniq_data = []
        for x in data:
            if x not in uniq_data:
                uniq_data.append(x)
        print("uniq data:", uniq_data)
        print("data1:", data1)
        uniq_data1 = []
        for x in data1:
            if x not in uniq_data1:
                uniq_data1.append(x)
        print("uniq data1:", uniq_data1)

        print(data1)
        print('ddd')
    return JsonResponse({'data':uniq_data, 'data1':uniq_data1}, safe=False)


#Physical bLotter loist view
# class PBListView(ListView):
#     template_name = "customer/pb-list2.html"
#     model = PhysicalBlotterModel
#     context_object_name = 'physicalblotters'


class PBListView(View):
    def get(self,request,*args,**kwargs):
        qs = PhysicalBlotterModel.objects.order_by('-Date')
        print("physicalblotters:",qs)
        update_pb_database(request)
        return render(request,"customer/pb-list2.html",{"physicalblotters":qs})


    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")


    def post(self, request,*args,**kwargs):
        id = self.request.POST.get('delete_feild')
        obj = PhysicalBlotterModel.objects.get(id=id)
        trade_id = obj.Trade_id
        port = obj.Port
        terminal = obj.Terminal
        tank = obj.Tank
        deliverymode = obj.Delivery_mode
        cargo = obj.Cargo
        density = obj.Density

        source_list = [tank, port, terminal]
        tank_updation_list = []



        print("tradeid", trade_id)

        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id)
        print("update_status_in_admin:", update_status_in_admin)
        print(update_status_in_admin.Status)
        update_status_in_admin.Status = "New"
        update_status_in_admin.save()
        obj.delete()

        if deliverymode == 'Tank':
            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, cargo, density)

        # update status in admin side :
        # copied code
        pb_volume_list = []
        admin_volume = GenerateTradeModel.objects.get(Trade_id=trade_id)
        print("tettesrt")
        print("admin volume:",admin_volume.Quantity)
        deal_volume = admin_volume.Quantity
        print("Deal volume:", deal_volume)


        pb_volume = PhysicalBlotterModel.objects.filter(Trade_id=trade_id)
        if pb_volume:
            print("work")
            print("pb_volume",pb_volume)
            # pb_volume_list.append(pb_volume.Quantity)
            for i in pb_volume:
                quantity = i.Quantity
                pb_volume_list.append(float(quantity))
            print("current volume:", pb_volume)

            print("pb_volume_list",pb_volume_list)
            pb_volume_sum = sum(pb_volume_list)

            print("pb_volume_sum",pb_volume_sum)
            print("end")

            deal_current_volume_update = float(deal_volume) - float(pb_volume_sum)
            print("deal_current_volume_update", deal_current_volume_update)

            if float(deal_volume) == float(pb_volume_sum):
                print("inside if ")
                GenerateTradeModel.objects.filter(Trade_id=trade_id).update(deal_current_qty=deal_current_volume_update,
                                                                            Status="Process", )
            else:
                print("hello elese")
                GenerateTradeModel.objects.filter(Trade_id=trade_id).update(deal_current_qty=deal_current_volume_update,
                                                                             Status="New",)
        else:
            pass

        return HttpResponseRedirect('/pb-list/')
        # return HttpResponse('deleted')


# update database physical blotter
def update_pb_database(request,*args,**kwargs):
    id = kwargs.get("id")
    print("ID OF MINE:",id)
    pb_values = PhysicalBlotterModel.objects.all()
    print("sb_values",pb_values)
    today_up = date.today()
    print("today_date in update:",today_up)

    for i in pb_values:
        print('iiiii',i)
        print("i.startdate",i.start_date)
        startdate_up = i.start_date
        print("startdate_up:",startdate_up)
        enddate_up = i.end_date
        print("enddate_up:", enddate_up)

        print("i.end_date", i.end_date)
        print("i.Holiday", i.Holiday)
        holiday_up = i.Holiday
        print("holiday_up:",holiday_up)
        volume = i.Quantity
        edit_trade_id=i.Trade_id
        print("Volume:",volume)

        pricing_methode= i.Pricing_method
        print("pricing_methode:", pricing_methode)



        print("************* Coversion from string to particular type")

        startdate_up = datetime.strptime(startdate_up, '%Y-%m-%d').date()
        print("converted start_date:", startdate_up)
        enddate_up = datetime.strptime(enddate_up, '%Y-%m-%d').date()
        print("converted end_date:", enddate_up)

        # date_ = datetime.strptime(date, '%Y-%m-%d').date()
        # print("converted date_:", date_)
        #
        # bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        # print("converted bl_date:", bl_date)
        print('****************************************')

        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday_up).values_list("date")
        holiday_date_df = pd.DataFrame(holiday_list_of_selected_holi,columns=['Dates'])
        holiday_date_df['Dates']= pd.to_datetime(holiday_date_df["Dates"])
        holiday_list_of_selected_holi=holiday_date_df['Dates'].to_list()

        print("new holiday list with only dates:",holiday_list_of_selected_holi,type(holiday_list_of_selected_holi))


        # holiday_list_of_selected_holi = str(holiday_list_of_selected_holi)
        # print("after string:, listt",holiday_list_of_selected_holi,type(holiday_list_of_selected_holi))
        # singapore_holiday = ['2023-01-30', '2023-01-09', '2023-01-29', '2023-02-01']

    #     print(":CALCULATING PRICED AND UNPRICED DAYS FOR UPDATING DATABASE1:")


        # workingdays
        workingdays = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
        workingdays = len(workingdays)
        print("working b4 overwrite 5:", workingdays)

        # <!----- priced and unpriced days start ----!>
        if today_up <= startdate_up:
            print("first condition priced days")
            priced_days= 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
            unpriced_days = len(unprice_calcu)
            print("unpriced in uodate:",unpriced_days)
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (today_up > startdate_up) and (today_up <= enddate_up):

            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=today_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi))

            workday = len(pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi))
            priced_days = workday - unpriced_days
            print("workday update:",workday)
            print("priced_days_up:",priced_days)
            print("unpriced_days update:", unpriced_days)
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        # elif (today > start_date_value) and (today<=end_date_value):

        elif (today_up > enddate_up):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=startdate_up, end=enddate_up, freq="C", holidays=holiday_list_of_selected_holi)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()

        else:
            pass
            # <!----- priced unpriced end ---!>
        print(":CALCULATING PRICED AND UNPRICED VOLUME FOR UPDATING DATABASE1:")
        # <!-----priced volume ----!>
        #    priced_volume_update = (priced_days_update / total_swaps_days_update) * volume_update
        #    priced_volume_update = round(priced_volume_update, 2)
        print("priced_days up:",priced_days, type(priced_days))
        print("working_days up:",workingdays,type(workingdays))
        print("Volume UP:",volume)

        priced_days = float(priced_days)
        print("float priced_days",priced_days)

        workingdays = float(workingdays)
        print("float priced_days", workingdays)

        print("error start")

        # priced_volume = (float(priced_days) / float(workingdays)) * float(volume)
        #
        # print("errror")
        #
        # print("priced volume up:", priced_volume)
        #
        # print("unpriced days",unpriced_days)
        #
        # unpriced_volume = (float(volume) / float(workingdays)) * float(unpriced_days)
        # print("hellllo")
        # priced_volume = round(priced_volume, 2)
        # unpriced_volume = round(unpriced_volume, 2)
        # print("priced volume up:", priced_volume)
        # print("Unpriced volume up:", unpriced_volume)
        # unpriced_volume = round(unpriced_volume, 2)
        # print("Unpriced volume round up:", unpriced_volume)

        pricing_methode = str(pricing_methode)

        if pricing_methode == "Fixed":
            print('hi')
            print("startdate:", startdate_up)
            print("enddate:", enddate_up)

            if startdate_up == enddate_up:
                total_volume = volume
                total_volume = round(volume, 3)
                print("totalk volume:",total_volume)
                priced_volume = total_volume
                unpriced_volume = 0
                print('+++++++++++++++++++++++++++++++++++++++++')
            else:
                pass
        elif pricing_methode == "Float":
            total_volume = volume
            priced_volume = (total_volume / workingdays) * priced_days
            priced_volume = round(priced_volume, 3)
            print("priced volume:", priced_volume)
            unpriced_volume = (total_volume / workingdays) * unpriced_days
            unpriced_volume = round(unpriced_volume, 3)
            print("unpriced_volume", unpriced_volume)
            print('+++++++++++++++++++++++++++++++++++++++++')


        ## TOTAL Volume
        total_volume = priced_volume + unpriced_volume
        print("TOTAL VOLUME: ", total_volume)
        total_volume = round(total_volume, 2)
        print("TOTAL VOLUME round: ", total_volume)
        # <!------priced volume end ---!>

        print("## ADDING PRICED/UNPRICED DAYS PRICED UNPRICED VOLUME TO DB AUTOMATICALLY ##")


        print("hello")

        all_swap_up = PhysicalBlotterModel.objects.all()
        # for i in all_swap_up:
        trade_id=i.Trade_id
        edit_start_date=i.start_date

        print(trade_id,'tarde_id')
        print("hello update swap")
        print("i.price_days",i.price_days)
        i.price_days = priced_days

        update_priced_days=i.price_days
        print("new priced up :", update_priced_days)
        print("i.unpriced:",i.unprice_days)
        i.unprice_days = unpriced_days
        update_unpriced_days=i.unprice_days
        print("new unprice up:", update_unpriced_days)
        #
        print("i.price_volume:", i.price_volume)
        i.priced_volume = priced_volume
        update_priced_volume=i.price_volume
        print("new priced volume up", i.price_volume)
        print("i.unprice_volume:", i.unprice_volume)
        i.unprice_volume = unpriced_volume
        update_unpriced_volume=i.unprice_volume
        print("new unpriced volume up")
        print("end update pb")
    #         # i.save()
        PhysicalBlotterModel.objects.filter(Trade_id=edit_trade_id,start_date=startdate_up,end_date=enddate_up,Quantity=volume).update(price_days=update_priced_days,unprice_days=update_unpriced_days,price_volume=update_priced_volume,unprice_volume=update_unpriced_volume,Total_no_days=workingdays)

        print("OUTSIDE LOOP SWAP")

    return HttpResponseRedirect("pb-list/")

    # update_status_in_admin.Status = "Discharged"
    # update_status_in_admin.save()

    # return render(request,"customer/sb.html")







# pb edit
class EditPhysicalBlotter(View):
    def get(self,request,**kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        print("obj.holiday",obj.Holiday)
        book = Book.objects.all()

        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:", holiday_distict)

        working_distinct_holiday = HolidayM.objects.order_by().values_list('name').distinct()
        print("working_distinct_holiday", working_distinct_holiday)

        unit = Unit1.objects.all()
        holiday = HolidayM.objects.all()
        print("holiday :", holiday)
        port = PortM.objects.all()
        terminal = TerminalM.objects.all()
        tank = TankCapacityM.objects.all()
        print("tank:", tank)
        # ntank = tank.name
        # print("new tank:",ntank)
        type = TYPEMODEL.objects.all()
        pricing_contract = ContractM.objects.all()
        data = FutureBlotterModel.objects.all()
        context = {'book': book, 'holiday': holiday, 'port': port,
                   'terminal': terminal, 'pricing_contract': pricing_contract,
                   'tank': tank, 'unit': unit,
                   'type': type, 'object_list': data, 'd': obj}
        print("context end:")
        return render(request, "customer/edit-physical-blotter.html", context)


    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")





    def post(self, request, *args, **kwargs):
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:",date)
        tradeid = request.POST.get('tradeid', '')
        trader = request.POST.get('trader', '')  # id
        print("trader:",trader)
        book = request.POST.get('book', '')  # id
        company_name = request.POST.get('company_name', '')
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        derivatives = request.POST.get('derivatives', '')
        print("derivatives:",derivatives)
        # buysell = request.POST.get('buysell', '')
        cargo = request.POST.get('cargo', '')
        pricing_contract = request.POST.get('pricing_contract','')
        pricing_methode = request.POST.get('pricing_methode', '')  # id
        print("pricing_methode:",pricing_methode)
        volume = request.POST.get('quantity', '')
        print("volume",volume)
        volume=float(volume)

        unit = request.POST.get('unit', '')
        print("Unit",unit)
        density = request.POST.get('density', '')
        nominated_quantity = request.POST.get('nominated_quantity', '')
        premium_discount = request.POST.get('premium_discount', '')
        pricing_term = request.POST.get('pricing_term', '')
        bl_date = request.POST.get('bl_date', '')
        print("BL date:",bl_date)
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        holiday = request.POST.get('holiday', '')
        print("holiday get:",holiday)
        deliverymode = request.POST.get('deliverymode', '')
        port = request.POST.get('port', '')
        print("port:",port)
        terminal = request.POST.get('terminal', '')
        vessal_name = request.POST.get('vessal_name', '')
        tank = request.POST.get('tank', '')
        print("Tank",tank)
        external_terminal = request.POST.get('external_terminal', '')
        print("external_terminal:",external_terminal)
        hedging = request.POST.get('hedging', '')
        print("hedging:", hedging)
        Remarks = request.POST.get('Remarks', '')
        print("Remarks:", Remarks)
        delete_feild = request.POST.get('delete_feild')
        print("over")


        ### newly added from dileena to conver to cubic meter
        if unit == 'MT':
            if float(density) < 1:
                m3 = round(float(volume) / float(density), 3)
            else:
                m3 = round((float(volume) / float(density)) / 1000, 3)
        elif unit == 'm³':
            m3 = round(float(volume) * 1, 3)

        elif unit == 'bbl':

            m3 = round(float((volume) / 6.289) / float(density), 3) if float(
                density) < 1 else round(float((volume) / 6.289) / (float(density) / 1000), 3)


        if volume>=0:
            buysell ="Buy"
        elif volume<=0:
            buysell="Sell"
        else:
            print("Invalid volume")


        print("************* Coversion from string to particular type")

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        print("converted start_date:", start_date)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        print("converted end_date:", end_date)

        date_ = datetime.strptime(date, '%Y-%m-%d').date()
        print("converted date_:", date_)

        bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        print("converted bl_date:", bl_date)
        print('****************************************')

        # HOLIDAY DATE LIST OF SELECTED HOLIDAY in DATAFRAME

        #   the working holiday list dates  using data frame
        print("Finding holiday:")
        print("Holioday selected", holiday)
        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        # workingdays
        holi_list_selcted = []
        for i in holiday_list_of_selected_holi:
            holi_list_selcted.append(i)
        print("new list of selected holi:", holi_list_selcted)

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holi_list_selcted, 'first++++++++total_swap_days')

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holi_list_selcted = holiday_date_df['Dates'].to_list()
        print(holiday_list, 'first++++++++total_swap_days')

        total_working_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holi_list_selcted))
        print(total_working_days, '++++++++total_swap_days')


        # <!----- priced and unpriced days start ----!>

        print("Priced unpriced starting")

        if date_ <= start_date:
            print("first condition priced days")
            priced_days = 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            unpriced_days = len(unprice_calcu)
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (date_ > start_date) and (date_ <= end_date):
            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=holi_list_selcted))

            workday = len(pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted))
            priced_days = workday - unpriced_days
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
        #
        elif (date_ > end_date):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        else:
            pass

        print("Priced unpriced end")
            # <!----- priced unpriced end ---!>

        # # <!-----priced volume ----!>

        print("Priced volume begining")

        print("pricing methode b4 price volume:",pricing_methode)

        pricing_methode = str(pricing_methode)
        unit = str(unit)

        if pricing_methode == "Fixed":
            print('hi')
            print("startdate:", start_date)
            print("enddate:", end_date)

            if start_date == end_date:
                total_volume = volume
                total_volume = round(volume, 3)
                priced_volume = total_volume
                unpriced_volume = 0
                # instance = form.save(commit=False)
                # instance.total_volume = total_volume
                # # instance.position = total_volume
                # instance.price_volume = priced_volume
                # instance.unprice_volume = unpriced_volume
                # instance.save()
                print('+++++++++++++++++++++++++++++++++++++++++')
            else:
                pass
        elif pricing_methode == "Float":
            print("hello float")
            total_volume = volume
            priced_volume = (total_volume / total_working_days) * priced_days
            priced_volume = round(priced_volume, 3)
            print("priced volume:", priced_volume)
            unpriced_volume = (total_volume / total_working_days) * unpriced_days
            unpriced_volume = round(unpriced_volume, 3)
            print("unpriced_volume", unpriced_volume)
            # instance = form.save(commit=False)
            # instance.total_volume = total_volume
            # # instance.position = total_volume
            # instance.price_volume = priced_volume
            # instance.unprice_volume = unpriced_volume
            # instance.save()
            print('+++++++++++++++++++++++++++++++++++++++++')




        PhysicalBlotterModel.objects.filter(Trade_id=tradeid).update(Pricing_contract_id=pricing_contract,
                                                                     Pricing_method=pricing_methode,
                                                                     Density=density,Quantity=volume,
                                                                     Nominated_quantity=nominated_quantity,
                                                                     Premium_discount=premium_discount,
                                                                     Pricing_term=pricing_term,
                                                                     bl_date=bl_date,
                                                                     start_date=start_date, end_date=end_date,
                                                                     Holiday=holiday,Delivery_mode=deliverymode,
                                                                     Port=port, Terminal=terminal,
                                                                     Vessal_name=vessal_name, Tank=tank,
                                                                     Remarks=Remarks,External_Terminal=external_terminal,Headging=hedging,
                                                                     # calculated and_ get_values
                                                                     price_days=priced_days, unprice_days=unpriced_days,
                                                                     Total_no_days=total_working_days,
                                                                     total_volume=total_volume,
                                                                     price_volume=priced_volume,
                                                                     unprice_volume=unpriced_volume,m3=m3,
                                                                     )


        print("object creation for pb")

        # update status in admin side :
        # copied code
        pb_volume_list = []
        admin_volume = GenerateTradeModel.objects.get(Trade_id=tradeid)
        print("tettesrt")
        print("admin volume:",admin_volume.Quantity)
        deal_volume = admin_volume.Quantity
        print("current volume:", deal_volume)

        pb_volume = PhysicalBlotterModel.objects.filter(Trade_id=tradeid)
        if pb_volume:
            print("work")
            print("pb_volume",pb_volume)
            # pb_volume_list.append(pb_volume.Quantity)
            for i in pb_volume:
                quantity = i.Quantity
                pb_volume_list.append(float(quantity))

            print("testt volumepb")

            print("current volume:", pb_volume)
            pb_volume_sum = sum(pb_volume_list)

            print("pb_volume_sum",pb_volume_sum)
            print("end")

            deal_current_volume_update = float(deal_volume) - float(pb_volume_sum)
            print("deal_current_volume_update", deal_current_volume_update)

            if float(deal_volume) == float(pb_volume_sum):
                print("inside if ")
                update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
                update_status_in_admin.Status = "Process"
                update_status_in_admin.deal_current_qty = deal_current_volume_update
                update_status_in_admin.save()
                print("after updating status:", update_status_in_admin.Status)
            else:
                print("hello elese")
                GenerateTradeModel.objects.filter(Trade_id=tradeid).update(deal_current_qty=deal_current_volume_update,
                                                                             Status="New",)
        else:
            pass

            # update tank code fxn call
        source_list = [tank, port, terminal]
        tank_updation_list = []

        if deliverymode == 'Tank':
            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, cargo, density)



        print(" updated Physical Blotter")
        messages.info(request, 'physical-blotter Trade Updated')
        return HttpResponseRedirect('/pb-list/')

# delete physical blotter

class DeletePhysicalBlotter(View):
    def get(self, request, *args, **kwargs):
        print("hello delete")
        return render(request, 'customer/delete-physical-blotter.html')
    def post(self, request, *args, **kwargs):
        print("Hi post")
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        trade_id = obj.Trade_id
        print("tradeid", trade_id)

        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id)
        print("update_status_in_admin:", update_status_in_admin)
        print(update_status_in_admin.Status)
        update_status_in_admin.Status = "New"
        update_status_in_admin.save()

        obj.delete()
        messages.info(request, 'Deleted Sucessfully')
        return HttpResponseRedirect('/pb-list/')


# def DeletePhysicalBlotter(request,*args,**kwargs):
#     id = kwargs.get("id")
#     invtrans= PhysicalBlotterModel.objects.get(id=id)
#     invtrans.delete()
#     messages.info(request,"invtrans  has been removed")
#     return HttpResponseRedirect('/future-blotter')


# Bill shore
class PB_BillShoreView(View):
    def get(self, request, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        book = Book.objects.all()


        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:",holiday_distict)

        working_distinct_holiday = HolidayM.objects.order_by().values_list('name').distinct()
        print("working_distinct_holiday",working_distinct_holiday)

        context = {
                   'd': obj,
        }
        print("context end:")
        return render(request, "customer/pb-billshore.html", context )



    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")





    def post(self, request, *args, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:", date)
        bldate = request.POST.get('bldate', '')
        purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
        print("purchase_sales_id:", purchase_sales_id)
        trade_id = request.POST.get('trade_id', '')  # id
        print("trade_id:", trade_id)
        product = request.POST.get('product', '')  # id
        pricing_contract = request.POST.get('pricing_contract', '')
        billed_quantity = request.POST.get('billed_quantity', '')
        print("billed_quantity:", billed_quantity)
        unit = request.POST.get('unit', '')
        print("unit:", unit)
        delivery_mode = request.POST.get('delivery_mode', '')
        print("delivery_mode:",delivery_mode)
        port = request.POST.get('port', '')
        terminal = request.POST.get('terminal', '')
        tank = request.POST.get('tank', '')  # id
        vessal_name = request.POST.get('vessal_name', '')
        shore_recieved = request.POST.get('shore_recieved', '')
        difference = request.POST.get('difference', '')
        terminal_cost = request.POST.get('terminal_cost', '')
        vessal_cost = request.POST.get('vessal_cost', '')
        freight_cost = request.POST.get('freight_cost', '')
        print("freight_cost:",freight_cost)

        density_uom = request.POST.get('density_uom', '')
        print("density_uom:", density_uom)



        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = PhysicalBlotterModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/pb-summary/")


        # additional_cost_type = request.POST.get('additional_cost_type', '')
        # print("additional_cost_type:",additional_cost_type)
        # total_secondary_cost = request.POST.get('total_secondary_cost', '')
        # print("total_secondary_cost:", total_secondary_cost)

        print("getting deal id ")

        # generate_trade = PhysicalBlotterModel.objects.filter(Purchase_sales_ID__icontains=purchase_sales_id)
        # print("generate_trade:",generate_trade)
        # admin_generate_trade_id = generate_trade.Trade_id
        # #
        # print("admin_generate_trade_id:",admin_generate_trade_id)
        # #
        # update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=admin_generate_trade_id)
        # update_status_in_admin.Status = "Discharged"
        # update_status_in_admin.save()

        generate_trade = PhysicalBlotterModel.objects.filter(Purchase_sales_ID=purchase_sales_id)
        print("generate_trade:",generate_trade)

        for i in generate_trade:
            print("i",i)
            print(i.Trade_id)
            trade_id_pb = i.Trade_id
            print("trade_id_pb:",trade_id_pb)


        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id_pb)
        print("update_status_in_admin:",update_status_in_admin)
        print(update_status_in_admin.Status)
        # update_status_in_admin.Status = "Discharged"
        update_status_in_admin.save()
        
        status = "Open"

        print("check what savedS")
        print("UPDATING ")
        PhysicalBlotterModel.objects.filter(Purchase_sales_ID=purchase_sales_id).update(Shore_recieved=shore_recieved,Difference=difference,Terminal_cost=terminal_cost,Vessal_cost=vessal_cost,
                                            Freight_cost=freight_cost,status=status,Density=density_uom,)



        # update tank code fxn call
        source_list = [tank, port, terminal]
        tank_updation_list = []

        if delivery_mode == 'Tank':
            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, product, density_uom)


        print(" saved BillShore")
        messages.info(request, 'BillShore Added')
        return HttpResponseRedirect('/pb-summary/')



# Edit Bill shore
class EditBillShore(View):
    def get(self, request, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        book = Book.objects.all()


        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:",holiday_distict)

        working_distinct_holiday = HolidayM.objects.order_by().values_list('name').distinct()
        print("working_distinct_holiday",working_distinct_holiday)

        context = {
                   'd': obj,
        }
        print("context end:")
        return render(request, "customer/edit-billshore.html", context )

    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")




    def post(self, request, *args, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:", date)
        bldate = request.POST.get('bldate', '')
        purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
        print("purchase_sales_id:", purchase_sales_id)
        product = request.POST.get('product', '')  # id
        pricing_contract = request.POST.get('pricing_contract', '')
        billed_quantity = request.POST.get('billed_quantity', '')
        print("billed_quantity:", billed_quantity)
        unit = request.POST.get('unit', '')
        print("unit:", unit)
        delivery_mode = request.POST.get('delivery_mode', '')
        print("delivery_mode:", delivery_mode)
        port = request.POST.get('port', '')
        terminal = request.POST.get('terminal', '')
        tank = request.POST.get('tank', '')  # id
        vessal_name = request.POST.get('vessal_name', '')
        shore_recieved = request.POST.get('shore_recieved', '')
        difference = request.POST.get('difference', '')
        terminal_cost = request.POST.get('terminal_cost', '')
        vessal_cost = request.POST.get('vessal_cost', '')
        freight_cost = request.POST.get('freight_cost', '')
        density_uom = request.POST.get('density_uom', '')

        print("freight_cost:", freight_cost)

        print("getting deal id ")
        generate_trade = PhysicalBlotterModel.objects.filter(Purchase_sales_ID=purchase_sales_id)
        print("generate_trade:", generate_trade)

        for i in generate_trade:
            print("i", i)
            print(i.Trade_id)
            trade_id_pb = i.Trade_id
            print("trade_id_pb:", trade_id_pb)

        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id_pb)
        print("update_status_in_admin:", update_status_in_admin)
        print(update_status_in_admin.Status)
        update_status_in_admin.Status = "Discharged"
        update_status_in_admin.save()

        status = "Open"

        print("check what savedS")
        print("UPDATING ")
        PhysicalBlotterModel.objects.filter(Purchase_sales_ID=purchase_sales_id).update(Shore_recieved=shore_recieved,
                                                                                        Difference=difference,
                                                                                        Terminal_cost=terminal_cost,
                                                                                        Vessal_cost=vessal_cost,
                                                                                        Freight_cost=freight_cost,
                                                                                        status=status,density_uom=density_uom)

        # update tank code fxn call
        source_list = [tank, port, terminal]
        tank_updation_list = []

        if delivery_mode == 'Tank':
            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, product, density_uom)

        print("BillShore updated")
        messages.info(request, 'BillShore Updated')
        return HttpResponseRedirect('/pb-summary/')



# Delete bill shore
class DeleteBillShore(View):
    def get(self, request, *args, **kwargs):
        print("hello delete")
        return render(request, 'customer/delete-bill-shore.html')
    def post(self, request, *args, **kwargs):
        print("Hi post")
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        trade_id = obj.Trade_id
        print("tradeid",trade_id)

        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id)
        print("update_status_in_admin:", update_status_in_admin)
        print(update_status_in_admin.Status)
        update_status_in_admin.Status = "New"
        update_status_in_admin.save()

        obj.delete()
        messages.info(request, 'Deleted Successfully')
        return HttpResponseRedirect('/pb-summary/')





# billshore pb summary
class PbSummaryView(View):
    # def get(self,request,*args,**kwargs):
    #     qs = PhysicalBlotterModel.objects.order_by('-Date')
    #     print("pb_summary:",qs)
    #     return render(request,"customer/pb-summary.html",{"pb_summary":qs})
    def get(self, request, *args, **kwargs):

        pb_trade_id = []
        pb_purchase_sales_id = []
        pb_container = []
        pb_port = []
        pb_terminal = []
        pb_vessel = []
        pb_shore_received_qty = []
        pb_loss_gain = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_Strategy = []
        pb_density = []
        pb_book = []
        pb_book = []

        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').order_by('-Date')

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_trade_id.append(pbx.Trade_id)
            pb_purchase_sales_id.append(pbx.Purchase_sales_ID)
            pb_book.append(pbx.Book)
            pb_Strategy.append(pbx.Strategy)
            pb_container.append(pbx.Delivery_mode)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_vessel.append(pbx.Vessal_name)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_loss_gain.append(pbx.Difference)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)

        pb_dict = {'Status': pb_status, 'Trade_id': pb_trade_id, 'Purchase_Sales_id': pb_purchase_sales_id,
                   'Book': pb_book, 'Strategy': pb_Strategy, 'Delivery_mode': pb_container,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Vessal': pb_vessel, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Gain_Loss': pb_loss_gain, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density}

        discharged_df = pd.DataFrame(pb_dict)
        discharged_df['Vessel_Tank'] = np.where(discharged_df['Delivery_mode'] == 'Vessel', discharged_df['Vessal'],
                                                discharged_df['Tank'])
        print(discharged_df, 'discharged_dfnewcol')

        agg = {
            'Status': 'last', 'Purchase_Sales_id': 'last',
            'Book': 'last', 'Strategy': 'last', 'Delivery_mode': 'last',
            'Vessal': 'last', 'Tank': 'last',
            'Shore_received': 'sum', 'Gain_Loss': 'sum', 'Cargo': 'last',
            'Unit': 'last', 'Density': 'last'
        }
        trade_current_qty = discharged_df.groupby(['Trade_id', 'Port', 'Terminal', 'Vessel_Tank']).agg(
            agg).reset_index()
        print(trade_current_qty, 'trade_current_qty')

        inv_trade_id = []
        inv_purchase_sales_id = []
        inv_distribution_type = []
        inv_strategy = []
        inv_delivery_mode = []
        inv_tank = []
        inv_vessel = []
        inv_port = []
        inv_terminal = []
        inv_unit = []
        inv_density = []
        inv_current_qty = []
        inv_dest_difference = []
        inv_cargo = []

        transferred_cargo = InventoryModel.objects.order_by('-date')
        for invx in transferred_cargo:
            inv_trade_id.append(invx.Trade_id)
            inv_purchase_sales_id.append(invx.Purchase_sales_ID)
            inv_distribution_type.append(invx.Distribution_Type)
            inv_strategy.append(invx.Strategy)
            inv_delivery_mode.append(invx.Delivery_mode)
            inv_tank.append(invx.Tank)
            inv_vessel.append(invx.Vessal_name)
            inv_port.append(invx.Port)
            inv_terminal.append(invx.Terminal)
            inv_unit.append(invx.Unit)
            inv_density.append(invx.Density)
            inv_current_qty.append(invx.source_cargo_LD_QTY)
            inv_cargo.append(invx.Cargo)
            inv_dest_difference.append(invx.dest_difference)

        inv_dict = {'Trade_id': inv_trade_id, 'Purchase_Sales_id': inv_purchase_sales_id,
                    'Strategy': inv_strategy, 'Delivery_mode': inv_delivery_mode,
                    'Port': inv_port, 'Terminal': inv_terminal, 'Vessal': inv_vessel, 'Tank': inv_tank,
                    'Shore_received': inv_current_qty, 'Gain_Loss': inv_dest_difference, 'Cargo': inv_cargo,
                    'Unit': inv_unit, 'Density': inv_density}

        inventory_df = pd.DataFrame(inv_dict)
        inventory_df['Vessel_Tank'] = np.where(inventory_df['Delivery_mode'] == 'Vessel', inventory_df['Vessal'],
                                               inventory_df['Tank'])
        agg = {
            'Purchase_Sales_id': 'last',
            'Strategy': 'last', 'Delivery_mode': 'last',
            'Vessal': 'last', 'Tank': 'last',
            'Shore_received': 'sum', 'Gain_Loss': 'sum', 'Cargo': 'last',
            'Unit': 'last', 'Density': 'last'
        }

        inventory_df = inventory_df.groupby(['Trade_id', 'Port', 'Terminal', 'Vessel_Tank']).agg(
            agg).reset_index()
        print(inventory_df, 'invtrade_current_qty')

        merged_inv_pb_df = pd.merge(trade_current_qty, inventory_df, how='outer')
        agg = {

            'Shore_received': 'sum', 'Gain_Loss': 'sum'}

        total_qty = merged_inv_pb_df.groupby(['Purchase_Sales_id', 'Port', 'Terminal', 'Vessel_Tank']).agg(
            agg).reset_index()

        total_qty.rename(columns={"Shore_received": "Instock", "Gain_Loss": "Total_Gain_Loss"},
                         inplace=True)
        print(total_qty, 'total_qty___')

        final_discharged_cargo = pd.merge(trade_current_qty, total_qty, how='left',
                                          on=['Purchase_Sales_id', 'Port', 'Terminal', 'Vessel_Tank'])
        print(final_discharged_cargo, 'final_discharged_cargogreater than 0')
        final_discharged_cargo = final_discharged_cargo[final_discharged_cargo["Instock"] > 0]

        instock_list = final_discharged_cargo['Instock'].to_list()

        purchase_sales_id = final_discharged_cargo['Purchase_Sales_id'].to_list()

        print('purchase_sales_idlist', purchase_sales_id)

        for i in purchase_sales_id:
            current_quantity_update = final_discharged_cargo[final_discharged_cargo["Purchase_Sales_id"] == i]
            current_quantity_update = current_quantity_update['Instock'].iloc[0]

            discharged_cargo = PhysicalBlotterModel.objects.filter(Purchase_sales_ID=i)

            for ds in discharged_cargo:
                ds.current_qty = current_quantity_update
                ds.save()

        discharged_details = PhysicalBlotterModel.objects.filter(Purchase_sales_ID__in=purchase_sales_id)
        #
        print('+++++++++++++++++++Updating Disched Cargo based on Transfer+++++++++++++++++++++++',
              final_discharged_cargo)

        return render(request, "customer/pb-summary.html", {"pb_summary": discharged_details})

    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")

    def post(self, request):
        id = self.request.POST.get('delete_feild')
        obj = PhysicalBlotterModel.objects.get(id=id)

        trade_id = obj.Trade_id
        tank = obj.Tank
        port = obj.Port
        terminal = obj.Terminal
        delivery_mode = obj.Delivery_mode
        product =obj.Cargo
        density_uom= obj.Density

        print("tradeid", trade_id)

        update_status_in_admin = GenerateTradeModel.objects.get(Trade_id=trade_id)
        print("update_status_in_admin:", update_status_in_admin)
        print(update_status_in_admin.Status)
        update_status_in_admin.Status = "New"
        update_status_in_admin.save()
        obj.delete()

        # update tank code fxn call
        source_list = [tank, port, terminal]
        tank_updation_list = []

        if delivery_mode == 'Tank':
            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, product, density_uom)





        return HttpResponseRedirect('/pb-summary/')

# class PbSummaryView(ListView):
#     template_name = "customer/pb-summary.html"
#     model = PhysicalBlotterModel
#     context_object_name = 'pb_summary'


# class InventoryListView(ListView):
#     template_name = "customer/inv-listview.html"
#     model = InventoryModel
#     context_object_name = 'inv_list'

 #Inventory listview
# class InventoryListView(View):
#     def get(self,request,*args,**kwargs):
#         qs = InventoryModel.objects.all()
#         print("pb_summary:",qs)
#         return render(request,"customer/inv-listview.html",{"inv_list":qs})
#
#     def post(self, request):
#         print("b4")
#         id = self.request.POST.get('delete_feild')
#         print("id:",id)
#         obj = InventoryModel.objects.get(id=id)
#         obj.delete()
#         return HttpResponseRedirect('/inventory-list/')


class InventoryListView(View):

    def get(self,request,*args,**kwargs):
        qs = InventoryModel.objects.all()
        return render(request,"customer/inv-listview.html",{"inv_list":qs})



    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                        (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                        tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                           Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                           Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")


    # def post(self, request,**kwargs):
    #     print("b4")
    #     id = self.request.POST.get('delete_feild')
    #     print("id:",id)
    #     obj = InventoryModel.objects.get(id=id)
    #
    #     if obj.duplicate_id == 'none':
    #         obj.delete()
    #
    #     else:
    #
    #         obj = InventoryModel.objects.get(id=id)
    #
    #         obj2 = InventoryModel.objects.filter(duplicate_id=obj.duplicate_id)
    #         for i in obj2:
    #             obj1 = InventoryModel.objects.get(id=i.id)
    #             obj1.delete()
    #
    #     messages.info(request, 'Deleted')
    #     return HttpResponseRedirect('/inventory-list/')

    def post(self, request, **kwargs):
        print("b4")
        id = self.request.POST.get('delete_feild')
        print("id:", id)
        obj = InventoryModel.objects.get(id=id)

        if obj.duplicate_id == 'none':
            obj.delete()

        else:
            obj = InventoryModel.objects.get(id=id)

            obj2 = InventoryModel.objects.filter(duplicate_id=obj.duplicate_id)
            for i in obj2:
                obj1 = InventoryModel.objects.get(id=i.id)
                tank_updation_list = []
                cargo = obj1.Cargo
                density = obj1.Density
                Delivery_mode = obj1.Delivery_mode

                source_list = [obj1.Tank, obj1.Port, obj1.Terminal]
                obj1.delete()

                if Delivery_mode == 'Tank' or Delivery_mode == 'PLT':
                    tank_updation_list.append(source_list)
                    print('second______', tank_updation_list)
                    print('m3=m3,Density=density_uom,', tank_updation_list)

                    self.tank_update(request, tank_updation_list, cargo, density)

        messages.info(request, 'Deleted')
        return HttpResponseRedirect('/inventory-list/')



class InventoryManagementView(View):

    def get(self, request, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])

        port = PortM.objects.all()
        print("port :", port)
        terminal = TerminalM.objects.all()
        print("terminal :", terminal)
        tank = TankCapacityM.objects.all()
        unit = Unit1.objects.all()

        tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
        print("tank_distinct:",tank_distinct)

        print("Tank no:",tank)
        context = {
            'd': obj,'port':port,'terminal':terminal,'tank':tank,'unit':unit,
        }
        print("context end:")
        return render(request, "customer/inventory-management.html", context )

    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                        (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                        tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                           Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                           Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")



    # def post(self, request, *args, **kwargs):
    #     print("hello")
    #     obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
    #     quantity = obj.Quantity
    #     print("quantity",quantity)
    #     #From
    #     print(" post methode:")
    #     date = request.POST.get('date', '')
    #     print("date:", date)
    #     trade_id = request.POST.get('trade_id', '')
    #     purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
    #     print("purchase_sales_id:", purchase_sales_id)
    #     distribution_type = request.POST.get('distribution_type', '')  # id
    #     deliverymode = request.POST.get('deliverymode', '')
    #     tank = request.POST.get('tank', '')
    #     print("tank:", tank)
    #     strategy = request.POST.get('strategy', '')
    #     print("strategy:", strategy)
    #     vesselname = request.POST.get('vesselname', '')
    #     print("vesselname:",vesselname)
    #     port = request.POST.get('port', '')
    #     terminal = request.POST.get('terminal', '')
    #     cargo = request.POST.get('cargo', '')  # id
    #     instock_shore_recieved = request.POST.get('shore_recieved', '')
    #     density = request.POST.get('density', '')
    #     unit = request.POST.get('unit', '')
    #     book = request.POST.get('book', '')
    #     print("book:",book)
    #
    #     # To
    #     print("To Get")
    #     dest_container_to = request.POST.get('dest_container_to', '')
    #     port_to = request.POST.get('port_to', '')
    #     terminal_to = request.POST.get('terminal_to', '')
    #     tankno_to = request.POST.get('tankno_to', '')
    #     vessalname_to = request.POST.get('vessalname_to', '')
    #     inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
    #     unit_to = request.POST.get('unit_to', '')
    #     dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
    #     dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
    #     temperature = request.POST.get('temperature', '')
    #
    #     delete_feild = request.POST.get('delete_feild')
    #     if delete_feild:
    #         obj = InventoryModel.objects.get(id=delete_feild)
    #         obj.delete()
    #         return HttpResponseRedirect("/inventory-list/")
    #
    #     #conversion
    #     dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
    #     dest_received_qty_to = float(dest_received_qty_to)
    #     if tankno_to:
    #         tankno_to = tankno_to
    #     else:
    #         pass
    #     print("retrieved")
    #     print("dest_received_qty_to:",dest_received_qty_to)
    #
    #     dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)
    #     print("swapLD QTY:", dest_cargo_LD_QTY_to)
    #     source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
    #     print("source_cargo_ld_qty:", source_cargo_ld_qty)
    #
    #     dest_diff = float(dest_cargo_LD_QTY_to) - float(dest_received_qty_to)
    #     print("dest_difference:", dest_diff)
    #
    #     # updating tank capacity model
    #     print("****** UPDATING TANK CAPACITY MODEL ******")
    #
    #
    #     print("Tank no:",tankno_to)
    #     tank_detail = TankCapacityM.objects.filter(Tank_no__name=tankno_to)
    #     print("Tank detail:",tank_detail)
    #
    #
    #
    #     for i in tank_detail:
    #         print(i, 'i insde')
    #         print("###### THE START tank ############")
    #         safe_fill_capacity = i.Safe_fill_capacity
    #         remaining_space = float(safe_fill_capacity) - float(dest_received_qty_to)
    #         print(safe_fill_capacity, 'safe_fill:', remaining_space, 'safe_fill:')
    #         print("Hello updates")
    #         TankCapacityM.objects.filter(Tank_no__name=tankno_to).update(current_quantity=dest_received_qty_to,
    #                                     Remaining_space=remaining_space)
    #
    #         print("updated")
    #
    #
    #
    #
    #     print("object creation for pb")
    #     obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id, Distribution_Type=distribution_type,
    #                              Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
    #                              Vessal_name=vesselname,
    #                              Port=port, Terminal=terminal,Cargo=cargo, Unit=unit,
    #                              Shore_recieved=instock_shore_recieved, Density=density,
    #                          #to
    #                              dest_container=dest_container_to, dest_port=port_to,
    #                              dest_terminal=terminal_to,dest_vessal_op=vessalname_to,
    #                              dest_tank_num=tankno_to,book=book,
    #                              inv_transfer_mode=inv_transfer_mode_to, dest_unit=unit_to,
    #                              dest_cargo_LD_QTY=dest_cargo_LD_QTY_to, dest_received_qty=dest_received_qty_to,
    #                              temperature=temperature,
    #
    #                          # calculated values
    #                              source_cargo_LD_QTY=source_cargo_ld_qty, dest_difference=dest_diff,
    #
    #                              )
    #     obj.save()
    #     print(" saved pb")
    #     messages.info(request, 'Inventory Saved')
    #     return HttpResponseRedirect('/inventory-list/')

    def post(self, request, *args, **kwargs):

        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        quantity = obj.Quantity
        # From

        date = request.POST.get('date', '')
        trade_id = request.POST.get('trade_id', '')
        purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
        distribution_type = request.POST.get('distribution_type', '')  # id
        deliverymode = request.POST.get('deliverymode', '')
        source_container = deliverymode
        tank = request.POST.get('tank', '')
        print("tank:", tank)
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        vesselname = request.POST.get('vesselname', '')
        print("vesselname:", vesselname)
        port = request.POST.get('port', '')
        terminal = request.POST.get('terminal', '')
        cargo = request.POST.get('cargo', '')  # id
        instock_shore_recieved = request.POST.get('shore_recieved', '')
        instock = instock_shore_recieved
        print("instock:",instock)
        density = request.POST.get('density', '')
        unit = request.POST.get('unit', '')
        book = request.POST.get('book', '')

        density = float(density)
        instock = float(instock)

        #
        if float(instock) <= 0:
            print('Cannot transfer cargo having quatity less than 0')
            messages.error(request, 'Cannot transfer cargo having quatity less than 0')
            raise

        # To
        print("To Get")
        dest_container_to = request.POST.get('dest_container_to', '')
        port_to = request.POST.get('port_to', '')
        terminal_to = request.POST.get('terminal_to', '')
        tankno_to = request.POST.get('tankno_to', '')
        vessalname_to = request.POST.get('vessalname_to', '')
        inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
        unit_to = request.POST.get('unit_to', '')
        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
        temperature = request.POST.get('temperature', '')

        if float(dest_cargo_LD_QTY_to) <= 0 or float(dest_received_qty_to) <= 0:
            print('Cannot transfer cargo having quatity less than 0')
            messages.error(request, 'Cannot transfer cargo having quatity less than 0')
            raise

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = InventoryModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
        dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)

        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
        dest_received_qty_to = float(dest_received_qty_to)
        dest_received_qty_to = abs(dest_received_qty_to)
        source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

        print("till here")

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':
            if (str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(tank) == str(tankno_to)):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                messages.error(request, 'Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        elif dest_container_to == 'Vessel':
            if str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(vesselname) == str(
                    vessalname_to):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                messages.error(request, 'Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        if unit == 'MT':

            instock_m3 = round(float(instock) / float(density), 3) if float(
                density) < 1 else round(float(instock) / (float(density) / 1000), 3)

            if unit_to == 'MT':

                # In MT
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
                # Convert MT to m3 equ: MT/Density if Density less than 0 else MT/(Density/1000)
                dest_received_qty_to_m3 = round(float(dest_received_qty_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float(dest_cargo_LD_QTY_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                # Convert   m3 to MT equ: MT*Density if Density less than 0 else MT*(Density/1000)

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'bbl':
            print("unit=bbl")

            instock_m3 = round(float((instock) / 6.289) / float(density), 3) if float(
                density) < 1 else round(float((instock) / 6.289) / (float(density) / 1000), 3)

            if unit_to == 'bbl':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

                # Convert bbl to m3 equ: (bbl/6.289)/Density if Density less than 0 else bbl/6.289/(Density/1000)

                dest_received_qty_to_m3 = round(float((dest_received_qty_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float((dest_cargo_LD_QTY_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'm3':

            dest_received_qty_to_m3 = dest_received_qty_to
            source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)
            instock_m3 = float(instock)

            if unit_to == 'm3':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(abs(dest_cargo_LD_QTY_to))

            elif unit_to == 'MT':

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

            elif unit_to == 'bbl':

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        dest_diff = abs(float(dest_received_qty_to)) - abs(float(source_cargo_ld_qty))

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = InventoryModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':

            tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tankno_to)).filter(Port__name=port_to).filter(
                Terminal__name=terminal_to)
            for i in tank_capacity:
                safe_fill_capacity = i.Safe_fill_capacity
                remaining_space = i.Remaining_space

            if abs(float(source_cargo_ld_qty_m3)) > float(remaining_space):
                print('remaining_space', remaining_space)
                print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
                print('This much quatity cannot accpmodate in this tank')
                messages.error(request,'This much quatity cannot accpmodate in this tank')

                raise

        if abs(float(source_cargo_ld_qty_m3)) > (float(instock_m3)):
            print('Instockm3', instock_m3)
            print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
            print('quantity trying to transfer is greater than instock')
            messages.error(request, 'quantity trying to transfer is greater than instock')
            raise
        else:
            print('Instockm3', instock_m3)
            print('Transferm3', source_cargo_ld_qty_m3)

        print("object creation for pb")

        # NEED SAME ID(Reference id)
        source_list = [tank, port, terminal]
        dest_list = [tankno_to, port_to, terminal_to]
        print(source_list, 'source_list')
        print(dest_list, 'dest_list')
        print(dest_container_to, 'dest_container_to')
        print(source_container, 'source_container')

        obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                             Distribution_Type=distribution_type,
                             Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
                             Vessal_name=vesselname,
                             Port=port, Terminal=terminal, Cargo=cargo, Unit=unit, dest_unit=unit_to,
                             Density=density, dest_cargo_LD_QTY=0,
                             inv_transfer_mode=inv_transfer_mode_to, dest_difference=0,
                             dest_received_qty=0, source_cargo_LD_QTY=source_cargo_ld_qty, m3=source_cargo_ld_qty_m3,
                             # Not Required Field
                             dest_container=dest_container_to, dest_port=port_to,
                             dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                             dest_tank_num=tankno_to,

                             )

        obj.save()
        obj.duplicate_id = obj.id
        obj.save()

        obj1 = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                              Distribution_Type=distribution_type,
                              Delivery_mode=dest_container_to, Tank=tankno_to, Strategy=strategy,
                              Vessal_name=vessalname_to,
                              Port=port_to, Terminal=terminal_to, Cargo=cargo, Unit=unit,
                              Density=density, dest_unit=unit_to,
                              inv_transfer_mode=inv_transfer_mode_to, dest_difference=dest_diff,
                              dest_received_qty=dest_received_qty_to,
                              source_cargo_LD_QTY=dest_received_qty_to, m3=dest_received_qty_to_m3,
                              Shore_recieved=dest_cargo_LD_QTY_to,
                              # Not Required Field
                              dest_cargo_LD_QTY=0,
                              dest_container=dest_container_to, dest_port=port_to,
                              dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                              dest_tank_num=tankno_to, duplicate_id=obj.id

                              )

        obj1.save()

        tank_updation_list = []

        if dest_container_to == 'Tank' or source_container == 'Tank' or dest_container_to == 'PLT' or source_container == 'PLT':
            print('+++++++++++++++++')

            if (dest_container_to == 'Tank' or dest_container_to == 'PLT') and (
                    source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                tank_updation_list.append(dest_list)
                print('first______', tank_updation_list)

            elif (dest_container_to == 'Tank' or dest_container_to == 'PLT') and source_container != 'Tank':
                tank_updation_list.append(dest_list)
                print('second______', tank_updation_list)
            elif dest_container_to != 'Tank' and (source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                print('third_____', tank_updation_list)

            print('m3=m3,Density=density_uom,', tank_updation_list)

            self.tank_update(request, tank_updation_list, cargo, density)

        messages.info(request, 'Inventory Saved')
        return HttpResponseRedirect('/inventory-list/')





# chained dropdown

def tank_port_terminal_relation_INV(request):
    print("Hi Port")
    if request.method == "POST":
        print("Hello Post methode")
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        port_name = data_dict.get('port_name')
        print("Port name:",port_name)
        obj = TankCapacityM.objects.filter(Port__name=port_name)
        print("obj:",obj)
        for data in obj:
            print("checking:",data.product_status)
            print("checking:", data.Terminal.name)
            print("checking:", data.Tank_no.name)

        data = [{'date': data.Terminal.name} for data in obj]
        data1 = [{'data': i.Tank_no.name} for i in obj]

        print("data:",data)
        uniq_data = []
        for x in data:
            if x not in uniq_data:
                uniq_data.append(x)
        print("uniq data:", uniq_data)
        print("data1:", data1)
        uniq_data1 = []
        for x in data1:
            if x not in uniq_data1:
                uniq_data1.append(x)
        print("uniq data1:", uniq_data1)

        print(data1)
        print('ddd')
    return JsonResponse({'data':uniq_data, 'data1':uniq_data1}, safe=False)





# Edit Inventory
class EditInventory(View):
    def get(self, request, **kwargs):
        obj = InventoryModel.objects.get(id=kwargs['id'])

        port = PortM.objects.all()
        print("port :", port)
        terminal = TerminalM.objects.all()
        print("terminal :", terminal)
        tank = TankCapacityM.objects.all()

        tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
        print("tank_distinct:",tank_distinct)

        print("Tank no:",tank)
        context = {
            'd': obj,'port':port,'terminal':terminal,'tank':tank,
        }
        print("context end:")
        return render(request, "customer/edit-inventory.html", context )


    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                        (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                        tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                           Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                           Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")


    # def post(self, request, *args, **kwargs):
    #     obj = InventoryModel.objects.get(id=kwargs['id'])
    #
    #     # From
    #     print(" post methode:")
    #     date = request.POST.get('date', '')
    #     print("date:", date)
    #     trade_id = request.POST.get('trade_id', '')
    #     purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
    #     print("purchase_sales_id:", purchase_sales_id)
    #     distribution_type = request.POST.get('distribution_type', '')  # id
    #     deliverymode = request.POST.get('deliverymode', '')
    #     tank = request.POST.get('tank', '')
    #     print("tank:", tank)
    #     strategy = request.POST.get('strategy', '')
    #     print("strategy:", strategy)
    #     vesselname = request.POST.get('vesselname', '')
    #     print("vesselname:", vesselname)
    #     port = request.POST.get('port', '')
    #     terminal = request.POST.get('terminal', '')
    #     cargo = request.POST.get('cargo', '')  # id
    #     instock_shore_recieved = request.POST.get('shore_recieved', '')
    #     density = request.POST.get('density', '')
    #     unit = request.POST.get('unit', '')
    #
    #     # To
    #     print("To Get")
    #     dest_container_to = request.POST.get('dest_container_to', '')
    #     port_to = request.POST.get('port_to', '')
    #     terminal_to = request.POST.get('terminal_to', '')
    #     tankno_to = request.POST.get('tankno_to', '')
    #     print("tankno_to:",tankno_to)
    #     vessalname_to = request.POST.get('vessalname_to', '')
    #     inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
    #     unit_to = request.POST.get('unit_to', '')
    #     dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
    #     dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
    #
    #     # conversion
    #     dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
    #     dest_received_qty_to = float(dest_received_qty_to)
    #     tankno_to =tankno_to
    #
    #     # if tankno_to is None:
    #     #     pass
    #     # else:
    #     #     tankno_to = int(tankno_to)
    #     #     pass
    #
    #     print("retrieved")
    #     print("dest_received_qty_to:", dest_received_qty_to)
    #
    #     dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)
    #     print("swapLD QTY:", dest_cargo_LD_QTY_to)
    #     source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
    #     print("source_cargo_ld_qty:", source_cargo_ld_qty)
    #
    #     dest_diff = float(dest_cargo_LD_QTY_to) - float(dest_received_qty_to)
    #     print("dest_difference:", dest_diff)
    #
    #     # updating tank capacity model
    #     print("****** UPDATING TANK CAPACITY MODEL ******")
    #
    #     print("Tank no:", tankno_to)
    #     tank_detail = TankCapacityM.objects.filter(Tank_no__name=tankno_to)
    #     print("Tank detail:", tank_detail)
    #
    #     for i in tank_detail:
    #         print(i, 'i insde')
    #         print("###### THE START tank ############")
    #         safe_fill_capacity = i.Safe_fill_capacity
    #         remaining_space = float(safe_fill_capacity) - float(dest_received_qty_to)
    #         print(safe_fill_capacity, 'safe_fill:', remaining_space, 'safe_fill:')
    #         print("Hello updates")
    #         TankCapacityM.objects.filter(Tank_no__name=tankno_to).update(current_quantity=dest_received_qty_to,
    #                                                                      Remaining_space=remaining_space)
    #
    #         print("updated")
    #
    #
    #
    #     InventoryModel.objects.filter(Purchase_sales_ID=purchase_sales_id).update(dest_container=dest_container_to, dest_port=port_to,
    #                                                                               dest_terminal=terminal_to,
    #                                                                               dest_vessal_op=vessalname_to,
    #                                                                               dest_tank_num=tankno_to,
    #                                                                               inv_transfer_mode=inv_transfer_mode_to,
    #                                                                               dest_unit=unit_to,
    #                                                                               dest_cargo_LD_QTY=dest_cargo_LD_QTY_to,
    #                                                                               dest_received_qty=dest_received_qty_to,
    #                                                                               # calculated values
    #                                                                               source_cargo_LD_QTY=source_cargo_ld_qty,
    #                                                                               dest_difference=dest_diff,
    #
    #
    #                                                                               )
    #
    #     print("object creation for pb")
    #     # obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id, Distribution_Type=distribution_type,
    #     #                          Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
    #     #                          Vessal_name=vesselname,
    #     #                          Port=port, Terminal=terminal,Cargo=cargo, Unit=unit,
    #     #                          Shore_recieved=instock_shore_recieved, Density=density,
    #     #                      #to
    #     #                          dest_container=dest_container_to, dest_port=port_to,
    #     #                          dest_terminal=terminal_to,dest_vessal_op=vessalname_to,
    #     #                          dest_tank_num=tankno_to,
    #     #                          inv_transfer_mode=inv_transfer_mode_to, dest_unit=unit_to,
    #     #                          dest_cargo_LD_QTY=dest_cargo_LD_QTY_to, dest_received_qty=dest_received_qty_to,
    #     #                      # calculated values
    #     #                          source_cargo_LD_QTY=source_cargo_ld_qty, dest_difference=dest_diff,
    #     #
    #     #                          )
    #     # obj.save()
    #     print(" saved pb")
    #     messages.info(request, 'Inventory Updated')
    #     return HttpResponseRedirect('/inventory-list/')

    def post(self, request, *args, **kwargs):
        obj = InventoryModel.objects.get(id=kwargs['id'])

        # From
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:", date)
        trade_id = request.POST.get('trade_id', '')
        purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
        print("purchase_sales_id:", purchase_sales_id)
        distribution_type = request.POST.get('distribution_type', '')  # id
        deliverymode = request.POST.get('deliverymode', '')
        source_container = deliverymode
        tank = request.POST.get('tank', '')
        print("tank:", tank)
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        vesselname = request.POST.get('vesselname', '')
        print("vesselname:", vesselname)
        port = request.POST.get('port', '')
        terminal = request.POST.get('terminal', '')
        cargo = request.POST.get('cargo', '')  # id
        instock_shore_recieved = request.POST.get('shore_recieved', '')
        instock = float(instock_shore_recieved)
        density = request.POST.get('density', '')
        unit = request.POST.get('unit', '')

        # To
        print("To Get")
        dest_container_to = request.POST.get('dest_container_to', '')
        port_to = request.POST.get('port_to', '')
        terminal_to = request.POST.get('terminal_to', '')
        tankno_to = request.POST.get('tankno_to', '')
        print("tankno_to:", tankno_to)
        vessalname_to = request.POST.get('vessalname_to', '')
        inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
        unit_to = request.POST.get('unit_to', '')
        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')

        if float(instock) < 0:
            print('Cannot transfer cargo having quatity less than 0')
            messages.error(request, 'Cannot transfer cargo having quatity less than 0')
            raise

        if float(dest_cargo_LD_QTY_to) < 0 or float(dest_received_qty_to) < 0:
            print('Cannot transfer cargo having quatity less than 0')
            messages.error(request, 'Cannot transfer cargo having quatity less than 0')

            raise

        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
        dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)

        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
        dest_received_qty_to = float(dest_received_qty_to)
        dest_received_qty_to = abs(dest_received_qty_to)
        source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':
            if (str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(tank) == str(tankno_to)):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        elif dest_container_to == 'Vessel':
            if str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(vesselname) == str(
                    vessalname_to):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        if unit == 'MT':

            instock_m3 = round(float(instock) / float(density), 3) if float(
                density) < 1 else round(float(instock) / (float(density) / 1000), 3)

            if unit_to == 'MT':

                # In MT
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
                # Convert MT to m3 equ: MT/Density if Density less than 0 else MT/(Density/1000)
                dest_received_qty_to_m3 = round(float(dest_received_qty_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float(dest_cargo_LD_QTY_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                # Convert   m3 to MT equ: MT*Density if Density less than 0 else MT*(Density/1000)

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'bbl':

            instock_m3 = round(float((instock) / 6.289) / float(density), 3) if float(
                density) < 1 else round(float((instock) / 6.289) / (float(density) / 1000), 3)

            if unit_to == 'bbl':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

                # Convert bbl to m3 equ: (bbl/6.289)/Density if Density less than 0 else bbl/6.289/(Density/1000)

                dest_received_qty_to_m3 = round(float((dest_received_qty_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float((dest_cargo_LD_QTY_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'm3':

            dest_received_qty_to_m3 = dest_received_qty_to
            source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)
            instock_m3 = float(instock)

            if unit_to == 'm3':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(abs(dest_cargo_LD_QTY_to))

            elif unit_to == 'MT':

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

            elif unit_to == 'bbl':

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        dest_diff = abs(float(dest_received_qty_to)) - abs(float(source_cargo_ld_qty))

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = InventoryModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':

            tank_capacity = TankCapacityM.objects.filter(Tank_no_name=str(tankno_to)).filter(Portname=port_to).filter(
                Terminal_name=terminal_to)
            for i in tank_capacity:
                safe_fill_capacity = i.Safe_fill_capacity
                remaining_space = i.Remaining_space

            if abs(float(source_cargo_ld_qty_m3)) > float(remaining_space):
                print('remaining_space', remaining_space)
                print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
                print('This much quatity cannot accpmodate in this tank')
                raise

        if abs(float(source_cargo_ld_qty_m3)) > (float(instock_m3)):
            print('Instockm3', instock_m3)
            print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
            print('quantity trying to transfer is greater than instock')
            raise
        else:
            print('Instockm3', instock_m3)
            print('Transferm3', source_cargo_ld_qty_m3)

        print("object creation for pb")

        # NEED SAME ID(Reference id)
        source_list = [tank, port, terminal]
        dest_list = [tankno_to, port_to, terminal_to]
        print(source_list, 'source_list')
        print(dest_list, 'dest_list')
        print(dest_container_to, 'dest_container_to')
        print(source_container, 'source_container')

        obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                             Distribution_Type=distribution_type,
                             Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
                             Vessal_name=vesselname,
                             Port=port, Terminal=terminal, Cargo=cargo, Unit=unit, dest_unit=unit_to,
                             Density=density, dest_cargo_LD_QTY=0,
                             inv_transfer_mode=inv_transfer_mode_to, dest_difference=0,
                             dest_received_qty=0, source_cargo_LD_QTY=source_cargo_ld_qty, m3=source_cargo_ld_qty_m3,
                             # Not Required Field
                             dest_container=dest_container_to, dest_port=port_to,
                             dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                             dest_tank_num=tankno_to,

                             )

        obj.save()
        obj.duplicate_id = obj.id
        obj.save()

        obj1 = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                              Distribution_Type=distribution_type,
                              Delivery_mode=dest_container_to, Tank=tankno_to, Strategy=strategy,
                              Vessal_name=vessalname_to,
                              Port=port_to, Terminal=terminal_to, Cargo=cargo, Unit=unit,
                              Density=density, dest_unit=unit_to,
                              inv_transfer_mode=inv_transfer_mode_to, dest_difference=dest_diff,
                              dest_received_qty=dest_received_qty_to,
                              source_cargo_LD_QTY=dest_received_qty_to, m3=dest_received_qty_to_m3,
                              Shore_recieved=dest_cargo_LD_QTY_to,
                              # Not Required Field
                              dest_cargo_LD_QTY=0,
                              dest_container=dest_container_to, dest_port=port_to,
                              dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                              dest_tank_num=tankno_to, duplicate_id=obj.id

                              )

        obj1.save()

        tank_updation_list = []

        if dest_container_to == 'Tank' or source_container == 'Tank' or dest_container_to == 'PLT' or source_container == 'PLT':
            print('+++++++++++++++++')

            if (dest_container_to == 'Tank' or dest_container_to == 'PLT') and (
                    source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                tank_updation_list.append(dest_list)
                print('first______', tank_updation_list)

            elif (dest_container_to == 'Tank' or dest_container_to == 'PLT') and source_container != 'Tank':
                tank_updation_list.append(dest_list)
                print('second______', tank_updation_list)
            elif dest_container_to != 'Tank' and (source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                print('third_____', tank_updation_list)

            print('m3=m3,Density=density_uom,', tank_updation_list)

            self.tank_update(request, tank_updation_list, cargo, density)

        messages.info(request, 'Inventory updated')
        return HttpResponseRedirect('/inventory-list/')


################# physical blotter userside Generate tradelistview #########################

class GenerateTradeUserListView(View):
    def get(self,request,*args,**kwargs):
        qs = GenerateTradeModel.objects.filter(Status = "New")
        print("qs:",qs)
        return render(request,"customer/pb-dash-new.html",{"generatetrade_user":qs})

        # return render(request, "customer/filtertable.html", {"generatetrade_user": qs})


####  stock summary in userside


class StockSummaryListView(View):
    def get(self,request,*args,**kwargs):
        qs = TankCapacityM.objects.all()
        print("qs:",qs)
        return render(request,"customer/stock_summary.html",{"stocksummary":qs})


############################## HEADGING #########################################

#
# def Headging(request):
#     print('Hedgig Starts here')
#     full_df=[]
#     swap_date_list = []
#     swap_tradetype_list = []
#     swap_Strategy_list = []
#     swap_Derivative_list = []
#     swap_Volume_list = []
#     swap_Contract_Name_list = []
#     swap_start_date_list = []
#     swap_end_date_list = []
#     swap_Holiday_list = []
#     swap_Total_no_days_list = []
#     single_diff=[]
#     mini_major=[]
#     mini_major_connection=[]
#
#     for obj in SwapBlotterModel.objects.all():
#         print("inside swapblotter")
#         # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
#         swap_date_list.append(obj.date)
#         swap_tradetype_list.append(obj.trader_type)
#         swap_Strategy_list.append(obj.strategy)
#         swap_Derivative_list.append(obj.derivatives)
#         swap_Volume_list.append(obj.volume)
#         print("swap_Volume_list",swap_Volume_list)
#         swap_Volume_list=[float(x) for x in swap_Volume_list]
#         print("swap_Volume_list2", swap_Volume_list)
#         #convert list values from model to Float
#         swap_Contract_Name_list.append(obj.contract)
#         swap_Contract_Name_list=[str(x) for x in swap_Contract_Name_list]    #convert list values from model to String
#         swap_start_date_list.append(obj.start_date)
#         swap_end_date_list.append(obj.end_date)
#         swap_Holiday_list.append(obj.holiday)
#         swap_Holiday_list = [str(x) for x in swap_Holiday_list]              #convert list values from model to String
#         swap_Total_no_days_list.append(obj.total_days)
#         single_diff.append(obj.singl_dif)
#         mini_major.append(obj.mini_major)
#         mini_major_connection.append(obj.mini_major_connection)
#
#     sb_headging_df = pd.DataFrame(
#         {"Date": swap_date_list, "Trade Type": swap_tradetype_list,
#           "Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
#           "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
#          "start_date": swap_start_date_list, "end_date": swap_end_date_list,
#          "Holiday": swap_Holiday_list,  "Total_no_days": swap_Total_no_days_list,
#          'Diff_Single':single_diff,
#          'Mini_Major':mini_major,'Mini_Major_Connection':mini_major_connection
#          })
#
#     print("sb_headging_df",sb_headging_df)
#
#     print(" b4 volume:", sb_headging_df['Volume'])
#     sb_headging_df['Volume'] = sb_headging_df['Volume'].astype(float)
#     print(" after volume:",sb_headging_df['Volume'].dtypes)
#
#     sb_headging_df['Total_no_days'] = sb_headging_df['Total_no_days'].astype(float)
#
#     print(" after volume:", sb_headging_df['Total_no_days'].dtypes)
#
#
#
#
#     sb_headging_df['new'] = np.where((sb_headging_df['Mini_Major'] == 'Mini'), sb_headging_df['Mini_Major_Connection'],
#                                     sb_headging_df['Contract_Name'])
#     sb_headging_df['Contract_Name'] = sb_headging_df['new']
#     sb_headging_df = sb_headging_df.loc[sb_headging_df['Diff_Single'] != 'Diff']
#
#     sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])
#     sb_headging_df['end_date'] = pd.to_datetime(sb_headging_df['end_date'])
#     print("b4 div")
#     sb_headging_df['vol/day'] = np.round(sb_headging_df['Volume'] / sb_headging_df['Total_no_days'], 2)
#     print("after div")
#
#     today = date.today()
#     month = today.month
#     year = today.year
#
#     first_date = (datetime.today().replace(day=1)).day
#     first_datecheck, num_days = calendar.monthrange(year, month)
#
#
#     sb_headging_df = sb_headging_df.loc[(sb_headging_df['start_date'].dt.month == month)]
#     contract_list = sb_headging_df['Contract_Name'].unique().tolist()
#
#     start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
#     end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#     end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#
#     dates = pd.date_range(start_date, end_date, freq='D')
#     dict = {'DATES': dates}
#     df_date = pd.DataFrame(dict)
#
#     Holiday_date_list = []
#     Holiday_type_list = []
#
#     for obj in HolidayM.objects.all():
#         Holiday_date_list.append(str(obj.date))
#         Holiday_type_list.append(str(obj.name))
#
#     holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
#     holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])
#
#     list_dict = {}
#     hd_swaps_dict = {}
#     holiday_swaps_list_dict = {}
#     for i in contract_list:
#         list_dictionary = []
#         holiday_swaps_list_dictionary = []
#         contract_data = sb_headging_df[(sb_headging_df["Contract_Name"] == i)]
#         contract_data = pd.DataFrame(contract_data)
#
#         for index, row in contract_data.iterrows():
#             holiday_name = row["Holiday"]
#             # dict_testholiday = {'Holiday':test_holiday}
#             # holiday_name=dict_testholiday['Holiday']
#             hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
#             hld_date = hld_df['Date'].to_list()
#
#             for hd in hld_date:
#                 hd_month=hd.month
#                 current_month=datetime.now().month
#
#                 # if hd_month==current_month:
#                 for dts in df_date['DATES']:
#                     curr_date = str(dts.date())
#
#                     if dts.date() >= row['start_date'].date() and dts.date() <= row['end_date'].date():
#                         print("month_date", dts)
#                         print(hd.date(), 'check hd_date', dts.date(), 'dts_date')
#
#                         if dts.date() != (hd.date()):
#                             list_dict.update({curr_date: row['vol/day']})
#                             holiday_swaps_list_dict.update({curr_date: 1})
#                         elif dts.date() == (hd.date()):
#                             print('its here')
#                             list_dict.update({curr_date: 0})
#                             holiday_swaps_list_dict.update({curr_date: 0})
#
#                     else:
#                         list_dict.update({curr_date: 0})
#                         holiday_swaps_list_dict.update({curr_date: 0})
#
#
#
#
#             df_dict = pd.DataFrame(list_dict.items(), columns=['Date', 'DateValue'])
#
#             df_holiday_swaps = pd.DataFrame(holiday_swaps_list_dict.items(),
#                                             columns=['Date', 'hd_bool'])
#             df_dict.set_index(['Date'], inplace=True)
#             df_holiday_swaps.set_index(['Date'], inplace=True)
#             list_dictionary.append(df_dict)
#             holiday_swaps_list_dictionary.append(df_holiday_swaps)
#
#         df_final = reduce(lambda a, b: a.add(b, fill_value=0), list_dictionary)
#         hd_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0),
#         holiday_swaps_list_dictionary)
#
#         df_final['DateValue'] = np.round(df_final['DateValue'], 2)
#
#         df_final = df_final.rename(columns={'DateValue': i})
#         hd_swaps_final = hd_swaps_final.rename(columns={'hd_bool': i})
#
#         hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
#         hd_swaps_final.reset_index(inplace=True)
#
#         df_final.index = pd.to_datetime(df_final.index)
#         df_final.reset_index(inplace=True)
#
#         for index, rows in contract_data.iterrows():
#             hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
#             if i == rows['Contract_Name']:
#
#                 if i in hd_swaps_dict:
#
#                     if rows['Holiday'] not in hd_swaps_dict[i]:
#                         hd_swaps_dict[i].append(rows['Holiday'])
#                         hd_swaps_dict[i].append(',')
#                 else:
#                     hd_swaps_dict[i] = [rows['Holiday']]
#                     hd_swaps_dict[i].append(',')
#
#             hld_date = hld_df['Date'].to_list()
#
#             for hd in hld_date:
#                 df_final.loc[(hd_swaps_final[i] == 0) & (df_final['Date'].isin([hd.date()])), i] = 'Holiday'
#
#             df_final.loc[(df_final['Date'].dt.dayofweek > 4), i] = 'Weekend'
#         #     df_final['Date'] = df_final["Date"].dt.strftime("%d-%b-%y")
#
#         df_final.set_index(['Date'], inplace=True)
#         full_df.append(df_final)
#
#     if len(full_df) > 0:
#
#         swaps_hedging = pd.concat(full_df, axis=1, ignore_index=False)
#         swaps_hedging.reset_index(inplace=True)
#         swaps_hedging['Date'] = swaps_hedging["Date"].dt.strftime("%d-%b-%y")
#         swaps_hedging.set_index(['Date'], inplace=True)
#         swaps_hedging_t = swaps_hedging.T
#         swaps_hedging_t.index.rename('Contracts', inplace=True)
#         swaps_hedging_t.reset_index(inplace=True)
#
#         for i in contract_list:
#             listToStr = ' '.join(map(str, hd_swaps_dict[i]))
#             listToStr = listToStr[:-1]
#             swaps_hedging_t.loc[(swaps_hedging_t['Contracts'] == i), 'Holiday'] = listToStr
#             mid = swaps_hedging_t['Holiday']
#             swaps_hedging_t.drop(labels=['Holiday'], axis=1, inplace=True)
#             swaps_hedging_t.insert(1, 'Holiday', mid)
#     else:
#
#         swaps_hedging = pd.DataFrame()
#         # swaps_hedging['DATES'] = df_date["DATES"].dt.strftime("%d-%b-%y")
#         # swaps_hedging.set_index(['DATES'], inplace=True)
#         swaps_hedging_t = pd.DataFrame()
#
#
#     print("hedgin df date:",swaps_hedging_t)
#
#
#
#     return (swaps_hedging_t)

    # context= {
    #     "sb_headging_df":swaps_hedging_t,
    # }
    #
    # return render(request,"customer/Hedging.html",context)


#Paper Hedging
def Headging(request):
    print('Hedgig Starts here')
    full_df=[]
    swap_date_list = []
    swap_tradetype_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Holiday_list = []
    swap_Total_no_days_list = []
    single_diff=[]
    mini_major=[]
    mini_major_connection=[]

    for obj in SwapBlotterModel.objects.all():
        print("inside swapblotter")
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        swap_Volume_list.append(obj.kbbl_mt_conversion)
        print("swap_Volume_list",swap_Volume_list)
        swap_Volume_list=[float(x) for x in swap_Volume_list]
        print("swap_Volume_list2", swap_Volume_list)
        #convert list values from model to Float
        swap_Contract_Name_list.append(obj.contract)
        swap_Contract_Name_list=[str(x) for x in swap_Contract_Name_list]    #convert list values from model to String
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Holiday_list.append(obj.holiday)
        swap_Holiday_list = [str(x) for x in swap_Holiday_list]              #convert list values from model to String
        swap_Total_no_days_list.append(obj.total_days)
        single_diff.append(obj.singl_dif)
        mini_major.append(obj.mini_major)
        mini_major_connection.append(obj.mini_major_connection)



    sb_headging_df = pd.DataFrame(
        {"Date": swap_date_list, "Trade Type": swap_tradetype_list,
          "Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
          "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
         "start_date": swap_start_date_list, "end_date": swap_end_date_list,
         "Holiday": swap_Holiday_list,  "Total_no_days": swap_Total_no_days_list,
         'Diff_Single':single_diff,
         'Mini_Major':mini_major,'Mini_Major_Connection':mini_major_connection
         })

    # print("sb_headging_df",sb_headging_df)

    # print(" b4 volume:", sb_headging_df['Volume'])
    sb_headging_df['Volume'] = sb_headging_df['Volume'].astype(float)
    # print(" after volume:",sb_headging_df['Volume'].dtypes)

    sb_headging_df['Total_no_days'] = sb_headging_df['Total_no_days'].astype(float)

    # print(" after volume:", sb_headging_df['Total_no_days'].dtypes)




    sb_headging_df['new'] = np.where((sb_headging_df['Mini_Major'] == 'mini'), sb_headging_df['Mini_Major_Connection'],
                                    sb_headging_df['Contract_Name'])
    sb_headging_df['Contract_Name'] = sb_headging_df['new']
    sb_headging_df = sb_headging_df.loc[sb_headging_df['Diff_Single'] != 'diff']

    sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])
    sb_headging_df['end_date'] = pd.to_datetime(sb_headging_df['end_date'])
    print("b4 div")
    sb_headging_df['vol/day'] = np.round(sb_headging_df['Volume'] / sb_headging_df['Total_no_days'], 2)
    print("after div")

    today = date.today()
    month = today.month
    year = today.year

    first_date = (datetime.today().replace(day=1)).day
    first_datecheck, num_days = calendar.monthrange(year, month)


    sb_headging_df = sb_headging_df.loc[(sb_headging_df['start_date'].dt.month == month)]
    contract_list = sb_headging_df['Contract_Name'].unique().tolist()

    start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
    end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    dates = pd.date_range(start_date, end_date, freq='D')
    dict = {'DATES': dates}
    df_date = pd.DataFrame(dict)

    Holiday_date_list = []
    Holiday_type_list = []

    for obj in HolidayM.objects.all():
        Holiday_date_list.append(str(obj.date))
        Holiday_type_list.append(str(obj.name))

    holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
    holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])

    list_dict = {}
    hd_swaps_dict = {}
    holiday_swaps_list_dict = {}
    for i in contract_list:
        list_dictionary = []
        holiday_swaps_list_dictionary = []
        contract_data = sb_headging_df[(sb_headging_df["Contract_Name"] == i)]
        contract_data = pd.DataFrame(contract_data)

        for index, row in contract_data.iterrows():
            holiday_name = row["Holiday"]
            # dict_testholiday = {'Holiday':test_holiday}
            # holiday_name=dict_testholiday['Holiday']
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            hld_date = hld_df['Date'].to_list()

            for hd in hld_date:
                hd_month=hd.month
                current_month=datetime.now().month

                # if hd_month==current_month:
                for dts in df_date['DATES']:
                    curr_date = str(dts.date())

                    if dts.date() >= row['start_date'].date() and dts.date() <= row['end_date'].date():
                        print("month_date", dts)
                        print(hd.date(), 'check hd_date', dts.date(), 'dts_date')

                        if dts.date()  not in [d.date() for d in hld_date]:
                            list_dict.update({curr_date: row['vol/day']})
                            holiday_swaps_list_dict.update({curr_date: 1})
                        elif dts.date() in [d.date() for d in hld_date]:
                            print('its here')
                            list_dict.update({curr_date: 0})
                            holiday_swaps_list_dict.update({curr_date: 0})

                    else:
                        list_dict.update({curr_date: 0})
                        holiday_swaps_list_dict.update({curr_date: 0})




            df_dict = pd.DataFrame(list_dict.items(), columns=['Date', 'DateValue'])

            df_holiday_swaps = pd.DataFrame(holiday_swaps_list_dict.items(),
                                            columns=['Date', 'hd_bool'])
            df_dict.set_index(['Date'], inplace=True)
            df_holiday_swaps.set_index(['Date'], inplace=True)
            list_dictionary.append(df_dict)
            holiday_swaps_list_dictionary.append(df_holiday_swaps)

        df_final = reduce(lambda a, b: a.add(b, fill_value=0), list_dictionary)
        hd_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0),
        holiday_swaps_list_dictionary)

        df_final['DateValue'] = np.round(df_final['DateValue'], 2)

        df_final = df_final.rename(columns={'DateValue': i})
        hd_swaps_final = hd_swaps_final.rename(columns={'hd_bool': i})

        hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
        hd_swaps_final.reset_index(inplace=True)

        df_final.index = pd.to_datetime(df_final.index)
        df_final.reset_index(inplace=True)

        for index, rows in contract_data.iterrows():
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            if i == rows['Contract_Name']:

                if i in hd_swaps_dict:

                    if rows['Holiday'] not in hd_swaps_dict[i]:
                        hd_swaps_dict[i].append(rows['Holiday'])
                        hd_swaps_dict[i].append(',')
                else:
                    hd_swaps_dict[i] = [rows['Holiday']]
                    hd_swaps_dict[i].append(',')

            hld_date = hld_df['Date'].to_list()

            for hd in hld_date:
                df_final.loc[(hd_swaps_final[i] == 0) & (df_final['Date'].isin([hd.date()])), i] = 'HLD'

            df_final.loc[(df_final['Date'].dt.dayofweek > 4), i] = 'WKND'
        #     df_final['Date'] = df_final["Date"].dt.strftime("%d-%b-%y")

        df_final.set_index(['Date'], inplace=True)
        full_df.append(df_final)

    if len(full_df) > 0:

        swaps_hedging = pd.concat(full_df, axis=1, ignore_index=False)
        swaps_hedging.reset_index(inplace=True)
        swaps_hedging['Date'] = swaps_hedging["Date"].dt.strftime("%d-%b-%y")
        swaps_hedging.set_index(['Date'], inplace=True)
        swaps_hedging_t = swaps_hedging.T
        swaps_hedging_t.index.rename('Contracts', inplace=True)
        swaps_hedging_t.reset_index(inplace=True)

        for i in contract_list:
            listToStr = ' '.join(map(str, hd_swaps_dict[i]))
            listToStr = listToStr[:-1]
            swaps_hedging_t.loc[(swaps_hedging_t['Contracts'] == i), 'HLD'] = listToStr
            mid = swaps_hedging_t['HLD']
            swaps_hedging_t.drop(labels=['HLD'], axis=1, inplace=True)
            swaps_hedging_t.insert(1, 'HLD', mid)
    else:

        swaps_hedging = pd.DataFrame()
        swaps_hedging['DATES'] = df_date["DATES"].dt.strftime("%d-%b-%y")
        swaps_hedging.set_index(['DATES'], inplace=True)
        swaps_hedging_t=swaps_hedging.T



    # print("hedgin df date:",swaps_hedging_t)




    today = pd.datetime.now().date()
    # print("today hedging:",today)

    today = today.strftime("%d-%b-%y")
    # print("new today:",today)

    # print("ffflter",swaps_hedging_t[today])
    return (swaps_hedging_t)


###################################################               hedging in Lots                        #################################################################


def hedging_in_lots(request):
    print('Hedgig Starts here')
    full_df=[]
    swap_date_list = []
    swap_tradetype_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Holiday_list = []
    swap_Total_no_days_list = []
    single_diff=[]
    mini_major=[]
    mini_major_connection=[]

    # for lots calculation

    kbbl_mt = []
    bbl_mt =[]
    tick = []
    bbl_mt_converion= []



    for obj in SwapBlotterModel.objects.all():
        print("inside swapblotter")
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        swap_Volume_list.append(obj.kbbl_mt_conversion)
        print("swap_Volume_list",swap_Volume_list)
        swap_Volume_list=[float(x) for x in swap_Volume_list]
        print("swap_Volume_list2", swap_Volume_list)
        #convert list values from model to Float
        swap_Contract_Name_list.append(obj.contract)
        swap_Contract_Name_list=[str(x) for x in swap_Contract_Name_list]    #convert list values from model to String
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Holiday_list.append(obj.holiday)
        swap_Holiday_list = [str(x) for x in swap_Holiday_list]              #convert list values from model to String
        swap_Total_no_days_list.append(obj.total_days)
        single_diff.append(obj.singl_dif)
        mini_major.append(obj.mini_major)
        mini_major_connection.append(obj.mini_major_connection)

        kbbl_mt.append(obj.kbbl_mt_conversion)
        bbl_mt.append(obj.bbi_mt)
        tick.append(obj.tick)
        bbl_mt_converion.append(obj.bbi_mt_conversion)

    sb_headging_df = pd.DataFrame(
        {"Date": swap_date_list, "Trade Type": swap_tradetype_list,
          "Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
          "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
         "start_date": swap_start_date_list, "end_date": swap_end_date_list,
         "Holiday": swap_Holiday_list,  "Total_no_days": swap_Total_no_days_list,
         'Diff_Single':single_diff,
         'Mini_Major':mini_major,'Mini_Major_Connection':mini_major_connection,
         'kbbl/MT':kbbl_mt,'bbl/MT':bbl_mt,"Tick":tick,'bbl/MT conversion':bbl_mt_converion,

         })

    # print("sb_headging_df",sb_headging_df)

    # print(" b4 volume:", sb_headging_df['Volume'])
    sb_headging_df['Volume'] = sb_headging_df['Volume'].astype(float)
    # print(" after volume:",sb_headging_df['Volume'].dtypes)

    sb_headging_df['Total_no_days'] = sb_headging_df['Total_no_days'].astype(float)

    # print(" after volume:", sb_headging_df['Total_no_days'].dtypes)


    ## convertting values for lots

    sb_headging_df['kbbl/MT'] = sb_headging_df['kbbl/MT'].astype(float)
    # print(" after volume:", sb_headging_df['kbbl/MT'].dtypes)

    # print("sb_headging_df['kbbl/MT']",sb_headging_df['kbbl/MT'])

    sb_headging_df['Tick'] = sb_headging_df['Tick'].astype(float)
    # print(" after volume:", sb_headging_df['Tick'].dtypes)

    sb_headging_df['bbl/MT'] = sb_headging_df['bbl/MT'].astype(float)
    # print(" after volume:", sb_headging_df['bbl/MT'].dtypes)

    # print("sb_headging_df['bbl/MT']:",sb_headging_df['bbl/MT'])

    sb_headging_df['bbl/MT conversion'] = sb_headging_df['bbl/MT conversion'].astype(float)
    # print(" after volume:", sb_headging_df['bbl/MT conversion'].dtypes)

    sb_headging_df['Tick'] = sb_headging_df['Tick'].astype(float)
    # print(" after volume Tick:", sb_headging_df['Tick'].dtypes)




    sb_headging_df['new'] = np.where((sb_headging_df['Mini_Major'] == 'mini'), sb_headging_df['Mini_Major_Connection'],
                                    sb_headging_df['Contract_Name'])
    sb_headging_df['Contract_Name'] = sb_headging_df['new']
    sb_headging_df = sb_headging_df.loc[sb_headging_df['Diff_Single'] != 'diff']

    sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])
    sb_headging_df['end_date'] = pd.to_datetime(sb_headging_df['end_date'])
    print("b4 div")
    # sb_headging_df['vol/day'] = np.round(sb_headging_df['Volume'] / sb_headging_df['Total_no_days'], 2)
    # print("after div")



    # lots hedging calculation
    sb_headging_df['Lots'] = np.round(sb_headging_df['kbbl/MT'] / sb_headging_df['bbl/MT conversion'], 2)
    # sb_headging_df['Lots'] = np.round(sb_headging_df['Lots'] / sb_headging_df['Tick'], 2)

    sb_headging_df['vol/day'] = np.round(sb_headging_df['Lots'] / sb_headging_df['Total_no_days'], 2)


    today = date.today()
    month = today.month
    year = today.year

    first_date = (datetime.today().replace(day=1)).day
    first_datecheck, num_days = calendar.monthrange(year, month)


    sb_headging_df = sb_headging_df.loc[(sb_headging_df['start_date'].dt.month == month)]
    contract_list = sb_headging_df['Contract_Name'].unique().tolist()

    start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
    end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    dates = pd.date_range(start_date, end_date, freq='D')
    dict = {'DATES': dates}
    df_date = pd.DataFrame(dict)

    Holiday_date_list = []
    Holiday_type_list = []

    for obj in HolidayM.objects.all():
        Holiday_date_list.append(str(obj.date))
        Holiday_type_list.append(str(obj.name))

    holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
    holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])

    list_dict = {}
    hd_swaps_dict = {}
    holiday_swaps_list_dict = {}
    for i in contract_list:
        list_dictionary = []
        holiday_swaps_list_dictionary = []
        contract_data = sb_headging_df[(sb_headging_df["Contract_Name"] == i)]
        contract_data = pd.DataFrame(contract_data)

        for index, row in contract_data.iterrows():
            holiday_name = row["Holiday"]
            # dict_testholiday = {'Holiday':test_holiday}
            # holiday_name=dict_testholiday['Holiday']
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            hld_date = hld_df['Date'].to_list()

            for hd in hld_date:
                hd_month=hd.month
                current_month=datetime.now().month

                # if hd_month==current_month:
                for dts in df_date['DATES']:
                    curr_date = str(dts.date())

                    if dts.date() >= row['start_date'].date() and dts.date() <= row['end_date'].date():
                        print("month_date", dts)
                        print(hd.date(), 'check hd_date', dts.date(), 'dts_date')

                        if dts.date()  not in [d.date() for d in hld_date]:
                            list_dict.update({curr_date: row['vol/day']})
                            holiday_swaps_list_dict.update({curr_date: 1})
                        elif dts.date() in [d.date() for d in hld_date]:
                            print('its here')
                            list_dict.update({curr_date: 0})
                            holiday_swaps_list_dict.update({curr_date: 0})

                    else:
                        list_dict.update({curr_date: 0})
                        holiday_swaps_list_dict.update({curr_date: 0})




            df_dict = pd.DataFrame(list_dict.items(), columns=['Date', 'DateValue'])

            df_holiday_swaps = pd.DataFrame(holiday_swaps_list_dict.items(),
                                            columns=['Date', 'hd_bool'])
            df_dict.set_index(['Date'], inplace=True)
            df_holiday_swaps.set_index(['Date'], inplace=True)
            list_dictionary.append(df_dict)
            holiday_swaps_list_dictionary.append(df_holiday_swaps)

        df_final = reduce(lambda a, b: a.add(b, fill_value=0), list_dictionary)
        hd_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0),
        holiday_swaps_list_dictionary)

        df_final['DateValue'] = np.round(df_final['DateValue'], 2)

        df_final = df_final.rename(columns={'DateValue': i})
        hd_swaps_final = hd_swaps_final.rename(columns={'hd_bool': i})

        hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
        hd_swaps_final.reset_index(inplace=True)

        df_final.index = pd.to_datetime(df_final.index)
        df_final.reset_index(inplace=True)

        for index, rows in contract_data.iterrows():
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            if i == rows['Contract_Name']:

                if i in hd_swaps_dict:

                    if rows['Holiday'] not in hd_swaps_dict[i]:
                        hd_swaps_dict[i].append(rows['Holiday'])
                        hd_swaps_dict[i].append(',')
                else:
                    hd_swaps_dict[i] = [rows['Holiday']]
                    hd_swaps_dict[i].append(',')

            hld_date = hld_df['Date'].to_list()

            for hd in hld_date:
                df_final.loc[(hd_swaps_final[i] == 0) & (df_final['Date'].isin([hd.date()])), i] = 'HLD'

            df_final.loc[(df_final['Date'].dt.dayofweek > 4), i] = 'WKND'
        #     df_final['Date'] = df_final["Date"].dt.strftime("%d-%b-%y")

        df_final.set_index(['Date'], inplace=True)
        full_df.append(df_final)

    if len(full_df) > 0:

        swaps_hedging = pd.concat(full_df, axis=1, ignore_index=False)
        swaps_hedging.reset_index(inplace=True)
        swaps_hedging['Date'] = swaps_hedging["Date"].dt.strftime("%d-%b-%y")
        swaps_hedging.set_index(['Date'], inplace=True)
        swaps_hedging_t = swaps_hedging.T
        swaps_hedging_t.index.rename('Contracts', inplace=True)
        swaps_hedging_t.reset_index(inplace=True)

        for i in contract_list:
            listToStr = ' '.join(map(str, hd_swaps_dict[i]))
            listToStr = listToStr[:-1]
            swaps_hedging_t.loc[(swaps_hedging_t['Contracts'] == i), 'HLD'] = listToStr
            mid = swaps_hedging_t['HLD']
            swaps_hedging_t.drop(labels=['HLD'], axis=1, inplace=True)
            swaps_hedging_t.insert(1, 'HLD', mid)
    else:

        swaps_hedging = pd.DataFrame()
        swaps_hedging['DATES'] = df_date["DATES"].dt.strftime("%d-%b-%y")
        swaps_hedging.set_index(['DATES'], inplace=True)
        swaps_hedging_t=swaps_hedging.T



    # print("hedgin df date:",swaps_hedging_t)




    today = pd.datetime.now().date()
    # print("today hedging:",today)

    today = today.strftime("%d-%b-%y")
    # print("new today:",today)

    # print("ffflter",swaps_hedging_t[today])



    return (swaps_hedging_t)


#########################################################################    hedging in lots end                ####################################################################################




#########################################  break by strategy swaps hedging ########################################################


def hedging_strategy_kbbl(request):
    print('Hedgig Starts here')
    full_df=[]
    swaps_distr_full_df = []
    swap_date_list = []
    swap_tradetype_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Holiday_list = []
    swap_Total_no_days_list = []
    single_diff=[]
    mini_major=[]
    mini_major_connection=[]

    for obj in SwapBlotterModel.objects.all():
        print("inside swapblotter")
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        swap_Volume_list.append(obj.kbbl_mt_conversion)
        print("swap_Volume_list",swap_Volume_list)
        swap_Volume_list=[float(x) for x in swap_Volume_list]
        print("swap_Volume_list2", swap_Volume_list)
        #convert list values from model to Float
        swap_Contract_Name_list.append(obj.contract)
        swap_Contract_Name_list=[str(x) for x in swap_Contract_Name_list]    #convert list values from model to String
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Holiday_list.append(obj.holiday)
        swap_Holiday_list = [str(x) for x in swap_Holiday_list]              #convert list values from model to String
        swap_Total_no_days_list.append(obj.total_days)
        single_diff.append(obj.singl_dif)
        mini_major.append(obj.mini_major)
        mini_major_connection.append(obj.mini_major_connection)

    sb_headging_df = pd.DataFrame(
        {"Date": swap_date_list, "Trade Type": swap_tradetype_list,
          "Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
          "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
         "start_date": swap_start_date_list, "end_date": swap_end_date_list,
         "Holiday": swap_Holiday_list,  "Total_no_days": swap_Total_no_days_list,
         'Diff_Single':single_diff,
         'Mini_Major':mini_major,'Mini_Major_Connection':mini_major_connection
         })

    # print("sb_headging_df",sb_headging_df)

    # print(" b4 volume:", sb_headging_df['Volume'])
    sb_headging_df['Volume'] = sb_headging_df['Volume'].astype(float)
    # print(" after volume:",sb_headging_df['Volume'].dtypes)

    sb_headging_df['Total_no_days'] = sb_headging_df['Total_no_days'].astype(float)

    sb_headging_df['Strategy'] = sb_headging_df['Strategy'].astype(str)

    # print(" after volume:", sb_headging_df['Total_no_days'].dtypes)




    sb_headging_df['new'] = np.where((sb_headging_df['Mini_Major'] == 'mini'), sb_headging_df['Mini_Major_Connection'],
                                    sb_headging_df['Contract_Name'])
    sb_headging_df['Contract_Name'] = sb_headging_df['new']
    sb_headging_df = sb_headging_df.loc[sb_headging_df['Diff_Single'] != 'diff']

    sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])
    sb_headging_df['end_date'] = pd.to_datetime(sb_headging_df['end_date'])
    print("b4 div")
    sb_headging_df['vol/day'] = np.round(sb_headging_df['Volume'] / sb_headging_df['Total_no_days'], 2)
    print("after div")

    today = date.today()
    month = today.month
    year = today.year

    first_date = (datetime.today().replace(day=1)).day
    first_datecheck, num_days = calendar.monthrange(year, month)


    sb_headging_df = sb_headging_df.loc[(sb_headging_df['start_date'].dt.month == month)]
    contract_list = sb_headging_df['Contract_Name'].unique().tolist()

    start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
    end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    dates = pd.date_range(start_date, end_date, freq='D')
    dict = {'DATES': dates}
    df_date = pd.DataFrame(dict)

    Holiday_date_list = []
    Holiday_type_list = []

    for obj in HolidayM.objects.all():
        Holiday_date_list.append(str(obj.date))
        Holiday_type_list.append(str(obj.name))

    holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
    holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])

    list_dict = {}
    hd_swaps_dict = {}
    holiday_swaps_list_dict = {}
    swap_strategy_contract = []
    swaps_dstr_list_dict  ={}
    hd_swaps_dstr_list_dict = {}
    swaps_strat_contract = []




    # for i in contract_list:
    #     list_dictionary = []
    #     holiday_swaps_list_dictionary = []
    #     contract_data = sb_headging_df[(sb_headging_df["Contract_Name"] == i)]
    #     contract_data = pd.DataFrame(contract_data)
    print("**********************************************************star")
    df_swaps_dist_group = sb_headging_df.groupby(['Contract_Name','Strategy'], as_index=False)
    # print("df_swaps_dist_group:",df_swaps_dist_group)

    for idx, group_swaps_df in df_swaps_dist_group:
        # print("idx",idx)
        # print("group_swaps_df",group_swaps_df)
        swaps_list_dstr_dictionary = []
        holiday_list_dstr_dictionary = []
        swaps_strat_contract.append(idx)

        # dict_testholiday = {'Holiday':test_holiday}
        # holiday_name=dict_testholiday['Holiday']
        for index, row in group_swaps_df.iterrows():
            holiday_name = row["Holiday"]
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            hld_date = hld_df['Date'].to_list()
            for hd in hld_date:
                hd_month=hd.month
                current_month=datetime.now().month

                # if hd_month==current_month:
                for dts in df_date['DATES']:
                    curr_date = str(dts.date())

                    if dts.date() >= row['start_date'].date() and dts.date() <= row['end_date'].date():
                        print("month_date", dts)
                        print(hd.date(), 'check hd_date', dts.date(), 'dts_date')

                        if dts.date()  not in [d.date() for d in hld_date]:
                            swaps_dstr_list_dict.update({curr_date: row['vol/day']})
                            hd_swaps_dstr_list_dict.update({curr_date: 1})
                        elif dts.date() in [d.date() for d in hld_date]:
                            print('its here')
                            swaps_dstr_list_dict.update({curr_date: 0})
                            hd_swaps_dstr_list_dict.update({curr_date: 0})

                    else:
                        swaps_dstr_list_dict.update({curr_date: 0})
                        hd_swaps_dstr_list_dict.update({curr_date: 0})

                    # print("swaps_dstr_list_dict:",swaps_dstr_list_dict)
                    # print("hd_swaps_dstr_list_dict:", hd_swaps_dstr_list_dict)

            df_dict = pd.DataFrame(swaps_dstr_list_dict.items(), columns=['Date', str(idx)])

            df_holiday_swaps = pd.DataFrame(hd_swaps_dstr_list_dict.items(),
                                            columns=['Date', str(idx)])
            df_dict.set_index(['Date'], inplace=True)
            df_holiday_swaps.set_index(['Date'], inplace=True)
            swaps_list_dstr_dictionary.append(df_dict)
            holiday_list_dstr_dictionary.append(df_holiday_swaps)
    #
        df_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0), swaps_list_dstr_dictionary)
        # print("df_swaps_final",df_swaps_final)
        hd_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0),holiday_list_dstr_dictionary)

        df_swaps_final.index = pd.to_datetime(df_swaps_final.index)
        df_swaps_final.reset_index(inplace=True)

        hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
        hd_swaps_final.reset_index(inplace=True)

        # print("hd_swaps_final____:",hd_swaps_final)
        # print("df_swaps_fina_____:", df_swaps_final)
        # print("holiday_name",holiday_name)

        for index, rows in group_swaps_df.iterrows():
            hld_df_swaps = holiday_data_df.loc[holiday_data_df['Holiday'] == rows['Holiday']]
            hld_date_swaps = hld_df_swaps['Date'].to_list()
        #
            for hd in hld_date_swaps:
                idx_col = str(idx)
                # print("df_swaps_final++++++++++++++++++",df_swaps_final)
                # print("hd_swaps_final&&&&&&&&&&&&&&&&&&&&&&&",hd_swaps_final)
                df_swaps_final.loc[
                    (hd_swaps_final[idx_col] == 0) & (df_swaps_final['Date'].isin([hd.date()])), idx_col] = 'Holiday'
        #
            df_swaps_final.loc[(df_swaps_final['Date'].dt.dayofweek > 4), idx_col] = 'Weekend'

        df_swaps_final.set_index(['Date'], inplace=True)
        swaps_distr_full_df.append(df_swaps_final)

        # print("swaps_distr_full_last_editttttttt",swaps_distr_full_df)

        if len(swaps_distr_full_df) > 0:
            swaps_hedging_dstr = pd.concat(swaps_distr_full_df, axis=1, ignore_index=False)
            swaps_hedging_dstr.reset_index(inplace=True)
            swaps_hedging_dstr['Date'] = swaps_hedging_dstr["Date"].dt.strftime("%d-%b-%y")
            swaps_hedging_dstr.set_index(['Date'], inplace=True)

            swaps_hedging_dstr_t = swaps_hedging_dstr.T

            swaps_hedging_dstr_t.reset_index(inplace=True)
            swaps_hedging_dstr_t['index'] = swaps_hedging_dstr_t['index'].map(lambda x: x.strip("('')"))
            swaps_hedging_dstr_t[['Contact', 'Strategy']] = swaps_hedging_dstr_t['index'].str.split(',', expand=True)
            mid = swaps_hedging_dstr_t['Contact'].str.replace("'", "")
            swaps_hedging_dstr_t.drop(labels=['Contact'], axis=1, inplace=True)
            swaps_hedging_dstr_t.insert(1, 'Contact', mid)
            mid_strat = swaps_hedging_dstr_t['Strategy'].str.replace("'", "")
            swaps_hedging_dstr_t.drop(labels=['Strategy'], axis=1, inplace=True)
            swaps_hedging_dstr_t.insert(2, 'Strategy', mid_strat)
            swaps_hedging_dstr_t.drop(labels=['index'], axis=1, inplace=True)
            print(swaps_hedging_dstr_t,"swaps_hedging_dstr_t")


        else:

            swapts_dist_hedging = df_date

            swapts_dist_hedging['DATES'] = swapts_dist_hedging["DATES"].dt.strftime("%d-%b-%y")
            swapts_dist_hedging.set_index(['DATES'], inplace=True)
            swapts_dist_hedging_t = swapts_dist_hedging.T


    # print("yyyy",swaps_hedging_dstr_t)
    return (swaps_hedging_dstr_t)

    # return render(request,"customer/break_strategy.html",{"swaps_hedging_dstr_t":swaps_hedging_dstr_t,"break_by_lots":break_strategy_lots})





##############  break by starategy lots



def hedging_strategy_lots(request):
    print('Hedgig Starts here')
    full_df=[]
    swaps_distr_full_df = []
    swap_date_list = []
    swap_tradetype_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Holiday_list = []
    swap_Total_no_days_list = []
    single_diff=[]
    mini_major=[]
    mini_major_connection=[]

    # for lots calculation

    kbbl_mt = []
    bbl_mt =[]
    tick = []
    bbl_mt_converion= []

    for obj in SwapBlotterModel.objects.all():
        print("inside swapblotter")
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        swap_Volume_list.append(obj.kbbl_mt_conversion)
        print("swap_Volume_list",swap_Volume_list)
        swap_Volume_list=[float(x) for x in swap_Volume_list]
        print("swap_Volume_list2", swap_Volume_list)
        #convert list values from model to Float
        swap_Contract_Name_list.append(obj.contract)
        swap_Contract_Name_list=[str(x) for x in swap_Contract_Name_list]    #convert list values from model to String
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Holiday_list.append(obj.holiday)
        swap_Holiday_list = [str(x) for x in swap_Holiday_list]              #convert list values from model to String
        swap_Total_no_days_list.append(obj.total_days)
        single_diff.append(obj.singl_dif)
        mini_major.append(obj.mini_major)
        mini_major_connection.append(obj.mini_major_connection)
        kbbl_mt.append(obj.kbbl_mt_conversion)
        bbl_mt.append(obj.bbi_mt)
        tick.append(obj.tick)
        bbl_mt_converion.append(obj.bbi_mt_conversion)

        # print("bbl_mt_converion&&",bbl_mt_converion)
        # print("kbbl_mt",kbbl_mt)
        # print("bbl_mt",bbl_mt)

    sb_headging_df = pd.DataFrame(
        {"Date": swap_date_list, "Trade Type": swap_tradetype_list,
          "Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
          "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
         "start_date": swap_start_date_list, "end_date": swap_end_date_list,
         "Holiday": swap_Holiday_list,  "Total_no_days": swap_Total_no_days_list,
         'Diff_Single':single_diff,
         'Mini_Major':mini_major,'Mini_Major_Connection':mini_major_connection,
         'kbbl/MT': kbbl_mt, 'bbl/MT': bbl_mt, "Tick": tick, 'bbl/MT conversion': bbl_mt_converion,

         })



    #
    sb_headging_df['Total_no_days'] = sb_headging_df['Total_no_days'].astype(int)
    #
    sb_headging_df['Strategy'] = sb_headging_df['Strategy'].astype(str)

    #
    #
    # ## convertting values for lots
    #
    sb_headging_df['kbbl/MT'] = sb_headging_df['kbbl/MT'].astype(float)
    sb_headging_df['Tick'] = sb_headging_df['Tick'].astype(float)
    sb_headging_df['bbl/MT'] = sb_headging_df['bbl/MT'].astype(float)
    sb_headging_df['bbl/MT conversion'] = sb_headging_df['bbl/MT conversion'].astype(float)
    print("sb_headging_dflotscolumn***",sb_headging_df['kbbl/MT'], sb_headging_df['bbl/MT conversion'])
    # # lots hedging calculation
    sb_headging_df['Lots'] = np.round(sb_headging_df['kbbl/MT'] / sb_headging_df['bbl/MT conversion'], 2)


    # print("lots break",   sb_headging_df['Lots'])
    sb_headging_df['vol/day'] = np.round(sb_headging_df['Lots'] / sb_headging_df['Total_no_days'], 2)

    sb_headging_df['new'] = np.where((sb_headging_df['Mini_Major'] == 'mini'), sb_headging_df['Mini_Major_Connection'],
                                    sb_headging_df['Contract_Name'])
    sb_headging_df['Contract_Name'] = sb_headging_df['new']
    sb_headging_df = sb_headging_df.loc[sb_headging_df['Diff_Single'] != 'diff']

    sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])
    sb_headging_df['end_date'] = pd.to_datetime(sb_headging_df['end_date'])
    print("b4 div")
    # sb_headging_df['vol/day'] = np.round(sb_headging_df['Volume'] / sb_headging_df['Total_no_days'], 2)
    # print("after div")



    today = date.today()
    month = today.month
    year = today.year

    first_date = (datetime.today().replace(day=1)).day
    first_datecheck, num_days = calendar.monthrange(year, month)


    sb_headging_df = sb_headging_df.loc[(sb_headging_df['start_date'].dt.month == month)]
    contract_list = sb_headging_df['Contract_Name'].unique().tolist()

    start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
    end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    #
    dates = pd.date_range(start_date, end_date, freq='D')
    dict = {'DATES': dates}
    df_date = pd.DataFrame(dict)

    Holiday_date_list = []
    Holiday_type_list = []
    #
    for obj in HolidayM.objects.all():
        Holiday_date_list.append(str(obj.date))
        Holiday_type_list.append(str(obj.name))

    holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
    holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])
    #
    list_dict = {}
    hd_swaps_dict = {}
    holiday_swaps_list_dict = {}
    swap_strategy_contract = []
    swaps_dstr_list_dict  ={}
    hd_swaps_dstr_list_dict = {}
    swaps_strat_contract = []
    #
    #
    #
    #
    # for i in contract_list:
    #     list_dictionary = []
    #     holiday_swaps_list_dictionary = []
    #     contract_data = sb_headging_df[(sb_headging_df["Contract_Name"] == i)]
    #     contract_data = pd.DataFrame(contract_data)
    print("**********************************************************star")
    df_swaps_dist_group = sb_headging_df.groupby(['Contract_Name','Strategy'], as_index=False)
    # print("df_swaps_dist_group:",df_swaps_dist_group)
    #
    for idx, group_swaps_df in df_swaps_dist_group:
        print("idx",idx)
        print("group_swaps_df",group_swaps_df)
        swaps_list_dstr_dictionary = []
        holiday_list_dstr_dictionary = []
        swaps_strat_contract.append(idx)
    #
        # dict_testholiday = {'Holiday':test_holiday}
        # holiday_name=dict_testholiday['Holiday']
        for index, row in group_swaps_df.iterrows():
            holiday_name = row["Holiday"]
            hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
            hld_date = hld_df['Date'].to_list()
            for hd in hld_date:
                hd_month=hd.month
                current_month=datetime.now().month

                # if hd_month==current_month:
                for dts in df_date['DATES']:
                    curr_date = str(dts.date())

                    if dts.date() >= row['start_date'].date() and dts.date() <= row['end_date'].date():
                        # print("month_date", dts)
                        # print(hd.date(), 'check hd_date', dts.date(), 'dts_date')

                        if dts.date()  not in [d.date() for d in hld_date]:
                            swaps_dstr_list_dict.update({curr_date: row['vol/day']})
                            hd_swaps_dstr_list_dict.update({curr_date: 1})
                        elif dts.date() in [d.date() for d in hld_date]:
                            print('its here')
                            swaps_dstr_list_dict.update({curr_date: 0})
                            hd_swaps_dstr_list_dict.update({curr_date: 0})

                    else:
                        swaps_dstr_list_dict.update({curr_date: 0})
                        hd_swaps_dstr_list_dict.update({curr_date: 0})

                    # print("swaps_dstr_list_dict:",swaps_dstr_list_dict)
                    # print("hd_swaps_dstr_list_dict:", hd_swaps_dstr_list_dict)

            df_dict = pd.DataFrame(swaps_dstr_list_dict.items(), columns=['Date', str(idx)])

            df_holiday_swaps = pd.DataFrame(hd_swaps_dstr_list_dict.items(),
                                            columns=['Date', str(idx)])
            df_dict.set_index(['Date'], inplace=True)
            df_holiday_swaps.set_index(['Date'], inplace=True)
            swaps_list_dstr_dictionary.append(df_dict)
            holiday_list_dstr_dictionary.append(df_holiday_swaps)
    #
        df_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0), swaps_list_dstr_dictionary)
        # print("df_swaps_final",df_swaps_final)
        hd_swaps_final = reduce(lambda a, b: a.add(b, fill_value=0),holiday_list_dstr_dictionary)

        df_swaps_final.index = pd.to_datetime(df_swaps_final.index)
        df_swaps_final.reset_index(inplace=True)

        hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
        hd_swaps_final.reset_index(inplace=True)

        # print("hd_swaps_final____:",hd_swaps_final)
        # print("df_swaps_fina_____:", df_swaps_final)
        # print("holiday_name",holiday_name)

        for index, rows in group_swaps_df.iterrows():
            hld_df_swaps = holiday_data_df.loc[holiday_data_df['Holiday'] == rows['Holiday']]
            hld_date_swaps = hld_df_swaps['Date'].to_list()
        #
            for hd in hld_date_swaps:
                idx_col = str(idx)
                # print("df_swaps_final++++++++++++++++++",df_swaps_final)
                # print("hd_swaps_final&&&&&&&&&&&&&&&&&&&&&&&",hd_swaps_final)
                df_swaps_final.loc[
                    (hd_swaps_final[idx_col] == 0) & (df_swaps_final['Date'].isin([hd.date()])), idx_col] = 'Holiday'
        #
            df_swaps_final.loc[(df_swaps_final['Date'].dt.dayofweek > 4), idx_col] = 'Weekend'

        df_swaps_final.set_index(['Date'], inplace=True)
        swaps_distr_full_df.append(df_swaps_final)

        # print("swaps_distr_full_last_editttttttt",swaps_distr_full_df)

        if len(swaps_distr_full_df) > 0:
            swaps_hedging_dstr = pd.concat(swaps_distr_full_df, axis=1, ignore_index=False)
            swaps_hedging_dstr.reset_index(inplace=True)
            swaps_hedging_dstr['Date'] = swaps_hedging_dstr["Date"].dt.strftime("%d-%b-%y")
            swaps_hedging_dstr.set_index(['Date'], inplace=True)

            swaps_hedging_dstr_t = swaps_hedging_dstr.T

            swaps_hedging_dstr_t.reset_index(inplace=True)
            swaps_hedging_dstr_t['index'] = swaps_hedging_dstr_t['index'].map(lambda x: x.strip("('')"))
            swaps_hedging_dstr_t[['Contact', 'Strategy']] = swaps_hedging_dstr_t['index'].str.split(',', expand=True)
            mid = swaps_hedging_dstr_t['Contact'].str.replace("'", "")
            swaps_hedging_dstr_t.drop(labels=['Contact'], axis=1, inplace=True)
            swaps_hedging_dstr_t.insert(1, 'Contact', mid)
            mid_strat = swaps_hedging_dstr_t['Strategy'].str.replace("'", "")
            swaps_hedging_dstr_t.drop(labels=['Strategy'], axis=1, inplace=True)
            swaps_hedging_dstr_t.insert(2, 'Strategy', mid_strat)
            swaps_hedging_dstr_t.drop(labels=['index'], axis=1, inplace=True)
            # print(swaps_hedging_dstr_t,"swaps_hedging_dstr_t")


        else:

            swapts_dist_hedging = df_date

            swapts_dist_hedging['DATES'] = swapts_dist_hedging["DATES"].dt.strftime("%d-%b-%y")
            swapts_dist_hedging.set_index(['DATES'], inplace=True)
            swapts_dist_hedging_t = swapts_dist_hedging.T

    # print("yyyy",swaps_hedging_dstr_t)
    return (swaps_hedging_dstr_t)

    # return render(request,"customer/break_strategy.html",{"fb_hedging_startegy":swaps_hedging_dstr_t})


















        # df_final['DateValue'] = np.round(df_final['DateValue'], 2)
        #
        # df_final = df_final.rename(columns={'DateValue': i})
        # hd_swaps_final = hd_swaps_final.rename(columns={'hd_bool': i})
        #
        # hd_swaps_final.index = pd.to_datetime(hd_swaps_final.index)
        # hd_swaps_final.reset_index(inplace=True)
    #
    #     df_final.index = pd.to_datetime(df_final.index)
    #     df_final.reset_index(inplace=True)
    #
    #     for index, rows in contract_data.iterrows():
    #         hld_df = holiday_data_df[(holiday_data_df["Holiday"] == holiday_name)]
    #         if i == rows['Contract_Name']:
    #
    #             if i in hd_swaps_dict:
    #
    #                 if rows['Holiday'] not in hd_swaps_dict[i]:
    #                     hd_swaps_dict[i].append(rows['Holiday'])
    #                     hd_swaps_dict[i].append(',')
    #             else:
    #                 hd_swaps_dict[i] = [rows['Holiday']]
    #                 hd_swaps_dict[i].append(',')
    #
    #         hld_date = hld_df['Date'].to_list()
    #
    #         for hd in hld_date:
    #             df_final.loc[(hd_swaps_final[i] == 0) & (df_final['Date'].isin([hd.date()])), i] = 'HLD'
    #
    #         df_final.loc[(df_final['Date'].dt.dayofweek > 4), i] = 'WKND'
    #     #     df_final['Date'] = df_final["Date"].dt.strftime("%d-%b-%y")
    #
    #     df_final.set_index(['Date'], inplace=True)
    #     full_df.append(df_final)
    #
    # if len(full_df) > 0:
    #
    #     swaps_hedging = pd.concat(full_df, axis=1, ignore_index=False)
    #     swaps_hedging.reset_index(inplace=True)
    #     swaps_hedging['Date'] = swaps_hedging["Date"].dt.strftime("%d-%b-%y")
    #     swaps_hedging.set_index(['Date'], inplace=True)
    #     swaps_hedging_t = swaps_hedging.T
    #     swaps_hedging_t.index.rename('Contracts', inplace=True)
    #     swaps_hedging_t.reset_index(inplace=True)
    #
    #     for i in contract_list:
    #         listToStr = ' '.join(map(str, hd_swaps_dict[i]))
    #         listToStr = listToStr[:-1]
    #         swaps_hedging_t.loc[(swaps_hedging_t['Contracts'] == i), 'HLD'] = listToStr
    #         mid = swaps_hedging_t['HLD']
    #         swaps_hedging_t.drop(labels=['HLD'], axis=1, inplace=True)
    #         swaps_hedging_t.insert(1, 'HLD', mid)
    # else:
    #
    #     swaps_hedging = pd.DataFrame()
    #     swaps_hedging['DATES'] = df_date["DATES"].dt.strftime("%d-%b-%y")
    #     swaps_hedging.set_index(['DATES'], inplace=True)
    #     swaps_hedging_t=swaps_hedging.T
    #
    #
    #
    # print("hedgin df date:",swaps_hedging_t)
    #
    #
    #
    #
    # today = pd.datetime.now().date()
    # print("today hedging:",today)
    #
    # today = today.strftime("%d-%b-%y")
    # print("new today:",today)
    #
    # print("ffflter",swaps_hedging_t[today])



    # return (swaps_hedging_t)















#########################################  end of break by strategy swaps hedging ##################################################


def Paperhedging(request):
    paperhedge = Headging(request)
    print(pd.datetime.now().date())

    paper_hedge_lots = hedging_in_lots(request)

    today = pd.datetime.now().date()
    print("today hedging:",today)

    today = today.strftime("%d-%b-%y")
    print("new today:",today)

    # swaps_hedging['DATES'] = df_date["DATES"].dt.strftime("%d-%b-%y")

    # sb_headging_df['start_date'] = pd.to_datetime(sb_headging_df['start_date'])

    print("gggggggggggg",paperhedge[today])

    redfilter = paperhedge[today]
    print("redfilter",redfilter)

    context={
        'paperhedge':paperhedge,
        'today':today,
        'redfilter':redfilter,
        'paper_hedge_lots':paper_hedge_lots,
    }
    # return render(request,"customer/paperhedge.html",context)
    return render(request,"customer/paper_exposure.html",context)




def paper_exposure_break_by_strategy(request):

    break_strategy_lots = hedging_strategy_lots(request)
    break_strategy_kbbl = hedging_strategy_kbbl(request)

    context={
        'break_strategy_lots':break_strategy_lots ,
        'break_strategy_kbbl':break_strategy_kbbl,
    }
    # return render(request,"customer/paperhedge.html",context)
    return render(request,"customer/break_by_strategy.html",context)



# def Physicalhedging(request):
#     paperhedge = Headging(request)
#     context={
#         'paperhedge':paperhedge,
#     }
#     return render(request,"customer/paperhedge.html",context)




# # trade position

# futures_lot_position********************Customer Company+Exchage+++++++++++++++++++++++++++++++++++++++++++++++++++++
# def futures_lot_position(request):
#     contract_month_list = []
#     contract_name_list = []
#     contract_volume_list = []
#
#     for obj in FutureBlotterModel.objects.all():
#         print("hey")
#         print("3 datas :",obj.id,obj.contract,obj.Contract_Month,obj.volume)
#         contract_name_list.append(obj.contract)
#         contract_month_list.append(obj.Contract_Month)
#         contract_volume_list.append(obj.volume)
#
#     position_data= pd.DataFrame({"contract_month":contract_month_list,
#                                 "contract_name": contract_name_list,
#                                 "Volume": contract_volume_list,
#                                 })
#
#     if len(position_data)>0:
#         print("newdataframe:", position_data)
#         print(contract_month_list)
#         print("future contract")
#         position_data = position_data[['contract_month', 'Volume', 'contract_name']]
#         print('Before converting : ', position_data['contract_month'].dtypes)
#         position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
#         print('After  converting : ', position_data['contract_month'].dtypes)
#         print("type of date time :", type(position_data['contract_month']))
#         print("position new data:", position_data.columns)
#         position_data.set_index('contract_month', inplace=True)
#         #
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         #
#         print("position new data:", position_data)
#         #
#         position_data["contract_name"] = position_data["contract_name"].values.astype('str')
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         print("###################################################################")
#         print("resampled:", resampled)
#         print("type of contract name ", type(position_data["contract_name"]))
#         # #
#         resampled.reset_index(inplace=True)
#         resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')
#
#         resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
#         resampled = resampled.rename_axis(None, axis=1)
#         print("resampled pivot:")
#         print(resampled)
#     else:
#         resampled= pd.DataFrame()
#     print("neww")
#
#
#     print("lots fb",resampled)
#     return (resampled)
#
#     # context = {
#     #
#     #
#     # }
#     # return render(request,"user/dashboard.html",context)
#     # return render(request, "user/dash2.html", context)



def futures_lot_position(request):
    contract_month_list = []
    contract_name_list = []
    contract_volume_list = []

    for obj in FutureBlotterModel.objects.all():

        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_volume_list.append(obj.volume)

    position_data= pd.DataFrame({"contract_month":contract_month_list,
                                "contract_name": contract_name_list,
                                "Volume": contract_volume_list,
                                })

    if len(position_data)>0:
        print("first ccondition")

        position_data = position_data[['contract_month', 'Volume', 'contract_name']]
        print("position_data",position_data)
        position_data["Volume"] = position_data["Volume"].values.astype('float')
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)

        resampled.reset_index(inplace=True)
        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)
        print("resampled pivot:")
        print("resampled",resampled)
    else:
        resampled= pd.DataFrame()
        print("1st")
    if len(resampled)>0:
        print("entered if")
        tot_data = resampled.copy()

        tot_data.drop('contract_month', inplace=True, axis=1)


        tot_data = tot_data.replace(to_replace="-", value=0.0)


        sum_product_position = tot_data.sum(axis=0)

        name_df = sum_product_position.to_frame(name='Total(lots)')


        name_df.index.name = 'Products'

        df_total = name_df
        df_total = name_df.transpose()
        print("df_total",df_total)

        df_total.reset_index(inplace=True)

        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()

        data_new = resampled.copy()  # Create copy of DataFrame

        data_new.loc[-1] = list_row

        data_new.index = data_new.index + 1  # Append list at the bottom

        data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

        data_new = data_new.rename(columns={'contract_month': 'Contract'})
        cols_new = list(data_new.columns)
        print('data_newfutures',data_new)


    else:
        data_new = pd.DataFrame()

    return (data_new)


# # swap_lot_position
# def swap_lot_position(request):
#     contract_end_date_list = []
#     contract_name_list = []
#     contract_unprice_volume_list = []
#     for obj in SwapBlotterModel.objects.all():
#         print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
#         contract_name_list.append(obj.contract)
#         contract_end_date_list.append(obj.end_date)
#         contract_unprice_volume_list.append(obj.unpriced_volume)
#
#     position_data= pd.DataFrame({"contract_month":contract_end_date_list,
#                                 "contract_name": contract_name_list,
#                                 "unprice_volume": contract_unprice_volume_list,
#                                 })
#
#     if len(position_data)>0:
#         print("swap contact")
#         print("newdataframe:", position_data)
#         print(contract_end_date_list)
#         position_data = position_data[['contract_month', 'unprice_volume', 'contract_name']]
#         print('Before converting : ', position_data['contract_month'].dtypes)
#         position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
#         print('After  converting : ', position_data['contract_month'].dtypes)
#         print("type of date time :", type(position_data['contract_month']))
#         position_data.set_index('contract_month', inplace=True)
#
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         position_data["contract_name"] = position_data["contract_name"].values.astype('str')
#         print("positin data22",position_data)
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(3)
#         resampled.reset_index(inplace=True)
#         # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
#         resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
#         resampled = resampled.rename_axis(None, axis=1)
#     else:
#         resampled= pd.DataFrame()
#
#     print("swap output:", resampled)
#
#     print("swaps lot",resampled)
#     return (resampled)
#     print("end of swap ")
#     # context = {
#     # #     # 'resampled_swap':resampled.to_html(),
#     # #     # 'position_data':position_data.to_html(),
#     # #
#     #  }
#     # return render(request,"customer/dash_swap.html",context)


# ********************swap_lot_position+++++++++++++++++++++++++++++++++++++++++++++++++++++
def swap_lot_position(request):
    contract_end_date_list = []
    contract_name_list = []
    contract_unprice_volume_list = []
    diff_single_list=[]

    for obj in SwapBlotterModel.objects.all():
        print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
        contract_name_list.append(obj.contract)
        contract_end_date_list.append(obj.end_date)
        contract_unprice_volume_list.append(obj.unpriced_volume)
        diff_single_list.append(obj.singl_dif)

    position_data= pd.DataFrame({"contract_month":contract_end_date_list,
                                "contract_name": contract_name_list,
                                "unprice_volume": contract_unprice_volume_list,
                                 "Diff_Single":diff_single_list
                                })

    if len(position_data)>0:

        position_data = position_data[['contract_month', 'unprice_volume', 'contract_name','Diff_Single']]

        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data['unprice_volume'] = position_data['unprice_volume'].astype(float)
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data["Diff_Single"] = position_data["Diff_Single"].values.astype('str')
        position_data = position_data.loc[(position_data['Diff_Single'] != 'diff')]
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(2)

        # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)

        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        if len(resampled) > 0:

            tot_data = resampled.copy()
            tot_data.drop('contract_month', inplace=True, axis=1)

            tot_data = tot_data.replace(to_replace="-", value=0.0)

            total_sum_lots = tot_data.sum().to_frame().transpose()
            sum_product_position = tot_data.sum(axis=0)

            name_df = sum_product_position.to_frame(name='Total(lots)')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()

            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)
            data_new = data_new.rename(columns={'contract_month': 'Contract'})
        else:
            data_new = pd.DataFrame()

        print("swap output:", data_new)

    else:
        data_new= pd.DataFrame()

    return (data_new)






#total fb sb postion
# def total_fbsb_trade_position_lots(request):
#     futures_position_data = futures_lot_position(request)
#     swaps_position_data = swap_lot_position(request)
#
#     print("swaps error:",swaps_position_data)
#     futures_position_data.reset_index(inplace=True)
#     swaps_position_data.reset_index(inplace=True)
#
#     if len(futures_position_data)>0:
#         futures_position_data["contract_month"]= pd.to_datetime(futures_position_data["contract_month"])
#         futures_position_data.contract_month = futures_position_data.contract_month.dt.strftime('01-%b-%y')
#         #     #covert date time format
#         futures_position_data["contract_month"] = pd.to_datetime(futures_position_data["contract_month"])
#
#     else:
#         pass
#     if len(swaps_position_data)>0:
#         swaps_position_data["contract_month"]= pd.to_datetime(swaps_position_data["contract_month"])
#         swaps_position_data.contract_month = swaps_position_data.contract_month.dt.strftime('01-%b-%y')
#         # #covert date time format
#         swaps_position_data["contract_month"] = pd.to_datetime(swaps_position_data["contract_month"])
#     else:
#         pass
#
#     print("futures_position_data",futures_position_data)
#     print("swaps_position_data", swaps_position_data)
# #
#
#
#     print("futures_position_data",futures_position_data.columns)
#     print("swaps_position_data",swaps_position_data.columns)
#
#     if len(futures_position_data) > 0 or len(swaps_position_data) > 0:
#
#         if len(futures_position_data) > 0:
#
#             futures_col_len = futures_position_data.copy()
#             Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
#                 futures_position_data) > 0 else []
#             Futures_column_name_list[0] = 'contract_month' if len(futures_col_len.columns) > 1 else []
#
#             swaps_col_len = swaps_position_data.copy()
#             swaps_col_len = swaps_col_len.set_index('contract_month') if len(swaps_position_data) > 0 else swaps_col_len
#             swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#
#         elif len(swaps_position_data) > 0 and len(futures_position_data) == 0:
#             swaps_col_len = swaps_position_data.copy()
#             swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#             swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
#             Futures_column_name_list = []
#
#         elif len(swaps_position_data) == 0 and len(futures_position_data) == 0:
#
#             Futures_column_name_list = []
#             swaps_column_name_list = []
#
#         Column_dist_list = Futures_column_name_list + swaps_column_name_list
# #
# #
#     print("Futures_column_name_list :",Futures_column_name_list)
#     print("swaps_column_name_list :",swaps_column_name_list)
#     Column_dist_list = Futures_column_name_list + swaps_column_name_list
#     print("Column_dist_list:",Column_dist_list)
#     #
#     futures_date = futures_position_data['contract_month'].tolist() if len(futures_position_data) > 0 else []
#     swaps_date = swaps_position_data['contract_month'].tolist() if len(swaps_position_data) > 0 else []
#     date_list = futures_date + swaps_date
#
#     print("date list:", date_list)
#
#     if len(date_list) > 0:
#         date_list = pd.to_datetime(date_list, format='%Y-%m-%d')
#         date_list = date_list.to_list()
#
#         min_date = min(date_list)
#         max_date = max(date_list)
#
#     date_generated = pd.date_range(min_date, max_date, freq='MS')
#     df = pd.DataFrame(date_generated, columns=['contract_month'])
#
#     df['contract_month'] = df['contract_month'].dt.strftime('%d-%b-%y')
#     if len(futures_position_data)>0:
#         futures_position_data['contract_month'] = futures_position_data['contract_month'].dt.strftime('%d-%b-%y')
#     if len(swaps_position_data) > 0:
#         swaps_position_data['contract_month'] = swaps_position_data['contract_month'].dt.strftime('%d-%b-%y')
#
#     print("date generated:", df)
#     #
#     print("start")
#     Outer_join = pd.merge(df, futures_position_data, on='contract_month', how='outer') if len(
#         futures_position_data) > 0 else df
#     futures_label = len(futures_position_data.columns)
#     print("zero")
#     print(futures_label)
#
#     print("first")
#
#     Outer_join = pd.merge(Outer_join, swaps_position_data, on='contract_month', how='outer') if len(
#         swaps_position_data) > 0 else Outer_join
#
#     print("second")
#
#     Outer_join.columns = Outer_join.columns.str.rstrip("_x")
#     print("third")
#     Outer_join.columns = Outer_join.columns.str.rstrip("_y")
#     print("4th")
#
#     outer_join_columns = Outer_join.columns.tolist()
#     print("5th")
#
#     Outer_join.columns = Column_dist_list
#     print("6th")
#     Outer_join.loc[-1] = outer_join_columns
#     print("7th")
#     Outer_join.index = Outer_join.index + 1
#     print("8th")
#     Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#     Outer_join.to_csv('Outer_Join.csv')
#     print("10th")
#     copy_whole_data = Outer_join.copy()
#     print("11th")
#     copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
#     print("12")
#
#     copy_whole_data.set_index('contract_month', inplace=True)
#     print("13")
#
#     copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
#     print("14")
#
#
#     copy_whole_data['Total'] = round(copy_whole_data['Total'], 3)
#     print("15")
#     #
#     total = copy_whole_data['Total'].tolist()
#     # # print('whole_position',whole_position)
#     Outer_join['Total(lots/statement)'] = total
#     Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
#
#
#     print("Outer_join:",Outer_join)
#     print("outerjoin.colum", Outer_join.columns)
#
#     Outer_join.columns = Outer_join.columns.str.strip()
#     # table_columns = Outer_join.columns.to_list()
#     # row_data = list(Outer_join._values.tolist())
#     # print("row data:",row_data)
#     print("outerjoin before send:",Outer_join)
#     return(Outer_join)



    #   #implement ag grid in django
    # context = {
    #     # 'futures_position_data':futures_position_data.to_html(),
    #     # 'swaps_position_data':swaps_position_data.to_html(),
    #     'Outerjoin':Outer_join
    # }
    # return render(request,"customer/fbsb_tot_position.html",context)

def total_fbsb_trade_position_lots(request):

    futures_position_data = futures_lot_position(request)
    swaps_position_data = swap_lot_position(request)

    print("swaps error:",swaps_position_data)
    # futures_position_data.reset_index(inplace=True)
    # swaps_position_data.reset_index(inplace=True)

    if len(futures_position_data) > 0 or len(swaps_position_data) > 0:

        if len(futures_position_data) > 0:

            futures_col_len = futures_position_data.copy()
            Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
                futures_position_data) > 0 else []
            Futures_column_name_list[0] = 'Contract Month' if len(futures_col_len.columns) > 1 else []

            swaps_col_len = swaps_position_data.copy()
            swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []

        elif len(swaps_position_data) > 0 and len(futures_position_data) == 0:
            swaps_col_len = swaps_position_data.copy()
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
            swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
            Futures_column_name_list = []

        elif len(swaps_position_data) == 0 and len(futures_position_data) == 0:

            Futures_column_name_list = []
            swaps_column_name_list = []

        Column_dist_list = Futures_column_name_list + swaps_column_name_list
    #
    #
        print("Futures_column_name_list :",Futures_column_name_list)
        print("swaps_column_name_list :",swaps_column_name_list)
        Column_dist_list = Futures_column_name_list + swaps_column_name_list
        print("Column_dist_list:",Column_dist_list)
        #
        futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
        swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
        date_list = futures_date + swaps_date

        print("date list:", date_list)

        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])

        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')

        print("date generated:", df)
        #
        Outer_join = pd.merge(df, futures_position_data, on='Contract', how='outer') if len(
            futures_position_data) > 0 else df
        futures_label = len(futures_position_data.columns)
        print(futures_label)

        Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
            swaps_position_data) > 0 else Outer_join

        Outer_join.columns = Outer_join.columns.str.rstrip("_x")
        Outer_join.columns = Outer_join.columns.str.rstrip("_y")

        outer_join_columns = Outer_join.columns.tolist()

        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        Outer_join.to_csv('Outer_Join.csv')
        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)

        print(copy_whole_data,'copy_whole_data')

        copy_whole_data.set_index('Contract Month', inplace=True)

        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        #
        total = copy_whole_data['Total'].tolist()
        # # print('whole_position',whole_position)
        Outer_join['Total(lots)'] = total
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)


        print("Outer_join:",Outer_join)
        print("outerjoin.colum", Outer_join.columns)

        Outer_join.columns = Outer_join.columns.str.strip()

    else:
        Outer_join=pd.DataFrame()

    # table_columns = Outer_join.columns.to_list()
    # row_data = list(Outer_join._values.tolist())
    # print("row data:",row_data)
    print("outerjoin before send:",Outer_join)
    return(Outer_join)








#######*******************  kbbl positions of All Customer Companies and Exchange***************** #######################

# def future_kbbl_position(request):
#     contract_month_list = []
#     contract_name_list = []
#     contract_kbbl_mt_list = []
#     exclude_list = ['LS Gas Oil Futures', 'Brent Crude Futures']
#     for obj in FutureBlotterModel.objects.all().exclude(contract='LS Gas Oil Futures').exclude(contract='Brent Crude Futures'):
#         print("fb without 2 cntra:",obj)
#         print("3 datas :",obj.id,obj.contract,obj.Contract_Month,obj.kbbl_mt_conversion)
#         contract_name_list.append(obj.contract)
#         contract_month_list.append(obj.Contract_Month)
#         contract_kbbl_mt_list.append(obj.kbbl_mt_conversion)
#
#     data_position= pd.DataFrame({"Contract Month":contract_month_list,
#                                 "Contract Name": contract_name_list,
#                                 "kbbl MT Conversion": contract_kbbl_mt_list,
#                                 })
#
#     print("position_data",data_position)
#     if len(data_position)>0:
#         print("position")
#         data_position['kbbl MT Conversion'] = data_position['kbbl MT Conversion'].astype(float)
#         data_position = data_position[['Contract Month', 'Contract Name', 'kbbl MT Conversion']]
#         data_position['Contract Month'] = pd.to_datetime(data_position['Contract Month'])
#
#         data_position.set_index('Contract Month', inplace=True)
#         #
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         #
#         print("position new data:", data_position)
#         #
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#
#         print("###################################################################")
#         print("resampled:", resampled)
#         print("type of contract name ", type(data_position["Contract Name"]))
#         # #
#         resampled.reset_index(inplace=True)
#         resampled['Contract Month'] = resampled['Contract Month'].dt.strftime('01-%b-%y')
#
#         # sum_product_position = resampled.sum(axis=0)
#         # print("sum_product_position:",sum_product_position)
#
#         resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
#         resampled = resampled.rename_axis(None, axis=1)
#         print("resampled pivot:")
#         print(resampled)
#
#         if len(resampled)>0:
#
#             tot_data = resampled.copy()
#             sum_product_position = tot_data.sum(axis=0)
#
#             print('+++++++++++++++++',sum_product_position,'sum_product_position')
#
#             name_df = sum_product_position.to_frame(name='Total')
#             name_df.index.name = 'Products'
#
#             df_total = name_df
#
#
#             df_total = name_df.transpose()
#
#
#             df_total.reset_index(inplace=True)
#             df_total.rename(columns={'index': 'Products'}, inplace=True)
#             print(df_total, 'ttt++++++++++total++++++++++++++++')
#
#             list_row = df_total.iloc[0].tolist()
#             data_new = resampled.copy()  # Create copy of DataFrame
#             data_new.reset_index(inplace=True)
#             data_new.loc[-1] = list_row
#             data_new.index = data_new.index + 1  # Append list at the bottom
#             data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#             data_new = data_new.rename(columns={'Contract Month': 'Contract'})
#             print(data_new, 'data_new', 'Reorder DataFrame')
#             cols_new = list(data_new.columns)
#
#         else:
#             data_new = pd.DataFrame()
#
#     else:
#         data_new = pd.DataFrame()
#     print("new ")
#
#
#     print("future kbbl return:",data_new)
#     return (data_new)
#
#     # context = {
#     #     'position_data':resampled
#     # }
#     #
#     # return render(request,'customer/fb_kbbl_position.html',context)


##############################################################################    STATEMNT  LOTS    ###############################################################################################



########################  FUTURE LOTS STATEMENT #####################################

def future_lots_statement(request):
    contract_month_list = []
    contract_name_list = []
    contract_volume_list = []

    for obj in FutureBlotterModel.objects.all():

        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_volume_list.append(obj.volume)

    position_data= pd.DataFrame({"contract_month":contract_month_list,
                                "contract_name": contract_name_list,
                                "Volume": contract_volume_list,
                                })

    if len(position_data)>0:
        print("first ccondition")

        position_data = position_data[['contract_month', 'Volume', 'contract_name']]
        print("position_data",position_data)
        position_data["Volume"] = position_data["Volume"].values.astype('float')
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)

        resampled.reset_index(inplace=True)
        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)
        print("resampled pivot:")
        print("resampled",resampled)
    else:
        resampled= pd.DataFrame()
        print("1st")
    if len(resampled)>0:
        print("entered if")
        tot_data = resampled.copy()

        tot_data.drop('contract_month', inplace=True, axis=1)


        tot_data = tot_data.replace(to_replace="-", value=0.0)


        sum_product_position = tot_data.sum(axis=0)

        name_df = sum_product_position.to_frame(name='Total(lots/statement)')


        name_df.index.name = 'Products'

        df_total = name_df
        df_total = name_df.transpose()
        print("df_total",df_total)

        df_total.reset_index(inplace=True)

        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()

        data_new = resampled.copy()  # Create copy of DataFrame

        data_new.loc[-1] = list_row

        data_new.index = data_new.index + 1  # Append list at the bottom

        data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

        data_new = data_new.rename(columns={'contract_month': 'Contract'})
        cols_new = list(data_new.columns)
        print('data_newfutures',data_new)


    else:
        data_new = pd.DataFrame()


    print("data_new:",data_new)
    
    return (data_new)


# ++++++++++++++++++++++++++++++    swap lot statement



def swap_lots_statement(request):
    contract_end_date_list = []
    contract_name_list = []
    contract_unprice_volume_list = []
    diff_single_list=[]

    for obj in SwapBlotterModel.objects.all():
        print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
        contract_name_list.append(obj.contract)
        contract_end_date_list.append(obj.end_date)
        contract_unprice_volume_list.append(obj.total_volume)
        diff_single_list.append(obj.singl_dif)

    position_data= pd.DataFrame({"contract_month":contract_end_date_list,
                                "contract_name": contract_name_list,
                                "unprice_volume": contract_unprice_volume_list,
                                 "Diff_Single":diff_single_list
                                })

    print("position_data::::::",position_data)

    if len(position_data)>0:

        position_data = position_data[['contract_month', 'unprice_volume', 'contract_name','Diff_Single']]

        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data['unprice_volume'] = position_data['unprice_volume'].astype(float)
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data["Diff_Single"] = position_data["Diff_Single"].values.astype('str')


        position_data = position_data.loc[(position_data['Diff_Single'] != 'Diff-Sub')]


        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(2)

        # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)

        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        if len(resampled) > 0:

            tot_data = resampled.copy()
            tot_data.drop('contract_month', inplace=True, axis=1)

            tot_data = tot_data.replace(to_replace="-", value=0.0)

            total_sum_lots = tot_data.sum().to_frame().transpose()
            sum_product_position = tot_data.sum(axis=0)

            name_df = sum_product_position.to_frame(name='Total(lots/statement)')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()

            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)
            data_new = data_new.rename(columns={'contract_month': 'Contract'})
        else:
            data_new = pd.DataFrame()

        print("swap output:", data_new)

    else:
        data_new= pd.DataFrame()



    print("output:",data_new)
    return (data_new)



########3   tototl lots statment

def fbsb_lots_statemnts(request):

    futures_statement_lots = future_lots_statement(request)
    swaps_statement_lots = swap_lots_statement(request)

    print("swaps error:",swaps_statement_lots)
    # futures_position_data.reset_index(inplace=True)
    # swaps_position_data.reset_index(inplace=True)

    if len(futures_statement_lots) > 0 or len(swaps_statement_lots) > 0:

        if len(futures_statement_lots) > 0:

            futures_col_len = futures_statement_lots.copy()
            Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
                futures_statement_lots) > 0 else []
            Futures_column_name_list[0] = 'Contract Month' if len(futures_col_len.columns) > 1 else []

            swaps_col_len = swaps_statement_lots.copy()
            swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_statement_lots) > 0 else swaps_col_len
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_statement_lots) > 0 else []

        elif len(swaps_statement_lots) > 0 and len(futures_statement_lots) == 0:
            swaps_col_len = swaps_statement_lots.copy()
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_statement_lots) > 0 else []
            swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
            Futures_column_name_list = []

        elif len(swaps_statement_lots) == 0 and len(futures_statement_lots) == 0:

            Futures_column_name_list = []
            swaps_column_name_list = []

        Column_dist_list = Futures_column_name_list + swaps_column_name_list
    #
    #
        print("Futures_column_name_list :",Futures_column_name_list)
        print("swaps_column_name_list :",swaps_column_name_list)
        Column_dist_list = Futures_column_name_list + swaps_column_name_list
        print("Column_dist_list:",Column_dist_list)
        #
        futures_date = futures_statement_lots['Contract'][1:].tolist() if len(futures_statement_lots) > 0 else []
        swaps_date = swaps_statement_lots['Contract'][1:].tolist() if len(swaps_statement_lots) > 0 else []
        date_list = futures_date + swaps_date

        print("date list:", date_list)

        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])

        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')

        print("date generated:", df)
        #
        Outer_join = pd.merge(df, futures_statement_lots, on='Contract', how='outer') if len(
            futures_statement_lots) > 0 else df
        futures_label = len(futures_statement_lots.columns)
        print(futures_label)

        Outer_join = pd.merge(Outer_join, swaps_statement_lots, on='Contract', how='outer') if len(
            swaps_statement_lots) > 0 else Outer_join

        Outer_join.columns = Outer_join.columns.str.rstrip("_x")
        Outer_join.columns = Outer_join.columns.str.rstrip("_y")

        outer_join_columns = Outer_join.columns.tolist()

        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        Outer_join.to_csv('Outer_Join.csv')
        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)

        print(copy_whole_data,'copy_whole_data')

        copy_whole_data.set_index('Contract Month', inplace=True)

        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        #
        total = copy_whole_data['Total'].tolist()
        # # print('whole_position',whole_position)
        Outer_join['Total(lots/statement)'] = total
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)


        print("Outer_join:",Outer_join)
        print("outerjoin.colum", Outer_join.columns)

        Outer_join.columns = Outer_join.columns.str.strip()

    else:
        Outer_join=pd.DataFrame()

    # table_columns = Outer_join.columns.to_list()
    # row_data = list(Outer_join._values.tolist())
    # print("row data:",row_data)
    print("outerjoin before send:",Outer_join)
    return(Outer_join)

    # return render(request,"customer/statement_lots.html",{"statement_lots":Outer_join})


#####################  FILTER  LOTS STATEMNENT

# future lot filter
def future_lots_statement_filter(company_name):

    company_name =company_name
    contract_month_list = []
    contract_name_list = []
    contract_volume_list = []

    for obj in FutureBlotterModel.objects.filter(book=company_name):
        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_volume_list.append(obj.volume)

    position_data = pd.DataFrame({"contract_month": contract_month_list,
                                  "contract_name": contract_name_list,
                                  "Volume": contract_volume_list,
                                  })

    if len(position_data) > 0:
        print("first ccondition")

        position_data = position_data[['contract_month', 'Volume', 'contract_name']]
        print("position_data", position_data)
        position_data["Volume"] = position_data["Volume"].values.astype('float')
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)

        resampled.reset_index(inplace=True)
        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)
        print("resampled pivot:")
        print("resampled", resampled)
    else:
        resampled = pd.DataFrame()
        print("1st")
    if len(resampled) > 0:
        print("entered if")
        tot_data = resampled.copy()

        tot_data.drop('contract_month', inplace=True, axis=1)

        tot_data = tot_data.replace(to_replace="-", value=0.0)

        sum_product_position = tot_data.sum(axis=0)

        name_df = sum_product_position.to_frame(name='Total(lots/statement)')

        name_df.index.name = 'Products'

        df_total = name_df
        df_total = name_df.transpose()
        print("df_total", df_total)

        df_total.reset_index(inplace=True)

        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()

        data_new = resampled.copy()  # Create copy of DataFrame

        data_new.loc[-1] = list_row

        data_new.index = data_new.index + 1  # Append list at the bottom

        data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

        data_new = data_new.rename(columns={'contract_month': 'Contract'})
        cols_new = list(data_new.columns)
        print('data_newfutures', data_new)


    else:
        data_new = pd.DataFrame()

    print("data_new:", data_new)

    return (data_new)



##############  swap lots statement filter
def swap_lots_statement_filter(company_name):
    company_name = company_name
    contract_end_date_list = []
    contract_name_list = []
    contract_unprice_volume_list = []
    diff_single_list=[]

    for obj in SwapBlotterModel.objects.filter(book=company_name):
        print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
        contract_name_list.append(obj.contract)
        contract_end_date_list.append(obj.end_date)
        contract_unprice_volume_list.append(obj.total_volume)
        diff_single_list.append(obj.singl_dif)

    position_data= pd.DataFrame({"contract_month":contract_end_date_list,
                                "contract_name": contract_name_list,
                                "unprice_volume": contract_unprice_volume_list,
                                 "Diff_Single":diff_single_list
                                })

    print("position_data::::::",position_data)

    if len(position_data)>0:

        position_data = position_data[['contract_month', 'unprice_volume', 'contract_name','Diff_Single']]

        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data['unprice_volume'] = position_data['unprice_volume'].astype(float)
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data["Diff_Single"] = position_data["Diff_Single"].values.astype('str')


        position_data = position_data.loc[(position_data['Diff_Single'] != 'Diff-Sub')]


        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(2)

        # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)

        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        if len(resampled) > 0:

            tot_data = resampled.copy()
            tot_data.drop('contract_month', inplace=True, axis=1)

            tot_data = tot_data.replace(to_replace="-", value=0.0)

            total_sum_lots = tot_data.sum().to_frame().transpose()
            sum_product_position = tot_data.sum(axis=0)

            name_df = sum_product_position.to_frame(name='Total(lots/statement)')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()

            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)
            data_new = data_new.rename(columns={'contract_month': 'Contract'})
        else:
            data_new = pd.DataFrame()

        print("swap output:", data_new)

    else:
        data_new= pd.DataFrame()



    print("output:",data_new)
    return (data_new)


#####################  lost statement filter fbsb

def fbsb_lots_statemnts_filter(company_name):

    futures_statement_lots = future_lots_statement_filter(company_name)
    swaps_statement_lots = swap_lots_statement_filter(company_name)

    print("swaps error:",swaps_statement_lots)
    # futures_position_data.reset_index(inplace=True)
    # swaps_position_data.reset_index(inplace=True)

    if len(futures_statement_lots) > 0 or len(swaps_statement_lots) > 0:

        if len(futures_statement_lots) > 0:

            futures_col_len = futures_statement_lots.copy()
            Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
                futures_statement_lots) > 0 else []
            Futures_column_name_list[0] = 'Contract Month' if len(futures_col_len.columns) > 1 else []

            swaps_col_len = swaps_statement_lots.copy()
            swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_statement_lots) > 0 else swaps_col_len
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_statement_lots) > 0 else []

        elif len(swaps_statement_lots) > 0 and len(futures_statement_lots) == 0:
            swaps_col_len = swaps_statement_lots.copy()
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_statement_lots) > 0 else []
            swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
            Futures_column_name_list = []

        elif len(swaps_statement_lots) == 0 and len(futures_statement_lots) == 0:

            Futures_column_name_list = []
            swaps_column_name_list = []

        Column_dist_list = Futures_column_name_list + swaps_column_name_list
    #
    #
        print("Futures_column_name_list :",Futures_column_name_list)
        print("swaps_column_name_list :",swaps_column_name_list)
        Column_dist_list = Futures_column_name_list + swaps_column_name_list
        print("Column_dist_list:",Column_dist_list)
        #
        futures_date = futures_statement_lots['Contract'][1:].tolist() if len(futures_statement_lots) > 0 else []
        swaps_date = swaps_statement_lots['Contract'][1:].tolist() if len(swaps_statement_lots) > 0 else []
        date_list = futures_date + swaps_date

        print("date list:", date_list)

        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])

        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')

        print("date generated:", df)
        #
        Outer_join = pd.merge(df, futures_statement_lots, on='Contract', how='outer') if len(
            futures_statement_lots) > 0 else df
        futures_label = len(futures_statement_lots.columns)
        print(futures_label)

        Outer_join = pd.merge(Outer_join, swaps_statement_lots, on='Contract', how='outer') if len(
            swaps_statement_lots) > 0 else Outer_join

        Outer_join.columns = Outer_join.columns.str.rstrip("_x")
        Outer_join.columns = Outer_join.columns.str.rstrip("_y")

        outer_join_columns = Outer_join.columns.tolist()

        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        Outer_join.to_csv('Outer_Join.csv')
        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)

        print(copy_whole_data,'copy_whole_data')

        copy_whole_data.set_index('Contract Month', inplace=True)

        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        #
        total = copy_whole_data['Total'].tolist()
        # # print('whole_position',whole_position)
        Outer_join['Total(lots/statement)'] = total
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)


        print("Outer_join:",Outer_join)
        print("outerjoin.colum", Outer_join.columns)

        Outer_join.columns = Outer_join.columns.str.strip()

    else:
        Outer_join=pd.DataFrame()

    # table_columns = Outer_join.columns.to_list()
    # row_data = list(Outer_join._values.tolist())
    # print("row data:",row_data)
    print("outerjoin before send:",Outer_join)
    return(Outer_join)

    # return render(request,"customer/statement_lots.html",{"statement_lots":Outer_join})










######################################################################### END OF STATEMENT LOTS #######################################################################################
# future kbbl dillena
def future_kbbl_position(request):

    contract_month_list = []
    contract_name_list = []
    contract_kbbl_mt_list = []
    exclude_list = ['LS Gas Oil Futures', 'Brent Crude Futures']

    for obj in FutureBlotterModel.objects.all().exclude(contract='LS Gas Oil Futures').exclude(contract='Brent Crude Futures'):
        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_kbbl_mt_list.append(obj.kbbl_mt_conversion)

    data_position= pd.DataFrame({"Contract Month":contract_month_list,
                                "Contract Name": contract_name_list,
                                "kbbl MT Conversion": contract_kbbl_mt_list,
                                })

    if len(data_position)>0:

        data_position['kbbl MT Conversion'] = data_position['kbbl MT Conversion'].astype(float)
        data_position['Contract Month'] = pd.to_datetime(data_position['Contract Month'])
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position = data_position[['Contract Month', 'Contract Name', 'kbbl MT Conversion']]
        data_position.set_index('Contract Month', inplace=True)


        resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled['Contract Month'] = resampled['Contract Month'].dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
        resampled = resampled.rename_axis(None, axis=1)
        print(resampled)

        if len(resampled)>0:

            tot_data = resampled.copy()
            sum_product_position = tot_data.sum(axis=0)

            print('+++++++++++++++++',sum_product_position,'sum_product_position')

            name_df = sum_product_position.to_frame(name='Total')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()


            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)
            print(df_total, 'ttt++++++++++total++++++++++++++++')

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.reset_index(inplace=True)
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
            data_new = data_new.rename(columns={'Contract Month': 'Contract'})
            cols_new = list(data_new.columns)

        else:
            data_new = pd.DataFrame()

    else:
        data_new = pd.DataFrame()

    print("data new:",data_new)
    return (data_new)
    # return render(request,"customer/testsb.html", {"data_new":data_new})



# # swap_kbbl_position
# def swap_kbbl_position(request):
#     end_date_list = []
#     contract_name_list = []
#     contract_unpriced_kbbl_mt_list = []
#     major_mini_list =[]
#     Mini_major_Conn_Contract_list = []
#
#     for obj in SwapBlotterModel.objects.all().exclude(contract='Brent 1st Line').exclude(contract='Brent 1st Line Mini').exclude(contract='LS GO 1st Line'):
#         print("fb without 2 cntra:", obj)
#         print("3 datas :", obj.id, obj.contract, obj.end_date, obj.unpriced_kbbl_mt)
#         contract_name_list.append(obj.contract)
#         end_date_list.append(obj.end_date)
#         contract_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
#         major_mini_list.append(obj.mini_major)
#         Mini_major_Conn_Contract_list.append(obj.mini_major_connection)
#
#     data_position = pd.DataFrame({
#         "Contract Name": contract_name_list,
#         "End Date": end_date_list,
#         "kbbl MT Conversion": contract_unpriced_kbbl_mt_list,
#         "Major_Mini":major_mini_list,
#         "Mini_Conn_Contract":Mini_major_Conn_Contract_list,
#     })
#
#     print("position_data", data_position)
#
#     data_position['new'] = np.where((data_position['Major_Mini'] == 'Mini'), data_position['Mini_Conn_Contract'],
#                                     data_position['Contract Name'])
#     data_position['Contract Name'] = data_position['new']
#     print("data posioton last:",data_position)
#
#
#     # data_position = data_position.loc[(data_position['Contract Name'] != 'LS GO 1st Line') & (data_position['Contract Name'] != 'Brent 1st Line') ]
#
#
#     if len(data_position)>0:
#
#         print("newdataframe:", data_position)
#         data_position = data_position[['End Date', 'kbbl MT Conversion', 'Contract Name']]
#         print('Before converting : ', data_position['End Date'].dtypes)
#         data_position['End Date'] = pd.to_datetime(data_position['End Date'])
#         data_position.set_index('End Date', inplace=True)
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#         print("positin data",data_position)
#         resampled = (data_position.resample('M').sum()).round(3)
#         resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#
#         # resampled = (position_data.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#         resampled.reset_index(inplace=True)
#
#         resampled['End Date'] = resampled['End Date'].dt.strftime('01-%b-%y')
#
#         resampled.rename(columns={'End Date': 'Contract Month'}, inplace=True)
#
#         resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
#         resampled = resampled.rename_axis(None, axis=1)
#
#
#         print("resampled end:",resampled)
#
#         # resampled['End Date'] = pd.to_datetime(resampled['End Date'].dt.date)
#         # resampled = resampled.sort_values(by=['End Date'], ignore_index=True)
#
#     #  WORKING CODE FOR TOTAL IN DOWN
#
#         tot_data = resampled.copy()
#
#         sum_product_position = tot_data.sum(axis=0)
#         name_df = sum_product_position.to_frame(name='Total')
#         name_df.index.name = 'Products'
#         df_total = name_df
#         print("df total:",df_total)
#         df_total = name_df.transpose()
#         print("transpose:",df_total)
#         df_total.reset_index(inplace=True)
#         df_total.rename(columns={'index': 'Products'}, inplace=True)
#         print("rename df tptal:",df_total)
#
#         list_row = df_total.iloc[0].tolist()
#         print("list_row df list_row:", list_row)
#         data_new = resampled.copy()  # Create copy of DataFrame
#         data_new.reset_index(inplace=True)
#         data_new.loc[-1] = list_row
#         print("loc-1:",data_new)
#         data_new.index = data_new.index + 1  # Append list at the bottom
#         data_new = data_new.sort_index().reset_index(drop=True)
#
#         data_new.rename(columns={'Contract Month': 'Contract'}, inplace=True)
#
#         print("data swaps new:",data_new)
#
#
#     else:
#         data_new= pd.DataFrame()
#
#     return (data_new)
#
#     #
#     # print("swap output new:", resampled)
#     #
#     # return render(request,'customer/fb_kbbl_position.html')


###SWAP KBBL DILLLENA
# # swap_kbbl_position
def swap_kbbl_position(request):

    end_date_list = []
    contract_name_list = []
    contract_unpriced_kbbl_mt_list = []
    major_mini_list = []
    Mini_major_Conn_Contract_list = []
    singl_diff = []

    for obj in SwapBlotterModel.objects.all().exclude(contract='Brent 1st Line').exclude(contract='Brent 1st Line Mini').exclude(contract='LS GO 1st Line').exclude(singl_dif='diff'):
        contract_name_list.append(obj.contract)
        end_date_list.append(obj.end_date)
        contract_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
        major_mini_list.append(obj.mini_major)
        Mini_major_Conn_Contract_list.append(obj.mini_major_connection)
        singl_diff.append(obj.singl_dif)

    data_position = pd.DataFrame({
        "Contract Name": contract_name_list,
        "End Date": end_date_list,
        "Unpriced_kbbl_MT": contract_unpriced_kbbl_mt_list,
        "Major_Mini": major_mini_list,
        "Mini_Conn_Contract": Mini_major_Conn_Contract_list,
        'Diff_Single': singl_diff
    })

    if len(data_position) > 0:

        print("position_data", data_position)
        data_position['new'] = np.where((data_position['Major_Mini'] == 'mini'), data_position['Mini_Conn_Contract'],
                                        data_position['Contract Name'])
        data_position['Contract Name'] = data_position['new']
        print("position_data", data_position)
        data_position = data_position[['End Date', 'Unpriced_kbbl_MT', 'Contract Name']]
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position['Unpriced_kbbl_MT'] = data_position['Unpriced_kbbl_MT'].astype(float)
        data_position['End Date'] = pd.to_datetime(data_position['End Date'])
        data_position.set_index('End Date', inplace=True)

        resampled = (data_position.resample('M').sum()).round(3)
        resampled = (data_position.groupby('Contract Name')['Unpriced_kbbl_MT'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled['End Date'] = resampled['End Date'].dt.strftime('01-%b-%y')
        resampled.rename(columns={'End Date': 'Contract Month'}, inplace=True)
        resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='Unpriced_kbbl_MT')
        resampled = resampled.rename_axis(None, axis=1)

        tot_data = resampled.copy()
        sum_product_position = tot_data.sum(axis=0)
        name_df = sum_product_position.to_frame(name='Total')
        name_df.index.name = 'Products'
        df_total = name_df

        df_total = name_df.transpose()
        print("transpose:", df_total)
        df_total.reset_index(inplace=True)
        df_total.rename(columns={'index': 'Products'}, inplace=True)
        list_row = df_total.iloc[0].tolist()

        data_new = resampled.copy()  # Create copy of DataFrame
        data_new.reset_index(inplace=True)
        data_new.loc[-1] = list_row
        data_new.index = data_new.index + 1  # Append list at the bottom
        data_new = data_new.sort_index().reset_index(drop=True)

        data_new.rename(columns={'Contract Month': 'Contract'}, inplace=True)


    else:
        data_new = pd.DataFrame()

    print("datanew",data_new)
    return (data_new)


#
# def futures_equivalent(request):
#
#     futures_position_kbbl_data = future_kbbl_position(request)
#     swaps_position_kbbl_data = swap_kbbl_position(request)
#
#
#     mini_major_list = []
#     mini_major_connection_list = []
#     contract_name_list = []
#     firstmonth_list = []
#     secondmonth_list = []
#     futures_equiv_first_kbbl_list = []
#     futures_equiv_second_kbbl_list = []
#
#     for obj in SwapBlotterModel.objects.filter(Q(contract='Brent 1st Line') | Q(contract='LS GO 1st Line')| Q(contract='Brent 1st Line Mini')):
#
#         # print("3 datas :", obj.id, obj.Contract_Name, obj.First_month, obj.Second_month)
#         print("object:",obj)
#         print(type(obj.contract))
#         mini_major_list.append(obj.mini_major)
#         print("mini_major_list",mini_major_list)
#         mini_major_connection_list.append(obj.mini_major_connection)
#         contract_name_list.append(obj.contract)
#         firstmonth_list.append(obj.First_month)
#         secondmonth_list.append(obj.Second_month)
#         futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
#         futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
#     #
#     swaps_data = pd.DataFrame({"Major_Mini": mini_major_list,
#                                   "Major_Mini_Conn": mini_major_connection_list,
#                                   "Contract_Name": contract_name_list,
#                               "First_Month": firstmonth_list,
#                               "Second_Month": secondmonth_list,
#                               "Futures_Equv_First_kbbl": futures_equiv_first_kbbl_list,
#                               "Futures_Equv_Second_kbbl": futures_equiv_second_kbbl_list,
#
#                                   })
#     print("Swaps data:", type(swaps_data['Futures_Equv_First_kbbl']))
#
#
#
#
#     swaps_data['new'] = np.where((swaps_data['Major_Mini'] == 'Mini'), swaps_data['Major_Mini_Conn'],
#                                     swaps_data['Contract_Name'])
#     swaps_data['Contract_Name'] = swaps_data['new']
#     print("data posioton swapdata:",swaps_data['Contract_Name'])
#
#     #
#     # print(type(swaps_data))
#     #
#     if len(swaps_data)>0:
#         print('working')
#
#         swaps_data_col = swaps_data.columns.tolist()
#         swaps_data_sub_first = swaps_data[['Contract_Name', 'First_Month', 'Futures_Equv_First_kbbl']].reset_index(
#             drop=True)
#         swaps_data_sub_first.rename(columns={'First_Month': 'Dates','Contract_Name':'Contract Name', 'Futures_Equv_First_kbbl': 'Futures EQV'},
#                                     inplace=True)
#         swaps_data_sub_first["Contract Name"] = swaps_data_sub_first["Contract Name"].values.astype('str')
#         swaps_data_sub_first = swaps_data_sub_first.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})
#
#         swaps_data_sub_second = swaps_data[['Contract_Name', 'Second_Month', 'Futures_Equv_Second_kbbl']].reset_index(
#             drop=True)
#         swaps_data_sub_second.rename(columns={'Second_Month': 'Dates', 'Contract_Name':'Contract Name','Futures_Equv_Second_kbbl': 'Futures EQV'},
#                                      inplace=True)
#
#         swaps_data_sub_second["Contract Name"] = swaps_data_sub_second["Contract Name"].values.astype('str')
#         swaps_data_sub_second = swaps_data_sub_second.groupby(["Dates", 'Contract Name'], as_index=False).agg(
#             {'Futures EQV': sum})
#
#         df = pd.concat([swaps_data_sub_first, swaps_data_sub_second],ignore_index=True)
#
#         print(df, 'beforedf++++fE test')
#
#         df=df.groupby(['Dates', 'Contract Name']).sum().reset_index()
#         df['Dates'] = pd.to_datetime(df['Dates'])
#         df['Dates'] = df['Dates'].dt.strftime('%d-%b-%y')
#         print(df,'df++++fE test')
#     else:
#
#         df = pd.DataFrame()
#
#
#
#     # FUTURES EQUIVALENT KBBL:
#
#
#     contract_name_list = []
#     Volume_kkbl_mt_list = []
#     contract_month_list = []
#
#
#     for obj in FutureBlotterModel.objects.filter(
#             Q(contract='Brent Crude Futures') | Q(contract='LS Gas Oil Futures')):
#         # print("3 datas :", obj.id, obj.Contract_Name, obj.First_month, obj.Second_month)
#         print("object:", obj)
#         print(type(obj.contract))
#         contract_name_list.append(obj.contract)
#         contract_month_list.append(obj.Contract_Month)
#         Volume_kkbl_mt_list.append(obj.kbbl_mt_conversion)
#      #
#     data_position = pd.DataFrame({
#                                "Contract_Name": contract_name_list,
#                                 "Contract_Month":contract_month_list,
#                                 "Volume_kbbl_MT": Volume_kkbl_mt_list,
#
#
#                                })
#     if len(data_position)>0:
#
#         data_position['Volume_kbbl_MT'] = data_position['Volume_kbbl_MT'].astype(float)
#         data_position.rename( columns = {'Volume_kbbl_MT': 'Futures EQV', 'Contract_Month': 'Dates', 'Contract_Name': 'Contract Name'},inplace = True)
#
#         data_position.Dates = pd.to_datetime(data_position.Dates)
#
#         data_position = data_position[['Dates', 'Contract Name', 'Futures EQV']]
#
#         data_position['Dates'] = pd.to_datetime(data_position['Dates'])
#
#         data_position['Dates'] = data_position['Dates'].dt.strftime('%d-%b-%y')
#
#     else:
#         data_position = pd.DataFrame()
#
#
#     print(data_position,df,'++++++++++++++++++++both eqv+++++++++++++++++++++++++')
#
#
#     try:
#         df["Contract Name"] = df["Contract Name"].values.astype('str')
#         df['Contract Name'] = df['Contract Name'].replace(['Brent 1st Line', 'LS GO 1st Line'], ['Brent Crude Futures', 'LS Gas Oil Futures'])
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#
#         df_final = pd.concat([df, data_position]).groupby(['Dates', 'Contract Name']).sum().reset_index()
#         print(df_final,'df_final')
#         if len(df_final) > 0:
#             df_final = df_final.replace(np.nan, '-')
#         #
#             contract_name = df_final['Contract Name'].unique().tolist()
#
#
#             contracts_sorted = sorted(contract_name)
#             contract_name = contracts_sorted
#
#             dataframe_list = []
#             for i in contract_name:
#                 futures_eqv_list = []
#
#                 subset = df_final[df_final["Contract Name"] == i]
#
#                 i = str(i) + '-' + 'EQV'
#
#                 for index, row in subset.iterrows():
#                     futures_eqv = {}
#                     futures_eqv['Dates'] = row['Dates']
#
#                     futures_eqv[i] = row['Futures EQV']
#
#                     futures_eqv_list.append(futures_eqv)
#
#                     df = pd.DataFrame(futures_eqv_list)
#                     df = round(df, 2)
#                 dataframe_list.append(df)
#
#             data_merge = reduce(lambda left, right:  # Merge DataFrames in list
#                                 pd.merge(left, right,
#                                          on=["Dates"],
#                                          how="outer"),
#                                 dataframe_list)
#
#             data_merge = data_merge.replace(np.nan, '-')
#
#             data_merge['Dates'] = pd.to_datetime(data_merge['Dates'])
#             data_merge = data_merge.sort_values(by='Dates').reset_index(drop=True)
#             data_merge.rename(columns={'Dates': 'Contract'}, inplace=True)
#
#             data_merge['Contract'] = data_merge['Contract'].dt.strftime('%d-%b-%y')
#
#             tot_data = data_merge.copy()
#
#             tot_data = data_merge.replace(to_replace="-", value=0.0)
#             tot_data.drop('Contract', inplace=True, axis=1)
#
#             sum_product_position = tot_data.sum(axis=0)
#
#             name_df = sum_product_position.to_frame(name='Total')
#
#             df_total = name_df
#             df_total = name_df.transpose()
#             df_total = df_total.round(2)
#
#             df_total.reset_index(inplace=True)
#             df_total.rename(columns={'index': 'Products'}, inplace=True)
#
#             list_row = df_total.iloc[0].tolist()
#
#             data_new = data_merge.copy()  # Create copy of DataFrame
#             data_new.loc[-1] = list_row
#             data_new.index = data_new.index + 1
#             futures_equivalent_df = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#
#         else:
#             futures_equivalent_df = pd.DataFrame()
#
#     except:
#         futures_equivalent_df = pd.DataFrame()
#
#
#
#     print(futures_equivalent_df,'futures_equivalent_df+++++++++test')
#
#     # futures_position_kbbl_data = future_kbbl_position(request)
#     # swaps_position_kbbl_data = swap_kbbl_position(request)
#
#     print("futures_position_kbbl_data:",futures_position_kbbl_data)
#     print("swaps_position_kbbl_data:", swaps_position_kbbl_data)
#
#     return (futures_equivalent_df)
#
#
#     # context = {
#     #
#     #     'futures_position_kbbl_data':futures_position_kbbl_data,
#     #     'swaps_position_kbbl_data': swaps_position_kbbl_data,
#     #     'futures_df':futures_equivalent_df,
#     #     'swaps_df': df
#     #
#     #
#     # }
#     #
#     # return render(request,'customer/swap_data_kbbl.html',context)


# FUTURES EQUIVALENT KBBL DILEENA
def futures_equivalent(request):

    mini_major_list = []
    mini_major_connection_list = []
    contract_name_list = []
    firstmonth_list = []
    secondmonth_list = []
    futures_equiv_first_kbbl_list = []
    futures_equiv_second_kbbl_list = []

    for obj in SwapBlotterModel.objects.filter(
            Q(contract='Brent 1st Line') | Q(contract='LS GO 1st Line') | Q(contract='Brent 1st Line Mini')):

        mini_major_list.append(obj.mini_major)
        mini_major_connection_list.append(obj.mini_major_connection)
        contract_name_list.append(obj.contract)
        firstmonth_list.append(obj.First_month)
        secondmonth_list.append(obj.Second_month)
        futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
        futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
    #
    swaps_data = pd.DataFrame({"Major_Mini": mini_major_list,
                               "Major_Mini_Conn": mini_major_connection_list,
                               "Contract_Name": contract_name_list,
                               "First_Month": firstmonth_list,
                               "Second_Month": secondmonth_list,
                               "Futures_Equv_First_kbbl": futures_equiv_first_kbbl_list,
                               "Futures_Equv_Second_kbbl": futures_equiv_second_kbbl_list,

                               })
    swaps_data['new'] = np.where((swaps_data['Major_Mini'] == 'mini'), swaps_data['Major_Mini_Conn'],
                                 swaps_data['Contract_Name'])
    swaps_data['Contract_Name'] = swaps_data['new']
    print("data posioton swapdata:", swaps_data['Contract_Name'])

    print("swaps_data",swaps_data)

    if len(swaps_data) > 0:

        swaps_data_col = swaps_data.columns.tolist()
        swaps_data_sub_first = swaps_data[['Contract_Name', 'First_Month', 'Futures_Equv_First_kbbl']].reset_index(drop=True)
        swaps_data_sub_first.rename(columns={'First_Month': 'Dates', 'Contract_Name': 'Contract Name','Futures_Equv_First_kbbl': 'Futures EQV'},inplace=True)
        swaps_data_sub_first["Contract Name"] = swaps_data_sub_first["Contract Name"].values.astype('str')
        swaps_data_sub_first = swaps_data_sub_first.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})

        # # new line added
        swaps_data_sub_first.Dates = pd.to_datetime(swaps_data_sub_first['Dates'])
        swaps_data_sub_first.Dates = swaps_data_sub_first.Dates.dt.strftime('01-%b-%y')


        swaps_data_sub_second = swaps_data[['Contract_Name', 'Second_Month', 'Futures_Equv_Second_kbbl']].reset_index(drop=True)
        swaps_data_sub_second.rename(columns={'Second_Month': 'Dates', 'Contract_Name': 'Contract Name','Futures_Equv_Second_kbbl': 'Futures EQV'},inplace=True)

        swaps_data_sub_second["Contract Name"] = swaps_data_sub_second["Contract Name"].values.astype('str')
        swaps_data_sub_second = swaps_data_sub_second.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})

        # # new line added
        swaps_data_sub_second.Dates = pd.to_datetime(swaps_data_sub_second['Dates'])
        swaps_data_sub_second.Dates = swaps_data_sub_second.Dates.dt.strftime('01-%b-%y')

        print(swaps_data_sub_second,'swaps_data_sub_second')

        df = pd.concat([swaps_data_sub_first, swaps_data_sub_second]).groupby(['Dates', 'Contract Name']).sum().reset_index()

        # df = df.
        df['Dates'] = pd.to_datetime(df['Dates'])
        df['Dates'] = df['Dates'].dt.strftime('%d-%b-%y')
        # print(df, 'df++++fE test')

        df["Contract Name"] = df["Contract Name"].values.astype('str')

        df['Contract Name'] = df['Contract Name'].replace(['Brent 1st Line', 'LS GO 1st Line'],
                                                          ['Brent Crude Futures', 'LS Gas Oil Futures'])
    else:

        df = pd.DataFrame()



    # FUTURES EQUIVALENT KBBL:

    contract_name_list = []
    Volume_kkbl_mt_list = []
    contract_month_list = []

    for obj in FutureBlotterModel.objects.filter(Q(contract='Brent Crude Futures') | Q(contract='LS Gas Oil Futures')):


        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        Volume_kkbl_mt_list.append(obj.kbbl_mt_conversion)
    #
    data_position = pd.DataFrame({
        "Contract_Name": contract_name_list,
        "Contract_Month": contract_month_list,
        "Volume_kbbl_MT": Volume_kkbl_mt_list,

    })


    print("contract_name_list",contract_name_list)
    print("Volume_kkbl_mt_list", Volume_kkbl_mt_list)
    print("contract_month_list", contract_month_list)


    print("data_position",data_position)
    if len(data_position) > 0:

        data_position['Volume_kbbl_MT'] = data_position['Volume_kbbl_MT'].astype(float)
        data_position.rename(
            columns={'Volume_kbbl_MT': 'Futures EQV', 'Contract_Month': 'Dates', 'Contract_Name': 'Contract Name'},
            inplace=True)

        data_position.Dates = pd.to_datetime(data_position.Dates)
        data_position = data_position[['Dates', 'Contract Name', 'Futures EQV']]
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position['Dates'] = pd.to_datetime(data_position['Dates'])
        data_position['Dates'] = data_position['Dates'].dt.strftime('%d-%b-%y')



        print("data_position::",data_position)

        # # new line added
        data_position.Dates = pd.to_datetime(data_position['Dates'])
        data_position.Dates = data_position.Dates.dt.strftime('01-%b-%y')



    else:
        data_position = pd.DataFrame()


    print("data_position::",data_position)


    # try:
    print("try:")


    # df["Contract Name"] = df["Contract Name"].values.astype('str')
    #
    # df['Contract Name'] = df['Contract Name'].replace(['Brent 1st Line', 'LS GO 1st Line'],
    #                                                       ['Brent Crude Futures', 'LS Gas Oil Futures'])

    print(data_position, 'dftest')

    if len(df)> 0 and len(data_position)>0:

        df_final = pd.concat([df, data_position]).groupby(['Dates', 'Contract Name']).sum().reset_index()

    elif  len(df)> 0 and len(data_position)==0:

        df_final=df.groupby(['Dates', 'Contract Name']).sum().reset_index()

    elif len(data_position)>0 and len(df)==0:
            df_final = data_position.groupby(['Dates', 'Contract Name']).sum().reset_index()

    else:
        df_final=pd.DataFrame()

    print("df_final:", df_final)

    if len(df_final) > 0:

        df_final = df_final.replace(np.nan, '-')
        contract_name = df_final['Contract Name'].unique().tolist()

        contracts_sorted = sorted(contract_name)
        contract_name = contracts_sorted

        dataframe_list = []
        for i in contract_name:
            futures_eqv_list = []

            subset = df_final[df_final["Contract Name"] == i]

            i = str(i) + '-' + 'EQV'

            for index, row in subset.iterrows():
                futures_eqv = {}
                futures_eqv['Dates'] = row['Dates']

                futures_eqv[i] = row['Futures EQV']

                futures_eqv_list.append(futures_eqv)

                df = pd.DataFrame(futures_eqv_list)
                df = round(df, 2)
            dataframe_list.append(df)

        data_merge = reduce(lambda left, right:  # Merge DataFrames in list
                            pd.merge(left, right,
                                     on=["Dates"],
                                     how="outer"),
                            dataframe_list)

        data_merge = data_merge.replace(np.nan, '-')

        data_merge['Dates'] = pd.to_datetime(data_merge['Dates'])
        data_merge = data_merge.sort_values(by='Dates').reset_index(drop=True)
        data_merge.rename(columns={'Dates': 'Contract'}, inplace=True)

        data_merge['Contract'] = data_merge['Contract'].dt.strftime('%d-%b-%y')

        tot_data = data_merge.copy()

        tot_data = data_merge.replace(to_replace="-", value=0.0)
        tot_data.drop('Contract', inplace=True, axis=1)

        print("tot_data:", tot_data)

        sum_product_position = tot_data.sum(axis=0)

        name_df = sum_product_position.to_frame(name='Total')
        print("name_df:", name_df)

        df_total = name_df
        df_total = name_df.transpose()
        df_total = df_total.round(2)

        print("df_total:", df_total)

        df_total.reset_index(inplace=True)
        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()

        data_new = data_merge.copy()  # Create copy of DataFrame
        data_new.loc[-1] = list_row
        data_new.index = data_new.index + 1
        futures_equivalent_df = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

    else:
        futures_equivalent_df = pd.DataFrame()

    # except Exception as ex :
    #
    #     print("execption ex",ex)
    #     futures_equivalent_df = pd.DataFrame()




    print("futures_equivalent_df:",futures_equivalent_df)
    return (futures_equivalent_df)

#
# ### TOTAL trade  kbbl position
#
# def total_kbbl_trade_position(request):
#
#     # PositionFilterdropdown(request)
#
#     total_fbsb_trade_position_data = total_fbsb_trade_position_lots(request)
#     futures_position_data = future_kbbl_position(request)
#     swaps_position_data = swap_kbbl_position(request)
#     futures_equivalent_data = futures_equivalent(request)
#
#     # getting all company filtering values
#
#     total_kbbl_position_companyName = request.session.get('final_out_kbbl')
#     print("total_kbbl_position_companyName:",total_kbbl_position_companyName)
#
#     # total_kbbl_position_companyName = total_kbbl_trade_position_companyName(request)
#     # print("total_kbbl_position_companyName:",total_kbbl_position_companyName)
#     # total_lots_companyname= total_fbsb_trade_position_lots_companyname(request)
#     print("jithins get:")
#
#     print("jithins after get:")
#     print('++++++++++++++++totall summary')
#     print(futures_position_data,'futures_position_data')
#     print(swaps_position_data, 'swaps_position_data')
#     print(futures_equivalent_data, 'futures_equivalent_data')
#
#
#     if len(futures_position_data) > 0 or len(swaps_position_data) or len(futures_equivalent_data):
#
#         futures_col_len = futures_position_data.copy()
#         futures_col_len = futures_col_len.set_index('Contract') if len(futures_position_data) > 0 else futures_col_len
#         Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(futures_position_data) > 0 else []
#
#         swaps_col_len = swaps_position_data.copy()
#         swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
#         swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#
#         FE_len = futures_equivalent_data.copy()
#         FE_column_name_list = len(FE_len.columns) * ['Futures  '] if len(futures_equivalent_data) > 0 else []
#         cols_len = len(futures_equivalent_data.columns)
#
#         if cols_len > 0:
#             FE_column_name_list[0] = 'Contract Month'
#         elif len(Futures_column_name_list) > 0 or len(swaps_column_name_list) > 0:
#             FE_column_name_list.append('Contract Month')
#         elif cols_len == 0 and len(Futures_column_name_list) == 0 and len(swaps_column_name_list) == 0:
#             FE_column_name_list = []
#
#         Column_dist_list = FE_column_name_list + Futures_column_name_list + swaps_column_name_list
#
#         print(Column_dist_list,'Column_dist_list')
#
#         futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
#         swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
#         FE_date = futures_equivalent_data['Contract'][1:].tolist() if len(futures_equivalent_data) > 0 else []
#         date_list = futures_date + swaps_date + FE_date
#
#         print(date_list,'date_list')
#
#         if len(date_list) > 0:
#             date_list = pd.to_datetime(date_list, format='%d-%b-%y')
#             date_list = date_list.to_list()
#
#             min_date = min(date_list)
#             max_date = max(date_list)
#
#         date_generated = pd.date_range(min_date, max_date, freq='MS')
#         df = pd.DataFrame(date_generated, columns=['Contract'])
#
#         df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')
#
#         print('df_contract',futures_equivalent_data)
#
#         Outer_join = pd.merge(df, futures_equivalent_data, on='Contract', how='outer') if len(
#             futures_equivalent_data) > 0 else df
#         FE_label = len(futures_equivalent_data.columns)
#         print(FE_label,'FE_label')
#         #
#         Outer_join = pd.merge(Outer_join, futures_position_data, on='Contract', how='outer') if len(
#             futures_position_data) > 0 else Outer_join
#
#         Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
#             swaps_position_data) > 0 else Outer_join
#
#
#         print(Outer_join,'Outer_join++++++')
#         #
#         outer_join_columns = Outer_join.columns.tolist()
#         #
#         # #
#         Outer_join.columns = Column_dist_list
#         Outer_join.loc[-1] = outer_join_columns
#         Outer_join.index = Outer_join.index + 1
#         Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#
#         #
#         # #
#         Outer_join.to_csv('Outer_Join.csv')
#         copy_whole_data = Outer_join.copy()
#         copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
#         print(copy_whole_data, 'copy_whole_data')
#
#         copy_whole_data.set_index('Contract Month', inplace=True)
#
#         copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
#         copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
#
#
#         #
#         # print('copy_whole_data++++++++',copy_whole_data)
#         # #
#         # #
#         total = copy_whole_data['Total'].tolist()
#         # # # print('whole_position',whole_position)
#         Outer_join['Total (kbbl)'] = total
#         # Outer_join.at[0,'Total (kbbl/MT)'] = '-'
#         print(Outer_join, 'Outer_join++++++++final test+++++++++++++')
#         #
#         Outer_join.replace(to_replace=['Brent Crude Futures-EQV', ' LS Gas Oil Futures-EQV'], value=['Brent Crude Futures', 'LS Gas Oil Futures'],
#                            inplace=True)
#         # #
#         Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
#         #
#         # Outer_join_tot_col = Outer_join['Total (kbbl/MT)']
#         # Outer_join = Outer_join.drop(columns=['Total (kbbl/MT)'])
#         # Outer_join.insert(loc=1, column='Total (kbbl/MT)', value=Outer_join_tot_col)
#         # #
#             # print('final', Outer_join)
#     else:
#         Outer_join = pd.DataFrame()
#
#     print(Outer_join,'Final output kbbl position++++++++++++++')
#     print("get value total_fbsb_trade_position_lots",total_fbsb_trade_position_lots)
#
#     book = Book.objects.all()
#
#     # test_company = lots_company(c)
#     # print("mmmm",test_company)
#
#     # print(jithinkbbl(company_name,b))
#     print("eerrr0r")
#
#     print("total_kbbl_position_companyName2:", total_kbbl_position_companyName)
#
#
#
#     context = {
#         'total_fbsb_trade_position_lots': total_fbsb_trade_position_data,
#         'kbbl_total_position':Outer_join,
#
#         #for filtering company name
#         'total_kbbl_position_companyName':total_kbbl_position_companyName, #kbbl calculation
#         # 'total_lots_companyname':total_lots_companyname,  #lots calculations
#
#         # for book dropdwoan
#         'book':book,
#
#     }
#
#     # return render(request, "customer/company_cust_position.html", context)
#     # return render(request,"customer/fbsb_tot_position.html",context)
#     # for presentation purpose
#     return render(request, "customer/presentation-position.html", context)




# This Month Dillena
def thismonthprice(request):
    from datetime import date

    priced_days_list = []
    unpriced_days_list =[]
    total_days_list=[]
    # holiday_list = []
    # holiday_dict = {}
    # holiday_type=[]
    holiday_type_list = []
    holidy_name_list = []
    for i in HolidayM.objects.all().values_list("name"):
        holidy_name_list.append(i)
    holidy_name_list = list(set(holidy_name_list))


    today = date.today()
    month=today.month
    year=today.year
    first_day, day_count = calendar.monthrange(year, month)

    start_date = '01' + "-" + str(month) + "-" + str(year)
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    start_date=start_date.date()

    end_date = str(day_count) + "-" + str(month) + "-" + str(year)
    end_date = datetime.strptime(end_date, '%d-%m-%Y')
    end_date=end_date.date()
    holiday_list = []

    for holiday in holidy_name_list:
        holiday=holiday[0]

        holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        print(holiday_check,'holiday_list+++++++++++++++')

        holiday_date_df = pd.DataFrame(holiday_check, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holiday_list,'holiday_list')
        total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
        print(total_swap_days, 'total_swap_days')

        today = date.today()
        today = today.strftime("%d-%b-%y")
        todays_date = datetime.strptime(today, "%d-%b-%y")
        todays_date=todays_date.date()
        start_date_value=start_date
        end_date_value=end_date

        # *******************Priced ,Unpriced Days*************************************************************************************************
        if todays_date <= start_date_value:

            unpriced_days = total_swap_days
            priced_days = 0

        elif (todays_date > start_date_value) and (todays_date <= end_date_value):

            unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
            priced_days = int(total_swap_days) - unpriced_days


        elif todays_date > end_date_value:
            unpriced_days = 0
            priced_days = int(total_swap_days)

        print('Holiday=',holiday)
        print('Total_days=',total_swap_days)
        print('Priced_Day=',priced_days)
        print('UnPriced_Day=', unpriced_days)

        priced_days_list.append(priced_days)
        unpriced_days_list.append(unpriced_days)
        total_days_list.append(total_swap_days)
        holiday_type_list.append(holiday)

    print(priced_days_list,unpriced_days_list,total_days_list,holiday_type_list,'final+++++data')

    zipped = list(zip(holiday_type_list, total_days_list, priced_days_list,unpriced_days_list))

    holiday_pricing_days = pd.DataFrame(zipped, columns=['Holiday', 'Total Days', 'Priced Days','Unpriced Days'])
    print(holiday_pricing_days,'holiday_pricing_days')

    return(holiday_pricing_days)


# thismonth holiday
def thismonthholiday(request):
    from datetime import date
    today = date.today()
    month = today.month
    year = today.year

    holiday_name = []
    holiday_date = []
    for i in HolidayM.objects.all():
        holiday_name.append(i.name)
        holiday_date.append(i.date)


    print("holiday_name:",holiday_name)
    print("holiday_date:", holiday_date)

    holiday_data = {'Holiday Name':holiday_name,'Holiday Date':holiday_date}

    holiday_df  = pd.DataFrame(holiday_data)
    print("holiday_df",holiday_df)



    holiday_df['Holiday Date'] = pd.to_datetime(holiday_df['Holiday Date'])


    holiday_df['Month']= holiday_df['Holiday Date'].dt.month
    holiday_df['Year'] = holiday_df['Holiday Date'].dt.year

    holiday_df['Holiday Date'] = holiday_df['Holiday Date'].dt.date




    print(holiday_df,"holiday_df")

    holiday_current_month = holiday_df[(holiday_df['Month']== month) & (holiday_df['Year'] == year)]
    print("holiday_current_month",holiday_current_month)

    holiday_current_month =  holiday_current_month[['Holiday Name','Holiday Date']]
    df_pivot_holiday = (holiday_current_month.assign(idx=holiday_current_month.groupby('Holiday Name').cumcount())
     .pivot(index='idx', columns='Holiday Name', values='Holiday Date'))

    df_pivot_holiday.fillna('', inplace=True)

    print("df_pivot_holiday:",df_pivot_holiday)
    
    return(df_pivot_holiday)













    start_date = '01' + "-" + str(month) + "-" + str(year)
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    start_date = start_date.date()

    end_date = str(day_count) + "-" + str(month) + "-" + str(year)
    end_date = datetime.strptime(end_date, '%d-%m-%Y')
    end_date = end_date.date()












    holiday_type_list = []
    holidy_name_list = []
    for i in HolidayM.objects.all().values_list("name"):
        holidy_name_list.append(i)
    holidy_name_list = list(set(holidy_name_list))


    today = date.today()
    month=today.month
    year=today.year
    first_day, day_count = calendar.monthrange(year, month)

    start_date = '01' + "-" + str(month) + "-" + str(year)
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    start_date=start_date.date()

    end_date = str(day_count) + "-" + str(month) + "-" + str(year)
    end_date = datetime.strptime(end_date, '%d-%m-%Y')
    end_date=end_date.date()
    holiday_list = []

    for holiday in holidy_name_list:
        holiday=holiday[0]

        holiday_check = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        print(holiday_check,'holiday_list+++++++++++++++')

        holiday_date_df = pd.DataFrame(holiday_check, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holiday_list,'holiday_list')
        total_swap_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holiday_list))
        print(total_swap_days, 'total_swap_days')

        today = date.today()
        today = today.strftime("%d-%b-%y")
        todays_date = datetime.strptime(today, "%d-%b-%y")
        todays_date=todays_date.date()
        start_date_value=start_date
        end_date_value=end_date

        # *******************Priced ,Unpriced Days*************************************************************************************************
        if todays_date <= start_date_value:

            unpriced_days = total_swap_days
            priced_days = 0

        elif (todays_date > start_date_value) and (todays_date <= end_date_value):

            unpriced_days = len(pd.bdate_range(todays_date, end_date_value, freq="C", holidays=holiday_list))
            priced_days = int(total_swap_days) - unpriced_days


        elif todays_date > end_date_value:
            unpriced_days = 0
            priced_days = int(total_swap_days)

        print('Holiday=',holiday)
        print('Total_days=',total_swap_days)
        print('Priced_Day=',priced_days)
        print('UnPriced_Day=', unpriced_days)

        priced_days_list.append(priced_days)
        unpriced_days_list.append(unpriced_days)
        total_days_list.append(total_swap_days)
        holiday_type_list.append(holiday)

    print(priced_days_list,unpriced_days_list,total_days_list,holiday_type_list,'final+++++data')

    zipped = list(zip(holiday_type_list, total_days_list, priced_days_list,unpriced_days_list))

    holiday_pricing_days = pd.DataFrame(zipped, columns=['Holiday', 'Total Days', 'Priced Days','Unpriced Days'])
    print(holiday_pricing_days,'holiday_pricing_days')

    return(holiday_pricing_days)









#### TOATAL KBBL DILEENA
def total_kbbl_trade_position(request):

    # total_fbsb_trade_position_data = total_fbsb_trade_position_lots(request)
    # total_kbbl_position_companyName = request.session.get('final_out_kbbl')
    # print("total_kbbl_position_companyName:",total_kbbl_position_companyName)

    total_fbsb_trade_position_data = total_fbsb_trade_position_lots(request)
    futures_position_data = future_kbbl_position(request)
    swaps_position_data = swap_kbbl_position(request)
    futures_equivalent_data = futures_equivalent(request)
    this_month_price =  thismonthprice(request)
    this_month_holiday = thismonthholiday(request)

    lots_statements = fbsb_lots_statemnts(request)

    print(futures_position_data,'futures_position_data')
    print(swaps_position_data,'swaps_position_data')
    print(futures_equivalent_data,'futures_equivalent_data')
    print(thismonthprice, 'thismonthprice')

    if len(futures_position_data) > 0 or len(swaps_position_data)>0 or len(futures_equivalent_data)>0:

        futures_col_len = futures_position_data.copy()
        futures_col_len = futures_col_len.set_index('Contract') if len(futures_position_data) > 0 else futures_col_len
        Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(futures_position_data) > 0 else []

        swaps_col_len = swaps_position_data.copy()
        swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
        swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []

        FE_len = futures_equivalent_data.copy()
        FE_column_name_list = len(FE_len.columns) * ['Futures  '] if len(futures_equivalent_data) > 0 else []
        cols_len = len(futures_equivalent_data.columns)

        if cols_len > 0:
            FE_column_name_list[0] = 'Contract Month'
        elif len(Futures_column_name_list) > 0 or len(swaps_column_name_list) > 0:
            FE_column_name_list.append('Contract Month')
        elif cols_len == 0 and len(Futures_column_name_list) == 0 and len(swaps_column_name_list) == 0:
            FE_column_name_list = []

        Column_dist_list = FE_column_name_list + Futures_column_name_list + swaps_column_name_list

        futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
        swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
        FE_date = futures_equivalent_data['Contract'][1:].tolist() if len(futures_equivalent_data) > 0 else []
        date_list = futures_date + swaps_date + FE_date


        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])
        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')


        Outer_join = pd.merge(df, futures_equivalent_data, on='Contract', how='outer') if len(
            futures_equivalent_data) > 0 else df
        FE_label = len(futures_equivalent_data.columns)

        Outer_join = pd.merge(Outer_join, futures_position_data, on='Contract', how='outer') if len(
            futures_position_data) > 0 else Outer_join

        Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
            swaps_position_data) > 0 else Outer_join

        outer_join_columns = Outer_join.columns.tolist()
        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
        copy_whole_data.set_index('Contract Month', inplace=True)
        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        total = copy_whole_data['Total'].tolist()
        Outer_join['Total (kbbl)'] = total
        # Outer_join.at[0,'Total (kbbl/MT)'] = '-'
        Outer_join.replace(to_replace=['Brent Crude Futures-EQV', 'LS Gas Oil Futures-EQV'], value=['Brent Crude Futures', 'LS Gas Oil Futures'], inplace=True)
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
        position_kbbl_allcompany = Outer_join

        # Outer_join_tot_col = Outer_join['Total (kbbl/MT)']
        # Outer_join = Outer_join.drop(columns=['Total (kbbl/MT)'])
        # Outer_join.insert(loc=1, column='Total (kbbl/MT)', value=Outer_join_tot_col)
        # #
            # print('final', Outer_join)
    else:
        position_kbbl_allcompany = pd.DataFrame()


    print(position_kbbl_allcompany,'position_kbbl_allcompany')

    book = Book.objects.all()


    print("total_kbbl",position_kbbl_allcompany)

    # return position_kbbl_allcompany


    # phyical_blotter_position = physical_position(request)

    #### ########################################################         this month holiday         ##################################################################################

    # todayy = pd.datetime.now().date()
    # print("todayyy",todayy)
    # tdayyyy = date.today()
    # print(" second todayyy",todayy)
    #
    # datelist_count = []
    #
    # total_hld_count = HolidayM.objects.filter(date__icontains="2023-12-25")
    # print("total_hld_count",total_hld_count)
    #
    # for i in total_hld_count:
    #     print("count:",i)
    #     print("date count",i.date)
    #     datelist_count.append(i.date)
    #
    # print("listcount:",len(datelist_count))
    #
    # res = todayy.replace(day=1)
    # print('First day of a month:', res)

    # today = pd.datetime.now().date()
    # print("todayyy", today)
    #
    # firstdayofmonth = today.replace(day=1)
    # print('First day of a month:', firstdayofmonth)




    context = {
        'total_fbsb_trade_position_lots': total_fbsb_trade_position_data,
        'kbbl_total_position':position_kbbl_allcompany,
        # 'phyical_blotter_position':phyical_blotter_position,

        #for filtering company name
        # 'total_kbbl_position_companyName':total_kbbl_position_companyName, #kbbl calculation
        # 'total_lots_companyname':total_lots_companyname,  #lots calculations

        # lotstatement

        'statement_lots':lots_statements,



        # for book dropdwoan
        'book':book,
        'thismonthprice':this_month_price,
        'this_month_holiday':this_month_holiday,

        ### this month priced unpriced
    }

    # return render(request, "customer/company_cust_position.html", context)
    # return render(request,"customer/fbsb_tot_position.html",context)
    # for presentation purpose
    # return render(request, "customer/presentation-position.html", context)
    return render(request, "customer/kbbl-total-position.html", context)

#######******************* Ends  kbbl positions of All Customer Companies and Exchange***************** #######################


# ****************************  kbbl company name/customer position *********************************8

# # working code mine
# def future_position_kbbl_company_name(f_kbbl):
#     # company_name = "Rawat"
#     print("data from fxn pass:")
#     company_name = f_kbbl
#     print(company_name,"company_name ella")
#     contract_month_list = []
#     contract_name_list = []
#     contract_kbbl_mt_list = []
#     exclude_list = ['LS Gas Oil Futures', 'Brent Crude Futures']
#     for obj in FuturesBlottersModel.objects.filter(Book__name=company_name).exclude(Contract_Name__contract_name='LS Gas Oil Futures').exclude(Contract_Name__contract_name='Brent Crude Futures'):
#
#         print("datas for filter kbbl new",obj.id,obj.Contract_Name,obj.Contract_Month,obj.kbbl_mt_conversion,obj.Book)
#         contract_name_= obj.Contract_Name
#         contract_name_list.append(contract_name_)
#         contract_month_list.append(obj.Contract_Month)
#         contract_kbbl_mt_list.append(obj.kbbl_mt_conversion)
#
#     print("contract_name_list:", contract_name_list)
#     print("contract_month_list:", contract_month_list)
#     print("contract_kbbl_mt_list:", contract_kbbl_mt_list)
#     #
#     data_position= pd.DataFrame({"Contract Month":contract_month_list,
#                                 "Contract Name": contract_name_list,
#                                 "kbbl MT Conversion": contract_kbbl_mt_list,
#                                 })
#     #
#     print("position_data",data_position)
#     if len(data_position)>0:
#         print("position")
#         data_position['kbbl MT Conversion'] = data_position['kbbl MT Conversion'].astype(float)
#         data_position = data_position[['Contract Month', 'Contract Name', 'kbbl MT Conversion']]
#         data_position['Contract Month'] = pd.to_datetime(data_position['Contract Month'])
#     #
#         data_position.set_index('Contract Month', inplace=True)
#         #
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         #
#         print("position new data:", data_position)
#     #     #
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#
#         print("###################################################################")
#         print("resampled:", resampled)
#         print("type of contract name ", type(data_position["Contract Name"]))
#     #     # #
#         resampled.reset_index(inplace=True)
#         resampled['Contract Month'] = resampled['Contract Month'].dt.strftime('01-%b-%y')
#
#         # sum_product_position = resampled.sum(axis=0)
#         # print("sum_product_position:",sum_product_position)
#
#         resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
#         resampled = resampled.rename_axis(None, axis=1)
#         print("resampled pivot:")
#         print(resampled)
#     #
#         if len(resampled)>0:
#
#             tot_data = resampled.copy()
#             sum_product_position = tot_data.sum(axis=0)
#
#             print('+++++++++++++++++',sum_product_position,'sum_product_position')
#
#             name_df = sum_product_position.to_frame(name='Total')
#             name_df.index.name = 'Products'
#
#             df_total = name_df
#
#
#             df_total = name_df.transpose()
#     #
#     #
#             df_total.reset_index(inplace=True)
#             df_total.rename(columns={'index': 'Products'}, inplace=True)
#             print(df_total, 'ttt++++++++++total++++++++++++++++')
#     #
#             list_row = df_total.iloc[0].tolist()
#             data_new = resampled.copy()  # Create copy of DataFrame
#             data_new.reset_index(inplace=True)
#             data_new.loc[-1] = list_row
#             data_new.index = data_new.index + 1  # Append list at the bottom
#             data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
#     #
#             data_new = data_new.rename(columns={'Contract Month': 'Contract'})
#             print(data_new, 'data_new', 'Reorder DataFrame')
#             cols_new = list(data_new.columns)
#             print("cols_new:",cols_new)
#             print("the end")
#     #
#         else:
#             data_new = pd.DataFrame()
#
#     else:
#         data_new = pd.DataFrame()
#     print("new ")
#     #
#     #
#     print("future kbbl return:",data_new)
#     return (data_new)
#
#     # context = {
#     #     'position_data':resampled
#     # }
#     #
#     # return render(request,'customer/fb_kbbl_position.html',context)
#     # return render(request,"customer/fb.html")


#### FUTURE POSITION KBBL DILLENA
def future_position_kbbl_company_name(company_name):
    company_name = company_name
    contract_month_list = []
    contract_name_list = []
    contract_kbbl_mt_list = []
    book_list=[]
    exclude_list = ['LS Gas Oil Futures', 'Brent Crude Futures']

    for obj in FutureBlotterModel.objects.filter(book=company_name).exclude(contract='LS Gas Oil Futures').exclude(contract='Brent Crude Futures'):
        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_kbbl_mt_list.append(obj.kbbl_mt_conversion)
        book_list.append(obj.book)

    data_position= pd.DataFrame({"Contract Month":contract_month_list,
                                "Contract Name": contract_name_list,
                                "kbbl MT Conversion": contract_kbbl_mt_list,
                                 'book':book_list
                                })
    data_position = data_position.loc[(data_position['book'] == company_name)]
    if len(data_position)>0:

        data_position['kbbl MT Conversion'] = data_position['kbbl MT Conversion'].astype(float)
        data_position['Contract Month'] = pd.to_datetime(data_position['Contract Month'])
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position = data_position[['Contract Month', 'Contract Name', 'kbbl MT Conversion']]
        data_position.set_index('Contract Month', inplace=True)


        resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled['Contract Month'] = resampled['Contract Month'].dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
        resampled = resampled.rename_axis(None, axis=1)
        print(resampled)

        if len(resampled)>0:

            tot_data = resampled.copy()
            sum_product_position = tot_data.sum(axis=0)

            print('+++++++++++++++++',sum_product_position,'sum_product_position')

            name_df = sum_product_position.to_frame(name='Total')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()


            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)
            print(df_total, 'ttt++++++++++total++++++++++++++++')

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.reset_index(inplace=True)
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
            data_new = data_new.rename(columns={'Contract Month': 'Contract'})
            cols_new = list(data_new.columns)

        else:
            data_new = pd.DataFrame()

    else:
        data_new = pd.DataFrame()


    print("fb kbbl compnay:",data_new)
    return (data_new)


#
# def swaps_position_kbbl_company_name(s_kbbl):
#
#     print("company name for swaps kbbl from  inout box:",s_kbbl)
#     print("++++++++++++")
#     company_name = s_kbbl
#     end_date_list = []
#     contract_name_list = []
#     contract_unpriced_kbbl_mt_list = []
#     major_mini_list =[]
#     Mini_major_Conn_Contract_list = []
#
#     for obj in SwapBlottersModel.objects.filter(Book__name=company_name).exclude(Contract_Name__contract_name='Brent 1st Line').exclude(Contract_Name__contract_name='Brent 1st Line Mini').exclude(Contract_Name__contract_name='LS GO 1st Line'):
#         print("fb without 2 cntra:", obj)
#         print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unpriced_kbbl_mt)
#         contract_name_list.append(obj.Contract_Name)
#         end_date_list.append(obj.end_date)
#         contract_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
#         major_mini_list.append(obj.mini_major)
#         Mini_major_Conn_Contract_list.append(obj.mini_major_connection)
#
#     data_position = pd.DataFrame({
#         "Contract Name": contract_name_list,
#         "End Date": end_date_list,
#         "kbbl MT Conversion": contract_unpriced_kbbl_mt_list,
#         "Major_Mini":major_mini_list,
#         "Mini_Conn_Contract":Mini_major_Conn_Contract_list,
#     })
#
#     print("position_data", data_position)
#
#     data_position['new'] = np.where((data_position['Major_Mini'] == 'Mini'), data_position['Mini_Conn_Contract'],
#                                     data_position['Contract Name'])
#     data_position['Contract Name'] = data_position['new']
#     print("data posioton last:",data_position)
#
#
#     ## data_position = data_position.loc[(data_position['Contract Name'] != 'LS GO 1st Line') & (data_position['Contract Name'] != 'Brent 1st Line') ]
#
#
#     if len(data_position)>0:
#
#         print("newdataframe:", data_position)
#         data_position = data_position[['End Date', 'kbbl MT Conversion', 'Contract Name']]
#         print('Before converting : ', data_position['End Date'].dtypes)
#         data_position['End Date'] = pd.to_datetime(data_position['End Date'])
#         data_position.set_index('End Date', inplace=True)
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#         print("positin data",data_position)
#         resampled = (data_position.resample('M').sum()).round(3)
#         resampled = (data_position.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#
#         # resampled = (position_data.groupby('Contract Name')['kbbl MT Conversion'].resample("M").sum()).reset_index().round(3)
#         resampled.reset_index(inplace=True)
#
#         resampled['End Date'] = resampled['End Date'].dt.strftime('01-%b-%y')
#
#         resampled.rename(columns={'End Date': 'Contract Month'}, inplace=True)
#
#         resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='kbbl MT Conversion')
#         resampled = resampled.rename_axis(None, axis=1)
#
#
#         print("resampled end:",resampled)
#
#         # resampled['End Date'] = pd.to_datetime(resampled['End Date'].dt.date)
#         # resampled = resampled.sort_values(by=['End Date'], ignore_index=True)
#
#     #  WORKING CODE FOR TOTAL IN DOWN
#
#         tot_data = resampled.copy()
#
#         sum_product_position = tot_data.sum(axis=0)
#         name_df = sum_product_position.to_frame(name='Total')
#         name_df.index.name = 'Products'
#         df_total = name_df
#         print("df total:",df_total)
#         df_total = name_df.transpose()
#         print("transpose:",df_total)
#         df_total.reset_index(inplace=True)
#         df_total.rename(columns={'index': 'Products'}, inplace=True)
#         print("rename df tptal:",df_total)
#
#         list_row = df_total.iloc[0].tolist()
#         print("list_row df list_row:", list_row)
#         data_new = resampled.copy()  # Create copy of DataFrame
#         data_new.reset_index(inplace=True)
#         data_new.loc[-1] = list_row
#         print("loc-1:",data_new)
#         data_new.index = data_new.index + 1  # Append list at the bottom
#         data_new = data_new.sort_index().reset_index(drop=True)
#
#         data_new.rename(columns={'Contract Month': 'Contract'}, inplace=True)
#
#         print("data swaps new:",data_new)
#     #
#     #
#     else:
#         data_new= pd.DataFrame()
#     #
#     print("return data for swaps kbbl:",data_new)
#     return (data_new)
#
#
#     #
#     # print("swap output new:", resampled)
#     #
#     # return render(request,'customer/fb_kbbl_position.html')
#
#
#     # return render(request, "customer/fb.html")
#


### SWAP POSITION KBBL DILLENA

# # swap_kbbl_position
def swaps_position_kbbl_company_name(company_name):

    company_name = company_name

    end_date_list = []
    contract_name_list = []
    contract_unpriced_kbbl_mt_list = []
    major_mini_list = []
    Mini_major_Conn_Contract_list = []
    singl_diff = []
    book_list=[]



    for obj in SwapBlotterModel.objects.filter(book=company_name).exclude(contract='Brent 1st Line').exclude(contract='Brent 1st Line Mini').exclude(contract='LS GO 1st Line').exclude(singl_dif='diff'):
        contract_name_list.append(obj.contract)
        end_date_list.append(obj.end_date)
        contract_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
        major_mini_list.append(obj.mini_major)
        Mini_major_Conn_Contract_list.append(obj.mini_major_connection)
        singl_diff.append(obj.singl_dif)
        book_list.append(obj.book)

    data_position = pd.DataFrame({
        "Contract Name": contract_name_list,
        "End Date": end_date_list,
        "Unpriced_kbbl_MT": contract_unpriced_kbbl_mt_list,
        "Major_Mini": major_mini_list,
        "Mini_Conn_Contract": Mini_major_Conn_Contract_list,
        'Diff_Single': singl_diff,
        'book':book_list
    })
    data_position = data_position.loc[(data_position['book'] == company_name)]

    if len(data_position) > 0:

        print("position_data", data_position)
        data_position['new'] = np.where((data_position['Major_Mini'] == 'mini'), data_position['Mini_Conn_Contract'],
                                        data_position['Contract Name'])
        data_position['Contract Name'] = data_position['new']
        print("position_data", data_position)
        data_position = data_position[['End Date', 'Unpriced_kbbl_MT', 'Contract Name']]
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position['Unpriced_kbbl_MT'] = data_position['Unpriced_kbbl_MT'].astype(float)
        data_position['End Date'] = pd.to_datetime(data_position['End Date'])
        data_position.set_index('End Date', inplace=True)

        resampled = (data_position.resample('M').sum()).round(3)
        resampled = (data_position.groupby('Contract Name')['Unpriced_kbbl_MT'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled['End Date'] = resampled['End Date'].dt.strftime('01-%b-%y')
        resampled.rename(columns={'End Date': 'Contract Month'}, inplace=True)
        resampled = resampled.pivot(index='Contract Month', columns='Contract Name', values='Unpriced_kbbl_MT')
        resampled = resampled.rename_axis(None, axis=1)

        tot_data = resampled.copy()
        sum_product_position = tot_data.sum(axis=0)
        name_df = sum_product_position.to_frame(name='Total')
        name_df.index.name = 'Products'
        df_total = name_df

        df_total = name_df.transpose()
        print("transpose:", df_total)
        df_total.reset_index(inplace=True)
        df_total.rename(columns={'index': 'Products'}, inplace=True)
        list_row = df_total.iloc[0].tolist()

        data_new = resampled.copy()  # Create copy of DataFrame
        data_new.reset_index(inplace=True)
        data_new.loc[-1] = list_row
        data_new.index = data_new.index + 1  # Append list at the bottom
        data_new = data_new.sort_index().reset_index(drop=True)

        data_new.rename(columns={'Contract Month': 'Contract'}, inplace=True)


    else:
        data_new = pd.DataFrame()

    print("swap posotion kbbl filter:",data_new)
    return (data_new)



###  filter kbbl in position 3rd
# def futures_equivalent_kbbl_company_name(f_equi):
#     print("future equivalent kbbl passed company name:",f_equi)
#     company_name = f_equi
#
#     # futures_position_kbbl_data = future_kbbl_position(request)
#     # swaps_position_kbbl_data = swap_kbbl_position(request)
#
#     mini_major_list = []
#     mini_major_connection_list = []
#     contract_name_list = []
#     firstmonth_list = []
#     secondmonth_list = []
#     futures_equiv_first_kbbl_list = []
#     futures_equiv_second_kbbl_list = []
#
#     company_name_filter = SwapBlottersModel.objects.filter(Book__name='CC')
#     print("futures equivalent company name:",company_name_filter)
#     print("lenth of company name:",len(company_name_filter))
#
#     print("type>",type(company_name_filter))
#
#     c = company_name_filter.filter(Contract_Name__contract_name='Brent Crude Futures')
#     print("cccc",c)
#
#
#
#     # for i in company_name_filter:
#
#
#
#
#     for obj in SwapBlottersModel.objects.filter(Q(Book__name=company_name) &
#                                                 (Q(Contract_Name__contract_name='Brent 1st Line')|
#                                                 Q(Contract_Name__contract_name='LS GO 1st Line')|
#                                                 Q(Contract_Name__contract_name='Brent 1st Line Mini')
#                                                 )):
#
#         # print("3 datas :", obj.id, obj.Contract_Name, obj.First_month, obj.Second_month)
#         print("object new:",obj)
#         print(type(obj.Contract_Name))
#         mini_major_list.append(obj.mini_major)
#         print("mini_major_list",mini_major_list)
#         mini_major_connection_list.append(obj.mini_major_connection)
#         contract_name_list.append(obj.Contract_Name)
#         firstmonth_list.append(obj.First_month)
#         secondmonth_list.append(obj.Second_month)
#         futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
#         futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
#     #
#     swaps_data = pd.DataFrame({"Major_Mini": mini_major_list,
#                                 "Major_Mini_Conn": mini_major_connection_list,
#                                 "Contract_Name": contract_name_list,
#                                 "First_Month": firstmonth_list,
#                                 "Second_Month": secondmonth_list,
#                                 "Futures_Equv_First_kbbl": futures_equiv_first_kbbl_list,
#                                 "Futures_Equv_Second_kbbl": futures_equiv_second_kbbl_list,
#
#                                   })
#     print("Swaps data for kbbl filter:", type(swaps_data['Futures_Equv_First_kbbl']))
#     print("data posioton swapdata:", swaps_data)
#
#
#     #
#     swaps_data['new'] = np.where((swaps_data['Major_Mini'] == 'Mini'),
#                                  swaps_data['Major_Mini_Conn'],swaps_data['Contract_Name'])
#
#     swaps_data['Contract_Name'] = swaps_data['new']
#     print("data posioton swapdata:",swaps_data['Contract_Name'])
#
#     # # print(type(swaps_data))
#
#     if len(swaps_data)>0:
#         print('working')
#
#         swaps_data_col = swaps_data.columns.tolist()
#         swaps_data_sub_first = swaps_data[['Contract_Name', 'First_Month', 'Futures_Equv_First_kbbl']].reset_index(
#             drop=True)
#         swaps_data_sub_first.rename(columns={'First_Month': 'Dates','Contract_Name':'Contract Name', 'Futures_Equv_First_kbbl': 'Futures EQV'},
#                                     inplace=True)
#         swaps_data_sub_first["Contract Name"] = swaps_data_sub_first["Contract Name"].values.astype('str')
#         swaps_data_sub_first = swaps_data_sub_first.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})
#
#         swaps_data_sub_second = swaps_data[['Contract_Name', 'Second_Month', 'Futures_Equv_Second_kbbl']].reset_index(
#             drop=True)
#         swaps_data_sub_second.rename(columns={'Second_Month': 'Dates', 'Contract_Name':'Contract Name','Futures_Equv_Second_kbbl': 'Futures EQV'},
#                                      inplace=True)
#
#         swaps_data_sub_second["Contract Name"] = swaps_data_sub_second["Contract Name"].values.astype('str')
#         swaps_data_sub_second = swaps_data_sub_second.groupby(["Dates", 'Contract Name'], as_index=False).agg(
#             {'Futures EQV': sum})
#
#         df = pd.concat([swaps_data_sub_first, swaps_data_sub_second],ignore_index=True)
#
#         print(df, 'beforedf++++fE test')
#     #
#         df=df.groupby(['Dates', 'Contract Name']).sum().reset_index()
#         df['Dates'] = pd.to_datetime(df['Dates'])
#         df['Dates'] = df['Dates'].dt.strftime('%d-%b-%y')
#         print(df,'df++++fE test')
#     else:
#
#         df = pd.DataFrame()
#
#     # FUTURES EQUIVALENT KBBL:
#
#
#     contract_name_list = []
#     Volume_kkbl_mt_list = []
#     contract_month_list = []
#     #
#     #
#     comp_filter_futures_blotter = FuturesBlottersModel.objects.filter(Book__name=company_name)
#     print("comp_filter_futures_blotter:",comp_filter_futures_blotter)
#
#     for obj in FuturesBlottersModel.objects.filter(
#             Q(Book__name=company_name) &
#             (Q(Contract_Name__contract_name='Brent Crude Futures') |
#             Q(Contract_Name__contract_name='LS Gas Oil Futures'))):
#         # print("3 datas :", obj.id, obj.Contract_Name, obj.First_month, obj.Second_month)
#         print("object:", obj)
#         print(type(obj.Contract_Name))
#         contract_name_list.append(obj.Contract_Name)
#         contract_month_list.append(obj.Contract_Month)
#         Volume_kkbl_mt_list.append(obj.kbbl_mt_conversion)
#         print("Volume_kkbl_mt_list:",Volume_kkbl_mt_list)
#     #  #
#     data_position = pd.DataFrame({
#                                "Contract_Name": contract_name_list,
#                                 "Contract_Month":contract_month_list,
#                                 "Volume_kbbl_MT": Volume_kkbl_mt_list,
#
#
#                                })
#
#     print("data_position test futures company name:",data_position)
#     if len(data_position)>0:
#         print("hello inside")
#
#         data_position['Volume_kbbl_MT'] = data_position['Volume_kbbl_MT'].astype(float)
#         data_position.rename( columns = {'Volume_kbbl_MT': 'Futures EQV', 'Contract_Month': 'Dates', 'Contract_Name': 'Contract Name'},inplace = True)
#
#         data_position.Dates = pd.to_datetime(data_position.Dates)
#
#         data_position = data_position[['Dates', 'Contract Name', 'Futures EQV']]
#
#         data_position['Dates'] = pd.to_datetime(data_position['Dates'])
#
#         data_position['Dates'] = data_position['Dates'].dt.strftime('%d-%b-%y')
#
#
#
#         print("chekcing .......................................")
#     #
#     else:
#         print("inside else:")
#         data_position = pd.DataFrame()
#
#
#     print(data_position,'++++++++++++++++++++both eqv+++++++++++++++++++++++++')
#
#     try:
#         df["Contract Name"] = df["Contract Name"].values.astype('str')
#         df['Contract Name'] = df['Contract Name'].replace(['Brent 1st Line', 'LS GO 1st Line'], ['Brent Crude Futures', 'LS Gas Oil Futures'])
#         data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
#
#         df_final = pd.concat([df, data_position]).groupby(['Dates', 'Contract Name']).sum().reset_index()
#         print(df_final,'df_final')
#         if len(df_final) > 0:
#             df_final = df_final.replace(np.nan, '-')
#         #
#             contract_name = df_final['Contract Name'].unique().tolist()
#
#
#             contracts_sorted = sorted(contract_name)
#             contract_name = contracts_sorted
#
#             dataframe_list = []
#             for i in contract_name:
#                 futures_eqv_list = []
#
#                 subset = df_final[df_final["Contract Name"] == i]
#
#                 i = str(i) + '-' + 'EQV'
#
#                 for index, row in subset.iterrows():
#                     futures_eqv = {}
#                     futures_eqv['Dates'] = row['Dates']
#
#                     futures_eqv[i] = row['Futures EQV']
#
#                     futures_eqv_list.append(futures_eqv)
#
#                     df = pd.DataFrame(futures_eqv_list)
#                     df = round(df, 2)
#                 dataframe_list.append(df)
#     #
#             data_merge = reduce(lambda left, right:  # Merge DataFrames in list
#                                 pd.merge(left, right,
#                                          on=["Dates"],
#                                          how="outer"),
#                                 dataframe_list)
#
#             data_merge = data_merge.replace(np.nan, '-')
#
#             data_merge['Dates'] = pd.to_datetime(data_merge['Dates'])
#             data_merge = data_merge.sort_values(by='Dates').reset_index(drop=True)
#             data_merge.rename(columns={'Dates': 'Contract'}, inplace=True)
#
#             data_merge['Contract'] = data_merge['Contract'].dt.strftime('%d-%b-%y')
#
#             tot_data = data_merge.copy()
#
#             tot_data = data_merge.replace(to_replace="-", value=0.0)
#             tot_data.drop('Contract', inplace=True, axis=1)
#
#             sum_product_position = tot_data.sum(axis=0)
#
#             name_df = sum_product_position.to_frame(name='Total')
#
#             df_total = name_df
#             df_total = name_df.transpose()
#             df_total = df_total.round(2)
#
#             df_total.reset_index(inplace=True)
#             df_total.rename(columns={'index': 'Products'}, inplace=True)
#
#             list_row = df_total.iloc[0].tolist()
#
#             data_new = data_merge.copy()  # Create copy of DataFrame
#             data_new.loc[-1] = list_row
#             data_new.index = data_new.index + 1
#             futures_equivalent_df = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#
#         else:
#             futures_equivalent_df = pd.DataFrame()
#
#     except:
#         futures_equivalent_df = pd.DataFrame()
#
#
#     print(futures_equivalent_df,'futures_equivalent_df+++++++++test')
#
#     # futures_position_kbbl_data = future_kbbl_position(request)
#     # swaps_position_kbbl_data = swap_kbbl_position(request)
#
#     # print("futures_position_kbbl_data:",futures_position_kbbl_data)
#     # print("swaps_position_kbbl_data:", swaps_position_kbbl_data)
#     print("returned data form future equivalent:",futures_equivalent_df)
#     print()
#     return (futures_equivalent_df)
#
#
#     # context = {
#     #
#     #     'futures_position_kbbl_data':futures_position_kbbl_data,
#     #     'swaps_position_kbbl_data': swaps_position_kbbl_data,
#     #     'futures_df':futures_equivalent_df,
#     #     'swaps_df': df
#     #
#     #
#     # }
#     #
#     # return render(request,'customer/swap_data_kbbl.html')


###### FUTURES EQUIVALENT COMPANY DILLNENA

def futures_equivalent_kbbl_company_name(company_name):

    company_name=company_name

    mini_major_list = []
    mini_major_connection_list = []
    contract_name_list = []
    firstmonth_list = []
    secondmonth_list = []
    futures_equiv_first_kbbl_list = []
    futures_equiv_second_kbbl_list = []
    book_list=[]

    for obj in SwapBlotterModel.objects.filter(Q(book=company_name) &
            Q(contract='Brent 1st Line') | Q(contract='LS GO 1st Line') | Q(contract='Brent 1st Line Mini')):

        mini_major_list.append(obj.mini_major)
        mini_major_connection_list.append(obj.mini_major_connection)
        contract_name_list.append(obj.contract)
        firstmonth_list.append(obj.First_month)
        secondmonth_list.append(obj.Second_month)
        futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
        futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
        book_list.append(obj.book)



    #
    swaps_data = pd.DataFrame({"Major_Mini": mini_major_list,
                               "Major_Mini_Conn": mini_major_connection_list,
                               "Contract_Name": contract_name_list,
                               "First_Month": firstmonth_list,
                               "Second_Month": secondmonth_list,
                               "Futures_Equv_First_kbbl": futures_equiv_first_kbbl_list,
                               "Futures_Equv_Second_kbbl": futures_equiv_second_kbbl_list,
                               'book':book_list

                               })

    swaps_data = swaps_data.loc[(swaps_data['book'] == company_name)]
    print(swaps_data, 'swaps_databooklist')

    swaps_data['new'] = np.where((swaps_data['Major_Mini'] == 'mini'), swaps_data['Major_Mini_Conn'],
                                 swaps_data['Contract_Name'])
    swaps_data['Contract_Name'] = swaps_data['new']
    print("data posioton swapdata:", swaps_data['Contract_Name'])

    if len(swaps_data) > 0:

        swaps_data_col = swaps_data.columns.tolist()
        swaps_data_sub_first = swaps_data[['Contract_Name', 'First_Month', 'Futures_Equv_First_kbbl']].reset_index(drop=True)
        swaps_data_sub_first.rename(columns={'First_Month': 'Dates', 'Contract_Name': 'Contract Name','Futures_Equv_First_kbbl': 'Futures EQV'},inplace=True)
        swaps_data_sub_first["Contract Name"] = swaps_data_sub_first["Contract Name"].values.astype('str')
        swaps_data_sub_first = swaps_data_sub_first.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})

        swaps_data_sub_second = swaps_data[['Contract_Name', 'Second_Month', 'Futures_Equv_Second_kbbl']].reset_index(drop=True)
        swaps_data_sub_second.rename(columns={'Second_Month': 'Dates', 'Contract_Name': 'Contract Name','Futures_Equv_Second_kbbl': 'Futures EQV'},inplace=True)

        swaps_data_sub_second["Contract Name"] = swaps_data_sub_second["Contract Name"].values.astype('str')
        swaps_data_sub_second = swaps_data_sub_second.groupby(["Dates", 'Contract Name'], as_index=False).agg({'Futures EQV': sum})

        print(swaps_data_sub_second,'swaps_data_sub_second')

        df = pd.concat([swaps_data_sub_first, swaps_data_sub_second]).groupby(['Dates', 'Contract Name']).sum().reset_index()

        # df = df.
        df['Dates'] = pd.to_datetime(df['Dates'])
        df['Dates'] = df['Dates'].dt.strftime('%d-%b-%y')
        # print(df, 'df++++fE test')

        df["Contract Name"] = df["Contract Name"].values.astype('str')

        df['Contract Name'] = df['Contract Name'].replace(['Brent 1st Line', 'LS GO 1st Line'],
                                                          ['Brent Crude Futures', 'LS Gas Oil Futures'])
    else:

        df = pd.DataFrame()

    # FUTURES EQUIVALENT KBBL:

    contract_name_list = []
    Volume_kkbl_mt_list = []
    contract_month_list = []
    futures_book=[]
    print('company_name',company_name)

    for obj in FutureBlotterModel.objects.filter(Q(book=company_name) & Q(contract='Brent Crude Futures') | Q(contract='LS Gas Oil Futures')):


        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        Volume_kkbl_mt_list.append(obj.kbbl_mt_conversion)
        futures_book.append(obj.book)
    #
    data_position = pd.DataFrame({
        "Contract_Name": contract_name_list,
        "Contract_Month": contract_month_list,
        "Volume_kbbl_MT": Volume_kkbl_mt_list,
        'book':futures_book

    })
    data_position = data_position.loc[(data_position['book'] == company_name)]

    if len(data_position) > 0:

        data_position['Volume_kbbl_MT'] = data_position['Volume_kbbl_MT'].astype(float)
        data_position.rename(
            columns={'Volume_kbbl_MT': 'Futures EQV', 'Contract_Month': 'Dates', 'Contract_Name': 'Contract Name'},
            inplace=True)

        data_position.Dates = pd.to_datetime(data_position.Dates)
        data_position = data_position[['Dates', 'Contract Name', 'Futures EQV']]
        data_position["Contract Name"] = data_position["Contract Name"].values.astype('str')
        data_position['Dates'] = pd.to_datetime(data_position['Dates'])
        data_position['Dates'] = data_position['Dates'].dt.strftime('%d-%b-%y')

    else:
        data_position = pd.DataFrame()


    # try:
    print(data_position, 'dftest')

    if len(df) > 0 and len(data_position) > 0:

        df_final = pd.concat([df, data_position]).groupby(['Dates', 'Contract Name']).sum().reset_index()

    elif len(df) > 0 and len(data_position) == 0:

        df_final = df.groupby(['Dates', 'Contract Name']).sum().reset_index()

    elif len(data_position) > 0 and len(df) == 0:
        df_final = data_position.groupby(['Dates', 'Contract Name']).sum().reset_index()

    else:
        df_final = pd.DataFrame()

    if len(df_final) > 0:

        df_final = df_final.replace(np.nan, '-')
        contract_name = df_final['Contract Name'].unique().tolist()

        contracts_sorted = sorted(contract_name)
        contract_name = contracts_sorted

        dataframe_list = []
        for i in contract_name:
            futures_eqv_list = []

            subset = df_final[df_final["Contract Name"] == i]

            i = str(i) + '-' + 'EQV'

            for index, row in subset.iterrows():
                futures_eqv = {}
                futures_eqv['Dates'] = row['Dates']

                futures_eqv[i] = row['Futures EQV']

                futures_eqv_list.append(futures_eqv)

                df = pd.DataFrame(futures_eqv_list)
                df = round(df, 2)
            dataframe_list.append(df)

        data_merge = reduce(lambda left, right:  # Merge DataFrames in list
                            pd.merge(left, right,
                                     on=["Dates"],
                                     how="outer"),
                            dataframe_list)

        data_merge = data_merge.replace(np.nan, '-')

        data_merge['Dates'] = pd.to_datetime(data_merge['Dates'])
        data_merge = data_merge.sort_values(by='Dates').reset_index(drop=True)
        data_merge.rename(columns={'Dates': 'Contract'}, inplace=True)

        data_merge['Contract'] = data_merge['Contract'].dt.strftime('%d-%b-%y')

        tot_data = data_merge.copy()

        tot_data = data_merge.replace(to_replace="-", value=0.0)
        tot_data.drop('Contract', inplace=True, axis=1)

        sum_product_position = tot_data.sum(axis=0)

        name_df = sum_product_position.to_frame(name='Total')

        df_total = name_df
        df_total = name_df.transpose()
        df_total = df_total.round(2)

        df_total.reset_index(inplace=True)
        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()

        data_new = data_merge.copy()  # Create copy of DataFrame
        data_new.loc[-1] = list_row
        data_new.index = data_new.index + 1
        futures_equivalent_df = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

    else:
        futures_equivalent_df = pd.DataFrame()

    # except:
    #     futures_equivalent_df = pd.DataFrame()

    print("futures_equivalent_df:",futures_equivalent_df)
    return (futures_equivalent_df)

# *************************** PLEASE NOTE THIS IMPORTANT-1 **********************
###  filter for kbbl total , also included lots total to pass into same page


# def total_kbbl_trade_position_companyName(company_name):
#     print("hello company name:",company_name)
#     print("data from future_position_kbbl_company_name: ",future_position_kbbl_company_name(company_name))
#     print("swaps_position_kbbl_company_name",swaps_position_kbbl_company_name(company_name))
#     print("futures_equivalent_kbbl_company_name:",futures_equivalent_kbbl_company_name(company_name))
#
#     futures_position_data = future_position_kbbl_company_name(company_name)
#     swaps_position_data = swaps_position_kbbl_company_name(company_name)
#     futures_equivalent_data = futures_equivalent_kbbl_company_name(company_name)
#
#   # WORKING CODE
#     # total_fbsb_trade_position_data = total_fbsb_trade_position_lots_companyname(request)
#     # futures_position_data = future_position_kbbl_company_name(request)
#     # print("checking futures_position_data:",futures_position_data)
#     # swaps_position_data = swaps_position_kbbl_company_name(request)
#     # print("checking swaps_position_data:", futures_position_data)
#     # futures_equivalent_data = futures_equivalent_kbbl_company_name(request)
#     # print("checking futures_equivalent_data:", futures_equivalent_data)
#
#
#     print('++++++++++++++++totall summary')
#     print(futures_position_data,'futures_position_data')
#     print(swaps_position_data, 'swaps_position_data')
#     print(futures_equivalent_data, 'futures_equivalent_data')
#
#
#     if len(futures_position_data) > 0 or len(swaps_position_data) or len(futures_equivalent_data):
#
#         futures_col_len = futures_position_data.copy()
#         futures_col_len = futures_col_len.set_index('Contract') if len(futures_position_data) > 0 else futures_col_len
#         Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(futures_position_data) > 0 else []
#
#         swaps_col_len = swaps_position_data.copy()
#         swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
#         swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#
#         FE_len = futures_equivalent_data.copy()
#         FE_column_name_list = len(FE_len.columns) * ['Futures  '] if len(futures_equivalent_data) > 0 else []
#         cols_len = len(futures_equivalent_data.columns)
#
#         if cols_len > 0:
#             FE_column_name_list[0] = 'Contract Month'
#         elif len(Futures_column_name_list) > 0 or len(swaps_column_name_list) > 0:
#             FE_column_name_list.append('Contract Month')
#         elif cols_len == 0 and len(Futures_column_name_list) == 0 and len(swaps_column_name_list) == 0:
#             FE_column_name_list = []
#
#         Column_dist_list = FE_column_name_list + Futures_column_name_list + swaps_column_name_list
#
#         print(Column_dist_list,'Column_dist_list')
#
#         futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
#         swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
#         FE_date = futures_equivalent_data['Contract'][1:].tolist() if len(futures_equivalent_data) > 0 else []
#         date_list = futures_date + swaps_date + FE_date
#
#         print(date_list,'date_list')
#
#         if len(date_list) > 0:
#             date_list = pd.to_datetime(date_list, format='%d-%b-%y')
#             date_list = date_list.to_list()
#
#             min_date = min(date_list)
#             max_date = max(date_list)
#
#         date_generated = pd.date_range(min_date, max_date, freq='MS')
#         df = pd.DataFrame(date_generated, columns=['Contract'])
#
#         df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')
#
#         print('df_contract',futures_equivalent_data)
#
#         Outer_join = pd.merge(df, futures_equivalent_data, on='Contract', how='outer') if len(
#             futures_equivalent_data) > 0 else df
#         FE_label = len(futures_equivalent_data.columns)
#         print(FE_label,'FE_label')
#         #
#         Outer_join = pd.merge(Outer_join, futures_position_data, on='Contract', how='outer') if len(
#             futures_position_data) > 0 else Outer_join
#
#         Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
#             swaps_position_data) > 0 else Outer_join
#
#
#         print(Outer_join,'Outer_join++++++')
#         #
#         outer_join_columns = Outer_join.columns.tolist()
#         #
#         # #
#         Outer_join.columns = Column_dist_list
#         Outer_join.loc[-1] = outer_join_columns
#         Outer_join.index = Outer_join.index + 1
#         Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#
#         #
#         # #
#         Outer_join.to_csv('Outer_Join.csv')
#         copy_whole_data = Outer_join.copy()
#         copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
#         print(copy_whole_data, 'copy_whole_data')
#
#         copy_whole_data.set_index('Contract Month', inplace=True)
#
#         copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
#         copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
#
#
#         #
#         # print('copy_whole_data++++++++',copy_whole_data)
#         # #
#         # #
#         total = copy_whole_data['Total'].tolist()
#         # # # print('whole_position',whole_position)
#         Outer_join['Total (kbbl)'] = total
#         # Outer_join.at[0,'Total (kbbl/MT)'] = '-'
#         print(Outer_join, 'Outer_join++++++++final test+++++++++++++')
#         #
#         Outer_join.replace(to_replace=['Brent Crude Futures-EQV', ' LS Gas Oil Futures-EQV'], value=['Brent Crude Futures', 'LS Gas Oil Futures'],
#                            inplace=True)
#         # #
#         Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
#         #
#         # Outer_join_tot_col = Outer_join['Total (kbbl/MT)']
#         # Outer_join = Outer_join.drop(columns=['Total (kbbl/MT)'])
#         # Outer_join.insert(loc=1, column='Total (kbbl/MT)', value=Outer_join_tot_col)
#         # #
#             # print('final', Outer_join)
#     else:
#         Outer_join = pd.DataFrame()
#
#     print(Outer_join,'Final output kbbl position++++++++++++++')
#     print("get value total_fbsb_trade_position_lots",total_fbsb_trade_position_lots)
#     Outer_join_copy = Outer_join
#     print("outerb join to send:",Outer_join)
#     return (Outer_join)
#
#     # context = {
#     #     'total_fbsb_trade_position_lots': total_fbsb_trade_position_data,
#     #     'kbbl_total_position':Outer_join,
#     #
#     # }
#     #
#     # return render(request,"customer/fbsb_tot_position.html",context)





##### TOTAL KBBL TRADE POSITIN COMPANYNAME DILLEENA


def total_kbbl_trade_position_companyName(company_name):

    # total_fbsb_trade_position_data = total_fbsb_trade_position_lots(request)
    # total_kbbl_position_companyName = request.session.get('final_out_kbbl')
    # print("total_kbbl_position_companyName:",total_kbbl_position_companyName)

    company_name= company_name
    print("company_name:",company_name)
    futures_position_data = future_position_kbbl_company_name(company_name)
    swaps_position_data = swaps_position_kbbl_company_name(company_name)
    futures_equivalent_data = futures_equivalent_kbbl_company_name(company_name)

    print(futures_position_data,'futures_position_data')
    print(swaps_position_data,'swaps_position_data')
    print(futures_equivalent_data,'futures_equivalent_data')

    if len(futures_position_data) > 0 or len(swaps_position_data)>0 or len(futures_equivalent_data)>0:

        futures_col_len = futures_position_data.copy()
        futures_col_len = futures_col_len.set_index('Contract') if len(futures_position_data) > 0 else futures_col_len
        Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(futures_position_data) > 0 else []

        swaps_col_len = swaps_position_data.copy()
        swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
        swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []

        FE_len = futures_equivalent_data.copy()
        FE_column_name_list = len(FE_len.columns) * ['Futures  '] if len(futures_equivalent_data) > 0 else []
        cols_len = len(futures_equivalent_data.columns)

        if cols_len > 0:
            FE_column_name_list[0] = 'Contract Month'
        elif len(Futures_column_name_list) > 0 or len(swaps_column_name_list) > 0:
            FE_column_name_list.append('Contract Month')
        elif cols_len == 0 and len(Futures_column_name_list) == 0 and len(swaps_column_name_list) == 0:
            FE_column_name_list = []

        Column_dist_list = FE_column_name_list + Futures_column_name_list + swaps_column_name_list

        futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
        swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
        FE_date = futures_equivalent_data['Contract'][1:].tolist() if len(futures_equivalent_data) > 0 else []
        date_list = futures_date + swaps_date + FE_date


        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])
        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')


        Outer_join = pd.merge(df, futures_equivalent_data, on='Contract', how='outer') if len(
            futures_equivalent_data) > 0 else df
        FE_label = len(futures_equivalent_data.columns)

        Outer_join = pd.merge(Outer_join, futures_position_data, on='Contract', how='outer') if len(
            futures_position_data) > 0 else Outer_join

        Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
            swaps_position_data) > 0 else Outer_join

        outer_join_columns = Outer_join.columns.tolist()
        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
        copy_whole_data.set_index('Contract Month', inplace=True)
        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        total = copy_whole_data['Total'].tolist()
        Outer_join['Total (kbbl)'] = total
        # Outer_join.at[0,'Total (kbbl/MT)'] = '-'
        Outer_join.replace(to_replace=['Brent Crude Futures-EQV', 'LS Gas Oil Futures-EQV'], value=['Brent Crude Futures', 'LS Gas Oil Futures'], inplace=True)
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
        position_kbbl_indvidual_company = Outer_join

        # Outer_join_tot_col = Outer_join['Total (kbbl/MT)']
        # Outer_join = Outer_join.drop(columns=['Total (kbbl/MT)'])
        # Outer_join.insert(loc=1, column='Total (kbbl/MT)', value=Outer_join_tot_col)
        # #
            # print('final', Outer_join)
    else:
        position_kbbl_indvidual_company = pd.DataFrame()


    print(position_kbbl_indvidual_company,'position_kbbl_allcompany')

    book = Book.objects.all()


    print("position_kbbl_indvidual_company:",position_kbbl_indvidual_company)
    return (position_kbbl_indvidual_company)


# ************************************ Lots company name filtering **********************************
#
# def futures_lot_position_companyname(company_name):
#     company_name = company_name
#     contract_month_list = []
#     contract_name_list = []
#     contract_volume_list = []
#     for obj in FutureBlotterModel.objects.filter(book=company_name):
#         print("3 datas :",obj.id,obj.contract,obj.Contract_Month,obj.volume)
#         contract_name_list.append(obj.contract)
#         contract_month_list.append(obj.Contract_Month)
#         contract_volume_list.append(obj.volume)
#
#     position_data= pd.DataFrame({"contract_month":contract_month_list,
#                                 "contract_name": contract_name_list,
#                                 "Volume": contract_volume_list,
#                                 })
#
#     if len(position_data)>0:
#         print("newdataframe:", position_data)
#         print(contract_month_list)
#         print("future contract")
#         position_data = position_data[['contract_month', 'Volume', 'contract_name']]
#         print('Before converting : ', position_data['contract_month'].dtypes)
#         position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
#         print('After  converting : ', position_data['contract_month'].dtypes)
#         print("type of date time :", type(position_data['contract_month']))
#         print("position new data:", position_data.columns)
#         position_data.set_index('contract_month', inplace=True)
#         #
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         #
#         print("position new data:", position_data)
#         #
#         position_data["contract_name"] = position_data["contract_name"].values.astype('str')
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         print("###################################################################")
#         print("resampled:", resampled)
#         print("type of contract name ", type(position_data["contract_name"]))
#         # #
#         resampled.reset_index(inplace=True)
#         resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')
#
#         resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
#         resampled = resampled.rename_axis(None, axis=1)
#         print("resampled pivot:")
#         print(resampled)
#     else:
#         resampled= pd.DataFrame()
#     print("neww")
#
#     print("resampled:",resampled)
#
#     return (resampled)

    # context = {
    #
    #
    # }
    # return render(request,"user/dashboard.html",context)
    # return render(request, "customer/dash2.html")





#+++++++++++++++++++++++++Position in Lots Individual Company+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def futures_lot_position_companyname(company_name):

    company_name = company_name
    contract_month_list = []
    contract_name_list = []
    contract_volume_list = []
    book_list=[]
    for obj in FutureBlotterModel.objects.filter(book=company_name):
        print("3 datas :",obj.id,obj.contract,obj.Contract_Month,obj.volume)
        contract_name_list.append(obj.contract)
        contract_month_list.append(obj.Contract_Month)
        contract_volume_list.append(obj.volume)
        book_list.append(obj.book)

    position_data= pd.DataFrame({"contract_month":contract_month_list,
                                "contract_name": contract_name_list,
                                "Volume": contract_volume_list,
                                 "Book":book_list
                                })

    position_data = position_data.loc[(position_data['Book'] == company_name)]

    if len(position_data)>0:

        position_data = position_data[['contract_month', 'Volume', 'contract_name']]
        position_data['Volume'] = position_data['Volume'].astype(float)
        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='Volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)

        if len(resampled)>0:

            tot_data = resampled.copy()
            tot_data.drop('contract_month', inplace=True, axis=1)
            tot_data = tot_data.replace(to_replace="-", value=0.0)

            sum_product_position = tot_data.sum(axis=0)

            name_df = sum_product_position.to_frame(name='Total(lots)')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()

            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame

            data_new = data_new.rename(columns={'contract_month': 'Contract'})
            cols_new = list(data_new.columns)
        else:
            data_new = pd.DataFrame()

    else:
        data_new= pd.DataFrame()


    return (data_new)






# ########### swaps lots  filter company name

# # swap_lot_position
# def swap_lot_position_companyname(company_name):
#     company_name = company_name
#     contract_end_date_list = []
#     contract_name_list = []
#     contract_unprice_volume_list = []
#     for obj in SwapBlotterModel.objects.filter(book=company_name):
#         print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
#         contract_name_list.append(obj.contract)
#         contract_end_date_list.append(obj.end_date)
#         contract_unprice_volume_list.append(obj.unpriced_volume)
#
#     position_data= pd.DataFrame({"contract_month":contract_end_date_list,
#                                 "contract_name": contract_name_list,
#                                 "unprice_volume": contract_unprice_volume_list,
#                                 })
#
#     if len(position_data)>0:
#         print("swap contact")
#         print("newdataframe:", position_data)
#         print(contract_end_date_list)
#         position_data = position_data[['contract_month', 'unprice_volume', 'contract_name']]
#         print('Before converting : ', position_data['contract_month'].dtypes)
#         position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
#         print('After  converting : ', position_data['contract_month'].dtypes)
#         print("type of date time :", type(position_data['contract_month']))
#         position_data.set_index('contract_month', inplace=True)
#
#         # position_data = position_data[['Contract_Name_id', 'Volume']]
#         position_data["contract_name"] = position_data["contract_name"].values.astype('str')
#         print("positin data22",position_data)
#         # resampled = (position_data.resample('M').sum()).round(3)
#         # resampled = (position_data.groupby('contract_name')['Volume'].resample("M").sum()).reset_index().round(3)
#
#         resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(3)
#         resampled.reset_index(inplace=True)
#         # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
#         resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
#         resampled = resampled.rename_axis(None, axis=1)
#     else:
#         resampled= pd.DataFrame()
#
#     print("swap output:", resampled)
#
#
#     print("resampled:",resampled)
#     return (resampled)
#     print("end of swap ")
    # context = {
    # #     # 'resampled_swap':resampled.to_html(),
    # #     # 'position_data':position_data.to_html(),
    # #
    #  }
    # return render(request,"customer/dash_swap.html",context)




# # swap_lot_position
def swap_lot_position_companyname(company_name):
    contract_end_date_list = []
    contract_name_list = []
    contract_unprice_volume_list = []
    diff_single_list=[]
    book_list=[]

    for obj in SwapBlotterModel.objects.all():
        print("3 datas :",obj.id,obj.contract,obj.end_date,obj.unpriced_volume)
        contract_name_list.append(obj.contract)
        contract_end_date_list.append(obj.end_date)
        contract_unprice_volume_list.append(obj.unpriced_volume)
        diff_single_list.append(obj.singl_dif)
        book_list.append(obj.book)

    position_data= pd.DataFrame({"contract_month":contract_end_date_list,
                                "contract_name": contract_name_list,
                                "unprice_volume": contract_unprice_volume_list,
                                 "Diff_Single":diff_single_list,
                                 "Book":book_list
                                })
    position_data = position_data.loc[(position_data['Book'] == company_name)]

    if len(position_data)>0:

        position_data = position_data[['contract_month', 'unprice_volume', 'contract_name','Diff_Single']]

        position_data['contract_month'] = pd.to_datetime(position_data['contract_month'])
        position_data['unprice_volume'] = position_data['unprice_volume'].astype(float)
        position_data["contract_name"] = position_data["contract_name"].values.astype('str')
        position_data["Diff_Single"] = position_data["Diff_Single"].values.astype('str')
        position_data = position_data.loc[(position_data['Diff_Single'] != 'diff')]
        position_data.set_index('contract_month', inplace=True)

        resampled = (position_data.groupby('contract_name')['unprice_volume'].resample("M").sum()).reset_index().round(2)

        # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
        resampled = resampled.pivot(index='contract_month', columns='contract_name', values='unprice_volume')
        resampled = resampled.rename_axis(None, axis=1)
        resampled.reset_index(inplace=True)

        resampled.contract_month = resampled.contract_month.dt.strftime('01-%b-%y')

        if len(resampled) > 0:

            tot_data = resampled.copy()
            tot_data.drop('contract_month', inplace=True, axis=1)

            tot_data = tot_data.replace(to_replace="-", value=0.0)

            total_sum_lots = tot_data.sum().to_frame().transpose()
            sum_product_position = tot_data.sum(axis=0)

            name_df = sum_product_position.to_frame(name='Total(lots)')
            name_df.index.name = 'Products'

            df_total = name_df
            df_total = name_df.transpose()

            df_total.reset_index(inplace=True)
            df_total.rename(columns={'index': 'Products'}, inplace=True)

            list_row = df_total.iloc[0].tolist()
            data_new = resampled.copy()  # Create copy of DataFrame
            data_new.loc[-1] = list_row
            data_new.index = data_new.index + 1  # Append list at the bottom
            data_new = data_new.sort_index().reset_index(drop=True)
            data_new = data_new.rename(columns={'contract_month': 'Contract'})
        else:
            data_new = pd.DataFrame()

        print("swap output:", data_new)

    else:
        data_new= pd.DataFrame()

    return (data_new)










#total fb sb postion for company name
# def total_fbsb_trade_position_lots_companyname(company_name):
#     # print("company bname args",company_name)
#     # print("company name totol lots company:",company_name)
#     print("hello")
#     futures_position_data = futures_lot_position_companyname(company_name)
#     swaps_position_data = swap_lot_position_companyname(company_name)
#
#     print("swaps error:",swaps_position_data)
#     futures_position_data.reset_index(inplace=True)
#     swaps_position_data.reset_index(inplace=True)
#
#     if len(futures_position_data)>0:
#         futures_position_data["contract_month"]= pd.to_datetime(futures_position_data["contract_month"])
#         futures_position_data.contract_month = futures_position_data.contract_month.dt.strftime('01-%b-%y')
#         #     #covert date time format
#         futures_position_data["contract_month"] = pd.to_datetime(futures_position_data["contract_month"])
#
#     else:
#         pass
#     if len(swaps_position_data)>0:
#         swaps_position_data["contract_month"]= pd.to_datetime(swaps_position_data["contract_month"])
#         swaps_position_data.contract_month = swaps_position_data.contract_month.dt.strftime('01-%b-%y')
#         # #covert date time format
#         swaps_position_data["contract_month"] = pd.to_datetime(swaps_position_data["contract_month"])
#     else:
#         pass
#
#     print("futures_position_data",futures_position_data)
#     print("swaps_position_data", swaps_position_data)
# #
#
#
#     print("futures_position_data",futures_position_data.columns)
#     print("swaps_position_data",swaps_position_data.columns)
#
#     if len(futures_position_data) > 0 or len(swaps_position_data) > 0:
#
#         if len(futures_position_data) > 0:
#
#             futures_col_len = futures_position_data.copy()
#             Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
#                 futures_position_data) > 0 else []
#             Futures_column_name_list[0] = 'contract_month' if len(futures_col_len.columns) > 1 else []
#
#             swaps_col_len = swaps_position_data.copy()
#             swaps_col_len = swaps_col_len.set_index('contract_month') if len(swaps_position_data) > 0 else swaps_col_len
#             swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#
#         elif len(swaps_position_data) > 0 and len(futures_position_data) == 0:
#             swaps_col_len = swaps_position_data.copy()
#             swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
#             swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
#             Futures_column_name_list = []
#
#         elif len(swaps_position_data) == 0 and len(futures_position_data) == 0:
#
#             Futures_column_name_list = []
#             swaps_column_name_list = []
#
#         Column_dist_list = Futures_column_name_list + swaps_column_name_list
# #
# #
#     print("Futures_column_name_list :",Futures_column_name_list)
#     print("swaps_column_name_list :",swaps_column_name_list)
#     Column_dist_list = Futures_column_name_list + swaps_column_name_list
#     print("Column_dist_list:",Column_dist_list)
#     #
#     futures_date = futures_position_data['contract_month'].tolist() if len(futures_position_data) > 0 else []
#     swaps_date = swaps_position_data['contract_month'].tolist() if len(swaps_position_data) > 0 else []
#     date_list = futures_date + swaps_date
#
#     print("date list:", date_list)
#
#     if len(date_list) > 0:
#         date_list = pd.to_datetime(date_list, format='%Y-%m-%d')
#         date_list = date_list.to_list()
#
#         min_date = min(date_list)
#         max_date = max(date_list)
#
#     date_generated = pd.date_range(min_date, max_date, freq='MS')
#     df = pd.DataFrame(date_generated, columns=['contract_month'])
#
#     df['contract_month'] = df['contract_month'].dt.strftime('%d-%b-%y')
#     if len(futures_position_data)>0:
#         futures_position_data['contract_month'] = futures_position_data['contract_month'].dt.strftime('%d-%b-%y')
#     if len(swaps_position_data) > 0:
#         swaps_position_data['contract_month'] = swaps_position_data['contract_month'].dt.strftime('%d-%b-%y')
#
#     print("date generated:", df)
#     #
#     Outer_join = pd.merge(df, futures_position_data, on='contract_month', how='outer') if len(
#         futures_position_data) > 0 else df
#     futures_label = len(futures_position_data.columns)
#     print(futures_label)
#
#     Outer_join = pd.merge(Outer_join, swaps_position_data, on='contract_month', how='outer') if len(
#         swaps_position_data) > 0 else Outer_join
#
#     Outer_join.columns = Outer_join.columns.str.rstrip("_x")
#     Outer_join.columns = Outer_join.columns.str.rstrip("_y")
#
#     outer_join_columns = Outer_join.columns.tolist()
#
#     Outer_join.columns = Column_dist_list
#     Outer_join.loc[-1] = outer_join_columns
#     Outer_join.index = Outer_join.index + 1
#     Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame
#
#     Outer_join.to_csv('Outer_Join.csv')
#     copy_whole_data = Outer_join.copy()
#     copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)
#
#     copy_whole_data.set_index('contract_month', inplace=True)
#
#     copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
#     copy_whole_data['Total'] = round(copy_whole_data['Total'], 3)
#     #
#     total = copy_whole_data['Total'].tolist()
#     # # print('whole_position',whole_position)
#     Outer_join['Total(lots/statement)'] = total
#     Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)
#
#
#     print("Outer_join:",Outer_join)
#     print("outerjoin.colum", Outer_join.columns)
#
#     Outer_join.columns = Outer_join.columns.str.strip()
#     # table_columns = Outer_join.columns.to_list()
#     # row_data = list(Outer_join._values.tolist())
#     # print("row data:",row_data)
#     print("outerjoin before send:",Outer_join)
#     print("total lots fbsb compnay filter:",Outer_join)
#     return(Outer_join)



    #   #implement ag grid in django
    # context = {
    #     # 'futures_position_data':futures_position_data.to_html(),
    #     # 'swaps_position_data':swaps_position_data.to_html(),
    #     'Outerjoin':Outer_join
    # }
    # return render(request,"customer/fbsb_tot_position.html")




def total_fbsb_trade_position_lots_companyname(company_name):

    print("1")


    futures_position_data = futures_lot_position_companyname(company_name)
    print("2")
    swaps_position_data = swap_lot_position_companyname(company_name)
    print("3")

    print("swaps error:",swaps_position_data)
    # futures_position_data.reset_index(inplace=True)
    # swaps_position_data.reset_index(inplace=True)

    if len(futures_position_data) > 0 or len(swaps_position_data) > 0:

        if len(futures_position_data) > 0:

            futures_col_len = futures_position_data.copy()
            Futures_column_name_list = len(futures_col_len.columns) * ['Futures'] if len(
                futures_position_data) > 0 else []
            Futures_column_name_list[0] = 'Contract Month' if len(futures_col_len.columns) > 1 else []

            swaps_col_len = swaps_position_data.copy()
            swaps_col_len = swaps_col_len.set_index('Contract') if len(swaps_position_data) > 0 else swaps_col_len
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []

        elif len(swaps_position_data) > 0 and len(futures_position_data) == 0:
            swaps_col_len = swaps_position_data.copy()
            swaps_column_name_list = len(swaps_col_len.columns) * ['Swaps'] if len(swaps_position_data) > 0 else []
            swaps_column_name_list[0] = 'Contract Month' if len(swaps_col_len.columns) > 1 else []
            Futures_column_name_list = []

        elif len(swaps_position_data) == 0 and len(futures_position_data) == 0:

            Futures_column_name_list = []
            swaps_column_name_list = []

        Column_dist_list = Futures_column_name_list + swaps_column_name_list
    #
    #
        print("Futures_column_name_list :",Futures_column_name_list)
        print("swaps_column_name_list :",swaps_column_name_list)
        Column_dist_list = Futures_column_name_list + swaps_column_name_list
        print("Column_dist_list:",Column_dist_list)
        #
        futures_date = futures_position_data['Contract'][1:].tolist() if len(futures_position_data) > 0 else []
        swaps_date = swaps_position_data['Contract'][1:].tolist() if len(swaps_position_data) > 0 else []
        date_list = futures_date + swaps_date

        print("date list:", date_list)

        if len(date_list) > 0:
            date_list = pd.to_datetime(date_list, format='%d-%b-%y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

        date_generated = pd.date_range(min_date, max_date, freq='MS')
        df = pd.DataFrame(date_generated, columns=['Contract'])

        df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')

        print("date generated:", df)
        #
        Outer_join = pd.merge(df, futures_position_data, on='Contract', how='outer') if len(
            futures_position_data) > 0 else df
        futures_label = len(futures_position_data.columns)
        print(futures_label)

        Outer_join = pd.merge(Outer_join, swaps_position_data, on='Contract', how='outer') if len(
            swaps_position_data) > 0 else Outer_join

        Outer_join.columns = Outer_join.columns.str.rstrip("_x")
        Outer_join.columns = Outer_join.columns.str.rstrip("_y")

        outer_join_columns = Outer_join.columns.tolist()

        Outer_join.columns = Column_dist_list
        Outer_join.loc[-1] = outer_join_columns
        Outer_join.index = Outer_join.index + 1
        Outer_join = Outer_join.sort_index().reset_index(drop=True)  # Reorder DataFrame

        Outer_join.to_csv('Outer_Join.csv')
        copy_whole_data = Outer_join.copy()
        copy_whole_data.replace(['-', 0, 0.0, np.nan], 0.0, inplace=True)

        print(copy_whole_data,'copy_whole_data')

        copy_whole_data.set_index('Contract Month', inplace=True)

        copy_whole_data['Total'] = copy_whole_data[1:].sum(axis=1)
        copy_whole_data['Total'] = round(copy_whole_data['Total'], 2)
        #
        total = copy_whole_data['Total'].tolist()
        # # print('whole_position',whole_position)
        Outer_join['Total(lots)'] = total
        Outer_join.replace([0, 0.0, np.nan], 0.0, inplace=True)


        print("Outer_join:",Outer_join)
        print("outerjoin.colum", Outer_join.columns)

        Outer_join.columns = Outer_join.columns.str.strip()

    else:
        Outer_join=pd.DataFrame()

    # table_columns = Outer_join.columns.to_list()
    # row_data = list(Outer_join._values.tolist())
    # print("row data:",row_data)
    print("outerjoin before send:",Outer_join)
    return(Outer_join)













# ************************************ Ends  Lots company name filtering **********************************

###################### TRADE HISTORY ###############################

# Future Trade History

def Future_tradehistory(request):
    future = FutureBlotterModel.objects.all()
    print("Future_tradehistory:",future)
    future_df = pd.DataFrame(future)
    print("future_df",future_df)
    print("#########################")
    swap_date_list = []
    swap_tradetype_list = []
    swap_Clearer_list = []
    swap_Trader_list = []
    swap_Book_list = []
    swap_Customer_Company_list = []
    swap_Account_list = []
    swap_Strategy_list = []
    swap_Buy_Sell_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_Contract_Month_list = []
    swap_Price_list = []
    swap_Approximate_EP_list = []
    swap_Type_list = []
    swap_EFS_Code_list = []
    swap_Broker_list = []
    for obj in FutureBlotterModel.objects.all():
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Clearer_list.append(obj.clearer)
        swap_Trader_list.append(obj.trader)
        swap_Book_list.append(obj.book)
        swap_Customer_Company_list.append(obj.customer_company)
        swap_Account_list.append(obj.customer_account)
        swap_Strategy_list.append(obj.strategy)
        # swap_Buy_Sell_list.append(obj.Buy_Sell)
        swap_Volume_list.append(obj.volume)
        swap_Contract_Name_list.append(obj.contract)
        swap_Contract_Month_list.append(obj.Contract_Month)
        swap_Price_list.append(obj.price)
        swap_Approximate_EP_list.append(obj.approx_ep)
        swap_Type_list.append(obj.type)
        swap_EFS_Code_list.append(obj.efs_code)
        swap_Broker_list.append(obj.broker)
    fb_history_df = pd.DataFrame(
        {"Date": swap_date_list, "Trade Type": swap_tradetype_list, "Clearer": swap_Clearer_list,
         "Trader": swap_Trader_list, "Book": swap_Book_list, "Customer Company": swap_Customer_Company_list,
         "Account": swap_Account_list, "Strategy": swap_Strategy_list,
         "Volume": swap_Volume_list, "Contract Name": swap_Contract_Name_list,"Price": swap_Price_list,
         "Approximate EP": swap_Approximate_EP_list,"Type": swap_Type_list,   "EFS Code": swap_EFS_Code_list,
         "Broker": swap_Broker_list,

         })

    print("new sb history df :", fb_history_df)
    print("end of future ")
    return (fb_history_df)
    # context = {
    #     'fb_history_df': fb_history_df,
    #
    # }
    # return render(request,"customer/fb-trade-hist.html",context)


######    classs swaps trade history
class SwapsTradeHistory(View):

    def get(self, request, *args, **kwargs):
        sb_history_df = Swap_tradehistory(request)
        print("sb_history_df2:", sb_history_df)

        uniq_cleaer = []
        uniq_book = []
        uniq_contract = []

        sb = SwapBlotterModel.objects.all()
        for i in sb:
            print("iii", i.clearer)
            if i.clearer not in uniq_cleaer:
                uniq_cleaer.append(i.clearer)
            if i.book not in uniq_book:
                uniq_book.append(i.book)
            if i.contract not in uniq_contract:
                uniq_contract.append(i.contract)

        print("unioq2", uniq_cleaer)

        print("uniq_contract", uniq_contract)


        # sb_history_df2 = sb_history_df[(sb_history_df['Clearer'] == 'RJO')]
        # print("fb_history_df2",sb_history_df2)


        context ={

            "sb_history_df":sb_history_df,
            'uniq_cleaer':uniq_cleaer,
            'uniq_book':uniq_book,
            'sb':sb,
            'uniq_contract':uniq_contract,


        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        # return render(request, "customer/Trade-history3.html", context)

        return render(request,"customer/sb-trade-hist.html",context)

    def post(self, request, *args, **kwargs):
        fb_history_df = Future_tradehistory(request)
        sb_history_df = Swap_tradehistory(request)
        # fb_history_df2 = fb_history_df[(fb_history_df['Clearer'] == clearer)]
        # print("fb_history_df2", fb_history_df2)

        date = request.POST.get('date', '')
        clearer = request.POST.get('clearer', '')
        book = request.POST.get('book', '')
        contract = request.POST.get('contract', '')
        print("date:", date)
        print("clearer:", clearer)
        print("book:", book)
        print("contract:", contract)
        # fb_history_df2 = fb_history_df[(fb_history_df['Clearer'] == clearer)]

        # filter_fb =  FutureBlotterModel.objects.filter(Q(book=book) & Q(contract=contract) & Q(contract=clearer))

        if date or clearer or book or contract:
            filter_sb =  SwapBlotterModel.objects.filter(Q(book=book) | Q(contract=contract) | Q(clearer=clearer))
            print("filter_sb:",filter_sb)
            # filter_sb = SwapBlotterModel.objects.filter(clearer=clearer)
        else:
            return HttpResponseRedirect("/swap-trade-history")


        context = {

            "sb_history_df": sb_history_df,
            # "pb_history_df":pb_history_df,
            # "myfilter":myfilter,
            # 'fbsb_history':future_swaps_merge,
            # 'fb':fb,
            'sb':filter_sb,

        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        return render(request, "customer/sb-trade-hist.html", context)









######    classs swaps futures trade history
class SwapsFuturesTradeHistory(View):

    def get(self, request, *args, **kwargs):
        future_swaps_merge = Fb_Sb_Tradehistory(request)
        print("future_swaps_merge:", future_swaps_merge.columns)

        trade_id = future_swaps_merge['Trade ID'].unique().tolist()
        contract = future_swaps_merge['Contract Name'].unique().tolist()
        start_date = future_swaps_merge['Start Date'].unique().tolist()
        clearer = future_swaps_merge['Clearer'].unique().tolist()

        uniq_trade_id = []

        print("trade_id:",trade_id)
        print("clearer",clearer)
        print("contract", contract)
        print("start_date", start_date)

        for i in trade_id:
            if i not in uniq_trade_id:
                uniq_trade_id.append(i)

        print("uniqtradeid", uniq_trade_id)

        context ={

            "future_swaps_merge":future_swaps_merge,
            'contract':contract,
            # 'contract_month':contract_month,
            'trade_id':trade_id,
            'clearer':clearer,
            

        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        # return render(request, "customer/Trade-history3.html", context)

        return render(request,"customer/sb-fb-trade-hist.html",context)

    def post(self, request, *args, **kwargs):
        fb_history_df = Future_tradehistory(request)
        sb_history_df = Swap_tradehistory(request)

        future_swaps_merge = Fb_Sb_Tradehistory(request)

        # date = request.POST.get('date', '')
        # date = datetime.strptime(date, '%Y-%m-%d')
        #
        # date  = date.strftime("%d-%b-%y")

        contract = request.POST.get('contract', '')
        trade_id = request.POST.get('trade_id', '')
        clearer = request.POST.get('clearer', '')

        # print("date GET:", date)
        print("clearer:", clearer)
        print("trade_id:", trade_id)
        print("contract:", contract)

        if contract and clearer =='' and trade_id =='':
            fb_sb_history_df2 = future_swaps_merge[(future_swaps_merge['Contract Name'] == contract)]
            print("all contract:", fb_sb_history_df2)

        elif trade_id and contract=='' and clearer =='' :
            fb_sb_history_df2 = future_swaps_merge[(future_swaps_merge['Trade ID'] == trade_id)]
        elif clearer and trade_id =='' and contract =='':
            fb_sb_history_df2 = future_swaps_merge[(future_swaps_merge['Clearer'] == clearer)]
        # else:
        #     return HttpResponseRedirect("/swap-futures-trade-history")
        #
        # if clearer!='' and contract!='':
        #     fb_sb_history_df2 = future_swaps_merge[(future_swaps_merge['Clearer'] == clearer) & (future_swaps_merge['Contract Name'] == contract)  ]
        else:
            return HttpResponseRedirect("/swap-futures-trade-history")

        context = {

            "future_swaps_merge": fb_sb_history_df2,

        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        return render(request, "customer/sb-fb-trade-hist.html", context)






# Class AllTradehist(request):
class AllTradehist(View):

    def get(self, request, *args, **kwargs):
        fb_history_df = Future_tradehistory(request)

        print("fb_history_df1:", fb_history_df)
        # sb_history_df = Swap_tradehistory(request)
        # print("sb_history_df2:", sb_history_df)
        # pb_history_df = Physical_tradehistory(request)
        # print("pb_history_df3:", pb_history_df)
        myfilter = HistoryFilter()

        uniq_cleaer = []
        uniq_book = []
        uniq_contract=[]

        date = request.POST.get('date', '')
        print("date:",date)

        search_query = request.GET.get('search_query')
        print(" new search_query:", search_query)

        if search_query:
            fb = FutureBlotterModel.objects.filter(
                Q(customer_company__istartswith=search_query) | Q(trader__name__istartswith=search_query)
                | Q(customer_account__istartswith=search_query) | Q(broker__istartswith=search_query) | Q(
                    efs_code__istartswith=search_query) | Q(contract__istartswith=search_query)

                | Q(clearer__istartswith=search_query) | Q(strategy__name__istartswith=search_query) | Q(
                    volume__istartswith=search_query) | Q(holiday__istartswith=search_query)

                | Q(type__istartswith=search_query) | Q(notes__istartswith=search_query) |
                Q(Trade_id__istartswith=search_query) | Q(tick__istartswith=search_query) |

                Q(trader_type__istartswith=search_query) | Q(price__istartswith=search_query)|
                Q(date__istartswith=search_query)
            )


        else:
            fb = FutureBlotterModel.objects.all()

        for i in fb:
            print("iii",i.clearer)
            if i.clearer not in uniq_cleaer:
                uniq_cleaer.append(i.clearer)
            if i.book not in uniq_book:
                uniq_book.append(i.book)
            if i.contract not in uniq_contract:
                uniq_contract.append(i.contract)

        print("unioq2",uniq_cleaer)

        sb = SwapBlotterModel.objects.all()


        # future_swaps_merge = Fb_Sb_Tradehistory(request)

        # fb_history_df2 = fb_history_df[(fb_history_df['Clearer'] == 'RJO')]
        # print("fb_history_df2",fb_history_df2)


        context ={
            "fb_history_df":fb_history_df,
            # "sb_history_df":sb_history_df,
            # "pb_history_df":pb_history_df,
            # "myfilter":myfilter,
            # 'fbsb_history':future_swaps_merge,
            'fb':fb,
            # 'sb':sb,
            'uniq_cleaer':uniq_cleaer,
            'uniq_book':uniq_book,
            'uniq_contract':uniq_contract,



        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        # return render(request, "customer/Trade-history3.html", context)

        return render(request, "customer/trade-history5.html", context)

    def post(self, request, *args, **kwargs):
        fb_history_df = Future_tradehistory(request)
        sb_history_df = Swap_tradehistory(request)

        date = request.POST.get('date', '')
        clearer = request.POST.get('clearer', '')
        book = request.POST.get('book', '')
        contract = request.POST.get('contract', '')
        print("date:",date)
        print("clearer:", clearer)
        print("book:", book)
        print("contract:", contract)
        # fb_history_df2 = fb_history_df[(fb_history_df['Clearer'] == clearer)]
        # filter_fb =  FutureBlotterModel.objects.filter(Q(book=book) & Q(contract=contract) & Q(contract=clearer))


        if date or clearer or book or contract:
            # filter_fb =  FutureBlotterModel.objects.filter(Contract_Month=date)
            filter_fb = FutureBlotterModel.objects.filter(Q(Contract_Month=date) | Q(book=book) | Q(contract=contract) | Q(clearer=clearer))

        else:
            return HttpResponseRedirect("/all-trade-history")



        print("filter_fb:",filter_fb)
        context ={

            'fb':filter_fb,
        }
        # return render(request,"customer/trade-history.html",context)
        # return render(request, "customer/trade-history2.html", context)
        return render(request, "customer/Trade-history5.html", context)





class FutureBlotterHistoryDetailsView(View):
    def get(self,request,*args,**kwargs):
        # print(kwargs)
        qs = FutureBlotterModel.objects.get(id=kwargs['id'])
        return render(request,"customer/fb-history-details.html",{"fb":qs})


class SwapsBlotterHistoryDetailsView(View):
    def get(self,request,*args,**kwargs):
        # print(kwargs)
        qs = SwapBlotterModel.objects.get(id=kwargs['id'])
        return render(request,"customer/sb-history-details.html",{"fb":qs})




######### Swap History ###############

def Swap_tradehistory(request):
    swap_date_list = []
    swap_tradetype_list = []
    swap_Clearer_list = []
    swap_Trader_list = []
    swap_Book_list = []
    swap_Customer_Company_list = []
    swap_Account_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Buy_Sell_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Price_list = []
    swap_Approximate_EP_list = []
    swap_Holiday_list = []
    swap_Type_list = []
    swap_EFS_Code_list = []
    swap_Broker_list = []
    swap_Total_no_days_list = []
    swap_price_days_list = []
    swap_unprice_days_list = []
    swap_total_volume_list = []
    swap_price_volume_list = []
    swap_unprice_volume_list = []
    for obj in SwapBlotterModel.objects.all():
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Clearer_list.append(obj.clearer)
        swap_Trader_list.append(obj.trader)
        swap_Book_list.append(obj.book)
        swap_Customer_Company_list.append(obj.customer_company)
        swap_Account_list.append(obj.customer_account)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        # swap_Buy_Sell_list.append(obj.Buy_Sell)
        swap_Volume_list.append(obj.volume)
        swap_Contract_Name_list.append(obj.contract)
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Price_list.append(obj.price)
        swap_Approximate_EP_list.append(obj.approx_ep)
        swap_Holiday_list.append(obj.holiday)
        swap_Type_list.append(obj.type)
        swap_EFS_Code_list.append(obj.efs_code)
        swap_Broker_list.append(obj.broker)
        swap_Total_no_days_list.append(obj.total_days)
        swap_price_days_list.append(obj.priced_days)
        swap_unprice_days_list.append(obj.unpriced_days)
        swap_total_volume_list.append(obj.total_volume)
        swap_price_volume_list.append(obj.priced_volume)
        swap_unprice_volume_list.append(obj.unpriced_volume)

    sb_history_df = pd.DataFrame({"Date": swap_date_list,"Trade Type": swap_tradetype_list,"Clearer": swap_Clearer_list,
                                  "Trader": swap_Trader_list, "Book": swap_Book_list, "Customer Company": swap_Customer_Company_list,
                                  "Account": swap_Account_list,"Strategy": swap_Strategy_list, "Derivative": swap_Derivative_list,
                                  "Volume": swap_Volume_list, "Contract_Name": swap_Contract_Name_list,
                                  "Start Date ": swap_start_date_list, "End Date": swap_end_date_list, "Price": swap_Price_list,
                                  "Approximate_EP": swap_Approximate_EP_list, "Holiday": swap_Holiday_list, "Type": swap_Type_list,

                                  "EFS_Code": swap_EFS_Code_list, "Broker": swap_Broker_list, "Total No Days": swap_Total_no_days_list,
                                  "Price Days": swap_price_days_list, "Unprice Days": swap_unprice_days_list, "Total Volume": swap_total_volume_list,
                                  "Price Volume": swap_price_volume_list, "Unprice volume": swap_unprice_volume_list,

                                  })


    print("new sb history df :",sb_history_df)

    print("end of swap ")

    return (sb_history_df)

    # context = {
    #     'sb_history_df': sb_history_df,
    # }
    # return render(request,"customer/sb-trade-hist.html",context)



def Fb_Sb_Tradehistory(request):

    future = FutureBlotterModel.objects.all()
    print("Future_tradehistory:",future)
    future_df = pd.DataFrame(future)
    print("future_df",future_df)
    print("#########################")
    fb_date_list = []
    fb_tradetype_list = []
    fb_Clearer_list = []
    fb_Trader_list = []
    fb_Book_list = []
    fb_Customer_Company_list = []
    fb_Account_list = []
    fb_Strategy_list = []
    fb_Buy_Sell_list = []
    fb_Volume_list = []
    fb_Contract_Name_list = []
    fb_Contract_Month_list = []
    fb_Price_list = []
    fb_Approximate_EP_list = []
    fb_Type_list = []
    fb_EFS_Code_list = []
    fb_Broker_list = []

    fb_tradeid = []
    fb_tick_list = []
    fb_bbl_mt_conversion_list = []
    fb_kbbl_mt_conversion_list = []
    fb_notes_list = []

    fb_Clearer_rate_list =[]

    fb_unit_list = []

    fb_holiday_list = []

    fb_brockerage_list =[]
    fb_totalfee_list = []
    fb_Exchange_rate_list = []
    fb_tradeid_list = []


    for obj in FutureBlotterModel.objects.all():
        fb_date_list.append(obj.date)
        fb_tradetype_list.append(obj.trader_type)
        fb_Clearer_list.append(obj.clearer)
        fb_Trader_list.append(obj.trader)
        fb_Book_list.append(obj.book)
        fb_Customer_Company_list.append(obj.customer_company)
        fb_Account_list.append(obj.customer_account)
        fb_Strategy_list.append(obj.strategy)
        # fb_Buy_Sell_list.append(obj.Buy_Sell)
        fb_Volume_list.append(obj.volume)
        fb_Contract_Name_list.append(obj.contract)
        fb_Contract_Month_list.append(obj.Contract_Month)
        fb_Price_list.append(obj.price)
        fb_Approximate_EP_list.append(obj.approx_ep)
        fb_Type_list.append(obj.type)
        fb_EFS_Code_list.append(obj.efs_code)
        fb_Broker_list.append(obj.broker)

        fb_tradeid.append(obj.Trade_id)
        fb_tick_list.append(obj.tick)
        fb_bbl_mt_conversion_list.append(obj.bbl_mt_conversion)

        fb_kbbl_mt_conversion_list.append(obj.kbbl_mt_conversion)
        fb_unit_list.append(obj.unit)

        fb_Clearer_rate_list.append(obj.Clearer_rate)

        fb_brockerage_list.append(obj.brockerage)
        fb_totalfee_list.append(obj.total_fee)

        fb_holiday_list.append(obj.holiday)
        fb_Exchange_rate_list.append(obj.Exchange_rate)



        fb_notes_list.append(obj.notes)

        

    fb_history_df = pd.DataFrame(
        {"Date": fb_date_list, "Trade ID":fb_tradeid, "Trade Type": fb_tradetype_list,  "Book": fb_Book_list,
          "Trader": fb_Trader_list, "Clearer": fb_Clearer_list, "Strategy": fb_Strategy_list,
         "Customer Company": fb_Customer_Company_list,"Account": fb_Account_list,"Volume": fb_Volume_list,
         "Contract Name": fb_Contract_Name_list,"Price": fb_Price_list,
         "Approximate EP": fb_Approximate_EP_list, "Holiday": fb_holiday_list,"Tick":fb_tick_list,"Unit":fb_unit_list, "Type":fb_Type_list,"EFS Code": fb_EFS_Code_list,
         "Broker": fb_Broker_list,"Clearer Rate":fb_Clearer_list ,
         "Exchange Rrate":fb_Exchange_rate_list,

         "Brokerage":fb_brockerage_list,"Total Fee":fb_totalfee_list,"bbl MT Conversion":fb_bbl_mt_conversion_list,  "kbbl MT conversion":fb_kbbl_mt_conversion_list,
         "Notes":fb_notes_list,
         })

    print("future :", fb_history_df)
    print("end of future ")
    #
    # fb_history_df = fb_history_df[
    #     ['date', 'Trade_id', 'trader_type', 'book',  'trader', 'clearer', 'strategy', 'customer_company','customer_account',
    #     'volume','contract', 'price', 'approx_ep','holiday','tick',  'unit',   'type', 'efs_code', 'broker',
    #      'Clearer_rate', 'Exchange_rate','brockerage','total_fee','bbl_mt_conversion',
    #      'kbbl_mt_conversion', 'notes']]
    #
    # fb_history_df.columns = ['Date', 'Trade id', 'Trade Type', 'Book','Trader', 'Clearer',
    #                                  'Strategy',"Customer Company", 'Customer Account','Volume', 'Contract','Price',
    #                                  'Approximate EP','Holiday','Tick','Unit','Type', 'EFS Code',  'Broker', 'Clearer Rate', "Exchabge Rate",
    #                                  'Brokerage','Total Fee',  'bbl/MT', 'kbbl/MT','Remarks'
    #                        ]

    fb_history_df['Date'] = pd.to_datetime(fb_history_df['Date'])
    fb_history_df['Date'] = fb_history_df['Date'].dt.strftime('%d-%b-%y')


    print("fb_history_df_new:",fb_history_df)




    swap_date_list = []
    swap_tradetype_list = []
    swap_Clearer_list = []
    swap_Trader_list = []
    swap_Book_list = []
    swap_Customer_Company_list = []
    swap_Account_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Buy_Sell_list = []
    swap_Volume_list = []
    swap_Contract_Name_list = []
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Price_list = []
    swap_Approximate_EP_list = []
    swap_Holiday_list = []
    swap_Type_list = []
    swap_EFS_Code_list = []
    swap_Broker_list = []
    swap_Total_no_days_list = []
    swap_price_days_list = []
    swap_unprice_days_list = []
    swap_total_volume_list = []
    swap_price_volume_list = []
    swap_unprice_volume_list = []
    swap_tradeid_list = []

    for obj in SwapBlotterModel.objects.all():
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.date)
        swap_tradetype_list.append(obj.trader_type)
        swap_Clearer_list.append(obj.clearer)
        swap_Trader_list.append(obj.trader)
        swap_Book_list.append(obj.book)
        swap_Customer_Company_list.append(obj.customer_company)
        swap_Account_list.append(obj.customer_account)
        swap_Strategy_list.append(obj.strategy)
        swap_Derivative_list.append(obj.derivatives)
        # swap_Buy_Sell_list.append(obj.Buy_Sell)
        swap_Volume_list.append(obj.volume)
        swap_Contract_Name_list.append(obj.contract)
        swap_start_date_list.append(obj.start_date)
        swap_end_date_list.append(obj.end_date)
        swap_Price_list.append(obj.price)
        swap_Approximate_EP_list.append(obj.approx_ep)
        swap_Holiday_list.append(obj.holiday)
        swap_Type_list.append(obj.type)
        swap_EFS_Code_list.append(obj.efs_code)
        swap_Broker_list.append(obj.broker)
        swap_Total_no_days_list.append(obj.total_days)
        swap_price_days_list.append(obj.priced_days)
        swap_unprice_days_list.append(obj.unpriced_days)
        swap_total_volume_list.append(obj.total_volume)
        swap_price_volume_list.append(obj.priced_volume)
        swap_unprice_volume_list.append(obj.unpriced_volume)
        swap_tradeid_list.append(obj.Trade_id)

    sb_history_df = pd.DataFrame(
        {"Date": swap_date_list,"Trade ID":swap_tradeid_list, "Trade Type": swap_tradetype_list,"Book": swap_Book_list,
         "Trader": swap_Trader_list,  "Clearer": swap_Clearer_list,  "Strategy": swap_Strategy_list,
         "Customer Company": swap_Customer_Company_list,
         "Account": swap_Account_list, "Derivative": swap_Derivative_list,
         "Volume": swap_Volume_list, "Contract Name": swap_Contract_Name_list,
        "Price": swap_Price_list,
         "Approximate EP": swap_Approximate_EP_list, "Holiday": swap_Holiday_list, "Type": swap_Type_list,

         "EFS_Code": swap_EFS_Code_list, "Broker": swap_Broker_list, "Total No Days": swap_Total_no_days_list,
         "Price Days": swap_price_days_list, "Unprice Days": swap_unprice_days_list,
         "Total Volume": swap_total_volume_list,
         "Price Volume": swap_price_volume_list, "Unprice volume": swap_unprice_volume_list,  "Start Date": swap_start_date_list, "End Date": swap_end_date_list,

         })

    print("swap blotter", sb_history_df)

    print("end of swap ")

    sb_history_df['Date'] = pd.to_datetime(sb_history_df['Date'])
    sb_history_df['Date'] = sb_history_df['Date'].dt.strftime('%d-%b-%y')



    # fb_history_df = pd.DataFrame(
    #     {"Date": fb_date_list, "Trade ID":fb_tradeid, "Trade Type": fb_tradetype_list,  "Book": fb_Book_list,
    #       "Trader": fb_Trader_list, "Clearer": fb_Clearer_list, "Strategy": fb_Strategy_list,
    #      "Customer Company": fb_Customer_Company_list,"Account": fb_Account_list,"Volume": fb_Volume_list,
    #      "Contract Name": fb_Contract_Name_list,"Price": fb_Price_list,
    #      "Approximate EP": fb_Approximate_EP_list, "Holiday": fb_holiday_list,"Tick":fb_tick_list,"Unit":fb_unit_list, "Type":fb_Type_list,"EFS Code": fb_EFS_Code_list,
    #      "Broker": fb_Broker_list,"Clearer Rate":fb_Clearer_list ,
    #      "Exchange Rrate":fb_Exchange_rate_list,
    #
    #      "Brokerage":fb_brockerage_list,"Total Fee":fb_totalfee_list,"bbl MT Conversion":fb_bbl_mt_conversion_list,  "kbbl MT conversion":fb_kbbl_mt_conversion_list,
    #      "Notes":fb_notes_list,
    #      })


    if len(sb_history_df) > 0 and len(fb_history_df) > 0:

        swpas_futured_df = pd.concat([sb_history_df, fb_history_df], join='outer')

    elif len(sb_history_df) > 0:
        swpas_futured_df = sb_history_df
    elif len(fb_history_df) > 0:
        swpas_futured_df = fb_history_df
    else:
        swpas_futured_df = pd.DataFrame(data=['No Trades'], columns=['Data'])

    print("swpas_futured_df::::",swpas_futured_df)

    return(swpas_futured_df)






















class CompanyFilterPosition(CreateView):
    def get(self, request, *args, **kwargs):
        book = Book.objects.all()
        print(book,":All Books")
        context = {
            "book":book,
        }
        # return render(request, "customer/fbsb_tot_position.html",context)
        return render(request, "customer/new-cust.html", context)

    def post(self, request, *args, **kwargs):
        company_name = request.POST.get('company_name')
        print("comapn b4:", company_name)
        # lots_kbbl = request.POST.get('lots_kbbl')
        # print("lots kbbl:", lots_kbbl)

        kbbl_filter = total_kbbl_trade_position_companyName(company_name)
        lots_filter = total_fbsb_trade_position_lots_companyname(company_name)
        lots_statement_filter = fbsb_lots_statemnts_filter(company_name)

        context={

            'filter_kbbl':kbbl_filter,
            'filter_lots':lots_filter,
            'company_name':company_name,
            'lots_statement_filter':lots_statement_filter,


        }


        return render(request, "customer/new-cust.html",context)



        # if lots_kbbl == "Lots":
        #     print("hello lots")
        #     lots_filter = total_fbsb_trade_position_lots_companyname(company_name)
        #     print("final lots df:", lots_filter)
        #     return render(request, "customer/new-cust.html", {"filterdata": lots_filter,"companyname":company_name})
        #
        # elif lots_kbbl == "kbbl":
        #
        #     kbbl_filter = total_kbbl_trade_position_companyName(company_name)
        #     print("final kkbl df:",kbbl_filter)
        #     return render(request, "customer/new-cust.html", {"filterdata": kbbl_filter,"companyname":company_name})






# def physical_position(request):
#
#     product_list=[]
#     priced_volume=[]
#     end_date=[]
#
#     for obj in PhysicalBlotterModel.objects.all():
#
#         product_list.append(obj.Cargo)
#         priced_volume.append(obj.price_volume)
#         end_date.append(obj.end_date)
#
#     data_position= pd.DataFrame({"PRODUCT":product_list,
#                                 "PRICED_VOLUME": priced_volume,
#                                 "END_DATE": end_date,
#                                 })
#     if len(data_position)>0:
#
#         data_position = data_position[['PRODUCT', 'PRICED_VOLUME', 'END_DATE']]
#         data_position['END_DATE'] = pd.to_datetime(data_position['END_DATE'])
#         data_position.set_index('END_DATE', inplace=True)
#         data_position["PRODUCT"] = data_position["PRODUCT"].values.astype('str')
#
#         resampled = (data_position.groupby('PRODUCT')['PRICED_VOLUME'].resample("M").sum()).reset_index().round(3)
#         resampled.reset_index(inplace=True)
#         # resampled.end_date = resampled.contract_month.dt.strftime('01-%b-%y')
#         resampled = resampled.pivot(index='END_DATE', columns='PRODUCT', values='PRICED_VOLUME')
#         resampled = resampled.rename_axis(None, axis=1)
#
#         tot_data = resampled.copy()
#
#         sum_product_position = tot_data.sum(axis=0)
#         name_df = sum_product_position.to_frame(name='Total')
#         name_df.index.name = 'Products'
#         df_total = name_df
#         df_total = name_df.transpose()
#         df_total.reset_index(inplace=True)
#         df_total.rename(columns={'index': 'Products'}, inplace=True)
#
#         list_row = df_total.iloc[0].tolist()
#         data_new = resampled.copy()  # Create copy of DataFrame
#         data_new.reset_index(inplace=True)
#         data_new.loc[-1] = list_row
#         data_new.index = data_new.index + 1  # Append list at the bottom
#         data_new = data_new.sort_index().reset_index(drop=True)
#         data_new.rename(columns={'END_DATE': 'Contract'}, inplace=True)
#         physical_date = data_new['Contract'][1:].tolist() if len(data_new) > 0 else []
#         date_list = physical_date
#
#         if len(date_list) > 0:
#             print("datelist",date_list)
#
#             date_list = pd.to_datetime(date_list, format='%Y-%m-%d')
#             date_list = date_list.to_list()
#
#             min_date = min(date_list)
#             max_date = max(date_list)
#
#             min_date=min_date.date()
#             max_date=max_date.date()
#
#             min_date= min_date.strftime('01-%b-%y')
#             max_date = max_date.strftime('01-%b-%y')
#
#             min_date = datetime.strptime(min_date, '%d-%b-%y').date()
#             print("*********")
#             max_date = datetime.strptime(max_date, '%d-%b-%y').date()
#
#             df = pd.DataFrame(pd.date_range(min_date, max_date, freq='MS'), columns=['Contract'])
#             print("df:",df)
#             df['Contract'] = df['Contract'].dt.strftime('%d-%b-%y')
#
#         phyical_blotter_position = pd.merge(df, data_new, on='Contract', how='outer') if len(
#                 data_new) > 0 else df
#
#         phyical_blotter_position.replace([0, 0.0, np.nan], 0.0, inplace=True)
#         print('phyical_blotter_position',phyical_blotter_position)
#
#
#
#
#     else:
#         phyical_blotter_position = pd.DataFrame()
#         print('phyical_blotter_position',phyical_blotter_position)
#
#     context = {
#         "phyical_blotter_position":phyical_blotter_position
#
#     }
#
#     return render(request,"customer/position-pb.html",context)







def index2(request):
    return render(request,"customer/index-2.html")



class TankSummary(CreateView):

    def get(self, request, *args, **kwargs):
        fb = FutureBlotterModel.objects.all()
        pb = PhysicalBlotterModel.objects.all()
        inv_t = InventoryModel.objects.all()
        sb = SwapBlotterModel.objects.all()
        print("fb",fb)

        for j in pb:
            pb_trade_id = j.Trade_id
            print("pb_trade_id",pb_trade_id)
        lis = []
        for obj in PhysicalBlotterModel.objects.all():
            if obj.Trade_id not in lis:
                lis.append(obj.Trade_id)
        print(lis,"LIS")

        if len(lis)>0:
            pb_trade_id=pb_trade_id
        else:
            pb_trade_id=''

        context = {

            "pb_trade_id":pb_trade_id,
            "lis":lis
        }
        # return render(request, "customer/fbsb_tot_position.html",context)
        return render(request, "customer/get-tank-summary.html", context)




    def post(self, request, *args, **kwargs):
        tank_summ_trade_id = request.POST.get('tank_summ_trade_id')
        # tank_summ_trade_id = "Rawa-5437-Rawat-10182"
        print("tank_summ_trade_id b4:", tank_summ_trade_id)

        sb_tradeid_filter = SwapBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)
        fb_tradeid_filter = FutureBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)
        inv_tradeid_filter = InventoryModel.objects.filter(Trade_id=tank_summ_trade_id)
        pb_tradeid_filter = PhysicalBlotterModel.objects.filter(Trade_id=tank_summ_trade_id)

        paper_tank_summary = Fb_Sb_Tradehistory(request)
        paper_tank_summary2 = paper_tank_summary[(paper_tank_summary['Trade ID'] == tank_summ_trade_id)]


        admin_trades=GenerateTradeModel.objects.filter(Trade_id=tank_summ_trade_id)
        admin_trade_purchased_volume=[]
        for admin_data in admin_trades:
            admin_trade_purchased_volume.append(admin_data.Quantity)
            admin_Unit=str(admin_data.Unit)
            admin_cargo=admin_Unit=str(admin_data.Cargo)

        total_purchased_qty=sum(admin_trade_purchased_volume)


        physical_trade_id_list=[]
        physical_shore_received_list=[]
        physical_difference_list=[]
        physica_total_volume_list=[]
        physical_cargo_list=[]
        physical_unit_list=[]
        m3_list=[]

        for physical_data in pb_tradeid_filter:
            physical_trade_id_list.append(physical_data.Trade_id)
            physical_shore_received_list.append(physical_data.Shore_recieved)
            physical_difference_list.append(physical_data.Difference)
            physica_total_volume_list.append(physical_data.Quantity)
            # physica_total_volume_list
            physical_cargo_list.append(physical_data.Cargo)
            physical_unit_list.append(physical_data.Unit)
            m3_list.append(physical_data.m3)

        physical_data=dict({'Trade_id':physical_trade_id_list,'Physical_Blotter_qty':physica_total_volume_list,'Shore_Received':physical_shore_received_list,'Difference':physical_difference_list,'m3':m3_list,'Unit':physical_unit_list})

        physical_data=pd.DataFrame(physical_data)



        if len(physical_data)>0:
            physical_data['current_qty_MT'] = np.where(physical_data['Unit'] == 'MT', physical_data['Shore_Received'],
                                                       physical_data['m3'])
            physical_data['Shore_Received'] = physical_data['Shore_Received'].astype(float)

            physical_data['Difference'] = physical_data['Difference'].astype(float)
            physical_data = physical_data[physical_data['Shore_Received'] > 0]

            if len(physical_data) > 0:
                physical_blotter_qty=physical_data['Physical_Blotter_qty'].sum()

                shore_received_qty = physical_data['Shore_Received'].sum()
                bill_shore_difference = physical_data['Difference'].sum()

                current_qty_MT=physical_data['current_qty_MT'].sum()

                Total_Volume=float(total_purchased_qty)
                print(Total_Volume,'Total_Volume')
                print('shore_received',shore_received_qty)
                print(bill_shore_difference,'bill_shore_difference')

                physical_data_sale = dict(
                    {'Trade_id': physical_trade_id_list, 'Physical_Blotter_qty': physica_total_volume_list,
                     'Shore_Received': physical_shore_received_list, 'Difference': physical_difference_list,
                     'm3': m3_list, 'Unit': physical_unit_list})

                physical_data_sale = pd.DataFrame(physical_data_sale)

                sales_value = physical_data_sale[physical_data_sale['Shore_Received'] < 0]
                print('+++++++++++++++++++', sales_value)
                if len(sales_value) > 0:
                    sales_value_qty = sales_value['Shore_Received'].sum()
                    print('sales_value_qty', sales_value_qty)
                else:
                    sales_value_qty = 0.0


                inv_diff_list=[]
                for inventory_data in  inv_tradeid_filter:
                    inv_diff_list.append(inventory_data.dest_difference)
                inv_difference=sum(inv_diff_list)

            total_purchased_qty = float(Total_Volume) + float(sales_value_qty) + float(bill_shore_difference)+float(inv_difference)


            summary_dict = {'Cargo':admin_cargo,'Trade Quantity':Total_Volume,'Unit':admin_Unit,'Billed Quantity':physical_blotter_qty , 'Shore Received':shore_received_qty,
                            'Bill-Shore Difference': bill_shore_difference, 'Sold Quantity': sales_value_qty,
                            'Inventory Transfer Difference': inv_difference, 'Inventory Remaining Quantity': total_purchased_qty}

            print(summary_dict,'summary_dict')
            summary_dict=pd.DataFrame(summary_dict,index=[0])




        sb_tradeid_filterdf = pd.DataFrame(sb_tradeid_filter)
        print("sb_tradeid_filterdf", sb_tradeid_filterdf)

        # swapblotter  df

        swap_date_list = []
        swap_tradetype_list = []
        swap_Clearer_list = []
        swap_Trader_list = []
        swap_Book_list = []
        swap_Customer_Company_list = []
        swap_Account_list = []
        swap_Strategy_list = []
        swap_derivatives_list = []
        swap_Buy_Sell_list = []
        swap_Volume_list = []
        swap_start_date_list = []
        swap_end_date_list = []
        swap_holiday_list = []
        swap_Contract_Name_list = []
        swap_Contract_Month_list = []
        swap_Price_list = []
        swap_Approximate_EP_list = []
        swap_Type_list = []
        swap_EFS_Code_list = []
        swap_Broker_list = []
        swap_notes_list = []

        swap_Trade_id_list =[]
        swap_tick_list =[]
        swap_unit_list = []
        swap_singl_dif_list =[]
        swap_mini_major_list = []
        swap_mini_major_connection_list = []
        swap_bbi_mt_conversion_list = []
        swap_kbbl_mt_conversion_list = []
        swap_total_days_list = []
        swap_priced_days_list = []
        swap_unpriced_days_list = []
        swap_total_volume_list =[]
        swap_priced_volume_list =[]
        swap_unpriced_volume_list =[]
        swap_block_fee_list = []
        swap_screen_fee_list = []
        swap_brockerage_list =[]
        swap_total_fee_list =[]
        swap_bbi_mt_list =[]
        swap_kbbi_mt_list =[]
        swap_unpriced_kbbl_mt_list=[]
        swap_fw_months_list=[]
        swap_LTD_list =[]
        swap_First_month_list=[]
        swap_Second_month_list=[]
        swap_MTM_list =[]
        swap_first_month_days_list =[]
        swap_second_month_settle_price_list=[]
        swap_PNL_list=[]
        swap_total_PNL_list=[]
        swap_futures_equiv_first_list=[]
        swap_futures_equiv_second_list=[]
        swap_futures_equiv_first_kbbl_list=[]
        swap_futures_equiv_second_kbbl_list=[]
        swap_bileteral_external_list=[]
        swap_buy_sell_list=[]
        swap_physical_code_list=[]
        swap_physica_blotter_connect_list=[]



        for obj in SwapBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id):
            swap_date_list.append(obj.date)
            swap_tradetype_list.append(obj.trader_type)
            swap_Trader_list.append(obj.trader)
            swap_Book_list.append(obj.book)
            swap_Customer_Company_list.append(obj.customer_company)
            swap_Account_list.append(obj.customer_account)
            swap_Strategy_list.append(obj.strategy)
            swap_derivatives_list.append(obj.derivatives)
            swap_Clearer_list.append(obj.clearer)
            swap_Contract_Name_list.append(obj.contract)
            swap_Volume_list.append(obj.volume)
            swap_start_date_list.append(obj.start_date)
            swap_end_date_list.append(obj.end_date)
            swap_Price_list.append(obj.price)
            swap_Approximate_EP_list.append(obj.approx_ep)
            swap_holiday_list.append(obj.holiday)
            swap_Type_list.append(obj.type)
            swap_Broker_list.append(obj.broker)
            swap_EFS_Code_list.append(obj.efs_code)
            swap_notes_list.append(obj.notes)
            swap_Trade_id_list.append(obj.Trade_id)
            swap_tick_list.append(obj.tick)
            swap_unit_list.append(obj.unit)
            swap_singl_dif_list.append(obj.singl_dif)
            swap_mini_major_list.append(obj.mini_major)
            swap_mini_major_connection_list.append(obj.mini_major_connection)
            swap_bbi_mt_conversion_list.append(obj.bbi_mt_conversion)
            swap_kbbl_mt_conversion_list.append(obj.kbbl_mt_conversion)
            swap_total_days_list.append(obj.total_days)
            swap_priced_days_list.append(obj.priced_days)
            swap_unpriced_days_list.append(obj.unpriced_days)
            swap_total_volume_list.append(obj.total_volume)
            swap_priced_volume_list.append(obj.priced_volume)
            swap_unpriced_volume_list.append(obj.unpriced_volume)
            swap_block_fee_list.append(obj.block_fee)
            swap_screen_fee_list.append(obj.screen_fee)
            swap_brockerage_list.append(obj.brockerage)
            swap_total_fee_list.append(obj.total_fee)
            swap_bbi_mt_list.append(obj.bbi_mt)
            swap_kbbi_mt_list.append(obj.kbbi_mt)
            swap_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
            swap_fw_months_list.append(obj.fw_months)
            swap_LTD_list.append(obj.LTD)
            swap_First_month_list.append(obj.First_month)
            swap_Second_month_list.append(obj.Second_month)
            swap_MTM_list.append(obj.MTM)
            swap_first_month_days_list.append(obj.first_month_days)
            swap_second_month_settle_price_list.append(obj.second_month_days)
            swap_PNL_list.append(obj.PNL)
            swap_total_PNL_list.append(obj.total_PNL)
            swap_futures_equiv_first_list.append(obj.futures_equiv_first)
            swap_futures_equiv_second_list.append(obj.futures_equiv_second)
            swap_futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
            swap_futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
            swap_bileteral_external_list.append(obj.bileteral_external)
            swap_buy_sell_list.append(obj.buy_sell)
            swap_physical_code_list.append(obj.physical_code)
            swap_physica_blotter_connect_list.append(obj.physica_blotter_connect)

        sb_trade_df = pd.DataFrame(
            {"Date": swap_date_list, "Trade Type": swap_tradetype_list, "Clearer": swap_Clearer_list,
             "Trader": swap_Trader_list, "Book": swap_Book_list, "Customer Company": swap_Customer_Company_list,
             "Account": swap_Account_list, "Strategy": swap_Strategy_list, "Derivative":swap_derivatives_list,
             "Contract Name": swap_Contract_Name_list,"Volume": swap_Volume_list, "Start Date":swap_start_date_list,
             "End Date":swap_end_date_list,"Price": swap_Price_list,"Approximate EP": swap_Approximate_EP_list,
             "Holiday":swap_holiday_list,"Type": swap_Type_list,"Broker": swap_Broker_list,"EFS Code": swap_EFS_Code_list,
             "Trade ID":swap_Trade_id_list,"Tick":swap_tick_list, "Unit":swap_unit_list,"Single/Diff":swap_singl_dif_list,
             "Mini/Major":swap_mini_major_list,"Mini/Major Connection":swap_mini_major_connection_list,
             "bbl MT Conversion":swap_bbi_mt_conversion_list,"kbbl MT Conversion":swap_kbbl_mt_conversion_list,"Total Days":swap_total_days_list,
             "Priced Days":swap_priced_days_list,"Unpriced Days":swap_unpriced_days_list,"Total Volume":swap_total_volume_list,
             "Priced Volume":swap_priced_volume_list,"Unpriced Volume":swap_unpriced_volume_list,"Block Fee":swap_block_fee_list,
             "Screen Fee":swap_screen_fee_list,"Brokerage":swap_brockerage_list,"Total Fee":swap_total_fee_list,"bbl MT":swap_bbi_mt_list,
             "kbbl MT":swap_kbbi_mt_list,"Unpriced kbbl MT":swap_unpriced_kbbl_mt_list,"FW Months":swap_fw_months_list,"LTD":swap_LTD_list,
             "First Month":swap_First_month_list,"Second Month":swap_Second_month_list,"PNL":swap_PNL_list,"Total PNL":swap_total_PNL_list,
             "Futures Equiv First":swap_futures_equiv_first_list,"Futures Equiv Second":swap_futures_equiv_second_list,
             "Futures Equiv First kbbl":swap_futures_equiv_first_kbbl_list,"Futures Equiv Second kbbl":swap_futures_equiv_second_kbbl_list,
             "Trade Type":swap_bileteral_external_list,"Buy/Sell": swap_buy_sell_list,"Physical Code":swap_physical_code_list,
             "Physical Blotter Equiv":swap_physica_blotter_connect_list,"Notes":swap_notes_list,

             })

        # fb_tradeid_filter = FutureBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)

        # inv_tradeid_filter = InventoryModel.objects.filter(Trade_id=tank_summ_trade_id)
        # pb_tradeid_filter = PhysicalBlotterModel.objects.filter(Trade_id=tank_summ_trade_id)
        column_names = summary_dict.columns.values,
        row_data = list(summary_dict.values.tolist())

        context ={
            "sb_trade_df":sb_trade_df,
            "fb_tradeid_filter":fb_tradeid_filter,
            "inv_tradeid_filter":inv_tradeid_filter,
            "pb_tradeid_filter":pb_tradeid_filter,
            "tank_summ_trade_id":tank_summ_trade_id,
            'summary_dict':summary_dict,

            'column_names':column_names,
            'row_data':row_data,
            'paper_tank_summary2':paper_tank_summary2,

        }

        print("sb_trade_df:", sb_trade_df)
        print("end of future ")

        return render(request, "customer/tank-summary.html",context)


    # def post(self, request, *args, **kwargs):
    #     tank_summ_trade_id = request.POST.get('tank_summ_trade_id')
    #     # tank_summ_trade_id = "Rawa-5437-Rawat-10182"
    #     print("tank_summ_trade_id b4:", tank_summ_trade_id)
    #
    #
    #
    #     sb_tradeid_filter = SwapBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)
    #     fb_tradeid_filter = FutureBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)
    #     inv_tradeid_filter = InventoryModel.objects.filter(Trade_id=tank_summ_trade_id)
    #     pb_tradeid_filter = PhysicalBlotterModel.objects.filter(Trade_id=tank_summ_trade_id)
    #
    #     print("sb_tradeid_filter",sb_tradeid_filter)
    #     print("fb_tradeid_filter", fb_tradeid_filter)
    #     print("inv_tradeid_filter", inv_tradeid_filter)
    #     print("pb_tradeid_filter", pb_tradeid_filter)
    #
    #
    #     sb_tradeid_filterdf = pd.DataFrame(sb_tradeid_filter)
    #     print("sb_tradeid_filterdf", sb_tradeid_filterdf)
    #
    #     # swapblotter  df
    #
    #     swap_date_list = []
    #     swap_tradetype_list = []
    #     swap_Clearer_list = []
    #     swap_Trader_list = []
    #     swap_Book_list = []
    #     swap_Customer_Company_list = []
    #     swap_Account_list = []
    #     swap_Strategy_list = []
    #     swap_derivatives_list = []
    #     swap_Buy_Sell_list = []
    #     swap_Volume_list = []
    #     swap_start_date_list = []
    #     swap_end_date_list = []
    #     swap_holiday_list = []
    #     swap_Contract_Name_list = []
    #     swap_Contract_Month_list = []
    #     swap_Price_list = []
    #     swap_Approximate_EP_list = []
    #     swap_Type_list = []
    #     swap_EFS_Code_list = []
    #     swap_Broker_list = []
    #     swap_notes_list = []
    #
    #     swap_Trade_id_list =[]
    #     swap_tick_list =[]
    #     swap_unit_list = []
    #     swap_singl_dif_list =[]
    #     swap_mini_major_list = []
    #     swap_mini_major_connection_list = []
    #     swap_bbi_mt_conversion_list = []
    #     swap_kbbl_mt_conversion_list = []
    #     swap_total_days_list = []
    #     swap_priced_days_list = []
    #     swap_unpriced_days_list = []
    #     swap_total_volume_list =[]
    #     swap_priced_volume_list =[]
    #     swap_unpriced_volume_list =[]
    #     swap_block_fee_list = []
    #     swap_screen_fee_list = []
    #     swap_brockerage_list =[]
    #     swap_total_fee_list =[]
    #     swap_bbi_mt_list =[]
    #     swap_kbbi_mt_list =[]
    #     swap_unpriced_kbbl_mt_list=[]
    #     swap_fw_months_list=[]
    #     swap_LTD_list =[]
    #     swap_First_month_list=[]
    #     swap_Second_month_list=[]
    #     swap_MTM_list =[]
    #     swap_first_month_days_list =[]
    #     swap_second_month_settle_price_list=[]
    #     swap_PNL_list=[]
    #     swap_total_PNL_list=[]
    #     swap_futures_equiv_first_list=[]
    #     swap_futures_equiv_second_list=[]
    #     swap_futures_equiv_first_kbbl_list=[]
    #     swap_futures_equiv_second_kbbl_list=[]
    #     swap_bileteral_external_list=[]
    #     swap_buy_sell_list=[]
    #     swap_physical_code_list=[]
    #     swap_physica_blotter_connect_list=[]
    #
    #
    #
    #     for obj in SwapBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id):
    #         swap_date_list.append(obj.date)
    #         swap_tradetype_list.append(obj.trader_type)
    #         swap_Trader_list.append(obj.trader)
    #         swap_Book_list.append(obj.book)
    #         swap_Customer_Company_list.append(obj.customer_company)
    #         swap_Account_list.append(obj.customer_account)
    #         swap_Strategy_list.append(obj.strategy)
    #         swap_derivatives_list.append(obj.derivatives)
    #         swap_Clearer_list.append(obj.clearer)
    #         swap_Contract_Name_list.append(obj.contract)
    #         swap_Volume_list.append(obj.volume)
    #         swap_start_date_list.append(obj.start_date)
    #         swap_end_date_list.append(obj.end_date)
    #         swap_Price_list.append(obj.price)
    #         swap_Approximate_EP_list.append(obj.approx_ep)
    #         swap_holiday_list.append(obj.holiday)
    #         swap_Type_list.append(obj.type)
    #         swap_Broker_list.append(obj.broker)
    #         swap_EFS_Code_list.append(obj.efs_code)
    #         swap_notes_list.append(obj.notes)
    #         swap_Trade_id_list.append(obj.Trade_id)
    #         swap_tick_list.append(obj.tick)
    #         swap_unit_list.append(obj.unit)
    #         swap_singl_dif_list.append(obj.singl_dif)
    #         swap_mini_major_list.append(obj.mini_major)
    #         swap_mini_major_connection_list.append(obj.mini_major_connection)
    #         swap_bbi_mt_conversion_list.append(obj.bbi_mt_conversion)
    #         swap_kbbl_mt_conversion_list.append(obj.kbbl_mt_conversion)
    #         swap_total_days_list.append(obj.total_days)
    #         swap_priced_days_list.append(obj.priced_days)
    #         swap_unpriced_days_list.append(obj.unpriced_days)
    #         swap_total_volume_list.append(obj.total_volume)
    #         swap_priced_volume_list.append(obj.priced_volume)
    #         swap_unpriced_volume_list.append(obj.unpriced_volume)
    #         swap_block_fee_list.append(obj.block_fee)
    #         swap_screen_fee_list.append(obj.screen_fee)
    #         swap_brockerage_list.append(obj.brockerage)
    #         swap_total_fee_list.append(obj.total_fee)
    #         swap_bbi_mt_list.append(obj.bbi_mt)
    #         swap_kbbi_mt_list.append(obj.kbbi_mt)
    #         swap_unpriced_kbbl_mt_list.append(obj.unpriced_kbbl_mt)
    #         swap_fw_months_list.append(obj.fw_months)
    #         swap_LTD_list.append(obj.LTD)
    #         swap_First_month_list.append(obj.First_month)
    #         swap_Second_month_list.append(obj.Second_month)
    #         swap_MTM_list.append(obj.MTM)
    #         swap_first_month_days_list.append(obj.first_month_days)
    #         swap_second_month_settle_price_list.append(obj.second_month_days)
    #         swap_PNL_list.append(obj.PNL)
    #         swap_total_PNL_list.append(obj.total_PNL)
    #         swap_futures_equiv_first_list.append(obj.futures_equiv_first)
    #         swap_futures_equiv_second_list.append(obj.futures_equiv_second)
    #         swap_futures_equiv_first_kbbl_list.append(obj.futures_equiv_first_kbbl)
    #         swap_futures_equiv_second_kbbl_list.append(obj.futures_equiv_second_kbbl)
    #         swap_bileteral_external_list.append(obj.bileteral_external)
    #         swap_buy_sell_list.append(obj.buy_sell)
    #         swap_physical_code_list.append(obj.physical_code)
    #         swap_physica_blotter_connect_list.append(obj.physica_blotter_connect)
    #
    #     sb_trade_df = pd.DataFrame(
    #         {"Date": swap_date_list, "Trade Type": swap_tradetype_list, "Clearer": swap_Clearer_list,
    #          "Trader": swap_Trader_list, "Book": swap_Book_list, "Customer Company": swap_Customer_Company_list,
    #          "Account": swap_Account_list, "Strategy": swap_Strategy_list, "Derivative":swap_derivatives_list,
    #          "Contract Name": swap_Contract_Name_list,"Volume": swap_Volume_list, "Start Date":swap_start_date_list,
    #          "End Date":swap_end_date_list,"Price": swap_Price_list,"Approximate EP": swap_Approximate_EP_list,
    #          "Holiday":swap_holiday_list,"Type": swap_Type_list,"Broker": swap_Broker_list,"EFS Code": swap_EFS_Code_list,
    #          "Trade ID":swap_Trade_id_list,"Tick":swap_tick_list, "Unit":swap_unit_list,"Single/Diff":swap_singl_dif_list,
    #          "Mini/Major":swap_mini_major_list,"Mini/Major Connection":swap_mini_major_connection_list,
    #          "bbl MT Conversion":swap_bbi_mt_conversion_list,"kbbl MT Conversion":swap_kbbl_mt_conversion_list,"Total Days":swap_total_days_list,
    #          "Priced Days":swap_priced_days_list,"Unpriced Days":swap_unpriced_days_list,"Total Volume":swap_total_volume_list,
    #          "Priced Volume":swap_priced_volume_list,"Unpriced Volume":swap_unpriced_volume_list,"Block Fee":swap_block_fee_list,
    #          "Screen Fee":swap_screen_fee_list,"Brokerage":swap_brockerage_list,"Total Fee":swap_total_fee_list,"bbl MT":swap_bbi_mt_list,
    #          "kbbl MT":swap_kbbi_mt_list,"Unpriced kbbl MT":swap_unpriced_kbbl_mt_list,"FW Months":swap_fw_months_list,"LTD":swap_LTD_list,
    #          "First Month":swap_First_month_list,"Second Month":swap_Second_month_list,"PNL":swap_PNL_list,"Total PNL":swap_total_PNL_list,
    #          "Futures Equiv First":swap_futures_equiv_first_list,"Futures Equiv Second":swap_futures_equiv_second_list,
    #          "Futures Equiv First kbbl":swap_futures_equiv_first_kbbl_list,"Futures Equiv Second kbbl":swap_futures_equiv_second_kbbl_list,
    #          "Trade Type":swap_bileteral_external_list,"Buy/Sell": swap_buy_sell_list,"Physical Code":swap_physical_code_list,
    #          "Physical Blotter Equiv":swap_physica_blotter_connect_list,"Notes":swap_notes_list,
    #
    #          })
    #
    #     # fb_tradeid_filter = FutureBlotterModel.objects.filter(physica_blotter_connect=tank_summ_trade_id)
    #
    #     # inv_tradeid_filter = InventoryModel.objects.filter(Trade_id=tank_summ_trade_id)
    #     # pb_tradeid_filter = PhysicalBlotterModel.objects.filter(Trade_id=tank_summ_trade_id)
    #
    #     context ={
    #         "sb_trade_df":sb_trade_df,
    #         "fb_tradeid_filter":fb_tradeid_filter,
    #         "inv_tradeid_filter":inv_tradeid_filter,
    #         "pb_tradeid_filter":pb_tradeid_filter,
    #         "tank_summ_trade_id":tank_summ_trade_id,
    #     }
    #
    #     print("sb_trade_df:", sb_trade_df)
    #     print("end of future ")
    #
    #     return render(request, "customer/tank-summary.html",context)




## PHYSICAL POSITION

def physical_position(request):

    product_list=[]
    priced_volume=[]
    end_date=[]

    for obj in PhysicalBlotterModel.objects.all():

        product_list.append(obj.Cargo)
        priced_volume.append(obj.price_volume)
        end_date.append(obj.end_date)

    data_position= pd.DataFrame({"PRODUCT":product_list,
                                "PRICED_VOLUME": priced_volume,
                                "END_DATE": end_date,
                                })
    if len(data_position)>0:

        data_position = data_position[['PRODUCT', 'PRICED_VOLUME', 'END_DATE']]
        data_position['END_DATE'] = pd.to_datetime(data_position['END_DATE'])
        data_position.set_index('END_DATE', inplace=True)
        data_position["PRODUCT"] = data_position["PRODUCT"].values.astype('str')

        resampled = (data_position.groupby('PRODUCT')['PRICED_VOLUME'].resample("M").sum()).reset_index().round(3)
        resampled.reset_index(inplace=True)
        resampled.END_DATE = resampled.END_DATE.dt.strftime('01-%m-%Y')
        resampled = resampled.pivot(index='END_DATE', columns='PRODUCT', values='PRICED_VOLUME')
        resampled = resampled.rename_axis(None, axis=1)

        tot_data = resampled.copy()

        sum_product_position = tot_data.sum(axis=0)
        name_df = sum_product_position.to_frame(name='Total')
        name_df.index.name = 'Products'
        df_total = name_df
        df_total = name_df.transpose()
        df_total.reset_index(inplace=True)
        df_total.rename(columns={'index': 'Products'}, inplace=True)

        list_row = df_total.iloc[0].tolist()
        data_new = resampled.copy()  # Create copy of DataFrame
        data_new.reset_index(inplace=True)
        data_new.loc[-1] = list_row
        data_new.index = data_new.index + 1  # Append list at the bottom
        data_new = data_new.sort_index().reset_index(drop=True)
        data_new.rename(columns={'END_DATE': 'Contract'}, inplace=True)
        physical_date = data_new['Contract'][1:].tolist() if len(data_new) > 0 else []
        date_list = physical_date

        if len(date_list) > 0:

            date_list = pd.to_datetime(date_list, format='%d-%m-%Y')
            date_list = date_list.to_list()

            min_date = min(date_list)
            max_date = max(date_list)

            min_date=min_date.date()
            max_date=max_date.date()

            min_date= min_date.strftime('01-%m-%Y')
            max_date = max_date.strftime('01-%m-%Y')

            min_date = datetime.strptime(min_date, '%d-%m-%Y')
            max_date = datetime.strptime(max_date, '%d-%m-%Y')

            df = pd.DataFrame(pd.date_range(min_date, max_date, freq='MS'), columns=['Contract'])
            df['Contract'] = df['Contract'].dt.strftime('%d-%m-%Y')

            print(df,data_new,'','data_new')

        phyical_blotter_position = pd.merge(df, data_new, on='Contract', how='outer') if len(
                data_new) > 0 else df
        phyical_blotter_position.replace([0, 0.0, np.nan], 0.0, inplace=True)

        # list_row = df_total.iloc[0].tolist()
        # data_new = data.copy()  # Create copy of DataFrame
        # data_new.loc[-1] = list_row
        # data_new.index = data_new.index + 1  # Append list at the bottom
        # data_new = data_new.sort_index().reset_index(drop=True)  # Reorder DataFrame
        # cols_new = list(data_new.columns)
        # print(data_new)



    else:
        phyical_blotter_position = pd.DataFrame()
        print('phyical_blotter_position',phyical_blotter_position)

    # return (phyical_blotter_position)

    context = {
        "phyical_blotter_position": phyical_blotter_position

    }

    return render(request, "customer/position-pb.html", context)


#### PHYSICAL HEDGING
# def physical_hedging(request):
#
#     # # sb_headging_df = Headging(request)
#     # print("sb_headging_df", sb_headging_df)
#
#
#     full_df=[]
#     start_date_list = []
#     end_date_list = []
#     volume_list = []
#     pricing_method_list = []
#     total_days_list = []
#     pricing_contract_list = []
#     holiday_list = []
#     hdval_physical_dict = {}
#     physical_full_df = []
#
#     today = date.today()
#     month = today.month
#     year = today.year
#     first_date = (datetime.today().replace(day=1)).day
#     first_datecheck, num_days = calendar.monthrange(year, month)
#     for obj in PhysicalBlotterModel.objects.all():
#
#         start_date_list.append(obj.start_date)
#         end_date_list.append(obj.end_date)
#         volume_list.append(obj.Quantity)
#         volume_list = [float(x) for x in volume_list]
#         total_days_list.append(obj.Total_no_days)
#         total_days_list = [int(x) for x in total_days_list]
#         pricing_method_list.append(obj.Pricing_method)
#         pricing_contract_list.append(obj.Pricing_contract)  # convert list values from model to Float
#         holiday_list.append(obj.Holiday)
#
#     load_physical_data = pd.DataFrame(
#         {"START_DATE": start_date_list, "END_DATE": end_date_list,
#           "PRICING_METHOD": pricing_method_list,"PRICING_CONTRACT": pricing_contract_list,
#             "TOTAL_VOLUME": volume_list,"TOTAL_DAYS": total_days_list, "HOLIDAY": holiday_list
#          })
#
#     load_physical_data.START_DATE = pd.to_datetime(load_physical_data.START_DATE)
#     load_physical_data.END_DATE = pd.to_datetime(load_physical_data.END_DATE)
#     load_physical_data['vol/day'] = np.where(load_physical_data['PRICING_METHOD'] == 'Float',
#                                              np.round(
#                                                  load_physical_data['TOTAL_VOLUME'] / load_physical_data['TOTAL_DAYS'],
#                                                  2), load_physical_data['TOTAL_VOLUME'])
#
#     print(load_physical_data,'load_physical_data')
#
#     df_filtered = load_physical_data[
#         (load_physical_data['START_DATE'].dt.month == month) | (load_physical_data['END_DATE'].dt.month == month)]
#     physical_contract_list = df_filtered['PRICING_CONTRACT'].unique().tolist()
#
#     print("df_filtered",df_filtered)
#
#     start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
#     end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#     end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#
#     dates = pd.date_range(start_date, end_date, freq='D')
#     dict = {'DATES': dates}
#     df_date = pd.DataFrame(dict)
#     # print(df_date,'df_date')
#
#     Holiday_date_list = []
#     Holiday_type_list = []
#
#     for obj in HolidayM.objects.all():
#         Holiday_date_list.append(str(obj.date))
#         Holiday_type_list.append(str(obj.name))
#
#     holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
#     holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])
#     # print('Holidays_data',holiday_data_df)
#
#     physical_dates = pd.date_range(start_date, end_date, freq='D')
#     dict = {'DATES': physical_dates}
#
#     physical_df = pd.DataFrame(dict)
#     # print(physical_df,'physical_df')
#
#     physical_list_dict = {}
#     holiday_list_dict = {}
#
#     for i in physical_contract_list:
#         physical_list_dictionary = []
#         holiday_list_dictionary = []
#         print(i)
#         contract_physical_data = df_filtered[(df_filtered["PRICING_CONTRACT"] == i)]
#         contract_physical_data = pd.DataFrame(contract_physical_data)
#         print(contract_physical_data,'contract_physical_data')
#
#         for index, row in contract_physical_data.iterrows():
#             holiday_name = row["HOLIDAY"]
#
#             hld_df_physical = holiday_data_df.loc[holiday_data_df['Holiday'] == row['HOLIDAY']]
#             hld_date_physical = hld_df_physical['Date'].to_list()
#             print(hld_date_physical,'hld_date_physical')
#
#             for hd in hld_date_physical:
#                 hd_month = hd.month
#                 current_month = datetime.now().month
#                 # if hd_month==current_month:
#                 for dts in df_date['DATES']:
#                     phys_curr_date = str(dts.date())
#
#                     if dts.date() >= row['START_DATE'].date() and dts.date() <= row['END_DATE'].date():
#                         print("month_date", dts)
#                         print(hd.date(), 'check hd_date', dts.date(), 'dts_date')
#
#                         if dts.date() != (hd.date()):
#                             physical_list_dict.update({phys_curr_date: row['vol/day']})
#                             holiday_list_dict.update({phys_curr_date: 1})
#                             # print(holiday_list_dict,'holiday_list_dict')
#                         elif dts.date() in ([hd.date()]):
#                             physical_list_dict.update({phys_curr_date: 0})
#                             holiday_list_dict.update({phys_curr_date: 0})
#                     else:
#                         physical_list_dict.update({phys_curr_date: 0})
#                         holiday_list_dict.update({phys_curr_date: 0})
#                     #         print(physical_list_dict)
#
#                 df_dict_phys = pd.DataFrame(physical_list_dict.items(), columns=['Date', 'DateValue'])
#                 df_holiday_phys = pd.DataFrame(holiday_list_dict.items(), columns=['Date', 'hd_bool'])
#
#                 df_dict_phys.set_index(['Date'], inplace=True)
#                 df_holiday_phys.set_index(['Date'], inplace=True)
#
#                 physical_list_dictionary.append(df_dict_phys)
#                 print(physical_list_dictionary)
#                 holiday_list_dictionary.append(df_holiday_phys)
#                 # print('holiday_list_dictionary',holiday_list_dictionary)
#
#         df_physical_final = reduce(lambda a, b: a.add(b, fill_value=0), physical_list_dictionary)
#         hd_physical_final = reduce(lambda a, b: a.add(b, fill_value=0), holiday_list_dictionary)
#
#         df_physical_final = df_physical_final.rename(columns={'DateValue': i})
#         hd_physical_final = hd_physical_final.rename(columns={'hd_bool': i})
#
#         df_physical_final.index = pd.to_datetime(df_physical_final.index)
#         df_physical_final.reset_index(inplace=True)
#
#         hd_physical_final.index = pd.to_datetime(hd_physical_final.index)
#         hd_physical_final.reset_index(inplace=True)
#
#         for index, rows in contract_physical_data.iterrows():
#             hld_df_physical = holiday_data_df.loc[holiday_data_df['Holiday'] == rows['HOLIDAY']]
#             if i == rows['PRICING_CONTRACT']:
#                 if i in hdval_physical_dict:
#                     if rows['HOLIDAY'] not in hdval_physical_dict[i]:
#                         hdval_physical_dict[i].append(rows['HOLIDAY'])
#                         hdval_physical_dict[i].append(",")
#                 else:
#                     hdval_physical_dict[i] = [rows['HOLIDAY']]
#                     hdval_physical_dict[i].append(",")
#
#             hld_date_physical = hld_df_physical['Date'].to_list()
#             for hd in hld_date_physical:
#                 df_physical_final.loc[
#                     (hd_physical_final[i] == 0) & (df_physical_final['Date'].isin([hd.date()])), i] = 'Holiday'
#             df_physical_final.loc[(df_physical_final['Date'].dt.dayofweek > 4), i] = 'Weekend'
#
#         df_physical_final.set_index(['Date'], inplace=True)
#         physical_full_df.append(df_physical_final)
#
#     if len(physical_full_df) > 0:
#         physical_hedging = pd.concat(physical_full_df, axis=1, ignore_index=False)
#         physical_hedging.reset_index(inplace=True)
#
#         physical_hedging['Date'] = physical_hedging["Date"].dt.strftime("%d-%b-%y")
#         physical_hedging.set_index(['Date'], inplace=True)
#         physical_hedging_t = physical_hedging.T
#         physical_hedging_t.index.rename('Contracts', inplace=True)
#         physical_hedging_t.reset_index(inplace=True)
#         for i in physical_contract_list:
#             hdToStr = ' '.join(map(str, hdval_physical_dict[i]))
#             hdToStr = hdToStr[:-1]
#             physical_hedging_t.loc[(physical_hedging_t['Contracts'] == i), 'Holiday'] = hdToStr
#             mid_phy = physical_hedging_t['Holiday']
#             physical_hedging_t.drop(labels=['Holiday'], axis=1, inplace=True)
#             physical_hedging_t.insert(1, 'Holiday', mid_phy)
#
#
#
#     else:
#
#         physical_hedging = physical_df
#         physical_hedging['DATES'] = physical_hedging["DATES"].dt.strftime("%d-%b-%y")
#         physical_hedging.set_index(['DATES'], inplace=True)
#         physical_hedging_t = physical_hedging.T
#
#
#     print(physical_hedging_t,'physical_hedging_t')
#
#
#
#     #
#     context = {
#         "physical_hedging_t": physical_hedging_t,
#         # "sb_headging_df":sb_headging_df,
#
#     }
#     # return render(request, "customer/hedge-pb.html", context)
#     return render(request, "customer/physical_hedge.html", context)

#### PHYSICAL HEDGING
def physical_hedging(request):

    # # sb_headging_df = Headging(request)
    # print("sb_headging_df", sb_headging_df)


    full_df=[]
    start_date_list = []
    end_date_list = []
    volume_list = []
    pricing_method_list = []
    total_days_list = []
    pricing_contract_list = []
    holiday_list = []
    hdval_physical_dict = {}
    physical_full_df=[]
    hdval_physical_dict = {}

    today = date.today()
    month = today.month
    year = today.year
    first_date = (datetime.today().replace(day=1)).day
    first_datecheck, num_days = calendar.monthrange(year, month)

    for obj in PhysicalBlotterModel.objects.all():

        start_date_list.append(obj.start_date)
        end_date_list.append(obj.end_date)
        volume_list.append(obj.Quantity)
        volume_list = [float(x) for x in volume_list]
        total_days_list.append(obj.Total_no_days)
        total_days_list = [int(x) for x in total_days_list]
        pricing_method_list.append(obj.Pricing_method)
        pricing_contract_list.append(obj.Pricing_contract)  # convert list values from model to Float
        holiday_list.append(obj.Holiday)

    load_physical_data = pd.DataFrame(
        {"START_DATE": start_date_list, "END_DATE": end_date_list,
          "PRICING_METHOD": pricing_method_list,"PRICING_CONTRACT": pricing_contract_list,
            "TOTAL_VOLUME": volume_list,"TOTAL_DAYS": total_days_list, "HOLIDAY": holiday_list
         })

    load_physical_data.START_DATE = pd.to_datetime(load_physical_data.START_DATE)
    load_physical_data.END_DATE = pd.to_datetime(load_physical_data.END_DATE)
    load_physical_data['vol/day'] = np.where(load_physical_data['PRICING_METHOD'] == 'Float',
                                             np.round(
                                                 load_physical_data['TOTAL_VOLUME'] / load_physical_data['TOTAL_DAYS'],
                                                 2), load_physical_data['TOTAL_VOLUME'])

    print(load_physical_data,'load_physical_data')

    df_filtered = load_physical_data[
        (load_physical_data['START_DATE'].dt.month == month) | (load_physical_data['END_DATE'].dt.month == month)]
    physical_contract_list = df_filtered['PRICING_CONTRACT'].unique().tolist()

    print("df_filtered",df_filtered)

    start_date_str = str(year) + "-" + str(month) + "-" + str(first_date)
    end_date_str = str(year) + "-" + str(month) + "-" + str(num_days)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    physical_dates = pd.date_range(start_date, end_date, freq='D')
    dict = {'DATES': physical_dates}
    physical_df = pd.DataFrame(dict)
    print(physical_df,'physical_df')

    Holiday_date_list = []
    Holiday_type_list = []

    for obj in HolidayM.objects.all():
        Holiday_date_list.append(str(obj.date))
        Holiday_type_list.append(str(obj.name))

    holiday_data_df = pd.DataFrame({"Date": Holiday_date_list, "Holiday": Holiday_type_list})
    holiday_data_df['Date'] = pd.to_datetime(holiday_data_df['Date'])
    # print('Holidays_data',holiday_data_df)

    physical_list_dict = {}
    holiday_list_dict = {}

    for i in physical_contract_list:
        physical_list_dictionary = []
        holiday_list_dictionary = []
        print(i)
        contract_physical_data = df_filtered[(df_filtered["PRICING_CONTRACT"] == i)]
        contract_physical_data = pd.DataFrame(contract_physical_data)
        print(contract_physical_data,'contract_physical_data')

        for index, row in contract_physical_data.iterrows():
            holiday_name = row["HOLIDAY"]

            hld_df_physical = holiday_data_df.loc[holiday_data_df['Holiday'] == row['HOLIDAY']]
            hld_date_physical = hld_df_physical['Date'].to_list()
            print(hld_date_physical,'hld_date_physical')

            for hd in hld_date_physical:
                hd_month = hd.month
                current_month = datetime.now().month
                # if hd_month==current_month:
                for dts in physical_df['DATES']:
                    phys_curr_date = str(dts.date())

                    if dts.date() >= row['START_DATE'].date() and dts.date() <= row['END_DATE'].date():
                        print("month_date", dts)
                        print(hd.date(), 'check hd_date', dts.date(), 'dts_date')

                        if dts.date() not in ( [d.date() for d in hld_date_physical]):
                            print('NOt in HD')
                            physical_list_dict.update({phys_curr_date: row['vol/day']})
                            holiday_list_dict.update({phys_curr_date: 1})
                            # print(holiday_list_dict,'holiday_list_dict')
                        elif dts.date() in ([d.date() for d in hld_date_physical]):
                            print('HD Present')
                            physical_list_dict.update({phys_curr_date: 0})
                            holiday_list_dict.update({phys_curr_date: 0})
                    else:
                        physical_list_dict.update({phys_curr_date: 0})
                        holiday_list_dict.update({phys_curr_date: 0})

            df_dict_phys = pd.DataFrame(physical_list_dict.items(), columns=['Date', 'DateValue'])
            df_holiday_phys = pd.DataFrame(holiday_list_dict.items(), columns=['Date', 'hd_bool'])

            df_dict_phys.set_index(['Date'], inplace=True)
            df_holiday_phys.set_index(['Date'], inplace=True)

            physical_list_dictionary.append(df_dict_phys)
            print(physical_list_dictionary)
            holiday_list_dictionary.append(df_holiday_phys)
            print('holiday_list_dictionary',holiday_list_dictionary)
            print('physical_list_dictionary', physical_list_dictionary)


        df_physical_final = reduce(lambda a, b: a.add(b, fill_value=0), physical_list_dictionary)
        hd_physical_final = reduce(lambda a, b: a.add(b, fill_value=0), holiday_list_dictionary)

        df_physical_final = df_physical_final.rename(columns={'DateValue': i})
        hd_physical_final = hd_physical_final.rename(columns={'hd_bool': i})

        df_physical_final.index = pd.to_datetime(df_physical_final.index)
        df_physical_final.reset_index(inplace=True)

        hd_physical_final.index = pd.to_datetime(hd_physical_final.index)
        hd_physical_final.reset_index(inplace=True)

        for index, rows in contract_physical_data.iterrows():
            hld_df_physical = holiday_data_df.loc[holiday_data_df['Holiday'] == rows['HOLIDAY']]
            if i == rows['PRICING_CONTRACT']:
                if i in hdval_physical_dict:
                    if rows['HOLIDAY'] not in hdval_physical_dict[i]:
                        hdval_physical_dict[i].append(rows['HOLIDAY'])
                        hdval_physical_dict[i].append(",")
                else:
                    hdval_physical_dict[i] = [rows['HOLIDAY']]
                    hdval_physical_dict[i].append(",")

            hld_date_physical = hld_df_physical['Date'].to_list()
            for hd in hld_date_physical:
                df_physical_final.loc[
                    (hd_physical_final[i] == 0) & (df_physical_final['Date'].isin([hd.date()])), i] = 'HLD'
            df_physical_final.loc[(df_physical_final['Date'].dt.dayofweek > 4), i] = 'WKND'

        df_physical_final.set_index(['Date'], inplace=True)
        physical_full_df.append(df_physical_final)

    if len(physical_full_df) > 0:
        physical_hedging = pd.concat(physical_full_df, axis=1, ignore_index=False)
        physical_hedging.reset_index(inplace=True)

        physical_hedging['Date'] = physical_hedging["Date"].dt.strftime("%d-%b-%y")
        physical_hedging.set_index(['Date'], inplace=True)
        physical_hedging_t = physical_hedging.T
        physical_hedging_t.index.rename('Contracts', inplace=True)
        physical_hedging_t.reset_index(inplace=True)
        for i in physical_contract_list:
            hdToStr = ' '.join(map(str, hdval_physical_dict[i]))
            hdToStr = hdToStr[:-1]
            physical_hedging_t.loc[(physical_hedging_t['Contracts'] == i), 'HLD'] = hdToStr
            mid_phy = physical_hedging_t['HLD']
            physical_hedging_t.drop(labels=['HLD'], axis=1, inplace=True)
            physical_hedging_t.insert(1, 'HLD', mid_phy)

    else:

        physical_hedging = physical_df
        physical_hedging['DATES'] = physical_hedging["DATES"].dt.strftime("%d-%b-%y")
        physical_hedging.set_index(['DATES'], inplace=True)
        physical_hedging_t = physical_hedging.T


    print(physical_hedging_t,'physical_hedging_t')



    #
    context = {
        "physical_hedging_t": physical_hedging_t,
        # "sb_headging_df":sb_headging_df,

    }
    # return render(request, "customer/hedge-pb.html", context)
    return render(request, "customer/physical_hedge.html", context)






### Inventory tansfer discharge load

# Inventory tansfer discharge load same as swap
class LoadDischargeInventory(CheckUserMixins,View):
    # def get(self, request, **kwargs):
    #     obj = InventoryModel.objects.get(id=kwargs['id'])
    #
    #     port = PortM.objects.all()
    #     print("port :", port)
    #     terminal = TerminalM.objects.all()
    #     print("terminal :", terminal)
    #     tank = TankCapacityM.objects.all()
    #     unit = Unit1.objects.all()
    #
    #     tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
    #     print("tank_distinct:",tank_distinct)
    #
    #     print("Tank no:",tank)
    #     context = {
    #         'd': obj,'port':port,'terminal':terminal,'tank':tank,'unit':unit,
    #     }
    #     print("context end:")
    #     return render(request, "customer/load-discharge.html", context )

    def get(self, request, **kwargs):

        obj = InventoryModel.objects.get(id=kwargs['id'])
        # +++++++++get from form++++++++++++++++++++++++++++

        get_trade_id = obj.Trade_id

        print(get_trade_id, 'get_trade_id')
        get_purchase_sales_id = obj.Purchase_sales_ID
        get_vesselname = obj.Vessal_name
        get_port = obj.Port
        get_terminal = obj.Terminal
        get_tank = obj.Tank
        get_deliverymode = obj.Delivery_mode

        print(get_deliverymode, 'get_deliverymode+++++++++++++')

        pb_trade_id = []
        pb_purchase_sales_id = []
        pb_container = []
        pb_port = []
        pb_terminal = []
        pb_vessel = []
        pb_shore_received_qty = []
        pb_loss_gain = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_book = []
        pb_Strategy = []

        if get_deliverymode == 'Tank' or get_deliverymode == 'PLT':

            physical_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Port=get_port).filter(
                Terminal=get_terminal).filter(Tank=get_tank)
            inventory_cargo = InventoryModel.objects.filter(Port=get_port).filter(Terminal=get_terminal).filter(
                Tank=get_tank)

        elif get_deliverymode == 'Vessel':

            physical_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Port=get_port).filter(
                Terminal=get_terminal).filter(Vessal_name=get_vesselname)

            inventory_cargo = InventoryModel.objects.filter(Port=get_port).filter(Terminal=get_terminal).filter(
                Vessal_name=get_vesselname)

        for pbx in physical_cargo:
            pb_status.append(pbx.status)
            pb_trade_id.append(pbx.Trade_id)
            pb_purchase_sales_id.append(pbx.Purchase_sales_ID)
            pb_book.append(pbx.Book)
            pb_Strategy.append(pbx.Strategy)
            pb_container.append(pbx.Delivery_mode)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_vessel.append(pbx.Vessal_name)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_loss_gain.append(pbx.Difference)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)

        pb_dict = {'Status': pb_status, 'Trade_id': pb_trade_id, 'Purchase_Sales_id': pb_purchase_sales_id,
                   'Book': pb_book, 'Strategy': pb_Strategy, 'Delivery_mode': pb_container,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Vessal': pb_vessel, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Gain_Loss': pb_loss_gain, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density}

        discharged_df = pd.DataFrame(pb_dict)
        discharged_df['Vessel_Tank'] = np.where(discharged_df['Delivery_mode'] == 'Vessel', discharged_df['Vessal'],
                                                discharged_df['Tank'])

        current_pb_qty = discharged_df['Shore_received'].sum()
        print(current_pb_qty, 'current_pb_qty')

        inv_trade_id = []
        inv_purchase_sales_id = []
        inv_distribution_type = []
        inv_strategy = []
        inv_delivery_mode = []
        inv_tank = []
        inv_vessel = []
        inv_port = []
        inv_terminal = []
        inv_unit = []
        inv_density = []
        inv_current_qty = []
        inv_dest_difference = []
        inv_cargo = []

        for invx in inventory_cargo:
            inv_trade_id.append(invx.Trade_id)
            inv_purchase_sales_id.append(invx.Purchase_sales_ID)
            inv_distribution_type.append(invx.Distribution_Type)
            inv_strategy.append(invx.Strategy)
            inv_delivery_mode.append(invx.Delivery_mode)
            inv_tank.append(invx.Tank)
            inv_vessel.append(invx.Vessal_name)
            inv_port.append(invx.Port)
            inv_terminal.append(invx.Terminal)
            inv_unit.append(invx.Unit)
            inv_density.append(invx.Density)
            inv_current_qty.append(invx.source_cargo_LD_QTY)
            inv_cargo.append(invx.Cargo)
            inv_dest_difference.append(invx.dest_difference)

        inv_dict = {'Trade_id': inv_trade_id, 'Purchase_Sales_id': inv_purchase_sales_id,
                    'Strategy': inv_strategy, 'Delivery_mode': inv_delivery_mode,
                    'Port': inv_port, 'Terminal': inv_terminal, 'Vessal': inv_vessel, 'Tank': inv_tank,
                    'Shore_received': inv_current_qty, 'Gain_Loss': inv_dest_difference, 'Cargo': inv_cargo,
                    'Unit': inv_unit, 'Density': inv_density}

        inventory_df = pd.DataFrame(inv_dict)
        inventory_df['Vessel_Tank'] = np.where(inventory_df['Delivery_mode'] == 'Vessel', inventory_df['Vessal'],
                                               inventory_df['Tank'])

        inventory_current_qty = inventory_df['Shore_received'].sum()

        print('inventory_current_qtyt', inventory_current_qty, 'current_pb_qty', current_pb_qty)

        current_container_qty = float(current_pb_qty) + float(inventory_current_qty)

        print('Secondory Transfer Current QUANTITY', current_container_qty)

        port = PortM.objects.all()
        terminal = TerminalM.objects.all()
        tank = TankCapacityM.objects.all()
        unit = Unit1.objects.all()

        tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
        context = {
            'd': obj, 'port': port, 'terminal': terminal, 'tank': tank, 'unit': unit,
            'current_container_qty': current_container_qty
        }
        return render(request, "customer/load-discharge.html", context)


    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                        (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                        tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                           Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                           Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")

    #
    # def post(self, request, *args, **kwargs):
    #     # obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
    #
    #     #From
    #     print(" post methode:")
    #     date = request.POST.get('date', '')
    #     print("date:", date)
    #     trade_id = request.POST.get('trade_id', '')
    #     purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
    #     print("purchase_sales_id:", purchase_sales_id)
    #     distribution_type = request.POST.get('distribution_type', '')  # id
    #     print("distribution_type:",distribution_type)
    #     deliverymode = request.POST.get('deliverymode', '')
    #     tank = request.POST.get('tank', '')
    #     print("tank:", tank)
    #     strategy = request.POST.get('strategy', '')
    #     print("strategy:", strategy)
    #     vesselname = request.POST.get('vesselname', '')
    #     print("vesselname:",vesselname)
    #     port = request.POST.get('port', '')
    #     terminal = request.POST.get('terminal', '')
    #     cargo = request.POST.get('cargo', '')  # id
    #     instock_shore_recieved = request.POST.get('shore_recieved', '')
    #     density = request.POST.get('density', '')
    #     unit = request.POST.get('unit', '')
    #
    #     # To
    #     print("To Get")
    #     dest_container_to = request.POST.get('dest_container_to', '')
    #     port_to = request.POST.get('port_to', '')
    #     terminal_to = request.POST.get('terminal_to', '')
    #     tankno_to = request.POST.get('tankno_to', '')
    #     print("tankno_to",tankno_to)
    #     vessalname_to = request.POST.get('vessalname_to', '')
    #     inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
    #     unit_to = request.POST.get('unit_to', '')
    #     dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
    #     print("dest_cargo_LD_QTY_to", dest_cargo_LD_QTY_to)
    #     dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
    #     print("dest_received_qty_to", dest_received_qty_to)
    #     temperature = request.POST.get('temperature', '')
    #     print("temperature", temperature)
    #
    #     delete_feild = request.POST.get('delete_feild')
    #     if delete_feild:
    #         obj = InventoryModel.objects.get(id=delete_feild)
    #         obj.delete()
    #         return HttpResponseRedirect("/inventory-list/")
    #
    #     #conversion
    #     dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
    #     print("dest_cargo_LD_QTY_to", dest_cargo_LD_QTY_to)
    #     dest_received_qty_to = float(dest_received_qty_to)
    #     print("dest_received_qty_to", dest_received_qty_to)
    #     if tankno_to:
    #         tankno_to = tankno_to
    #     else:
    #         pass
    #
    #     print("tankno_to", tankno_to)
    #
    #     print("retrieved")
    #     print("dest_received_qty_to:",dest_received_qty_to)
    #
    #     dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)
    #     print("swapLD QTY:", dest_cargo_LD_QTY_to)
    #     source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
    #     print("source_cargo_ld_qty:", source_cargo_ld_qty)
    #
    #     dest_diff = float(dest_cargo_LD_QTY_to) - float(dest_received_qty_to)
    #     print("dest_difference:", dest_diff)
    #
    #     # updating tank capacity model
    #     print("****** UPDATING TANK CAPACITY MODEL ******")
    #
    #
    #     print("Tank no:",tankno_to)
    #     tank_detail = TankCapacityM.objects.filter(Tank_no__name=tankno_to)
    #     print("Tank detail:",tank_detail)
    #
    #
    #
    #     for i in tank_detail:
    #         print(i, 'i insde')
    #         print("###### THE START tank ############")
    #         safe_fill_capacity = i.Safe_fill_capacity
    #         remaining_space = float(safe_fill_capacity) - float(dest_received_qty_to)
    #         print(safe_fill_capacity, 'safe_fill:', remaining_space, 'safe_fill:')
    #         print("Hello updates")
    #         TankCapacityM.objects.filter(Tank_no__name=tankno_to).update(current_quantity=dest_received_qty_to,
    #                                     Remaining_space=remaining_space)
    #         print("updated")
    #
    #
    #
    #
    #     print("object creation for pb")
    #     obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id, Distribution_Type=distribution_type,
    #                              Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
    #                              Vessal_name=vesselname,
    #                              Port=port, Terminal=terminal,Cargo=cargo, Unit=unit,
    #                              Shore_recieved=instock_shore_recieved, Density=density,
    #                          #to
    #                              dest_container=dest_container_to, dest_port=port_to,
    #                              dest_terminal=terminal_to,dest_vessal_op=vessalname_to,
    #                              dest_tank_num=tankno_to,
    #                              inv_transfer_mode=inv_transfer_mode_to, dest_unit=unit_to,
    #                              dest_cargo_LD_QTY=dest_cargo_LD_QTY_to, dest_received_qty=dest_received_qty_to,
    #                              temperature=temperature,
    #                          # calculated values
    #                              source_cargo_LD_QTY=source_cargo_ld_qty, dest_difference=dest_diff,
    #
    #                              )
    #     obj.save()
    #     print(" saved pb")
    #     messages.info(request, 'Inventory Saved')
    #     return HttpResponseRedirect('/inventory-list/')

    def post(self, request, *args, **kwargs):
        # obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # From
        print(" post methode:")
        date = request.POST.get('date', '')
        trade_id = request.POST.get('trade_id', '')
        purchase_sales_id = request.POST.get('purchase_sales_id', '')  # id
        distribution_type = request.POST.get('distribution_type', '')  # id
        deliverymode = request.POST.get('deliverymode', '')
        source_container = deliverymode
        tank = request.POST.get('tank', '')
        strategy = request.POST.get('strategy', '')
        vesselname = request.POST.get('vesselname', '')
        port = request.POST.get('port', '')
        terminal = request.POST.get('terminal', '')
        cargo = request.POST.get('cargo', '')  # id
        instock_shore_recieved = request.POST.get('shore_recieved', '')
        instock = float(instock_shore_recieved)
        density = request.POST.get('density', '')
        unit = request.POST.get('unit', '')

        # To
        print("To Get")
        dest_container_to = request.POST.get('dest_container_to', '')
        port_to = request.POST.get('port_to', '')
        terminal_to = request.POST.get('terminal_to', '')
        tankno_to = request.POST.get('tankno_to', '')
        vessalname_to = request.POST.get('vessalname_to', '')
        inv_transfer_mode_to = request.POST.get('inv_transfer_mode_to', '')
        unit_to = request.POST.get('unit_to', '')
        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
        temperature = request.POST.get('temperature', '')

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = InventoryModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        # conversion
        if float(instock) < 0:
            print('Cannot transfer cargo having quatity less than 0')
            raise

        if float(dest_cargo_LD_QTY_to) < 0 or float(dest_received_qty_to) < 0:
            print('Cannot transfer cargo having quatity less than 0')
            raise

        dest_cargo_LD_QTY_to = request.POST.get('dest_cargo_LD_QTY_to', '')
        dest_cargo_LD_QTY_to = float(dest_cargo_LD_QTY_to)
        dest_cargo_LD_QTY_to = abs(dest_cargo_LD_QTY_to)

        dest_received_qty_to = request.POST.get('dest_received_qty_to', '')
        dest_received_qty_to = float(dest_received_qty_to)
        dest_received_qty_to = abs(dest_received_qty_to)
        source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':
            if (str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(tank) == str(tankno_to)):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        elif dest_container_to == 'Vessel':
            if str(port) == str(port_to) and str(terminal) == str(terminal_to) and str(vesselname) == str(
                    vessalname_to):
                print('Source and Destination is same.Not allowed..Give Different Source and Destination')
                raise

        if unit == 'MT':

            instock_m3 = round(float(instock) / float(density), 3) if float(
                density) < 1 else round(float(instock) / (float(density) / 1000), 3)

            if unit_to == 'MT':

                # In MT
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)
                # Convert MT to m3 equ: MT/Density if Density less than 0 else MT/(Density/1000)
                dest_received_qty_to_m3 = round(float(dest_received_qty_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float(dest_cargo_LD_QTY_to) / float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                # Convert   m3 to MT equ: MT*Density if Density less than 0 else MT*(Density/1000)

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'bbl':

            instock_m3 = round(float((instock) / 6.289) / float(density), 3) if float(
                density) < 1 else round(float((instock) / 6.289) / (float(density) / 1000), 3)

            if unit_to == 'bbl':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(dest_cargo_LD_QTY_to)

                # Convert bbl to m3 equ: (bbl/6.289)/Density if Density less than 0 else bbl/6.289/(Density/1000)

                dest_received_qty_to_m3 = round(float((dest_received_qty_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = round(float((dest_cargo_LD_QTY_to) / 6.289) / float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) / 6.289) / (float(density) / 1000), 3)
                source_cargo_ld_qty_m3 = -(abs(source_cargo_ld_qty_m3))

            elif unit_to == 'm3':

                dest_received_qty_to_m3 = dest_received_qty_to
                source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        elif unit == 'm3':

            dest_received_qty_to_m3 = dest_received_qty_to
            source_cargo_ld_qty_m3 = -(dest_cargo_LD_QTY_to)
            instock_m3 = float(instock)

            if unit_to == 'm3':
                dest_received_qty_to = dest_received_qty_to
                source_cargo_ld_qty = -(abs(dest_cargo_LD_QTY_to))

            elif unit_to == 'MT':

                dest_received_qty_to = round(float(dest_received_qty_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_received_qty_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float(dest_cargo_LD_QTY_to) * float(density), 3) if float(
                    density) < 1 else round(float(dest_cargo_LD_QTY_to) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

            elif unit_to == 'bbl':

                dest_received_qty_to = round(float((dest_received_qty_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_received_qty_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = round(float((dest_cargo_LD_QTY_to) * 6.289) * float(density), 3) if float(
                    density) < 1 else round(float((dest_cargo_LD_QTY_to) * 6.289) * (float(density) / 1000), 3)
                source_cargo_ld_qty = -(abs(source_cargo_ld_qty))

        dest_diff = abs(float(dest_received_qty_to)) - abs(float(source_cargo_ld_qty))

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = InventoryModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        if dest_container_to == 'Tank' or dest_container_to == 'PLT':

            tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tankno_to)).filter(
                Port__name=port_to).filter(Terminal__name=terminal_to)
            for i in tank_capacity:
                safe_fill_capacity = i.Safe_fill_capacity
                remaining_space = i.Remaining_space

            if abs(float(source_cargo_ld_qty_m3)) > float(remaining_space):
                print('remaining_space', remaining_space)
                print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
                print('This much quatity cannot accpmodate in this tank')
                raise

        if abs(float(source_cargo_ld_qty_m3)) > (float(instock_m3)):
            print('Instockm3', instock_m3)
            print('Transferm3', abs(float(source_cargo_ld_qty_m3)))
            print('quantity trying to transfer is greater than instock')
            raise
        else:
            print('Instockm3', instock_m3)
            print('Transferm3', source_cargo_ld_qty_m3)

        print("object creation for pb")

        # NEED SAME ID(Reference id)
        source_list = [tank, port, terminal]
        dest_list = [tankno_to, port_to, terminal_to]
        print(source_list, 'source_list')
        print(dest_list, 'dest_list')
        print(dest_container_to, 'dest_container_to')
        print(source_container, 'source_container')

        obj = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                             Distribution_Type=distribution_type,
                             Delivery_mode=deliverymode, Tank=tank, Strategy=strategy,
                             Vessal_name=vesselname,
                             Port=port, Terminal=terminal, Cargo=cargo, Unit=unit, dest_unit=unit_to,
                             Density=density, dest_cargo_LD_QTY=0,
                             inv_transfer_mode=inv_transfer_mode_to, dest_difference=0,
                             dest_received_qty=0, source_cargo_LD_QTY=source_cargo_ld_qty, m3=source_cargo_ld_qty_m3,
                             # Not Required Field
                             dest_container=dest_container_to, dest_port=port_to,
                             dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                             dest_tank_num=tankno_to,

                             )

        obj.save()
        obj.duplicate_id = obj.id
        obj.save()

        obj1 = InventoryModel(date=date, Trade_id=trade_id, Purchase_sales_ID=purchase_sales_id,
                              Distribution_Type=distribution_type,
                              Delivery_mode=dest_container_to, Tank=tankno_to, Strategy=strategy,
                              Vessal_name=vessalname_to,
                              Port=port_to, Terminal=terminal_to, Cargo=cargo, Unit=unit,
                              Density=density, dest_unit=unit_to,
                              inv_transfer_mode=inv_transfer_mode_to, dest_difference=dest_diff,
                              dest_received_qty=dest_received_qty_to,
                              source_cargo_LD_QTY=dest_received_qty_to, m3=dest_received_qty_to_m3,
                              Shore_recieved=dest_cargo_LD_QTY_to,
                              # Not Required Field
                              dest_cargo_LD_QTY=0,
                              dest_container=dest_container_to, dest_port=port_to,
                              dest_terminal=terminal_to, dest_vessal_op=vessalname_to,
                              dest_tank_num=tankno_to, duplicate_id=obj.id

                              )
        obj1.save()

        tank_updation_list = []

        if dest_container_to == 'Tank' or source_container == 'Tank' or dest_container_to == 'PLT' or source_container == 'PLT':
            print('+++++++++++++++++')

            if (dest_container_to == 'Tank' or dest_container_to == 'PLT') and (
                    source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                tank_updation_list.append(dest_list)
                print('first______', tank_updation_list)

            elif (dest_container_to == 'Tank' or dest_container_to == 'PLT') and source_container != 'Tank':
                tank_updation_list.append(dest_list)
                print('second______', tank_updation_list)
            elif dest_container_to != 'Tank' and (source_container == 'Tank' or source_container == 'PLT'):
                tank_updation_list.append(source_list)
                print('third_____', tank_updation_list)

            print('m3=m3,Density=density_uom,', tank_updation_list)

            self.tank_update(request, tank_updation_list, cargo, density)

        messages.info(request, 'Inventory Saved')
        return HttpResponseRedirect('/inventory-list/')









##############  Inventory sale  #####################



# Inventory tansfer discharge load same as swap
class InventorySale(CheckUserMixins,View):
    def get(self, request, **kwargs):
        obj = InventoryModel.objects.get(id=kwargs['id'])

        port = PortM.objects.all()
        print("port :", port)
        terminal = TerminalM.objects.all()
        print("terminal :", terminal)
        tank = TankCapacityM.objects.all()
        pricing_contract = ContractM.objects.all()

        tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
        print("tank_distinct:",tank_distinct)

        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:", holiday_distict)

        uniq_holiday_list = []
        for x in holiday_distict:
            if x not in uniq_holiday_list:
                uniq_holiday_list.append(x)
        print("uniq_holiday_list:", uniq_holiday_list)


        print("Tank no:",tank)
        context = {
            'd': obj,'port':port,'terminal':terminal,
            'tank':tank,'pricing_contract':pricing_contract,
            'holiday':uniq_holiday_list,
        }
        print("context end:")
        return render(request, "customer/sale-inv-pb.html", context )

    def post(self, request, *args, **kwargs):
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:", date)
        tradeid = request.POST.get('tradeid', '')
        print("tradeid:", tradeid)
        trader = request.POST.get('trader', '')  # id
        print("trader:", trader)
        book = request.POST.get('book', '')  # id
        print("book:", book)
        company_name = request.POST.get('company_name', '')
        print("company_name:", company_name)
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        derivatives = request.POST.get('derivatives', '')
        print("derivatives:", derivatives)
        # buysell = request.POST.get('buysell', '')
        cargo = request.POST.get('cargo', '')
        print("cargo:", cargo)
        pricing_contract = request.POST.get('pricing_contract', '')
        print("pricing_contract:", pricing_contract)
        pricing_methode = request.POST.get('pricing_methode', '')  # id
        print("pricing_methode:", pricing_methode)
        volume = request.POST.get('quantity', '')
        print("volume QTY:", volume)
        unit = request.POST.get('unit', '')
        print("Unit", unit)
        density = request.POST.get('density', '')
        print("density:", density)
        nominated_quantity = request.POST.get('nominated_quantity', '')
        print("nominated_quantity:", nominated_quantity)
        premium_discount = request.POST.get('premium_discount', '')
        print("premium_discount:", premium_discount)
        pricing_term = request.POST.get('pricing_term', '')
        bl_date = request.POST.get('bl_date', '')
        print("BL date:", bl_date)
        start_date = request.POST.get('start_date', '')
        print("start_date:", start_date)
        end_date = request.POST.get('end_date', '')
        print("end_date:", end_date)
        holiday = request.POST.get('holiday', '')
        print("holiday get:", holiday)
        deliverymode = request.POST.get('deliverymode', '')
        port = request.POST.get('port', '')
        print("port:", port)
        terminal = request.POST.get('terminal', '')
        vessal_name = request.POST.get('vessal_name', '')
        tank = request.POST.get('tank', '')
        print("Tank", tank)
        external_terminal = request.POST.get('external_terminal', '')
        hedging = request.POST.get('hedging', '')
        Remarks = request.POST.get('Remarks', '')

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = PhysicalBlotterModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        # # update status in admin side :
        # admin_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        # current_admin_status = admin_status.Status
        # print("current status:", current_admin_status)
        #
        # update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
        # update_status_in_admin.Status = "Process"
        # update_status_in_admin.save()

        # print("after updating status:", update_status_in_admin.Status)
        #
        # Purchase/salesID
        volume = float(volume)

        print("volumeb4:",volume)

        volume = -abs(volume)
        print("negative volume:", volume)

        if volume >= 0:
            print("Buying")
            print("cargo buying:", cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "P" + "-" + cargo + "-" + randint_
            print("purchase_id buying:", purchase_id)
            buysell = "Buy"
        elif volume <= 0:
            print("selling")
            print("cargo selling:", cargo)
            cargo = str(cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "S" + "-" + cargo + "-" + randint_
            print("purchase_id selling:", purchase_id)
            buysell = "Sell"
        else:
            pass
        #
        print("************* Coversion from string to particular type")

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        print("converted start_date:", start_date)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        print("converted end_date:", end_date)

        date_ = datetime.strptime(date, '%Y-%m-%d').date()
        print("converted date_:", date_)

        bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        print("converted bl_date:", bl_date)
        print('****************************************')

        # HOLIDAY DATE LIST OF SELECTED HOLIDAY in DATAFRAME

        #   the working holiday list dates  using data frame
        print("Finding holiday:")
        print("Holioday selected", holiday)
        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        # workingdays
        holi_list_selcted = []
        for i in holiday_list_of_selected_holi:
            holi_list_selcted.append(i)
        print("new list of selected holi:", holi_list_selcted)

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holi_list_selcted, 'first++++++++total_swap_days')

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holi_list_selcted = holiday_date_df['Dates'].to_list()
        print(holiday_list, 'first++++++++total_swap_days')

        total_working_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holi_list_selcted))
        print(total_working_days, '++++++++total_swap_days')

        # <!----- priced and unpriced days start ----!>

        print("Priced unpriced starting")

        if date_ <= start_date:
            print("first condition priced days")
            priced_days = 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            unpriced_days = len(unprice_calcu)
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (date_ > start_date) and (date_ <= end_date):
            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=holi_list_selcted))

            workday = len(pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted))
            priced_days = workday - unpriced_days
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
        #
        elif (date_ > end_date):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        else:
            pass

        print("Priced unpriced end")
        # <!----- priced unpriced end ---!>

        # # <!-----priced volume ----!>

        print("Priced volume begining")

        pricing_methode = str(pricing_methode)
        unit = str(unit)

        if pricing_methode == "Fixed":
            print('hi')
            print("startdate:", start_date)
            print("enddate:", end_date)

            if start_date == end_date:
                total_volume = volume
                total_volume = round(volume, 3)
                print("totalk volume:", total_volume)
                priced_volume = total_volume
                unpriced_volume = 0
                # instance = form.save(commit=False)
                # instance.total_volume = total_volume
                # # instance.position = total_volume
                # instance.price_volume = priced_volume
                # instance.unprice_volume = unpriced_volume
                # instance.save()
                print('+++++++++++++++++++++++++++++++++++++++++')
            else:
                pass
        elif pricing_methode == "Float":
            total_volume = volume
            priced_volume = (total_volume / total_working_days) * priced_days
            priced_volume = round(priced_volume, 3)
            print("priced volume:", priced_volume)
            unpriced_volume = (total_volume / total_working_days) * unpriced_days
            unpriced_volume = round(unpriced_volume, 3)
            print("unpriced_volume", unpriced_volume)
            # instance = form.save(commit=False)
            # instance.total_volume = total_volume
            # # instance.position = total_volume
            # instance.price_volume = priced_volume
            # instance.unprice_volume = unpriced_volume
            # instance.save()
            print('+++++++++++++++++++++++++++++++++++++++++')

        # ######## status change ###############
        status = "Open"
        status = str(status)
        print("status converted to open:", status)

        shore_recieved = 0

        # generate_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        # print("hai", generate_status.Status)
        # print("testing")

        print("total volume b4:", total_volume)
        #
        print("object creation for pb")
        obj = PhysicalBlotterModel(Date=date, Trader=trader, Book=book, Company_name=company_name,
                                   Strategy=strategy, Derivative=derivatives,
                                   Trade_id=tradeid, Buy_sell=buysell,
                                   Cargo=cargo,
                                   Pricing_contract_id=pricing_contract, Pricing_method=pricing_methode,
                                   Quantity=volume, Unit=unit,
                                   Density=density, Nominated_quantity=nominated_quantity,
                                   Premium_discount=premium_discount, Pricing_term=premium_discount,

                                   bl_date=bl_date, start_date=start_date, end_date=end_date,
                                   Holiday=holiday,
                                   Total_no_days=total_working_days, Delivery_mode=deliverymode,
                                   Port=port, Terminal=terminal,
                                   Vessal_name=vessal_name, Tank=tank, Remarks=Remarks,
                                   External_Terminal=external_terminal, Headging=hedging,
                                   #                            # calculated and_ get_values
                                   Purchase_sales_ID=purchase_id, status=status,
                                   price_days=priced_days, unprice_days=unpriced_days,
                                   total_volume=total_volume, price_volume=priced_volume,
                                   unprice_volume=unpriced_volume, Shore_recieved=shore_recieved
                                   )
        obj.save()
        print(" saved Inventory Sale")
        messages.info(request, 'Inventory Sale Saved')
        return HttpResponseRedirect('/pb-list/')

##### Discharge cargo sale
class DischargeCargoSale(CheckUserMixins,View):
    def get(self, request, **kwargs):
        obj = PhysicalBlotterModel.objects.get(id=kwargs['id'])

        port = PortM.objects.all()
        print("port :", port)
        terminal = TerminalM.objects.all()
        print("terminal :", terminal)
        tank = TankCapacityM.objects.all()
        pricing_contract = ContractM.objects.all()

        tank_distinct = TankCapacityM.objects.order_by().values_list('Tank_no__name').distinct()
        print("tank_distinct:",tank_distinct)

        holiday_distict = HolidayM.objects.values_list('name', flat=True).distinct()
        print("Holiday distinct:", holiday_distict)

        uniq_holiday_list = []
        for x in holiday_distict:
            if x not in uniq_holiday_list:
                uniq_holiday_list.append(x)
        print("uniq_holiday_list:", uniq_holiday_list)


        print("Tank no:",tank)
        context = {
            'd': obj,'port':port,'terminal':terminal,
            'tank':tank,'pricing_contract':pricing_contract,
            'holiday':uniq_holiday_list,
        }
        print("context end:")
        return render(request, "customer/sale-discharge-pb.html", context )

    def tank_update(self, request, tank_details, cargo, Density):

        pb_port = []
        pb_terminal = []
        pb_shore_received_qty = []
        pb_status = []
        pb_cargo = []
        pb_unit = []
        pb_tank = []
        pb_density = []
        pb_m3 = []

        for data in tank_details:
            print(data, 'tank list to updation')

            tank_number = data[0]
            port = data[1]
            terminal = data[2]

        print(terminal, 'terminal', 'tank_number', tank_number, 'port', port)
        discharged_cargo = PhysicalBlotterModel.objects.filter(status='Open').filter(Tank=tank_number).filter(
            Port=port).filter(Terminal=terminal)

        for pbx in discharged_cargo:
            pb_status.append(pbx.status)
            pb_port.append(pbx.Port)
            pb_terminal.append(pbx.Terminal)
            pb_tank.append(pbx.Tank)
            pb_shore_received_qty.append(pbx.Shore_recieved)
            pb_cargo.append(pbx.Cargo)
            pb_unit.append(pbx.Unit)
            pb_density.append(pbx.Density)
            pb_m3.append(pbx.m3)

        pb_dict = {'Status': pb_status,
                   'Port': pb_port, 'Terminal': pb_terminal, 'Tank': pb_tank,
                   'Shore_received': pb_shore_received_qty, 'Cargo': pb_cargo,
                   'Unit': pb_unit, 'Density': pb_density, 'm3': pb_m3}

        discharged_df = pd.DataFrame(pb_dict)

        print('Physical Blotter Quantity', discharged_df)

        if len(discharged_df) > 0:

            discharged_df['pb_convert_m3_MT'] = [(discharged_df['m3'] * discharged_df['Density']) if x < 1 else (
                    (discharged_df['m3']) * (discharged_df['Density'] / 1000)) for x in discharged_df['Density']]

            discharged_df['current_qty_MT'] = np.where(discharged_df['Unit'] == 'MT', discharged_df['Shore_received'],
                                                       discharged_df['pb_convert_m3_MT'])

            pb_update_current_qty_m3 = round(discharged_df['m3'].sum(), 3)
            pb_update_current_qty_MT = round(discharged_df['current_qty_MT'].sum(), 3)
        else:
            pb_update_current_qty_m3 = 0.0
            pb_update_current_qty_MT = 0.0

        tank_capacity = TankCapacityM.objects.filter(Tank_no__name=str(tank_number)).filter(Port__name=port).filter(
            Terminal__name=terminal)
        for i in tank_capacity:
            safe_fill_capacity = i.Safe_fill_capacity
            remaining_space = i.Remaining_space

        print('Tank Capasity Quantity', tank_capacity, safe_fill_capacity, 'safe_fill_capacity', 'remaining_space',
              remaining_space)

        inventory_transfer = InventoryModel.objects.filter(Tank=tank_number).filter(Port=port).filter(Terminal=terminal)
        m3_list = []
        mt_bbl_m3_list = []
        unit_list = []
        density_list = []

        for inv_data in inventory_transfer:
            m3_list.append(inv_data.m3)
            mt_bbl_m3_list.append(inv_data.dest_received_qty)
            unit_list.append(inv_data.Unit)
            density_list.append(inv_data.Density)

        dict_tank_details = {'current_qty_m3': m3_list, 'Current_QTY': mt_bbl_m3_list, 'Unit': unit_list,
                             'Density': density_list}
        tank_details_df = pd.DataFrame(dict_tank_details)

        print('Inventory Blotter Quantity', tank_details_df)
        #
        tank_details_df['convert_m3_MT'] = [
            (tank_details_df['current_qty_m3'] * tank_details_df['Density']) if x < 1 else (
                    tank_details_df['current_qty_m3'] * (tank_details_df['Density'] / 1000)) for x in
            tank_details_df['Density']]
        tank_details_df['current_qty_MT'] = np.where(tank_details_df['Unit'] == 'MT', tank_details_df['Current_QTY'],
                                                     tank_details_df['convert_m3_MT'])

        update_current_qty_m3 = tank_details_df['current_qty_m3'].sum()
        update_current_qty_MT = tank_details_df['current_qty_MT'].sum()
        print(len(tank_details_df['current_qty_MT']), 'tank_details_df++++++')

        up_current_tank_LD_qty_m3 = float(pb_update_current_qty_m3) + float(update_current_qty_m3)
        up_current_tank_LD_qty_mt = float(pb_update_current_qty_MT) + float(update_current_qty_MT)
        update_remaining_space_m3 = float(safe_fill_capacity) - float(up_current_tank_LD_qty_m3)

        TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
            Terminal__name=terminal).update(Qty_add_discharge=up_current_tank_LD_qty_m3,
                                            Cargo=cargo, Density=Density, current_quantity=up_current_tank_LD_qty_mt,
                                            Remaining_space=update_remaining_space_m3)

        if float(up_current_tank_LD_qty_mt) <= 0:
            TankCapacityM.objects.filter(Tank_no__name=tank_number).filter(Port__name=port).filter(
                Terminal__name=terminal).update(Cargo='EMPTY', Density=0.0)

        print("updated")


    def post(self, request, *args, **kwargs):
        print(" post methode:")
        date = request.POST.get('date', '')
        print("date:", date)
        tradeid = request.POST.get('tradeid', '')
        print("tradeid:", tradeid)
        trader = request.POST.get('trader', '')  # id
        print("trader:", trader)
        book = request.POST.get('book', '')  # id
        print("book:", book)
        company_name = request.POST.get('company_name', '')
        print("company_name:", company_name)
        strategy = request.POST.get('strategy', '')
        print("strategy:", strategy)
        derivatives = request.POST.get('derivatives', '')
        print("derivatives:", derivatives)
        # buysell = request.POST.get('buysell', '')
        cargo = request.POST.get('cargo', '')
        print("cargo:", cargo)
        pricing_contract = request.POST.get('pricing_contract', '')
        print("pricing_contract:", pricing_contract)
        pricing_methode = request.POST.get('pricing_methode', '')  # id
        print("pricing_methode:", pricing_methode)
        volume = request.POST.get('quantity', '')
        print("volume:", volume)

        unit = request.POST.get('unit', '')
        print("Unit", unit)
        density = request.POST.get('density', '')
        print("density:", density)
        nominated_quantity = request.POST.get('nominated_quantity', '')
        print("nominated_quantity:", nominated_quantity)
        premium_discount = request.POST.get('premium_discount', '')
        print("premium_discount:", premium_discount)
        pricing_term = request.POST.get('pricing_term', '')
        bl_date = request.POST.get('bl_date', '')
        print("BL date:", bl_date)
        start_date = request.POST.get('start_date', '')
        print("start_date:", start_date)
        end_date = request.POST.get('end_date', '')
        print("end_date:", end_date)
        holiday = request.POST.get('holiday', '')
        print("holiday get:", holiday)
        deliverymode = request.POST.get('deliverymode', '')
        port = request.POST.get('port', '')
        print("port:", port)
        terminal = request.POST.get('terminal', '')
        vessal_name = request.POST.get('vessal_name', '')
        tank = request.POST.get('tank', '')
        print("Tank", tank)
        external_terminal = request.POST.get('external_terminal', '')
        hedging = request.POST.get('hedging', '')
        Remarks = request.POST.get('Remarks', '')

        delete_feild = request.POST.get('delete_feild')
        if delete_feild:
            obj = PhysicalBlotterModel.objects.get(id=delete_feild)
            obj.delete()
            return HttpResponseRedirect("/inventory-list/")

        # # update status in admin side :
        # admin_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        # current_admin_status = admin_status.Status
        # print("current status:", current_admin_status)
        #
        # update_status_in_admin = GenerateTradeModel.objects.get(id=kwargs['id'])
        # update_status_in_admin.Status = "Process"
        # update_status_in_admin.save()

        # print("after updating status:", update_status_in_admin.Status)
        #
        # Purchase/salesID
        volume = int(volume)
        volume = -abs(volume)
        print("negative volume:", volume)

        if volume >= 0:
            print("Buying")
            print("cargo buying:", cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "P" + "-" + cargo + "-" + randint_
            print("purchase_id buying:", purchase_id)
            buysell = "Buy"
        elif volume <= 0:
            print("selling")
            print("cargo selling:", cargo)
            cargo = str(cargo)
            randint_ = str(random.randint(1000, 99999))
            purchase_id = "S" + "-" + cargo + "-" + randint_
            print("purchase_id selling:", purchase_id)
            buysell = "Sell"
        else:
            pass
        #
        print("************* Coversion from string to particular type")

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        print("converted start_date:", start_date)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        print("converted end_date:", end_date)

        date_ = datetime.strptime(date, '%Y-%m-%d').date()
        print("converted date_:", date_)

        bl_date = datetime.strptime(bl_date, '%Y-%m-%d').date()
        print("converted bl_date:", bl_date)
        print('****************************************')

        # HOLIDAY DATE LIST OF SELECTED HOLIDAY in DATAFRAME

        #   the working holiday list dates  using data frame
        print("Finding holiday:")
        print("Holioday selected", holiday)
        holiday_list_of_selected_holi = HolidayM.objects.filter(name__icontains=holiday).values_list("date")
        # workingdays
        holi_list_selcted = []
        for i in holiday_list_of_selected_holi:
            holi_list_selcted.append(i)
        print("new list of selected holi:", holi_list_selcted)

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holiday_list = holiday_date_df['Dates'].to_list()
        print(holi_list_selcted, 'first++++++++total_swap_days')

        holiday_date_df = pd.DataFrame(holi_list_selcted, columns=['Dates'])
        holiday_date_df['Dates'] = pd.to_datetime(holiday_date_df["Dates"]).dt.date
        holi_list_selcted = holiday_date_df['Dates'].to_list()
        print(holiday_list, 'first++++++++total_swap_days')

        total_working_days = len(pd.bdate_range(start_date, end_date, freq="C", holidays=holi_list_selcted))
        print(total_working_days, '++++++++total_swap_days')

        # <!----- priced and unpriced days start ----!>

        print("Priced unpriced starting")

        if date_ <= start_date:
            print("first condition priced days")
            priced_days = 0
            # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            unprice_calcu = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            unpriced_days = len(unprice_calcu)
            print("Priced days:", priced_days)
            print("Unpriced Days:", unpriced_days)
            print("first Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
            print("ending of 2nd condition price days")
        # ---------------------------------------------------------------------------
        elif (date_ > start_date) and (date_ <= end_date):
            print("2nd pricing days condition")
            unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=holi_list_selcted))

            workday = len(pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted))
            priced_days = workday - unpriced_days
            # instance = form.save(commit=False)
            # instance.price_days = priced_days
            # instance.unprice_days = unpriced_days
            # instance.save()
            print("second Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')
        #
        elif (date_ > end_date):
            print("Hi 3rd priced days CONDITION")
            unpriced_days = 0
            # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=holi_list_selcted)
            print(priced_days)
            priced_days = len(priced_days)

            print("priced days:", priced_days)
            print("Unpriced days:", unpriced_days)

            print("Third Priced/unpriced days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

        else:
            pass

        print("Priced unpriced end")
        # <!----- priced unpriced end ---!>

        # # <!-----priced volume ----!>

        print("Priced volume begining")

        pricing_methode = str(pricing_methode)
        unit = str(unit)

        if pricing_methode == "Fixed":
            print('hi')
            print("startdate:", start_date)
            print("enddate:", end_date)

            if start_date == end_date:
                total_volume = volume
                total_volume = round(volume, 3)
                print("totalk volume:", total_volume)
                priced_volume = total_volume
                unpriced_volume = 0
                # instance = form.save(commit=False)
                # instance.total_volume = total_volume
                # # instance.position = total_volume
                # instance.price_volume = priced_volume
                # instance.unprice_volume = unpriced_volume
                # instance.save()
                print('+++++++++++++++++++++++++++++++++++++++++')
            else:
                pass
        elif pricing_methode == "Float":
            total_volume = volume
            priced_volume = (total_volume / total_working_days) * priced_days
            priced_volume = round(priced_volume, 3)
            print("priced volume:", priced_volume)
            unpriced_volume = (total_volume / total_working_days) * unpriced_days
            unpriced_volume = round(unpriced_volume, 3)
            print("unpriced_volume", unpriced_volume)
            # instance = form.save(commit=False)
            # instance.total_volume = total_volume
            # # instance.position = total_volume
            # instance.price_volume = priced_volume
            # instance.unprice_volume = unpriced_volume
            # instance.save()
            print('+++++++++++++++++++++++++++++++++++++++++')

        # ######## status change ###############
        status = "Open"
        status = str(status)
        print("status converted to open:", status)

        shore_recieved = 0

        # generate_status = GenerateTradeModel.objects.get(id=kwargs['id'])
        # print("hai", generate_status.Status)
        # print("testing")

        print("total volume b4:", total_volume)
        #
        print("object creation for pb")
        obj = PhysicalBlotterModel(Date=date, Trader=trader, Book=book, Company_name=company_name,
                                   Strategy=strategy, Derivative=derivatives,
                                   Trade_id=tradeid, Buy_sell=buysell,
                                   Cargo=cargo,
                                   Pricing_contract_id=pricing_contract, Pricing_method=pricing_methode,
                                   Quantity=volume, Unit=unit,
                                   Density=density, Nominated_quantity=nominated_quantity,
                                   Premium_discount=premium_discount, Pricing_term=premium_discount,

                                   bl_date=bl_date, start_date=start_date, end_date=end_date,
                                   Holiday=holiday,
                                   Total_no_days=total_working_days, Delivery_mode=deliverymode,
                                   Port=port, Terminal=terminal,
                                   Vessal_name=vessal_name, Tank=tank, Remarks=Remarks,
                                   External_Terminal=external_terminal, Headging=hedging,
                                   #                            # calculated and_ get_values
                                   Purchase_sales_ID=purchase_id, status=status,
                                   price_days=priced_days, unprice_days=unpriced_days,
                                   total_volume=total_volume, price_volume=priced_volume,
                                   unprice_volume=unpriced_volume, Shore_recieved=shore_recieved
                                   )
        obj.save()




        source_list=[tank,port,terminal]
        tank_updation_list = []

        if deliverymode=='Tank':


            tank_updation_list.append(source_list)
            self.tank_update(request, tank_updation_list, cargo, density)


        print(" saved Inventory Sale")
        messages.info(request, 'Discharge Sale Saved')
        return HttpResponseRedirect('/pb-list/')



# CHARTS JS

def charts(request):
    chart="hi chart"
    tankcapacity = TankCapacityM.objects.all()

    context={
        "chart":chart,
        "tank_capacity":tankcapacity,
    }

    return render(request,"customer/chart.html",context)


def copydata(request):
    return render(request,"customer/copy-data.html")


## DEAL STATUS

class DealStatus(View):
    def get(self,request,*args,**kwargs):
        open_pb = PhysicalBlotterModel.objects.filter(status="Open").order_by('-Date')
        closed_pb = PhysicalBlotterModel.objects.filter(status="Closed").order_by('-Date')
        print("physicalblotters open:",open_pb)
        print("physicalblotters closed:", closed_pb)
        update_pb_database(request)

        context ={

                  "open_pb":open_pb,
                   "closed_pb":closed_pb,


        }

        return render(request,"customer/deals_status.html",context)



###  Physical Trade History


######### Physical History ###############

def Physical_tradehistory(request):
    swap_date_list = []
    swap_Book_list = []
    swap_Trader_list = []
    swap_Company_name_list =[]

    swap_tradeid_list = []
    swap_cargo_list =[]
    swap_Pricing_contract_list =[]

    swap_Pricing_method_list=[]
    swap_Unit_list=[]
    swap_Density_list=[]
    swap_Nominated_quantity =[]
    swap_Premium_discount_list=[]
    swap_Pricing_term_list=[]
    swap_bl_date_list=[]
    swap_start_date_list = []
    swap_end_date_list = []
    swap_Delivery_mode_list=[]
    swap_Port_list=[]
    swap_Terminal_list =[]
    swap_Tank_list=[]
    swap_Purchase_sales_ID_list=[]

    swap_status_list =[]
    swap_Customer_Company_list = []
    swap_Strategy_list = []
    swap_Derivative_list = []
    swap_Volume_list = []
    swap_Vessal_name_list = []
    swap_Tank_list=[]
    swap_Holiday_list = []
    swap_Total_no_days_list = []

    for obj in PhysicalBlotterModel.objects.all():
        print("hi forloop")
        # print("3 datas :", obj.id, obj.Contract_Name, obj.end_date, obj.unprice_volume)
        swap_date_list.append(obj.Date)
        print("swap_date_list",swap_date_list)
        swap_Trader_list.append(obj.Trader)
        print("swap_Trader_list", swap_Trader_list)
        swap_Book_list.append(obj.Book)
        print("swap_Book_list", swap_Book_list)
        swap_Company_name_list.append(obj.Company_name)
        print("swap_Company_name_list", swap_Company_name_list)
        swap_Strategy_list.append(obj.Strategy)
        print("swap_Strategy_list", swap_Strategy_list)
        swap_Derivative_list.append(obj.Derivative)
        print("swap_Derivative_list", swap_Derivative_list)
        swap_tradeid_list.append(obj.Trade_id)
        print("swap_tradeid_list", swap_tradeid_list)
        swap_cargo_list.append(obj.Cargo)
        print("swap_cargo_list", swap_cargo_list)
        swap_Pricing_contract_list.append(obj.Pricing_contract)
        print("swap_Pricing_contract_list", swap_Pricing_contract_list)
        swap_Pricing_method_list.append(obj.Pricing_method)
        print("swap_Pricing_method_list", swap_Pricing_method_list)
        swap_Volume_list.append(obj.Quantity)
        print("swap_Volume_list", swap_Volume_list)
        swap_Unit_list.append(obj.Unit)
        print("swap_Unit_list", swap_Unit_list)
        swap_Density_list.append(obj.Density)
        print("swap_Density_list", swap_Density_list)
        swap_Nominated_quantity.append(obj.Nominated_quantity)
        print("swap_Nominated_quantity", swap_Nominated_quantity)
        swap_Premium_discount_list.append(obj.Premium_discount)
        print("swap_Premium_discount_list", swap_Premium_discount_list)
        swap_Pricing_term_list.append(obj.Pricing_term)
        print("swap_Pricing_term_list", swap_Pricing_term_list)
        swap_bl_date_list.append(obj.bl_date)
        print("swap_bl_date_list", swap_bl_date_list)
        swap_start_date_list.append(obj.start_date)
        print("swap_start_date_list", swap_start_date_list)
        swap_end_date_list.append(obj.end_date)
        print("swap_end_date_list", swap_end_date_list)
        swap_Holiday_list.append(obj.Holiday)
        print("swap_Holiday_list", swap_Holiday_list)
        swap_Total_no_days_list.append(obj.Total_no_days)
        print("swap_Total_no_days_list", swap_Total_no_days_list)
        swap_Delivery_mode_list.append(obj.Delivery_mode)
        print("swap_Delivery_mode_list", swap_Delivery_mode_list)
        swap_Port_list.append(obj.Port)
        print("swap_Port_list", swap_Port_list)
        swap_Terminal_list.append(obj.Terminal)
        print("swap_Terminal_list", swap_Terminal_list)
        swap_Vessal_name_list.append(obj.Vessal_name)
        print("swap_Vessal_name_list", swap_Vessal_name_list)
        swap_Tank_list.append(obj.Tank)
        print("swap_Tank_list", swap_Tank_list)
        swap_Purchase_sales_ID_list.append(obj.Purchase_sales_ID)
        print("swap_Purchase_sales_ID_list", swap_Purchase_sales_ID_list)
        swap_status_list.append(obj.status)
        print("swap_status_list", swap_status_list)
        print("endforloop")

    print("converting to df")

    pb_history_df = pd.DataFrame(
        {"Date": swap_date_list,"Trade ID":swap_tradeid_list, "Trader": swap_Trader_list,"Book": swap_Book_list,
         "Company Name": swap_Company_name_list, "Strategy": swap_Strategy_list, "Cargo": swap_cargo_list,
         "Pricing Contract": swap_Pricing_contract_list, "Pricing Methode": swap_Pricing_method_list,
         "Derivative": swap_Derivative_list,
         "Quantity": swap_Volume_list, "Unit": swap_Unit_list, "Density": swap_Density_list,
         "Nominated Quantity": swap_Nominated_quantity,
         "Start Date ": swap_start_date_list, "End Date": swap_end_date_list, "Holiday": swap_Holiday_list,
         "Total No Days": swap_Total_no_days_list, "Delivery Mode": swap_Delivery_mode_list,
         "Port": swap_Port_list, "Terminal": swap_Terminal_list,
         "Vessal Name": swap_Vessal_name_list, "Tank": swap_Tank_list,
         "Purchase/Sales ID": swap_Purchase_sales_ID_list, "Status": swap_status_list,
         })

    print("new pb history df :",pb_history_df)

    print("end of pb ")
    return (pb_history_df)

    # context = {
    #     'pb_history_df': pb_history_df,
    # }
    # return render(request,"customer/pb-trade-hist.html",context)



def Checkhistory(request):
    return render(request,"customer/trade-history.html")



class InventoryData(View):

    def get(self, request, *args, **kwargs):

        cargo = []
        cqty = []
        port=[]
        tankno =[]

        # tabk = TankCapacityM.objects.values('Cargo', 'current_quantity')
        tankcapacity = TankCapacityM.objects.all()

        for j in TankCapacityM.objects.all():
            print("j", j.Cargo)
            # if (j.current_quantity>0):
            print("newj", j)
            cargo.append(j.Cargo)
            print("tank no", j.Tank_no)
            cqty.append(j.current_quantity)
            tankno.append(j.Tank_no)

        cargo_tank = [str(i) +'-'+ j for i, j in zip(tankno, cargo)]
        for p in TankCapacityM.objects.all():

            if p.Port not in port:
                port.append(p.Port)
        print("port",port)

        print("cargo:",cargo)
        print("current_qty",cqty)

        context = {

            "cargo":cargo,
            "cqty":cqty,

            "tankno":tankno,
            'port':port,
            'tankcapacity':tankcapacity,
            'cargo_tank':cargo_tank,

        }
        # return render(request, "customer/inventory-dash-visual.html",context)

        return render(request, "customer/inv-dash.html", context)

    def post(self, request, *args, **kwargs):
        print(" post methode:")
        port = request.POST.get('port', '')
        print("port:",port)
        terminal = request.POST.get('terminal', '')
        print("terminal:",terminal)

        filter_cargo=[]
        filter_qty =[]
        filter_tankno=[]

        if port:
            if terminal:
                print("hai p t")

                p_t_filter=TankCapacityM.objects.filter(Q(Port__name=port) & Q(Terminal__name=terminal))

                for i in p_t_filter:
                    print("pt i", i)
                    # if (i.current_quantity > 0):
                    print("newj", i)
                    filter_cargo.append(i.Cargo)
                    filter_qty.append(i.current_quantity)
                    filter_tankno.append(i.Tank_no)

                    print("filter_cargo",filter_cargo)
                    print("filter_qty", filter_qty)

                    filter_cargo_tank = [str(i) + '-' + j for i, j in zip(filter_tankno, filter_cargo)]


                    return render(request, "customer/inv-dash.html",
                                  {"cargo": filter_cargo, "cqty": filter_qty,
                                   "tankcapacity":p_t_filter,"cargo_tank":filter_cargo_tank,})

                # print("filter_cargo:",filter_cargo)
                # print("filter_qty:", filter_qty)
                #
                # context = {
                #
                #     "cargo": filter_cargo,
                #     "cqty": filter_qty,
                #
                # }
                #
                # print("the end")


        # return render(request, "customer/inventory-dash-visual.html", context)

        return HttpResponseRedirect("/inventory_data")

####### INVENTORY DASH TYPE 2:


def invdash(request):
    print(" hello tanc")

    cargo = []
    cqty = []
    port = []

    for j in TankCapacityM.objects.all():
        print("j", j.Cargo)
        if (j.current_quantity > 0):
            print("newj", j)
            cargo.append(j.Cargo)
            cqty.append(j.current_quantity)
        else:
            pass

    for p in TankCapacityM.objects.all():

        if p.Port not in port:
            port.append(p.Port)

    print("port", port)

    print("cargo:", cargo)
    print("current_qty", cqty)

    if request.method == 'POST':

        print(" post methode:")
        port = request.POST.get('port', '')
        print("port:", port)
        terminal = request.POST.get('terminal', '')
        print("terminal:", terminal)

        filter_cargo = []
        filter_qty = []

        if port:
            if terminal:
                print("hai p t")

                p_t_filter = TankCapacityM.objects.filter(Q(Port__name=port) & Q(Terminal__name=terminal))

                for i in p_t_filter:
                    print("pt i", i)
                    if (i.current_quantity > 0):
                        print("newj", i)
                        filter_cargo.append(i.Cargo)
                        filter_qty.append(i.current_quantity)
                        return render(request, "customer/inventory-dash-visual.html",
                                      {"cargo": filter_cargo, "cqty": filter_qty})
                    else:
                        pass

        # form = ProductForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('index')
    else:

        return HttpResponseRedirect("/inventory_data")
        # form = ProductForm()

    context = {
         "cargo":cargo,
            "cqty":cqty,
            'port':port,
    }

    return render(request, 'customer/inventory-dash-visual.html', context)




def pie_chart(request):
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    data = [12, 19, 3, 5, 2, 3]
    context = {'labels': json.dumps(labels), 'data': json.dumps(data)}
    return render(request, 'customer/pie_chart.html', context)

def bar_chart(request):
    # Query the data for the chart
    data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        'data': [12, 19, 3, 5, 2, 3, 14]
    }
    return JsonResponse(data)


















#### INVEMTPRY DASH TYPE 2 END

def port_terminal_chart_relation(request):
    print("Hi Port")
    if request.method == "POST":
        print("Hello Post methode")
        request_data = request.body.decode('utf-8')
        data_dict = json.loads(request_data)
        port_name = data_dict.get('port_name')
        print("Port name:",port_name)
        obj = TankCapacityM.objects.filter(Port__name=port_name)
        print("obj:",obj)
        for data in obj:
            print("checking:",data.product_status)
            print("checking:", data.Terminal.name)
            print("checking:", data.Tank_no.name)

        data = [{'date': data.Terminal.name} for data in obj]
        data1 = [{'data': i.Tank_no.name} for i in obj]

        print("data:",data)
        uniq_data = []
        for x in data:
            if x not in uniq_data:
                uniq_data.append(x)
        print("uniq data:", uniq_data)
        print("data1:", data1)
        uniq_data1 = []
        for x in data1:
            if x not in uniq_data1:
                uniq_data1.append(x)
        print("uniq data1:", uniq_data1)

        print(data1)
        print('ddd')
    return JsonResponse({'data':uniq_data, 'data1':uniq_data1}, safe=False)




##############   FUTURE LTD ####################

def futureltd(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        try:
            if reader:
                for row in reader:
                    FutureLTD.objects.create(
                        Contract_symbol=row['Contract Symbol'],
                        Ls_gas_oil=row['Ls Gas Oil'],
                        Brent_crude_futures=row['Brent Crude Futures'],
                        RBOB_Gasoline_futures=row['RBOB Gasoline Futures'],
                        Heating_oil_futures=row['Heating Oil Futures'],
                        WTI_crude_futures=row['WTI Crude Futures'],
                    )
                messages.info(request, f"Added Trader")
            else:
                messages.error(request, "There are no values in file")
        except:
            messages.info(request, "Error ❌ Column Book not Found")

        return HttpResponseRedirect("/futureltd")
    return render(request, 'customer/future_ltd.html')


     ## KARTHIK'S CODE

           # try:
           #      df = pd.read_csv(file,usecols=['Book'or'book' ])
           #      print(df)
           #      if len(df)>0:
           #          for i,name in df.iterrows():
           #              obj = self.model.objects.create(name=name['Book'or'book'])
           #              obj.save()
           #          messages.info(request,f"Added {len(df)} Trader")
           #      else:
           #          messages.error(request, "There are no values in file")
           #  except:
           #      messages.info(request, "Error ❌ Column Book not Found")






class FutureLTDView(View):
    def get(self, request, *args, **kwargs):

        qs = FutureLTD.objects.all()
        print("qs",qs)

        return render(request, "customer/future_ltd.html",{"object_list":qs})

    def post(self, request, *args, **kwargs):
        print(" post methode:")
        file = request.FILES.get('file')
        print("file:",file)

        # try:
        df = pd.read_csv(file, usecols=['Contract_symbol',
                                         'Ls_gas_oil',
                                         'Brent_crude_futures',
                                         'RBOB_Gasoline_futures',
                                         'Heating_oil_futures',
                                          'WTI_crude_futures',

                                        ])

        #
        # df['Contract_symbol'] = df['Contract_symbol'].astype('string')
        # df['Ls_gas_oil'] = df['Ls_gas_oil'].astype('string')
        # df['Brent_crude_futures'] = df['Brent_crude_futures'].astype('string')
        # df['RBOB_Gasoline_futures'] = df['RBOB_Gasoline_futures'].astype('string')
        # df['Heating_oil_futures'] = df['Heating_oil_futures'].astype('string')
        # df['WTI_crude_futures'] = df['WTI_crude_futures'].astype('string')

        df['Contract_symbol'] = pd.to_datetime(df.Contract_symbol)
        df['Ls_gas_oil'] = pd.to_datetime(df.Ls_gas_oil)
        df['Brent_crude_futures'] = pd.to_datetime(df.Brent_crude_futures)
        df['RBOB_Gasoline_futures'] = pd.to_datetime(df.RBOB_Gasoline_futures)
        df['Heating_oil_futures'] = pd.to_datetime(df.Heating_oil_futures)
        df['WTI_crude_futures'] = pd.to_datetime(df.WTI_crude_futures)

        df['Contract_symbol'] = df['Contract_symbol'].dt.strftime('%Y-%m-%d')
        df['Ls_gas_oil'] = df['Ls_gas_oil'].dt.strftime('%Y-%m-%d')
        df['Brent_crude_futures'] = df['Brent_crude_futures'].dt.strftime('%Y-%m-%d')
        df['RBOB_Gasoline_futures'] = df['RBOB_Gasoline_futures'].dt.strftime('%Y-%m-%d')
        df['Heating_oil_futures'] = df['Heating_oil_futures'].dt.strftime('%Y-%m-%d')
        df['WTI_crude_futures'] = df['WTI_crude_futures'].dt.strftime('%Y-%m-%d')
        print(df)

        check_nan_in_df = df.isnull().values.any()
        if check_nan_in_df==False:
            print('no null values')
        else:
            print('null exist')
            messages.info(request, "Error ❌ Null values exist in file ")
            return HttpResponseRedirect('/futureltd2')


        print("Type:", type(df['Contract_symbol']))
        print("df", df)
        if len(df) > 0:
            for i, Contract_symbol in df.iterrows():
                print(i,"printi")
                print("Contract_symbol",Contract_symbol)
                obj = FutureLTD.objects.update_or_create(
                    Contract_symbol=Contract_symbol['Contract_symbol'],
                    Ls_gas_oil=Contract_symbol['Ls_gas_oil'],
                    Brent_crude_futures=Contract_symbol['Brent_crude_futures'],
                    RBOB_Gasoline_futures=Contract_symbol['RBOB_Gasoline_futures'],
                    Heating_oil_futures=Contract_symbol['Heating_oil_futures'],
                    WTI_crude_futures=Contract_symbol['WTI_crude_futures'],
                    )
                obj.save()
                messages.info(request, f"Added {len(df)} Trader")
        else:
            messages.error(request, "There are no values in file")
    # except:
        #
        #     messages.info(request, "Error ❌ Column not Found")
        return HttpResponseRedirect("/futureltd2")




        # reader = csv.DictReader(file)
        # for row in reader:
        #     # Check if all required fields are present in the CSV row
        #     if 'Contract Symbol' not in row or 'Ls Gas Oil' not in row or 'Brent Crude Futures' or 'RBOB Gasoline Futures' or 'Heating Oil Futures' or 'WTI Crude Futures' not in row:
        #         print('Error: Required field(s) missing in CSV row')
        #         continue
        #
        #     # Create an instance of the model and set the fields from the CSV row
        #     obj = FutureLTD()
        #     obj.Contract_symbol = row['Contract Symbol']
        #     obj.Ls_gas_oil = row['Ls Gas Oil']
        #     obj.Brent_crude_futures = row['Brent Crude Futures']
        #     obj.RBOB_Gasoline_futures = row['RBOB Gasoline Futures']
        #     obj.Heating_oil_futures = row['Heating Oil Futures']
        #     obj.WTI_crude_futures = row['WTI Crude Futures']
        #
        #     # Set any additional fields if they are present in the CSV row
        #
        #     # Save the object to the database
        #     obj.save()
        #
        #
        # return HttpResponseRedirect("/futureltd2")


# views.py
def bar_chart2(request):
    # Data
    data = {
        'apples': 10,
        'oranges': 15,
        'pears': 5,
        'bananas': 20,
    }

    # Plot
    fig = plt.figure(figsize=(10,5))
    plt.bar(data.keys(), data.values(), color='green')
    plt.title('Fruit Count')
    plt.xlabel('Fruit')
    plt.ylabel('Count')
    plt.grid(True)

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Add legend
    legend = plt.legend(['Count'], loc='upper right')

    # Pass plot and legend to template
    return render(request, 'customer/bar_chart.html', {'graphic': graphic, 'legend': legend})



def display_csv(request):
    df = pd.read_csv('plattes_prices.csv')
    print("plattes_prices",df)

    df = df[(df['DATE'] =='09/01/2018' )]
    
    print("ddf",df)

    # if request.method == 'POST':
    #     C:\Users\pkanu\Downloads\accer(17)\accer(14)\accer\accer
    #     csv_file = request.FILES['csv_file']
    #     print("csvfile",csv_file)
    #     csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
    #     context = {'csv_data': csv_data}
    #     return render(request, 'customer/display_csv.html', context)
    # else:
    #     return render(request, 'customer/upload_csv.html')




class PricingView(View):
    def get(self, request, *args, **kwargs):

        plattes_prices_df = pd.read_csv('plattes_prices.csv')
        Futures_pricing_df =  pd.read_csv('Futures_pricing.csv')

        plattes_prices_df['DATE'] = pd.to_datetime(plattes_prices_df['DATE'])
        print("info",plattes_prices_df['DATE'].isna().sum())


        plattes_prices_df.sort_values(by='DATE', ascending=True, inplace=True)
        print("sort plattes_prices_df:", plattes_prices_df)

        plattes_prices_df['DATE'] = plattes_prices_df['DATE'].dt.strftime('%d-%b-%y')

        print("new",plattes_prices_df)
        plattes_prices_df= plattes_prices_df.tail()

        # plattes_prices_df['Sort_column'] = pd.to_datetime(plattes_prices_df['DATE'])
        # plattes_prices_df.sort_values(by='Sort_column', inplace=True)
        # print("sotrcol:",plattes_prices_df)

        this_month_price = thismonthprice(request)
        this_month_holiday = thismonthholiday(request)

        print("this_month_price",this_month_price)



        #### FUTURES PRICING PLATT
        Futures_pricing_df['Contract Month'] = pd.to_datetime(Futures_pricing_df['Contract Month'])
        Futures_pricing_df['Contract Month'] = Futures_pricing_df['Contract Month'].dt.strftime('%d-%b-%y')

        context = {
            "plattes_prices_df": plattes_prices_df,
            'Futures_pricing_df':Futures_pricing_df,
            'this_month_price':this_month_price,
            'this_month_holiday':this_month_holiday,
        }
        return render(request, "customer/pricing.html",context)

    def post(self, request, *args, **kwargs):
        print("pricing post")
        plattes_prices_df = pd.read_csv('plattes_prices.csv')
        # plattes_prices_df['DATE'] = plattes_prices_df['DATE'].dt.strftime('%Y/%m/%d')

        plattes_prices_df['DATE'] = pd.to_datetime(plattes_prices_df['DATE'])
        # plattes_prices_df['DATE'] = plattes_prices_df['DATE'].dt.strftime('%d-%b-%y')

        print("plattes_prices_df:",plattes_prices_df)

        date = request.POST.get('date', '')
        print("date:",date)

        plattes_prices_df = plattes_prices_df[(plattes_prices_df['DATE'] == date)]
        print("plattes_prices_df:",plattes_prices_df)


        # # change in date time format
        # date = pd.to_datetime(pd.Series("date"))
        # date = date.dt.strftime('%d-%m-%Y')


        # 1999-10-25 ------>25-10-1999

        # date = date.dt.strftime('%d-%m-%y')
        print("new date:",date)

    #
    #         messages.info(request, "Error ❌ Column Book not Found")
        return HttpResponseRedirect("/pricing")

class HistoricalSettelment(View):
    def get(self, request, *args, **kwargs):

        settlement_prices_df = pd.read_csv('settlement_prices.csv')

        # settlement_prices_df['DATE'] = pd.to_datetime(settlement_prices_df['DATE'])
        # print("info",settlement_prices_df['DATE'].isna().sum())
        #
        #
        # settlement_prices_df.sort_values(by='DATE', ascending=True, inplace=True)
        # print("sort plattes_prices_df:", settlement_prices_df)
        #
        # settlement_prices_df['DATE'] = settlement_prices_df['DATE'].dt.strftime('%d-%b-%y')

        print("new",settlement_prices_df)
        settlement_prices_df= settlement_prices_df.tail()

        # plattes_prices_df['Sort_column'] = pd.to_datetime(plattes_prices_df['DATE'])
        # plattes_prices_df.sort_values(by='Sort_column', inplace=True)
        # print("sotrcol:",plattes_prices_df)

        context = {
            "settlement_prices_df": settlement_prices_df,
        }
        return render(request, "customer/historicalsettlement.html",context)




def customerindex(request):
    return render(request,"customer/index-customer.html")

def invdash2(request):
    return render(request,"customer/inv-dash.html")

def neeew(request):
    return render(request,"customer/inv-dash.html")


def filtertable(request):
    return render(request,"customer/filtertable.html")

### last day of month


from datetime import datetime, timedelta
from django.shortcuts import render


def last_date_of_month(request):
    if request.method == 'POST':
        # Retrieve the date entered by the user
        date_string = request.POST.get('date')

        try:
            # Convert the user input to a datetime object
            date = datetime.strptime(date_string, '%Y-%m-%d').date()

            # Calculate the last day of the month
            year = date.year
            month = date.month
            _, last_day = calendar.monthrange(year, month)
            last_date = datetime(year, month, last_day).date()

            return render(request, 'customer/result.html', {'last_date': last_date})

        except ValueError:
            error_message = 'Invalid date format. Please enter a date in the format YYYY-MM-DD.'
            return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'customer/input.html')


# *********************************************** INITIAL MARGIN ***************************************************************************************
# import subprocess
# import os
# def initialmargin(request):
#     # Specify the path to your batch file
#
#     batch_file_path = 'D:/PAPER TRADING FINAL/accer/initialmargin/marbats.bat'
#     try:
#         # Open the batch file using the subprocess module
#         subprocess.Popen(batch_file_path, shell=True)
#         return HttpResponse("Batch file opened successfully!")
#     except Exception as e:
#         return HttpResponse(f"Error opening batch file: {str(e)}")



    # subprocess.call([r'D:\PAPER TRADING FINAL\accer\initialmargin\marbats.bat'])
    #
    # if os.path.isfile('D:\PAPER TRADING FINAL\accer\initialmargin/results.csv'):
    #
    #     print("hello intial")
    #     pass




