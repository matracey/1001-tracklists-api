from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """
    BaseSchema is a base class for data models that provides configuration for
    alias generation, population by name, and attribute-based initialization.

    Attributes:
        model_config (ConfigDict): Configuration dictionary that includes:
            - alias_generator: Function to generate aliases for fields.
            - populate_by_name: Boolean indicating if fields should be populated by name.
            - from_attributes: Boolean indicating if fields should be initialized from attributes.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
