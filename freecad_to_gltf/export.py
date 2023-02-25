import json
import struct
from base64 import b64encode
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from typing import List, Optional, Tuple

DATA_URI_HEADER = 'data:application/octet-stream;base64,'


@dataclass
class Asset:
    version: str


class AccessorType(Enum):
    """Specifies if the accessor's elements are scalars, vectors, or matrices.
    https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/schema/accessor.schema.json#L75-L103"""
    SCALAR = "SCALAR"
    VEC2 = "VEC2"
    VEC3 = "VEC3"
    VEC4 = "VEC4"
    MAT2 = "MAT2"
    MAT3 = "MAT3"
    MAT4 = "MAT4"


class ComponentType(Enum):
    """The datatype of the accessor's components.
    https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/schema/accessor.schema.json#L22-L61"""
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126


class Mode(Enum):
    """The topology type of primitives to render.
    https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/schema/mesh.primitive.schema.json#L27-L70
    """
    POINTS = 0
    LINES = 1
    LINE_LOOP = 2
    LINE_STRIP = 3
    TRIANGLES = 4
    TRIANGLE_STRIP = 5
    TRIANGLE_FAN = 6


@dataclass
class Attributes:
    POSITION: int
    NORMAL: Optional[int] = None


@dataclass
class Buffer:
    byteLength: int
    uri: str


@dataclass
class BufferView:
    buffer: int
    byteOffset: int
    byteLength: int
    target: int
    byteStride: Optional[int] = None


@dataclass
class Accessor:
    bufferView: int
    byteOffset: int
    type: AccessorType
    componentType: ComponentType
    count: int
    min: List[float]
    max: List[float]


@dataclass
class Primitive:
    attributes: Attributes
    indices: Optional[int] = None
    mode: Mode = Mode.TRIANGLES


@dataclass
class Mesh:
    primitives: List[Primitive]
    name: Optional[str] = None


@dataclass
class Node:
    """A node in the node hierarchy. 
    https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/schema/node.schema.json
    """
    mesh: int
    children: Optional[List[int]] = None
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)


@dataclass
class Scene:
    nodes: List[int]


def serialize(obj: object) -> str:
    if isinstance(obj, Enum):
        return obj.value
    else:
        return delete_keys_with_none_values(obj.__dict__)


@dataclass
class Gltf2:
    asset: Asset
    scene: int
    scenes: List[Scene]
    nodes: List[Node]
    meshes: List[Mesh]
    buffers: List[Buffer]
    bufferViews: List[BufferView]
    accessors: List[Accessor]

    def to_json(self) -> str:
        return json.dumps(
            self.__dict__,
            default=serialize)


def export_to_gltf(export_list: List[object]) -> str:
    # Create a simple triangle as embedded glTF:
    # https://github.com/KhronosGroup/glTF-Sample-Models/blob/master/2.0/Triangle/glTF-Embedded/Triangle.gltf
    indices = [0, 1, 2, 0]
    vertexes = [(0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0)]
    data = struct.pack('<4H9f', *indices, *chain.from_iterable(vertexes))
    buffer = str(b64encode(data).decode('utf-8'))
    uri = DATA_URI_HEADER + buffer
    return Gltf2(
        asset=Asset(version='2.0'),
        scene=0,
        scenes=[Scene(nodes=[0])],
        nodes=[Node(mesh=0)],
        meshes=[Mesh(primitives=[
            Primitive(Attributes(POSITION=1), indices=0)
        ])],
        buffers=[Buffer(byteLength=44, uri=uri)],
        bufferViews=[
            BufferView(buffer=0, byteOffset=0, byteLength=6, target=34963),
            BufferView(buffer=0, byteOffset=8, byteLength=36, target=34962)
        ],
        accessors=[
            Accessor(
                bufferView=0,
                byteOffset=0,
                componentType=ComponentType.UNSIGNED_SHORT,
                count=3,
                type=AccessorType.SCALAR,
                max=[2],
                min=[0]),
            Accessor(
                bufferView=1,
                byteOffset=0,
                componentType=ComponentType.FLOAT,
                count=3,
                type=AccessorType.VEC3,
                max=[1.0, 1.0, 0.0],
                min=[0.0, 0.0, 0.0]),
        ]
    ).to_json()


def delete_keys_with_none_values(dictionary):
    """Delete keys with the value ``None`` in a dictionary, recursively."""
    copy = dictionary.copy()
    for key, value in dictionary.items():
        if value is None:
            del copy[key]
        elif isinstance(value, dict):
            delete_keys_with_none_values(value)
    return copy
