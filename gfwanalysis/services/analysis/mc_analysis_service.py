"""MC ANALYSIS SERVICE"""

import ee
import logging
import pandas as pd
import numpy as np
from gfwanalysis.errors import MCAnalysisError


class MCAnalysisService(object):

    @staticmethod
    def analyze(timeseries, window, bin_number, mc_number):
        """This is the Monte Carlo Analysis Service
        """
        if not window:
            window = 5
        if not bin_number:
            bin_number = 100
        if not mc_number:
            mc_number = 1000
        logging.info(f"[MC Service] {timeseries}, {window}, {bin_number}, {mc_number}")
        logging.info(f"[MC service] pandas: {pd.__version__}")
        d={}
        d["window"]=window
        d["bin_number"]=bin_number
        d["mc_number"]=mc_number
        df = pd.DataFrame(list(timeseries.values()), index= list(timeseries.keys()), columns = ["Carbon_emissions"])
        boxcar = df.rolling(window=window, min_periods=window,win_type="boxcar", center=True).mean()
        t0_sigma=np.std(df.values[0:window])
        logging.info(f"[MC service] pandas: {t0_sigma}")
        tn_sigma=np.std(df.values[-window:])
        logging.info(f"[MC service] pandas: {tn_sigma}")
        cumulative_sigma = np.sqrt(t0_sigma**2 + tn_sigma**2)
        logging.info(f"[MC service] pandas: {cumulative_sigma}")
        boxcar_values = boxcar.carbon_emissions.values
        mask = np.isnan(boxcar_values)
        cleaned_boxcar_values = boxcar_values[mask != True]
        t0 = cleaned_boxcar_values[0]
        logging.info(f"[MC service] pandas: {t0}")
        tn = cleaned_boxcar_values[-1]
        logging.info(f"[MC service] pandas: {tn}")
        anomaly = tn - t0
        logging.info(f"[MC service] pandas: {anomaly}")

        # Build the Monte Carlo distribution (null cases)
        values = list(df.values.flatten())
        logging.info(f"[MC service] pandas: {values}")

        mc_pop = []
        for draw in range(mc_number):
            tmp_mean1 = np.array(random.choices(population=values, k=window)).mean()
            tmp_mean2 = np.array(random.choices(population=values, k=window)).mean()
            tmp_anom = tmp_mean1 - tmp_mean2
            mc_pop.append(tmp_anom)

        hist = np.histogram(mc_pop, bins=bin_number)   
        bins = hist[1]
        density = hist[0] / hist[0].sum()
        step = (bins[1] - bins[0])
        bcenter = [bpos + step for bpos in bins[:-1]] 






        return d