from abc import abstractmethod
import json
import configparser
from io import StringIO
import csv
import os.path
import time
import tornado.httpserver
import tornado.web
import pandas as pd
import requests
from pyesasky.models import Catalogue, FootprintSet, MetadataType, HiPS
from pyesasky.legacy.legacy_api_interactions import LApiInteractionsMixin


class ApiInteractionsMixin(LApiInteractionsMixin):
    def __init__(self):
        super().__init__()
        self.message_timeout = 10

    @abstractmethod
    def _send_ignore(self, content):
        pass

    @abstractmethod
    def _send_receive(self, content):
        pass

    def show_coo_grid(self, show=True):
        """Overlays a coordinate grid on the sky"""

        content = dict(event="showCoordinateGrid", content=dict(show=show))
        self._send_ignore(content)

    def get_center(self, cooframe="J2000"):
        """Returns the coordinate of the center of the screen
        in specified coordinate Frame."""

        if cooframe not in ["J2000", "GALACTIC"]:
            print("Coordinate frame must be J2000 or GALACTIC")
            return
        content = dict(event="getCenter", content=dict(cooFrame=cooframe))
        return self._send_receive(content)

    def plot_obs(self, mission_id):
        """Overlays availabe observations for the specified mission on the sky"""

        content = dict(event="plotObservations", content=dict(missionId=mission_id))
        return self._send_receive(content)

    def plot_cat(self, mission_id):
        """Overlays availabe catalogues for the specified mission on the sky"""

        content = dict(event="plotCatalogues", content=dict(missionId=mission_id))
        return self._send_receive(content)

    def plot_spec(self, mission_id):
        """Overlays availabe spectra for the specified mission on the sky"""

        content = dict(event="plotSpectra", content=dict(missionId=mission_id))
        return self._send_receive(content)

    def cs_obs(self, mission_id, ra, dec, radius):
        """Overlays availabe observations within the specified cone for
        the specified mission on the sky

         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """

        content = dict(
            event="plotObservations",
            content=dict(missionId=mission_id, ra=ra, dec=dec, radius=radius),
        )
        return self._send_receive(content)

    def cs_cat(self, mission_id, ra, dec, radius):
        """Overlays availabe catalogues within the specified cone for the
        specified mission on the sky

         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """
        content = dict(
            event="plotCatalogues",
            content=dict(missionId=mission_id, ra=ra, dec=dec, radius=radius),
        )
        return self._send_receive(content)

    def cs_spec(self, mission_id, ra, dec, radius):
        """Overlays availabe spectra within the specified cone for the
        specified mission on the sky

         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """

        content = dict(
            event="plotSpectra",
            content=dict(missionId=mission_id, ra=ra, dec=dec, radius=radius),
        )
        return self._send_receive(content)

    def get_obs_count(self):
        """Returns the number of observations per mission in the current
        view of the sky"""

        content = dict(event="getObservationsCount")
        return self._send_receive(content)

    def get_cat_count(self):
        """Returns the number of catalogs per mission in the current view of the sky"""

        content = dict(event="getCataloguesCount")
        return self._send_receive(content)

    def get_pub_count(self):
        """Returns the number of publications in the current view of the sky"""

        content = dict(event="getPublicationsCount")
        return self._send_receive(content)

    def get_spec_count(self):
        """Returns the number of spectra per mission in the current view of the sky"""

        content = dict(event="getSpectraCount")
        return self._send_receive(content)

    def get_result_data(self):
        """Returns the content of the currently active datapanel as a dictionary"""
        content = dict(event="getResultPanelData")
        return self._send_receive(content)

    def close_result_tab(self, index=-1):
        """Close the tab on index or current open if no argument"""
        content = dict(event="closeResultPanelTab", content=dict(index=index))
        return self._send_ignore(content)

    def close_result(self):
        """Close all open result panel tabs"""
        content = dict(event="closeAllResultPanelTabs")
        return self._send_ignore(content)

    def get_available_public_hips(self, wavelength=""):
        """Returns available HiPS in ESASky
        No argument for all available HiPS.
        Specify wavelength for those available in that specific wavelength"""

        response = requests.get(
            "http://sky.esa.int/esasky-tap/hips-sources", timeout=self.message_timeout
        )
        response.raise_for_status()
        hips_map = self._parse_hips_json(response.text)
        if len(wavelength) > 0:
            if wavelength.upper() in hips_map.keys():
                return hips_map[wavelength.upper()]
            else:
                print("No wavelength: " + wavelength + " in ESASky")
                print("Available wavelengths are: ")
                print(hips_map.keys())
        else:
            return hips_map

    def get_available_hips(self, wavelength=""):
        """Returns available HiPS in ESASky
        No argument for all available HiPS.
        Specify wavelength for those available in that specific wavelength"""

        content = dict(event="getAvailableHiPS", content=dict(wavelength=wavelength))
        return self._send_receive(content)

    def _parse_hips_json(self, HiPSJson):
        HiPSJson = json.loads(HiPSJson)
        if "total" in HiPSJson.keys():
            hips_map = dict()
            for i in range(HiPSJson["total"]):
                wavelength = HiPSJson["menuEntries"][i]
                wavelength_map = dict()
                for j in range(wavelength["total"]):
                    hips = wavelength["hips"][j]
                    wavelength_map[hips["surveyName"]] = hips
                hips_map[wavelength["wavelength"]] = wavelength_map
            return hips_map

    def go_to(self, ra, dec):
        """Moves the center of the view to the specified coordinate
        in current coordinate system

        Arguments:
        ra -- float or string in sexagesimal or decimal format
        dec -- float or string in sexagesimal or decimal format
        """

        content = dict(event="goToRaDec", content=dict(ra=ra, dec=dec))
        self._send_ignore(content)

    def go_to_target(self, target_name):
        """Moves to targetName resolved by SIMBAD"""

        content = dict(event="goToTargetName", content=dict(targetName=target_name))
        self._send_ignore(content)
        # Add small sleeper to wait for simbad to react
        time.sleep(1)

    def set_fov(self, fov_deg):
        """Sets the views Field of View in degrees"""

        content = dict(event="setFov", content=dict(fov=fov_deg))
        self._send_ignore(content)

    def set_hips_color(self, color_palette):
        """Sets the colorpalette of the currently active sky to spcified value"""

        content = dict(
            event="setHipsColorPalette", content=dict(colorPalette=color_palette)
        )
        self._send_ignore(content)

    def close_jwst(self):
        """Closes the JWST observation planning tool panel"""

        content = dict(event="closeJwstPanel")
        self._send_ignore(content)

    def open_jwst(self):
        """Opens the JWST observation planning tool panel"""

        content = dict(event="openJwstPanel")
        self._send_ignore(content)

    def clear_jwst(self):
        """Removes all rows in the JWST observation planning tool panel"""
        content = dict(event="clearJwstAll")
        self._send_ignore(content)

    def add_jwst(
        self, instrument, detector, show_all_instr, ra=None, dec=None, rotation=None
    ):
        """Adds specified instrument and detector to the center of the screen
        for the JWST observation planning tool panel"""

        content: str
        if ra and dec and rotation:
            content = dict(
                event="addJwstWithCoordinates",
                content=dict(
                    instrument=instrument,
                    detector=detector,
                    showAllInstruments=show_all_instr,
                    ra=ra,
                    dec=dec,
                    rotation=rotation,
                ),
            )
        else:
            content = dict(
                event="addJwst",
                content=dict(
                    instrument=instrument,
                    detector=detector,
                    showAllInstruments=show_all_instr,
                ),
            )

        self._send_receive(content)

    def overlay_cat(self, catalogue, show_data=False):
        """Overlays a catalogue created by pyesasky.catalogue in the sky"""

        event = "overlayCatalogueWithDetails" if show_data else "overlayCatalogue"
        content = dict(event=event, content=catalogue.to_dict())
        self._send_ignore(content)

    def clear_cat(self, name):
        """Clears all objects in named visualised catalogue"""

        content = dict(event="clearCatalogue", content=dict(overlayName=name))
        self._send_ignore(content)

    def delete_cat(self, name):
        """Deletes named visualised cataloge"""

        content = dict(event="deleteCatalogue", content=dict(overlayName=name))
        self._send_ignore(content)

    def overlay_footprints(self, footprints, show_data=False):
        """Overlays footprints created by pyesasky.footprint in the sky"""

        event = "overlayFootprintsWithDetails" if show_data else "overlayFootprints"
        content = dict(event=event, content=dict(footprints.to_dict()))
        self._send_ignore(content)

    def clear_footprints(self, overlay_name):
        """Clears all objects in named visualised footprint table"""
        content = dict(
            event="clearFootprintsOverlay", content=dict(overlayName=overlay_name)
        )
        self._send_ignore(content)

    def delete_footprints(self, overlay_name):
        """Deletes named visualised footprint table"""

        content = dict(
            event="deleteFootprintsOverlay", content=dict(overlayName=overlay_name)
        )
        self._send_ignore(content)

    def overlay_footprints_csv(self, path, delimiter, descriptor):
        """Overlays footprints read from a csv file"""

        footprint_set = FootprintSet(
            descriptor.get_dataset_name(),
            "J2000",
            descriptor.get_histo_color(),
            descriptor.get_line_width(),
        )

        # read colums
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    columns = row
                    print(f'Columns identified: {", ".join(row)}')
                    line_count += 1
                    i = 0
                    while i < len(columns):
                        if columns[i] == descriptor.get_id_col():
                            col_id = columns[i]
                            print("{id} mapped to " + col_id)
                            if (
                                descriptor.get_id_col()
                                == descriptor.get_name_col()
                            ):
                                col_name = col_id
                                print("{name} mapped to " + col_name)
                        elif columns[i] == descriptor.get_name_col():
                            col_name = columns[i]
                            print("{name} mapped to " + col_name)
                        elif columns[i] == descriptor.get_stcs_col():
                            col_stcs = columns[i]
                            print("{stcs} mapped to " + col_stcs)
                        elif columns[i] == descriptor.get_ra_center_col():
                            col_ra = columns[i]
                            print("{centerRaDeg} mapped to " + col_ra)
                        elif columns[i] == descriptor.get_dec_center_col():
                            col_dec = columns[i]
                            print("{centerDecDeg} mapped to " + col_dec)
                        i += 1
                else:
                    i = 0
                    c_details = []
                    c_id = ""
                    c_name = ""
                    c_stcs = ""
                    c_ra = ""
                    c_deg = ""

                    while i < len(row):
                        if columns[i] == descriptor.get_id_col():
                            c_id = row[i]
                            if (
                                descriptor.get_id_col()
                                == descriptor.get_name_col()
                            ):
                                c_name = c_id
                        elif columns[i] == descriptor.get_name_col():
                            c_name = row[i]
                        elif columns[i] == descriptor.get_stcs_col():
                            c_stcs = row[i]
                        elif columns[i] == descriptor.get_ra_center_col():
                            c_ra = row[i]
                        elif columns[i] == descriptor.get_dec_center_col():
                            c_deg = row[i]
                        else:
                            c_meta = {}
                            found = False
                            if len(descriptor.get_metadata()) > 0:
                                j = 0
                                while j < len(descriptor.get_metadata()):
                                    if (
                                        descriptor.get_metadata()[j].get_label()
                                        == columns[i]
                                    ):
                                        found = True
                                        c_meta["name"] = descriptor.get_metadata()[
                                            j
                                        ].get_label()
                                        c_meta["value"] = row[i]
                                        c_meta["type"] = descriptor.get_metadata()[
                                            j
                                        ].get_col_type()

                                        break
                                    j += 1
                            elif not found:
                                c_meta["name"] = columns[i]
                                c_meta["value"] = row[i]
                                c_meta["type"] = MetadataType.STRING

                            c_details.append(c_meta)

                        i += 1

                    footprint_set.add_footprint(
                        c_name, c_stcs, c_id, c_ra, c_deg, c_details
                    )

                    line_count += 1
            print(f"Processed {line_count} lines.")
            self.overlay_footprints(footprint_set, show_data=True)

    def overlay_footprints_astropy(self, descriptor, table):
        i = 0

        footprint_set = FootprintSet(
            descriptor.get_dataset_name(),
            "J2000",
            descriptor.get_histo_color(),
            descriptor.get_line_width(),
        )

        while i < len(table.colnames):

            if table.colnames[i] == descriptor.get_id_col():
                col_id = table.colnames[i]
                print("{id} mapped to " + col_id)
                if descriptor.get_id_col() == descriptor.get_name_col():
                    col_name = col_id
                    print("{name} mapped to " + col_name)
            elif table.colnames[i] == descriptor.get_name_col():
                col_name = table.colnames[i]
                print("{name} mapped to " + col_name)
            elif table.colnames[i] == descriptor.get_stcs_col():
                col_stcs = table.colnames[i]
                print("{stcs} mapped to " + col_stcs)
            elif table.colnames[i] == descriptor.get_ra_center_col():
                col_ra = table.colnames[i]
                print("{centerRaDeg} mapped to " + col_ra)
            elif table.colnames[i] == descriptor.get_dec_center_col():
                col_dec = table.colnames[i]
                print("{centerDecDeg} mapped to " + col_dec)
            i += 1

        j = 0
        c_id = j

        while j < len(table):
            c_details = []
            k = 0
            while k < len(table.colnames):
                col_meta = {}
                col_name = table.colnames[k]
                if isinstance(table[j][k], bytes):
                    col_val = str(table[j][k].decode("utf-8"))
                else:
                    col_val = str(table[j][k])
                c_ra = []
                c_dec = []

                if col_name == descriptor.get_name_col():
                    c_name = col_val
                elif col_name == descriptor.get_stcs_col():
                    c_stcs = col_val
                elif col_name == descriptor.get_ra_center_col():
                    c_ra = col_val
                elif col_name == descriptor.get_dec_center_col():
                    c_dec = col_val
                else:
                    col_meta = {}
                    found = False
                    if len(descriptor.get_metadata()) > 0:
                        index = 0
                        while index < len(descriptor.get_metadata()):
                            if descriptor.get_metadata()[j].get_label() == col_name:
                                found = True
                                col_meta["name"] = descriptor.get_metadata()[
                                    j
                                ].get_label()
                                col_meta["value"] = col_val
                                col_meta["type"] = descriptor.get_metadata()[
                                    j
                                ].get_col_type()

                                break
                            index += 1
                    elif not found:
                        col_meta["name"] = col_name
                        col_meta["value"] = col_val
                        col_meta["type"] = MetadataType.STRING

                    c_details.append(col_meta)
                k += 1

            j += 1
            footprint_set.add_footprint(c_name, c_stcs, c_id, c_ra, c_dec, c_details)

        print(f"Processed {j} lines.")
        self.overlay_footprints(footprint_set, show_data=True)

    def overlay_cat_astropy(
        self,
        name,
        frame,
        color,
        line_width,
        table,
        ra_col,
        dec_col,
        id_col,
    ):

        is_user_ra_col = True
        is_user_dec_col = True
        is_user_id_col = True

        if not ra_col:
            ra_col = ""
            is_user_ra_col = False

        if not dec_col:
            dec_col = ""
            is_user_dec_col = False

        if not id_col:
            id_col = ""
            is_user_id_col = False

        i = 0

        if not is_user_ra_col and not is_user_dec_col and not is_user_id_col:

            while i < len(table.colnames):

                col_name = table.colnames[i]

                if len(table[col_name].meta) > 0:
                    meta_type = table[col_name].meta["ucd"]
                    if "pos.eq.ra;meta.main" in meta_type and not is_user_ra_col:
                        ra_col = col_name
                    elif "pos.eq.dec;meta.main" in meta_type and not is_user_dec_col:
                        dec_col = col_name
                    elif "meta.id;meta.main" in meta_type and not is_user_id_col:
                        id_col = col_name
                i += 1

        if not line_width:
            line_width = 5

        cat = Catalogue(name, frame, color, line_width)

        j = 0
        source_id = 0
        while j < len(table):
            details = []
            ra = None
            dec = None
            k = 0
            while k < len(table.colnames):
                meta = {}
                col_name = table.colnames[k]
                if isinstance(table[j][k], bytes):
                    value = str(table[j][k].decode("utf-8"))
                else:
                    value = str(table[j][k])

                if col_name == ra_col:
                    ra = value

                elif col_name == dec_col:
                    dec = value

                elif col_name == id_col:
                    name = value

                else:
                    meta["name"] = col_name
                    meta["value"] = value
                    if "ucd" in table[col_name].meta:
                        meta["type"] = self._ucd_type_to_esasky(
                            table[col_name].meta["ucd"]
                        )
                    else:
                        meta["type"] = "STRING"
                    details.append(meta)

                k += 1

            source_id = j
            cat.add_source(name, ra, dec, source_id, details)
            j += 1

        self.overlay_cat(cat)

    def _ucd_type_to_esasky(self, tap_type):
        if tap_type == "meta.number":
            return "DOUBLE"
        else:
            return "STRING"

    def overlay_cat_csv(self, file_path, delimiter, descriptor, cooframe):
        """Overlays catalogue read from a csv file"""

        catalogue = Catalogue(
            descriptor.get_dataset_name(),
            cooframe,
            descriptor.get_histo_color(),
            descriptor.get_line_width(),
        )

        # read colums
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    columns = row
                    print(f'Column identified: {", ".join(row)}')
                    line_count += 1
                    i = 0
                    while i < len(columns):
                        if columns[i] == descriptor.get_id_col():
                            col_id = columns[i]
                            print("{id} column identified: " + col_id)
                            if descriptor.get_id_col() == descriptor.get_name_col():
                                col_name = col_id
                                print("{name} column identified: " + col_name)
                        elif columns[i] == descriptor.get_name_col():
                            col_name = columns[i]
                            print("{name} column identified: " + col_name)
                        elif columns[i] == descriptor.get_ra_col():
                            col_ra = columns[i]
                            print("{centerRaDeg} column identified: " + col_ra)
                        elif columns[i] == descriptor.get_dec_col():
                            col_dec = columns[i]
                            print("{currDecDeg} column identified: " + col_dec)
                        i += 1
                else:
                    i = 0
                    details = []
                    col_id = ""
                    name = ""
                    ra = ""
                    dec = ""

                    while i < len(row):
                        if columns[i] == descriptor.get_id_col():
                            col_id = row[i]
                            if descriptor.get_id_col() == descriptor.get_name_col():
                                name = col_id
                        elif columns[i] == descriptor.get_name_col():
                            name = row[i]
                        elif columns[i] == descriptor.get_ra_col():
                            ra = row[i]
                        elif columns[i] == descriptor.get_dec_col():
                            dec = row[i]
                        else:
                            meta = {}
                            found = False
                            if len(descriptor.get_metadata()) > 0:
                                j = 0
                                while j < len(descriptor.get_metadata()):
                                    if (
                                        descriptor.get_metadata()[j].get_label()
                                        == columns[i]
                                    ):
                                        found = True
                                        meta["name"] = descriptor.get_metadata()[
                                            j
                                        ].get_label()
                                        meta["value"] = row[i]
                                        meta["type"] = descriptor.get_metadata()[
                                            j
                                        ].get_col_type()
                                        break
                                    j += 1
                            elif not found:
                                meta["name"] = columns[i]
                                meta["value"] = row[i]
                                meta["type"] = MetadataType.STRING

                            details.append(meta)

                        i += 1

                    catalogue.add_source(name, ra, dec, col_id, details)
                    line_count += 1
            print(f"Processed {line_count} lines.")
            self.overlay_cat(catalogue, show_data=True)

    def overlay_moc(self, moc_obj, name="MOC", color="", opacity=0.2, mode="healpix"):
        """Overlay HealPix Multi-Order Coverage map"""
        moc_str = "{"
        if isinstance(moc_obj, dict):
            for order in moc_obj.keys():
                moc_str += '"' + order + '":['
                for val in moc_obj[order]:
                    if "-" in str(val):
                        start = int(val.split("-")[0])
                        end = int(val.split("-")[1])
                        for i in range(start, end + 1):
                            moc_str += str(i) + ","
                    else:
                        moc_str += str(val) + ","
                moc_str = moc_str[:-1] + "],"

            moc_str = moc_str[:-1] + "}"
        elif "/" in moc_obj:
            order = ""
            for val in moc_obj.split(" "):
                if "/" in val:
                    if order != "":
                        moc_str = moc_str[:-1] + "],"
                    order = val.split("/")[0]
                    moc_str += '"' + order + '":['
                    val = val.split("/")[1]

                if "-" in str(val):
                    start = int(val.split("-")[0])
                    end = int(val.split("-")[1])
                    for i in range(start, end + 1):
                        moc_str += str(i) + ","
                else:
                    moc_str += str(val) + ","
            moc_str = moc_str[:-1] + "]}"
        else:
            moc_str = moc_obj
        content = dict(
            event="addMOC",
            content=dict(
                options=dict(color=color, opacity=opacity, mode=mode),
                mocData=moc_str,
                name=name,
            ),
        )
        self._send_ignore(content)

    def remove_moc(self, name="MOC"):
        content = dict(event="removeMOC", content=dict(name=name))
        return self._send_ignore(content)

    def open_sky_panel(self):
        """Opens the sky selector panel"""
        content = dict(event="openSkyPanel")
        self._send_ignore(content)

    def close_sky_panel(self):
        """Closes the sky selector panel"""
        content = dict(event="closeSkyPanel")
        self._send_ignore(content)

    def get_sky_row_count(self):
        """Returns the number of rows in the sky panel"""
        content = dict(event="getNumberOfSkyRows")
        return self._send_receive(content)

    def remove_hips(self, index=-1):
        """Removes HiPS row in the skypanel either at "index"
        or no argument for all except the first"""
        content = dict(event="removeHips", content=dict(index=index))
        self._send_receive(content)

    def set_hips_slider(self, value):
        """Sets the value of the HiPS slider to fade between
        the HiPS in the skypanel.
        Valid values are 0 to nSkyRows - 1"""
        content = dict(event="setHipsSliderValue", content=dict(value=value))
        self._send_ignore(content)

    def add_hips_local(self, hips_url):
        """Starts a tornado server which will supply the widget with
        HiPS from a local source on client machine"""
        if not hasattr(self, "tornadoServer"):
            self._start_tornado()
        drive, tail = os.path.splitdrive(hips_url)
        if drive:
            # Windows
            url = tail.replace("\\", "/")
        else:
            url = hips_url
        url_pattern = url + "(.*)"
        self.tornadoserver.add_handlers(
            r".*", [(str(url_pattern), self.FileHandler, dict(baseUrl=hips_url))]
        )
        return url

    def select_hips(self, name, url="default"):
        """Sets the currently active row in the skypanel to either
        hipsName already existing in ESASky or adds a new name from specified URL
        """
        if url != "default":
            hips = self._parse_hips_url(name, url)
            content = dict(event="changeHipsWithParams", content=dict(hips.to_dict()))
            self._send_ignore(content)
        else:
            content = dict(event="changeHips", content=dict(hipsName=name))
            return self._send_receive(content)

    def add_hips(self, name, url="default"):
        """Adds a new row win the skypanel with either
        hipsName already existing in ESASky or adds a new name from specified URL"""
        if url != "default":
            hips = self._parse_hips_url(name, url)
            content = dict(event="addHipsWithParams", content=dict(hips.to_dict()))
            self._send_ignore(content)
        else:
            content = dict(event="addHips", content=dict(hipsName=name))
            return self._send_receive(content)

    def browse_hips(self):
        """Queries CDS for the global HiPS list and returns it as a pandas dataframe"""
        url = "http://skyint.esac.esa.int/esasky-tap/global-hipslist"
        columns = [
            "ID",
            "obs_title",
            "moc_order",
            "moc_sky_fraction",
            "em_min",
            "em_max",
            "hips_service_url",
        ]
        with requests.get(url, stream=True, timeout=self.message_timeout) as response:
            response_content = StringIO(response.content.decode("utf-8"))
            df = pd.io.json.read_json(response_content)
            return df[columns]

    def _read_properties(self, url):
        config = configparser.RawConfigParser(strict=False)
        if not url.startswith("http"):
            text = "[Dummy section]\n"
            try:
                with open(url + "properties", "r") as f:
                    text += f.read() + "\n"
                config.read_string(text)
                return config
            except FileNotFoundError as fnf_error:
                print(
                    url
                    + " not found or missing properties file.\n Did you mean http://"
                    + url
                )
                raise (fnf_error)
        else:
            response = requests.get(url + "properties", timeout=self.message_timeout)
            response.raise_for_status()
            text = "[Dummy section]\n" + response.text
            config.read_string(text)
            return config

    def _parse_hips_url(self, name, url):
        if not url.endswith("/"):
            url += "/"
        config = self._read_properties(url)
        if not url.startswith("http"):
            url = self.add_hips_local(url)
            port = self.httpserverport
            url = "http://localhost:" + str(port) + url

        max_order = config.get("Dummy section", "hips_order")
        img_format = config.get("Dummy section", "hips_tile_format").split()
        cooframe = config.get("Dummy section", "hips_frame")
        if cooframe == "equatorial":
            cooframe = "J2000"
        else:
            cooframe = "Galactic"
        if url.endswith("/"):
            url = url[:-1]
        hips = HiPS(name, url, cooframe, max_order, img_format[0])
        print("hipsURL " + url + "/index.html")
        print("imgFormat " + img_format[0])
        return hips

    def _start_tornado(self):
        class DummyHandler(tornado.web.RequestHandler):
            pass

        app = tornado.web.Application(
            [
                tornado.web.url(r"dummy", DummyHandler),
            ]
        )
        server = tornado.httpserver.HTTPServer(app)
        port_start = 8900
        port_end = 8910
        for port in range(port_start, port_end + 1):
            try:
                server.listen(port)
            except OSError as os_error:
                if port is port_end:
                    raise (os_error)
            else:
                break
        self.httpserver = server
        self.tornadoserver = app
        self.httpserverport = port

    class FileHandler(tornado.web.RequestHandler):
        def initialize(self, base_url):
            self.base_url = base_url

        def set_default_headers(self):
            self.set_header("Access-Control-Allow-Origin", "*")

        def get(self, path):
            host = self.request.host
            print(host)
            origin = host.split(":")[0]
            if not origin == "localhost":
                raise tornado.web.HTTPError(status_code=403)
            file_location = os.path.abspath(os.path.join(self.base_url, path))
            if not os.path.isfile(file_location):
                raise tornado.web.HTTPError(status_code=404)
            with open(file_location, "rb") as source_file:
                self.write(source_file.read())

    """ External TAP Services"""

    def get_tap_services(self):
        """Returns the available predefined External TAP Services in ESASky"""

        content = dict(event="getAvailableTapServices")
        return self._send_receive(content)

    def get_tap_missions(self):
        """Returns all the missions and dataproducts from the available predefined
        External TAP Services in ESASky"""

        content = dict(event="getAllAvailableTapMissions")
        return self._send_receive(content)

    def get_tap_query(self, service_name):
        """Returns the adql that will be run on this tapService"""

        content = dict(event="getTapADQL", content=dict(tapService=service_name))
        return self._send_receive(content)

    def get_tap_count(self, service_name=""):
        """Returns the available data in the current sky for the named tapService"""

        content = dict(
            event="getTapServiceCount", content=dict(tapService=service_name)
        )
        return self._send_receive(content)

    def plot_tap(self, service_name):
        """Plots data from selected mission in the an external TAP service"""

        content = dict(event="plotTapService", content=dict(tapService=service_name))
        return self._send_receive(content)

    def plot_custom_tap(
        self,
        name,
        tap_url,
        adql,
        data_in_view=True,
        color="",
        limit=-1,
    ):
        """Searches and plots data from specified TAP service

        Arguments:
        name -- (String) Name that will be shown on the screen
        tapUrl -- (String) URL to the tap service
        ADQL -- (String) The ADQL that will be used for retrieving the data
        dataOnlyInView -- (Boolean, default:True) Adds a WHERE statement to only
        retrieve data in the current view
        color -- (String, default: preset list) Color for display in RGB
        format (e.g. #FF0000 for red)
        limit -- (Int, default: 3000) Limit for amount of results to display
        """

        content = dict(
            event="plotTapServiceWithDetails",
            content=dict(
                name=name,
                tapUrl=tap_url,
                dataOnlyInView=data_in_view,
                adql=adql,
                color=color,
                limit=limit,
            ),
        )
        self._send_ignore(content)

    def save_session(self, file_name=None):
        """Saves the current ESASky session as a JSON file object with all settings,
        HiPS stack, datapanels etc. Returns the dict with settings

        Arguments:
        fileName -- (String, Optional ) Filename or path to file where to save the
        settings. Won't save to file if empty
        """
        content = dict(event="saveState")
        session = self._send_receive(content)
        if "session" in session:
            session = session["session"]
        if file_name:
            out_file = open(file_name, "w")
            out_file.write(json.dumps(session))
            out_file.close()
        return session

    def restore_session_file(self, file_name):
        """Restores a ESASky session from a JSON file with all settings, HiPS stack,
        datapanels etc

        Arguments:
        fileName -- (String ) Filename or path to file where settings are saved
        """
        file = open(file_name, "r")
        state = json.loads(file.read())
        self.restore_session_obj(state)

    def restore_session_obj(self, session):
        """Restores a ESASky session from a dict with all settings,
        HiPS stack, datapanels etc

        Arguments:
        sessiont -- (Dict) Dictionary with the settings to restore
        """
        content = dict(event="restoreState", content=dict(state=session))
        self._send_ignore(content)

    def get_gw_ids(self):
        """Returns the IDs of all available Gravitational Events in ESASky"""

        content = dict(event="getGWIds")
        return self._send_receive(content)

    def get_gw_data(self):
        """Returns the metadata of all available Gravitational Events in ESASky"""

        content = dict(event="getAllGWData")
        return self._send_receive(content)

    def get_neutorino_data(self):
        """Returns the metadata of all available Neutrino Events in ESASky"""

        content = dict(event="getNeutrinoEventData")
        return self._send_receive(content)

    def show_gw_event(self, id: str):
        """Shows the Gravitational Event by ID in ESASky
        Arguments:
        id -- (String) Grace ID of gravitational event to show
        """

        content = dict(event="showGWEvent", content=dict(id=id))
        self._send_ignore(content)

    def open_neutorino_panel(self):
        """Opens the neutrino event panel"""

        content = dict(event="openNeutrinoPanel")
        return self._send_ignore(content)

    def open_gw_panel(self):
        """Opens the Gravitational Wave event panel"""

        content = dict(event="openGWPanel")
        return self._send_ignore(content)

    def close_event_panel(self):
        """Closes the alert/event panel"""

        content = dict(event="closeAlertPanel")
        return self._send_ignore(content)

    def open_search_panel(self):
        """Opens the search tool panel"""

        content = dict(event="showSearchTool")
        self._send_ignore(content)

    def close_search_panel(self):
        """Close the search tool panel"""

        content = dict(event="closeSearchTool")
        self._send_ignore(content)

    def cone_search(self, ra, dec, radius):
        """Create a cone search area"""

        content = dict(
            event="setConeSearchArea", content=dict(ra=ra, dec=dec, radius=radius)
        )

        self._send_ignore(content)

    def poly_search(self, stcs):
        """Create a polygon search area"""

        content = dict(event="setPolygonSearchArea", content=dict(stcs=stcs))

        self._send_ignore(content)

    def clear_search(self):
        """Clear the search area"""

        content = dict(event="clearSearchArea")

        self._send_ignore(content)
