from pyesasky.legacy.legacy_descriptors import (
    LCatalogueDescriptor,
    LFootprintSetDescriptor,
    LMetadataDescriptor,
)


class CatalogueDescriptor(LCatalogueDescriptor):

    _id_col = ""
    _name_col = ""
    _dataset_name = ""
    _line_width = 5
    _histo_color = "green"
    _metadata = []

    def __init__(
        self,
        dataset_name,
        color,
        line_width,
        id_col,
        name_col,
        ra_col,
        dec_col,
        metadata,
    ):
        self._dataset_name = dataset_name
        self._histo_color = color
        self._line_width = line_width

        self._id_col = id_col
        self._name_col = name_col
        self._ra_col = ra_col
        self._dec_col = dec_col

        self._metadata = metadata

    def get_dataset_name(self):
        return self._dataset_name

    def get_histo_color(self):
        return self._histo_color

    def get_line_width(self):
        return self._line_width

    def get_id_col(self):
        return self._id_col

    def get_name_col(self):
        return self._name_col

    def get_ra_col(self):
        return self._ra_col

    def get_dec_col(self):
        return self._dec_col

    def get_metadata(self):
        return self._metadata

    def add_metadata(self, metadataDescriptor):
        self._metadata.append(metadataDescriptor)

    def to_dict(self):

        content = dict(
            mission=self._dataset_name,
            tapTable="",
            countColumn="",
            guiShortName=self._dataset_name,
            guiLongName=self._dataset_name,
            histoColor=self._histo_color,
            countFovLimit=360,
            fovLimit=90.0,
            archiveURL="",
            archiveProductURI="",
            adsPublicationsMaxRows=0,
            tabCount=0,
            sourceLimit=100000,
            sourceLimitDescription="",
            posTapColumn="pos",
            polygonRaTapColumn=self._ra_col,
            polygonDecTapColumn=self._dec_col,
            polygonNameTapColumn=self._name_col,
            orderBy="",
            metadata=self._metadata,
        )
        return content


class FootprintSetDescriptor(LFootprintSetDescriptor):

    _id_col = ""
    _name_col = ""
    _stcs_col = ""
    _ra_center_col = ""
    _dec_center_col = ""
    _dataset_name = ""
    _line_width = 5
    _histo_color = "green"
    _metadata = []

    def __init__(
        self,
        dataset_name,
        color,
        line_width,
        id_col,
        name_col,
        stcs_col,
        ra_center_col,
        dec_center_col,
        metadata,
    ):
        self._dataset_name = dataset_name
        self._histo_color = color
        self._line_width = line_width

        self._id_col = id_col
        self._name_col = name_col
        self._stcs_col = stcs_col
        self._ra_center_col = ra_center_col
        self._dec_center_col = dec_center_col

        self._metadata = metadata

    def get_dataset_name(self):
        return self._dataset_name

    def get_histo_color(self):
        return self._histo_color

    def get_line_width(self):
        return self._line_width

    def get_id_col(self):
        return self._id_col

    def get_name_col(self):
        return self._name_col

    def get_stcs_col(self):
        return self._stcs_col

    def get_ra_center_col(self):
        return self._ra_center_col

    def get_dec_center_col(self):
        return self._dec_center_col

    def get_metadata(self):
        return self._metadata

    def add_metadata(self, metadataDescriptor):
        self._metadata.append(metadataDescriptor)


class MetadataDescriptor(LMetadataDescriptor):

    _tap_name = ""
    _label = ""
    _visible = True
    _type = ""
    _index = 0
    _max_decimals = 4

    def __init__(self, label, col_type, max_decimals):
        self._tap_name = label
        self._label = label
        self._type = col_type
        if max_decimals:
            self._max_decimals = max_decimals

    def get_label(self):
        return self._tap_name

    def get_col_type(self):
        return self._type
