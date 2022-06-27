###############################################################################
# Auxiliary
#   Non-specific functions needed by routines
###############################################################################
import os
import warnings
import matplotlib.colors as mcolors
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

def makeFolder(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            raise OSError(
                "Can't create destination directory (%s)!" % (path)
            )
    
def colorPaletteFromHexList(clist):
    c = mcolors.ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
    return rvb

