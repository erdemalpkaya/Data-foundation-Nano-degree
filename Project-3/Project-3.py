# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Udacity Data Foundation Nanodegree

# ## Project 3: Query a Digital Music Store Database

# This is Udacity Data foundation Nanodegree Project 3 

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))

import pandas as pd
import numpy as np
import math
import plotly



# +
# Load libraries
import pandas as pd
from sqlalchemy import create_engine

# Create a connection to the database
database_connection = create_engine('sqlite:///chinook.db')

# Load data
dataframe1 = pd.read_sql_query("""

select strftime('%Y-%m-01',Date) as Month, country, sum(monthTotal) as totalSale
from
(
SELECT Invoice.invoiceDate as Date, invoice.billingCountry as country, invoice.billingCity as City, Invoice.BillingAddress as Address, InvoiceLine.unitPrice, Invoice.total monthTotal
From Artist
JOIN Album on Artist.ArtistId = Album.ArtistId
JOIN Track on Track.AlbumId = Album.AlbumId
JOIN Genre on Genre.GenreId = Track.genreId
JOIN InvoiceLine on InvoiceLine.trackId = Track.trackId
JOIN Invoice on Invoice.invoiceId = invoiceLine.invoiceId
JOIN Customer on Customer.customerId = Invoice.customerId
group by Date, Country, Address
) t1
where country = "USA"
group by Month, country

""", database_connection)

# View first 10 rows
dataframe1.head(10)

# +

import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Scatter(
    x=dataframe1.Month,
    y=dataframe1.totalSale,
    marker = dict(
        color = 'rgba(17, 60, 96, 0.6)'),
    line = dict (
    dash = 'solid',
    width = 3
    ),
    name='Monthly Sales'
)


data = [trace1]
layout = go.Layout(
    paper_bgcolor= 'rgb(236, 239, 239)',
    plot_bgcolor= 'rgb(236, 239, 239)',
    title = 'USA Monthly Total Sales',
    xaxis = dict(
    title = 'Date'),
    yaxis = dict(
    title='Sales'),
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='USA-Month Sales')
# -

#     The graph shows us the total sales in USA between January 2009 and December 2013. As we can see the graph that we do not have any significant trend. 
#     The minimum value is per month us $0.99 for 7 months and the highest sales in September 2012 which is $29.85 
#

# +
# Load libraries
import pandas as pd
from sqlalchemy import create_engine

# Create a connection to the database
database_connection = create_engine('sqlite:///chinook.db')

# Load data
dataframe2 = pd.read_sql_query("""

select customer.customerId, customer.firstName, customer.lastName, sum(invoice.Total) as totalAmount from invoice
join customer on customer.customerId = invoice.customerId
where invoice.InvoiceDate >= '2012-01-01' and invoice.InvoiceDate <'2013-01-01' and invoice.BillingCountry = 'USA'
group by customer.customerId
Order by totalAmount Desc
LIMIT 10


""", database_connection)

dataframe2

# +
import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Bar(
    x=dataframe2.FirstName + " " + dataframe2.LastName,
    y=dataframe2.totalAmount,
    marker = dict(
        color = 'rgba(17, 60, 96, 0.6)'),
    name='Customer Sales'
)


data = [trace1]
layout = go.Layout(
    paper_bgcolor= 'rgb(236, 239, 239)',
    plot_bgcolor= 'rgb(236, 239, 239)',
    title = 'Top 10 Customer in 2012',
    xaxis = dict(
    title = 'Customer name'),
    yaxis = dict(
    title='Total amount Sales'),
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Top-10')

# +
# Load libraries
import pandas as pd
from sqlalchemy import create_engine

# Create a connection to the database
database_connection = create_engine('sqlite:///chinook.db')

# Load data
dataframe3 = pd.read_sql_query("""

select artist.Name as ArtistName, album.title as AlbumTitle, sum(invoiceline.UnitPrice) as Total from artist
join album on album.artistId = artist.artistId
join track on track.albumId = album.albumId
join invoiceLine on invoiceLine.trackId = track.trackId
group by AlbumTitle
order by Total desc
LIMIT 10

""", database_connection)

dataframe3

# +
import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Bar(
    x=dataframe3.AlbumTitle,
    y=dataframe3.Total,
    marker = dict(
        color = 'rgba(97, 20, 16, 0.6)'),
    name='Monthly Sales'
)


data = [trace1]
layout = go.Layout(
    paper_bgcolor= 'rgb(236, 239, 239)',
    plot_bgcolor= 'rgb(236, 239, 239)',
    title = 'Top 10 Album',
    xaxis = dict(
    title = 'Album Name',
    tickangle = 15),
    yaxis = dict(
    title='Total Number of Album Sold'),
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Top-ALbum')

# +
# Load libraries
import pandas as pd
from sqlalchemy import create_engine

# Create a connection to the database
database_connection = create_engine('sqlite:///chinook.db')

# Load data
dataframe4 = pd.read_sql_query("""

select genre.name, invoice.billingCountry as Country, count(invoiceLine.unitPrice) as Total from Genre
join track on track.genreId = genre.genreId
join invoiceline on invoiceLine.trackId = track.trackId
join invoice on invoice.invoiceid = invoiceLine.invoiceId
where genre.name = 'Rock'
group by Country
order by Total desc

""", database_connection)

dataframe4

# +
import plotly.plotly as py
import plotly.graph_objs as go



trace1 = go.Bar(
    x=dataframe4.Country,
    y=dataframe4.Total,
    marker = dict(
        color = 'rgba(170, 60, 96, 0.6)'),
    name='Total Number of sales'
)




data = [trace1]
layout = go.Layout(
    paper_bgcolor= 'rgb(236, 239, 239)',
    plot_bgcolor= 'rgb(236, 239, 239)',
    title = 'Number of Rock Tracks sales by each Country',
    xaxis = dict(
    title = 'Countries',
    tickangle = 25),
    yaxis = dict(
    title='Total Number of Track'),
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Rock-countries')
# -




