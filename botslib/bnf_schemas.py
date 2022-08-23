from marshmallow import Schema, fields, pre_load, validate
from schemas.base_schema import BaseSchema


class BaseSchema(Schema):
    timestamp = fields.Int(required=True)
    signature = fields.Str()
    signal_provider = fields.Str(data_key="signalProvider", required=True)


class BaseQueryStringSchema(Schema):
    """
    Used for:
        /balance,
        /balance/total,
        /symbols
    """
    timestamp = fields.Int(required=True)
    signature = fields.Str()
    signal_provider = fields.Str(data_key="signalProvider", required=True)


class CancelOrderSchema(BaseSchema):
    """
    Used for:
        /orders/cancel
    """
    symbol = fields.Str(required=True)
    order_id = fields.Str(required=True, data_key="orderId")


class CreateOrderSchema(BaseSchema):
    """
    Used for:
        /orders/place
    """
    symbol = fields.Str(required=True, allow_none=False)
    quantity = fields.Float(required=True)
    price = fields.Str(required=True)
    side = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.OneOf(["SELL", "BUY"]),
    )

    @pre_load
    def massage_data(self, data, **kwargs):
        if "side" in data and data["side"]:
            data["side"] = data["side"].upper()

        if "symbol" in data and data["symbol"]:
            data["symbol"] = data["symbol"].upper()

        return data


class GetOrdersQueryStringSchema(BaseSchema):
    """
    Used for:
        /orders/list-open
    """
    symbol = fields.Str()
    since = fields.Int()
    limit = fields.Int(default=50, missing=50)


class GetOrderQueryStringSchema(BaseSchema):
    """
    Used for:
        /orders/status
    """
    symbol = fields.Str(required=True)
    order_id = fields.Str(data_key="orderId", required=True)


class BorrowRepaySchema(BaseSchema):
    """
    Used for:
        /loans/borrow,
        /loans/repay
    """
    amount = fields.Float(required=True)
    asset = fields.Str(required=True)
    symbol = fields.Str()
