# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: equipamentos.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x65quipamentos.proto\"\xec\x01\n\x07\x43ommand\x12$\n\x04type\x18\x01 \x01(\x0e\x32\x16.Command.EquipmentType\x12\x1f\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32\x0f.Command.Action\x12\x13\n\x0btemperature\x18\x03 \x01(\x02\"A\n\rEquipmentType\x12\x0b\n\x07LAMPADA\x10\x00\x12\x13\n\x0f\x41R_CONDICIONADO\x10\x01\x12\x0e\n\nSensorData\x10\x02\"B\n\x06\x41\x63tion\x12\x13\n\x0fSET_TEMPERATURE\x10\x00\x12\x06\n\x02ON\x10\x01\x12\x07\n\x03OFF\x10\x02\x12\x08\n\x04SAIR\x10\x03\x12\x08\n\x04NULL\x10\x04\"!\n\nSensorData\x12\x13\n\x0btemperature\x18\x01 \x01(\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'equipamentos_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_COMMAND']._serialized_start=23
  _globals['_COMMAND']._serialized_end=259
  _globals['_COMMAND_EQUIPMENTTYPE']._serialized_start=126
  _globals['_COMMAND_EQUIPMENTTYPE']._serialized_end=191
  _globals['_COMMAND_ACTION']._serialized_start=193
  _globals['_COMMAND_ACTION']._serialized_end=259
  _globals['_SENSORDATA']._serialized_start=261
  _globals['_SENSORDATA']._serialized_end=294
# @@protoc_insertion_point(module_scope)