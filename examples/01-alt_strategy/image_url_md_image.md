# Markdown Image Example

This is an example of images in a markdown to test ``gallery_thumbnail`` for myst ``image`` directive.

Conventional markdown image syntax:

![](/_static/bar_colors.png)

![gallery_thumbnail](/_static/barchart.png)

Image example:

```{image} /_static/affine.png
   :align: center
   :width: 60%
   :alt: gallery_thumbnail
```

Figure example:

```{figure} /_static/rgb.png
   :align: center
   :width: 60%

This is the caption of the figure (a simple paragraph).
```

The image above is a thumbnail of a bar chart.