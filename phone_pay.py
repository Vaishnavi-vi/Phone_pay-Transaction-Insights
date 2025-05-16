import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

from mysql.connector import connect
connection=connect(host="localhost",
                   port="3306",
                  user="root",
                  password="Sunita@123",
                  database="phone_pay_pulse")

    
page = st.sidebar.radio("Go to", ["Home", "Business Case Study"])
if page=="Home":
    st.header("Phone Pay Project--India Overview")
    latitude = 23.5937
    longitude = 80.9629
    map_data=pd.DataFrame({"latitude":[latitude],"longitude":[longitude]})
    st.map(map_data,zoom=3.5)
elif page=="Business Case Study":
    st.header("Phone Pay Dashboard")
    
    operations=st.selectbox("Select one among the operations:",
                            ["Decoding Transaction Dynamics on PhonePe","Device Dominance and User Engagement Analysis",
                             "Insurance Penetration and Growth Potential Analysis","Transaction Analysis for Market Expansion",
                             "User Engagement and Growth Stratergy"])
    
    if operations=="Decoding Transaction Dynamics on PhonePe":
        st.subheader("Decoding Transaction Dynamics on PhonePe") 
        #_1.1_______________
        st.subheader("Total Transaction amount analysis") 
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox1")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="quarter_selectbox1")    
        query=f"SELECT state,sum(transaction_amount) as total_transaction_amount from aggreated_transaction where year='{selected_year}'and quarter='{selected_quarter}' group by state order by total_transaction_amount desc;"
        at=pd.read_sql(query,connection)  
        
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        at["state"]=at["state"].str.strip().replace(state_corrections)
        at["state"]=at["state"].str.title()
       
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson_data=requests.get(url).json()
        fig=px.choropleth(at,geojson=geojson_data,featureidkey="properties.ST_NM",locations="state",color="total_transaction_amount",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        
        #1.2________________________________

        st.subheader("Transaction behavior across years and Quaters")
        query="select year,quarter,sum(transaction_amount) as total_transaction_amount from aggreated_transaction group by year ,quarter order by sum(transaction_amount) asc;"
        op2=pd.read_sql(query,connection)
        fig=px.bar(op2,x="year",y="total_transaction_amount",color="quarter",barmode="group",title="Transaction trend accross years and Quarters")
        st.plotly_chart(fig)
        st.write("Output:In all the years Quarter 4 shows greater transaction among all.")
        #1.3___________________________________
        
        st.subheader("Transaction behavior across payment categories")
        
        query="select transaction_name,sum(transaction_amount) as total_transaction_amount from aggreated_transaction group by transaction_name order by sum(transaction_amount) desc;"
        op3=pd.read_sql(query,connection)
        fig=px.pie(op3,names="transaction_name",values="total_transaction_amount",title="Share of total transaction amount by transaction_category")
        st.plotly_chart(fig)
        st.write("Output: Peer to peer has max contribution in transaction category")
        
        query="select transaction_name,sum(transaction_count) as total_transaction_count from aggreated_transaction group by transaction_name order by sum(transaction_count) desc;"
        op_3=pd.read_sql(query,connection)
        fig=px.pie(op_3,names="transaction_name",values="total_transaction_count",title="Share of total transaction count by transaction_category")
        st.plotly_chart(fig)
        #_1.4___________________
        st.subheader("Top 10 states has maximum transaction amount")
        query="select state,sum(transaction_amount) as total_transaction_amount from aggreated_transaction group by state order by total_transaction_amount desc limit 10;"
        op4=pd.read_sql(query,connection)
        fig=px.bar(op4,x="state",y="total_transaction_amount",title="Transaction_amount accross states")
        st.plotly_chart(fig)
        #1.5_____________________
        st.subheader("Transaction behavior accross states in different payment categories")
        states=pd.read_sql("select distinct(state) from aggreated_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox1")
        query=f"select transaction_name, sum(transaction_amount) as total_transaction_amount from aggreated_transaction where state='{select_state}' group by transaction_name;"
        op5=pd.read_sql(query,connection)
        fig=px.bar(op5,x="transaction_name",y="total_transaction_amount",title="Transaction behavior in different payment categories")
        st.plotly_chart(fig)
        #1.6______________________
        st.subheader("States that have lowest transaction count")
        query="select state, sum(transaction_count) as total_transaction_count from aggreated_transaction group by state order by total_transaction_count asc limit 10;"
        op6=pd.read_sql(query,connection)
        fig=px.bar(op6,x="state",y="total_transaction_count",title="States with lowest transaction count")
        st.plotly_chart(fig)
    #__________________________________________________________________________________   
    elif operations=="Device Dominance and User Engagement Analysis":
        st.subheader("Device Dominance and User Engagement Analysis") 
        st.subheader("Total registered users analysis")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox2")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="quarter_selectbox2") 
        
        query=f"""select state,sum(registered_users) as total_registered_users from aggreated_user where year={selected_year} and quarter={selected_quarter} group by state order by total_registered_users desc;"""
        au=pd.read_sql(query,connection)
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        au["state"]=au["state"].str.strip().replace(state_corrections)
        au["state"]=au["state"].str.title()
        fig=px.choropleth(au,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_registered_users",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        #_2.1______________________________________
        st.subheader("Total appOpeners analysis")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023])
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4]) 
        
        query=f"""select state,sum(app_opens) as total_app_openers from aggreated_user where year={selected_year} and quarter={selected_quarter} group by state order by total_app_openers desc;"""
        au_=pd.read_sql(query,connection)
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        au_["state"]=au_["state"].str.strip().replace(state_corrections)
        au_["state"]=au_["state"].str.title()
        fig=px.choropleth(au_,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_app_openers",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        
        #2.2______________________________________
        st.subheader("Registered Users accross Phone's brand")
        query="select brand,sum(registered_users) as total_registered_users from aggreated_user group by brand order by total_registered_users desc;"
        au1=pd.read_sql(query,connection)
        fig=px.bar(au1,x="brand",y="total_registered_users",title="Registered_users among phone brands")
        st.plotly_chart(fig)
        #2.3_________________________________________
        st.subheader("Registered_users accross states with different phone's brand")
        states=pd.read_sql("select distinct(state) from aggreated_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox2")
        query=f"select brand,sum(registered_users) as total_registered_users from aggreated_user where state='{select_state}' group by brand;"  
        au2=pd.read_sql(query,connection)
        fig=px.bar(au2,x="brand",y="total_registered_users",title="Registered_users accross phone's brand")
        st.plotly_chart(fig)                     
        
        #_2.4________________________________________
        st.subheader("Percentage users among states")
        pu=st.selectbox("Percentage users among ststes",["Top 10 Highest percentage users amomg states","Top 10 lowest percentage users among states"])
        if pu=="Top 10 Highest percentage users amomg states":
            query="select state,sum(registered_users) as total_registered_users,sum(app_opens) as appOpens, round(sum(app_opens)/sum(registered_users),2) as percentage_users from aggreated_user group by state order by percentage_users desc limit 10;"
            au3_1=pd.read_sql(query,connection)
            fig=px.bar(au3_1,x="state",y="percentage_users",title="Registered_users among states")
            st.plotly_chart(fig)
        elif pu=="Top 10 lowest percentage users among states":
            query="select state,sum(registered_users) as total_registered_users,sum(app_opens) as appOpens, round(sum(app_opens)/sum(registered_users),2) as percentage_users from aggreated_user group by state order by percentage_users asc limit 10;"
            au3_2=pd.read_sql(query,connection)
            fig=px.bar(au3_2,x="state",y="percentage_users",title="Registered_users among states")
            st.plotly_chart(fig)
        #2.5_____________________________________
        
        st.subheader("Utilization_rate accross mobile brands")
        query="select brand,sum(registered_users) as total_registered_users,sum(app_opens) as total_appOpens, sum(app_opens)/sum(registered_users) as utilization_rate from aggreated_user group by brand;"
        au4=pd.read_sql(query,connection)
        fig=px.line(au4,x="brand",y="utilization_rate",title="utilization_rate accross different phone's brands")
        st.plotly_chart(fig)
        st.write("Output: Tenco has highest utilization rate among all phone's brands.")
        #________________________________________________________________________________
        
       ##_3_______________ 
    elif operations=="Insurance Penetration and Growth Potential Analysis":
        st.subheader("Insurance Penetration and Growth Potential Analysis")
        #_______________3.1
        st.subheader("Insurance_amount Analysis")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2020,2021,2022,2023],key="year_selectbox3")
        with col2:
            selected_quarter=st.selectbox("Quarter",[2,3,4],key="Quarter_selectbox3") 
        
        query=f"""select state,sum(insurance_amount) as total_insurance_amount from aggreated_insurance where year={selected_year} and quarter={selected_quarter} group by state order by total_insurance_amount desc;"""
        ai=pd.read_sql(query,connection)
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        ai["state"]=ai["state"].str.strip().replace(state_corrections)
        ai["state"]=ai["state"].str.title()
    
        fig=px.choropleth(ai,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_insurance_amount",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        
        #_________________________3.2
        st.subheader("Insurance trends among Years and Quarter")
        insurance=st.selectbox("Insurance among Year and Quarters",["Insurance amount among Year and Quarter","Insurance count among Year and Quarter"])
        if insurance=="Insurance amount among Year and Quarter":
            query="select year,Quarter,sum(insurance_amount) as total_insurance_amount from aggreated_insurance group by year,Quarter order by total_insurance_amount;"
            ai_2=pd.read_sql(query,connection)
            fig=px.bar(ai_2,x="year",y="total_insurance_amount",color="Quarter",barmode="group",title="Insurance amount trends among year and Quarter")
            st.plotly_chart(fig)
        elif insurance=="Insurance count among Year and Quarter":
            query="select year,Quarter,sum(insurance_count) as total_insurance_count from aggreated_insurance group by year,Quarter order by total_insurance_count;"
            ai_2_1=pd.read_sql(query,connection)
            fig=px.bar(ai_2_1,x="year",y="total_insurance_count",color="Quarter",barmode="group",title="Insurance count trends among year and Quarter")
            st.plotly_chart(fig)
        #_________________3.3    
            
        st.subheader("Insurance_count Analysis")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2020,2021,2022,2023],key="year_selectbox4")
        with col2:
            selected_quarter=st.selectbox("Quarter",[2,3,4],key="Quarter_selectbox4") 
        
        query=f"""select state,sum(insurance_count) as total_insurance_count from aggreated_insurance where year={selected_year} and quarter={selected_quarter} group by state order by total_insurance_count desc;"""
        ai_3=pd.read_sql(query,connection)
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
        "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        ai_3["state"]=ai_3["state"].str.strip().replace(state_corrections)
        ai_3["state"]=ai_3["state"].str.title()
        fig=px.choropleth(ai_3,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_insurance_count",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)    
        #________________ 3.4  
        st.subheader("Top states that contribute in insurance_amount")
        insurance_count=st.selectbox("Top states that contribute in insurance_amount",["Top 10 states that contribute to highest insurance amount","Top 10 states that contribute to lowest insurance amount"]) 
        if insurance_count=="Top 10 states that contribute to highest insurance amount":
            st.subheader("Top 10 states that contribute to highest insurance amount")
            query="select state,sum(insurance_amount) as total_insurance_amount from aggreated_insurance group by state order by total_insurance_amount desc limit 10;"
            ai_4=pd.read_sql(query,connection)
            fig=px.bar(ai_4,x="state",y="total_insurance_amount",title="States that shows higher contribution to insurance_amount")
            st.plotly_chart(fig)
        elif insurance_count=="Top 10 states that contribute to lowest insurance amount":
            st.subheader("Top 10 states that contribute to lowest insurance amount")
            query="select state,sum(insurance_amount) as total_insurance_amount from aggreated_insurance group by state order by total_insurance_amount asc limit 10;"
            ai_4_=pd.read_sql(query,connection)
            fig=px.bar(ai_4_,x="state",y="total_insurance_amount",title="States that shows lowest contribution to insurance_amount")
            st.plotly_chart(fig)
            
        #___________________3.5
        st.subheader("Top states that contribute in insurance_count")
        insurance_amount=st.selectbox("Top states that contribute in insurance_count",["Top 10 states that contribute to highest insurance count","Top 10 states that contribute to lowest insurance count"]) 
        if insurance_amount=="Top 10 states that contribute to highest insurance count":
            st.subheader("Top 10 states that contribute to highest insurance count")
            query="select state,sum(insurance_count) as total_insurance_count from aggreated_insurance group by state order by total_insurance_count desc limit 10;"
            ai_5=pd.read_sql(query,connection)
            fig=px.bar(ai_5,x="state",y="total_insurance_count",title="States that shows higher contribution to insurance_count")
            st.plotly_chart(fig)
            
        elif insurance_amount=="Top 10 states that contribute to lowest insurance count":
            st.subheader("Top 10 states that contribute to lowest transaction count")
            query="select state,sum(insurance_count) as total_insurance_count from aggreated_insurance group by state order by total_insurance_count asc limit 10;"
            ai_5_=pd.read_sql(query,connection)
            fig=px.bar(ai_5_,x="state",y="total_insurance_count",title="States that shows lowest contribution to insurance_count")
            st.plotly_chart(fig)
            
        #________________________________________________________________________________________________
        #4________________________________________________________________________________________________    
    elif operations=="Transaction Analysis for Market Expansion":
        st.subheader("Transaction Analysis for Market Expansion.")  
        #______________________________4.1
        st.subheader("Transaction amount analysis accross Indian States")  
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox5")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="Quarter_selectbox5") 
        query=f"select state, sum(transaction_amount) as total_transaction_amount from map_transaction where year='{selected_year}' and quater='{selected_quarter}' group by state order by total_transaction_amount desc;"
        mt1=pd.read_sql(query,connection)  
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
        "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        mt1["state"]=mt1["state"].str.strip().replace(state_corrections)
        mt1["state"]=mt1["state"].str.title()  
        fig=px.choropleth(mt1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_transaction_amount",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)    
        
        #_____________________________4.2
        st.subheader("Transaction count analysis accross Indian States")  
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox6")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="Quarter_selectbox6") 
        query=f"select state, sum(transaction_count) as total_transaction_count from map_transaction where year='{selected_year}' and quater='{selected_quarter}' group by state order by total_transaction_count desc;"
        mt1_1=pd.read_sql(query,connection) 
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
        "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        mt1_1["state"]=mt1_1["state"].str.strip().replace(state_corrections)
        mt1_1["state"]=mt1_1["state"].str.title()     
        fig=px.choropleth(mt1_1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey="properties.ST_NM",locations="state",color="total_transaction_count",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)    
        #________________________4.3
        st.subheader("Growth Opportunities")
        transaction_amount=st.selectbox("Growth Opportunities",["Top States with highest transaction amount","Top states with lowest transaction amount"])
        if transaction_amount=="Top States with highest transaction amount":
            st.subheader("Top States with highest transaction amount")
            query="select state,sum(transaction_amount) as total_transaction_amount from map_transaction group by state order by total_transaction_amount desc limit 10;"
            mt2=pd.read_sql(query,connection)
            fig=px.bar(mt2,x="state",y="total_transaction_amount",title="States with highest transaction amount")
            st.plotly_chart(fig)
            
        elif transaction_amount=="Top states with lowest transaction amount":
            st.subheader("Top States with lowest transaction amount")
            query="select state,sum(transaction_amount) as total_transaction_amount from map_transaction group by state order by total_transaction_amount asc limit 10;"
            mt2_=pd.read_sql(query,connection)
            fig=px.bar(mt2_,x="state",y="total_transaction_amount",title="States with lowest transaction amount")
            st.plotly_chart(fig)
        #__________________________________4.4
        st.subheader("Growth Opportunities")
        transaction_count=st.selectbox("Growth Opportunities",["Top States with highest transaction count","Top states with lowest transaction count"])
        if transaction_count=="Top States with highest transaction count":
            st.subheader("Top States with highest transaction count")
            query="select state,sum(transaction_count) as total_transaction_count from map_transaction group by state order by total_transaction_count desc limit 10;"
            mt3=pd.read_sql(query,connection)
            fig=px.bar(mt3,x="state",y="total_transaction_count",title="States with highest transaction count")
            st.plotly_chart(fig)
            
        elif transaction_count=="Top states with lowest transaction count":
            st.subheader("Top States with lowest transaction count")
            query="select state,sum(transaction_count) as total_transaction_count from map_transaction group by state order by total_transaction_count asc limit 10;"
            mt_3=pd.read_sql(query,connection)
            fig=px.bar(mt_3,x="state",y="total_transaction_count",title="States with lowest transaction count")
            st.plotly_chart(fig)
        #__________________________________________4.5
        st.subheader("Seasonality & Patterns")
        st.subheader("Transaction trends among Years and Quarter")
        transaction=st.selectbox("Transaction among Year and Quarters",["Transaction amount among Year and Quarter","Transaction count among Year and Quarter"])
        if transaction=="Transaction amount among Year and Quarter":
            query="select year,Quater,sum(transaction_amount) as total_transaction_amount from map_transaction group by year,Quater order by total_transaction_amount;"
            mt4=pd.read_sql(query,connection)
            fig=px.bar(mt4,x="year",y="total_transaction_amount",color="Quater",barmode="group",title="Transaction amount trends among year and Quarter")
            st.plotly_chart(fig)
        elif transaction=="Transaction count among Year and Quarter":
            query="select year,Quater,sum(transaction_count) as total_transaction_count from map_transaction group by year,Quater order by total_transaction_count;"
            mt4_=pd.read_sql(query,connection)
            fig=px.bar(mt4_,x="year",y="total_transaction_count",color="Quater",barmode="group",title="Treansaction count trends among year and Quarter")
            st.plotly_chart(fig)
        #______________________________________4.6
    
        st.subheader("Urban vs Rural Dynamics")
        st.subheader("Transaction behavior accross states in different rural and urban areas")
        states=pd.read_sql("select distinct(state) from map_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox2")
        query=f"select name, sum(transaction_amount) as total_transaction_amount from map_transaction where state='{select_state}' group by name;"
        mt5=pd.read_sql(query,connection)
        fig=px.bar(mt5,x="name",y="total_transaction_amount",title="Transaction amount behavior in rural and urban areas")
        st.plotly_chart(fig)
        #_____________________________________4.7
    
        
        states=pd.read_sql("select distinct(state) from map_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox3")
        query=f"select name, sum(transaction_count) as total_transaction_count from map_transaction where state='{select_state}' group by name;"
        mt5_=pd.read_sql(query,connection)
        fig=px.bar(mt5_,x="name",y="total_transaction_count",title="Transaction count behavior in rural and urban areas")
        st.plotly_chart(fig)
        #__________________________________4.8
        
        st.subheader("Market Share Benchmarking")
        st.subheader("Top 10 states with highest market share")
        query="SELECT state, sum(transaction_amount) as total_amount,sum(transaction_amount)*100/sum(sum(transaction_amount)) over() as market_share from map_transaction group by state order by market_share desc limit 10;"
        mt6=pd.read_sql(query,connection)
        fig=px.bar(mt6,x="state",y="market_share",title="States with highest market share")
        st.plotly_chart(fig)
        
        #___________________________5
    elif operations== "User Engagement and Growth Stratergy":
        st.subheader("User Engagement and Growth Stratergy.")
        st.subheader("Registered_Users in Indian States accross Years and Quarters")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox7")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="quarter_selectbox7") 
        
        query=f"select state,sum(registered_users) as total_registered_users from map_user where year='{selected_year}' and quater='{selected_quarter}' group by state order by total_registered_users desc;"
        mu=pd.read_sql(query,connection)
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        mu["state"]=mu["state"].str.strip().replace(state_corrections)
        mu["state"]=mu["state"].str.title()
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson_data=requests.get(url).json()
        fig=px.choropleth(mu,geojson=geojson_data,featureidkey="properties.ST_NM",locations="state",color="total_registered_users",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        #_________________________________5.1
        st.subheader("AppOpeners in Indian States accross Years and Quarters")
        col1,col2=st.columns(2)
        with col1:
            selected_year=st.selectbox("Year",[2018,2019,2020,2021,2022,2023],key="year_selectbox8")
        with col2:
            selected_quarter=st.selectbox("Quarter",[1,2,3,4],key="quarter_selectbox8") 
        
        query=f"select state,sum(app_opens) as total_app_openers from map_user where year='{selected_year}' and quater='{selected_quarter}' group by state order by total_app_openers desc;"
        mu_1=pd.read_sql(query,connection)
        
        state_corrections = {
        "andaman-&-nicobar-islands":"Andaman & Nicobar",
        "andhra-pradesh":"Andhra Pradesh",
        "arunachal-pradesh":"Arunachal Pradesh",
        "dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu",
        "himachal-pradesh":"Himachal Pradesh",
       "jammu-&-kashmir":"Jammu & Kashmir",
        "madhya-pradesh":"Madhya Pradesh",
        "tamil-nadu":"Tamil Nadu",
        "uttar-pradesh":"Uttar Pradesh",
        "west-bengal":"West Bengal"}
    
        
        mu_1["state"]=mu_1["state"].str.strip().replace(state_corrections)
        mu_1["state"]=mu_1["state"].str.title()
       
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson_data=requests.get(url).json()
        fig=px.choropleth(mu_1,geojson=geojson_data,featureidkey="properties.ST_NM",locations="state",color="total_app_openers",color_continuous_scale="Blues")    
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        
        #__________________________5.2
        st.subheader("Growth Opportunities")
        registered_users=st.selectbox("Growth Opportunities",["Top States with highest registered_users","Top states with lowest registered_users"])
        if registered_users=="Top States with highest registered_users":
            st.subheader("Top States with highest registered_users")
            query="select state,sum(registered_users) as total_registered_users from map_user group by state order by total_registered_users desc limit 10;"
            mu2=pd.read_sql(query,connection)
            fig=px.bar(mu2,x="state",y="total_registered_users",title="States with highest registered_users")
            st.plotly_chart(fig)
            
        elif registered_users=="Top states with lowest registered_users":
            st.subheader("Top States with lowest registered_users")
            query="select state,sum(registered_users) as total_registered_users from map_user group by state order by total_registered_users asc limit 10;"
            mu2_2=pd.read_sql(query,connection)
            fig=px.bar(mu2_2,x="state",y="total_registered_users",title="States with lowest registered_users")
            st.plotly_chart(fig)
            
        #______________________________5.3
        st.subheader("Growth Opportunities")
        app_openers=st.selectbox("Growth Opportunities",["Top States with highest app_openers","Top states with lowest app_openers"])
        if app_openers=="Top States with highest app_openers":
            st.subheader("Top States with highest app_openers")
            query="select state,sum(app_opens) as total_app_opens from map_user group by state order by total_app_opens desc limit 10;"
            mu3=pd.read_sql(query,connection)
            fig=px.bar(mu3,x="state",y="total_app_opens",title="States with highest appOpens")
            st.plotly_chart(fig)
            
        elif app_openers=="Top states with lowest app_openers":
            st.subheader("Top States with lowest app_openers")
            query="select state,sum(app_opens) as total_app_opens from map_user group by state order by total_app_opens asc limit 10;"
            mu3_2=pd.read_sql(query,connection)
            fig=px.bar(mu3_2,x="state",y="total_app_opens",title="States with lowest appOpens")
            st.plotly_chart(fig)
            
         #____________________________5.4
        st.subheader("Seasonality & Patterns")
        st.subheader("Users trend among Years and Quarter")
        Users=st.selectbox("Users among Year and Quarters",["Registered Users among Year and Quarter","AppOpens among Year and Quarter"])
        if Users=="Registered Users among Year and Quarter":
            query="select year,Quater,sum(registered_users) as total_registered_users from map_user group by year,Quater order by total_registered_users;"
            mu4=pd.read_sql(query,connection)
            fig=px.bar(mu4,x="year",y="total_registered_users",color="Quater",barmode="group",title="Registered Users trends among year and Quarter")
            st.plotly_chart(fig)
        elif Users=="AppOpens among Year and Quarter":
            query="select year,Quater,sum(app_opens) as total_app_opens from map_user group by year,Quater order by total_app_opens;"
            mu4_=pd.read_sql(query,connection)
            fig=px.bar(mu4_,x="year",y="total_app_opens",color="Quater",barmode="group",title="appOpens trend among year and Quarter")
            st.plotly_chart(fig)
        #_______________________________5.5
        st.subheader("Urban vs Rural Dynamics")
        st.subheader("Registered_users accross states in different rural and urban areas")
        states=pd.read_sql("select distinct(state) from map_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox3")
        query=f"select district, sum(registered_users) as total_registered_users from map_user where state='{select_state}' group by district;"
        mu5=pd.read_sql(query,connection)
        fig=px.bar(mu5,x="district",y="total_registered_users",title="Registered_users in rural and urban areas")
        st.plotly_chart(fig)
        #_____________________________________5.6
    
        
        states=pd.read_sql("select distinct(state) from map_transaction",connection)
        select_state=st.selectbox("State",states["state"].tolist(),key="state_selectbox4")
        query=f"select district, sum(app_opens) as total_app_opens from map_user where state='{select_state}' group by district;"
        mu5_=pd.read_sql(query,connection)
        fig=px.bar(mu5_,x="district",y="total_app_opens",title="AppOpens in rural and urban areas")
        st.plotly_chart(fig)
    #_______________________________________5.7
        st.subheader("Engagement Rate accross States")
        st.subheader("Top 10 states with highest Engagement Rate")
        query="SELECT state ,sum(app_opens)/(sum(registered_users)) as engagement_rate from map_user group by state order by engagement_rate desc limit 10;"
        mu6=pd.read_sql(query,connection)
        fig=px.bar(mu6,x="state",y="engagement_rate",title="States with highest engegement_rate")
        st.plotly_chart(fig)
            
        st.subheader("Thankyou!!")    
    
        
            
            
        
        
        
        

    
        
            
        
        
        
        
        
        
        
    
        
        


            
        

    





