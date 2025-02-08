import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#DATAFRAME PREPARATION
def create_cust_seasons_df(df):
    cust_seasons_df = df.groupby('season').cnt.sum().sort_values(ascending=True).reset_index()

    return cust_seasons_df

def create_temp_seasons_df(df):
    temp_seasons_df = df.groupby('season').temp.mean().sort_values(ascending=True).reset_index()
    temp_seasons_df['temp'] = temp_seasons_df['temp']*41
    return temp_seasons_df

def create_cust_hour_df(df):
    cust_hour_df = df.groupby('hr').cnt.sum().reset_index()

    return cust_hour_df

#LOAD DATA SET YANG DIGUNAKAN
hours_df = pd.read_csv("hours_data.csv")

#MEMBUAT FILTER TAHUN

with st.sidebar:
    st.image('logo.png')

    #MEMBUAT FILTER TAHUN
    tahun_map={0: 2021, 1: 2022}
    hours_df['yr'] = hours_df['yr'].map(tahun_map)

    tahun_pilihan = hours_df['yr'].unique()
    tahun_pilihan = st.selectbox('Pilih Tahun', tahun_pilihan)

    # Filter data berdasarkan tahun yang dipilih
    filter_tahun_df = hours_df[hours_df['yr'] == tahun_pilihan]

cust_seasons_df = create_cust_seasons_df(filter_tahun_df)
temp_seasons_df = create_temp_seasons_df(filter_tahun_df)
cust_hour_df = create_cust_hour_df(filter_tahun_df)

#DASHBOARD
st.header(":bike: Bike Sharing Dashboard :bike: \n")

st.subheader("Jumlah Pengguna Berdasarkan Musim")
# Peta musim
musim_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
cust_seasons_df['season'] = cust_seasons_df['season'].map(musim_map)

# Mengurutkan data
cust_seasons_df = cust_seasons_df.sort_values(by="cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=cust_seasons_df, ax=ax)
plt.xlabel('Musim')
plt.ylabel('Jumlah Pengguna')
plt.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

with st.expander("see details"):
    st.write(
        """
        Musim gugur menjadi musim dimana jasa Bike Sharing
        mendapat paling banyak pengguna, sedangkan untuk jumlah pengguna paling sedikit 
        terjadi pada musim semi.
        """
    )


st.text("Setelah ditelusuri, ternyata hasil ini selaras dengan suhu rata-rata pada musim tersebut")
    
st.subheader("Rata-Rata Suhu Harian Setiap Musim")
temp_seasons_df['season'] = temp_seasons_df['season'].map(musim_map)
temp_seasons_df = temp_seasons_df.sort_values(by='temp', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='temp', data=temp_seasons_df, ax=ax)
plt.xlabel('Musim')
plt.ylabel('Suhu °C')
plt.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

with st.expander("see details"):
    st.write(
        """
        Musim gugur menjadi musim dimana jasa Bike Sharing mendapat paling banyak pengguna, 
        sedangkan untuk jumlah pengguna paling sedikit terjadi pada musim semi. 
        Hal ini dapat terjadi karena pada musim semi, 
        suhu rata-rata tiap harinya lebih rendah dari tiga musim lainnya, 
        bahkan lebih rendah dari musim dingin.
        """
    )

st.subheader("Jumlah Pengguna Tiap Jam Setiap Hari")

fig, ax= plt.subplots(figsize=(10,6))
plt.plot(cust_hour_df.index, cust_hour_df['cnt'], marker='o')
plt.xlabel('Jam')
plt.ylabel('Jumlah Pengguna')
plt.grid(True)
st.pyplot(fig)

with st.expander("see details"):
    st.write(
        """
        Peningkatang pengguna paling signifikan terjadi pada 2 waktu, yaitu pada jam 08:00 dan 17:00. 
        yang dimana pada jam tersebut merupakan waktu orang-orang berangkat dan pulang kerja.
        """
    )


st.subheader(
    """
    Kesimpulan dan Saran Strategis :sparkles:
    1. Musim gugur menjadi musim dimana jasa bike sharing mendapat paling banyak pengguna, sedangkan untuk jumlah pengguna paling sedikit terjadi pada musim semi. Hal ini dapat terjadi karena pada musim semi, suhu rata-rata tiap harinya lebi rendah dari tiga musim lainnya, bahkan lebih rendah dari musim dingin.
    2. Terkait dengan jumlah pengguna pada musim-musim tertentu, saat terjadi puncak jumlah pengguna pada musim gugur, agar menarik lebih banyak pengguna dapat diadakan paket berlangganan bulanan yang relatif lebih murah. Sedangkan untuk menangani jumlah pengguna paling sedikit pada musim semi, dapat disediakan promo berupa fasilitas pemanas tubuh ynag dapat digunakan dalam berkendara menggunakan sepeda atau voucher free hot drink bagi pengguna.

    3. Peningkatang pengguna paling signifikan terjadi pada 2 waktu, yaitu pada 08:00 dan 17:00. yang dimana pada jam tersebut merupakan waktu orang-orang berangkat dan pulang kerja.
    4. Untuk peningkatan pengguna saat jam-jam sibuk, tentu perlu diantisipasi dengan menambah pengalokasian armada terutama di sekitar daerah perkantoran dan penempatan stasiun bike sharing yang strategis, seperti dekat dengan transportasi umum lain, agar pengguna dapat lebih mudah jika ingin melakukan perjalanan yg memerlukan beberapa moda transportasi.
    """
)