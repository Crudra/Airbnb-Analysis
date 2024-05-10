import pandas as pd
import json
from pandas import json_normalize
import mysql.connector
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

mydb = mysql.connector.connect(
host='127.0.0.1',
user="root",
password="nayagam57",
database = "airbnbdb",
auth_plugin = 'mysql_native_password')
cursor = mydb.cursor()


def extract_data(data_frame, column_names):
    new_frame = data_frame.loc[:, column_names]
    return new_frame

class preprocessing:
    
    def load_json():
        with open(r'C:\Users\RUDRA\project\capstone4\sample_airbnb.json') as data_file:    
            data = json.load(data_file)  
        df = pd.json_normalize(data)
        return df
        
    def parentTable(df):
        columns_p =['_id','listing_url','name','property_type','room_type','bed_type','minimum_nights','maximum_nights','cancellation_policy','accommodates','bedrooms','beds','number_of_reviews','bathrooms','price','cleaning_fee','extra_people','guests_included','images.picture_url','review_scores.review_scores_rating']
        df_p = extract_data(df,columns_p)
        df_p.rename(columns = {'images.picture_url':'images', 'review_scores.review_scores_rating':'review_scores'}, inplace = True)
    
        # null value handling
        df_p['bedrooms'].fillna(0, inplace=True)
        df_p['beds'].fillna(0, inplace=True)
        df_p['bathrooms'].fillna(0, inplace=True)
        df_p['cleaning_fee'].fillna('Not Specified', inplace=True)
        df_p['review_scores'].fillna(0, inplace=True)
        
        # data types conversion
        df_p['minimum_nights'] = df_p['minimum_nights'].astype(int)
        df_p['maximum_nights'] = df_p['maximum_nights'].astype(int)
        df_p['bedrooms'] = df_p['bedrooms'].astype(int)
        df_p['beds'] = df_p['beds'].astype(int)
        df_p['bathrooms'] = df_p['bathrooms'].astype(str).astype(float)
        df_p['price'] = df_p['price'].astype(str).astype(float).astype(int)
        #df_p['cleaning_fee'] = df_p['cleaning_fee'].apply(lambda x: int(float(str(x))) if x != 'Not Specified' else 'Not Specified')
        df_p['extra_people'] = df_p['extra_people'].astype(str).astype(float).astype(int)
        df_p['guests_included'] = df_p['guests_included'].astype(int)
        
        return df_p

    def host_table(df):
        columns_host =['_id','host.host_id', 'host.host_url', 'host.host_name', 'host.host_location', 'host.host_response_time', 'host.host_thumbnail_url','host.host_picture_url', 'host.host_neighbourhood','host.host_response_rate', 'host.host_is_superhost','host.host_has_profile_pic', 'host.host_identity_verified','host.host_listings_count', 'host.host_total_listings_count', 'host.host_verifications']
        df_host = extract_data(df,columns_host)
        df_host.rename(columns = {'host.host_id':'host_id', 
                                  'host.host_url':'host_url',
                                  'host.host_name':'host_name', 
                                  'host.host_location':'host_location', 
                                  'host.host_response_time':'host_response_time', 
                                  'host.host_thumbnail_url':'host_thumbnail_url',
                                  'host.host_picture_url':'host_picture_url', 
                                  'host.host_neighbourhood':'host_neighbourhood',
                                  'host.host_response_rate':'host_response_rate', 
                                  'host.host_is_superhost':'host_is_superhost',
                                  'host.host_has_profile_pic':'host_has_profile_pic', 
                                  'host.host_identity_verified':'host_identity_verified',
                                  'host.host_listings_count':'host_listings_count', 
                                  'host.host_total_listings_count':'host_total_listings_count', 
                                  'host.host_verifications':'host_verifications'}, inplace = True)
        # null value handling
        df_host['host_response_time'].fillna('Not Specified', inplace=True)
        df_host['host_response_rate'].fillna(0, inplace=True)
        # data type conversion
        df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False: 'No', True: 'Yes'})
        df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False: 'No', True: 'Yes'})
        df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False: 'No', True: 'Yes'})

        return df_host

    def address_table(df):
        columns_address =['_id', 'address.street', 'address.suburb','address.government_area', 'address.market', 'address.country','address.country_code', 'address.location.type','address.location.coordinates', 'address.location.is_location_exact']
        df_address = extract_data(df,columns_address)
        df_address.rename(columns = {'address.street':'street', 
                                  'address.suburb':'suburb',
                                  'address.government_area':'government_area', 
                                  'address.market':'market', 
                                  'address.country':'country',
                                  'address.country_code':'country_code',
                                  'address.location.type':'location_type',
                                  'address.location.coordinates':'coordinates',
                                  'address.location.is_location_exact':'is_location_exact'
                                    }, inplace = True)
        # creating longitude & latitude from coordinates column
        df_address['longitude'] = df_address.apply(lambda row: row['coordinates'][0], axis = 1) 
        df_address['latitude'] = df_address.apply(lambda row: row['coordinates'][1], axis = 1) 
    
        return df_address

    def availability_table(df):
        columns_availability =['_id', 'availability.availability_30', 'availability.availability_60','availability.availability_90', 'availability.availability_365']
        df_avail = extract_data(df,columns_availability)
        df_avail.rename(columns = {'availability.availability_30':'availability_30', 
                                     'availability.availability_60':'availability_60',
                                     'availability.availability_90':'availability_90', 
                                     'availability.availability_365':'availability_365',
                                    }, inplace = True)
        return df_avail

    
        
    def amenities_table(df):
        def amenities_sort(x):
            a = x
            a.sort(reverse=False)
            return a
        
        columns_amenities =['_id','amenities']
        df_amenities = extract_data(df,columns_amenities)
        df_amenities['amenities'] = df_amenities['amenities'].apply(lambda x: amenities_sort(x))
        return df_amenities

    def load_dataframe():
        df = preprocessing.load_json()
        df_p= preprocessing.parentTable(df)
        df_host=preprocessing.host_table(df)
        df_address=preprocessing.address_table(df)
        df_avail=preprocessing.availability_table(df)
        df_amenities = preprocessing.amenities_table(df)
        df_main = pd.merge(df_p, df_host, on='_id')
        df_main = pd.merge(df_main, df_address, on='_id')
        df_main = pd.merge(df_main, df_avail, on='_id')
        df_main = pd.merge(df_main, df_amenities, on='_id')
        return df_main

class plotly:

    def pie_chart(df, x, y, title, title_x=0.20):
        fig = px.pie(df, names=x, values=y, hole=0.5, title=title)
        fig.update_layout(title_x=title_x, title_font_size=22)
        fig.update_traces(text=df[y], textinfo='percent+value',
                          textposition='outside',
                          textfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)

    def horizontal_bar_chart(df, x, y, text, color, title, title_x=0.25):
        fig = px.bar(df, x=x, y=y, labels={x: '', y: ''}, title=title)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_layout(title_x=title_x, title_font_size=22)
        text_position = ['inside' if val >= max(
            df[x]) * 0.75 else 'outside' for val in df[x]]
        fig.update_traces(marker_color=color,
                          text=df[text],
                          textposition=text_position,
                          texttemplate='%{x}<br>%{text}',
                          textfont=dict(size=14),
                          insidetextfont=dict(color='white'),
                          textangle=0,
                          hovertemplate='%{x}<br>%{y}')
        st.plotly_chart(fig, use_container_width=True)

    def vertical_bar_chart(df, x, y, text, color, title, title_x=0.25):
        fig = px.bar(df, x=x, y=y, labels={x: '', y: ''}, title=title)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_layout(title_x=title_x, title_font_size=22)
        text_position = ['inside' if val >= max(df[y]) * 0.90 else 'outside' for val in df[y]]
        fig.update_traces(marker_color=color,
                          text=df[text],
                          textposition=text_position,
                          texttemplate='%{y}<br>%{text}',
                          textfont=dict(size=14),
                          insidetextfont=dict(color='white'),
                          textangle=0,
                          hovertemplate='%{x}<br>%{y}'
                          )

        st.plotly_chart(fig, use_container_width=True, height=100)

    def line_chart(df, x, y, text, textposition, color, title, title_x=0.25):
        fig = px.line(df, x=x, y=y, labels={
                      x: '', y: ''}, title=title, text=df[text])
        fig.update_layout(title_x=title_x, title_font_size=22)
        fig.update_traces(line=dict(color=color, width=3.5),
                          marker=dict(symbol='diamond', size=10),
                          texttemplate='%{x}<br>%{text}',
                          textfont=dict(size=13.5),
                          textposition=textposition,
                          hovertemplate='%{x}<br>%{y}')
        st.plotly_chart(fig, use_container_width=True, height=100)

class feature:

    def feature(df,column_name):

        #df_f= df_main.groupby([column_name]).size().reset_index(name='count').sort_values(ascending=False)
        df_f= df_main.groupby([column_name]).size().reset_index(name='count').sort_values(by = 'count',ascending=False)
        df_f = df_f.head(10)

        #i = [i for i in range(1, len(s)+1)]
        data = pd.DataFrame(df_f, columns=[column_name, 'count'])
        data = data.rename_axis('S.No')
        data.index = data.index.map(lambda x: '{:^{}}'.format(x, 10))
        data['percentage'] = data['count'].apply(lambda x: str('{:.2f}'.format(x/55.55)) + '%')
        data['y'] = data[column_name].apply(lambda x: str(x)+'`')
        return data
    
    def feature_analysis(df_main):
        property_type = feature.feature(df_main,'property_type')
        plotly.vertical_bar_chart(df=property_type, x='property_type', y='count',text='percentage', color='#ff5a5f', title='Property Type', title_x=0.43)

        # line & pie chart
        
        bed_type = feature.feature(df_main,'bed_type')
        plotly.line_chart(df=bed_type, y='bed_type', x='count', text='percentage', color='#6e6e6e',
                            textposition=[
                                'top center', 'bottom center', 'middle right', 'middle right', 'middle right'],
                            title='Bed Type', title_x=0.50)
    
        room_type = feature.feature(df_main,'room_type')
        plotly.pie_chart(df=room_type, x='room_type',
                            y='count', title='Room Type', title_x=0.30)

        # vertical_bar chart
        tab1, tab2 = st.tabs(['Minimum Nights', 'Maximum Nights'])
        with tab1:
            minimum_nights = feature.feature(df_main,'minimum_nights')
            plotly.vertical_bar_chart(df=minimum_nights, x='y', y='count', text='percentage',
                                      color='#ff0c13', title='Minimum Nights', title_x=0.43)
        with tab2:
            maximum_nights = feature.feature(df_main,'maximum_nights')
            plotly.vertical_bar_chart(df=maximum_nights, x='y', y='count', text='percentage',
                                      color='#ff8185', title='Maximum Nights', title_x=0.43)

        # line chart
        cancellation_policy = feature.feature(df_main,'cancellation_policy')
        plotly.line_chart(df=cancellation_policy, y='cancellation_policy', x='count', text='percentage', color='#505050',
                          textposition=['top center', 'top right',
                                        'top center', 'bottom center', 'middle right'],
                          title='Cancellation Policy', title_x=0.43)

        # vertical_bar chart
        accommodates = feature.feature(df_main,'accommodates')
        plotly.vertical_bar_chart(df=accommodates, x='y', y='count', text='percentage',
                                  color='#767676', title='Accommodates', title_x=0.43)

        # vertical_bar chart
        tab1, tab2, tab3 = st.tabs(['Bedrooms', 'Beds', 'Bathrooms'])
        with tab1:
            bedrooms = feature.feature(df_main,'bedrooms')
            plotly.vertical_bar_chart(df=bedrooms, x='y', y='count', text='percentage',
                                      color='#ff0e15', title='Bedrooms', title_x=0.43)
        with tab2:
            beds = feature.feature(df_main,'beds')
            plotly.vertical_bar_chart(df=beds, x='y', y='count', text='percentage',
                                      color='#ff5a5f', title='Beds', title_x=0.43)
        with tab3:
            bathrooms = feature.feature(df_main,'bathrooms')
            plotly.vertical_bar_chart(df=bathrooms, x='y', y='count', text='percentage',
                                      color='#ffa7a9', title='Bathrooms', title_x=0.43)



 # page configuration
    page_icon_url = 'C:/Users/RUDRA/project/capstone4/p1.png'
    st.set_page_config(page_title='Airbnb',
                       page_icon=page_icon_url, layout="wide")

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">Airbnb Analysis</h1>',
                unsafe_allow_html=True)
    
st.write('')


with st.sidebar:
    image_url = 'https://raw.githubusercontent.com/gopiashokan/Airbnb-Analysis/main/airbnb_banner.jpg'
    st.image(image_url, use_column_width=True)

#loading data
df_main = preprocessing.load_dataframe()


#with st.headbar:
SELECT = option_menu(
    menu_title = None,
    options = ["Availability","Features Charts","Host Analysis","Price Analysis","Geospatial Map"],
    icons =["house","bar-chart","person-lines-fill","currency-exchange","map"],
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},
            
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#969696"},
        "nav-link-selected": {"background-color": "#505050"}})

if SELECT == 'Features Charts':
        st.markdown("### :red[TOP 10 in each Features]")

        feature.feature_analysis(df_main)

if SELECT == 'Price Analysis':
        df =df_main
        st.markdown("### :red[PRICE DIFFERENCE]")

        col1,col2= st.columns(2)

        with col1:
            
            
            country= st.selectbox("Select the Country",df["country"].unique())

            df1= df[df["country"] == country]
            df1.reset_index(drop= True, inplace= True)

            room_ty= st.selectbox("Select the Room Type",df1["room_type"].unique())
            
            df2= df1[df1["room_type"] == room_ty]
            df2.reset_index(drop= True, inplace= True)

            df_bar= pd.DataFrame(df2.groupby("property_type")[["price","review_scores","number_of_reviews"]].sum())
            df_bar.reset_index(inplace= True)

            fig_bar= px.bar(df_bar, x='property_type', y= "price", title= "PRICE FOR PROPERTY_TYPES",hover_data=["number_of_reviews","review_scores"],color_discrete_sequence=px.colors.sequential.Peach, width=600, height=500)
            st.plotly_chart(fig_bar)

        
        with col2:
            
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
     
            proper_ty= st.selectbox("Select the Property_type",df2["property_type"].unique())

            df4= df2[df2["property_type"] == proper_ty]
            df4.reset_index(drop= True, inplace= True)

            df_pie= pd.DataFrame(df4.groupby("host_response_time")[["price","bedrooms"]].sum())
            df_pie.reset_index(inplace= True)

            fig_pi= px.pie(df_pie, values="price", names= "host_response_time",
                            hover_data=["bedrooms"],
                            color_discrete_sequence=px.colors.sequential.RdPu_r,
                            title="PRICE DIFFERENCE BASED ON HOST RESPONSE TIME",
                            width= 600, height= 500)
            st.plotly_chart(fig_pi)

        col1,col2= st.columns(2)

        with col1:

            
            hostresponsetime= st.selectbox("Select the host_response_time",df4["host_response_time"].unique())

            df5= df4[df4["host_response_time"] == hostresponsetime]

            df_do_bar= pd.DataFrame(df5.groupby("bed_type")[["minimum_nights","maximum_nights","price"]].sum())
            df_do_bar.reset_index(inplace= True)

            fig_do_bar = px.bar(df_do_bar, x='bed_type', y=['minimum_nights', 'maximum_nights'], 
            title='MINIMUM NIGHTS AND MAXIMUM NIGHTS',hover_data="price",
            barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow, width=600, height=500)
            

            st.plotly_chart(fig_do_bar)

        with col2:

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            df_do_bar_2= pd.DataFrame(df5.groupby("bed_type")[["bedrooms","beds","accommodates","price"]].sum())
            df_do_bar_2.reset_index(inplace= True)

            fig_do_bar_2 = px.bar(df_do_bar_2, x='bed_type', y=['bedrooms', 'beds', 'accommodates'], 
            title='BEDROOMS AND BEDS ACCOMMODATES',hover_data="price",
            barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow_r, width= 600, height= 500)
           
            st.plotly_chart(fig_do_bar_2)



if SELECT == 'Geospatial Analysis':

        st.write('')

        fig_4 = px.scatter_mapbox(df_main, lat='latitude', lon='longitude', color='price', size='accommodates',
                        color_continuous_scale= "rainbow",hover_name='name',range_color=(0,49000), mapbox_style="carto-positron",
                        zoom=1)
        fig_4.update_layout(width=1150,height=800,title='Geospatial Distribution of Listings')
        st.plotly_chart(fig_4)   

        #col1, col2, col3 = st.columns(3)
        #with col1:
           # countries_list = host.countries_list()
            #country = st.selectbox(label='Country', options=countries_list)
        #if country:
         #   host.host_analysis()

if SELECT == 'Host Analysis':
        df_l= df_main

        country_l= st.selectbox("Select the Country",df_l["country"].unique())

        df1_l= df_l[df_l["country"] == country_l]
        df1_l.reset_index(drop= True, inplace= True)

        proper_ty_l= st.selectbox("Select the Property_type",df1_l["property_type"].unique())

        df2_l= df1_l[df1_l["property_type"] == proper_ty_l]
        df2_l.reset_index(drop= True, inplace= True)

        st.write("")

        def select_the_df(sel_val):
            if sel_val == str(df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.25 + df2_l['price'].min())+' '+str("(> 25%)"):

                df_val_25= df2_l[df2_l["price"] <= differ_max_min*0.25 + df2_l['price'].min()]
                df_val_25.reset_index(drop= True, inplace= True)
                return df_val_25

            elif sel_val == str(differ_max_min*0.25 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.50 + df2_l['price'].min())+' '+str("(25% to 50%)"):
            
                df_val_50= df2_l[df2_l["price"] >= differ_max_min*0.25 + df2_l['price'].min()]
                df_val_50_1= df_val_50[df_val_50["price"] <= differ_max_min*0.50 + df2_l['price'].min()]
                df_val_50_1.reset_index(drop= True, inplace= True)
                return df_val_50_1
            
            elif sel_val == str(differ_max_min*0.50 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.75 + df2_l['price'].min())+' '+str("(25% to 50%)"):
            
                df_val_75= df2_l[df2_l["price"] >= differ_max_min*0.50 + df2_l['price'].min()]
                df_val_75_1= df_val_75[df_val_75["price"] <= differ_max_min*0.75 + df2_l['price'].min()]
                df_val_75_1.reset_index(drop= True, inplace= True)
                return df_val_75_1
            
            elif sel_val == str(differ_max_min*0.75 + df2_l['price'].min())+' '+str('to')+' '+str(df2_l['price'].max())+' '+str("(< 75%)"):

                df_val_100= df2_l[df2_l["price"] >= differ_max_min*0.75 + df2_l['price'].min()]
                df_val_100.reset_index(drop= True, inplace= True)
                return df_val_100
            
        differ_max_min= df2_l['price'].max()-df2_l['price'].min()

        val_sel= st.radio("Select the Price Range",[str(df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.25 + df2_l['price'].min())+' '+str("(> 25%)"),                            
                                                    str(differ_max_min*0.25 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.50 + df2_l['price'].min())+' '+str("(25% to 50%)"),
                                                    str(differ_max_min*0.50 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.75 + df2_l['price'].min())+' '+str("(50% to 75%)"),
                                                    str(differ_max_min*0.75 + df2_l['price'].min())+' '+str('to')+' '+str(df2_l['price'].max())+' '+str("(< 75%)")])
                                          
        df_val_sel= select_the_df(val_sel)

        st.dataframe(df_val_sel)

        # checking the correlation


        df_val_sel_gr= pd.DataFrame(df_val_sel.groupby("accommodates")[["bedrooms","beds","extra_people"]].sum())
        df_val_sel_gr.reset_index(inplace= True)

        fig_1= px.bar(df_val_sel_gr, x="accommodates", y= ["bedrooms","beds"], title="ACCOMMODATES",
                    hover_data= "extra_people", barmode='group', color_discrete_sequence=px.colors.sequential.Sunset,width=1000)
        st.plotly_chart(fig_1)
        
        
        room_ty_l= st.selectbox("Select the Room Type", df_val_sel["room_type"].unique())

        df_val_sel_rt= df_val_sel[df_val_sel["room_type"] == room_ty_l]

        fig_2= px.bar(df_val_sel_rt, x= ["street","host_location","host_neighbourhood"],y="market", title="MARKET",
                    hover_data= ["name","host_name","market"], barmode='group',orientation='h', color_discrete_sequence=px.colors.sequential.Sunset,width=1000)
        st.plotly_chart(fig_2)

        fig_3= px.bar(df_val_sel_rt, x="government_area", y= ["host_is_superhost","host_neighbourhood","cancellation_policy"], title="GOVERNMENT_AREA",
                    hover_data= ["guests_included","location_type"], barmode='group', color_discrete_sequence=px.colors.sequential.Sunset,width=1000)
        st.plotly_chart(fig_3)

if SELECT == 'Availability':
        
        df_a= df_main
        df=df_main

        st.title("**AVAILABILITY ANALYSIS**")
        col1,col2= st.columns(2)

        with col1:
            
            
            country_a= st.selectbox("Select the Country",df_a["country"].unique())

            df1_a= df[df["country"] == country_a]
            df1_a.reset_index(drop= True, inplace= True)

            property_ty_a= st.selectbox("Select the Property Type",df1_a["property_type"].unique())
            
            df2_a= df1_a[df1_a["property_type"] == property_ty_a]
            df2_a.reset_index(drop= True, inplace= True)

            roomtype_a= st.selectbox("Select the Room Type", df2_a["room_type"].unique())

            df3_a= df2_a[df2_a["room_type"] == roomtype_a]

            df_a_sunb_30= px.sunburst(df2_a, path=["room_type","bed_type"], values="availability_30",width=600,height=500,title="Availability_30",color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(df_a_sunb_30)
        
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            

            df_a_sunb_60= px.sunburst(df2_a, path=["room_type","bed_type"], values="availability_60",width=600,height=500,title="Availability_60",color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(df_a_sunb_60)

        col1,col2= st.columns(2)

        with col1:
            
            df_a_sunb_90= px.sunburst(df2_a, path=["room_type","bed_type"], values="availability_90",width=600,height=500,title="Availability_90",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
            st.plotly_chart(df_a_sunb_90)

        with col2:

            df_a_sunb_365= px.sunburst(df2_a, path=["room_type","bed_type"], values="availability_365",width=600,height=500,title="Availability_365",color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(df_a_sunb_365)
        


        df_mul_bar_a= pd.DataFrame(df3_a.groupby("host_response_time")[["availability_30","availability_60","availability_90","availability_365"]].sum())
        df_mul_bar_a.reset_index(inplace= True)

        fig_df_mul_bar_a = px.bar(df_mul_bar_a, x='host_response_time', y=['availability_30', 'availability_60', 'availability_90', "availability_365"], 
        title='AVAILABILITY BASED ON HOST RESPONSE TIME',hover_data="host_response_time",
        color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1000)

        st.plotly_chart(fig_df_mul_bar_a)

    

