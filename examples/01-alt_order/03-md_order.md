# Markdown Image

This is a ``.md`` gallery example with image URLs in the rst file to test ``gallery_thumbnail``. 

Conventional markdown image syntax:

```markdown
![](/_static/bar_colors.png)
```

![](/_static/bar_colors.png)


Image with ``alt`` text:
```markdown
![a random text](/_static/barchart.png)
```

![a random text](/_static/barchart.png)

Image example:

````markdown
```{image} /_static/bar_colors.png
   :align: center
```
````

```{image} /_static/rgb.png
   :align: center
   :width: 60%
```


Figure example:


````markdown
```{figure} /_static/rgb.png
   :align: center

This is the caption of the figure.
```
````


:::{note}
This figure directive has set the ``alt`` attribute to ``gallery_thumbnail``. Therefore, This image will be used as the thumbnail for the gallery.
:::


```{figure} /_static/affine.png
   :align: center
   :alt: gallery_thumbnail
   :width: 60%

This is the caption of the figure (a simple paragraph).
```