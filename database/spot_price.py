
days=pd.bdate_range(start='20110101',periods=300)
def get_spot():
    for date in days[:5]:
        date=date.strftime('%Y-%m-%d')
        url='http://www.100ppi.com/sf/day-%s.html'%date
        data=pd.read_html(url)
        df=data[1].dropna()
        spot=df.iloc[:,:2]
        spot.column=['commodity','spot']
        spot['date']=date
        print(spot.head())
        return spot
