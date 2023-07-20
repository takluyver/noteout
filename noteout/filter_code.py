#!/usr/bin/env python3
""" Panflute filter to filter code blocks
"""

import re

import panflute as pf
from jupytext import cell_metadata as jcm

from noteout.filter_nb_only import Filter


CODE_CONFIG_RE = re.compile(r'^{(.*?)}')


class MetaFilter(Filter):

    metadata_field = 'noteout.filter-langs'

    @classmethod
    def get_bad_names(cls, doc):
        dds = doc.get_metadata(cls.metadata_field)
        if dds is not None:
            return {dds} if isinstance(dds, str) else set(dds)
        return set()

    @classmethod
    def action(cls, elem, doc):
        bad_names = doc.bad_names
        if not isinstance(elem, pf.Code):
            return
        if not (match := CODE_CONFIG_RE.match(elem.text)):
            return
        lang, opts = jcm.rmd_options_to_metadata(match.groups()[0])
        if not opts.get('all_eds', False) and lang.lower() in bad_names:
            return []


def main(doc=None):
    MetaFilter.main(doc=doc)


if __name__ == "__main__":
    main()
