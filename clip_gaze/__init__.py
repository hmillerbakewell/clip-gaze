"""Ask art-related questions about an image, using CLIP.

Given a list of prompts CLIP will calculate the relative likelihood
that each prompt is the "correct" one for the image.
CLIP is provided by OpenAI;

Expected end-points:

    gaze(image, categories) # human-readable
"""

import functools
from typing import *

import transformers
import torch


from .artists_by_name import ARTISTS_BY_NAME
from .artists_by_prevalence import ARTISTS_BY_TRAINING_PREVALENCE
from .movements import MOVEMENTS
from .media import PAINTING_MATERIALS, SCULTPURE_MATERIALS, PRINTING_TECHNIQUES, SURFACES, TOOLS
from .sites import SITES
from .qualities import QUALITIES


@functools.lru_cache()
def model_and_processor():
    """Load and cache the model and pre-processor."""
    model = transformers.CLIPModel.from_pretrained(
        "openai/clip-vit-base-patch32")
    processor = transformers.CLIPProcessor.from_pretrained(
        "openai/clip-vit-base-patch32")
    return model, processor


def image_and_prompts_to_logit_tensor(image: "PIL.Image", prompts: List[str]) -> torch.Tensor:
    """Run CLIP to get a list of scores in logits."""
    if len(prompts) == 0:
        return torch.tensor([[]])
    model, processor = model_and_processor()
    inputs = processor(text=prompts, images=image,
                       return_tensors="pt", padding=True)

    outputs = model(**inputs)

    return outputs.logits_per_image.detach()


def image_and_prompts_to_logit_tensor_by_batch(image: "PIL.Image", prompts: List[str], batch_size: int) -> torch.Tensor:
    """Run CLIP to get a list of scores in logits."""
    collected_tensors = []
    batch_count = 1+(len(prompts) // batch_size)
    for index in range(batch_count):
        # print(f"{index}/{batch_count}")
        collected_tensors.append(image_and_prompts_to_logit_tensor(
            image=image, prompts=prompts[index *
                                         batch_size: (index+1)*batch_size]
        ))

    return torch.cat(collected_tensors, dim=1)


def probabilities(image: "PIL.Image", prompts: List[str], batch_size=10) -> List[Tuple[str, float]]:
    """Batch-run the model and combine the responses to get a probability distribution."""
    assert batch_size > 0, "batch_size should be a positive integer"

    prompt_logits = image_and_prompts_to_logit_tensor_by_batch(
        image, prompts, batch_size=batch_size)[0, :]
    softmax_tensor = torch.softmax(prompt_logits, dim=0)

    return [(prompt, softmax_tensor[index].item())
            for index, prompt in enumerate(prompts)]


EXAMPLE_CATEGORIES = {
    "artist": ARTISTS_BY_TRAINING_PREVALENCE[:200],
    "movement": MOVEMENTS,
    "surface": SURFACES,
}


def gaze(image: "PIL.Image",
         prompts: List[str],
         only_show_best: Optional[int] = 5,
         format_output=True,
         batch_size=10
         ) -> Dict[str, str]:
    """Prompt inferred probabilities in human-readable output."""
    def format_tuple(str_float: Tuple[str, float]) -> str:
        return f"{str_float[0]} ({100*str_float[1]:02.0f}%)"

    prompt_with_prob = probabilities(image=image,
                                     prompts=prompts,
                                     batch_size=batch_size)

    def format_category(prompts_with_probs: List[Tuple[str, float]]):
        entries = [entry for entry in prompts_with_probs]
        entries.sort(key=lambda e: e[1], reverse=True)
        if only_show_best:
            entries = entries[0:only_show_best]
        if format_output:
            entries = list(map(format_tuple, entries))
        return entries

    return format_category(prompt_with_prob)


"""
The MIT License (MIT)

Copyright © 2022 Hex Miller-Bakewell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
