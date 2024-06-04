from typing import List, Type

from loguru import logger
import pandas as pd
from pydantic import BaseModel


class ModelUtils:
    @staticmethod
    def pydantic_list_to_pandas(list_of_objects: List[BaseModel], model: Type[BaseModel]):
        column_names = model.model_fields.keys()
        logger.debug(f"column names: {column_names}")
        return pd.DataFrame([c.model_dump() for c in list_of_objects], columns=column_names)

    @staticmethod
    def convert_pandas_to_pydantic(dataframe: pd.DataFrame, model: Type[BaseModel]):
        competencies = [model.model_validate(row) for row in dataframe.to_dict(orient="records")]
        return competencies
