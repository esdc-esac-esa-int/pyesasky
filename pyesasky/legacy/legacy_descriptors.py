from pyesasky.legacy.legacy_utils import deprecated


class LCatalogueDescriptor:

    @deprecated('get_dataset_name')
    def getDatasetName(self):
        pass

    @deprecated('get_histo_color')
    def getHistoColor(self):
        pass

    @deprecated('get_line_width')
    def getLineWidth(self):
        pass

    @deprecated('get_id_col')
    def getIdColumnName(self):
        pass

    @deprecated('get_name_col')
    def getNameColumnName(self):
        pass

    @deprecated('get_ra_col')
    def getRADegColumnName(self):
        pass

    @deprecated('get_dec_col')
    def getDecDegColumnName(self):
        pass

    @deprecated('get_metadata')
    def getMetadata(self):
        pass

    @deprecated('add_metadata')
    def addMetadataDefinition(self, metadataDescriptor):
        pass

    @deprecated('to_dict')
    def toDict(self):
        pass


class LFootprintSetDescriptor:

    @deprecated('get_dataset_name')
    def getDatasetName(self):
        pass

    @deprecated('get_histo_color')
    def getHistoColor(self):
        pass

    @deprecated('get_line_width')
    def getLineWidth(self):
        pass

    @deprecated('get_id_col')
    def getIdColumnName(self):
        pass

    @deprecated('get_name_col')
    def getNameColumnName(self):
        pass

    @deprecated('get_stcs_col')
    def getStcsColumnName(self):
        pass

    @deprecated('get_ra_center_col')
    def getCentralRADegColumnName(self):
        pass

    @deprecated('get_dec_center_col')
    def getCentralDecDegColumnName(self):
        pass

    @deprecated('get_metadata')
    def getMetadata(self):
        pass

    @deprecated('add_metadata')
    def addMetadataDefinition(self, metadataDescriptor):
        pass


class LMetadataDescriptor:

    @deprecated('get_label')
    def getLabel(self):
        pass

    @deprecated('get_col_type')
    def getColumnType(self):
        pass
