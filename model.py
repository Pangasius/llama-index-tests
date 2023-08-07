from typing import Any, List, Mapping, Optional, Sequence
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

from langchain.llms.base import LLM
     
class ModelLLM(LLM) :

    model_path = "./model/models--openlm-research--open_llama_3b_v2/snapshots/bce5d60d3b0c68318862270ec4e794d83308d80a"

    _tokenizer = LlamaTokenizer.from_pretrained(model_path)
    _model = LlamaForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map='auto',
    )
        
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
            stop = ["STOP"]
        stop_ids = self._tokenizer.convert_tokens_to_ids(stop)
        
        input_ids = self._tokenizer.encode(prompt, return_tensors="pt").to(self._model.device)
        output_ids = self._model.generate(
            input_ids=input_ids,
            max_new_tokens=512,
            do_sample=True,
            top_k=10,
            top_p=0.95,
            temperature=0.5,
            pad_token_id=self._tokenizer.eos_token_id,
            eos_token_id=self._tokenizer.eos_token_id,
            early_stopping=True,
            bad_words_ids=[stop_ids],
        )
        output_text = self._tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "path": self.model_path,
        }