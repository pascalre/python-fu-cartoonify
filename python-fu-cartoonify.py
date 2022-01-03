#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *


def apply_cartoon_filter(img, drawable):
    # docs
    # https://developer.gimp.org/api/2.0/libgimp/index.html
    # https://developer.gimp.org/api/2.0/libgimp/libgimp-gimpenums.html#GimpLayerModeEffects
    pdb.gimp_image_undo_group_start(img)
    # step 1: duplicate layer two times
    # layer2
    layer2 = pdb.gimp_layer_copy(drawable, False)
    pdb.gimp_image_add_layer(img, layer2, 0)
    pdb.gimp_item_set_name(layer2, "temp_merge_layer")

    # layer3
    layer3 = pdb.gimp_layer_copy(drawable, False)
    pdb.gimp_image_add_layer(img, layer3, 0)
    pdb.gimp_item_set_name(layer3, "temp_sobel_operator")
    # set layer3 mode to GIMP_GRAIN_EXTRACT_MODE (20)
    pdb.gimp_layer_set_mode(layer3, 20)

    # step 2: execute sobel operator
    # alternative pdb.plug_in_sobel(img, layer3, True, True, True)
    pdb.plug_in_edge(img, layer3, 1, 0, 0)

    # step 3: adjust curves
    # https://developer.gimp.org/api/2.0/libgimp/libgimp-gimpcolor.html#gimp-curves-spline
    pdb.gimp_curves_spline(layer3, 0, 6,
                           [0, 0,
                            130, 255,
                            255, 255])

    # step 4: adjust levels
    # https://developer.gimp.org/api/2.0/libgimp/libgimp-gimpcolor.html#gimp-levels
    pdb.gimp_levels(layer3, 0, 0, 130, 1.0, 0, 255)

    # step 5: merge layers down
    pdb.gimp_image_merge_down(img, layer3, 0)
    # set layer2 mode to GIMP_OVERLAY_MODE (23)
    layer2 = pdb.gimp_image_get_active_drawable(img)
    pdb.gimp_layer_set_mode(layer2, 23)
    pdb.gimp_image_merge_down(img, layer2, 0)
    pdb.gimp_image_undo_group_end(img)


register(
    "python-fu-cartoonify",                       # Plugin name
    "Apply cartoon filter",                       # Short description
    "Apply cartoon filter",                       # Long description
    "Pascal Reitermann",                          # Plugin author
    "Pascal Reitermann",                          # Copyright or license
    "2022",                                       # Year of publishing
    "Cartoonify...",                              # Name of the plug-in
    "*",                                          # Supported images
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],                                            # Input parameter
    [],                                           # Output result
    apply_cartoon_filter,                         # Name of the function
    menu="<Image>/Filters/Artistic"
    )


main()
