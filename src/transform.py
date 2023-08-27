import json
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

        # Extract timestamp and convert to RFC 3339 format
        timestamp = payload["t"]
        utc_time = datetime.datetime.utcfromtimestamp(timestamp).replace(
            tzinfo=datetime.timezone.utc
        )
        rfc3339_time = utc_time.isoformat()

        data = {}
        for reading in payload["r"]:
            vid = reading.pop("_vid", None)

            # Check for None values in the reading
            if vid and all(value is not None for value in reading.values()):
                # Clean the reading data by removing keys with '_' values or values that are NaN
                cleaned_reading = {
                    key: value
                    for key, value in reading.items()
                    if not key.startswith("_") and value is not None
                }

                if cleaned_reading:
                    data.setdefault(vid, {}).update(cleaned_reading)

        transformed_payload = {"time": rfc3339_time, "data": data}
        print("transformed=", json.dumps(transformed_payload, indent=2))
        return transformed_payload
    except Exception as e:
        logger.error("An error occurred in transform_payload: %s", e)


