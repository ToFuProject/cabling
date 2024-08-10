# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:27:36 2024

@author: dvezinet
"""

import os
import getpass
import warnings
import datetime as dtm


import numpy as np
import matplotlib.colors as mcolors
from matplotlib.pyplot import cm
import datastock as ds


from .inputs import _config


# #################################################################
# #################################################################
#          Default values
# #################################################################


_COLOR = 'k'


# #################################################################
# #################################################################
#          Main
# #################################################################


def main(
    # ---------------
    # input from tofu
    coll=None,
    devices=None,
    connectors=None,
    # ---------------
    # options
    factor=None,
    color_by=None,
    # ---------------
    # saving
    pfe_save=None,
    verb=None,
    overwrite=None,
):

    # -------------
    # check inputs
    # -------------

    (
        devices, connectors,
        factor,
        iso,
        pfe_save, verb, overwrite,
    ) = _check(
        # ---------------
        # input from tofu
        coll=coll,
        devices=devices,
        connectors=connectors,
        # ---------------
        # options
        factor=factor,
        # ---------------
        # saving
        pfe_save=pfe_save,
        verb=verb,
        overwrite=overwrite,
    )

    fname = os.path.split(pfe_save)[-1][:-4]

    # ------------------------------
    # get color dict for connectors
    # ------------------------------

    dcolorby_con = _get_dcolorby(
        coll,
        which=coll._which_connector,
        keys=connectors,
        color_by=color_by,
    )

    # ----------------------------
    # extract and pre-format data
    # ----------------------------

    dptsx_con, dptsy_con, dptsz_con = _extract(
        coll=coll,
        devices=devices,
        connectors=connectors,
        dcolorby_con=dcolorby_con,
    )

    # scaling factor
    for k0, v0 in dptsx_con.items():
        dptsx_con[k0]['data'] *= factor
        dptsy_con[k0]['data'] *= factor
        dptsz_con[k0]['data'] *= factor

    # -----------------------
    # loop on groups of color
    # -----------------------

    # ----------------
    # get file content
    # ----------------

    # HEADER
    msg_header = _get_header(
        fname=fname,
        iso=iso,
    )

    # DATA
    msg_data = _get_data(
        dptsx=dptsx_con,
        dptsy=dptsy_con,
        dptsz=dptsz_con,
        fname=fname,
        # options
        dcolor=dcolorby_con,
        # norm
        iso=iso,
    )

    # -------------
    # save to stp
    # -------------

    _save(
        msg=msg_header + "\n" + msg_data,
        pfe_save=pfe_save,
        overwrite=overwrite,
    )

    return


# #################################################################
# #################################################################
#          check
# #################################################################


def _check(
    # ---------------
    # input from tofu
    coll=None,
    devices=None,
    connectors=None,
    # ---------------
    # options
    factor=None,
    color_by=None,
    # ---------------
    # saving
    pfe_save=None,
    verb=None,
    overwrite=None,
):

    kco = '3d'

    # ---------------
    # connectors
    # ---------------

    wcon = coll._which_connector
    lok = list(coll.dobj.get(wcon, {}).keys())
    connectors = ds._generic_check._check_var_iter(
        connectors, 'connectors',
        allowed=lok,
    )

    # adjust to make sure only those with '3d' coords are selected
    connectors = [
        k0 for k0 in connectors
        if coll.dobj[wcon][k0].get('dcoords') is not None
        and coll.dobj[wcon][k0]['dcoords'].get(kco) is not None
        and np.all([
            np.all(np.isfinite(v1))
            for v1 in coll.dobj[wcon][k0]['dcoords'][kco].values()
        ])
    ]

    # ---------------
    # devices
    # ---------------

    if devices is not None:
        msg = "Export of devices to stp not implemented yet"
        raise NotImplementedError(msg)

    # ---------------
    # factor
    # ---------------

    factor = float(ds._generic_check._check_var(
        factor, 'factor',
        types=(float, int),
        default=1.,
    ))

    # ---------------
    # iso
    # ---------------

    iso = 'ISO-10303-21'

    # ---------------
    # pfe_save
    # ---------------

    # Default
    if pfe_save is None:
        path = os.path.abspath('.')
        t0 = dtm.datetime.now().strftime('%Y%m%d_%H%M%S')
        name = f'cabling_{getpass.getuser()}_{t0}.stp'
        pfe_save = os.path.join(path, name)

    # check
    c0 = (
        isinstance(pfe_save, str)
        and (
            os.path.split(pfe_save)[0] == ''
            or os.path.isdir(os.path.split(pfe_save)[0])
        )
    )
    if not c0:
        msg = (
            "Arg pfe_save must be a saving file str ending in '.stp'!\n"
            f"Provided: {pfe_save}"
        )
        raise Exception(msg)

    # makesure extension is included
    if not pfe_save.endswith('.stp'):
        pfe_save = f"{pfe_save}.stp"

    # ----------------
    # verb
    # ----------------

    verb = ds._generic_check._check_var(
        verb, 'verb',
        types=bool,
        default=True,
    )

    # ----------------
    # overwrite
    # ----------------

    overwrite = ds._generic_check._check_var(
        overwrite, 'overwrite',
        types=bool,
        default=False,
    )

    return (
        devices, connectors,
        factor,
        iso,
        pfe_save, verb, overwrite,
    )


# #################################################################
# #################################################################
#           Get color dict
# #################################################################


def _get_dcolorby(coll, which=None, keys=None, color_by=None):

    # ----------------
    # colorby
    # ----------------

    if color_by is None or isinstance(color_by, str):

        color_by = ds._generic_check._check_var(
            color_by, 'color_by',
            types=str,
            default='L2',
            allowed=_config._SYSTEMS + ['key', 'label'],
        )
        colorby = color_by

    elif isinstance(color_by, dict):

        assert len(color_by) == 1
        colorby = list(color_by.keys())[0]
        colorby = ds._generic_check._check_var(
            colorby, 'colorby',
            types=str,
            default='L2',
            allowed=_config._SYSTEMS + ['key', 'label'],
        )

    # ---------------
    #  cases
    # ----------------

    dout = _colorby_keys(coll, which, keys, colorby)

    ncol = len(dout)
    color = iter(cm.rainbow(np.linspace(0, 1, ncol)))
    if isinstance(color_by, dict):

        # ---------------
        # add keys

        dcolorby = {
            k0: {
                'keys': v0,
                'color': mcolors.to_rgb(color_by.get(k0, next(color))),
            }
            for ii, (k0, v0) in enumerate(dout.items())
        }

    else:

        # ---------------
        #  add colors

        dcolorby = {
            k0: {
                'keys': v0,
                'color': mcolors.to_rgb(next(color)),
            }
            for ii, (k0, v0) in enumerate(dout.items())
        }

    return dcolorby


def _colorby_keys(coll, which, keys, color_by):

    dcolorby = {}
    if color_by == 'key':
        dout = {k0: [k0] for k0 in keys}

    elif color_by in ['label', 'tag', 'PID']:

        lu = sorted(set([coll.dobj[which][k0][color_by] for k0 in keys]))
        dout = {
            [k0 for k0 in keys if coll.dobj[which][k0][color_by] == uu]
            for uu in lu
        }

    elif color_by in _config._SYSTEMS:

        lu = sorted(set([coll.dobj[which][k0]['systems'][color_by] for k0 in keys]))
        dout = {
            uu: [k0 for k0 in keys if coll.dobj[which][k0]['systems'][color_by] == uu]
            for uu in lu
        }

    else:
        msg = f"color_by = '{color_by}' not implemented yet!"
        raise NotImplementedError(msg)

    return dout


# #################################################################
# #################################################################
#          extract
# #################################################################


def _extract(
    coll=None,
    devices=None,
    connectors=None,
    dcolorby_con=None,
):

    # ----------------------
    # initialize
    # ----------------------

    dptsx = {}
    dptsy = {}
    dptsz = {}

    # ----------------------
    # extract points from connectors
    # ----------------------

    kco = '3d'
    wcon = coll._which_connector
    for k0, v0 in dcolorby_con.items():
        for ii, k1 in enumerate(v0['keys']):
            dptsx[k1] = {
                'data': np.copy(coll.dobj[wcon][k1]['dcoords'][kco]['x']),
                'color': v0['color'],
            }
            dptsy[k1] = {
                'data': np.copy(coll.dobj[wcon][k1]['dcoords'][kco]['y']),
                'color': v0['color'],
            }
            dptsz[k1] = {
                'data': np.copy(coll.dobj[wcon][k1]['dcoords'][kco]['z']),
                'color': v0['color'],
            }

    return dptsx, dptsy, dptsz


# #################################################################
# #################################################################
#          HEADER
# #################################################################


def _get_header(
    fname=None,
    iso=None,
):

    # -------------
    # parameters
    # -------------

    # author
    author = getpass.getuser()

    # timestamp
    t0 = dtm.datetime.now()
    tstr = t0.strftime('%Y-%m-%dT%H:%M:%S-05:00')

    # niso
    niso = iso.split('-')[1]

    # -------------
    # Header
    # -------------

    msg = (
f"""{iso};
HEADER;
/* Generated by software containing ST-Developer
 * from STEP Tools, Inc. (www.steptools.com)
 */
/* OPTION: using custom schema-name function */

FILE_DESCRIPTION(
/* description */ (''),
/* implementation_level */ '2;1');

FILE_NAME(
/* name */ '{fname}.stp',
/* time_stamp */ '{tstr}',
/* author */ ('{author}'),
/* organization */ (''),
/* preprocessor_version */ 'ST-DEVELOPER v18.102',
/* originating_system */ 'SIEMENS PLM Software NX2206.4040',
/* authorisation */ '');\n
"""
    + "FILE_SCHEMA (('AUTOMOTIVE_DESIGN { 1 0 " + f"{niso}" + " 214 3 1 1 1 }'));\n"
    + "ENDSEC;"
    )

    return msg


# #################################################################
# #################################################################
#          DATA
# #################################################################


def _get_data(
    dptsx=None,
    dptsy=None,
    dptsz=None,
    fname=None,
    # options
    dcolor=None,
    # norm
    iso=None,
):

    # -----------
    # nrays
    # -----------

    # vectors
    dvx = {k0: np.diff(v0['data']) for k0, v0 in dptsx.items()}
    dvy = {k0: np.diff(v0['data']) for k0, v0 in dptsy.items()}
    dvz = {k0: np.diff(v0['data']) for k0, v0 in dptsz.items()}

    # dok
    dok = {k0: np.isfinite(v0) for k0, v0 in dvx.items()}

    # length
    dlength = {
        k0: np.sqrt(dvx[k0]**2 + dvy[k0]**2 + dvz[k0]**2)
        for k0 in dptsx.keys()
    }

    # directions
    ddx = {k0: dvx[k0] / dlength[k0] for k0 in dptsx.keys()}
    ddy = {k0: dvy[k0] / dlength[k0] for k0 in dptsx.keys()}
    ddz = {k0: dvz[k0] / dlength[k0] for k0 in dptsx.keys()}

    # nrays
    dnrays = {k0: v0.sum() for k0, v0 in dok.items()}
    nrays = np.sum([v0 for v0 in dnrays.values()])

    # -----------
    # colors
    # -----------

    colors = sorted(set([v0['color'] for v0 in dcolor.values()]))
    ncol = len(colors)

    # --------------
    # order of connectors

    lkcon = sorted(dptsx.keys())
    k0ind = _get_k0ind(
        dind_ok={k0: v0.nonzero() for k0, v0 in dok.items()},
        ncum=np.cumsum([dnrays[kcon] for kcon in lkcon]),
        lkcon=lkcon,
    )


    # -----------------
    # get index
    # ------------------

    i0 = 31
    dind = {
        'GEOMETRIC_CURVE_SET': {'order': 0},
        'PRESENTATION_LAYER_ASSIGNMENT': {'order': 1},
        'STYLED_ITEM': {
            'order': 2,
            'nn': nrays,
        },
        'PRESENTATION_STYLE_ASSIGNMENT': {
            'order': 3,
            'nn': ncol,
        },
        'CURVE_STYLE': {
            'order': 4,
            'nn': ncol,
        },
        'COLOUR_RGB': {
            'order': 5,
            'nn': ncol,
        },
        'DRAUGHTING_PRE_DEFINED_CURVE_FONT': {
            'order': 6,
            # 'nn': nrays,
        },
        'TRIMMED_CURVE': {
            'order': 7,
            'nn': nrays,
        },
        'LINE': {
            'order': 8,
            'nn': nrays,
        },
        'VECTOR': {
            'order': 9,
            'nn': nrays,
        },
        'AXIS2_PLACEMENT_3D': {'order': 10},
        'DIRECTION0': {
            'order': 11,
            'str': "DIRECTION('',(0.,0.,1.));",
        },
        'DIRECTION1': {
            'order': 12,
            'str': "DIRECTION('',(1.,0.,0.));",
        },
        'DIRECTION': {
            'order': 13,
            'nn': nrays,
        },
        'CARTESIAN_POINT0': {
            'order': 14,
            'str': "CARTESIAN_POINT('',(0.,0.,0.));",
        },
        'CARTESIAN_POINT': {
            'order': 15,
            'nn': nrays,
        },
        'MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION': {'order': 16},
    }

    # complement
    lkey = [k0 for k0 in dind.keys()]
    lorder = [dind[k0]['order'] for k0 in lkey]

    # safety ceck
    assert np.unique(lorder).size == len(lorder)
    inds = np.argsort(lorder)
    lkey = [lkey[ii] for ii in inds]

    # derive indices
    for k0 in lkey:
        nn = dind[k0].get('nn', 1)
        dind[k0]['ind'] = i0 + np.arange(0, nn)
        i0 += nn

    # -----------------
    # COLOUR_RGB
    # -----------------

    k0 = 'COLOUR_RGB'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        lines.append(f"#{ni}={k0}('color {ii}',{colors[ii][0]},{colors[ii][1]},{colors[ii][2]});")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # CARTESIAN_POINT
    # -----------------

    k0 = 'CARTESIAN_POINT'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        lines.append(f"#{ni}={k0}('{kcon}',({dptsx[kcon]['data'][ind]},{dptsy[kcon]['data'][ind]},{dptsz[kcon]['data'][ind]}));")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # DIRECTION
    # -----------------

    k0 = 'DIRECTION'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        lines.append(f"#{ni}={k0}('{kcon}',({ddx[kcon][ind]},{ddy[kcon][ind]},{ddz[kcon][ind]}));")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # VECTOR
    # -----------------

    k0 = 'VECTOR'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        lines.append(f"#{ni}={k0}('{kcon}',#{dind['DIRECTION']['ind'][ii]},{dlength[kcon][ind]});")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # AXIS2_PLACEMENT_3D
    # -----------------

    k0 = 'AXIS2_PLACEMENT_3D'
    ni = dind[k0]['ind'][0]
    lstr = ', '.join([f"#{ii}" for ii in dind['TRIMMED_CURVE']['ind']])
    dind[k0]['msg'] = f"#{ni}={k0}('',#{dind['CARTESIAN_POINT0']['ind'][0]},#{dind['DIRECTION0']['ind'][0]},#{dind['DIRECTION1']['ind'][0]});"

    # -----------------
    # LINE
    # -----------------

    k0 = 'LINE'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        lines.append(f"#{ni}={k0}('{kcon}',#{dind['CARTESIAN_POINT']['ind'][ii]},#{dind['VECTOR']['ind'][ii]});")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # TRIMMED_CURVE
    # -----------------

    k0 = 'TRIMMED_CURVE'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        lines.append(f"#{ni}={k0}('{kcon}',#{dind['LINE']['ind'][ii]},(PARAMETER_VALUE(0.)),(PARAMETER_VALUE(1.)),.T.,.PARAMETER.);")
    dind[k0]['msg'] = "\n".join(lines)

    # ----------------
    # DRAUGHTING_PRE_DEFINED_CURVE_FONT
    # ----------------

    k0 = 'DRAUGHTING_PRE_DEFINED_CURVE_FONT'
    ni = dind[k0]['ind'][0]
    dind[k0]['msg'] = f"#{ni}={k0}('continuous');"

    # ------------------
    # CURVE_STYLE
    # ------------------

    k0 = 'CURVE_STYLE'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        lines.append(f"#{ni}={k0}('style {ii}',#{dind['DRAUGHTING_PRE_DEFINED_CURVE_FONT']['ind'][0]},POSITIVE_LENGTH_MEASURE(0.7),#{dind['COLOUR_RGB']['ind'][ii]});")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # PRESENTATION_STYLE_ASSIGNMENT
    # ------------------

    k0 = 'PRESENTATION_STYLE_ASSIGNMENT'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        lines.append(f"#{ni}={k0}((#{dind['CURVE_STYLE']['ind'][ii]}));")
    dind[k0]['msg'] = "\n".join(lines)

    #1605=PRESENTATION_STYLE_ASSIGNMENT((#2488));

    # -----------------
    # STYLED_ITEM
    # -----------------

    k0 = 'STYLED_ITEM'
    lines = []
    for ii, ni in enumerate(dind[k0]['ind']):
        kcon, ind = k0ind(ii)
        jj = colors.index(dptsx[kcon]['color'])
        lines.append(f"#{ni}={k0}('{kcon}',(#{dind['PRESENTATION_STYLE_ASSIGNMENT']['ind'][jj]}),#{dind['TRIMMED_CURVE']['ind'][ii]});")
    dind[k0]['msg'] = "\n".join(lines)

    # -----------------
    # GEOMETRIC_CURVE_SET
    # -----------------

    k0 = 'GEOMETRIC_CURVE_SET'
    ni = dind[k0]['ind'][0]
    lstr = ','.join([f"#{ii}" for ii in dind['TRIMMED_CURVE']['ind']])
    dind[k0]['msg'] = f"#{ni}={k0}('None',({lstr}));"

    # ----------------------
    # PRESENTATION_LAYER_ASSIGNMENT
    # ----------------------

    k0 = 'PRESENTATION_LAYER_ASSIGNMENT'
    ni = dind[k0]['ind'][0]
    lstr = ','.join([f"#{ii}" for ii in dind['TRIMMED_CURVE']['ind']])
    dind[k0]['msg'] = f"#{ni}={k0}('1','Layer 1',({lstr}));"

    # ----------------------------------
    # MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION
    # ----------------------------------

    k0 = 'MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION'
    ni = dind[k0]['ind'][0]
    lstr = ','.join([f"#{ii}" for ii in dind['STYLED_ITEM']['ind']])
    dind[k0]['msg'] = f"#{ni}={k0}('',({lstr}),#{i0});"

    # ------------
    # LEFTOVERS
    # ------------

    for k0, v0 in dind.items():
        if v0.get('msg') is None:
            if v0.get('str') is None:
                msg = f"Looks like '{k0}' is missing!"
                raise Exception(msg)
            else:
                ni = dind[k0]['ind'][0]
                dind[k0]['msg'] = f"#{ni}={v0['str']}"


    # --------------------
    # msg_pre
    # --------------------

    msg_pre = (
f"""
DATA;
#10=PROPERTY_DEFINITION_REPRESENTATION(#14,#12);
#11=PROPERTY_DEFINITION_REPRESENTATION(#15,#13);
#12=REPRESENTATION('',(#16),#{i0});
#13=REPRESENTATION('',(#17),#{i0});
#14=PROPERTY_DEFINITION('pmi validation property','',#21);
#15=PROPERTY_DEFINITION('pmi validation property','',#21);
#16=VALUE_REPRESENTATION_ITEM('number of annotations',COUNT_MEASURE(0.));
#17=VALUE_REPRESENTATION_ITEM('number of views',COUNT_MEASURE(0.));
#18=SHAPE_REPRESENTATION_RELATIONSHIP('None', 'relationship between {fname}-None and {fname}-None',#30,#19);
#19=GEOMETRICALLY_BOUNDED_WIREFRAME_SHAPE_REPRESENTATION('{fname}-None',(#31),#{i0});
#20=SHAPE_DEFINITION_REPRESENTATION(#21,#30);
#21=PRODUCT_DEFINITION_SHAPE('','',#22);
#22=PRODUCT_DEFINITION(' ','',#24,#23);
#23=PRODUCT_DEFINITION_CONTEXT('part definition',#29,'design');
#24=PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE(' ',' ',#26,.NOT_KNOWN.);
#25=PRODUCT_RELATED_PRODUCT_CATEGORY('part','',(#26));
#26=PRODUCT('{fname}','{fname}',' ', (#27));
#27=PRODUCT_CONTEXT(' ',#29,'mechanical');
#28=APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2010,#29);
#29=APPLICATION_CONTEXT('core data for automotive mechanical design processes');
#30=SHAPE_REPRESENTATION('{fname}-None',(#6215),#{i0});
"""
    )

    # --------------------
    # msg_post
    # --------------------

    # 5->91
    ind = i0 + np.arange(0, 8)
    msg_post = (
f"""
#{ind[0]}=(
GEOMETRIC_REPRESENTATION_CONTEXT(3)
GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{ind[1]}))
GLOBAL_UNIT_ASSIGNED_CONTEXT((#{ind[7]},#{ind[3]},#{ind[2]}))
REPRESENTATION_CONTEXT('{fname}','TOP_LEVEL_ASSEMBLY_PART')
);
#{ind[1]}=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(2.E-5),#{ind[7]}, 'DISTANCE_ACCURACY_VALUE','Maximum Tolerance applied to model');
#{ind[2]}=(
NAMED_UNIT(*)
SI_UNIT($,.STERADIAN.)
SOLID_ANGLE_UNIT()
);
#{ind[3]}=(
CONVERSION_BASED_UNIT('DEGREE',#{ind[5]})
NAMED_UNIT(#{ind[4]})
PLANE_ANGLE_UNIT()
);
#{ind[4]}=DIMENSIONAL_EXPONENTS(0.,0.,0.,0.,0.,0.,0.);
#{ind[5]}=PLANE_ANGLE_MEASURE_WITH_UNIT(PLANE_ANGLE_MEASURE(0.0174532925), #{ind[6]});
#{ind[6]}=(
NAMED_UNIT(*)
PLANE_ANGLE_UNIT()
SI_UNIT($,.RADIAN.)
);
#{ind[7]}=(
LENGTH_UNIT()
NAMED_UNIT(*)
SI_UNIT(.MILLI.,.METRE.)
);
ENDSEC;
END-{iso};"""
    )

    # --------------------
    # assemble
    # --------------------

    msg = msg_pre + "\n".join([dind[k0]['msg'] for k0 in lkey]) + msg_post

    return msg


# #################################################################
# #################################################################
#          Utility
# #################################################################


def _get_k0ind(dind_ok=None, ncum=None, lkcon=None):

    def k0ind(
            ii,
            dind_ok=dind_ok,
            ncum=ncum,
            lkcon=lkcon,
        ):

        icon = np.searchsorted(ncum-1, ii)
        inew = ii - ncum[icon-1] if icon>0 else ii

        return lkcon[icon], tuple([tt[inew] for tt in dind_ok[lkcon[icon]]])

    return k0ind


# #################################################################
# #################################################################
#          save to stp
# #################################################################


def _save(
    msg=None,
    pfe_save=None,
    overwrite=None,
):

    # -------------
    # check before overwriting

    if os.path.isfile(pfe_save):
        err = "File already exists!"
        if overwrite is True:
            err = f"{err} => overwriting"
            warnings.warn(err)
        else:
            err = f"{err}\nFile:\n\t{pfe_save}"
            raise Exception(err)

    # ----------
    # save

    with open(pfe_save, 'w') as fn:
        fn.write(msg)

    # --------------
    # verb

    msg = f"Saved to:\n\t{pfe_save}"
    print(msg)

    return