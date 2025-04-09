import struct


def extract_bmd6_to_obj(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    # Header information
    magic_number = struct.unpack('<I', data[0x0:0x4])[0]
    header_offset = struct.unpack('<I', data[0x4:0x8])[0] # Path ends at 8 + header_offset

    unknowns_offset = 0x1a

    mesh_count = struct.unpack('<I', data[0x8 + header_offset + unknowns_offset:0x8 + header_offset + unknowns_offset + 4])[0]

    offset = 0xc + header_offset + unknowns_offset

    vertices = []

    faces = []

    # face_counts = [1222]
    face_counts = [6285, 1571]
    previous_vertices = 0

    for i in range(mesh_count):
        model_name_length = struct.unpack('<I', data[offset:offset + 4])[0]

        offset = offset + 4 + model_name_length

        material_length = struct.unpack('<I', data[offset:offset + 4])[0]

        offset = offset + 4 + 0x41 + material_length

        # scale_or_something_offset = 0x41

        # Example values - replace with your findings
        vertex_count = struct.unpack('<I', data[offset:offset + 4])[0]  # Example offset for count

        offset = offset + 12
        # vertex_offset = 0x18 + header_offset + unknowns_offset + model_name_length + material_length + scale_or_something_offset + 8  # Where vertex data begins

        # Extract vertices
        # vertices = []
        for j in range(vertex_count):
            x = struct.unpack('<f', data[offset:offset + 4])[0]
            y = struct.unpack('<f', data[offset + 4:offset + 8])[0]
            z = struct.unpack('<f', data[offset + 8:offset + 12])[0]
            vertices.append((x, y, z))
            offset += 12

        offset = offset + 4 + (24 * vertex_count)
        # face_offset = 0x78b9  # Where face indices begin
        # face_count = 1222
        # face_count = 6285 # Why? Needs to change for each model.
        # face_count = struct.unpack('<I', data[0x44:0x48])[0]  # Example offset for count

        face_count = face_counts[i]

        # Extract faces
        # faces = []
        for k in range(face_count):
            a = struct.unpack('<H', data[offset:offset + 2])[0] + 1 + previous_vertices  # +1 for OBJ indexing
            b = struct.unpack('<H', data[offset + 2:offset + 4])[0] + 1 + previous_vertices
            c = struct.unpack('<H', data[offset + 4:offset + 6])[0] + 1 + previous_vertices
            faces.append((a, b, c))
            offset = offset + 6  # Assuming 6 bytes per face (3 shorts)

        previous_vertices += vertex_count
        offset += 24 + 68

    # Write OBJ file
    with open(output_file, 'w') as f:
        f.write("# Extracted from " + input_file + "\n")
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")


extract_bmd6_to_obj("input/gun_emily.bmd6model", "output/test.obj")