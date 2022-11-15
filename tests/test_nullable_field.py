from io import BytesIO

import pytest
from fastavro import parse_schema, schemaless_reader, schemaless_writer
from fastavro._read_common import SchemaResolutionError

schema_1 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [{"name": "f1", "type": ["null", "string"]}],
}


schema_2 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [
        {"name": "f1", "type": ["null", "string"]},
        {"name": "f2", "type": ["null", "string"], "default": None},
    ],
}

schema_3 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [
        {"name": "f1", "type": ["null", "string"]},
        {"name": "f2", "type": ["null", "string"]},
    ],
}


def test_nullable_field_set_to_null():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": None})
    fo.seek(0)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=writer_schema
    )

    assert record["f1"] is None


def test_nullable_field_not_set():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {})
    fo.seek(0)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=writer_schema
    )

    assert record["f1"] is None


def test_nullable_field_in_reader():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello"})
    fo.seek(0)

    reader_schema = parse_schema(schema_2)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=reader_schema
    )

    assert record["f1"] == "hello"
    assert record["f2"] is None


def test_nullable_field_no_default_in_reader_raises():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello"})
    fo.seek(0)

    reader_schema = parse_schema(schema_3)

    # no default value for the new field... raises error on read
    with pytest.raises(SchemaResolutionError):
        schemaless_reader(fo, writer_schema=writer_schema, reader_schema=reader_schema)


def test_remove_nullable_field_in_reader():

    writer_schema = parse_schema(schema_3)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f2": "world"})
    fo.seek(0)

    reader_schema = parse_schema(schema_1)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=reader_schema
    )

    assert record["f1"] is None
    assert "f2" not in record
