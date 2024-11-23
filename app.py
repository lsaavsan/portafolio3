import streamlit as st
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import plotly.express as px

# carga el archivo
df_unido = pd.read_excel('dataunida.xlsx')

# Definir colores personalizados para cada modalidad
unique_modalities = df_unido['Modalidad'].unique()
unique_ciclo = sorted(df_unido['Ciclo'].unique(), reverse=True)
#unique_carrera = sorted(df_unido['Carrera'].unique())


palette = sns.color_palette('Set1', len(unique_modalities))  # Paleta de colores distintivos
color_dict = dict(zip(unique_modalities, [f'rgb({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})' for c in palette]))

# Configurar la aplicación de Streamlit
st.title('Agrupamiento de Alumnos por PPA y Modalidad de Ingreso')

# Selector de modalidad
selected_modality = st.sidebar.selectbox('Seleccione la modalidad para visualizar el gráfico:', unique_modalities,key='select_modality')
# Selector de ciclo
selected_ciclo = st.sidebar.selectbox('Seleccione el ciclo para visualizar el gráfico:', unique_ciclo,key='select_ciclo')
# Selector de carrera
#selected_carrera = st.sidebar.selectbox('Seleccione la modalidad para visualizar el gráfico:', unique_carrera)



# Filtrar los datos según la modalidad seleccionada
subset = df_unido[(df_unido['Modalidad'] == selected_modality) & (df_unido['Ciclo'] == selected_ciclo)]# & (df_unido['Carrera'] == selected_carrera)]
color = color_dict[selected_modality]

# Crear el gráfico para la modalidad seleccionada
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=subset['PPA'],
        y=subset['Cluster'],
        mode='markers',
        marker=dict(color=color, size=8),
        name=selected_modality
    )
)

# Ajustar el diseño del gráfico
fig.update_layout(
    title_text=f'Grupos de Alumnos por PPA del semestre {selected_ciclo} y Modalidad de Ingreso: {selected_modality}',
    xaxis_title='PPA',
    yaxis_title='Cluster',
    yaxis=dict(
        range=[-0.5, 9],      # Rango fijo de 0 a 8
        tickmode='linear',  # Modo de ticks lineales
        dtick=1             # Intervalo de uno
    ),
    template='plotly_white'
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

st.markdown("""____""")

dfx=pd.read_excel('dataunida.xlsx')


# Agrupación y cálculo de rangos
result = dfx[(dfx['Ciclo'] == selected_ciclo)&(dfx['Modalidad'] == selected_modality)&(dfx['PPA'] <10.5)].groupby(['Modalidad', 'Cluster']).agg(
    min_PPA=('PPA', 'min'),
    max_PPA=('PPA', 'max'),
    count_PPA=('PPA', 'count')
).reset_index()

# Crear una columna para la leyenda personalizada
result['Cluster_Range'] = result.apply(
    lambda row: f"Cluster {row['Cluster']}: {row['min_PPA']:.2f}-{row['max_PPA']:.2f}", axis=1
)

# Crear el gráfico
fig = px.bar(
    result,
    x='Modalidad',
    y='count_PPA',
    color='Cluster_Range',  # Usamos la columna de rango como color
    text='count_PPA',
    title=f'Distribución de Clusters por Modalidad:{selected_modality} en el semestre {selected_ciclo} <br> con Rango de PPA menor a 10.5',
    labels={'count_PPA': 'Cantidad de PPA', 'Modalidad': 'Modalidad de Ingreso'}
)

# Ajustar diseño
fig.update_layout(
    width=1000,  # Ancho del gráfico
    height=800,  # Altura del gráfico
    legend_title_text='Cluster y Rango de PPA',
    xaxis_title='Modalidad de Ingreso',
    yaxis_title='Cantidad de PPA',
    xaxis=dict(
        tickangle=0  # Rotar etiquetas 90 grados
    )
)

# Mostrar el gráfico
st.plotly_chart(fig)
st.markdown("""____""")
# Agrupación y cálculo de rangos
result = dfx[(dfx['Ciclo'] == selected_ciclo)&(dfx['Modalidad'] == selected_modality)&(dfx['PPA'] >=10.5)].groupby(['Modalidad', 'Cluster']).agg(
    min_PPA=('PPA', 'min'),
    max_PPA=('PPA', 'max'),
    count_PPA=('PPA', 'count')
).reset_index()

# Crear una columna para la leyenda personalizada
result['Cluster_Range'] = result.apply(
    lambda row: f"Cluster {row['Cluster']}: {row['min_PPA']:.2f}-{row['max_PPA']:.2f}", axis=1
)

# Crear el gráfico
fig = px.bar(
    result,
    x='Modalidad',
    y='count_PPA',
    color='Cluster_Range',  # Usamos la columna de rango como color
    text='count_PPA',
    title=f'Distribución de Clusters por Modalidad:{selected_modality} en el semestre {selected_ciclo} <br> con Rango de PPA mayor o igual a 10.5',
    labels={'count_PPA': 'Cantidad de PPA', 'Modalidad': 'Modalidad de Ingreso'}
)

# Ajustar diseño
fig.update_layout(
    width=1000,  # Ancho del gráfico
    height=800,  # Altura del gráfico
    legend_title_text='Cluster y Rango de PPA',
    xaxis_title='Modalidad de Ingreso',
    yaxis_title='Cantidad de PPA',
    xaxis=dict(
        tickangle=0  # Rotar etiquetas 90 grados
    )
)

# Mostrar el gráfico
st.plotly_chart(fig)