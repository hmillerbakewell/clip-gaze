# clip-gaze

An art analysis tool powered by CLIP.

## What does it do?

Given an image and a series of (text) phrases it calculates the *relative* likelihood of each phrase to be a good description of the image.
Note that this is not the same thing as "given a text phrase, calculate the accuracy of that phrase".

## An example

Let's show it the painting ["Brücke über die Marne bei Creteil" by Cézanne](https://commons.wikimedia.org/wiki/File:Cezanne_bruecke-ueber-die-marne-bei-creteil.jpg).
If we download the 2,175 × 1,713 pixel version of the painting and open it (e.g. using `PIL.Image.open` from the package `pillow`) as `image` we can then pass it to the `gaze` command.

```python
# Assuming you have already saved the image
from clip_gaze import gaze, EXAMPLE_CATEGORIES
gaze(image, EXAMPLE_CATEGORIES)
```

The expected output is below.
If you downloaded a different resolution version of the file you will get slightly different results,
and I also tidied up the output using `pprint`.

```python
{'artist': ['by paul cézanne (82%)',
            'by clyfford still (07%)',
            'by arnold böcklin (04%)',
            'by franz kline (01%)',
            'by giorgio de chirico (01%)'],
 'movement': ['tonalism movement (16%)',
              'impressionism movement (09%)',
              'american scene painting movement (09%)',
              'modern european ink painting movement (09%)',
              'post-impressionism movement (09%)'],
 'surface': ['on canvas (86%)',
             'on paperboard (11%)',
             'on vellum (01%)',
             'on wood (01%)',
             'on card stock (00%)']}
```

What was in `EXAMPLE_CATEGORIES`?

```python
# The second argument to `gaze` is just a dictionary of (category name) -> (list of strings)
EXAMPLE_CATEGORIES = {
    "artist": ARTISTS_BY_TRAINING_PREVALENCE[:200],
    "movement": MOVEMENTS,
    "surface": SURFACES,
}
```

The example categories we passed to `gaze` only checks 200 artists,
and these artists are listed in order of prevalence in CLIP's training data.
`gaze` works by having CLIP assess the *relative* likelihood of the options within each category.
Here is a table of lists built into the module.

| Variable | Description | Example |
|----|----|----|
| ARTISTS_BY_NAME | List of **5000 artists** in alphabetical order. | Sandra Chevrier |
| ARTISTS_BY_TRAINING_PREVALENCE | List of **900 artists** in the order of prevalence in the training data (most prevalent first). Sometimes the most famous artists are credited *without* a first name, and so you may find those as separate entries alongside their full name. | Sandra Chevrier |
| MOVEMENTS | Artistic movement | Afrofuturism |
| PAINTING_MATERIALS | Materials for creating paintings | Acrylic Paint |
| PRINTING_TECHNIQUES | Technique for creating an impression | Aquatint |
| QUALITIES | Subjective (even more-so than the others) assessment of artwork | Exceptional |
| SCULTPURE_MATERIALS | Material that is sculpted into artwork | Bronze |
| SITES | Art websites, each of which have their own tastes (and phrasing) | Popular on Reddit |
| SURFACES | Material to which the artistic material is applied | Canvas |
| TOOLS | Object this is used to apply the material to the surface | Brush |

For example:

```python
clip_gaze.MOVEMENTS # A list of the prompts describing art history movements
```

### Arguments for `gaze`

| Argument | Description | Default |
|----|----|----|
| image | The image to inspect | *Required* |
| prompt_categories | A dictionary of (categories) -> (prompts in that category) | *Required* |
| batch_size | How many prompts to inspect at once. This is set intentionally low; increase it to trade memory resources for speed | `10` |
| only_show_best | Show only this many results in each category, set it to `None` for no limit | `3` |
| format_output | Turn the output into something easier for people to read (e.g. percentage in brackets) | `True` |

### Finer control

The `clip_gaze.gaze` command wraps multiple calls to `clip_gaze.probabilities`, selecting the highest-probabilitiy options and formatting text.
If you want raw results based on just one list of prompts then you can skip using `gaze` and instead use:

```python
# Type probabilities(image: "PIL.Image", prompts: List[str], batch_size: int) -> List[Tuple[str, float]]
probabilities(image, cip_gaze.ARTISTS, 10)

# Returns the probability score for all 900 or so artists in the list
```

## How does it work?

CLIP is a tool provided by OpenAI that calculates the similarity between an image and some text.
This is a machine learning system trained on an enormous amount of data,
and that data will contain biases (intentional and unintentional).
**It is not a source of truth, but a useful tool to give you ideas about where to search next.**

This tool works by downloading CLIP onto your computer and running it locally.
This is not an easy task for all computers, especially older ones.

## Biases

As mentioned above this software is a machine learning system, and the biases in this tool comes in two parts:

1. CLIP itself comes with its own biases, and we refer the user to OpenAI's own work on explaining and mitigating that bias
2. The lists of chosen phrases

The lists used in this software are primarily from Wikipedia and from the training data that CLIP used.
Neither of these sources are perfect, and care should be taken when using this software to account for these biases where possible.
Although the lists are long (e.g. the list of 5000 artists) there are no claims of completeness or relative importance made.
