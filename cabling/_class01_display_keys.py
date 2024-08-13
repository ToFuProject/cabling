# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 18:01:13 2024

@author: dvezinet
"""


import datastock as ds


from .inputs import _config


#############################################
#############################################
#       display keys
#############################################


def main(
    coll=None,
    which=None,
    keys=None,
    include=None,
):

    # --------------
    # check input
    # --------------

    which, wmodel, wtype, keys, include = _check(
        coll=coll,
        which=which,
        keys=keys,
        include=include,
    )

    # --------------
    # run
    # --------------

    dout = {}
    for key in keys:

        # systems
        kwdargs = {
            k0: coll._dobj[which][key]['systems'][k0]
            for k0 in _config._SYSTEMS
            if coll._dobj[which][key]['systems'].get(k0) is not None
        }

        # modela and type
        kmod = coll._dobj[which][key].get(wmodel)
        if kmod is not None:
            ktype = coll._dobj[wmodel][kmod].get(wtype)
        else:
            ktype = None

        kwdargs[wmodel] = kmod
        kwdargs[wtype] = ktype

        # call
        dout[key] = _display_key(
            include=include,
            key=key,
            tag=coll._dobj[which][key].get('tag'),
            PID=coll._dobj[which][key].get('PID'),
            label=coll._dobj[which][key]['label'],
            **kwdargs,
        )

    return dout


#############################################
#############################################
#       check
#############################################


def _check(
    coll=None,
    which=None,
    keys=None,
    include=None,
):

    # -----------
    # which
    # -----------

    # which
    lok = [coll._which_connector, coll._which_device]
    which = ds._generic_check._check_var(
        which, 'which',
        types=str,
        allowed=lok,
    )

    # type, model
    wmodel = getattr(coll, f"_which_{which}_model")
    wtype = getattr(coll, f"_which_{which}_type")

    # -----------
    # keys
    # -----------

    if isinstance(keys, str):
        keys = [keys]
    lok = list(coll.dobj.get(which, {}).keys())
    keys = ds._generic_check._check_var_iter(
        keys, 'keys',
        types=(list, tuple),
        types_iter=str,
        allowed=lok,
        default=lok,
    )

    # -----------
    # include
    # -----------

    if isinstance(include, str):
        include = [include]

    ldef = _config._SYSTEMS + ['label']
    lok = ['key', 'tag', 'PID', wtype, wmodel] + ldef
    include = ds._generic_check._check_var_iter(
        include, 'include',
        types=(list, tuple),
        types_iter=str,
        allowed=lok,
        default=ldef,
    )

    return which, wmodel, wtype, keys, include


#############################################
#############################################
#       display keys low-level
#############################################


def _display_key(include=None, **kwdargs):

    ls = []
    for ss in include:
        if kwdargs.get(ss) is not None:
            ls.append(kwdargs[ss])

    return "_".join(ls)