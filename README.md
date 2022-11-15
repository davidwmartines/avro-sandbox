# Avro Sandbox

Experiments with evolving Avro schemas, using fastavro for serialization and deserialization.

## Purpose

Determine how Avro handles differences in writer and reader schemas.

From a reader schema perspective:

- Which differences with writer schema are allowed?

- Which differences with the writer schema would raise an error?

## Some Findings

1.  Adding a `default` value to a field makes it "optional".
    - A reader schema may include new fields, with defaults, and still be able to read data from the writer schema that does not have the field (reader made a backwards compatible change).
    - If the reader schema does not include a field that the writer has added and specified a default, the reader can still read it (writer made a forwards compatible change).

2.  Fields are considered "required" unless a `default` is specified.  
     - A reader cannot add a required field in a backwards-compatible manner. 
     - A reader can remove a required field in a backwards-compatible manner.
     - A writer may add a new required field and still be considered a forwards-compatible change.

3.  Setting a field's type to a union of "null" and one or more other types, means it is "nullable" (can contain `null`, i.e. `None` in Python), **but does not make it optional**.

## Run

```sh
pip install -r requirements.txt

pytest
```
