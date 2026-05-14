---
permalink: /
title: "Me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I'm a rising 3rd-year PhD Student at UC San Diego, advised by [Dr. Prithviraj Ammanabrolu](https://prithvirajva.com/) in the [PEARLS](https://pearls-lab.github.io/) Lab, united in our love for boba tea and our interest in embodied RL agents and interactive, human-aligned AI systems.

In general, I am interested in all things Natural Language Processing (NLP), Reinforcement Learning (RL), and any systems that collaborate with people to improve the human experience as a whole.

Most of my current work centers on the reasoning capabilities of LLMs, especially in multi-turn agentic settings, where the standard paradigm of "burn tokens until something happens" can actually hurt performance. I think about how to make reasoning *monitorable* and *controllable* from the outside, how to train agents that can recover from their own bad reasoning, and how to stress-test what current LLMs can and can't do as agents in text environments.

This summer (June–August 2026), I'll be interning at **Microsoft Research Montréal** with [Marc-Alexandre Côté](https://www.microsoft.com/en-us/research/people/macote/) and [Xingdi "Eric" Yuan](https://www.microsoft.com/en-us/research/people/xinyuan/), continuing our collaboration on LLM agents and situated text environments.

Prior to UCSD, I did my Master's at the Georgia Institute of Technology under the guidance of Dr. Thad Starner and Dr. Mark Riedl. I also had the privilege of serving as a Head Graduate Teaching Assistant for Dr. Thomas Ploetz — although our research interests didn't end up aligning, he was a mentor and friend whose influence is a big part of why I chose to pursue a PhD in the first place.

## Research Highlights:

**[Behavior Cue Reasoning: Monitorable Reasoning Improves Efficiency and Safety through Oversight](https://arxiv.org/abs/2605.07021)** (Cui, Killian, Ammanabrolu — pre-print)

Can we train an LLM to anchor specific reasoning behaviors — *continue thinking*, *stop and answer*, *return a final action* — to special token sequences ("behavior cues")? Turns out yes: doing so makes chain-of-thought reasoning monitorable and externally controllable, cuts wasted reasoning tokens by up to 50% under an efficiency objective, and more than doubles success rate under a safety-constrained objective by recovering safe actions from otherwise-unsafe reasoning traces 80% of the time.

**[TALES: Text Adventure Learning Environment Suite](https://microsoft.github.io/tale-suite/)** (Cui, Yuan, Xiao, Ammanabrolu, Côté — Oral, REALM 2025)

A progressive stress test of LLMs' baseline agentic capabilities, spanning 122 tasks across which we benchmarked 49 models. Curious whether you're better than an LLM at a text adventure game? Check out the TALES page and click on the 'Environments' tab to try Zork1 yourself.

**[Socratic Mind](https://socraticmind.com)** — Research Lead

Using foundation models to conduct scalable, interactive oral assessments. Our work was chosen as a winner of the [2023–24 Tools Competition](https://tools-competition.org/23-24-accelerating-and-assessing-learning-winners/#:~:text=students%20with%20disabilities.-,Socratic%20Mind,-%7C%20Socratic%20Mind%20Inc); the tool has since garnered interest from 15+ professors across 7 universities and served over 1,000 students. Try a demo [here](https://socraticmind.com).

---

Check out the other [cool stuff my labmates are working on](https://pearls-lab.github.io/people/)!



