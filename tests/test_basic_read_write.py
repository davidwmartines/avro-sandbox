from fastavro import reader, writer, parse_schema, schemaless_reader, schemaless_writer
from io import BytesIO


schema_1 = {
    "doc": "a test schema",
    "name": "Thing",
    "namespace": "test",
    "type": "record",
    "fields": [{"name": "f1", "type": "string"}],
}


def test_reader_can_read():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    writer(fo, writer_schema, [{"f1": "hello"}])
    fo.seek(0)

    for record in reader(fo, writer_schema):
        assert record["f1"] == "hello"


def test_schemaless_read_write():

    writer_schema = parse_schema(schema_1)

    fo = BytesIO()
    schemaless_writer(fo, writer_schema, {"f1": "hello"})
    fo.seek(0)

    record = schemaless_reader(
        fo, writer_schema=writer_schema, reader_schema=writer_schema
    )

    assert record["f1"] == "hello"
