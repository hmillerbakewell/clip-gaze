r"""All the code for running CLIP, handling tensors, and so on."""

import functools
from typing import *

import transformers
import torch
import logging


@functools.lru_cache()
def model_and_processor(device: str) -> Tuple[transformers.CLIPModel, transformers.CLIPProcessor]:
    """Load and cache the model and pre-processor."""
    logging.info("Initialising the model.")
    model = transformers.CLIPModel.from_pretrained(
        "openai/clip-vit-base-patch32")
    processor = transformers.CLIPProcessor.from_pretrained(
        "openai/clip-vit-base-patch32")
    model.to(device)
    return model, processor


def image_and_prompts_to_logit_tensor(image: "PIL.Image", prompts: List[str], device: str) -> torch.Tensor:
    """Run CLIP to get a list of scores in logits."""
    if len(prompts) == 0:
        return torch.tensor([]).to(device)
    model, processor = model_and_processor(device)
    inputs = processor(text=prompts, images=image,
                       return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(
            **{key: inputs[key].to(device) for key in inputs.keys()}
        )

    return outputs.logits_per_image.detach().squeeze()


def image_and_prompts_to_logit_tensor_by_batch(image: "PIL.Image", prompts: List[str], batch_size: int, device: str) -> torch.Tensor:
    """Run CLIP to get a list of scores in logits."""
    batch_count = 1+(len(prompts) // batch_size)
    collected = []
    for index in range(batch_count):
        # print(f"{index}/{batch_count}")
        processed_batch = image_and_prompts_to_logit_tensor(
            image=image,
            prompts=prompts[index * batch_size: (index+1)*batch_size],
            device=device
        )
        collected.append(processed_batch)
    return torch.cat(collected)


def probabilities(image: "PIL.Image", prompts: List[str], batch_size: Optional[int] = None, device: str = "cuda") -> List[Tuple[str, float]]:
    """Check all the prompts and construct a probability distribution.

    Defaults to trying to run on the gpu (`device="cuda"`),
    but will fall back to using the cpu if cuda is not available.

    If you run out of memory then try batch runs by setting the batch_size.
    """
    if device == "cuda" and not torch.cuda.is_available():
        logging.error(
            "You have requested device='cuda', but cuda has not been found by torch.")
        logging.info("Switching to cpu.")
        device = "cpu"

    if batch_size is None:
        prompt_logits = image_and_prompts_to_logit_tensor(
            image, prompts, device=device)
    else:
        prompt_logits = image_and_prompts_to_logit_tensor_by_batch(
            image, prompts, batch_size=batch_size, device=device)

    softmax_tensor = torch.softmax(prompt_logits, dim=0)

    return [(prompt, softmax_tensor[index].item())
            for index, prompt in enumerate(prompts)]


def format_tuple(str_float: Tuple[str, float]) -> str:
    """Make a probability human readable."""
    return f"{str_float[0]} ({100*str_float[1]:02.0f}%)"


def gaze(image: "PIL.Image",
         prompts: List[str],
         only_show_best: Optional[int] = 5,
         format_output=True,
         **kwargs
         ) -> Dict[str, str]:
    """Prompt inferred probabilities in human-readable output.

    Unused keyword arguments are passed to `probabilities`.
    """
    if torch.cuda.is_available():
        defaults = {"device": "cuda", "batch_size": None}
    else:
        defaults = {"device": "cpu", "batch_size": None}

    prompt_with_prob = probabilities(image=image,
                                     prompts=prompts,
                                     **{**defaults, **kwargs})

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
