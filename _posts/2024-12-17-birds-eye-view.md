---
layout: post
title: "Bird's eye view"
subtitle: An interactive representation to see large collection of text "from above".
mathjax: true
excerpt: How do you make sense of a 300-page book in 15 minutes? Or get insights from thousands of news articles without relying on recommendation algorithms?
hide_from_list: false
permalink: birds-eye-view
---

{: .box-note}
You can navigate the map and hover the points, click on a point to display its text on the left. For the best experience, consider viewing on a laptop or desktop.
An online application to create such visualization is available [here](https://birds-eye-view.fly.dev/).

{% include iframe_embed.html 
   container_id="main-plot" 
   iframe_src="/assets/html/birds-eye-view/main.html"
   iframe_width="90%"
%}

How do you make sense of a 300-page book in 15 minutes? Or get insights from thousands of news articles without relying on recommendation algorithms? Our usual approach is to filter: we use search engines, summaries, or recommendations to select a manageable subset of content. But what if we could keep all the content and instead adjust how deeply we engage with each piece?

I created bird's eye view, an interactive visualization tool that lets you explore large collections of text from above, like looking at a landscape from an airplane. Instead of reading sequentially or filtering content, you get a complete view of the document's scope while retaining the ability to zoom into specific areas. This perspective allows you to gradually build understanding at your own pace, moving between high-level semantic clusters and in-depth reading of excerpts.

The tool has already proven valuable for my own use cases for:
- Getting quick insights from large documents or collections
- Exploring AI model outputs at scale for brainstorming
- Qualitatively evaluate LLM benchmarks

This post will first succinctly explain how bird's eye view works, then demonstrate its applications through concrete examples - from exploring Darwin's travel diary to visualizing the MMLU benchmark. We'll then show you how to use the tool yourself, and finally describe how this tool fits in a broader reflexion about the future of AI development.

I encourage you to interact with the visualizations throughout this post - they are the main feature, and exploring them directly will give you a better understanding of the tool than any written description.

The code is [open-source](https://github.com/aVariengien/birds-eye-view), and you can create your own semantic maps using [this web application](https://birds-eye-view.fly.dev/).

# How Bird's Eye View Works

Bird's eye view transforms documents into interactive maps through six steps:

1. **Chunking**: Long documents are split into smaller pieces (around 600 characters each)
2. **Embedding**: Each chunk is converted into a semantic vector using OpenAI embedding API
3. **Dimension Reduction**: UMAP reduces these high-dimensional embeddings to 2D coordinates
4. **Emoji Assignment**: Each point is assigned representative emojis based on its dot product between the chunk embedding and the emoji embeddings.
6. **Visualization**: The result is rendered as an interactive plot where:
    - Points represent chunks of text
    - Position reflects semantic similarity (the axis units are abitrary).
    - Emojis provide quick visual context
    - Lines show document flow

# Exploring Bird's Eye View Through Examples

## Understanding Books and Large Documents

{% include iframe_embed.html 
   container_id="beagle" 
   iframe_src="/assets/html/birds-eye-view/voyage_of_the_beaggle.html" 
   iframe_width="70%"
%}

**Darwin's _Voyage of the Beagle_** by Charles Darwin, a 300-page travel diary of his 1831-1836 expedition in South America that made the biologist famous. The book is split into chunks of around 600 characters long. [Source of the book.](https://www.gutenberg.org/cache/epub/944/pg944-images.html).

The visualization breaks the traditional sequential reading flow, presenting Darwin's travel diary as interconnected clusters. Key themes emerge naturally:
- Animal descriptions cluster on the right (🐢 🦁)
- Geological observations gather on the left (🌋 🗻)
- Fossils descriptions (🦕)
- Travel narratives occupy the center (🚢)
- Historical conflicts and encounters appear at the bottom (🔫)

When interacting with the book this way, you have to make sense of chunks without knowing their content. This disrupts our habits of reading text, where we know what each word is referencing to. So far, I found it was a feature more than a bug, it forced me to focus more on the likely meaning of the sentences, and verifying my hypothesis by navigating forward and backward with the arrow at the bottom.

Beyond just organizing content, this representation might transform how we think about the book. When reading sequentially the book after interacting with bird's eye view, I start to mentally "see" in my mind where the passage belong to this spatial map, adding a new dimension to comprehension.


## Creative Applications with LLMs


**Weekend Activity Brainstorming**. 450 outputs from [deepseek-chat](https://api-docs.deepseek.com/quick_start/pricing) to the prompt "Brainstorm ideas for a weekend that leaves a long-lasting positive effect". I created 50 conversations happening in parallel, for 9 turns. The LLM was prompted to generate ideas significantly different from the ones in the previous turns. Note that `deepseek-chat` has not rate limit, making it suitable for this kind experiments.

{% include iframe_embed.html 
   container_id="weekend" 
   iframe_src="/assets/html/birds-eye-view/weekend_brainstorming.html" 
   iframe_width="70%"
%}

The map reveals meditations-related activities (🧘), sensory explorations (💆), and learning endeavors (🧑‍🎓).

We can see how certain specific suggestions keep appearing across different conversations (such as the time capsule idea 📼, or the no-phone 📵), visible as dense clusters in the visualization. The spatial organization makes it easy to identify creative outliers, and filter out redundant propositions, providing a more efficient way to explore the idea space than reading through sequential lists.

*Other Possible use cases*

The key benefit is that you can afford diversity of LLM outputs. For instance, if a prompting strategy has only 5% chance of giving a good results and is boring or irrelevant in 95% of the cases, it's worth adding to the mix. Bird's eye view significantly reduces the evaluation cost compared to having to judge answers one by one. From there, one can imagine mixing model size, iterative prompting strategy, system prompts, etc.

## Qualitative evaluations of LLM Benchmarks

LLM benchmarks are often succinctly described, and even specialist in the field rarely directly engage with their content. I think this currently prevent LLM users and researcher to form  accurate qualitative judgement to interpret the result of LLM benchmarks.

Bird's eye view help alleviate this limitation by allowing to semantically organize the dataset, and directly engage with the content of the benchmark with little time investement.


**MMLU Dataset**, 7,000 multiple-choice questions from the [test set](https://huggingface.co/datasets/cais/mmlu).

{% include iframe_embed.html 
   container_id="mmlu" 
   iframe_src="/assets/html/birds-eye-view/mmlu.html" 
   iframe_width="70%"
%}

The visualization of this famous benchmark reveals the breadth of topics covered. For instance, medical knowledge clusters in the bottom right of the main cluster (🩺) with a large region dedicated to genetics and molecular biology (🧬), while STEM forms their own clusters on the bottom (⚛️ and ⚗️ for physics and chemistry, 🧮 for math). Economics (📉) is on the left, while law (🧑‍⚖️) is on the top.

Direct visualization of the questions provides a qualitative understanding that complements the usual statistical metrics. One qualitative observation is that many questions test memorized knowledge that don't require significant reasoning.

*Other possible use cases*
The tool opens new possibilities for AI evaluation research beyond benchmarks:
- Supervising LLM agent behavior by visualizing interaction traces
- Evaluating long-form answers by comparing semantic clusters
- Supporting interpretability research by visualizing dataset examples where specific features activate

The next section will show you how to integrate these visualization techniques into your own workflows. 
# How to Use Bird's Eye View

## Web Interface

The simplest way to start is through the [web interface](https://birds-eye-view.fly.dev/) powered by Streamlit. You'll see a simple input field where you can enter URLs of documents you want to visualize. The tool supports:
- HTML format (preferred, preserves rich text)
- PDF documents (text extraction only)
- Plain text files
- JSON files with specific formatting (see the code example below).
In the online app, only web urls are supported. You can use path to local files if you run the app locally!

Processing takes around 30 seconds for a 400-page book. For a quick start, you can explore pre-computed examples from the home menu.

![img](/assets/img/birds-eye-view/interface_screenshot.png)
*Bird's eye view interface*

## Interacting with the Map

Once your visualization is generated, you'll see a scatter plot where each point represents a chunk of text. The visualization offers several ways to explore:

**Basic Navigation**

The light orange lines connect to chunks that come before your selected point in the original text, while dark orange lines point to what comes after. Click any point to display its content in the side panel, then use the arrows below the text to move sequentially through the document.

**Emoji View**

The default view shows emojis representing the content of each region. As you zoom in and out, the visualization adjusts to show the most representative emojis for each area, preventing visual clutter while maintaining context.

**Semantic Search**

The embedding search feature lets you highlight related content across the map. Enter a prompt in the search box, and points will be colored based on their semantic similarity to your query. The coloring uses a sharpened version of the raw similarity scores to enhance contrast.

Search works best with:
- Lists of keywords
- Short descriptive phrases
- Captions that capture the kind of content you're looking for

For example, searching for "A paragraph talking about birds" in Darwin's Voyage clearly highlights regions discussing geese, raptors, and hummingbirds, even when these specific words aren't mentioned.

## Python Interface

For developers and researchers, the Python package offers more flexibility. Here is a minimal example:

```python

from birds_eye_view.core import ChunkCollection

from birds_eye_view.plotting import visualize_chunks

chunks = [
	{
		"text": str(n),
		"number": n,
		"modulo 10": n % 10,
		"quotient 10": n // 10,
	}
	for n in range(1000)
]

collection = ChunkCollection.load_from_list(chunks)
collection.process_chunks()
visualize_chunks(collection, n_connections=0)

```
Install via pip:

```bash
pip install git+https://github.com/aVariengien/birds-eye-view.git
```

The Python interface allows integration with existing workflows and custom data processing pipelines. See the [GitHub repository](https://github.com/aVariengien/birds-eye-view) for detailed documentation and richer examples.

# Current Limitations and Future Development

Bird's eye view remains an early prototype with rough edges. The code is experimental, and the interface needs refinement. Yet even in this state, it demonstrates the value of having alternative ways to access information at scale.

**Epistemic value of bird's eye view.** When we rely solely on filtered information, we miss the context and connections that might challenge our assumptions. Bird's eye view enables discovery of "unknown unknowns" - data points that would have never surfaced through targeted searches or recommendations. 

Several promising directions for development emerge:
1. **Visualisation beyond emojis.** While emojis are fun and provide a good way to visualize collection of text that spans different topics, they become less relevant when analysis corpus with homengenous topics. Possible improvement could be to assign keywords of clusters at different scale.
2. **Beyond Semantic Mapping** The current implementation relies on general semantic embeddings, but we could develop specialized "prisms" for viewing content. Imagine toggling between maps organized by writing style, technical complexity, or chronological relationships.
3. **Comparative Embedding Space** We could anchor new documents in familiar semantic spaces. For instance, when reading a new paper, you could visualize it within a reference space made from a familiar set of papers from the same field. This would leverage your existing mental models to accelerate comprehension of new material.

# The Broader Picture: Building Alternative Futures for AI Development

Bird's eye view points to a broader possibility: AI tools that enhance rather than replace human cognitive practices. Current AI development focuses heavily on increasingly autonomous and general agents. This direction is driven by major AI labs racing towards artificial general intelligence (AGI), motivated by economic incentives and a particular vision of progress.

This narrow focus on agent AI creates an _imagination shortage_ in the field. While the pursuit of increasingly powerful autonomous agents might be the fastest path to transformative AI, it's also a risky one. 

We need alternative development paths that:
- Provide immediate societal benefits that scale safely
- Create tools that augment rather than replace human capabilities
- Foster human connections and improve collective decision-making
- Demonstrate that "AI progress" doesn't have to mean "increasingly autonomous agents"

Current AI tools prioritize immediate ease of use - you can chat with them like a person from day one. This design principle, while valuable, might be blocking exploration of tools that require practice to master. Like musical instruments or programming languages, some tools deliver their full value only after users develop new mental models and ways of thinking. Bird's eye view exemplifies this: it disrupts normal reading patterns but potentially enables new ways of understanding text.

The goal isn't to make tools unnecessarily complex, but to recognize that some valuable capabilities might only emerge through sustained engagement and practice. This approach frames AI systems not just as autonomous entities, but as mediators - "smart pipes" that can:
- Connect humans with each other and with information in novel ways
- Create new cognitive artifacts and ways of thinking
- Increase the bandwidth between humans and machines, leading to better intuitive understanding of their behavior

This suggests an alternative narrative for AI development: instead of racing towards autonomous superintelligent entities, we could build towards a healthy ecosystem of hybrid human-AI cognitive tools. "Healthy" here means a multi-level system that maintains balance through:
- Collective epistemic practices that help us understand the system's dynamics
- Information governance that enables informed collective decision-making
- Technical and social mechanisms to correct course when needed

While major AI labs might continue their current trajectory, developing and demonstrating compelling alternatives could help shift public perception and support towards safer, more beneficial directions for AI progress.