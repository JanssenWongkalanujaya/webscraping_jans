from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', class_='table table-striped table-hover table-hover-solid-row table-simple history-data')
#___ = tbody.find_all('___')
#temp = [] #initiating a tuple

#for i in range(1, len(tr)):
#insert the scrapping process here
temp = []
for team in table.find_all('tbody'):
    rows = table.find_all('tr')
    for row in rows:
        conversion = row.find('td', class_='text-narrow-screen-hidden').text.strip()
        tanggal = row.find_all('td')[0].text
        hari = row.find_all('td')[1].text
        rupiah = row.find_all('td')[2].text
        #kurs = row.find_all('div', class_='inner')
        #print((tanggal,hari,rupiah,conversion))
        
        temp.append((tanggal,hari,rupiah))
        
temp

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns=('Date','Day','Kurs'))

#insert data wrangling here

df['Kurs'] = df['Kurs'].str.replace(" IDR", "")
df['Date'] = df['Date'].astype('Datetime64')
df['Kurs'] = df['Kurs'].str.replace(",", "")
df['Kurs'] = df['Kurs'].astype('float')
df['Day'] = df['Day'].astype('category')
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["Kurs"].mean()}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
