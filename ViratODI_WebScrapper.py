import requests
from bs4 import BeautifulSoup 
import re
import csv
import datetime
from csv import writer

link = "https://stats.espncricinfo.com/ci/engine/stats/index.html?batting_hand=1;class=2;filter=advanced;orderby=start;player_involve=49752;size=200;template=results;type=batting;view=innings"
parentLink = "https://stats.espncricinfo.com"
page = requests.get(link)
html = page.text
soup = BeautifulSoup(html, 'html.parser') 

PlayerName = "V Kohli"
   
# Function to covert string to datetime 
def convert(date_time): 
	format = '%d %b %Y' # The format 
	datetime_str = datetime.datetime.strptime(date_time, format)
	return datetime_str

#getting the column names
columns = []
headlinks = soup.find('tr' , class_ = 'headlinks')
Names = headlinks.find_all('th')
for name in Names:
	if(name.text != ''):
		columns.append(name.text)

NextLink = link
table = []
while(NextLink != ''):

	nextPage = requests.get(NextLink)
	html2 = nextPage.text
	soup2 = BeautifulSoup(html2, 'html.parser')
	results = soup2.find_all('tr', class_ = 'data1')


	for result in results:
		data = result.find('td').find('a')
		if(data.text == PlayerName):

			runs = result.find('td').findNext('td')
			mins = runs.findNext('td')
			bf = mins.findNext('td')
			fours = bf.findNext('td')
			sixes = fours.findNext('td')
			SR = sixes.findNext('td')
			Inns = SR.findNext('td')
			Opp = Inns.findNext('td').findNext('td')
			Ground = Opp.findNext('td')
			Date = Ground.findNext('td')
			score = re.split(r'\*' , runs.text )
			opp = re.split(r'v ', Opp.text)
	
			row = {}
			row['runs'] = score[0]
			row['NotOut'] = len(score) - 1
			row['mins'] = mins.text
			row['bf'] = bf.text
			row['fours'] = fours.text
			row['sixes'] = sixes.text
			row['sr'] = SR.text
			row['Inns'] = Inns.text
			row['Opp'] = opp[1]
			row['Ground'] = Ground.text
			row['Date'] = Date.text
			table.append(row)
			print(score[0])

	#getting the next link
	NextLink = ''
	links = soup2.find_all('a', class_ = 'PaginationLink')
	if(links != None):
		for link in links:
			if(link.find('img')!=None):
				if(link.find('img')['title'] == "Next page"):
					NextLink = parentLink + link['href']
					break

filename = 'Virat_ODI.csv'
with open(filename, 'a+', newline='') as f:
	w = csv.DictWriter(f,['runs','NotOut','mins','bf','fours','sixes','sr','Inns','Opp','Ground','Date'])
	w.writeheader() 
	for row in table:
		w.writerow(row)
	
        


	



