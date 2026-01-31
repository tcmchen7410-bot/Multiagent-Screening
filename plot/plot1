install.packages("ggplot2")
library(ggplot2)
df <- data.frame(
  metric = c("F1 Score", "Accuracy", "Specificity", "Sensitivity"),
  estimate = c(93.7, 97.2, 97.6, 95.8),
  lower = c(93.1,96.9, 97.3, 95.1),
  upper = c(94.2, 97.4, 97.8, 96.4),
  y_pos = c(0.8, 1.8, 2.8, 3.8)
)
fill_colors <- c(
  "Sensitivity" = "#007f7f",
  "Specificity" = "#2a9d8f",
  "Accuracy"    = "#7fb3b5",
  "F1 Score"    = "#d9e6e6"
)
ggplot(df, aes(x = estimate, y = y_pos)) +
  geom_col(
    aes(fill = metric),
    orientation = "y",
    width = 0.6,
    color = "black",
    linewidth = 0.3
  ) +
  geom_errorbarh(
    aes(
      xmin = lower,
      xmax = upper
    ),
    height = 0.2,
    linewidth = 0.3,
    color = "black"
  ) +
  geom_text(
    aes(
      x = estimate / 2,  
      label = sprintf("%.1f%% (95%% CI, %.1f%%–%.1f%%)", estimate, lower, upper)
    ),
    color = "black",      
    size = 3.5,
    fontface = "bold",
    hjust = 0.5           
  ) +
  scale_y_continuous(
    breaks = df$y_pos,
    labels = df$metric,
    expand = expansion(add = c(0.2, 0.2))
  ) +
  scale_fill_manual(values = fill_colors) +
  scale_x_continuous(
    limits = c(0, 102),
    breaks = seq(0, 100, by = 20),
    expand = c(0, 0)
  ) +
  labs(x = "Percentage (%)", y = NULL) +
  theme_classic(base_size = 12) +
  theme(
    legend.position = "none",
    # Bolden the coordinate axes
    axis.line = element_line(linewidth = 0.3, color = "black"),
    axis.ticks = element_line(linewidth = 0.3, color = "black"),
    axis.ticks.length = unit(0.2, "cm"),
    # Font-style
    axis.text.y = element_text(color = "black", face = "bold", size = 12),
    axis.text.x = element_text(color = "black", face = "bold", size = 12),
    axis.title.x = element_text(face = "bold", size = 12, margin = margin(t = 15)),
    plot.margin = margin(20, 40, 20, 20)
  )
