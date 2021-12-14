def plotdata1(infodata):  
    crime_2019 = [] 
    crime_2020 = []
    for item in infodata:
        year = item['data_year']
        if year == 2019:
            stolen = item['actual_count']
            crime_2019.append(stolen)
        elif year == 2020:
            stolen = item['actual_count']
            crime_2020.append(stolen)


    state = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA','WV','WI','WY']


    fig = go.Figure()

    fig.add_trace(go.Scatter(x=state, y = crime_2019, name = '2019',
                         line=dict(color='lightgreen', width=3)))

    fig.add_trace(go.Scatter(x=state, y= crime_2020, name='2020',
                            line=dict(color='red', width=3)))
 
    fig.update_layout(title='Crime Rate By State',
                    xaxis_title='States',
                    yaxis_title='Burglaries')
    fig.show()


def averagecrimeperyear(infodata):
    stateslist = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA','WV','WI','WY']
    total2019 = 0
    total2020 = 0
    for item in infodata:
        year = item['data_year']
        stolenlist =[]
        if year == 2019:
            stolen = item['actual_count']
            stolenlist.append(stolen)
            for item in stolenlist:
                total2019 += item
                average2019 = total2019 // len(stateslist)
        elif year == 2020:
            stolen = item['actual_count']
            stolenlist.append(stolen)
            for item in stolenlist:
                total2020 += item
                average2020 = total2020 // len(stateslist)

        #     total2020 = (total2020 + stolen) // len(stateslist)
    print("The average amount of burglaries per state in 2019 was: " + str(average2019))
    print("The average amount of burglaries per state in 2020 was: " + str(average2020))


def main():
    # infodata = readDataFromAPI()
    # cur, conn = setUpDatabase('Database-Claire.db')
    # setUpCrimeTable(cur, conn)
    # storeData(infodata, cur, conn)
    plotdata1(infodata)
    averagecrimeperyear(infodata)
    createfile("Crime.txt")

    # delete_table(cur, conn)
    conn.close()

    # plotdata(infodata)


if __name__ == "__main__":
    main()   