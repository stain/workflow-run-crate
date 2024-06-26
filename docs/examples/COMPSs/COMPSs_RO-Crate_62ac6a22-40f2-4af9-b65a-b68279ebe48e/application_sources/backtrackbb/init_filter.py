# -*- coding: utf8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .rec_filter import rec_filter_coeff, rec_filter_norm
from .mod_filter_picker import make_LinFq, make_LogFq
from pycompss.api.task import task
from pycompss.api.parameter import INOUT

@task(config=INOUT)
def init_filter(config):
    if config.band_spacing == 'lin':
        config.frequencies = make_LinFq(config.f_min, config.f_max,
                                        config.delta, config.n_freq_bands)
    elif config.band_spacing == 'log':
        config.frequencies = make_LogFq(config.f_min, config.f_max,
                                        config.delta, config.n_freq_bands)
    print('frequencies for filtering in (Hz):', config.frequencies)

    config.CN_HP, config.CN_LP = rec_filter_coeff(config.frequencies,
                                                  config.delta)
    if config.filter_type == 'highpass':
        config.CN_LP = [None, ] * len(config.CN_HP)
    config.filter_norm = rec_filter_norm(config.frequencies, config.delta,
                                         config.CN_HP, config.CN_LP,
                                         config.filter_npoles)
