# Hybrid Human-Machine Arpproach

This approach work proposes to frame CPS security in two different levels, strategic and battlefield, by meeting ideas from game theory and Multi-Agent Reinforcement Learning (MARL). The strategic level is modeled as an imperfect information, extensive form game. Here, the human administrator and the virus author decide on the strategies of defense and attack, respectively. At the battlefield level, strategies are implemented by machine learning agents that derive optimal policies for run time decisions. The outcomes of these policies manifest as the utility at the higher level, where we aim to reach a Nash Equilibrium (NE) in favor of the defender. We simulate the scenario of a virus spreading in a realistic CPS network.

In this approach we use two tools:

1. [OpenAI GYM](https://github.com/openai/gym "gym github repo")
2. [MiniCPS](https://github.com/scy-phy/minicps "minicps github repo")
