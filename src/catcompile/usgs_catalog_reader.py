import pandas as pd
import datetime
from openquake.cat.parsers.base import (BaseCatalogueDatabaseReader,_to_str)
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
        super(UsgsCsvReader, self).__init__(filename,
                                selected_origin_agencies,
                                selected_magnitude_agencies)

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
        for i in range(len(df.index)):
            eventID = _to_str(df.at[i, 'eventID'])
            year = df.at[i, 'year']
            month = df.at[i, 'month']
            day = df.at[i, 'day']
            hour = df.at[i, 'hour']
            minute = df.at[i, 'minute']
            second = df.at[i, 'second']
            latitude = df.at[i, 'latitude']
            longitude = df.at[i, 'longitude']
            depth = df.at[i, 'depth']
            magnitude = df.at[i, 'magnitude']
            magnitudeType = _to_str(df.at[i, 'magnitudeType'])
            nst = df.at[i, 'nst']
            gap = df.at[i, 'gap']
            dmin = df.at[i, 'dmin']
            rms = df.at[i, 'rms']
            type = _to_str(df.at[i, 'type'])
            horizontalError = df.at[i, 'horizontalError']
            depthError = df.at[i, 'depthError']
            magError = df.at[i, 'magError']
            magNst = df.at[i, 'magNst']
            status = _to_str(df.at[i, 'status'])
            locationSource = _to_str(df.at[i, 'locationSource'])
            magSource = _to_str(df.at[i, 'magSource'])

            date = datetime.date(year, month, day)
            time = datetime.time(int(hour), int(minute), int(second), 
                                 int(1.E6*(second % 1)))
            origin_metadata = {
                'Nstations': nst, 'AzimuthGap': gap,
                'minDist': dmin, 'EventType': type}
            
            location = Location(eventID, longitude, latitude, depth, 
                depth_error=depthError)
            
            if len(self.selected_origin_agencies) and \
                locationSource.upper() not in \
                    [origs.upper() for origs in self.selected_origin_agencies]:
                # Origin not an instance of (or authored by) a selected agency
                continue
            origins.append(
                Origin(eventID, date, time, location, locationSource, 
                    is_prime=True, time_rms=rms, metadata=origin_metadata)) 
            
            if len(self.selected_magnitude_agencies) and \
                magSource.upper() not in \
                    [mags.upper() for mags in self.selected_magnitude_agencies]:
                # Magnitude not an instance of (or authored by) selected agency
                continue
            magnitudes.append(
                Magnitude(eventID, eventID, magnitude, magSource, 
                    scale=magnitudeType, sigma=magError, stations=magNst)) 

            event = Event(eventID, origins, magnitudes)
            self._get_event(event, origins, magnitudes)

            print(f'[{i+1}] Event {eventID} successfully appended.')

        self.catalogue.ids = [e.id for e in self.catalogue.events]

        return self.catalogue
