import struct
from typing import BinaryIO

__all__ = ["Time", "MetaData", "SummaryData", "MeanData", "RunDataPoint", "FullDataHeaders", "DataFile"]

N_TAGS = 4

class Time:
    _format = "6B"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        if len(data) != Time._size:
            raise ValueError(f"Data must be exactly {Time._size} bytes long")
        self.hour, self.minute, self.second, self.day, self.month, self.year = struct.unpack(Time._format, data)
    
    def __repr__(self):
        return f"Time(hour={self.hour}, minute={self.minute}, second={self.second}, day={self.day}, month={self.month}, year={self.year})"
    
class MetaData:
    _format = f"6s H 6s 2B 4B 4B 2I 6s 6s 6s 6s 6s B B I B B H H H {N_TAGS}I"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        if len(data) != MetaData._size:
            raise ValueError(f"Data must be exactly {MetaData._size} bytes long")
        unpacked_data = struct.unpack(MetaData._format, data)
        
        self.file_creation = Time(unpacked_data[0])
        self.R1 = unpacked_data[1]
        self.gps_file_creation = Time(unpacked_data[2])
        self.software_version_patch = unpacked_data[3]
        self.head_software_version_patch = unpacked_data[4]
        self.hardware = (unpacked_data[5], unpacked_data[6])
        self.software = (unpacked_data[7], unpacked_data[8])
        self.head_software = (unpacked_data[9], unpacked_data[10])
        self.head_hardware = (unpacked_data[11], unpacked_data[12])
        self.device_id = unpacked_data[13]
        self.head_id = unpacked_data[14]
        self.last_service = Time(unpacked_data[15])
        self.load_cells_last_test_measurement = Time(unpacked_data[16])
        self.load_cells_last_calibration = Time(unpacked_data[17])
        self.rail_temperature_last_calibration = Time(unpacked_data[18])
        self.air_temperature_last_calibration = Time(unpacked_data[19])
        self.repeats = unpacked_data[20]
        self.runs = unpacked_data[21]
        self.averaging_mode = unpacked_data[22]
        self.full_data = unpacked_data[23]
        self.R2 = unpacked_data[24]
        self.R3 = unpacked_data[25]
        self.n_mean_sections = unpacked_data[26]
        self.n_full_data_sections = unpacked_data[27]
        self.tag_info_lengths = unpacked_data[28:]
    
    def __repr__(self):
        return (f"MetaData(file_creation={self.file_creation}, R1={self.R1}, gps_file_creation={self.gps_file_creation}, "
                f"software_version_patch={self.software_version_patch}, head_software_version_patch={self.head_software_version_patch}, "
                f"hardware={self.hardware}, software={self.software}, head_software={self.head_software}, head_hardware={self.head_hardware}, "
                f"device_id={self.device_id}, head_id={self.head_id}, last_service={self.last_service}, "
                f"load_cells_last_test_measurement={self.load_cells_last_test_measurement}, load_cells_last_calibration={self.load_cells_last_calibration}, "
                f"rail_temperature_last_calibration={self.rail_temperature_last_calibration}, air_temperature_last_calibration={self.air_temperature_last_calibration}, "
                f"averaging_mode={self.averaging_mode}, repeats={self.repeats}, runs={self.runs}, full_data={self.full_data}, "
                f"n_mean_sections={self.n_mean_sections}, n_full_data_sections={self.n_full_data_sections}, "
                f"tag_info_lengths={self.tag_info_lengths})")
    
class SummaryData:
    _format = f"{N_TAGS}B 11f 4I"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        
        if len(data) != SummaryData._size:
            raise ValueError(f"Data must be exactly {SummaryData._size} bytes long")
        unpacked_data = struct.unpack(SummaryData._format, data)

        self.tags = unpacked_data[:N_TAGS]
        self.rail_head_temperature = unpacked_data[N_TAGS]
        self.humidity = unpacked_data[N_TAGS+1]
        self.air_temperature = unpacked_data[N_TAGS+2]
        self.air_pressure = unpacked_data[N_TAGS+3]
        self.incline = unpacked_data[N_TAGS+4]
        self.roll = unpacked_data[N_TAGS+5]
        self.latitude = unpacked_data[N_TAGS+6]
        self.longitude = unpacked_data[N_TAGS+7]
        self.run_cof_max = unpacked_data[N_TAGS+8]
        self.run_cof_min = unpacked_data[N_TAGS+9]
        self.cov_fn_max = unpacked_data[N_TAGS+10]
        self.test_number_dev_total = unpacked_data[N_TAGS+11]
        self.fault_codes = unpacked_data[N_TAGS+12]
        self.R1 = unpacked_data[N_TAGS+13]
        self.R2 = unpacked_data[N_TAGS+14]
    
    def __repr__(self):
        return (f"SummaryData(tags={self.tags}, rail_head_temperature={self.rail_head_temperature}, humidity={self.humidity}, "
                f"air_temperature={self.air_temperature}, air_pressure={self.air_pressure}, incline={self.incline}, "
                f"roll={self.roll}, latitude={self.latitude}, longitude={self.longitude}, run_cof_max={self.run_cof_max}, "
                f"run_cof_min={self.run_cof_min}, cov_fn_max={self.cov_fn_max}, test_number_dev_total={self.test_number_dev_total}, "
                f"fault_codes={self.fault_codes}, R1={self.R1}, R2={self.R2})")
    
class MeanData:
    _format = "4f"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        if len(data) != MeanData._size:
            raise ValueError(f"Data must be exactly {MeanData._size} bytes long")
        self.average_fn, self.average_ft, self.cov_fn, self.cof = struct.unpack(MeanData._format, data)
    
    def __repr__(self):
        return f"MeanData(average_fn={self.average_fn}, average_ft={self.average_ft}, cov_fn={self.cov_fn}, cof={self.cof})"

class RunDataPoint:
    _format = "2B 2H I 3f"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        if len(data) != RunDataPoint._size:
            raise ValueError(f"Data must be exactly {RunDataPoint._size} bytes long")
        (self.progress, self.set_angle, self.set_speed, self.set_force,
         self.millis_from_start, self.angle, self.fn, self.ft) = struct.unpack(RunDataPoint._format, data)
    
    def __repr__(self):
        return (f"RunDataPoint(progress={self.progress}, set_angle={self.set_angle}, set_speed={self.set_speed}, "
                f"set_force={self.set_force}, millis_from_start={self.millis_from_start}, angle={self.angle}, "
                f"fn={self.fn}, ft={self.ft})")

class FullDataHeaders:
    _format = "4f 2B H I"
    _size = struct.calcsize(_format)

    def __init__(self, data: bytes):
        if len(data) != FullDataHeaders._size:
            raise ValueError(f"Data must be exactly {FullDataHeaders._size} bytes long")
        (self.rail_temperature, self.humidity, self.air_temperature, self.air_pressure, 
         self.rep, self.run, self.R1, self.length) = struct.unpack(FullDataHeaders._format, data)
    
    def __repr__(self):
        return (f"FullDataHeaders(rail_temperature={self.rail_temperature}, humidity={self.humidity}, "
                f"air_temperature={self.air_temperature}, air_pressure={self.air_pressure}, rep={self.rep}, "
                f"run={self.run}, length={self.length})")
    
class FullRunData:
    headers: FullDataHeaders
    points: list[RunDataPoint]
    def __init__(self, f:BinaryIO):
        self.headers = FullDataHeaders(f.read(FullDataHeaders._size))
        self.points = []
        for i in range(self.headers.length):
            self.points.append(RunDataPoint(f.read(RunDataPoint._size)))


class DataFile:
    offsets: tuple[int]
    full_data_offsets: tuple[int]
    metadata: MetaData
    summary: SummaryData
    tag_descriptions: list[str]
    means: list[MeanData]
    full_data: list[FullRunData]
    
    def __init__(self, filename: str):
        with open(filename, "rb") as f:
            self.offsets = struct.unpack(f"{5+N_TAGS}I", f.read((5+N_TAGS) * 4))
            f.seek(self.offsets[0])
            self.metadata = MetaData(f.read(MetaData._size))
            f.seek(self.offsets[1])
            self.summary = SummaryData(f.read(SummaryData._size))
            # read in tags
            self.tag_descriptions = []
            for i in range(N_TAGS):
                f.seek(self.offsets[i+2])
                self.tag_descriptions.append(f.read(self.metadata.tag_info_lengths[i]))
            
            # read in mean results
            self.means = []
            f.seek(self.offsets[N_TAGS+2])
            for i in range(self.metadata.n_mean_sections):
                self.means.append(MeanData(f.read(MeanData._size)))
            
            # read in the full data offsets
            f.seek(self.offsets[N_TAGS+3])
            n_full_sections = self.metadata.n_full_data_sections
            self.full_data_offsets = struct.unpack(f"{n_full_sections}I", f.read((n_full_sections) * 4))

            # read in the full data
            self.full_data = []
            for i in range(self.metadata.n_full_data_sections):
                f.seek(self.full_data_offsets[i])
                self.full_data.append(FullRunData(f))