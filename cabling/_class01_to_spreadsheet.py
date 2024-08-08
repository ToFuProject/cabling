# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:58:44 2024

@author: dvezinet
"""


import os
import datetime as dtm


import pandas as pd
import datastock as ds


from . import _class01_to_graph as _to_graph


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    devices=None,
    connectors=None,
    # options
    startrow=None,
    startcol=None,
    # pfe
    pfe=None,
    verb=None,
):

    # --------------
    # check inputs
    # ---------------

    pfe, verb = _check(
        pfe=pfe,
        verb=verb
    )

    # ---------------
    # select devices and connectors
    # ---------------

    ldev, lcon = _to_graph._select(
        coll=coll,
        devices=devices,
        connectors=connectors,
     )

    # --------------
    # to DataFrames
    # ---------------

    dout = _DataFrames(
        coll,
        ldev=ldev,
        lcon=lcon,
    )

    # --------------
    # write to spreadsheet
    # ---------------

    _spreadsheet(dout)

    return


#############################################
#############################################
#       check
#############################################


def _check(
    pfe=None,
    verb=None
):

    # -----------
    # pfe
    # -----------

    if pfe is None:
        time = dtm.datetime.now().strftime('%Y%m%d_%H%M%S')
        name = f"cabling_getpass.user()_{time}.xlsx"
        path = os.path.abspath('.')
        pfe = os.path.join(path, name)

    elif not isinstance(pfe, str):
        msg = (
            "Arg 'pfe' must be a str pointing to a valid <path/file.ext>\n"
            f"Provided:\n\t{pfe}"
        )
        raise Exception(msg)

    else:

        try:
            path, fe = os.path.split(pfe)
            assert os.path.isdir(path)

        except Exception as err:
            msg = (
                "Arg 'pfe' must be a pointing to a valid <path/file.ext>\n"
                f"Provided:\n\t{pfe}"
            )
            raise Exception(msg) from err

        if not fe.endswith('.xlsx'):
            pfe = f"{pfe}.xlsx"

    # -----------
    # verb
    # -----------

    verb = ds._generic_check._check_var(
        verb, 'verb',
        types=bool,
        default=True,
    )

    return pfe, verb


#############################################
#############################################
#       to DataFrame
#############################################


def _DataFrames(
    coll=None,
    ldev=None,
    lcon=None,
    # options
    startrow=None,
    startcol=None,
):

    # --------------
    # prepare
    # --------------

    wpt = coll._which_plug_type
    wct = coll._which_connector_type
    wcm = coll._which_connector_model
    wcon = coll._which_connector
    wdt = coll._which_device_type
    wdm = coll._which_device_model
    wdev = coll._which_device

    # models
    ldm = sorted(set([
        coll.dobj[wdev][k0][wdm] for k0 in ldev
        if coll.dobj[wdev][k0].get(wdm) is not None
    ]))
    lcm = sorted(set([
        coll.dobj[wcon][k0][wcm] for k0 in lcon
        if coll.dobj[wcon][k0].get(wcm) is not None
    ]))

    # types
    ldt = sorted(set([
        coll.dobj[wdm][k0][wdt] for k0 in ldm
        if coll.dobj[wdm][k0].get(wdt) is not None
    ]))
    lct = sorted(set([
        coll.dobj[wcm][k0][wct] for k0 in lcm
        if coll.dobj[wcm][k0].get(wct) is not None
    ]))

    # plug types
    lpt = sorted(set([
        coll.dobj[wct][k0][wpt] for k0 in lct
        if coll.dobj[wct][k0].get(wpt) is not None
    ]))

    dwhich = {
        # device connectors
        wdev: ldev,
        wcon: lcon,
        # models
        wdm: ldm,
        wcm: lcm,
        # types
        wdt: ldt,
        wct: lct,
        # plugs
        wpt: lpt,
    }

    # --------------
    # loop
    # --------------

    dout = {}
    for k0, v0 in dwhich.items():

        df = coll.to_DataFrame(which=k0, keys=dwhich[k0])

        dout[k0] = {
            'DataFrame': df,
            'columns': None,
            'freeze_panes': (1 + startrow, 1 + startcol),
        }

    return dout


#############################################
#############################################
#       to Spreadsheet
#############################################


def _spreadsheet(
    dout=None,
    pfe=None,
    verb=None,
):

    # ------------
    # excel_writer
    # ------------

    excel_writer = pd.ExcelWriter(
        path=pfe,
        engine=None,
        date_format='YYYY-MM-DD',
        datetime_format='YYYY-MM-DD',
        mode='w',
        storage_options=None,
        if_sheet_exists='overlay',
        engine_kwargs=None,
    )

    # ------------
    # write
    # ------------

    with excel_writer as writer:
        for k0, v0 in dout.items():
            v0['df'].to_excel(
                writer,
                sheet_name=k0,
                na_rep='',
                float_format="%.3e",
                columns=v0['columns'],
                header=True,
                index=True,
                index_label=None,
                startrow=1,
                startcol=1,
                merge_cells=True,
                inf_rep='inf',
                freeze_panes=v0['freeze_panes'],
            )

    # ------------
    # verb
    # ------------

    if verb is True:
        msg = (
            "Saved in:\n\t{pfe}"
        )
        print(msg)

    return