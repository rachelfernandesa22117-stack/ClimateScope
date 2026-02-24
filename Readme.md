<h1>Milestone 2: Core Analysis & Visualization Design</h1>
<h3>Project: ClimateScope – Visualizing Global Weather Trends</h3>
<p><strong>Author:</strong> RachelFernandes</p>

<hr>

<h2>1. Data Preparation</h2>
<p>
I began by loading the Global Weather Repository dataset and selecting the most relevant variables, including:
</p>
<ul>
  <li>Temperature (°C)</li>
  <li>Humidity</li>
  <li>Wind Speed (kph)</li>
  <li>Pressure (mb)</li>
  <li>PM2.5 and PM10 (Air Quality)</li>
  <li>Country and Date</li>
</ul>
<p>
I converted the <code>last_updated</code> column into proper datetime format and extracted new columns (year, month, day) to support time-based analysis. 
This allowed me to perform structured seasonal and trend analysis.
</p>


<hr>

<h2>2. Distribution Analysis</h2>
<p>I created histograms to understand the distribution of:</p>
<ul>
  <li>Temperature</li>
  <li>Humidity</li>
  <li>PM2.5</li>
</ul>
<p>
This helped me observe variability, skewness, and general data spread across key environmental variables.
</p>

<hr>

<h2>3. Correlation Analysis</h2>
<p>I computed a correlation matrix using:</p>
<ul>
  <li>Temperature</li>
  <li>Humidity</li>
  <li>Wind Speed</li>
  <li>Pressure</li>
  <li>PM2.5</li>
</ul>
<p>
I visualized these relationships using a heatmap to clearly identify positive and negative correlations.
Additionally, I created a scatter plot (Temperature vs PM2.5) with an OLS trendline, which showed a weak but noticeable relationship between temperature and air quality levels.
</p>

<hr>
