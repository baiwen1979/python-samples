'''
工具函数
'''

def plot_series(ax, series, index = False):
    '''
    Series绘图函数
    '''
    y = series.values
    if index:
        x = series.index.astype(str).values
        ax.plot(x, y)
    ax.plot(y)

def print_title(title, style_str='-', times=10):
    '''
    打印形如----title----的标题
    '''
    print(title.join([style_str * times]*2))

def print_props(data, **kw_props):
    '''
    打印属性，用法:print_props(obj, prop1='属性1', prop2='属性2'...)
    '''
    for k in kw_props:
        print('{}: {}'.format(kw_props[k], data.__getattr__(k)))
        