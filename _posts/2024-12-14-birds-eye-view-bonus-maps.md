---
layout: post
title: "Bird's eye view - bonus interactive maps."
mathjax: true
hide_from_list: true
---


**500 Canadian News Articles** (July 1-8, 2024) retrieved using the [World News API](https://worldnewsapi.com/docs/). 
{% include iframe_embed.html 
   container_id="canadian" 
   iframe_src="/assets/html/birds-eye-view/canadian_news.html" 
   iframe_width="70%"
%}
The visualization reveals the classic news topics organization. Foreign affairs dominates the bottom of the map, with various national flags (🇺🇸 🇨🇦 🇬🇧) marking international coverage. A dense cluster of sports coverage appears in the middle, with particular emphasis on hockey (🏒). The economic news spreads across the center (💰 📊), while local politics and governance occupies the upper regions (🏛️ 📜).

This bird's eye perspective provides an exhaustive sense of the news landscape without being tied to any particular news source. It's particularly valuable for understanding proportions - seeing how much space each topic occupies in the overall coverage. You can afford to notice topics you might not actively seek out, yet remain aware of their presence in the broader discourse.

**Surprising Cognitive Abilities** (240 outputs from Claude Haiku 3)
The visualization represents 40 parallel conversations of 6 turns each. 

{% include iframe_embed.html 
   container_id="cog" 
   iframe_src="/assets/html/birds-eye-view/what_can_brain_do.html" 
   iframe_width="70%"
%}


**MATH Dataset**. 5,000 problems from [math competitions](https://huggingface.co/datasets/hendrycks/competition_math).

{% include iframe_embed.html 
   container_id="math_dataset" 
   iframe_src="/assets/html/birds-eye-view/math_dataset.html" 
   iframe_width="70%"
%}

Even within mathematics, the semantic embeddings and UMAP reveal meaningful subdivisions. Probability problems cluster together (🎲 📊), while number theory occupies its own region (🔢 ➗). Geometry problems form distinct clusters (📐 ⭕), and trigonometry is attributed an inspiring sunrise emoji 🌄.
