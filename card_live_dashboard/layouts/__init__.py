from typing import Dict, List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import card_live_dashboard
import card_live_dashboard.layouts.figures as figures

external_stylesheets = [dbc.themes.BOOTSTRAP]


def default_layout():
    """
    Builds the default layout of the CARD:Live dashboard.
    :return: The default layout of the CARD:Live dashboard.
    """
    LOADING = '[LOADING]'
    AUTO_UPDATE_MILLIS = 10 * 60 * 1000 # milliseconds

    layout = html.Div(className='card-live-all container-fluid', children=[
        html.Div(className='row', children=[
            html.Div(className='card-live-panel col-sm-3', children=[
                html.Div(className='sticky-top', children=[
                    html.H1([
                        'CARD:Live'
                    ]),
                    html.Div(className='pt-2 pb-1', children=[
                        'Welcome to the ',
                        html.A(children=['CARD:Live'], href='https://card.mcmaster.ca/live'),
                        ' dashboard.'
                    ]),
                    html.Div(className='card-live-badges pb-3', children=[
                        html.Span(className='badge badge-secondary', children=[
                            html.Span(id='global-sample-count', children=[LOADING]),
                            ' samples']),
                        ' ',
                        html.Span(className='badge badge-secondary',
                                  children=[f'Most recent: ', html.Span(id='global-most-recent', children=[LOADING])]),
                    ]),
                    html.Div([
                        html.H2('Selection criteria'),
                        html.P([
                            'Please select from the options below to examine subsets of the ',
                            html.A(children=['CARD:Live'], href='https://card.mcmaster.ca/live'),
                            ' data.',
                            html.Div(className='card-live-badges pt-1', children=[
                                html.Span(className='badge badge-secondary', children=[
                                    'Showing ', html.Span(id='selected-samples-count',
                                                          children=[LOADING]),
                                    ' samples'
                                ]),
                            ]),
                        ]),
                    ]),
                    html.Div([
                        dbc.Button(id='rgi-parameters-toggle', color='link',
                                   className='cardlive-collapse pl-0', children=[html.H3('RGI')]),
                        dbc.Collapse(id='rgi-parameters', is_open=True, children=[
                            html.Div(children=['RGI cutoff: ',
                                               dbc.RadioItems(
                                                   id='rgi-cutoff-select',
                                                   className='sidepanel-selection-light',
                                                   options=[
                                                       {'label': 'All', 'value': 'all'},
                                                       {'label': 'Perfect', 'value': 'perfect'},
                                                       {'label': 'Strict', 'value': 'strict'},
                                                   ],
                                                   value='all',
                                                   inline=True,
                                               ),
                                               ]),
                            html.Div(children=['Filter display by drug class: ',
                                               dcc.Dropdown(
                                                   id='drug-class-select',
                                                   className='sidepanel-selection',
                                                   multi=True,
                                                   placeholder='Select a drug class',
                                               ),
                                               ]),
                            html.Div(children=['Filter display by Best Hit ARO: ',
                                               dcc.Dropdown(
                                                   id='besthit-aro-select',
                                                   className='sidepanel-selection',
                                                   multi=True,
                                                   placeholder='Select a Best Hit ARO value',
                                               ),
                                               ]),
                        ]),
                    ]),
                    html.Div([
                        dbc.Button(id='time-parameters-toggle', color='link',
                                   className='cardlive-collapse pl-0', children=[html.H3('Time')]),
                        dbc.Collapse(id='time-parameters', is_open=True, children=[
                            html.Div(children=['Select a time period: ',
                                               dcc.Dropdown(id='time-period-items',
                                                            className='sidepanel-selection',
                                                            value='all',
                                                            clearable=False)
                                               ]),
                        ]),
                    ]),
                    html.P(className='text-center card-live-badges', children=[
                        html.Br(),
                        html.A(className='badge badge-primary',
                               children=[f'Version | {card_live_dashboard.__version__}'],
                               href='https://devcard.mcmaster.ca:8888/apetkau/card-live-dashboard'),
                    ]),
                ]),
            ]),
            html.Div(className='col', children=[
                # component to auto update data
                dcc.Interval(
                    id='auto-update-interval',
                    interval=AUTO_UPDATE_MILLIS,  # in milliseconds
                    n_intervals=0
                ),
                html.Div(className='container', children=[
                    html.Div(className='row', children=[
                        html.Div(className='col', id='main-pane',
                                 # Need to display initial empty figures
                                 # So callbacks can be linked up correctly
                                 children=figures_layout(figures.EMPTY_FIGURE_DICT)
                                 ),
                    ]),
                ]),
            ]),
        ]),
    ])

    return layout


def figures_layout(figures_dict: Dict[str, go.Figure]):
    """
    Builds the layout of the figures on the page.
    :param figures_dict: A dictionary mapping names of constructed figures to the figure objects.
    :return: A list of figures to place on the page.
    """
    return [
        html.Div(className='cardlive-figures', children=[
            single_figure_layout(title='Map',
                                 id='figure-geographic-map-id',
                                 fig=figures_dict['map']
                                 ),
            single_figure_layout(title='Timeline',
                                 id='figure-timeline-id',
                                 fig=figures_dict['timeline'],
                                 dropdowns=figure_menus_layout(
                                     id_type='timeline-type-select',
                                     options_type=[
                                        {'label': 'Cumulative', 'value': 'cumulative'},
                                        {'label': 'Rate', 'value': 'rate'},
                                     ],
                                     value_type='cumulative',
                                     id_color='timeline-color-select',
                                     options_color=[
                                        {'label': 'Default', 'value': 'default'},
                                        {'label': 'Geographic region', 'value': 'geographic'},
                                        {'label': 'Organism (LMAT)', 'value': 'organism_lmat'},
                                        {'label': 'Organism (RGI Kmer)', 'value': 'organism_rgi_kmer'}
                                     ],
                                     value_color='default'
                                 ),
                             ),
            single_figure_layout(title='Totals',
                                 id='figure-totals-id',
                                 fig=figures_dict['totals'],
                                 dropdowns=figure_menus_layout(
                                     id_type='totals-type-select',
                                     options_type=[
                                         {'label': 'Geographic region', 'value': 'geographic'},
                                         {'label': 'Organism (LMAT)', 'value': 'organism_lmat'},
                                         {'label': 'Organism (RGI Kmer)', 'value': 'organism_rgi_kmer'},
                                     ],
                                     value_type='geographic',
                                     id_color='totals-color-select',
                                     options_color=[
                                         {'label': 'Default', 'value': 'default'},
                                         {'label': 'Geographic region', 'value': 'geographic'},
                                         {'label': 'Organism (LMAT)', 'value': 'organism_lmat'},
                                         {'label': 'Organism (RGI Kmer)', 'value': 'organism_rgi_kmer'}
                                     ],
                                     value_color='default'
                                 ),
                             ),
        ])
    ]


def single_figure_layout(title: str, id: str, fig: go.Figure, dropdowns: html.Div = None):
    component = dbc.Card(className='my-3', children=[
        dbc.CardHeader(children=[
            html.H4(title),
            dropdowns,
        ]),
        dcc.Loading(type='circle', children=[
            dbc.CardBody(children=[
                dcc.Graph(id=id, figure=fig),
            ]),
        ]),
    ])

    return component


def figure_menus_layout(id_type: str, options_type: List[Dict[str,str]], value_type: str,
                        id_color: str, options_color: List[Dict[str,str]], value_color: str) -> html.Div:
    return html.Div(className='d-flex align-items-center', children=[
        html.Div(['Type:']),
        html.Div(className='ml-2', children=[dcc.Dropdown(
            id=id_type,
            options=options_type,
            searchable=False,
            clearable=False,
            value=value_type,
        )]),
        html.Div(className='ml-3', children=['Color by:']),
        html.Div(className='ml-2', children=[dcc.Dropdown(
            id=id_color,
            options=options_color,
            searchable=False,
            clearable=False,
            value=value_color,
        )]),
    ])