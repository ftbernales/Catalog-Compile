"""
Weatherill (2015) Table 1. Mw conversions
"""
def iscgem_mw(magnitude):
    """
    For Mw recorded by ISCGEM take the value with no uncertainty
    """
    return magnitude

def iscgem_mw_sigma():
    """
    No additional uncertainty   
    """
    return 0.0

def gcmt_mw(magnitude):
    """
    For Mw recorded by GCMT take the value with no uncertainty
    """
    return magnitude

def gcmt_mw_sigma():
    """
    No additional uncertainty   
    """
    return 0.0

def neic_mw(magnitude):
    """
    If Mw reported by NEIC,
    """
    return 1.021 * magnitude - 0.091

def neic_mw_sigma():
    """
    Uncertainty of 0.101 units
    """
    return 0.105

def nied_mw(magnitude):
    """
    If Mw reported by NIED,
    """
    return 0.964 * magnitude + 0.248

def nied_mw_sigma():
    """
    Uncertainty of 0.11 units
    """
    return 0.11

def isc_ms(magnitude):
    """
    If Ms reported by ISC, convert to Mw from Weatherill (2015),
    """
    if magnitude > 6.0:
        return 0.994 * magnitude + 0.1        
    else:
        return 0.616 * magnitude + 2.369

def isc_ms_sigma(magnitude):
    """
    With Magnitude dependent uncertainty
    """
    if magnitude > 6.0:
        return 0.174
    else:
        return 0.147

def neic_ms(magnitude):
    """
    If Ms reported by NEIC, convert to Mw from Weatherill (2015),
    """
    if magnitude > 6.47:
        return 1.005 * magnitude - 0.026       
    else:
        return 0.723 * magnitude + 1.798

def neic_ms_sigma(magnitude):
    """
    With Magnitude dependent uncertainty
    """
    if magnitude > 6.47:
        return 0.187
    else:
        return 0.159
    
def neic_msz(magnitude):
    """
    If Msz reported by NEIC, convert to Mw from Weatherill (2015),
    """
    if magnitude > 6.47:
        return 0.950 * magnitude + 0.359     
    else:
        return 0.707 * magnitude + 1.933

def neic_msz_sigma(magnitude):
    """
    With Magnitude dependent uncertainty
    """
    if magnitude > 6.47:
        return 0.204
    else:
        return 0.179

def neic_mb(magnitude):
    """
    If Mb reported by NEIC,
    """
    return 1.159 * magnitude - 0.659

def neic_mb_sigma(magnitude):
    """
    Uncertainty of 0.283 units
    """
    return 0.283

def isc_mb(magnitude):
    """
    If Mw reported by isc,
    """
    return 1.084 * magnitude - 0.142

def isc_mb_sigma():
    """
    Uncertainty of 0.317 units
    """
    return 0.317

def ps_ms(magnitude):
    """
    For Ms recorded by paS take the value with no uncertainty. 
    In their database Pacheco & Sykes (1992) use
    the 20-s period Ms value, which, for our purposes, we treat as
    equivalent to MW in the magnitude range 7.0 ≤ MW ≤ 8.0. (Weatherill, 2015)
    """
    return magnitude

def ps_ms_sigma(magnitude):
    """
    0.2 additional uncertainty   
    """
    return 0.2

def phivolcs_ms(magnitude):
    """
    own regression
    """
    if magnitude < 5.8:
        return 0.407 * magnitude + 3.225  
    else:
        return 1.470 * magnitude - 2.937

def phivolcs_ms_sigma(magnitude):
    """
    own regression
    """
    if magnitude < 5.8:
        return 0.223
    else:
        return 0.255

def phivolcs_mw(magnitude):
    """
    own regression
    """
    return 0.944 * magnitude + 0.362   

def phivolcs_mw_sigma(magnitude):
    """
    own regression
    """
    return 0.104

def phivolcs_mb(magnitude):
    """
    own regression
    """
    return 0.998 * magnitude - 0.305   


def phivolcs_mb_sigma(magnitude):
    """
    own regression
    """
    return 0.350

def phivolcs_mL(magnitude):
    """
    own regression
    """
    return 0.979 * magnitude + 0.711


def phivolcs_mL_sigma(magnitude):
    """
    own regression
    """
    return 0.300