

import pandas as pd

import requests

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import json

import locale

locale.setlocale(locale.LC_ALL, '')

# app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/uditagarwal/pen/oNvwKNP.css'])
# app = dash.Dash(__name__, external_stylesheets=['https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-oil-and-gas/assets/styles.css'])
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'])
token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'


def get_rows(str_query=None):
    response = requests.post("http://ec2-3-133-150-215.us-east-2.compute.amazonaws.com:8020/raw_query",
                             json={"raw_query": str_query})
    return response.json()


def fetch_series(dfx, series_name):
    series_name = dfx[series_name]
    return series_name


with open('Colombia_Transformado.json') as f:
    geojson = json.loads(f.read())

df_correc = pd.read_csv('df_colombia.csv')

df_correc['DPTO'] = df_correc['DPTO'].apply(lambda x: '{0:0>3}'.format(x))
df_correc['MPIO'] = df_correc['MPIO'].apply(lambda x: '{0:0>3}'.format(x))
df_correc['COD_DANE'] = df_correc['DPTO'].astype(str) + df_correc['MPIO'].astype(str)

df_areas = get_rows("select * from areas where activo is true order by area")
df_areas = pd.DataFrame.from_dict(df_areas['data']['table'])


def download_dict_api(dict_name=None):
    r = requests.get('http://ec2-3-133-150-215.us-east-2.compute.amazonaws.com:8020/factors/' + dict_name)
    r = pd.DataFrame.from_dict(r.json()['data']['topics'])
    index_col_name = r.columns[0]
    r = r.set_index(index_col_name)
    return r


marital_status = download_dict_api(dict_name='marital_dict')
sex = download_dict_api(dict_name='sex_dict')
educational = download_dict_api(dict_name='education_dict')


def get_areas():
    df_areas2 = get_rows("select * from areas where activo is true")
    df_areas2 = pd.DataFrame.from_dict(df_areas2['data']['table'])
    return df_areas2


def create_radio_selector(sel_id=None, pandas_series=None):
    radio_selector = dcc.RadioItems(
        id=sel_id,
        options=[{'label': value, 'value': index} for index, value in pandas_series.items()],
        labelStyle={'display': 'inline-block'}
    )
    return radio_selector


def create_dropdown_selector(sel_id=None, pandas_series=None):
    dropdown_selector = dcc.Dropdown(
        id=sel_id,
        options=[{'label': value, 'value': index} for index, value in pandas_series.items()],
    )
    return dropdown_selector


def get_how_many():
    df_how_many = get_rows(
        "select round(sum(fex_c_2011)) from area_personas where mes=1 and area=11 and p6040 between 14 and 26")
    df_areas2 = pd.DataFrame.from_dict(df_areas2['data']['table'])
    return df_areas2


marital_select = create_dropdown_selector(sel_id='marital-select', pandas_series=marital_status['valor'])
sex_select = create_radio_selector(sel_id='sex-select', pandas_series=sex['valor'])
educational_select = create_dropdown_selector(sel_id='educational-select', pandas_series=educational['valor'])

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("colombia.png"),
                        id="team30-image",
                        style={
                            "height": "150px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                    ),
                ],
                className="three columns center",
            ),
            html.Div(
                [
                    html.H3(
                        "Cuántos Como Yo?",
                        style={"margin-bottom": "0px"},
                    ),
                    html.H5(
                        "Production Overview", style={"margin-top": "0px"}
                    ),
                ],
                className="six columns",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("mintic_nuevo.jpg"),
                                id="mintic-image",
                                style={
                                    "height": "150px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            ),
                        ],
                    ),

                ],
                className="two columns",
            )
        ],

    ),
    html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                children=[
                                    html.H6("Seleccione Municipio"),
                                    dcc.Dropdown(
                                        id="study-dropdown2",
                                        value='Bogotá',
                                        options=[{'label': label, 'value': label} for label in
                                                 df_areas['area'].unique()]
                                    )
                                ]
                            ),
                            html.H6(
                                "Seleccione un mes:",
                                className="control_label",
                            ),
                            dcc.Dropdown(
                                id='month-dropdown',
                                options=[
                                    {'label': 'Enero', 'value': '1'},
                                    {'label': 'Febrero', 'value': '2'},
                                    {'label': 'Marzo', 'value': '3'},
                                    {'label': 'Abril', 'value': '4'},
                                    {'label': 'Mayo', 'value': '5'},
                                    {'label': 'Junio', 'value': '6'},
                                    {'label': 'Julio', 'value': '7'},
                                    {'label': 'Agosto', 'value': '8'},
                                    {'label': 'Septiembre', 'value': '9'},
                                    {'label': 'Octubre', 'value': '10'},
                                    {'label': 'Noviembre', 'value': '11'},
                                    {'label': 'Diciembre', 'value': '12'}

                                ],
                                value='12'
                            ),
                            html.H6(
                                "Seleccione un rango de edad:",
                                className="control_label",
                            ),
                            dcc.RangeSlider(
                                id="age_slider",
                                min=18,
                                max=96,
                                marks={
                                    18: '18',
                                    26: '26',
                                    32: '32',
                                    40: '40',
                                    48: '48',
                                    56: '56',
                                    64: '64',
                                    72: '72',
                                    80: '80',
                                    88: '88',
                                    96: '96',
                                },
                                value=[10, 30],
                                className="dcc_control",
                            ),
                            html.Div(
                                children=[
                                    html.H6("Género:", className="control_label"),
                                    dcc.RadioItems(id='sex_radio',
                                                   options=[{'label': i, 'value': i} for i in ['Hombre', 'Mujer']],
                                                   value='Hombre')
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.H6("Nivel Educativo:", className="control_label"),

                                    dcc.Dropdown(
                                        id="educational_select",
                                        value='Bachiller',
                                        options=[{'label': label, 'value': label} for label in
                                                 educational['valor'].unique()]
                                    )
                                ]
                            ),

                        ],
                        id="cross-filter-options",
                    ),
                ],
                className="pretty_container three columns",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(children="Mapa de Colombia", style={'textAlign': 'center'}),
                            dcc.Graph(id='map-plot', figure={
                                'data': [go.Choroplethmapbox()],
                                'layout': go.Layout(
                                    mapbox_style="dark",
                                    mapbox_accesstoken=token,
                                    mapbox_zoom=5,
                                    margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                                    mapbox_center={"lat": 4.6109886, "lon": -74.072092}
                                )
                            }
                                      )
                        ],
                        className="pretty_container",
                    ),
                ],
                className="six columns",
            ),
            html.Div(
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Cuántos Como Yo?"),
                                    html.H6(
                                        id="how_many",
                                        className="info_text"
                                    )
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    html.H5("Cuántos Como Yo (Económicamente Activos)?"),
                                    html.H6(id="how_many_eco",
                                            className="info_text"),
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    html.H5("% Desempleo en Personas Como Yo"),
                                    html.H6(id="tasa_desem_comoyo",
                                            className="info_text"), ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    html.H5("% Desempleo en la Ciudad"),
                                    html.H6(id="tasa_desem_ciud",
                                            className="info_text"), ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    html.H5("Tiempo estimado para encontrar Empleo"),
                                    html.H6(id="tiempo_estimado_model",
                                            className="info_text"), ],
                                className="pretty_container",
                            ),
                        ],
                    ),
                ],
                className="three columns",
            )
        ],

    ),
    html.Div(
        className='twelve columns card 3 pretty_container',
        children=[
            html.H5("Ocupaciones con Mayor Tasa de Desempleo"),
            dcc.Graph(id="unemp_ocup"),
        ]
    ),
    html.Div(
        className='twelve columns card 3 pretty_container',
        children=[
            html.H5("Ingreso Promedio Por Ocupación"),
            dcc.Graph(id="ing_ocup"),
        ]
    ),
    html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id="barplot"),
                        ],
                        className="pretty_container",
                    ),
                ],
                className="six columns center",
            ),
            html.Div(
                [
                    dcc.Graph(id="barplot_oficio"),
                ],
                className="six columns",
            ),
        ],

    ),

])


def get_filtered_rows(municipios):
    df_areas_sel = get_areas()
    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]
    area_cod = area_selected.iloc[0]['area_cod']
    area_code = str(area_cod).zfill(3)
    data = df_correc[(df_correc['DPTO'] == area_code) & (df_correc['MPIO'] == '001')]
    return data


def info_por_municipio(municipios):
    data = []
    df = get_filtered_rows(municipios)
    data.append(go.Choroplethmapbox(
        geojson=geojson,
        locations=df['MPIOS'],
        z=df['DESEMPLEO'],
        colorscale='earth',
        text=df['NOMBRE_MPI'],
        colorbar_title="DESEMPLEO"
    ))
    return data


@app.callback(
    dash.dependencies.Output('map-plot', 'figure'),
    # component with id map-plot will be changed, the 'figure' argument is updated
    [
        dash.dependencies.Input('study-dropdown2', 'value'),
    ]
)
def actualizar_mapa(value):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == value]

    # print(area_selected)
    area_lat = area_selected.iloc[0]['latitude']
    area_lon = area_selected.iloc[0]['longitude']
    return {
        'data': info_por_municipio(value),
        'layout': go.Layout(
            mapbox_style="dark",
            mapbox_accesstoken=token,
            mapbox_zoom=7,
            margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
            mapbox_center={"lat": area_lat, "lon": area_lon}
        )
    }


@app.callback(
    dash.dependencies.Output('barplot', 'figure'),
    (
            dash.dependencies.Input('month-dropdown', 'value'),
    )
)
def update_barplot(month_value):
    x_name = 'Edad'
    y_name = 'Cantidad de personas'
    test_json = get_rows(
        "select ap.p6040 as \"Edad\", round(sum(fex_c_2011)) as \"Cantidad de personas\" from area_personas ap where mes=" + month_value + " group by ap.p6040")
    # test_json = get_rows("select ap.p6040 as \"Edad\", round(sum(fex_c_2011)) as \"Cantidad de personas\" from area_personas ap where mes=5 group by ap.p6040")
    df = pd.DataFrame.from_dict(test_json['data']['table'])

    series_x = fetch_series(df, x_name)
    series_y = fetch_series(df, y_name)

    series_plot = go.Bar(x=series_x, y=series_y)
    return {'data':
                [series_plot],
            'layout': {'title': 'Diagrama de barras de {} y {}'.format(x_name, y_name), },
            }


@app.callback(dash.dependencies.Output('how_many', 'children'),
              (
                      dash.dependencies.Input('month-dropdown', 'value'),
                      dash.dependencies.Input('study-dropdown2', 'value'),
                      dash.dependencies.Input('age_slider', 'value'),
              )
              )
def update_how_many(month_value, municipios, age_slider):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]

    # print(area_selected)
    area_cod = area_selected.iloc[0]['area_cod']
    # area_code = area_cod.astype(str).apply(lambda x: '{0:0>3}'.format(x))
    area_code = str(area_cod).zfill(3)
    sql_many = "select round(sum(fex_c_2011)) from area_personas where mes=" + month_value + " and area=" + area_code + " and p6040 between " + str(
        age_slider[0]) + " and " + str(age_slider[1]) + ""
    how_json = get_rows(sql_many)
    df = pd.DataFrame.from_dict(how_json['data']['table'])
    value = df['round']
    return "   Total: " + locale.format("%d", value, grouping=True)


@app.callback(dash.dependencies.Output('how_many_eco', 'children'),
              (
                      dash.dependencies.Input('month-dropdown', 'value'),
                      dash.dependencies.Input('study-dropdown2', 'value'),
                      dash.dependencies.Input('age_slider', 'value'),
              )
              )
def update_how_many_eco(month_value, municipios, age_slider):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]

    # print(area_selected)
    area_cod = area_selected.iloc[0]['area_cod']
    # area_code = area_cod.astype(str).apply(lambda x: '{0:0>3}'.format(x))
    area_code = str(area_cod).zfill(3)

    sql_many = "SELECT round(sum(fex_c_2011)) as \"PEA\" FROM view_ocupados_desocupados where mes=" + month_value + " and area=" + area_code + " and \"Edad\" between " + str(
        age_slider[0]) + " and " + str(age_slider[1]) + ""
    how_json = get_rows(sql_many)
    df = pd.DataFrame.from_dict(how_json['data']['table'])
    value = df['PEA']
    return "   Total: " + locale.format("%d", value, grouping=True)


@app.callback(dash.dependencies.Output('tasa_desem_ciud', 'children'),
              (
                      dash.dependencies.Input('month-dropdown', 'value'),
                      dash.dependencies.Input('study-dropdown2', 'value'),
              )
              )
def update_how_many_eco(month_value, municipios):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]

    # print(area_selected)
    area_cod = area_selected.iloc[0]['area_cod']
    # area_code = area_cod.astype(str).apply(lambda x: '{0:0>3}'.format(x))
    area_code = str(area_cod).zfill(3)

    sql_many = "select * from view_desempleo_por_mes_ciudad where area=" + area_code + " and mes=" + month_value + ""
    how_json = get_rows(sql_many)
    df = pd.DataFrame.from_dict(how_json['data']['table'])
    value = df['Tasa de desempleo']
    return "   Total: " + locale.format("%.2f", value, grouping=True) + "%"


@app.callback(dash.dependencies.Output('tasa_desem_comoyo', 'children'),
              (
                      dash.dependencies.Input('month-dropdown', 'value'),
                      dash.dependencies.Input('study-dropdown2', 'value'),
                      dash.dependencies.Input('educational_select', 'value'),
                      dash.dependencies.Input('sex_radio', 'value'),
                      dash.dependencies.Input('age_slider', 'value'),
              )
              )
def update_how_many_comoyo(month_value, municipios, educ_value, sex_value, age_slider):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]

    # print(area_selected)
    area_cod = area_selected.iloc[0]['area_cod']
    # area_code = area_cod.astype(str).apply(lambda x: '{0:0>3}'.format(x))
    area_code = str(area_cod).zfill(3)

    sql_many = "select round(100-100*(sum(\"Ocupado\"::INTEGER::FLOAT*fex_c_2011) / sum(fex_c_2011)::FLOAT)::NUMERIC, 2) as \"Tasa de desempleo\" from view_ocupados_desocupados where area = " + area_code + " and mes = " + month_value + " and \"Sexo\" = '" + sex_value + "'  and \"Nivel educativo\" = '" + educ_value + "' and \"Edad\" between " + str(
        age_slider[0]) + " and " + str(age_slider[1]) + ""
    how_json = get_rows(sql_many)
    if how_json['data']['table'] == 'no info':
        return "   Total: 0 meses"

    df = pd.DataFrame.from_dict(how_json['data']['table'])
    # value = df['Tasa de desempleo']

    # print(value)
    if df['Tasa de desempleo'] is None:
        return "   Total: 0 meses"
    else:
        value = df['Tasa de desempleo']
        return "   Total: " + locale.format("%.2f", value, grouping=True) + "%"

    # if df['Tasa de desempleo'].notnull():
    #    value = df['Tasa de desempleo']
    #    return "   Total: " + locale.format("%.2f", value, grouping=True) + "%"
    # else:
    #    value = df['Tasa de desempleo']


@app.callback(dash.dependencies.Output('tiempo_estimado_model', 'children'),
              (
                      dash.dependencies.Input('study-dropdown2', 'value'),
                      dash.dependencies.Input('educational_select', 'value'),
                      dash.dependencies.Input('sex_radio', 'value'),
                      dash.dependencies.Input('age_slider', 'value'),
              )
              )
def update_tiempo_estimado_model(municipios, educ_value, sex_value, age_slider):
    df_areas_sel = get_areas()
    # print(df_areas_sel)

    area_selected = df_areas_sel.loc[df_areas_sel['area'] == municipios]

    # print(area_selected)
    area_cod = area_selected.iloc[0]['area_cod']
    # area_code = area_cod.astype(str).apply(lambda x: '{0:0>3}'.format(x))
    area_code = str(area_cod).zfill(3)
    edad_str = 'MAYOR'
    if (age_slider[1] >= 28):
        edad_str = 'MAYOR'
    else:
        edad_str = 'MENOR'

    sql_many = "select * from modelo where area = " + area_code + " and sexo = '" + sex_value + "' and nivel_educ = '" + educ_value + "' and edad = '" + edad_str + "' "
    print(sql_many)
    how_json = get_rows(sql_many)
    if how_json['data']['table'] == 'no info':
        return "   Total: 0 meses"

    df = pd.DataFrame.from_dict(how_json['data']['table'])
    value = df['tiempo']
    return "   Total: " + locale.format("%d", value, grouping=True) + " meses"


@app.callback(
    dash.dependencies.Output('barplot_oficio', 'figure'),
    (
            dash.dependencies.Input('month-dropdown', 'value'),
    )
)
def update_barplot(month_value):
    x_name = 'nivel_educ'
    y_name = 'tasa'

    r = requests.post("http://ec2-3-133-150-215.us-east-2.compute.amazonaws.com:8020/employement_rate",
                      json={"month": 1, "gender": "Hombre", "municipio": 13, "age_base": 18, "age_top": 25,
                            "aggregator": "nivel_educ"})
    df = pd.DataFrame.from_dict(r.json()['data']['table'])
    df = df[df['ocupado'] == 0]

    series_x = fetch_series(df, x_name)
    series_y = fetch_series(df, y_name)

    series_plot = go.Bar(x=series_x, y=series_y)
    return {'data':
                [series_plot],
            'layout': {'title': 'Tasa de desempleo por Nivel Educativo', },
            }


@app.callback(
    dash.dependencies.Output('unemp_ocup', 'figure'),
    (
            dash.dependencies.Input('month-dropdown', 'value'),
            dash.dependencies.Input('sex_radio', 'value'),
    )
)
def update_unemp_ocup(month_value, sex_value):
    x_name = 'Ocupación'
    y_name = 'Tasa de desempleo'
    unemp_ocup_query = "select \"Ocupación\", round(100-100*(sum(\"Ocupado\"::INTEGER::FLOAT*fex_c_2011) / sum(fex_c_2011)::FLOAT)::NUMERIC, 2) as \"Tasa de desempleo\" from view_ocupados_desocupados"
    filters = "where mes = " + month_value + " and \"Ocupación\" <> 'ND' and \"Sexo\" = '" + sex_value + "'"
    # filters = "where mes = " + month_value + "and \"Ocupación\" <> 'ND' and \"Sexo\" = 'Hombre'"
    groupby = "group by \"Ocupación\""
    orderby = "order by \"Tasa de desempleo\" desc limit 10;"
    unemp_ocup_query = unemp_ocup_query + ' ' + filters + ' ' + groupby + ' ' + orderby
    # print("unemp_ocup_query> " + unemp_ocup_query)
    df_unemp_ocup = get_rows(unemp_ocup_query)

    df_unemp_ocup = pd.DataFrame.from_dict(df_unemp_ocup['data']['table'])
    df_unemp_ocup.dropna(inplace=True)

    series_x = fetch_series(df_unemp_ocup, x_name)
    series_y = fetch_series(df_unemp_ocup, y_name)

    series_plot = go.Bar(x=series_x, y=series_y)
    return {'data':
                [series_plot],
            }


@app.callback(
    dash.dependencies.Output('ing_ocup', 'figure'),
    (
            dash.dependencies.Input('month-dropdown', 'value'),
            dash.dependencies.Input('sex_radio', 'value'),
    )
)
def update_ing_ocup(month_value, sex_value):
    x_name = 'Ocupación'
    y_name = 'Ingreso promedio'
    ing_ocu_query = "select \"Ocupación\", avg(\"Ingresos\") as \"Ingreso promedio\" from view_ocupados_desocupados"
    filters = "where mes = " + month_value + "and \"Ocupación\" <> 'ND' and \"Sexo\" = '" + sex_value + "' and \"Ocupado\" is True "
    # filters = "where mes = " + month_value + " and \"Ocupación\" <> 'ND' and \"Sexo\" = 'Hombre' and \"Ocupado\" is True  and \"Ingresos\" IS NOT NULL"
    groupby = "group by \"Ocupación\""
    orderby = "order by \"Ingreso promedio\" DESC limit 10;"
    ing_ocu_query = ing_ocu_query + ' ' + filters + ' ' + groupby + ' ' + orderby
    # print(ing_ocu_query)

    df_ing_ocu = get_rows(ing_ocu_query)
    df_ing_ocu = pd.DataFrame.from_dict(df_ing_ocu['data']['table'])
    df_ing_ocu['Ingreso promedio'] = round(df_ing_ocu['Ingreso promedio'])
    df_ing_ocu.dropna(inplace=True)

    series_x = fetch_series(df_ing_ocu, x_name)
    series_y = fetch_series(df_ing_ocu, y_name)

    series_plot = go.Bar(x=series_x, y=series_y)
    return {'data':
                [series_plot],
            }


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8021, debug=True)