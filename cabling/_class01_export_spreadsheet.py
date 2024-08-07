# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:58:44 2024

@author: dvezinet
"""


import os
import datetime as dtm


import pandas as pd
import datastock as ds


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    devices=None,
    connectors=None,
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

    # --------------
    # to DataFrames
    # ---------------

    dout = _DataFrames(coll)

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


def _DataFrames(coll):

    # --------------
    #
    # --------------



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