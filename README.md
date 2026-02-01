# Multiagent-Screening
This is a multi-agent approach for screening citations of randomized controlled trials on acupuncture.
## Running the script
1. Set up your Python environment (requires Python 3.12.10 or newer required). Then, install OpenAI Agents SDK package.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai-agents
```
2. Set the API Key in the Terminal
```bash
export OPENAI_API_KEY="YOUR API_KEY"
```
3. Set the script

Set the path of the CSV file to be read and the path of the input result in lines 181 and 182 of ```agent.py```. The CSV file in the script is in the dataset file. The script is in the agent file.

4. Run ```agent.py``` in the terminal
```bash
python3 ~/Desktop/agent.py
```
5. Results
结果在results-sample_size_results.csv获取。
## Statistical analysis
1. 统计分析

①```smple (300).R```是从17044引种随机抽取300条引文用于pretesting。结果在results-sample (300).csv获取

②```Confusion Matrix.R```用于统计True positives (TP), true negatives (TN), false positives (FP), false negatives (FN)的数量，读取的CSV文件是：results-statistic_analysis.csv

③```performance1.R```用于计算敏感度，特异性，准确度及其95% CI。TP, TN, FP, FN可以从```Confusion Matrix.R```运行结果获取

④```performance2.R```用于计算F1 score及其95% CI。TP, TN, FP, FN可以从```Confusion Matrix.R```运行结果获取

⑤```sample (852).R```是从17044引种随机抽取5%的引文（852条）用于稳定性的计算。结果在results-sample (852).csv获取

⑥```fleiss_kappa.R```用于计算5%的引文的一致性，读取的CSV文件是：results-kappa.csv

⑦```mean_sd.R```用于计算均数加减标准差，读取的CSV文件是：results-statistic_analysis.csv

2. Plot

①```plot1.R```用于绘制敏感度，特异性，准确度、F1指数的柱状图，脚本的data.frame从```performance1.R```，```performance2.R```运行结果中获取

②```plot2.R```用于绘制不同agent的一致性的柱状图，脚本的data.frame从```fleiss_kappa.R```运行结果中获取

③```plot2.R```用于绘制错误情况的柱状图

