import csv

listings = open('listings.csv')
listingReader = csv.reader(listings)
listingData = list(listingReader)

l_ID = []
host_ID = []
host_name = []
host_since = []
host_RR = []
host_AR = []
host_LC = []
neigh_C = []
state = []
zip_code = []
lat = []
longitude = []
prop_type = []
room_type = []
accom = []
bath = []
bedrooms = []
beds = []
sq_ft = []
price = []
week_price = []
month_price = []
sec_deposit = []
cleaning_fee = []
guest_inc = []
extra_peop = []
min_night = []
max_night = []
avail_30 = []
avail_60 = []
avail_90 = []
avail_365 = []
number_reviews = []
f_review = []
l_review = []
review_score = []
review_score_acc = []
review_score_clean = []
review_score_checkin = []
review_score_comm = []
review_score_loc = []
review_score_value = []
review_permonth = []

for i in range (1,3274):
    l_ID.append(listingData[i][0])
    host_ID.append(listingData[i][16])
    host_name.append(listingData[i][18])
    host_since.append(listingData[i][19])
    host_RR.append(listingData[i][23])
    host_AR.append(listingData[i][24])
    host_LC.append(listingData[i][29])
    neigh_C.append(listingData[i][36])
    state.append(listingData[i][39])
    zip_code.append(listingData[i][40])
    lat.append(listingData[i][45])
    longitude.append(listingData[i][46])
    prop_type.append(listingData[i][48])
    room_type.append(listingData[i][49])
    accom.append(listingData[i][50])
    bath.append(listingData[i][51])
    bedrooms.append(listingData[i][52])
    beds.append(listingData[i][53])
    sq_ft.append(listingData[i][56])
    price.append(listingData[i][57])
    week_price.append(listingData[i][58])
    month_price.append(listingData[i][59])
    sec_deposit.append(listingData[i][60])
    cleaning_fee.append(listingData[i][61])
    guest_inc.append(listingData[i][62])
    extra_peop.append(listingData[i][63])
    min_night.append(listingData[i][64])
    max_night.append(listingData[i][65])
    avail_30.append(listingData[i][68])
    avail_60.append(listingData[i][69])
    avail_90.append(listingData[i][70])
    avail_365.append(listingData[i][71])
    number_reviews.append(listingData[i][73])
    f_review.append(listingData[i][74])
    l_review.append(listingData[i][75])
    review_score.append(listingData[i][76])
    review_score_acc.append(listingData[i][77])
    review_score_clean.append(listingData[i][78])
    review_score_checkin.append(listingData[i][79])
    review_score_comm.append(listingData[i][80])
    review_score_loc.append(listingData[i][81])
    review_score_value.append(listingData[i][82])
    review_permonth.append(listingData[i][91])

print type(l_review)

# print('The median accommodation number is ' + str(statistics.median(listingAccom)))
#
# listingDataPrice = [i.lstrip('$') for i in listingDataPrice]
# listingDataPrice = [i.replace(',','') for i in listingDataPrice]
# listingDataPrice = [float(i) for i in listingDataPrice]
#
# print('The median listing price is $' + str(statistics.median(listingDataPrice)))
