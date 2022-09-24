# clip-gaze

An art analysis tool powered by CLIP.

## Motivation

Diffusion models (such as [Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release)) used [OpenAI's CLIP](https://openai.com/blog/clip/) in order to perform textual analysis of their training data.
Precisely what these machine learning systems actually learned from their training data is
opaque.
This tool helps us understand how CLIP, and therefore the models that use CLIP,
see images.

## What does it do?

Given an image and a series of (text) phrases it calculates the *relative* likelihood of each phrase to be a good description of the image.
Note that this is not the same thing as "given a text phrase, calculate the accuracy of that phrase".

## An example

Let's show it the painting ["Brücke über die Marne bei Creteil" by Cézanne](https://commons.wikimedia.org/wiki/File:Cezanne_bruecke-ueber-die-marne-bei-creteil.jpg).
If we download the 2,175 × 1,713 pixel version of the painting and open it (e.g. using `PIL.Image.open` from the package `pillow`) as `image` we can then pass it to the `gaze` command.

```python
# Assuming you have already saved the image
import clip_gaze
clip_gaze.gaze(image, clip_gaze.MOVEMENTS)
```

Just looking at the highest probability outputs for `clip_gaze.ARTISTS_BY_TRAINING_PREVALENCE`, `clip_gaze.Movements`, and `clip_gaze.SURFACES` we see:

```python
{'artist': ['by paul cézanne (82%)'], 'movement': ['tonalism movement (16%)'], 'surface': ['on canvas (86%)']}
```

So the terms "by paul cézanne", "tonalism movement", and "on canvas" are the most likely to describe the input image.

For more examples and fuller documentation please see the [project's page on github](https://github.com/hmillerbakewell/clip-gaze).

## How does it work?

CLIP is a tool provided by OpenAI that calculates the similarity between an image and some text.
This is a machine learning system trained on an enormous amount of data,
and that data will contain biases (intentional and unintentional).
**It is not a source of truth, but a useful tool to give you ideas about where to search next.**

This tool works by downloading CLIP onto your computer and running it locally.
This is not an easy task for all computers, especially older ones.
See the "Arguments for `gaze`" section of the project's README for a way to change memory load.

## Biases

This software is built on a machine learning system, and the biases in this tool come in two parts:

1. CLIP itself comes with its own biases, and we refer the user to OpenAI's own work on explaining and mitigating that bias
2. The lists of chosen phrases

The lists used in this software are primarily from Wikipedia and from the training data that CLIP used.
Neither of these sources are perfect, and care should be taken when using this software to account for these biases where possible.
Although the lists are long (e.g. the list of 6000 artists) there are no claims of completeness or relative importance made.
