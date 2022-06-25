###############################################################################
# Auxiliary
#   
###############################################################################
import warnings
warnings.filterwarnings("ignore")

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        elif shell == 'TerminalInteractiveShell':
            return False
        else:
            return False
    except NameError:
        return False

def padList(lst, n):
    lst.extend([None] * n)
    lst = lst[:n]
    return lst

def removeBanned(lastfmData, bans, label='Artist'):
    return lastfmData[~lastfmData[label].isin(bans)]

def replace(dataframe, replacementDict, columnNames):
    (df, repDict, col) = (dataframe, replacementDict, columnNames)
    cats = sorted(list(repDict.keys()))
    for cat in cats:
        repSet = repDict[cat]
        df.loc[df[col[0]].isin(repSet), col[1]] = cat
    return df