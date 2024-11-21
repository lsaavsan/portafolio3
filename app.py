import streamlit as st
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd

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
    title_text=f'Agrupamiento de Alumnos por PPA y Modalidad de Ingreso: {selected_modality}',
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
