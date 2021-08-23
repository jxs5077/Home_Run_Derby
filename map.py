import folium
import pandas as pd

HRD_df = pd.read_csv('HRDstats.csv')
HRD_df = HRD_df.rename(columns={"Exit Velocity (MPH)": "Exit_Velocity", "Distance (Ft.)": "Distance", "Launch Angle": "Launch_Angle", "HR Count": "HR_Count" })

#create list of unique batter names
Players = []
Players = HRD_df["Player"].unique()

HRD_df.set_index("Player", inplace = True)

#filter for distance data
dist=["Distance"]
distance_df=HRD_df.loc[:, dist]

#create column for distance converted from feet to meters
FEET_TO_M = 0.3048
distance_df['Distance(m)'] = distance_df['Distance'] * FEET_TO_M

total_dist = distance_df.groupby(["Player"]).sum()

#location of home plate at Progressive Field
lat = 41.495544
lon = -81.685285

tooltip="Click For Information"

mymap = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker(
    [lat, lon], popup="Home Plate - Progressive Field",
    tooltip=tooltip
    ).add_to(mymap)

colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'cadetblue']
n=0
tdistm=0
tdistft=0

for index, row in total_dist.iterrows():
    
    label= '{}, {} feet'.format(index, row[0])
    
    folium.Circle(
        radius=row["Distance(m)"],
        location=[lat, lon],
        popup=label,
        color=colors[n],
        fill=False,
        weight=5,
        tooltip=tooltip
#         fill_opacity= .2,
        ).add_to(mymap)
    
    tdistm=tdistm + row["Distance(m)"]
    tdistft=tdistft + row["Distance"]
    
    n=n+1
tlabel='{}, {} feet'.format("All Batters",tdistft)
folium.Circle(
    radius=tdistm,
    location=[lat,lon],
    popup=tlabel,
    color='black',
    tooltip=tooltip
    ).add_to(mymap)
mymap.save('mymap.html')