# Multiagent-Screening
This is a multi-agent approach for screening citations of randomized controlled trials on acupuncture.
## 运行调用脚本
1. 设置您的 Python 环境（需要 Python 3.9 或更高版本），然后安装 OpenAI Agents SDK：
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai-agents
```
2.	在终端设置API Key：
```bash
export OPENAI_API_KEY="YOUR API_KEY"
```
3. ```agent.py```设置需要读取的CSV文件的路径，已经输入结果的路径
4. 在终端运行```agent.py```
