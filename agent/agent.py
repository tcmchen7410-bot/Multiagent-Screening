import asyncio
import csv
import os
import time
from typing import Any, Tuple
from agents import Agent, Runner, trace

# ==================== Model configuration ====================
acupuncture_agent = Agent(
    name="acupuncture_agent",
    instructions=(
        """You are an acupuncture expert. The following is an excerpt of two sets of criteria, A study is considered included if it meets all the inclusion criteria, If a study meets any of the exclusion criteria, it should be excluded. Here are the two sets of criteria:
Inclusion criteria
-Interventions include acupuncture, electroacupuncture, dry needling, and needling.
-Also consider acupoint stimulation or acupoint electrical stimulation, which may indicate acupuncture or electroacupuncture.
Exclusion Criteria
The following acupoint interventions will be excluded.
-Invasive interventions
acupotomy/acupotome, acupoint catgut embedding, electrothermal acupuncture, warm needling, acupoint injection, fire needling, acupuncture bloodletting, intradermal needle, press needle, thumbtack needle, bee venom acupuncture, rolling needle, etc.
-Non-invasive interventions
laser acupuncture, moxibustion (any type), tuina/massage/acupressure, TENS, gua sha, cupping, plum-blossom needling, acupoint application, transcranial magnetic stimulation (TMS), etc.
-Other interventions
Whether it is an invasive intervention or not: auricular acupuncture/ear acupoints, electromagnetic acupuncture, etc.
We now assess whether the paper should be included in the systematic review by evaluating it against each and every predefined inclusion and exclusion criterion. First, we will reflect on how we will decide whether a paper should be included or excluded. Then, we will think step by step for each criterion, giving reasons for why they are met or not met.
Studies that may not fully align with the primary focus of our inclusion criteria but provide data or insights potentially relevant to our review deserve thoughtful consideration. Given the nature of abstracts as concise summaries of comprehensive research, some degree of interpretation is necessary.
Our aim should be to inclusively screen abstracts, ensuring broad coverage of pertinent studies while filtering out those that are clearly irrelevant. We will conclude by outputting (on the very last line) ‘No’ if the paper warrants exclusion, or ‘Yes’ if inclusion is advised or uncertainty persists. We must output either ‘No’ or ‘Yes’."""
    ),
    output_type=str,
    model="gpt-5",
)

rct_agent = Agent(
    name="rct_agent",
    instructions=(
        """You are an evidence-based medicine expert. The following is an excerpt of two sets of criteria, A study is considered included if it meets all the inclusion criteria, If a study meets any of the exclusion criteria, it should be excluded. Here are the two sets of criteria:
Exclusion Criteria
-Non-clinical studies: reviews, animal experiments, letters, comments, meta-analyses, study protocols, clinical guidelines, qualitative studies, bibliometric studies, etc.
-Non-randomized studies: cohort studies, cross-sectional studies, case-control studies, case reports, retrospective studies, single-arm studies, or matched studies with predictable group allocation.
-Other types of randomized trials: pragmatic RCTs, randomized crossover studies, cluster randomized trials, etc.
Inclusion criteria
Describe as two or more groups, regardless of whether random allocation is explicitly indicated, even if the group sizes are unequal.
We now assess whether the paper should be included in the systematic review by evaluating it against each and every predefined inclusion and exclusion criterion. First, we will reflect on how we will decide whether a paper should be included or excluded. Then, we will think step by step for each criterion, giving reasons for why they are met or not met.
Studies that may not fully align with the primary focus of our inclusion criteria but provide data or insights potentially relevant to our review deserve thoughtful consideration. Given the nature of abstracts as concise summaries of comprehensive research, some degree of interpretation is necessary.
Our aim should be to inclusively screen abstracts, ensuring broad coverage of pertinent studies while filtering out those that are clearly irrelevant. We will conclude by outputting (on the very last line) ‘No’ if the paper warrants exclusion, or ‘Yes’ if inclusion is advised or uncertainty persists. We must output either ‘No’ or ‘Yes’."""
    ),
    output_type=str,
    model="gpt-5",
)

coordinator_agent = Agent(
    name="coordinator_agent",
    instructions=(
        """You are a coordinator. Based on the input: is_acupuncture, is_rct.
Here, is_acupuncture indicates whether the intervention is acupuncture (Yes/No),
and is_rct indicates whether it is a randomized controlled trial (Yes/No).

Decision logic: 
- If both is_acupuncture and is_rct are Yes, the final decision is Yes;
- Otherwise, the final decision is No.

IMPORTANT: Only output 'Yes' or 'No' — nothing else, no explanation, no punctuation."""
    ),
    output_type=str,
    model="gpt-4o-mini",
)

# ==================== asynchronous call ====================
SEM_LIMIT = 10
sem = asyncio.Semaphore(SEM_LIMIT)


# ==================== tool function ====================
def get_usage_value(usage_obj: Any, fields: list[str]) -> int:
    """Extract the value of the specified field from the usage object"""
    # Try attribute access
    for field in fields:
        if hasattr(usage_obj, field):
            try:
                val = getattr(usage_obj, field)
                if val is not None:
                    return int(val)
            except (ValueError, TypeError):
                continue
    
    # Try dictionary access
    if isinstance(usage_obj, dict):
        for field in fields:
            if field in usage_obj and usage_obj[field] is not None:
                try:
                    return int(usage_obj[field])
                except (ValueError, TypeError):
                    continue
    
    # Try __dict__ access
    if hasattr(usage_obj, "__dict__"):
        for field in fields:
            if field in usage_obj.__dict__ and usage_obj.__dict__[field] is not None:
                try:
                    return int(usage_obj.__dict__[field])
                except (ValueError, TypeError):
                    continue
    
    return 0


def usage_or_zero(res: Any, fields: list[str]) -> int:
    """Extract the usage information from the results"""
    # Check context_wrapper.usage first（The standard way of the ModelContext agents library）
    if hasattr(res, "context_wrapper") and res.context_wrapper:
        if hasattr(res.context_wrapper, "usage") and res.context_wrapper.usage:
            return get_usage_value(res.context_wrapper.usage, fields)
    
    # Backward compatibility: Check res.usage
    if hasattr(res, "usage") and res.usage:
        usage = res.usage if isinstance(res.usage, dict) else getattr(res.usage, "__dict__", {})
        return get_usage_value(usage, fields)
    
    # Finally, check res.__dict__
    if hasattr(res, "__dict__"):
        usage = res.__dict__.get("usage")
        if usage:
            return get_usage_value(usage, fields)
    
    return 0


async def run_agent(agent: Agent, content: str) -> Tuple[Any, float]:
    """Run the agent and return the result and the actual processing time (excluding the time spent waiting for the semaphore)"""
    async with sem:
        t_start = time.monotonic()
        result = await Runner.run(agent, content)
        t_end = time.monotonic()
        return result, round(t_end - t_start, 3)


async def process_row(row: list[str]) -> dict:
    """Process single-row data"""
    paper_id, title, abstract = row[0], row[1], row[2]
    text = f"ID: {paper_id}\nTitle: {title}\nAbstract: {abstract}"

    with trace(f"paper-{paper_id}"):
        # Run three agents
        acu_res, latency_agent1 = await run_agent(acupuncture_agent, text)
        rct_res, latency_agent2 = await run_agent(rct_agent, text)
        
        coord_input = (
            f"{text}\n"
            f"is_acupuncture: {acu_res.final_output.strip()}\n"
            f"is_rct: {rct_res.final_output.strip()}"
        )
        coord_res, latency_agent3 = await run_agent(coordinator_agent, coord_input)
    
    # Calculate the total processing time (the sum of the actual processing times of the three agents)
    latency_total = round(latency_agent1 + latency_agent2 + latency_agent3, 3)
    
    # Extract token information
    results = [acu_res, rct_res, coord_res]
    total_tokens = sum(usage_or_zero(r, ["total_tokens"]) for r in results)
    completion_tokens = sum(usage_or_zero(r, ["output_tokens", "completion_tokens"]) for r in results)
    prompt_tokens = sum(usage_or_zero(r, ["input_tokens", "prompt_tokens"]) for r in results)

    return {
        "id": paper_id,
        "title": title,
        "abstract": abstract,
        "agent1": acu_res.final_output.strip(),
        "agent2": rct_res.final_output.strip(),
        "agent3": coord_res.final_output.strip(),
        "latency_seconds": latency_total,
        "latency_agent1": latency_agent1,
        "latency_agent2": latency_agent2,
        "latency_agent3": latency_agent3,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


async def main():
    """Main function"""
    desktop_path = os.path.expanduser("~/Desktop/1111.csv")#File reading path
    out_path = os.path.expanduser("~/Desktop/papers_results.csv")#File output path
    
    # Read data
    print(f"Reading the file: {desktop_path}")
    tasks = []
    
    with open(desktop_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        first_row = next(reader, None)
        
        # Check and skip the header
        if first_row and any(cell.lower() in ("id", "title", "abstract") for cell in first_row):
            print("The header has been detected and skipped")
        elif first_row:
            tasks.append(process_row(first_row))
        
        # Add the remaining lines
        for row in reader:
            if len(row) >= 3:
                tasks.append(process_row(row))
    
    print(f"total {len(tasks)} a piece of data is pending processing. Start processing...")
    
    # Handle all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Write the result
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "title", "abstract",
            "agent1", "agent2", "agent3",
            "latency_seconds", "latency_agent1", "latency_agent2", "latency_agent3",
            "prompt_tokens", "completion_tokens", "total_tokens",
        ])
        for r in results:
            writer.writerow([
                r["id"], r["title"], r["abstract"],
                r["agent1"], r["agent2"], r["agent3"],
                r["latency_seconds"], r["latency_agent1"], r["latency_agent2"], r["latency_agent3"],
                r["prompt_tokens"], r["completion_tokens"], r["total_tokens"],
            ])
    
    # Print statistical information
    print(f"\nProcessing completed! The result has been output to: {out_path}")
    print(f"\nToken Use statistics:")
    print(f"  total prompt tokens: {sum(r['prompt_tokens'] for r in results):,}")
    print(f"  total completion tokens: {sum(r['completion_tokens'] for r in results):,}")
    print(f"  total tokens: {sum(r['total_tokens'] for r in results):,}")


if __name__ == "__main__":
    asyncio.run(main())
