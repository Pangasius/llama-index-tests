<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">LlamaIndex P-o-C</h3>

<div align="center">


</div>

---

<p align="center"> Introducing the capabilities of LLMs in a controlled environment
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)
- [Example](#🤪-example-of-interaction)

## 🧐 About <a name = "about"></a>

In an investigation on the benefits of using LLMs in a production environment, it appeared that LlamaIndex would be a great contender.

This repository has for purpose to create simple codes to use in a proof-of-concept manner.

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

It is, as always, advised to install libraries and run the code in a contained environment like [conda](https://anaconda.org/).

To run the LLMs, either you have to download your models (see HuggingFace), or use your own OpenAPI keys.

### Installing

The conda environment used to run the chatbot and the tests is present in the file "environment.yml". To load it use :

> [!WARNING]
> This environment contains pip references, only use pip to install further libraries or conda could break.

```
conda env create -f environment.yml
```

By default, the model will be searched in [model/models--openlm-research--open_llama_3b_v2/snapshots/bce5d60d3b0c68318862270ec4e794d83308d80a](https://huggingface.co/openlm-research/open_llama_3b_v2). This is the open-llama-3b-v2 model from HuggingFace, moved to `model` after being downloaded automatically elsewhere. It is highly likely you will need to tweek that.

By default, the querier will search in `examples/F12-FR/available/`. It is highly likely you will need to tweek that.

### Tweeking

Use a custom model by changing `model_path` in `backend/model.py`. 

If you want to use a custom Embedder, change the `embedder` variable in `backend/querier.py`.

> [!NOTE]
> Removing any of the two arguments `llm` or `embed_model` in `service_context` will default to querying OpenAPI. The `querier.py` works with it alone but `chatbot.py` will require your own tinkering.

Change the directory of reference for the construction of the index of `SimpleDirectoryReader` in `backend/querier.py`. There you can also play with the nature of the querier, see other examples in `tests/discord_index.py`.

## 🎈 Usage <a name="usage"></a>

Once installed, you can start using the chatbot by running :

```
python src/main.py
```

### Other things to run

You can run the model locally (port 8080), without querier using :

```
python src/main.py --runnable endpoint
```

Then search for `http://localhost:8080/?prompt=` followed by your prompt.

You can run the querier with a single prompt, defined in the files themselves, by running :

```
python python src/main.py --runnable querier
```
or 
```
python src/main.py --runnable discord_index
```

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>

- [llama-index](https://github.com/jerryjliu/llama_index) - Query tool for LLM
- [llama-hub](https://llamahub.ai/) - Tools on top of llama-index
- [HuggingFace](https://huggingface.co/) - LLM models

## ✍️ Authors <a name = "authors"></a>

- [@Pangasius](https://github.com/Pangasius)

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Much code from [llama-index](https://github.com/jerryjliu/llama_index), [llama-hub](https://llamahub.ai/)

## 🤪 Example of interaction

```
You: What is the densest city in France?
Querying search engine... 
Done.
Answering without query...
Done.
Refining answer with query...
Done.

Chatbot: 
Lyon is the third most populous city in France.



> Source (Doc id: b50c1938-d2f2-4a3c-8050-eec797aee3b9): France (French: [fʁɑ̃s] ), officially the French Republic (French: République française [ʁepyblik...

> Source (Doc id: ce2cc5c3-d360-4e34-8b08-79212894d159): cities having underground or tramway services complementing bus services.
There are approximately...


You: Using the demography statistics of France, give the first densest city.
Querying search engine... 
Done.
Answering without query...
Done.
Refining answer with query...
Done.

Chatbot: 
Using the demography statistics of France, give the first densest city.

The answer is Lyon.
The density in 1997 was 540.0 people per square kilometer. This is the densest city in the world according to the data given.

> Source (Doc id: b50c1938-d2f2-4a3c-8050-eec797aee3b9): France (French: [fʁɑ̃s] ), officially the French Republic (French: République française [ʁepyblik...

> Source (Doc id: 69588a5d-2179-4ae3-a855-6393c5648269): the 2022 Global Innovation Index, compared to 12th in 2020 and 16th in 2019.


== Demographics ==...
```