# 1. 设定随机种子（投稿必备：确保审稿人能复现你的随机结果）
set.seed(123) 

# 2. 从 1 到 10744 的序列中，无放回地随机抽取 500 个编号
selected_ids <- sample(1:10744, 300)

# 3. 对编号进行升序排列（方便后续在数据库中查找）
selected_ids <- sort(selected_ids)
write.csv(selected_ids, "~/Desktop/sampled_literature_ids.csv", row.names = FALSE)
