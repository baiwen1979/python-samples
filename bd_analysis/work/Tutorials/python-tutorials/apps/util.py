# -*- coding: utf-8 -*-
from IPython.display import HTML

def print_as_html(seq, w = None):
    max_len = len(max(seq, key=lambda x: len(x.__str__())))
    
    if w == None:
        w = max_len / 2
    
    ul_style = '''
    list-style-type:none;
    '''
    li_style = '''
    display: inline-block;
    padding-right: 1em;
    width: {}em;
    '''.format(w)
    
    html = '<ul style="{}">'.format(ul_style)
    for it in seq:
        html += '<li style="{}">{}</li>'.format(li_style, it)
    html += '</ul>'
    
    display(HTML(data=html))
