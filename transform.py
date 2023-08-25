import json
import math
import datetime
import logging

logger = logging.getLogger(__name__)


def transform_payload(payload_json: str) -> dict:
    """
    Transform the input MQTT payload from JSON format to a structured data pipeline format.

    Args:
        payload_json (str): JSON payload to be transformed.

    Returns:
        dict: Transformed payload in a structured format.
    """
    try:
        # Load the JSON payload
        payload = json.loads(payload_json)
        # print("untransformed=", json.dumps(payload, indent=2))

        # Extract timestamp and convert to RFC 3339 format
        timestamp = payload["t"]
        utc_time = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
        rfc3339_time = utc_time.isoformat()
        print(rfc3339_time)

        data = {}
        for reading in payload["r"]:
            vid = reading.pop("_vid", None)
            if vid:
                # Clean the reading data by removing keys starting with "_" and None values
                cleaned_reading = {
                    key: value
                    for key, value in reading.items()
                    if not key.startswith("_") and value is not None
                }
                if all(
                    isinstance(v, float) and not math.isnan(v)
                    for v in cleaned_reading.values()
                ):
                    data.setdefault(vid, {}).update(cleaned_reading)

        transformed_payload = {"time": rfc3339_time, "data": data}

        return transformed_payload
    except Exception as e:
        logger.error("An error occurred in transform_payload: %s", e)
