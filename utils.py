from typing import Type
from sqlalchemy import asc, desc
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import ColumnElement


def get_ordering(
    model: Type[DeclarativeMeta],
    sort_by: str,
    order: str = "asc"
) -> ColumnElement:

    sort_column = getattr(model, sort_by, None)
    if sort_column is None:
        raise ValueError(f"Invalid sort_by field: {sort_by}")

    return asc(sort_column) if order.lower() == "asc" else desc(sort_column)
