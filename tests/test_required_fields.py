from io import BytesIO

import pytest
from fastavro import parse_schema, schemaless_reader, schemaless_writer
from fastavro._read_common import SchemaResolutionError

schema_1 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [{"name": "f1", "type": "string"}],
}


schema_2 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [
        {"name": "f1", "type": "string"},
        {"name": "f2", "type": "string"},
    ],
}


def test_required_field_writer_raises():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    with pytest.raises(ValueError):
        schemaless_writer(fo, writer_schema, {})


def test_add_required_field_reader_raises():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello"})
    fo.seek(0)

    reader_schema = parse_schema(schema_2)

    with pytest.raises(SchemaResolutionError):
        schemaless_reader(fo, writer_schema=writer_schema, reader_schema=reader_schema)


def test_remove_required_field():

    writer_schema = parse_schema(schema_2)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello", "f2": "world"})
    fo.seek(0)

    reader_schema = parse_schema(schema_1)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=reader_schema
    )

    assert record["f1"] == "hello"
    assert "f2" not in record
