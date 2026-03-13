# Milestone 1 – ClimateScope Project Submission
**Author:** Rachel Fernandes

## Project Status
- Dataset successfully downloaded  
- Data cleaned and standardized  
- Missing values inspected  
- Dataset aggregated  
- Ready for visualization using Plotly & Streamlit  



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

<h2>Dashboard Layout Plan</h2>
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

</body>
</html>


# ClimateScope — Milestone 3 Report
### Visualization Development & Interactivity

## Visualization Development
The dashboard integrates multiple visualization types to analyze climate patterns:

• Choropleth world map showing **average temperature by country**  
• Histograms for **temperature, humidity, wind speed, pressure, UV index, and visibility distributions**  
• Seasonal trend visualizations including **monthly line charts and box plots**  
• **Heatmaps** comparing temperature patterns across countries and months  
• **Correlation matrix** to analyze relationships between weather variables  
• **Scatter plots with regression trendlines** to explore pollutant and climate relationships  
• **Violin plots** for distribution comparison between countries  
• **Extreme weather event analysis** using percentile thresholds  
• **Rolling average time-series analysis** to reveal long-term trends

---

## Interactive Features
The dashboard includes multiple forms of interactivity:

• **Country selection filter**
• **Month selection filter**
• Dynamic **filter-driven chart updates**
• **Hover-based data exploration**
• Interactive **tabs for grouped visualizations**
• **Collapsible filter panel**
• Dynamic **data sampling for performance optimization**

All visualizations automatically update when filter selections change.

---

## Visualization Design & User Experience
Several design improvements were implemented to enhance usability:

• Consistent color themes across visualizations  
• Clear axis labels and chart titles  
• Styled **insight boxes** highlighting key findings  
• Structured layout using **sections and columns**  
• Performance optimization using **Streamlit caching**

---

## Key Analytical Insights
The dashboard automatically extracts insights from the dataset, including:

• Identification of the **hottest and coldest countries**
• Detection of **extreme weather events**
• Analysis of **pollution levels by country**
• Identification of **correlations between climate variables**
• Seasonal climate patterns across months

---

## Technologies Used
• Python  
• Streamlit  
• Plotly  
• Pandas  
• NumPy


