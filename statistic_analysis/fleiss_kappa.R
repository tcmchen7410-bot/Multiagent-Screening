devtools::install_github("kgwet/irrCAC")#https://github.com/kgwet/pairedCAC
library(irrCAC)
df<- read.csv("~/Desktop/kappa.csv")
fleiss.kappa.raw(df)
