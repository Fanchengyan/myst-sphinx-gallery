# Markdown Figure Directive

This is a ``.md`` file with ``figure`` directive.
The example thumbnail is selected with ``figure`` directive ``alt`` option
being set to ``gallery_thumbnail``.


## without ``alt`` text


````{code-block} markdown
```{figure} /_static/barchart.png
   :align: center
   :width: 60%

This is the caption of the figure (a simple paragraph).
```
````

```{figure} /_static/barchart.png
   :align: center
   :width: 60%

This is the caption of the figure (a simple paragraph).
```


## ``alt`` set to ``gallery_thumbnail``


````{code-block} markdown
:emphasize-lines: 3
```{figure} /_static/affine.png
   :align: center
   :alt: gallery_thumbnail
   :width: 60%

This is the caption of the figure (a simple paragraph).
```
````


```{figure} /_static/affine.png
   :align: center
   :alt: gallery_thumbnail
   :width: 60%

This is the caption of the figure (a simple paragraph).
```

## ``alt`` set to a random text

````{code-block} markdown
:emphasize-lines: 3
```{figure} /_static/bar_colors.png
   :align: center
   :alt: a random text
   :width: 60%

This is the caption of the figure (a simple paragraph).
```
````

```{figure} /_static/bar_colors.png
   :align: center
   :alt: a random text
   :width: 60%

This is the caption of the figure (a simple paragraph).
```
