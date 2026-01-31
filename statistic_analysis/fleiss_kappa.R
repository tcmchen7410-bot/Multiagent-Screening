devtools::install_github("kgwet/irrCAC")#https://github.com/kgwet/pairedCAC
library(irrCAC)
df<- read.csv("~/Desktop//kappa.csv")
df <- df[, c(4, 5, 6)]#Select the columns you need to calculate. For agent1, it is 4, 5, and 6. Agent 2 is 7, 8, and 9. Agent 3 is 10, 11, 12
fleiss.kappa.raw(df)
