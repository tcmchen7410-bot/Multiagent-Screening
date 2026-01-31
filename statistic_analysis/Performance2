install.packages("boot")
library(boot)
# 1. Values extracted from the results of tab in the confusion matrix
TP <- 45
FP <- 5
FN <- 4
TN <- 246
# 2. Construct observation-level data
boot_data <- data.frame(
  pred = c(rep(1, TP), rep(1, FP), rep(0, FN), rep(0, TN)),
  gold = c(rep(1, TP), rep(0, FP), rep(1, FN), rep(0, TN))
)
# 3. Define the F1 statistical function
f1_stat <- function(data, indices) {
  d <- data[indices, ]
  TP <- sum(d$pred == 1 & d$gold == 1)
  FP <- sum(d$pred == 1 & d$gold == 0)
  FN <- sum(d$pred == 0 & d$gold == 1)
  2 * TP / (2 * TP + FP + FN)
}
# 4. Bootstrap resampling
set.seed(123)
boot_f1 <- boot(
  data = boot_data,
  statistic = f1_stat,
  R = 2000
)
# 5. Calculate the 95% CI (percentile method) using the complete parameter form
f1_ci <- boot.ci(
  boot.out = boot_f1,         # bootstrap object
  conf = 0.95,                
  type = "perc"              # percentile method
)
# 6. Output the F1 point estimation and CI
cat(sprintf("F1 Estimate: %.4f | 95%% CI: [%.4f, %.4f]\n", boot_f1$t0, f1_ci$percent[4], f1_ci$percent[5]))
