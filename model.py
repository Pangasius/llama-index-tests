from typing import Any, List, Mapping, Optional
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

from langchain.llms.base import LLM

from singleton import Singleton

def convert_tokens_to_ids(tokens):
    return ModelLoader().tokenizer.convert_tokens_to_ids(tokens)

def encode(text):
    return ModelLoader().tokenizer.encode(text, return_tensors="pt", max_length=2048, truncation=True).to(ModelLoader().model.device)

def generate(input_ids, stop_ids):
    model = ModelLoader().model
    
    output_ids = model.generate(
        input_ids=input_ids,
        max_new_tokens=256,
        do_sample=True,
        top_k=10,
        top_p=0.95,
        temperature=0.9,
        pad_token_id=model.config.pad_token_id,
        eos_token_id=model.config.eos_token_id,
        early_stopping=True,
        bad_words_ids=[stop_ids],
    )
    return output_ids

def decode(ids):
    return ModelLoader().tokenizer.decode(ids[0], skip_special_tokens=True)
    
class ModelLoader(metaclass=Singleton):
    model_path = "./model/models--openlm-research--open_llama_3b_v2/snapshots/bce5d60d3b0c68318862270ec4e794d83308d80a"
    
    model = LlamaForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map='auto',
    )

    tokenizer = LlamaTokenizer.from_pretrained(model_path)

class ModelLLM(LLM) :
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is None:
            stop = ["Q: "]
        stop_ids = convert_tokens_to_ids(stop)
        
        input_ids = encode(prompt)
        output_ids = generate(input_ids, stop_ids)
        output_text = decode(output_ids)
        return output_text[len(prompt):]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "path": ModelLoader().model_path,
        }