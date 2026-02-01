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
## Statistical analysis
