# Multiagent-Screening
This is a multi-agent approach for screening citations of randomized controlled trials on acupuncture.

The multi-agent framework is built based on the OpenAI SDK framework. We have made public the script for the multi-agent interaction with ChatGpt as well as all the statistical analysis scripts. Our dataset consists of 300 citations from the pretesting stage. Once the paper is officially accepted, we will make the complete dataset publicly available.

## Running the script
1. Set up your Python environment

Python 3.12.10 or newer required. Then, install OpenAI Agents SDK package.
```bash
python -m venv .venv
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
pip install openai-agents
```
2. Set the API Key in the Terminal
```bash
export OPENAI_API_KEY="YOUR API_KEY"
```
3. Set the script

Set the path of the CSV file to be read and the path of the input result in lines 181 and 182 of ```agent.py```. The CSV file in the script is in  ```dataset-sample_size.csv```. The    script is in the ```agent-agent.py```.

4. Run ```agent.py``` in the terminal
```bash
python3 ~/Desktop/agent.py
```
Note！！！！

If a corresponding delay is prompted, it usually does not affect the running result, but it will affect the running speed. Therefore, we suggest running the script in a stable network environment.

5. Results
   
Results can be found in ```results-sample_size_results.csv```.
## Statistical analysis
1. Statistical analysis

① ```smple (300).R``` randomly selected 300 citations from 17,044 for pretesting. The results are obtained in ```result-sample (300).csv```.

② ```Confusion Matrix.R``` is used to count the number of True positives (TP), true negatives (TN), false positives (FP), and false negatives (FN). The CSV file read is ```results-statistic_analysis.csv```.

③ ```performance1.R``` is used to calculate sensitivity, specificity, accuracy and its 95% CI. TP, TN, FP, FN can be obtained from the running result of ```Confusion Matrix.R```.

④ ```performance2.R``` is used to calculate the F1 score and its 95% CI. TP, TN, FP, FN can be obtained from the running result of ```Confusion Matrix.R```.

⑤ ```sample (852).R``` is randomly selected from 17,044 citations, with 5% of the citations (852) being used for stability calculation. The results are available at ```results-sample (852).csv```.

⑥ ```fleiss_kappa.R``` is used to calculate the consistency of 5% citations. The CSV file read is ```results-kappa.csv```

⑦ ```mean_sd.R``` is used to calculate the Mean ± SD. The CSV file read is ```results-statistic_analysis.csv```

2. Plot

① ```plot1.R``` is used to draw bar charts of sensitivity, specificity, accuracy, and F1 index. The data.frame of the script is obtained from the running results of ```performance1.R``` and ```performance2.R```.

② ```plot2.R``` is used to draw the bar chart of consistency among different agents, and the data.frame of the script is obtained from the running result of ```fleiss_kappa.R```.

③ ```plot3.R``` is used to draw bar charts of error situations.
## Contact
Chen Guang

Chengdu University of Traditional Chinese Medicine, China

E-mail: tcm_chen7410@163.com
