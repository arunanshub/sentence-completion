import pydantic
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from .models import CompletionConfig


class Completion(pydantic.BaseModel):
    sentence: str
    probability: list[float]


class SentenceCompletion:
    def __init__(
        self,
    ) -> None:
        self._model = AutoModelForCausalLM.from_pretrained("distilbert/distilgpt2").to(
            "cuda:0"
        )
        self._tokenizer = AutoTokenizer.from_pretrained("distilbert/distilgpt2")

    def complete_with_scores(
        self,
        sentence: str,
        config: CompletionConfig,
    ) -> list[Completion]:
        inputs = self._tokenizer([sentence], return_tensors="pt").to("cuda:0")

        outputs = self._model.generate(
            **inputs,
            do_sample=True,
            return_dict_in_generate=True,
            output_scores=True,
            pad_token_id=self._tokenizer.eos_token_id,
            min_new_tokens=config.max_new_tokens,
            **config.model_dump(),
        )

        transition_scores = self._model.compute_transition_scores(
            outputs.sequences,
            outputs.scores,
            outputs.beam_indices,
            normalize_logits=True,
        )
        probabilities = F.softmax(transition_scores, dim=1)

        completions = []
        for completed_sentence, probability in zip(
            outputs.sequences, probabilities, strict=True
        ):
            completed_sentence = self._tokenizer.decode(
                completed_sentence,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
            completions.append(
                Completion(
                    sentence=completed_sentence.split(sentence)[-1].strip(),
                    probability=probability.tolist(),
                )
            )
        return completions
