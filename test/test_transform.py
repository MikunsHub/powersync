import json
import unittest

from src.transform import transform_payload


class TestTransformPayload(unittest.TestCase):
    def test_transform_valid_payload(self):
        payload = {
            "t": 1692979330,
            "r": [
                {
                    "_d": "logger",
                    "_vid": "strato-1",
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                },
                {
                    "_d": "logger_strato",
                    "_vid": "strato-1",
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                },
                {
                    "_d": "sma_stp_1",
                    "_vid": "60e0cc5f-2c90-4625-a3b0-0d72552ab3f4",
                    "I_L1": 0.007,
                    "I_L2": 0.025,
                    "P_L1": 0.0,
                    "P_L2": 0.0,
                    "P_L3": 0.0,
                    "freq": 50.07,
                    "status": 295,
                    "I_total": 0.064,
                    "P_total": 0.0,
                    "dc_in_P1": 0.0,
                    "total_yield": 84188413.0,
                    "temp_internal": 52.1,
                    "operating_mode": 1074,
                },
                {"_d": "sma_emeter", "_vid": "4294967295"},
                {"_d": "cg_meter_2", "_vid": "carlogavazzi-2"},
                {
                    "_d": "cg_meter_2",
                    "_vid": "carlogavazzi-3",
                    "temp_internal": 52.18,
                    "temp_internal_out": 0.0,
                },
                {
                    "_d": "holykell_pressure_sensor_1",
                    "_vid": "holykell-1",
                    "level": 0.6028432006835938,
                    "genset_fuel_level_percent": 27.527086789205196,
                    "genset_fuel_volume": 881.6581809997559,
                },
            ],
            "m": {"snap_rev": 894, "reading_duration": 131.1362009048462},
        }
        transformed_payload = transform_payload(json.dumps(payload))
        expected_output = {
            "time": "2023-08-25T16:02:10+00:00",
            "data": {
                "strato-1": {
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                },
                "60e0cc5f-2c90-4625-a3b0-0d72552ab3f4": {
                    "I_L1": 0.007,
                    "I_L2": 0.025,
                    "P_L1": 0.0,
                    "P_L2": 0.0,
                    "P_L3": 0.0,
                    "freq": 50.07,
                    "status": 295,
                    "I_total": 0.064,
                    "P_total": 0.0,
                    "dc_in_P1": 0.0,
                    "total_yield": 84188413.0,
                    "temp_internal": 52.1,
                    "operating_mode": 1074,
                },
                "carlogavazzi-3": {"temp_internal": 52.18, "temp_internal_out": 0.0},
                "holykell-1": {
                    "level": 0.6028432006835938,
                    "genset_fuel_level_percent": 27.527086789205196,
                    "genset_fuel_volume": 881.6581809997559,
                },
            },
        }
        self.assertEqual(transformed_payload, expected_output)

    def test_transform_payload_with_null_values(self):
        payload = {
            "t": 1692979330,
            "r": [
                {
                    "_d": "logger",
                    "_vid": "strato-1",
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                },
                {
                    "_d": "logger_strato",
                    "_vid": "strato-1",
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                },
                {
                    "_d": "sma_stp_1",
                    "_vid": "60e0cc5f-2c90-4625-a3b0-0d72552ab3f4",
                    "S_L1": 2.0,
                    "S_L2": 6.0,
                    "S_L3": None,
                },
            ],
            "m": {"snap_rev": 894, "reading_duration": 131.1362009048462},
        }
        transformed_payload = transform_payload(json.dumps(payload))
        expected_output = {
            "time": "2023-08-25T16:02:10+00:00",
            "data": {
                "strato-1": {
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                }
            },
        }

        self.assertEqual(transformed_payload, expected_output)

    def test_transform_payload_with_same_vids(self):
        payload = {
            "t": 1692979330,
            "r": [
                {
                    "_d": "logger",
                    "_vid": "strato-1",
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                },
                {
                    "_d": "logger_strato",
                    "_vid": "strato-1",
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                }
            ],
            "m": {"snap_rev": 894, "reading_duration": 131.1362009048462},
        }
        transformed_payload = transform_payload(json.dumps(payload))
        expected_output = {
            "time": "2023-08-25T16:02:10+00:00",
            "data": {
                "strato-1": {
                    "cpu_load": 0.0,
                    "boot_time": 1692964810.0,
                    "memory_usage": 17.5,
                    "cpu_temp": 66.604,
                    "disk_usage": 30.3,
                }
            },
        }

        self.assertEqual(transformed_payload, expected_output)

    def test_missing_t_key(self):
        payload = {"r": []}
        payload_json = json.dumps(payload)
        result = transform_payload(payload_json)
        self.assertIsNone(result)

    def test_missing_r_key(self):
        payload = {"t": 1692979330}
        payload_json = json.dumps(payload)
        result = transform_payload(payload_json)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
