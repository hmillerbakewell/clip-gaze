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


def image_and_prompts_to_tensor(image: "PIL.Image", prompts: List[str]) -> torch.Tensor:
    """Run CLIP to get a list of scores in logits."""
    if len(prompts) == 0:
        return torch.tensor([[]])
    model, processor = model_and_processor()
    inputs = processor(text=prompts, images=image,
                       return_tensors="pt", padding=True)

    outputs = model(**inputs)

    return outputs.logits_per_image.detach()


def probabilities(image: "PIL.Image", prompts: List[str], batch_size: int) -> List[Tuple[str, float]]:
    """Batch-run the model and combine the responses to get a probability distribution."""
    computed: List[torch.Tensor] = []
    for i in range(1 + (len(prompts) // batch_size)):
        selection = prompts[i*batch_size:(i+1)*batch_size]
        if len(selection) > 0:
            computed.append(image_and_prompts_to_tensor(
                image, selection))
    probabilitites = torch.cat(computed, dim=1)[0].softmax(0)

    return [(prompt, probabilitites[index].item()) for index, prompt in enumerate(prompts)]


EXAMPLE_CATEGORIES = {
    "artist": ARTISTS_BY_TRAINING_PREVALENCE[:200],
    "movement": MOVEMENTS,
    "surface": SURFACES,
}


def gaze(image: "PIL.Image",
         prompt_categories: Dict[str, List[str]],
         batch_size=10,
         only_show_best: Optional[int] = 5,
         format_output=True,
         ) -> Dict[str, str]:
    """By-category probabilities in human-readable output."""
    assert batch_size > 0, "Batch size must be at least 1"

    def format_tuple(str_float: Tuple[str, float]) -> str:
        return f"{str_float[0]} ({100*str_float[1]:02.0f}%)"

    def order_list_by_category(prompts) -> List[str]:

        prompt_with_prob = probabilities(image=image,
                                         prompts=prompts,
                                         batch_size=batch_size)

        prompt_with_prob.sort(
            key=lambda str_float_tuple: str_float_tuple[1], reverse=True)

        if only_show_best:
            prompt_with_prob = prompt_with_prob[0:only_show_best]
        if format_output:
            return list(map(format_tuple, prompt_with_prob))
        return prompt_with_prob

    return {category: order_list_by_category(prompt_categories[category]) for category in prompt_categories}


"""
The MIT License (MIT)

Copyright © 2022 Hex Miller-Bakewell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
