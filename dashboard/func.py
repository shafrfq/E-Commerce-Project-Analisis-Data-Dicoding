import pandas as pd
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_df(self):
        daily_orders_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_df = daily_orders_df.reset_index()
        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)
        
        return daily_orders_df
    
    def create_sum_spend_df(self):
        sum_spend_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "payment_value": "sum"
        })
        sum_spend_df = sum_spend_df.reset_index()
        sum_spend_df.rename(columns={
            "payment_value": "total_spend"
        }, inplace=True)

        return sum_spend_df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df
    
    def create_monthly_transactions_df(self):
        monthly_transactions_df = self.df.resample(rule='M', on='order_approved_at').agg({
            "payment_value":"sum"
        })
        monthly_transactions_df.index = monthly_transactions_df.index.strftime('%B') #mengubah format order_approved_at menjadi Tahun-Bulan
        monthly_transactions_df = monthly_transactions_df.reset_index()
        monthly_transactions_df.rename(columns={
            "payment_value":"total_transactions"
        }, inplace=True)
        monthly_transactions_df = monthly_transactions_df.sort_values('total_transactions').drop_duplicates('order_approved_at', keep='last')

        return monthly_transactions_df
    
    def create_monthly_sells_df(self):
        monthly_sells_df = self.df.resample(rule='M', on='order_approved_at').agg({
            "order_id": "nunique",
        })
        monthly_sells_df.index = monthly_sells_df.index.strftime('%B')
        monthly_sells_df = monthly_sells_df.reset_index()
        monthly_sells_df.rename(columns={
            "order_id": "order_count",
        }, inplace=True)
        monthly_sells_df = monthly_sells_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')

        return monthly_sells_df
    
    def create_order_status(self):
        order_status_df = self.df["order_status"].value_counts().sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()

        return order_status_df, most_common_status

    def create_bystate_df(self):
        bystate_df = self.df.groupby(by="customer_state").customer_id.nunique().reset_index()
        bystate_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']
        bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)

        return bystate_df, most_common_state
    
    def create_bycity_df(self):
        bycity_df = self.df.groupby(by="customer_city").customer_id.nunique().reset_index()
        bycity_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_city = bycity_df.loc[bycity_df['customer_count'].idxmax(), 'customer_city']
        bycity_df = bycity_df.sort_values(by='customer_count', ascending=False).head(10) 
        
        return bycity_df, most_common_city
    
    def review_score_df(self):
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()

        return review_scores, most_common_score