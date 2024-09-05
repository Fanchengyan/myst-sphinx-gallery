# Markdown Image Directive

This is a ``.md`` file with ``image`` directive.
The example thumbnail is selected with ``image`` directive ``alt`` option
being set to ``gallery_thumbnail``.

## without ``alt`` text

````{code-block} markdown
```{image} /_static/barchart.png
   :align: center
   :width: 60%
```
````

```{image} /_static/barchart.png
   :align: center
   :width: 60%
```

## ``alt`` set to ``gallery_thumbnail``

````{code-block} markdown
:emphasize-lines: 3
```{image} /_static/affine.png
   :align: center
   :alt: gallery_thumbnail
   :width: 60%
```
````


```{image} /_static/affine.png
   :align: center
   :alt: gallery_thumbnail
   :width: 60%
```

## ``alt`` set to a random text

````{code-block} markdown
:emphasize-lines: 3
```{image} /_static/bar_colors.png
   :align: center
   :alt: a random text
   :width: 60%
```
````

```{image} /_static/bar_colors.png
   :align: center
   :alt: a random text
   :width: 60%
```
