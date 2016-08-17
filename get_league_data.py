# Written by Jonathan Saewitz, released August 17th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

import requests, re, csv
from bs4 import BeautifulSoup

NUMBER_OF_LEAGUES_TO_SEARCH=100 #the number of leagues to check

#taken from https://stackoverflow.com/a/7085715/2150542
#this code will get the numbers at the end of a string:
def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

f=open('ff_draft_picks.csv', 'w')
w=csv.writer(f)
w.writerow(['League #', 'Winner draft pick #', '# Teams in league']) #write the header row

league_number=0
while league_number<NUMBER_OF_LEAGUES_TO_SEARCH: #keep checking until NUMBER_OF_LEAGUES_TO_SEARCH are searched
	print "Currently checking league #" + str(league_number)
	page=requests.get('http://games.espn.com/ffl/leagueoffice?leagueId=' + str(league_number) + "&seasonId=2015").text
	if "2015 League Champion!" in page: #a way to check if the league is public
		soup=BeautifulSoup(page, 'html.parser')
		team_name=soup.find_all('strong')[4].text #the winning team name is the fifth 'strong' element on the page

		#the number of teams in the league is the last digits of the text of the info-area class:
		number_teams=get_trailing_number(soup.find_all('div', class_="info-area")[0].text)
		
		draft_page=requests.get("http://games.espn.com/ffl/tools/draftrecap?leagueId=" + str(league_number) + "&seasonId=2015").text
		soup=BeautifulSoup(draft_page, 'html.parser')
		all_picks=soup.find_all("tr", class_="tableBody")
		for pick in all_picks: #loop through every pick
			try:
				#pick.find_all("a")[1] is the team name
				if pick.find_all("a")[1].text==team_name: #if the current team name is the same as the winning team name:
					pick_number=int(pick.find_all("td")[0].text) #get the pick number
					w.writerow([league_number, pick_number, number_teams]) #write it to the csv
					break #stop looping because we've already found the team's first pick

			except IndexError: #if there's an IndexError, assume the league didn't have a draft order (e.g. auction style draft)
				break

	league_number+=1 #increment the league_number to search the next league

f.close() #close the csv
