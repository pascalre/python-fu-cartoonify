#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A set of GIMP plug-ins to turn a photo into a cartoon."""

from gimpfu import pdb, register, main, PF_IMAGE, PF_DRAWABLE,\
    PF_ADJUSTMENT  # pylint: disable=import-error


def copy_layer(img, drawable, name, tattoo):
    """Copy a layer, set name and tattoo."""
    layer = pdb.gimp_layer_copy(drawable, False)
    pdb.gimp_image_add_layer(img, layer, -1)
    pdb.gimp_item_set_name(layer, name)
    pdb.gimp_item_set_tattoo(layer, tattoo)
    return layer


def merge_down_with_mode(img, layer, mode):
    """Apply mode to layer and merge it down."""
    pdb.gimp_layer_set_mode(layer, mode)
    pdb.gimp_image_merge_down(img, layer, 0)


def cartoonify_pop(img, drawable, line_size, shadow_intensity, color_levels):
    """Apply carton filter 'pop' to a given image."""
    pdb.gimp_image_undo_group_start(img)

    copy_layer(img, drawable, "layer_temp7", 700)
    layer_gmic = copy_layer(img, drawable, "layer_gmic", 800)
    layer_temp6 = copy_layer(img, drawable, "layer_temp6", 600)
    copy_layer(img, drawable, "layer_temp5", 500)
    copy_layer(img, drawable, "layer_temp4", 400)
    copy_layer(img, drawable, "layer_temp3", 300)

    if shadow_intensity > 0:
        layer_temp2a = copy_layer(img, drawable, "layer_temp2a", 210)
        pdb.gimp_layer_set_mode(layer_temp2a, 3)
        pdb.gimp_desaturate_full(layer_temp2a, 2)
        pdb.gimp_threshold(layer_temp2a, shadow_intensity, 255)

    copy_layer(img, drawable, "layer_temp1", 100)
    layer_temp2 = copy_layer(img, drawable, "layer_temp2", 200)
    pdb.gimp_levels_stretch(drawable)

    pdb.plug_in_sel_gauss(img, layer_gmic, 4, 11)

    pdb.gimp_layer_set_mode(layer_temp6, 3)

    pdb.plug_in_gauss(img, layer_temp2, line_size, line_size, 1)
    pdb.gimp_invert(layer_temp2)
    pdb.gimp_layer_set_mode(layer_temp2, 16)
    pdb.gimp_image_merge_down(img, layer_temp2, 0)

    layer_temp1 = pdb.gimp_image_get_active_drawable(img)
    pdb.gimp_threshold(layer_temp1, 245, 255)
    pdb.gimp_layer_set_mode(layer_temp1, 3)

    layer_temp3 = pdb.gimp_image_get_layer_by_tattoo(img, 300)
    pdb.gimp_desaturate_full(layer_temp3, 2)
    merge_down_with_mode(img, layer_temp3, 15)

    layer_temp5 = pdb.gimp_image_get_layer_by_tattoo(img, 500)
    pdb.gimp_desaturate_full(layer_temp5, 2)
    merge_down_with_mode(img, layer_temp5, 15)

    layer_temp4 = pdb.gimp_image_get_layer_by_tattoo(img, 400)
    pdb.gimp_layer_set_mode(layer_temp4, 3)
    pdb.gimp_image_raise_layer(img, layer_temp4)
    pdb.gimp_image_merge_down(img, layer_temp4, 0)

    layer_temp6 = pdb.gimp_image_get_layer_by_tattoo(img, 600)
    merge_down_with_mode(img, layer_temp6, 14)

    layer_temp1 = pdb.gimp_image_get_layer_by_tattoo(img, 100)
    pdb.gimp_image_merge_down(img, layer_temp1, 0)
    layer_temp2a = pdb.gimp_image_get_layer_by_tattoo(img, 210)
    merge_down_with_mode(img, layer_temp2a, 3)
    layer_gmic = pdb.gimp_image_get_layer_by_tattoo(img, 800)
    pdb.gimp_image_merge_down(img, layer_gmic, 0)
    layer_temp7 = pdb.gimp_image_get_layer_by_tattoo(img, 700)
    pdb.gimp_levels(layer_temp7, 0, 0, 255, 1.0, 0, 255)
    pdb.gimp_image_merge_down(img, layer_temp7, 0)

    pdb.gimp_image_convert_indexed(img, 0, 0, color_levels, 0, 0, "")
    pdb.gimp_image_convert_rgb(img)

    pdb.gimp_displays_flush()
    pdb.gimp_image_undo_group_end(img)


register(
    "python-fu-cartoonify-pop",                   # Plugin name
    "Pop cartoon",                                # Short description
    "Apply pop cartoon filter",                   # Long description
    "Pascal Reitermann",                          # Plugin author
    "Pascal Reitermann",                          # Copyright
    "2022",                                       # Year of publishing
    "Pop...",                                     # Name of the plug-in
    "*",                                          # Supported images
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_ADJUSTMENT, "line_size", "Line thickness", 10, (2, 30, 1)),
        (PF_ADJUSTMENT, "shadow_intensity", "Shadow intensity", 35,
         (0, 50, 1)),
        (PF_ADJUSTMENT, "color_levels", "Color levels", 16, (4, 20, 4)),
    ],                                            # Input parameter
    [],                                           # Output result
    cartoonify_pop,                               # Name of the function
    menu="<Image>/Filters/Artistic/Cartoonify"
    )


def cartoonify_simple(img, drawable):
    """Apply carton filter 'simple' to a given image."""
    pdb.gimp_image_undo_group_start(img)

    temp_layer = pdb.gimp_layer_copy(drawable, False)
    pdb.gimp_image_add_layer(img, temp_layer, 0)
    pdb.gimp_item_set_name(temp_layer, "temp_layer")
    pdb.gimp_threshold(temp_layer, 127, 255)
    pdb.gimp_layer_set_mode(temp_layer, 14)
    pdb.gimp_image_merge_down(img, temp_layer, 0)
    pdb.gimp_image_convert_indexed(img, 0, 0, 24, 0, 0, "")
    pdb.gimp_image_convert_rgb(img)
    layer3 = pdb.gimp_image_get_active_drawable(img)
    pdb.gimp_posterize(layer3, 3)

    pdb.gimp_image_undo_group_end(img)


register(
    "python-fu-cartoonify-simple",                # Plugin name
    "Simple cartoon",                             # Short description
    "Apply simple cartoon filter",                # Long description
    "Pascal Reitermann",                          # Plugin author
    "Pascal Reitermann",                          # Copyright
    "2022",                                       # Year of publishing
    "Simple...",                                  # Name of the plug-in
    "*",                                          # Supported images
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],                                            # Input parameter
    [],                                           # Output result
    cartoonify_simple,                            # Name of the function
    menu="<Image>/Filters/Artistic/Cartoonify"
    )


def cartoonify_realistic(img, drawable):
    """Apply carton filter 'realistic' to a given image."""
    # docs
    # https://developer.gimp.org/api/2.0/libgimp/index.html
    # https://developer.gimp.org/api/2.0/libgimp/libgimp-gimpenums.html
    # https://developer.gimp.org/api/2.0/libgimp/libgimp-gimpcolor.html
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
    pdb.gimp_curves_spline(layer3, 0, 6,
                           [0, 0,
                            130, 255,
                            255, 255])

    # step 4: adjust levels
    pdb.gimp_levels(layer3, 0, 0, 130, 1.0, 0, 255)

    # step 5: merge layers down
    pdb.gimp_image_merge_down(img, layer3, 0)
    # set layer2 mode to GIMP_OVERLAY_MODE (23)
    layer2 = pdb.gimp_image_get_active_drawable(img)
    pdb.gimp_layer_set_mode(layer2, 23)
    pdb.gimp_image_merge_down(img, layer2, 0)
    pdb.gimp_image_undo_group_end(img)


register(
    "python-fu-cartoonify-realistic",             # Plugin name
    "Realistic cartoon",                          # Short description
    "Apply realistic cartoon filter",             # Long description
    "Pascal Reitermann",                          # Plugin author
    "Pascal Reitermann",                          # Copyright
    "2022",                                       # Year of publishing
    "Realistic...",                               # Name of the plug-in
    "*",                                          # Supported images
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],                                            # Input parameter
    [],                                           # Output result
    cartoonify_realistic,                         # Name of the function
    menu="<Image>/Filters/Artistic/Cartoonify"
    )


main()
