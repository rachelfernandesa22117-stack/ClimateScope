<h1>Milestone 2: Core Analysis & Visualization Design</h1>
<h3>Project: ClimateScope – Visualizing Global Weather Trends</h3>
<p><strong>Author:</strong> Rachel Fernandes</p>

<hr>

<ul>
  <li>Performed statistical exploration of the dataset</li>
  <li>Identified seasonal climate trends</li>
  <li>Analyzed regional differences</li>
  <li>Detected extreme weather events using percentile thresholds</li>
  <li>Designed a visualization strategy aligned with analytical findings</li>
</ul>

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
Additionally, I created a scatter plot (Temperature vs PM2.5) with an OLS trendline.
</p>

<hr>

<h2>4. Seasonal Pattern Analysis</h2>
<p>I calculated monthly averages for:</p>
<ul>
  <li>Temperature</li>
  <li>Humidity</li>
</ul>
<p>
I used line charts to highlight seasonal fluctuations and observe recurring patterns across months.
</p>

<hr>

<h2>5. Regional Comparison</h2>
<p>I computed country-level averages to compare climate conditions across regions.</p>
<ul>
  <li>Identified the top 10 hottest countries based on mean temperature.</li>
  <li>Identified the top 10 coldest countries.</li>
  <li>Analyzed country-wise PM2.5 averages to determine regions with higher pollution levels.</li>
</ul>
<p>
This comparison clearly highlighted geographic climate differences.
</p>

<hr>

<h2>6. Extreme Weather Event Identification</h2>
<p>I defined extreme thresholds using percentile-based methods:</p>
<ul>
  <li>Top 5% temperature → Extreme Heat</li>
  <li>Bottom 5% temperature → Extreme Cold</li>
  <li>Top 5% PM2.5 → Extreme Pollution</li>
</ul>
<p>
Using quantiles allowed me to detect extreme events dynamically and ensured that the classification was statistically justified.
</p>

<hr>

<h2>7. Dashboard Layout Plan</h2>
<ol>
  <li>Key weather indicators (summary metrics)</li>
  <li>Global geographic overview</li>
  <li>Distribution analysis</li>
  <li>Seasonal trends</li>
  <li>Correlation analysis</li>
  <li>Regional comparison</li>
  <li>Extreme events summary</li>
  <li>Country deep dive</li>
</ol>

<p>
I will incorporate interactive filters to allow users to explore data by country, month, and percentile thresholds.
</p>

<hr>

