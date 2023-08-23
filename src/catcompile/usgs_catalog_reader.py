import pandas as pd
import datetime
from openquake.cat.parsers.base import BaseCatalogueDatabaseReader
from openquake.cat.parsers.isf_catalogue_reader import ISFReader
from openquake.cat.isf_catalogue import (Magnitude, Location, Origin,
                                         Event, ISFCatalogue)
                                         

class UsgsCsvReader(BaseCatalogueDatabaseReader):
    """
    Class to read an CSV formatted USGS NEIC earthquake catalog considering only
    the origin agencies, the magnitude agencies, and the magnitude types
    defined by the user
    """
    def __init__(self, filename: str, selected_origin_agencies=[],
                 selected_magnitude_agencies=[]):
        super(UsgsCsvReader, self).__init__(filename, selected_origin_agencies,
                                                    selected_magnitude_agencies)
        self.rejected_catalogue = []
        self.selected_origin_agencies = [s.upper() 
                                         for s in selected_origin_agencies]
        self.selected_magnitude_agencies = [s.upper() 
                                         for s in selected_magnitude_agencies]

    def _get_event(self, event: Event, origins: Origin, magnitudes: Magnitude):
        """
        Add magnitudes and origins and event and append to the catalogue
        """
        event.origins = origins
        event.magnitudes = magnitudes
        if len(event.origins) and len(event.magnitudes):
            event.assign_magnitudes_to_origins()
            self.catalogue.events.append(event)
    
    def read_file(self, identifier, name):
        """
        Reads the catalog from csv file and assigns the identifier and name
        """
        self.catalogue = ISFCatalogue(identifier, name)
        df = pd.read_csv(self.filename, na_values="", encoding='windows-1252')

        origins = []
        magnitudes = []
        
        locationSource = (df['locationSource']).str.upper()
        magSource = (df['magSource']).str.upper() # all caps

        if len(self.selected_origin_agencies):
            origin_boolmask = locationSource.isin(self.selected_origin_agencies)
            # Origin not an instance of (or authored by) a selected agency
            self.rejected_catalogue.append(
                df.loc[origin_boolmask].values.tolist())
        else: 
            origin_boolmask = pd.Series([True] * len(df.index))

        if len(self.selected_magnitude_agencies):
            mag_boolmask = magSource.isin(self.selected_magnitude_agencies)
            # Magnitude not an instance of (or authored by) selected agency
            self.rejected_catalogue.append(df.loc[mag_boolmask].values.tolist())
        else:
            mag_boolmask = pd.Series([True] * len(df.index))

        # filter out rejected events and update dataframe
        df = df.loc[origin_boolmask & mag_boolmask]

        eventID = (df['eventID'])
        year = df['year']
        month = df['month']
        day = df['day']
        hour = df['hour']
        minute = df['minute']
        second = df['second']
        latitude = df['latitude']
        longitude = df['longitude']
        depth = df['depth']
        magnitude = df['magnitude']
        magnitudeType = (df['magnitudeType'])
        nst = df['nst']
        gap = df['gap']
        dmin = df['dmin']
        rms = df['rms']
        type = (df['type'])
        depthError = df['depthError']
        magError = df['magError']
        magNst = df['magNst']

        date = list(
            map(lambda y, m, d: datetime.date(y, m, d), year, month, day))
        time = list(
            map(lambda h, m, s: datetime.time(int(h), int(m), int(s), 
                                              int(1.E6*(s % 1))), 
                hour, minute, second))

        origin_metadata = list(
            map(lambda n, g, d, t: {'Nstations': n, 'AzimuthGap': g, 
                    'minDist': d, 'EventType': t}, 
                nst, gap, dmin, type))
                
        location = list(
            map(lambda id, lon, lat, dep, deperr: Location(id, lon, lat, dep, 
                    depth_error=deperr), 
                eventID, longitude, latitude, depth, depthError))

        origins = list(
            map(lambda id, d, t, loc, locsrc, rms, meta:
                Origin(id, d, t, loc, locsrc, is_prime=True, time_rms=rms, 
                    metadata=meta),
                eventID, date, time, location, locationSource, rms, 
                    origin_metadata)) 
        
        magnitudes = list(
            map(lambda eid, oid, mag, magsrc, scale, magerr, magnst:
                Magnitude(eid, oid, mag, magsrc, scale=scale, sigma=magerr, 
                    stations=magnst),
                eventID, eventID, magnitude, magSource, magnitudeType, magError, 
                    magNst))
        
        events = list(
            map(lambda eid, origs, mags:
                Event(eid, origs, mags),
                eventID, origins, magnitudes))
        
        # build event then append to catalog
        print(f'Length of events = {len(events)}')
        print(f'Length of origins = {len(origins)}')
        print(f'Length of magnitudes = {len(magnitudes)}')
        [self._get_event(item, origins, magnitudes) for item in events]
            
        print("Finished building events...")
        if len(self.rejected_catalogue):
            # Turn list of rejected events into its own instance of ISFCatalogue
            self.rejected_catalogue = ISFCatalogue(
                identifier + "-R",
                name + " - Rejected",
                events=self.rejected_catalogue)
        print("Reading event ids...")
        self.catalogue.ids = [e.id for e in self.catalogue.events]

        return self.catalogue
