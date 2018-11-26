from copy import deepcopy


def format_translations(datadict, translationkey):
    # deepcopy before data manipulation
    newdict = deepcopy(datadict[translationkey])
    # format each values of the translation dict
    for key, value in datadict[translationkey].items():
        newdict[key] = value.format(**datadict)
    return newdict
