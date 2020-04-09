# Bug fixed + Revised
# v0.4: changed since title extraction format changed (1-May-12) -> (1 May 2014)
# v0.5: first description line was wrong in out file.
# v0.6: Added Halloween Day for Holiday [11/27/2014]

# 11/08/2014 made by KWAK, BAEK SOO
# CMPE 239, San Jose State University
# Python Code for Transforming "released date" into "seasonality"

# Seasonality definition
setSeasonDays = 10 # set within 10 days before the Holiday
cntForDiffYear = 0 # exception counter
cntForSeasonal = 0 # counter for seasonal movies

fr = open("C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/total_title_result_in.csv", 'r') 
fw1 = open("C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/total_title_result_out_v0_6.csv", 'w')
#fr = open("C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/Title_Num5_result.csv", 'r') 
#fw1 = open("C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/Title_Num5_result_out.csv", 'w')

lines = fr.readlines()
#fw1.write('Title,Genre,Actors,Director,Award,Production,Released,Rated,GenreN,ActorsN,DirectorN,Award_Number,ProductionN,BoxOffice,Seasonality,imdbRating,imdbVotes,tomatoUserReviews,tomatoUserRating,tomatoUserMeter,RatedN,Metascore,Wikistats,Seasonality\n')
fw1.write('Title,Genre,Actors,Director,Award,Production,imdbRating,imdbVotes,Released,tomatoUserReviews,tomatoUserRating,tomatoUserMeter,BoxOffice,Rated,Metascore,Wikistats,Seasonality\n')

yearUsHoliday = range(2007, 2015) # 2007 - 2014
#monthUsHoliday = [1,1,2,5,7,9,10,11,11,12] # 10 US Holidays
monthUsHoliday = [1,1,2,5,7,9,10,10,11,11,12] # 10 US Holidays + Halloween
# US Federal Holiday
# New Year’s Day, Birthday of Martin Luther King, Jr., Washington’s Birthday, Memorial Day, Independence Day
# Labor Day, Columbus Day, Veterans Day, Halloween, Thanksgiving Day, Christmas Day

dayUsHolidayPerYear = [
#    [1,15,19,28,4,3, 8,12,22,25], # 2007
#    [1,21,18,26,4,1,13,11,27,25], # 2008
#    [1,19,16,25,3,7,12,11,26,25], # 2009
#    [1,18,15,31,5,6,11,11,25,24], # 2010
#    [1,17,21,30,4,5,10,11,24,25], # 2011
#    [2,16,20,28,4,3, 8,12,22,25], # 2012
#    [1,21,18,27,4,2,14,11,28,25], # 2013
#    [1,20,17,26,4,1,13,11,27,25]  # 2014
    [1,15,19,28,4,3, 8,31,12,22,25], # 2007
    [1,21,18,26,4,1,13,31,11,27,25], # 2008
    [1,19,16,25,3,7,12,31,11,26,25], # 2009
    [1,18,15,31,5,6,11,31,11,25,24], # 2010
    [1,17,21,30,4,5,10,31,11,24,25], # 2011
    [2,16,20,28,4,3, 8,31,12,22,25], # 2012
    [1,21,18,27,4,2,14,31,11,28,25], # 2013
    [1,20,17,26,4,1,13,31,11,27,25]  # 2014
]

from datetime import date

dicMonth2Num = {' Jan ':1, ' Feb ':2, ' Mar ':3, ' Apr ':4, ' May ':5, ' Jun ':6, ' Jul ':7, ' Aug ':8, ' Sep ':9, ' Oct ':10, ' Nov ':11, ' Dec ':12}

for line in lines:     
    for k, v in dicMonth2Num.items():
        monst=line.find(k,1)
        if monst!=-1:
            dayst=line.find(',', monst-4)  
            if dayst!=-1:
                day=line[dayst+1:monst]
                month=v
#                year='20'+line[monst+5:monst+7]
                year=line[monst+5:monst+9]
                if year.isalpha()==True: 
                    break
                elif (year.isalnum()==True) and (len(year)==4):
                    yearN=int(year)
                    monthN=int(month)
                    dayN=int(day)
                    movieDate=date(yearN, monthN, dayN)
#                    print(movieDate)
           
                    if (yearN >= 2007 and yearN <=2014):
                        for y in range(0, len(yearUsHoliday)-1, 1):
                            for m in range(0, len(monthUsHoliday)-1, 1):                        
                                diff=date(yearUsHoliday[y], monthUsHoliday[m], dayUsHolidayPerYear[y][m]) - movieDate
                                dayDiff=diff.days
                                seasonal=0
                                if ((dayDiff >= 0) and (dayDiff <= setSeasonDays)):
                                    seasonal=1
                                    cntForSeasonal += 1
                                    print(seasonal, dayDiff, 'Movie', movieDate, 'Holiday', date(yearUsHoliday[y], monthUsHoliday[m], dayUsHolidayPerYear[y][m]))
                                    break
#                            print(dayDiff, seasonal)
                            if (seasonal):
                                break
                        listWseason=line[0:len(line)-1]+","+str(seasonal)+"\n"
#                        print(seasonal)
                        fw1.write(listWseason)
                    else:
                        cntForDiffYear += 1
#                        print('There are moives in year: ', year)
#    fw1.write(listWseason)

print("\n\n\n")
print('Total Number of Movie: ', len(lines))
print('Number of Movies not for 2007 - 2014: ', cntForDiffYear)
subTotal = len(lines) - cntForDiffYear
print('Resultant Number of Movies for 2007 - 2014: ', subTotal)
print('Seasonal Movies for 2007 - 2014: ', cntForSeasonal)

fr.close() 
fw1.close() 
