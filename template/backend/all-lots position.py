
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






#####




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


###################33



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


