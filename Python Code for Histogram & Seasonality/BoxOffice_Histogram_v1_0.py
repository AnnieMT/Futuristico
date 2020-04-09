# Programmed by Kwak, B @ 12/02/2014
# Histogram Plot and Analysis


import numpy as np
import pylab as P
import csv

f = open('C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/transformed/topActorDirectorProd.csv')
#j = open('C:/00 - MyWork/SJSU/CMPE 239/Project/Movie/ftp.sunet.se/00 - progress/new_data/transformed/topActorDirectorProd_v1.csv','wb')

csv_f = csv.reader(f)
writer = csv.writer(j)
cnt1 = 0
tf_row = 12 # when counting from 0
#writer.writerow('Title,Genre,Actors,Director,Award,Production,imdbRating,imdbVotes,Released,tomatoUserReviews,tomatoUserRating,tomatoUserMeter,BoxOffice,Rated,Metascore,Wikistats')
#j.write('Title,Genre,Actors,Director,Award,Production,imdbRating,imdbVotes,Released,tomatoUserReviews,tomatoUserRating,tomatoUserMeter,BoxOffice,Rated,Metascore,Wikistats\n')

boxOff = []
for row in csv_f: 
	cnt1 += 1

	if cnt1 > 1:
		boxOff.append(float(row[tf_row]))


# the histogram of the data with histtype='step'
n, bins, patches = P.hist(boxOff, 30, normed=0, histtype='stepfilled')
P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

#l = P.plot(bins, y, 'k--', linewidth=1.5)

P.figure()
n, bins, patches = P.hist(boxOff, 30, normed=1, histtype='step', cumulative=True)

#hist, bin_edges = np.histogram(boxOff, 10, None, False, None, False)


f.close()
#j.close()
