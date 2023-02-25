# freecad-to-gltf

Experimental and work in progress glTF 2.0 exporter for FreeCAD.

Solves current limitations of FreeCAD's standard glTF exporter:
1. Doesn't export mirrored objects.
    * https://forum.freecad.org/viewtopic.php?t=76320
2. Doesn't respect `LinkTransform` `True` property for Links to App::Part.
    * https://forum.freecad.org/viewtopic.php?t=76323
3. Doesn't expose wires.
4. As of 0.20.2 FreeCAD's standard glTF exported isn't avaliable to Python headless.
    * However, this will be available in a future version:
    * https://forum.freecad.org/viewtopic.php?t=76348
