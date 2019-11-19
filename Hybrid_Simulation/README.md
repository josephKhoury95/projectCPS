# A Hybrid Human-Machine Arpproach for Cyber-Physical Systems Security

This approach proposes to frame Cyber Physical System (CPS) security in two different levels, strategic and battlefield, by meeting ideas from game theory and Multi-Agent Reinforcement Learning (MARL). The strategic level is modeled as an imperfect information, extensive form game. Here, the human administrator and the virus author decide on the strategies of defense and attack, respectively. At the battlefield level, strategies are implemented by machine learning agents that derive optimal policies for run time decisions. The outcomes of these policies manifest as the utility at the higher level, where we aim to reach a Nash Equilibrium (NE) in favor of the defender. We simulate the scenario of a virus spreading in a realistic CPS network.

-----------------------------

## First.. We present the design of the framework

For better understanding of the designed framework, we illustrate the architecture in the figure below.

<object data="https://josephkhoury95.github.io/Architecture.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://josephkhoury95.github.io/Architecture.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: 
            <a href="https://josephkhoury95.github.io/Architecture.pdf">Download PDF</a>.
        </p>
    </embed>
</object>

The designed framework is a combination between two tools:

1. [OpenAI GYM](https://github.com/openai/gym "openai gym github repo")
2. [MiniCPS](https://github.com/scy-phy/minicps "minicps github repo")

___
Below are the required installation for both OpenAI GYM and MiniCPS:

* [Installation setup for OpenAI GYM](https://github.com/openai/gym#installation "openai gym installation setup")
* [Installation setup for MiniCPS](https://minicps.readthedocs.io/en/latest/userguide.html#installation "minicps installation setup")
