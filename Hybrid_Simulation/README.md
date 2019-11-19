# A Hybrid Human-Machine Arpproach for Cyber-Physical Systems Security

This approach proposes to frame Cyber Physical System (CPS) security in two different levels, strategic and battlefield, by meeting ideas from game theory and Multi-Agent Reinforcement Learning (MARL). The strategic level is modeled as an imperfect information, extensive form game. Here, the human administrator and the virus author decide on the strategies of defense and attack, respectively. At the battlefield level, strategies are implemented by machine learning agents that derive optimal policies for run time decisions. The outcomes of these policies manifest as the utility at the higher level, where we aim to reach a Nash Equilibrium (NE) in favor of the defender. We simulate the scenario of a virus spreading in a realistic CPS network.

-----------------------------

## Framework Design

For better understanding of the designed framework, we illustrate the architecture in the figure below.

<object data="https://josephkhoury95.github.io/Architecture.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://josephkhoury95.github.io/Architecture.pdf">
        <p><i>This browser does not support PDFs. Please download the PDF to view it:
            <a href="https://josephkhoury95.github.io/Architecture.pdf">Download PDF</a></i>
        </p>
    </embed>
</object>

The designed framework is a combination between two tools:

1. [MiniCPS](https://github.com/scy-phy/minicps "minicps github repo")
2. [OpenAI GYM](https://github.com/openai/gym "openai gym github repo")

First, the CPS network is created using MiniCPS. It generates a Python file describing the designed network with all its hosts, switches, and links. Second, using OpenAI GYM, we create the environment for the proposed game model, and we define agents strategies. Finally, we feed the network file to the game model, and we apply the [Q-Learning](https://en.wikipedia.org/wiki/Q-learning "q-learning wikipedia") algorithm to derive optimal policies.

___
## Installation Setup
Below are the required installation for both MiniCPS and OpenAI GYM:

* [Installation setup for MiniCPS](https://minicps.readthedocs.io/en/latest/userguide.html#installation "minicps installation setup")
* [Installation setup for OpenAI GYM](https://github.com/openai/gym#installation "openai gym installation setup")

We also present below a link for an article describing how to custom an OpenAI GYM environment:

* [Making a custom environment in gym](https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa "openai gym custom environment")


