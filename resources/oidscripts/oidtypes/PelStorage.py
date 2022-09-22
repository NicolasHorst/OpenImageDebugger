# -*- coding: utf-8 -*-

"""
This module is concerned with the analysis of each variable found by the
debugger, as well as identifying and describing the buffers that should be
plotted in the ImageWatch window.
"""

import re

from oidscripts import symbols
from oidscripts.oidtypes import interface


class PelStorage(interface.TypeInspectorInterface):
    """
    Implementation for inspecting AreaBuf type (NextSoftware)
    """
    def get_buffer_metadata(self, obj_name, picked_obj, debugger_bridge):
        """
        Gets the buffer meta data from types of the NextSoftware
        Note that it only implements single channel matrix display,
        which should be quite common in for AreaBuffers. You can simply
        write out the color channels in different matrices.
        """
        type_str = str(picked_obj.type)
        current_type = str(picked_obj['bufs']['_arr'][0].type.template_argument(0))

        width = int(picked_obj['bufs']['_arr'][0]['width'])
        height= int(picked_obj['bufs']['_arr'][0]['height'])
        row_stride = int(picked_obj['bufs']['_arr'][0]['stride'])

        # Assign the GIW type according to underlying type
        if current_type == 'short':
            type_value = symbols.GIW_TYPES_INT16
        elif current_type == 'float':
            type_value = symbols.GIW_TYPES_FLOAT32
        elif current_type == 'double':
            type_value = symbols.GIW_TYPES_FLOAT64
        elif current_type == 'int':
            type_value = symbols.GIW_TYPES_INT32

        buffer = debugger_bridge.get_casted_pointer(current_type,picked_obj['bufs']['_arr'][0]['buf'])

        if buffer == 0x0:
            raise Exception('Received null buffer!')

        # Set row stride and pixel layout
        pixel_layout = 'bgra'

        return {
            'display_name': str(type_str) + ' ' + obj_name,
            'pointer': buffer,
            'width': width,
            'height': height,
            'channels': 1,
            'type': type_value,
            'row_stride': row_stride,
            'pixel_layout': pixel_layout,
            'transpose_buffer': False
        }

    def is_symbol_observable(self, symbol, symbol_name):
        """
        Returns true if the given symbol is of observable type (the type of the
        buffer you are working with). Make sure to check for pointers of your
        type as well
        """
        # Check if symbol type is the expected buffer
        symbol_type = str(symbol.type)
        type_regex = r'(const\s+)?PelStorage(\s+?[*&])?'
        return re.match(type_regex, symbol_type) is not None
