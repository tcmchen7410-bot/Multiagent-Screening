install.packages("ggplot2")
library(ggplot2)
df <- data.frame(
  metric = c("Agent 3", "Agent 2", "Agent 1"),
  estimate = c(95.0, 97.9, 91.6),
  lower = c(92.9,96.7, 89.4),
  upper = c(97.2, 99.1, 93.8),
  y_pos = c(0.8, 1.8, 2.8)
)

fill_colors <- c(
  "Agent 1" = "#2a9d8f",
  "Agent 2"    = "#7fb3b5",
  "Agent 3"    = "#d9e6e6"
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
