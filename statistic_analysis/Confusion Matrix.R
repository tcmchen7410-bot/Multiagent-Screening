#A confusion matrix is used to determine the number of true positives (TP), false positives (FP), false negatives (FN), and true negatives (TN).
df<- read.csv("~/Desktop/statistic_analysis.csv")#statistic_analysis.csv in dataset file
df[, c(4, 7)]#Column of multi-agent results and corresponding gold standard
df <- df[, c(4, 7)]
class(df)
df$agent3 <- factor(df$agent3, levels = c("Yes", "No"))
df$gold_standard <- factor(df$gold_standard, levels = c("Yes", "No"))
table(df$agent3, useNA = "ifany")
table(df$gold_standard, useNA = "ifany")
tab <- table(df$agent3, df$gold_standard)
tab
