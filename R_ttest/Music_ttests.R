user_based <- data.frame(
  precision = c(0.160538, 0.135238, 0.106790),
  recall = c(0.376578, 0.383914, 0.385326),
  f1_score = c(0.210663, 0.182866, 0.146987),
  map = c(0.159807, 0.145565, 0.127938),
  mrr = c(0.508699, 0.451112, 0.371049)
)



item_based <- data.frame(
  precision = c(0.018852, 0.014273, 0.010866),
  recall = c(0.044648, 0.039910, 0.037500),
  f1_score = c(0.024849, 0.019203, 0.014720),
  map = c(0.007825, 0.006341, 0.005627),
  mrr = c(0.570034, 0.572679, 0.573531)
)



# Perform t-tests for all metrics
metrics <- c("precision", "recall", "f1_score", "map", "mrr")
t_tests <- lapply(metrics, function(metric) {
  t.test(user_based[[metric]], item_based[[metric]])
})

# Print results
for (i in seq_along(metrics)) {
  cat("T-test for", metrics[i], ":\n")
  print(t_tests[[i]])
  cat("\n")
}

user_means <- c(0.135238, 0.383914 , 0.182866,  0.145565)
item_means <- c(0.014273,  0.039910,  0.019203,  0.006341)
ttest_metrics <- t.test(user_means, item_means)
ttest_metrics
