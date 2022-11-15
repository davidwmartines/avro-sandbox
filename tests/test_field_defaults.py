from io import BytesIO

import pytest
from fastavro import parse_schema, schemaless_reader, schemaless_writer
from fastavro._read_common import SchemaResolutionError

schema_1 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [{"name": "f1", "type": "string", "default": "foo"}],
}


schema_2 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [
        {"name": "f1", "type": "string", "default": "foo"},
        {"name": "f2", "type": "string", "default": "bar"},
    ],
}


def test_default_field_read():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {})
    fo.seek(0)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=writer_schema
    )

    assert record["f1"] == "foo"


def test_add_default_field_read():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello"})
    fo.seek(0)

    reader_schema = parse_schema(schema_2)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=reader_schema
    )

    assert record["f1"] == "hello"
    assert record["f2"] == "bar"


def test_remove_default_field_read():

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
