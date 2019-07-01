I made a python file called spatial.

Check out the ipython notebook for a set of example. 

Mainly, pass the data as is to the function "generate_hex_heatmap"

There function takes the parameters:
	- (data) any data with columns 'lat' and 'long'
        - (aggregateThis="count") the variable to sum on every haxagon
        - (outpath="index.html") the place where to write the html file
        - (h3_resolution=8) the higher the value the smaller the 'diameter' of the hexagon
        - (map_zoom_level=11) the higher the value the more zoomed in
        - (midpoint=[24.71284, 46.70490]) the center point of the map defaulted to Riyadh
        - (logScale=False) for heavy tailed plots, this take the effect of outliers in the aggregated data 
