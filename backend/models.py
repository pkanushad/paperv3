from django.db import models
from django.contrib.auth.models import AbstractUser
from django_softdelete.models import SoftDeleteModel
from datetime import datetime
import uuid
# Create your models here.


class CustomUser(AbstractUser):
    user_type_data = (
        (0,'admin'),
        (1,'user')
    )
    user_type=models.CharField(max_length=100, choices=user_type_data, default=0)



    

class Traders(SoftDeleteModel):
    name = models.TextField()

    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        

class Book(SoftDeleteModel):
    name = models.TextField()

    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        
class Product(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        

class Strategy(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)


class DerivativeM(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        

class Type(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        
class Unit1(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)


class BrokerM(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)


class ClearearM(SoftDeleteModel):
    name = models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return str(self.name)
        

class ContractM(SoftDeleteModel):
    derivative=models.CharField(max_length=100, null=True)
    single_dif = models.CharField(max_length=100, null=True)
    major_mini = models.CharField(max_length=100, null=True,blank=True)
    contract_name = models.TextField(null=True)
    contract1 = models.TextField(null=True)
    contract2 = models.TextField(null=True)
    major_mini_conn =  models.TextField(null=True,blank=True)
    unit =  models.TextField(null=True)
    tick =  models.TextField(null=True)
    holiday =  models.TextField(null=True)
    bbi_mt_conversion = models.TextField(null=True)
    f_w_months =  models.TextField(null=True)
    exchange_fee =  models.TextField(null=True,blank=True)
    exchanging_clearing_fee =  models.TextField(null=True, blank=True)
    block_fee =  models.TextField(null=True,blank=True)
    screen_fee =  models.TextField(null=True,blank=True)
    gmifc_code =  models.TextField(null=True)
    physical_code =  models.TextField(null=True)
    logical_code =  models.TextField(null=True)
    symbol_code =  models.TextField(null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.contract_name)
    

class HolidayM(models.Model):
    name = models.CharField(max_length=1000)
    date = models.DateField()
    
    class Meta:
        ordering=['-id']

    def __str__(self):
        return str(self.name)
    

class ClearerRateM(SoftDeleteModel):
    clearer = models.ForeignKey(ClearearM, on_delete=models.CASCADE)
    derivative = models.CharField(max_length=1000)
    contract = models.ForeignKey(ContractM, on_delete=models.CASCADE)
    clearer_house_fee = models.CharField(max_length=2000)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.derivative)

    

class BrockerageM(SoftDeleteModel):
    contract_name = models.ForeignKey(ContractM, on_delete=models.CASCADE)
    brocker = models.ForeignKey(BrokerM, on_delete=models.CASCADE)
    apply_mode = models.CharField(max_length=200)
    brockerage = models.CharField(max_length=100)
    derivatives=models.CharField(max_length=100)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.contract_name.contract_name
      
    
    
class CargoM(SoftDeleteModel):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)


class CounterpartyM(SoftDeleteModel):
    created_date = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=1000)
    trader_license_number = models.CharField(max_length=2000)
    email = models.CharField(max_length=10000)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.company_name)


class PortM(SoftDeleteModel):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)


class TerminalM(SoftDeleteModel):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)


class TankNumberM(SoftDeleteModel):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)

class TankTypeM(SoftDeleteModel):
    name = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)


class GenerateTradeModel(models.Model):
    Trade_id = models.CharField(max_length=10000, unique=True)
    Company_name = models.ForeignKey(CounterpartyM, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Cargo = models.ForeignKey(CargoM, on_delete=models.CASCADE)
    Status = models.CharField(max_length=100, null=True, blank=True, default='New')
    Strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    Unit = models.ForeignKey(Unit1,on_delete = models.CASCADE,null=True,blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deal_current_qty = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.Trade_id:
            while True:
                trader_id = str(self.Company_name.company_name[:4])+"-"+str(self.Company_name.trader_license_number[:4])+"-"+str(self.Book.name)+"-"+ str(uuid.uuid4().int)[:5]
                if not GenerateTradeModel.objects.filter(Trade_id=trader_id).exists():
                    break
            self.Trade_id=trader_id # set the Trade_id field after finding a unique trader_id
        super(GenerateTradeModel, self).save(*args, **kwargs)
                

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Company_name)



class TankCapacityM(SoftDeleteModel):
    Port = models.ForeignKey(PortM, on_delete=models.CASCADE)
    Terminal = models.ForeignKey(TerminalM, on_delete=models.CASCADE)
    Tank_type = models.ForeignKey(TankTypeM, on_delete=models.CASCADE)
    Tank_no = models.ForeignKey(TankNumberM, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=100, null=True, blank=True, default="Empty")
    Density = models.FloatField(null=True, blank=True)
    Nominal_capacity = models.FloatField()
    Safe_fill_capacity = models.FloatField()
    Prevailing_GOV = models.FloatField()
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)

    Qty_add_discharge = models.FloatField(null=True, blank=True)  # calc
    Remaining_space = models.FloatField(null=True, blank=True)  # calc
    current_quantity = models.FloatField(null=True, blank=True, default=0)  # calc
    duration = models.IntegerField(null=True, blank=True)  # calc
    Today = models.DateField(default=datetime.now, null=True, blank=True)
    Remaining_days = models.IntegerField(null=True, blank=True)  # calc
    Cargo = models.CharField(max_length=100, null=True, blank=True)  # calc
    Cost = models.FloatField(null=True, blank=True)
    Remarks = models.CharField(max_length=100, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Tank_no)




class CompanyInvestmentModel(models.Model):
    Customer_Company_name = models.CharField(max_length=100)
    Customer_Account =  models.CharField(max_length=100)
    TRANSFERTYPE_CHOICE = (
        ("Credit", "Credit"),
        ("Debit", "Debit"),
    )
    Customer_Transfer_Type = models.CharField(max_length=100, choices=TRANSFERTYPE_CHOICE,)
    Transfer_Amount = models.FloatField()
    Cash_Factor = models.FloatField(null=True)
    Email = models.EmailField()
    Remarks = models.CharField(max_length=250, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Customer_Company_name)
    

#future blotter model

## futureblotter  same as swap
class FutureBlotterModel(SoftDeleteModel):
    date = models.CharField(max_length=100)
    trader_type = models.CharField(max_length=1000, null=True)
    # clearer = models.ForeignKey(ClearerRateM, on_delete=models.CASCADE)
    bileteral_external = models.CharField(max_length=100, default='bilateral')
    clearer = models.CharField(max_length=1000, null=True)
    trader = models.ForeignKey(Traders, on_delete=models.CASCADE)
    book = models.CharField(max_length=1000, null=True)
    customer_company = models.CharField(max_length=10000, null=True)
    customer_account = models.CharField(max_length=10000, null=True)
    volume = models.CharField(max_length=1000, null=True)
    contract = models.CharField(max_length=100, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    # Contract_Month = models.DateField(default=datetime.now,max_length=100, null=True)
    Contract_Month = models.CharField(max_length=100,null=True, blank=True)
    price = models.CharField(max_length=100, null=True)
    approx_ep = models.CharField(max_length=100, null=True,blank=True)
    # holiday =  models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=1000, null=True)
    broker = models.CharField(max_length=1000, null=True)
    efs_code = models.CharField(max_length=100, null=True)
    notes = models.CharField(max_length=250, blank=True, null=True)

    #calculatins
    unit =models.CharField(max_length=2000, null=True)
    Clearer_rate = models.CharField(max_length=2000, null=True)
    Exchange_rate = models.CharField(max_length=2000, null=True)
    brockerage = models.CharField(max_length=2000, null=True)
    total_fee = models.CharField(max_length=2000, null=True)
    holiday = models.CharField(max_length=1000, null=True)
    tick = models.CharField(max_length=2000, null=True)
    bbl_mt_conversion = models.CharField(max_length=2000, null=True)
    kbbl_mt_conversion = models.CharField(max_length=2000, null=True)
    Trade_id = models.CharField(max_length=250, blank=True, null=True)
    physical_code = models.CharField(max_length=250, blank=True, null=True)
    physica_blotter_connect = models.CharField(max_length=250, blank=True, null=True)
    duplicate_id= models.CharField(max_length=100, default='none')

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.clearer)

#futureblotter end



# swap blotter model
class SwapBlotterModel(SoftDeleteModel):
    date = models.CharField(max_length=100) #1
    trader_type = models.CharField(max_length=1000, null=True) 
    trader = models.ForeignKey(Traders, on_delete=models.CASCADE)#2
    book = models.CharField(max_length=1000, null=True)#4
    customer_company = models.CharField(max_length=10000, null=True)#9
    customer_account = models.CharField(max_length=10000, null=True)#5
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)#6
    derivatives = models.CharField(max_length=1000, null=True)#7
    clearer = models.CharField(max_length=100, null=True) #3
    contract = models.CharField(max_length=100, null=True) #10
    volume =  models.CharField(max_length=1000, null=True) #8
    start_date = models.CharField(max_length=100, null=True) #11
    end_date = models.CharField(max_length=100, null=True) #12
    price = models.CharField(max_length=100, null=True) #18
    approx_ep = models.CharField(max_length=100, null=True,blank=True) #13
    holiday =  models.CharField(max_length=1000, null=True) #14
    type = models.CharField(max_length=1000, null=True) #15
    broker = models.CharField(max_length=1000, null=True) #16
    efs_code = models.CharField(max_length=100, null=True) #17
    notes = models.CharField(max_length=250, blank=True, null=True)  # 18
    # newly added fields for storing calculated values
    Trade_id = models.CharField(max_length=250, blank=True, null=True)
    tick = models.CharField(max_length=2000, null=True)
    unit =models.CharField(max_length=2000, null=True)
    singl_dif = models.CharField(max_length=2000, null=True)
    mini_major = models.CharField(max_length=2000, null=True)
    mini_major_connection = models.CharField(max_length=2000, null=True)
    bbi_mt_conversion = models.CharField(max_length=2000, null=True)
    kbbl_mt_conversion = models.CharField(max_length=2000, null=True)
    total_days = models.CharField(max_length=2000, null=True)
    priced_days= models.CharField(max_length=2000, null=True)
    unpriced_days = models.CharField(max_length=2000, null=True)
    total_volume  = models.CharField(max_length=2000, null=True)
    priced_volume  = models.CharField(max_length=2000, null=True)
    unpriced_volume = models.CharField(max_length=2000, null=True)
    block_fee  = models.CharField(max_length=2000, null=True)
    screen_fee  = models.CharField(max_length=2000, null=True)
    brockerage = models.CharField(max_length=2000, null=True)
    total_fee = models.CharField(max_length=2000, null=True)
    bbi_mt = models.CharField(max_length=2000, null=True)
    kbbi_mt = models.CharField(max_length=2000, null=True)
    unpriced_kbbl_mt = models.CharField(max_length=2000, null=True)
    fw_months = models.CharField(max_length=2000, null=True)
    # new columns
    LTD = models.CharField(max_length=2000, null=True)
    First_month = models.DateField(null=True, blank=True)
    Second_month = models.DateField(null=True, blank=True)
    MTM = models.FloatField(null=True, blank=True)
    first_month_days = models.IntegerField(null=True, blank=True)
    second_month_days = models.IntegerField(null=True, blank=True)
    first_month_settle_price = models.FloatField(null=True, blank=True)
    second_month_settle_price = models.FloatField(null=True, blank=True)
    PNL = models.FloatField(null=True, blank=True)
    total_PNL = models.FloatField(null=True, blank=True)
    futures_equiv_first = models.FloatField(null=True, blank=True)
    futures_equiv_second = models.FloatField(null=True, blank=True)
    futures_equiv_first_kbbl = models.FloatField(null=True, blank=True)
    futures_equiv_second_kbbl = models.FloatField(null=True, blank=True)
    # Till here
    duplicate_id= models.CharField(max_length=100, default='none')
    # bileteral_external = models.CharField(max_length=100, null=True, blank=True)
    bileteral_external = models.CharField(max_length=100, default='bilateral')
    buy_sell = models.CharField(max_length=100, default='none')
    physical_code =  models.CharField(max_length=2000, null=True)
    physica_blotter_connect = models.CharField(max_length=250, blank=True, null=True)

    total_n_days = models.CharField(max_length=2000, null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']


    def __str__(self):
        return str(self.contract)


# CustomerTrades blotter model
class CustomerTradesModel(SoftDeleteModel):
    date = models.CharField(max_length=100)  # 1
    trader_type = models.CharField(max_length=1000, null=True)
    # trader = models.ForeignKey(Traders, on_delete=models.CASCADE)  # 2
    trader = models.CharField(max_length=100, null=True, blank=True)  # 11
    book = models.CharField(max_length=1000, null=True)  # 4
    customer_company = models.CharField(max_length=10000, null=True)  # 9
    customer_account = models.CharField(max_length=10000, null=True)  # 5
    # strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # 6
    strategy = models.CharField(max_length=100, null=True)  # 10
    derivatives = models.CharField(max_length=1000, null=True)  # 7
    clearer = models.CharField(max_length=100, null=True)  # 3
    contract = models.CharField(max_length=100, null=True)  # 10
    volume = models.CharField(max_length=1000, null=True)  # 8
    start_date = models.CharField(max_length=100, null=True)  # 11
    end_date = models.CharField(max_length=100, null=True)  # 12
    price = models.CharField(max_length=100, null=True)  # 18
    approx_ep = models.CharField(max_length=100, null=True, blank=True)  # 13
    holiday = models.CharField(max_length=1000, null=True)  # 14
    type = models.CharField(max_length=1000, null=True)  # 15
    broker = models.CharField(max_length=1000, null=True)  # 16
    efs_code = models.CharField(max_length=100, null=True)  # 17
    notes = models.CharField(max_length=250, blank=True, null=True)  # 18
    # newly added fields for storing calculated values
    Trade_id = models.CharField(max_length=250, blank=True, null=True)
    tick = models.CharField(max_length=2000, null=True)
    unit = models.CharField(max_length=2000, null=True)
    singl_dif = models.CharField(max_length=2000, null=True)
    mini_major = models.CharField(max_length=2000, null=True)
    mini_major_connection = models.CharField(max_length=2000, null=True)
    bbi_mt_conversion = models.CharField(max_length=2000, null=True)
    kbbl_mt_conversion = models.CharField(max_length=2000, null=True)
    total_days = models.CharField(max_length=2000, null=True)
    priced_days = models.CharField(max_length=2000, null=True)
    unpriced_days = models.CharField(max_length=2000, null=True)
    total_volume = models.CharField(max_length=2000, null=True)
    priced_volume = models.CharField(max_length=2000, null=True)
    unpriced_volume = models.CharField(max_length=2000, null=True)
    block_fee = models.CharField(max_length=2000, null=True)
    screen_fee = models.CharField(max_length=2000, null=True)
    brockerage = models.CharField(max_length=2000, null=True)
    total_fee = models.CharField(max_length=2000, null=True)
    bbi_mt = models.CharField(max_length=2000, null=True)
    kbbi_mt = models.CharField(max_length=2000, null=True)
    unpriced_kbbl_mt = models.CharField(max_length=2000, null=True)
    fw_months = models.CharField(max_length=2000, null=True)
    # new columns
    LTD = models.CharField(max_length=2000, null=True)
    First_month = models.DateField(null=True, blank=True)
    Second_month = models.DateField(null=True, blank=True)
    MTM = models.FloatField(null=True, blank=True)
    first_month_days = models.IntegerField(null=True, blank=True)
    second_month_days = models.IntegerField(null=True, blank=True)
    first_month_settle_price = models.FloatField(null=True, blank=True)
    second_month_settle_price = models.FloatField(null=True, blank=True)
    PNL = models.FloatField(null=True, blank=True)
    total_PNL = models.FloatField(null=True, blank=True)
    futures_equiv_first = models.FloatField(null=True, blank=True)
    futures_equiv_second = models.FloatField(null=True, blank=True)
    futures_equiv_first_kbbl = models.FloatField(null=True, blank=True)
    futures_equiv_second_kbbl = models.FloatField(null=True, blank=True)
    # Till here
    duplicate_id = models.CharField(max_length=100, default='none')
    # bileteral_external = models.CharField(max_length=100, null=True, blank=True)
    bileteral_external = models.CharField(max_length=100, default='bilateral')
    buy_sell = models.CharField(max_length=100, default='none')
    physical_code = models.CharField(max_length=2000, null=True)
    physica_blotter_connect = models.CharField(max_length=250, blank=True, null=True)

    total_n_days = models.CharField(max_length=2000, null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.contract)


class TestBlotter(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Contract_name = models.ForeignKey(ContractM, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Book)
    
class FutureLTD(models.Model):
    Contract_symbol = models.DateField(null=True,blank=True)
    Ls_gas_oil = models.DateField(null=True,blank=True)
    Brent_crude_futures = models.DateField(null=True,blank=True)
    RBOB_Gasoline_futures = models.DateField(null=True,blank=True)
    Heating_oil_futures = models.DateField(null=True,blank=True)
    WTI_crude_futures = models.DateField(null=True,blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Contract_symbol)


# class FuturesBlottersModel(models.Model):
#     Date = models.DateField(default=datetime.now)
#     TRADETYPE_CHOICE = (
#         ("External ", "External"),
#         ("Bilateral", "Bilateral"),
#     )
#     Trade_Type = models.CharField(max_length=100, choices=TRADETYPE_CHOICE)
#     Clearer = models.ForeignKey(ClearerRateM, on_delete=models.CASCADE)   # change clearer model to clearer rate model
#     Trader = models.ForeignKey(Traders, on_delete=models.CASCADE)
#     Book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
#     Customer_Company = models.ForeignKey(CompanyInvestmentModel, on_delete=models.CASCADE, null=True, blank=True, related_name="Compnay_name_from_company_investment")   #counter party..but not now
#     Account = models.ForeignKey(CompanyInvestmentModel, on_delete=models.CASCADE, null=True,blank=True, related_name="Account_from_companyinvestment")
#     Strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, null=True,blank=True)
#     Buy_Sell = models.CharField(max_length=100, null=True)
#     Volume = models.FloatField(null=True, blank=True)
#     Contract_Name = models.ForeignKey(ContractM, on_delete=models.CASCADE, null=True,related_name="fb_contractname")   # change to from clearerrate models selected clearers coreesponding  contractname
#     Contract_Month = models.DateField(default=datetime.now)
#     Price = models.FloatField(null=True, blank=True)
#     Approximate_EP = models.FloatField(null=True, blank=True)
#     Type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True,blank=True)
#     EFS_Code = models.IntegerField(null=True, blank=True)
#     Broker = models.ForeignKey(BrokerM, on_delete=models.CASCADE, null=True)
#
#     # newly added fields for storing calculated values
#     Unit = models.CharField(max_length=100, null=True, blank=True)
#     Clearer_rate = models.FloatField(null=True,blank=True)
#     Exchange_rate = models.FloatField(null=True,blank=True)
#     Brokerage = models.FloatField(null=True,blank=True)
#     Total_Fee = models.FloatField(null=True,blank=True)
#     Holiday = models.CharField(max_length=100, null=True, blank=True)
#     bbl_mt_conversion = models.FloatField(null=True, blank=True)
#     kbbl_mt_conversion = models.FloatField(null=True,blank=True)
#
#     Notes = models.CharField(max_length=250, blank=True, null=True)
#
#     def __str__(self):
#         return str(self.Trade_Type)


##############################  PHYSICAL BLOTTER  USERSIDE #######################

#Physical blotter
class PhysicalBlotterModel(SoftDeleteModel):
    Date = models.CharField(max_length=100) #1
    Trader = models.CharField(max_length=100, null=True, blank=True)
    # Book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    Book = models.CharField(max_length=100, null=True, blank=True)
    Company_name = models.CharField(max_length=100, null=True, blank=True)
    Strategy = models.CharField(max_length=100, null=True, blank=True)
    DERIVATIVE_CHOICE = (
        ("Physical", "Physical"),
    )
    Derivative = models.CharField(max_length=100, choices=DERIVATIVE_CHOICE, default="Physical")
    Trade_id = models.CharField(max_length=100, null=True, blank=True)

    BUYSELL_CHOICE = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    Buy_sell = models.CharField(max_length=100, choices=BUYSELL_CHOICE, null=True, blank=True)
    Cargo = models.CharField(max_length=100)
    Pricing_contract = models.ForeignKey(ContractM, on_delete=models.CASCADE, null=True, blank=True)
    PRICING_METHODE_CHOICE = (
        ("Fixed", "Fixed"),
        ("Float", "Float"),
    )
    Pricing_method = models.CharField(max_length=100,choices=PRICING_METHODE_CHOICE, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    # Unit = models.ForeignKey(Unit1, on_delete=models.CASCADE, null=True,blank=True)
    Unit = models.CharField(max_length=100, null=True, blank=True)
    Density = models.FloatField(null=True,blank=True)
    Nominated_quantity = models.CharField(max_length=100, null=True,blank=True)
    Premium_discount = models.CharField(max_length=100, null=True,blank=True)
    Pricing_term = models.CharField(max_length=100, null=True,blank=True)
    # BL_Date = models.DateField(default=datetime.now, null=True,blank=True)
    # start_date = models.DateField()
    bl_date = models.CharField(max_length=100, null=True,blank=True) #1
    start_date = models.CharField(max_length=100) #1
    end_date = models.CharField(max_length=100) #1
    # Holiday = models.ForeignKey(HolidayM, on_delete=models.CASCADE)
    Holiday = models.CharField(max_length=100)
    Total_no_days = models.IntegerField(null=True, blank=True)
    DELIVERY_MODE_CHOICES = (
        ("Tank", "Tank"),
        ("Vessel", "Vessel"),
        ("PLT", "PLT"),
    )
    Delivery_mode = models.CharField(max_length=100, choices=DELIVERY_MODE_CHOICES, null=True, blank=True)
    # Port = models.ForeignKey(PortM, on_delete=models.CASCADE, null=True, blank=True)
    Port = models.CharField(max_length=100, null=True, blank=True)
    # Terminal = models.ForeignKey(TerminalM, on_delete=models.CASCADE, null=True, blank=True)
    Terminal = models.CharField(max_length=100) #1
    Vessal_name = models.CharField(max_length=120, null=True, blank=True)
    # Tank = models.ForeignKey(TankCapacityM, on_delete=models.CASCADE, null=True, blank=True , related_name="Tank_tankcapacity")
    Tank = models.CharField(max_length=100, null=True,blank=True)
    External_Terminal = models.CharField(max_length=120, null=True, blank=True)
    HEADGING_CHOICE = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    Headging = models.CharField(max_length=100, choices=HEADGING_CHOICE, null=True, blank=True)
    Purchase_sales_ID= models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    Remarks = models.CharField(max_length=100, null=True, blank=True)
    # file = models.FileFiled(null=True,blank=True)

    # for backend calculations
    Terminal_cost = models.IntegerField(null=True, blank=True)
    Freight_cost = models.IntegerField(null=True, blank=True)
    Vessal_cost = models.IntegerField(null=True, blank=True)
    additional_secondary_charge = models.IntegerField(null=True, blank=True)
    additional_cost_type = models.CharField(max_length=100,null=True, blank=True)
    Total_Secondary_Cost = models.IntegerField(null=True, blank=True)
    price_days = models.IntegerField(null=True, blank=True)
    unprice_days = models.IntegerField(null=True, blank=True)
    total_volume = models.FloatField(null=True, blank=True)
    price_volume = models.FloatField(null=True, blank=True)
    unprice_volume = models.FloatField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    priced_price = models.IntegerField(null=True, blank=True)
    unpriced_price = models.IntegerField(null=True, blank=True)
    Shore_recieved = models.IntegerField(null=True, blank=True)
    Difference = models.IntegerField(null=True, blank=True)
    PnL = models.IntegerField(null=True, blank=True)
    Difference_Pnl = models.IntegerField(null=True, blank=True)
    Total_Profit_Loss = models.IntegerField(null=True, blank=True)
    m3 = models.FloatField(null=True,blank=True)
    current_qty = models.FloatField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Trader)

    class Meta:
        ordering = ['-Date']


# inventory transfer
class InventoryModel(SoftDeleteModel):
    #from
    date =  models.CharField(max_length=100) #1
    Trade_id = models.CharField(max_length=100)
    Purchase_sales_ID= models.CharField(max_length=100)
    Distribution_Type = models.CharField(max_length=100)
    Delivery_mode = models.CharField(max_length=100)    #source_container
    Strategy = models.CharField(max_length=100)   #source_strategy
    Tank = models.CharField(max_length=100,null=True,blank=True)
    Vessal_name = models.CharField(max_length=120,null=True,blank=True)
    Port = models.CharField(max_length=100)
    Terminal = models.CharField(max_length=100)
    Cargo = models.CharField(max_length=100)
    Shore_recieved = models.IntegerField(null=True, blank=True)
    Unit = models.CharField(max_length=100)
    Density = models.FloatField(null=True,blank=True)

    # To

    dest_trade_strategy = models.CharField(max_length=100) #backend calclation
    DESTINATION_CONTAINER_CHOICE = (
        ("Tank", "Tank"),
        ("Vessal", "Vessal"),
    )
    dest_container = models.CharField(max_length=100, choices=DESTINATION_CONTAINER_CHOICE, null=True, blank=True)
    dest_port = models.CharField(max_length=100)
    # dest_port = models.ForeignKey(PortM, on_delete=models.CASCADE)
    dest_terminal = models.CharField(max_length=100)
    # dest_terminal = models.ForeignKey(TerminalM, on_delete=models.CASCADE)
    dest_vessal_op = models.CharField(max_length=100,null=True,blank=True)
    dest_tank_num = models.CharField(max_length=100,null=True,blank=True)
    # dest_tank_num =  models.ForeignKey(TankNumberM, on_delete=models.CASCADE,null=True,blank=True)
    dest_cargo = models.CharField(max_length=100,null=True,blank=True) #backend calculation

    INV_TRANSFER_MODE_CHOICE = (
        ("None", "None"),
        ("Truck", "Truck"),
    )

    inv_transfer_mode = models.CharField(max_length=100, choices=INV_TRANSFER_MODE_CHOICE, null=True, blank=True)
    # inv_transfer_mode = models.CharField(max_length=100)
    dest_unit = models.CharField(max_length=100)
    dest_cargo_LD_QTY = models.FloatField()
    source_cargo_LD_QTY = models.FloatField(null=True,blank=True)
    dest_received_qty = models.FloatField()
    dest_tank_end_qty = models.FloatField(max_length=100,null=True,blank=True)
    dest_tank_remain_space = models.FloatField(max_length=100,null=True,blank=True)
    dest_difference= models.FloatField()
    book = models.CharField(max_length=100,null=True,blank=True)
    m3 = models.FloatField(null=True,blank=True)
    temperature = models.FloatField(null=True,blank=True)
    duplicate_id= models.CharField(max_length=100, default='none')

    created_date = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)


    # source_name = models.CharField(max_length=100)
    # source_port = models.CharField(max_length=100)
    # source_terminal = models.CharField(max_length=100)
    # source_trade_id = models.CharField(max_length=100)
    # # purchase_sales_id = models.CharField(max_length=100)
    # # source_pricing_contract = models.CharField(max_length=100)
    # source_product = models.CharField(max_length=100)
    # source_cargo_LD_QTY = models.IntegerField()
    # source_unit = models.CharField(max_length=100)
    # source_price = models.IntegerField()
    # dest_container = models.CharField(max_length=100)
    # dest_trade_strategy = models.CharField(max_length=100)
    # dest_port = models.CharField(max_length=100)
    # dest_terminal = models.CharField(max_length=100)
    # dest_vessal_op = models.CharField(max_length=100)
    # dest_tank_num = models.CharField(max_length=100)
    # dest_tank_density = models.IntegerField()
    # dest_cargo_LD_QTY = models.IntegerField()
    #
    # distribution_type = models.CharField(max_length=100)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.Trade_id)


















