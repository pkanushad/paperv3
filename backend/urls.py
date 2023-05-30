"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="backendapp"

urlpatterns = [
    path('', Login.as_view(), name="login"),
    path('admin-login', AdminLogin.as_view(), name="admin-login"),
    path('index', Index.as_view(), name="index"),
    path('logout', CustomLogoutView.as_view(), name="logout"),

    # ________________________________Create Uers______________________________________________________

    path('create-users', CreateUsers.as_view(), name='create_user'),
    path('create-admin-user', CreateAdminUser.as_view(), name='create_admin_user'),
    
    #_______________________Traders Crud _______________________________________________________
    path('add-trader/', AddTraders.as_view(), name='addtraders'),
    path('traders-detail/<int:pk>', TradersDetail.as_view(), name='traderdetails'),
    
    #_______________________Book Crud _______________________________________________________
    path('add-book/', AddBook.as_view(), name='addbook'),
    path('book-detail/<int:pk>', BooksDetail.as_view(), name='bookdetails'),
    
    
    #_______________________Product Crud _______________________________________________________
    path('add-product/', AddProduct.as_view(), name='addproduct'),
    path('Product-detail/<int:pk>', ProductDetails.as_view(), name='productdetails'),
    
    #_______________________Derivative Crud _______________________________________________________
    path('add-derivative/', Derivative.as_view(), name='derivative'),
    path('derivative-detail/<int:pk>', DerivativeDetails.as_view(), name='derivativedetails'),
    
    #_______________________Type Crud _______________________________________________________
    path('add-type/', Type.as_view(), name='type'),
    path('type-detail/<int:pk>', TypeDetails.as_view(), name='typedetails'),
    
    #_______________________UnitCrud _______________________________________________________
    path('add-unit/', Unit.as_view(), name='unit'),
    path('unit-detail/<int:pk>', UnitDetails.as_view(), name='unitdetails'),
    
    #________________________Strategy __________________________________________________
    path('add-strategy', AddStrategy.as_view(), name='add_startegy'),
    path('strategy-detail/<int:pk>', StrategyDetails.as_view(), name="startegy_details"),
        #_______________________Broker Crud _______________________________________________________
    path('add-broker/', Broker.as_view(), name='broker'),
    path('broker-detail/<int:pk>', BrokerDetails.as_view(), name='brokerdetails'),
    
     #_______________________Clearer Crud _______________________________________________________
    path('add-clearer/', Clearer.as_view(), name='clearer'),
    path('clearer-detail/<int:pk>', ClearerDetails.as_view(), name='clearerdetails'),
    
    #_______________________Contract Crud _______________________________________________________
    path('add-contract/', Contract.as_view(), name='contract'), 
    path('edit-contract/<int:id>', EditContract.as_view(), name='edit-contract'),
    
        #_______________________holiday Crud _______________________________________________________
    path('add-holiday/', Holiday.as_view(), name='holiday'),
     #______ajax
     
    path('all_holiday_api', AllHoliday.as_view(), name="all_holiday"),
    
    #____________________________Clearer Rate__________________________________________________________
    
    path('add-clearer-rate', ClearerRate.as_view(), name='clearear_rate'),
    path('edit-clearer-rate/<int:id>', EditClearer.as_view(), name='edit_clearer_rate'),
    path('clearer_rate_filter', clearer_rate_filter, name='clearer_rate_filter'),
    
    
    #________________________________API_____________________________________________________________
    
    path('clearear_api_swaps', clearear_api_swaps, name='clearear_api_swaps'),
    
    
    
    #_______________________________ brockerage____________________________________________________
    
    path('add-brockerage', BrockerageView.as_view() ,name='add_brockerage'),
    path('brockerage_contract_change/<str:contract_name>', brockerage_contract_change, name='brockerage_contract_change'),
    
    path('edit-brockerage-model/<int:id>', EditBrockerage.as_view(), name="edit_brockerage"),
    
    path('add-cargo', Cargo.as_view(), name='cargo'),
    path('add-counterparty', Counterparty.as_view(), name='counterparty'),
    path('add-port', Port.as_view(), name='port'),
    path('add-terminal', Terminal.as_view(), name='terminal'),
    path('add-tankno', TankNumber.as_view(), name='tankno'),
    path('add-tanktype', TankType.as_view(), name='tanktype'),

    path('add-generate-trade/', AddGenerateTradeView.as_view(), name="add-generate-trade"),
    
    

    
    
    #_____________________________________Unique Trader_____________________________________________
    
    path('unique-trader', UniqueTrader.as_view(), name='unique_trader'),
    path('edit-generate-trader-id/<int:id>', EditUniqueTrader.as_view(), name='edit_unique_trader'),
    path('close-request/<int:id>', Closerequest, name='close-request'),
    path('cancel-request/<int:id>',Cancelrequest, name='cancel-request'),

    path('close-request-admin/<int:id>', CloseRequestView.as_view(), name='close-request-admin'),
    
    #___________________________________Customer____________________________________________________

    path('customer-dashboard', CustomerDashboard.as_view(), name="customer_dashboard"),
    path('swaps-blotter', SwapsBlotter.as_view(), name="swaps-blotter"),
    path('copy-swaps-blotter/<int:id>', CopySwapsBlotter.as_view(), name="copy-swaps-blotter"),
    path('edit-swaps-blotter/<int:id>', EditSwapsBlotter.as_view(), name='swaps_blotter'),

    path('swaps-blotter-detail/<int:id>', SwapsBlotterDetailsView.as_view(), name='swaps_blotter_detail'),

    path('delete-swaps-blotter/<int:id>', DeleteSwapsBlotter.as_view(), name='delete_swaps_blotters'),
    path('search_customer_company/<str:company_name>', search_customer_company, name="search_customer_company" ),
    path('swaps_bloters_clearer_derivative', swaps_bloters_clearer_derivative, name='swaps_bloters_clearer_derivative'),
    path('contract_name_holiday_relation',contract_name_holiday_relation, name='contract_name_holiday_relation'),
    path('enddate_of_month',enddate_of_month, name='enddate_of_month'),
    path('export_sb_csv_today', export_sb_csv_today, name='export_sb_csv_today'),
    path('swaps_blotters_company_broker_derivative', swaps_blotters_company_broker_derivative, name='swaps_blotters_company_broker_derivative'),



    # update swapblotter
    path('update_database', update_database, name="update_database"),


    # fututre blotter same as swap

    path('future-blotter', FutureBlotter.as_view(), name="future-blotter"),
    path('copy-future-blotter/<int:id>', CopyFutureBlotter.as_view(), name="copy-future-blotter"),
    path('edit-future-blotter/<int:id>', EditFutureBlotter.as_view(), name='future_blotter'),
    path('delete-future-blotter/<int:id>', DeleteFutureBlotter.as_view(), name='delete_future_blotters'),
    # path('search_customer_company/<str:company_name>', search_customer_company, name="search_customer_company"),
    path('future_bloters_clearer_derivative', future_bloters_clearer_derivative, name='future_bloters_clearer_derivative'),

    path('future_bloters_holiday_relation', future_bloters_holiday_relation, name='future_bloters_holiday_relation'),

    # filter broker based on compnay name same as cleaer
    path('future_bloters_company_broker_derivative', future_bloters_company_broker_derivative, name='future_bloters_company_broker_derivative'),

    path('future_bloters_company_holiday_relation', future_bloters_company_holiday_relation, name='future_bloters_company_holiday_relation'),






    path('contract_name_holiday_relation_fb', contract_name_holiday_relation_fb, name='contract_name_holiday_relation_fb'),

    path('filter_futureblotter_table', filter_futureblotter_table, name='filter_futureblotter_table'),

    path('future-blotter-detail/<int:id>', FutureBlotterDetailsView.as_view(), name='future_blotter_detail'),

    path('export_fb_csv_today', export_fb_csv_today, name='export_fb_csv_today'),






    # ____________________________________Physicalblotter __________________________________________________
   # same as swap
    path('physical-blotter/<int:id>', PhysicalBlotterView.as_view(), name="physical-blotter"),
    path('edit-physical-blotter/<int:id>', EditPhysicalBlotter.as_view(), name='edit-physical-blotter'),
    path('delete-physical-blotter/<int:id>', DeletePhysicalBlotter.as_view(), name='delete_physical_blotters'),
    path('tank_port_terminal_relation',tank_port_terminal_relation, name='tank_port_terminal_relation'),
    path('update_pb_database', update_pb_database, name="update_pb_database"),

    # pb list
    path('pb-list/', PBListView.as_view(), name="pb-list"),
    # bill shore
    path('add-bill-shore/<str:id>', PB_BillShoreView.as_view(), name="bill-shore"),
    path('edit-bill-shore/<int:id>', EditBillShore.as_view(), name='edit-bill-shore'),
    path('delete-bill-shore/<int:id>', DeleteBillShore.as_view(), name='delete_bill_shore'),

    #pb summary/bill shore
    path('pb-summary/', PbSummaryView.as_view(), name="pb-summary"),

    # inventory management
    path('inventory/<str:id>/', InventoryManagementView.as_view(), name="inventory"),
    path('inventory-list/', InventoryListView.as_view(), name="inventory-list"),
    path('edit-inventory/<int:id>', EditInventory.as_view(), name='edit-inventory'),
    path('tank_port_terminal_relation_INV', tank_port_terminal_relation_INV, name='tank_port_terminal_relation_INV'),



   # userside generate listview
    path('generate-trade-user/', GenerateTradeUserListView.as_view(), name="generate-trade-user"),

  ## Stock summary
    path('stock-summary/', StockSummaryListView.as_view(), name="stock-summary"),



    # tank details , capacity
    path('tank-capacity', TankCapacityView.as_view(), name="tank-capacity"),




    #____________________________________Company Investment__________________________________________________

 path('add-company-investment/',AddCompanyInvestment.as_view(), name="add-company-investment"),
 path('edit-compinvest/<str:id>',CompanyInvestmentEditView.as_view(), name="edit-company-investment"),
 path('delete-compinvest/<str:id>',RemoveCompanyInvestment, name="remove-company-investment"),

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$physical blotter%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # HEDGING

    path('hedging', Headging, name="hedging"),
    path('hedging_in_lots',hedging_in_lots, name="hedging_in_lots"),
    path('paper_hedging',Paperhedging,name="paper_hedging"),
    path('hedging_strategy_kbbl', hedging_strategy_kbbl, name="hedging_strategy_kbbl"),
    path('hedging_strategy_lots', hedging_strategy_lots, name="hedging_strategy_lots"),
    path('paper_exposure_break_by_strategy', paper_exposure_break_by_strategy, name="paper_exposure_break_by_strategy"),



    # TRADE POSITION
    #lots
    path('dash_future/', futures_lot_position, name="dash_future"),
    path('dash_swap/', swap_lot_position, name="dash_swap"),
    path('fbsb_total/', total_fbsb_trade_position_lots, name="fbsb_total"),

    ### lot statement position

    path('future_lots_statement/', future_lots_statement, name="future_lots_statement"),
    path('swap_lots_statement/', swap_lots_statement, name="swap_lots_statement"),
    path('fbsb_lots_statemnts/', fbsb_lots_statemnts, name="fbsb_lots_statemnts"),

    ##########  future lots statement by filter:

    path('future_lots_statement_filter /', future_lots_statement_filter, name="future_lots_statement_filter"),
    path('swap_lots_statement_filter/', swap_lots_statement_filter, name="swap_lots_statement_filter"),
    path('fbsb_lots_statemnts_filter/', fbsb_lots_statemnts_filter, name="fbsb_lots_statemnts_filter"),



    # # kbbl
    path('fb-position-kbbl', future_kbbl_position, name="fb-kbbl-position"),
    path('sb-position-kbbl', swap_kbbl_position, name="sb-kbbl-position"),
    path('futures_eqvi', futures_equivalent, name="futures_eqvi"),
    # single url for all positions including filter company and kbbl\lots
    path('tatal_kbbl_position', total_kbbl_trade_position, name="tatal_kbbl_position"),
    path('thismonth',thismonthprice,name='thismonth'),
    path('thismonthholiday',thismonthholiday,name='thismonthholiday'),



################ trade posiiton kbbl and lots filter company name
    # kbbl
    path('future_filter_position/', future_position_kbbl_company_name, name="future_filter_position"),
    path('swaps_position_kbbl_company_name/', swaps_position_kbbl_company_name,name="swaps_position_kbbl_company_name"),
    path('futures_equivalent_kbbl_company_name/', futures_equivalent_kbbl_company_name,name="futures_equivalent_kbbl_company_name"),
    path('total_kbbl_trade_position_companyName/', total_kbbl_trade_position_companyName,name="total_kbbl_trade_position_companyName"),
    # lots
    path('futures_lot_position_companyname/', futures_lot_position_companyname,name="futures_lot_position_companyname"),
    path('swap_lot_position_companyname/', swap_lot_position_companyname, name="swap_lot_position_companyname"),
    # all company filter
    path('total_fbsb_trade_position_lots_companyname/', total_fbsb_trade_position_lots_companyname,name="total_fbsb_trade_position_lots_companyname"),

    # TRADE HISTORY
    path('fb-trade-hist/', Future_tradehistory, name="fb-trade-hist"),
    path('sb-trade-hist/', Swap_tradehistory, name="sb-trade-hist"),
    path('pb-trade-hist/', Physical_tradehistory, name="pb-trade-hist"),



    path('fb-sb-trade-hist/',Fb_Sb_Tradehistory, name='fbsbtradehistory'),
    path('hist',Checkhistory,name="hist"),


    path('swap-trade-history',SwapsTradeHistory.as_view(),name="swap-trade-history"),
    path('delete-swaps-tradehistory/<int:id>', DeleteSwapsTradeHistory.as_view(), name='delete_swaps_tradehistory'),
    path('swap-futures-trade-history',SwapsFuturesTradeHistory.as_view(),name="swap-futures-trade-history"),
    path('all-trade-history',AllTradehist.as_view(),name="alltradehist"),

    path('fb-tradehistory-detail/<int:id>', FutureBlotterHistoryDetailsView.as_view(), name='future_blotter_trade_detail'),
    path('sb-tradehistory-detail/<int:id>', SwapsBlotterHistoryDetailsView.as_view(), name='swaps_blotter_trade_detail'),


    # checking filter
    # path('book', PositionFilterdropdown, name='book'),
    # path('book2', filter_position_company_lots, name='book2'),
    path('filter', CompanyFilterPosition.as_view(), name='filter'),


    #POSITION PHYSICAL
    path('physical_position',physical_position,name="physical_position"),

    path('physical_hedging',physical_hedging,name="physical_hedging"),


    path('index2',index2,name='index2'),

    path('tank-summary',TankSummary.as_view(),name="tank-summary"),
    path('deal-status',DealStatus.as_view(),name="deal-status"),


    #INVENTORY LOAD DISCHARGE
    path('load-discharge-inv/<str:id>/', LoadDischargeInventory.as_view(), name="load-discharge-inv"),
    path('inv-sale-pb/<str:id>/',InventorySale.as_view(), name="inv-sale-pb"),
    path('discharge-cargo-sale/<str:id>/',DischargeCargoSale.as_view(), name="discharge-cargo-sale"),

    # CHARTS
    path('charts',charts,name="chart"),
    path("copydata",copydata,name="copydata"),

    path("inventory_data", InventoryData.as_view(), name="inventory_data"),
    path("invdash2", invdash, name="invdash2"),
    path('pie-chart/', pie_chart, name='pie-chart'),


    path('bar_chart/', bar_chart, name='bar_chart'),
    path('bar_chart2', bar_chart2, name='bar_chart2'),





    path('port_terminal_chart_relation', port_terminal_chart_relation, name='port_terminal_chart_relation'),

    path('futureltd/', futureltd, name='futureltd'),
    path('futureltd2', FutureLTDView.as_view(), name='futureltd2'),
    path('displaycsv', display_csv, name='displaycsv'),

    # PRICING
    path('pricing', PricingView.as_view(), name='pricing'),
    path('historicalsettle', HistoricalSettelment.as_view(), name='historicalsettle'),

    path("customer-index",customerindex,name="customer-index"),
    path("invdash2",invdash2,name="invdash2"),

    path("neeew",neeew,name="neeew"),

    path('exportfb-to-csv/',export_fb_csv, name="exportfb"),
    path('exportsb-to-csv/', export_sb_csv, name="exportsb"),

    path('filtertable', filtertable, name="filtertable"),

    path('last_date/', last_date_of_month, name='last_date_of_month'),

    # path('initialmargin', initialmargin, name="initialmargin"),

]

