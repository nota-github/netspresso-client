import pandas as pd
import yaml

from netspresso_real_client.modules.types import ReturnDataType


def encoder(json_data, output_format: ReturnDataType = ReturnDataType.JSON):
    if output_format == ReturnDataType.DATA_FRAME:
        retn = pd.DataFrame(json_data)
    elif output_format == ReturnDataType.JSON:
        retn = json_data
    elif output_format == ReturnDataType.YAML:
        retn = yaml.dump(json_data)
    else:
        raise RuntimeError(f'return type "{output_format}" is an invalid option')
    return retn