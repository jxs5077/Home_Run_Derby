from flask import Flask, render_template, redirect
import pandas as pd
import plotly.express as px
import plotly.io as pio


app=Flask(__name__)

@app.route('/')
def index():

    HRD_df = pd.read_csv('HRDstats.csv')
    HRD_df = HRD_df.rename(columns={"Exit Velocity (MPH)": "Exit_Velocity", "Distance (Ft.)": "Distance", "Launch Angle": "Launch_Angle", "HR Count": "HR_Count" })
    HRDrn_df = HRD_df
    HRDrn_df.set_index("Player", inplace = True)



    # Use column names instead. This is the same chart as above.
    fig = px.scatter(HRDrn_df, size='Launch_Angle', y='Distance', color=HRDrn_df.index, x='Exit_Velocity')

    fig.update_layout(
        title={
            'text': "Every Home Run From 2019 Home Run Derby",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Distance (Feet)",
        xaxis_title="Exit Velocity (MPH)",
        legend_title="Batter"),

    fig.show()
    pio.write_html(fig, file='scatterall.html', auto_open=True)
    


    fig = px.histogram(HRDrn_df, y="Launch_Angle")

    fig.update_layout(
        title={
            'text': "Number of Home Runs by Launch Angle",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Launch Angle in Degrees",
        xaxis_title="Number of Home Runs",
        legend_title="Batter"),
    fig.show()
    pio.write_html(fig, file='hist.html', auto_open=True)



    fig = px.scatter_polar(HRDrn_df,theta='Launch_Angle', r='Distance', color=HRDrn_df.index, range_theta=[0,90], start_angle=0, direction="counterclockwise") 
                        
    fig.update_layout(
        title={
            'text': "Every Home Run From 2019 Home Run Derby",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Distance (Feet)",
        yaxis_title="Launch Angle in Degrees",
        legend_title="Batter",
        showlegend = True,
        polar = dict(# setting parameters for the second plot would be polar2=dict(...)
        sector = [0,90],
        ))
    fig.show()
    pio.write_html(fig, file='scatter90.html', auto_open=True)



    HRDmean = HRDrn_df.groupby(["Player"]).mean().round(1)
    fig = px.scatter(HRDmean, size='Launch_Angle', y='Distance', color=HRDmean.index, x='Exit_Velocity')
    fig.update_layout(
        title={
            'text': "2019 Home Run Derby Batter Averages",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Distance (Feet)",
        xaxis_title="Exit Velocity (MPH)",
        legend_title="Batter"),
    fig.show()
    pio.write_html(fig, file='scatteravg.html', auto_open=True)




if __name__=='__main__': 
	app.run()