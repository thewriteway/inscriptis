#!/usr/bin/env python3
# encoding: utf-8
'''
Classes for representing Tables, Rows and TableCells.
'''

from inscriptis.html_properties import HorizontalAlignment


class AbstractTableCell():
    ''' A single table cell '''

    __slots__ = ('canvas', 'align', 'width', 'height')

    def __init__(self, canvas, align, width=None, height=None):
        '''
        Args:
          canvas: canvas to which the table cell is written.
          align: the :class:`~inscriptis.html_properties.HorizontalAlignment`
            of the given line.
         width: line width
        '''
        self.canvas = canvas
        self.align = align
        self.width = width
        self.height = height

    def get_format_spec(self):
        '''
        The format specification according to the values of `align` and
        `width`.
        '''
        return '{{:{self.align.value}{self.width}}}'.format(self=self)

    def get_cell_lines(self):
        '''
        Returns:
          list -- A list of all the lines stores within the :class:`TableCell`.
        '''
        raise NotImplemented


class AbstractRow():
    ''' A single row within a table '''
    __slot__ = ('columns', )

    def __init__(self):
        self.columns = []

    def get_cell_lines(self, column_idx):
        '''
        Computes the list of lines in the cell specified by the column_idx.

        Args:
          column_idx: The column index of the cell.
        Returns:
          list -- The list of lines in the cell specified by the column_idx or
                  an empty list if the column does not exist.
        '''
        raise NotImplemented

    def get_text(self):
        '''
        Returns:
          str -- A rendered string representation of the given row.
        '''
        raise NotImplemented


class AbstractTable():
    ''' A HTML table. '''

    __slot__ = ('rows', 'td_is_open')

    def __init__(self):
        self.rows = []
        # keep track of whether the last td tag has been closed
        self.td_is_open = False

    def add_row(self):
        '''
        Adds an empty :class:`Row` to the table.
        '''
        self.rows.append(Row())

    def add_cell(self, canvas, align=HorizontalAlignment.left):
        '''
        Adds a new :class:`TableCell` to the table's last row. If no row
        exists yet, a new row is created.
        '''
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(TableCell(canvas, align))

    def get_text(self):
        '''
        Returns:
          A rendered string representation of the given table.
        '''
        raise NotImplemented

