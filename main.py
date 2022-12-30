"""
Tugas Besar Visualisasi Data

Oleh:
- Muhammad Tsaqif Ammar (1301194222)
- Butrahandisya (1301190206)
- Vincentius Arnold Fridolin (1301190221)
"""

# Import libraries
import pandas as pd
import itertools
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import Column, ColumnDataSource
from bokeh.models.widgets import TextInput, Select, CheckboxButtonGroup
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from math import pi
import warnings
warnings.filterwarnings("ignore")

# Import data
dataset_path = './data_covid_indonesia.csv'
df = pd.read_csv(dataset_path)
df['tanggal'] = pd.to_datetime(df['tanggal'])

# Fungsi untuk mendapatkan data berdasarkan bulan, tahun, dan banyak provinsi yang ditampilkan
def get_data(month='1', year='2022', show_count='20'):
    month, year, show_count = int(month), int(year), int(show_count)
    show_count -= 1

    # Filter berdasarkan parameter
    df_filtered = df[(df['tanggal'].dt.month == month) & (df['tanggal'].dt.year == year)]

    # Mengelompokkan beberapa provinsi terakhir menjadi satu yaitu 'Lainnya'
    x = df_filtered.groupby('PROVINSI').sum()['KASUS'].to_dict()
    x = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))
    top = dict(itertools.islice(x.items(), show_count))
    top['Lainnya'] = sum(dict(list(x.items())[show_count:]).values())

    # Menghitung derajat dari masing-masing provinsi pada pie chart
    data = pd.Series(top).reset_index(name='value').rename(columns={'index': 'provinsi'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(top)]
    return data

source = ColumnDataSource(data=get_data())

# Membuat Widget (bulan, tahun, dan banyak provinsi yang ditampilkan)
month_options = [str(i) for i in range(1, 13)]
month = Select(title='Bulan', value='1', options=month_options)

year_options = ['2020', '2021', '2022']
year = Select(title='Tahun', value='2022', options=year_options)

show_count_options = [str(i) for i in range(3, 21)]
show = Select(title='Banyak Provinsi', value='20', options=show_count_options)

# Plot figure dari pie chart nya
p = figure(title="Persebaran Kasus COVID di Indonesia", toolbar_location="below",
           tools="hover", tooltips="@provinsi: @value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='provinsi', source=source)

p.sizing_mode = 'scale_height'
p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

# Callback untuk meng-update data berdasarkan interaksi user
def update_data(attrname, old, new):
    source.data = get_data(month.value, year.value, show.value)

month.on_change('value', update_data)
year.on_change('value', update_data)
show.on_change('value', update_data)

# Tambah plot dan widgets ke halaman
inputs = Column(month, year, show)
curdoc().add_root(row(children=[p, inputs], sizing_mode='stretch_both'))
curdoc().title = 'Final Project - Visualisasi Data'
curdoc().theme = 'caliber'