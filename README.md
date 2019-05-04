# Final_Project
Title: Factors that affect Crime Rate in Major Cities

Team member: 
Shuang Ke, Yiwen Wang, Xinrong Li


Summary: Chicago is the most populous city in Illinois, it is famous for its fancy skyscrapers, and is also notorious for its high crime rates. The city's overall crime rate, especially the violent crime rate, is higher than the US average. Finding the causes of crime could be the most effective process to reduce the crime rate.


Additional to Chicago, we would also analyze other major cities such as Los Angeles, New York City. We would analyze the relationship between crime and weather factors(temperature, humidity etc.), as well as the relationship between crime and air pollution. By doing this analysis, we can compare and determine which factors have greater impact on each city.


Hypothesis:
1. Temperature could be one of the factors that affect crimes in major cities. The frequency of crime is relatively high in warm seasons and low in cold seasons.
2. Air pollution could be one of the factors that affect crime rate. Server air pollution can trigger physical discomfort which could lead to antisocial behavior and induce aggression, thus increasing the crime rate.
3. The temperature and air pollution might have different effects on different type of crimes, it might have greater effect on personal crimes like assault and have less impact on property crime like theft.


Data source: <br>
crime data: <br>
Chicago: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g  <br>
Los Angeles: https://data.lacity.org/A-Safe-City/Crime-Data-from-2010-to-Present/y8tr-7khq    <br>
New York City: https://catalog.data.gov/dataset/nypd-complaint-data-historic

Weather data: https://www.kaggle.com/selfishgene/historical-hourly-weather-data

Air Pollution data: https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI


Results:

1. The frequency of crime in Chicago shows positive relation with temperature, the scartter plot and the regression results all indicate that the crime count is relatively high in warm seasons and low in cold seasons. We applied the same analysis on Los Angeles and New York, and got the similar results in New York, while in Los Angeles, weather's affect on crime is not that significant.
2. The frequency of crime in Chicago has shows some positive correlation with air pollution. The scartter plot and the regression results all indicate that the crime count is relatively high in higer AQI and low in lower AQI. The correlation is weak but positive. We applied the same analysis on Los Angeles and New York, both show less correlation between air pollution and crime.
3. Although air pollution does not have much correlation with crime rate especially in Los Angeles, the correlation table does show that correlation between ASSAULT and AQI higer than THEFT in all of these three cities.
4. Temperature's effect on different type of crimes are similar, most of crimes have positive relation with temperature, few has negative relation with temperature. 
 <br> <br>
Details shown in the jupyter notebook.
