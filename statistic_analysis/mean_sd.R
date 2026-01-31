install.packages("psych")
library(psych)
df<- read.csv("~/Desktop/statistic_analysis.csv")
describe(df[[9]])#Select the columns to be analyzed for statistics
